"""Opt-in synthetic evaluation: python -m eval.run --set dev --out results/dev.json."""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor,as_completed
from dotenv import dotenv_values
from eval.protocol import ROOT,load_set,source_fingerprint,corpus_fingerprint,acquire_heldout
from eval.scoring import VERSION,summarize,markdown


def save(path,report):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.pending')
    temp.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');temp.replace(path)
    if report.get('summary'):path.with_suffix('.md').write_text(markdown(report))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--set',choices=['dev','adversarial','heldout'],default='dev')
    parser.add_argument('--out',type=Path,default=Path('results/dev.json'))
    parser.add_argument('--config',type=Path,default=ROOT/'eval/m4-config.json')
    parser.add_argument('--env-file',type=Path,default=ROOT/'.env')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--limit',type=int,help='Diagnostic subset; report is explicitly partial')
    parser.add_argument('--repeats',type=int)
    args=parser.parse_args()
    config=json.loads(args.config.read_text())
    if args.repeats is not None:config['repeats']=args.repeats
    if args.set=='heldout':
        if args.resume or args.dry_run or args.limit or args.repeats not in {None,1}:
            raise ValueError('Heldout has no diagnostic, resume or repeated-run mode')
        config['repeats']=1
        acquire_heldout(ROOT,config)
    if config['repeats']<1 or config['workers'] not in {1,2,3,4}:raise ValueError('Invalid run configuration')
    items=load_set(args.set)
    if args.set=='heldout' and len(items)!=config['protocol']['heldout_required_count']:
        raise ValueError('Heldout must contain ten samples; attempt consumed, do not rerun')
    fingerprint=source_fingerprint()
    corpus=corpus_fingerprint(items)
    expected_count=sum(len(item['variants']) for item in items)*config['repeats']
    if args.dry_run:
        print(json.dumps({'set':args.set,'sample_count':len(items),'planned_records':expected_count,
                          'code_sha256':fingerprint,'corpus_sha256':corpus,'no_api_calls':True},indent=2));return
    if args.out.resolve().is_relative_to((ROOT/'frontend').resolve()):raise ValueError('Reports must not be publicly served')
    values=dotenv_values(args.env_file) if args.env_file.exists() else {}
    key=os.environ.get('OPENAI_API_KEY') or values.get('OPENAI_API_KEY')
    if not key:raise ValueError('Configure the private backend credential before running')
    tesseract=os.environ.get('TESSERACT_CMD') or values.get('TESSERACT_CMD') or 'tesseract'
    report={'version':'m4-v1','scorer_version':VERSION,'set':args.set,
      'run_date':datetime.now(ZoneInfo('America/New_York')).date().isoformat(),
      'config':config,'cost_basis':config['cost'],'code_sha256':fingerprint,'corpus_sha256':corpus,
      'planned_records':expected_count,'status':'running','records':[]}
    if args.out.exists():
        if not args.resume:raise ValueError('Output already exists; use a new name or explicit dev/adversarial resume')
        old=json.loads(args.out.read_text())
        if any(old[name]!=report[name] for name in ['set','config','code_sha256','corpus_sha256']):
            raise ValueError('Resume refuses changed code/config/corpus')
        report=old;report['status']='running'
    elif args.resume:raise ValueError('No report to resume')
    done={(row['sample'],row['variant'],row['repetition']) for row in report['records']}
    jobs=[(item,variant,rep) for rep in range(1,config['repeats']+1) for item in items
          for variant in item['variants'] if variant['name'] in config['variants'] and
          (item['id'],variant['name'],rep) not in done]
    if args.limit is not None:jobs=jobs[:args.limit]
    save(args.out,report)
    from eval.engine import run_notice
    with ThreadPoolExecutor(max_workers=config['workers']) as executor:
        pending={executor.submit(run_notice,item,variant,rep,config,key,tesseract):(item,variant,rep) for item,variant,rep in jobs}
        for future in as_completed(pending):
            item,variant,rep=pending[future]
            try:row=future.result()
            except Exception:
                row={'sample':item['id'],'variant':variant['name'],'repetition':rep,
                     'expected':item['expected'],'expected_state':item['expected_state'],
                     'error':'evaluation_request_failed','methods':{}}
            report['records'].append(row)
            report['summary']=summarize(report['records']);save(args.out,report)
            print(f"{len(report['records'])}/{expected_count} {item['id']} {variant['name']} repeat={rep} complete",flush=True)
    report['status']='completed' if len(report['records'])==expected_count else 'partial_diagnostic'
    report['summary']=summarize(report['records']);save(args.out,report)
    print(markdown(report))


if __name__=='__main__':
    try:main()
    except (ValueError,FileNotFoundError,KeyError,json.JSONDecodeError) as error:
        # Never include arbitrary provider/body/credential exception strings.
        print('Evaluation stopped: configuration, input, freeze gate or existing-output check failed. No result was fabricated.',file=sys.stderr)
        sys.exit(2)
