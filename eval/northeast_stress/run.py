"""Opt-in live exploratory run. Sends ONLY synthetic OCR text to the configured model.

This calls the same process_photo/extract_and_verify/explain_notice functions as
the app. It is a component integration run, not a deployed/mobile/browser test.
No production code, frozen set, prompt, validator or answer is changed here.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import subprocess
import time
from types import SimpleNamespace

from dotenv import dotenv_values
from backend.main import process_photo
from backend.readers import make_reader
from backend.extraction import extract_and_verify
from backend.explanation import explain_notice
from backend.structured_model import StructuredModel
from eval.engine import CaptureExtractor
from eval.scoring import score_field, aggregate, VERSION, FIELDS
from .build import DATA, ROOT

OUT = ROOT / 'results' / 'northeast-stress'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def app_hash():
    digest=hashlib.sha256()
    for folder in ('backend','frontend'):
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                digest.update(str(p.relative_to(ROOT)).encode());digest.update(p.read_bytes())
    return digest.hexdigest()

def load_corpus():
    m=json.loads((DATA/'manifest.json').read_text())
    if not m['synthetic'] or m['independent_heldout']:raise ValueError('Wrong corpus')
    for name,expected in m['files'].items():
        p=DATA/name
        if p.parent != DATA or sha(p)!=expected:raise ValueError('Corpus integrity failure')
    items=[json.loads((DATA/name).read_text()) for name in m['cases']]
    if len(items)!=18 or any(not c['synthetic'] for c in items):raise ValueError('Wrong corpus size')
    return m,items

def run_one(item,variant,config,key,tesseract):
    started=time.monotonic()
    row={'sample':item['id'],'state':item['state'],'variant':variant['name'],
         'issuer':item['issuer'],'input_image':variant['image'],
         'expected':item['expected'],'expected_state':item['expected_state'],
         'expected_aliases':item['expected_aliases'],'challenges':item['challenges'],
         'selected_type':'parking_ticket','human_amount_review':False,'stages':{}}
    options={'temperature':config['temperature'],'reasoning_effort':config['reasoning_effort']}
    extractor=CaptureExtractor(key,config['model'],**options)
    model=StructuredModel(key,config['model'],**options)
    try:
        stage=time.monotonic()
        reader=make_reader(SimpleNamespace(reader=config['reader'],tesseract_command=tesseract,api_key=key,model=config['model']))
        row['reading']=process_photo((DATA/variant['image']).read_bytes(),reader)
        row['stages']['read_ms']=round((time.monotonic()-stage)*1000,2)
    except Exception:
        row['error']='reader_unavailable'
    if not row.get('error'):
        try:
            stage=time.monotonic()
            row['extraction']=extract_and_verify(row['reading']['text'],'parking_ticket',extractor,date.fromisoformat(config['today']),False)
            row['stages']['extract_ms']=round((time.monotonic()-stage)*1000,2)
            row['proposal']=extractor.last.proposed.model_dump()
        except Exception:
            row['error']='extraction_unavailable'
    if not row.get('error'):
        try:
            stage=time.monotonic()
            row['explanation']=explain_notice(row['extraction']['fields'],'parking_ticket','en',model)
            row['stages']['explain_ms']=round((time.monotonic()-stage)*1000,2)
        except Exception:
            row['explanation_error']='explanation_unavailable'
    row['language_usage']=dict(model.stats)
    row['extraction_usage']=extractor.last.usage if extractor.last else {}
    row['latency_ms']=round((time.monotonic()-started)*1000,2)
    fields=row.get('extraction',{}).get('fields',{})
    row['scores']={'full':{name:score_field(name,item['expected'][name],item['expected_state'][name],
        fields.get(name,{}),item['expected_aliases'].get(name,[]),bool(row.get('error'))) for name in FIELDS}}
    row['case_pass']=not row.get('error') and not row.get('explanation_error') and all(not s['wrong'] for s in row['scores']['full'].values())
    return row

def summarize(rows):
    summary={'cases':len(rows),'case_pass':sum(r['case_pass'] for r in rows),
        'all_fields':aggregate(rows,'full'),
        'critical':aggregate(rows,'full',('deadline','amount_due','required_action')),
        'per_field':{n:aggregate(rows,'full',(n,)) for n in FIELDS},
        'per_state':{s:aggregate([r for r in rows if r['state']==s],'full') for s in sorted({r['state'] for r in rows})},
        'per_variant':{v:aggregate([r for r in rows if r['variant']==v],'full') for v in sorted({r['variant'] for r in rows})}}
    values=[s for r in rows for s in r['scores']['full'].values()]
    summary['all_opportunity_correct']=sum(not s['wrong'] for s in values)
    summary['all_opportunity_total']=len(values)
    summary['missing_or_unverified']=sum(s['status'] in {'missing','unverified'} and not s['unavailable'] for s in values)
    summary['classification_correct']=sum(r.get('reading',{}).get('doc_type')=='parking_ticket' for r in rows)
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--resume',action='store_true');p.add_argument('--dry-run',action='store_true');args=p.parse_args()
    manifest,items=load_corpus();jobs=[(i,v) for i in items for v in i['variants']]
    if args.dry_run:
        print(f'Integrity OK: {len(items)} notices, {len(jobs)} images, 9 states. No API calls.');return
    OUT.mkdir(exist_ok=True,parents=True)
    snapshot={'started_at':datetime.now(timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'application_sha256':app_hash(),'manifest_sha256':sha(DATA/'manifest.json'),
        'config':manifest['protocol'],'scorer':VERSION,'planned_cases':len(jobs)}
    ledger=OUT/'records.jsonl';meta=OUT/'run.json'
    if meta.exists():
        if not args.resume:raise ValueError('Output already exists; refusing another run')
        old=json.loads(meta.read_text())
        if any(old[k]!=snapshot[k] for k in ['application_sha256','manifest_sha256','config','scorer']):raise ValueError('Resume fingerprint mismatch')
        snapshot=old
    elif args.resume:raise ValueError('No run to resume')
    else:
        with meta.open('x') as f:json.dump(snapshot,f,indent=2)
    rows=[json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
    done={(r['sample'],r['variant']) for r in rows}
    jobs=[(i,v) for i,v in jobs if (i['id'],v['name']) not in done]
    # Secret is read in-process and never serialized, logged, put on a command line,
    # or copied into any output. Only the standard provider clients receive it.
    env=dotenv_values(ROOT/'.env');key=os.environ.get('OPENAI_API_KEY') or env.get('OPENAI_API_KEY','')
    tesseract=os.environ.get('TESSERACT_CMD') or env.get('TESSERACT_CMD') or 'tesseract'
    if not key:raise ValueError('Key not configured')
    logging.getLogger('httpx').setLevel(logging.WARNING)
    def save(row):
        # Defense in depth: never persist a credential even if a lower layer changes.
        encoded=json.dumps(row,ensure_ascii=False)
        if key in encoded:raise ValueError('Secret detected; output refused')
        with ledger.open('a') as f:f.write(encoded+'\n');f.flush()
        rows.append(row)
        print(f'{len(rows)}/36 {row["sample"]} {row["variant"]}: '+('PASS' if row['case_pass'] else 'FAIL'),flush=True)
    # First case is a real measurement, not a separate preflight that is rerun.
    if jobs and not rows:
        item,variant=jobs.pop(0);first=run_one(item,variant,manifest['protocol'],key,tesseract);save(first)
        if first.get('error'):raise ValueError('First pipeline request failed; additional calls stopped')
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending=[pool.submit(run_one,i,v,manifest['protocol'],key,tesseract) for i,v in jobs]
        for task in as_completed(pending):save(task.result())
    if app_hash()!=snapshot['application_sha256']:raise ValueError('Application changed during run')
    rows.sort(key=lambda r:(r['sample'],r['variant']))
    result=dict(snapshot,completed_at=datetime.now(timezone.utc).isoformat(),records=rows,summary=summarize(rows))
    serialized=json.dumps(result,indent=2,ensure_ascii=False)
    if key in serialized:raise ValueError('Secret detected; output refused')
    (OUT/'results.json').write_text(serialized+'\n')
    print(json.dumps(result['summary'],indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,FileNotFoundError,KeyError,json.JSONDecodeError):
        raise SystemExit('Stress run stopped safely. Check corpus integrity/configuration or existing results; no provider details logged.') from None
