"""Evaluation-only input provenance, configuration, and single-use heldout gates."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIELDS=('deadline','amount_due','required_action','contact')


def safe_path(folder,name):
    path=(folder/name).resolve()
    if not path.is_relative_to(folder.resolve()) or path.suffix not in {'.json','.png','.jpg','.jpeg','.webp'}:
        raise ValueError('Unsafe evaluation input path')
    return path


def load_set(name,root=ROOT):
    # Caller MUST acquire the heldout gate before calling with name=heldout.
    folder=root/'eval'/('heldout' if name=='heldout' else 'm4/'+name)
    manifest=json.loads((folder/'manifest.json').read_text())
    if manifest.get('synthetic') is not True:raise ValueError('Only declared synthetic evaluation inputs are allowed')
    items=[];seen=set()
    for filename in manifest['samples']:
        path=safe_path(folder,filename)
        if path.name=='expected-fields.template.json':raise ValueError('Template is not a heldout sample')
        item=json.loads(path.read_text())
        if item.get('synthetic') is not True or item['id'] in seen:raise ValueError('Non-synthetic/duplicate sample')
        if set(item['expected'])!=set(FIELDS):raise ValueError('Expected four field annotations')
        if item['doc_type'] not in {'parking_ticket','court_notice','utility_bill','school_letter','unknown'}:raise ValueError('Unknown type annotation')
        item.setdefault('expected_state',{key:'present' if value is not None else 'missing' for key,value in item['expected'].items()})
        for variant in item['variants']:
            variant['resolved_image']=str(safe_path(folder,variant['image']))
        item['_annotation_path']=str(path);seen.add(item['id']);items.append(item)
    return items


def source_fingerprint(root=ROOT):
    # Intentionally never traverses eval/heldout or .env, including for hashing.
    paths=[]
    for folder in ['backend','frontend','tests']:
        paths.extend(p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    paths.extend((root/'eval').glob('*.py'))
    paths.extend([root/'eval/m4-config.json',root/'requirements.txt'])
    digest=hashlib.sha256()
    for path in sorted(paths):
        if path.exists():digest.update(str(path.relative_to(root)).encode()+b'\0'+path.read_bytes())
    return digest.hexdigest()


def acquire_heldout(root,config):
    # No heldout directory/file is read before code freeze verification succeeds.
    tag=subprocess.run(['git','rev-parse','eval-freeze^{commit}'],cwd=root,capture_output=True,text=True)
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
    if tag.returncode or head.returncode or tag.stdout.strip()!=head.stdout.strip():
        raise ValueError('Heldout requires HEAD at eval-freeze; no test inputs were read')
    freeze_path=root/'eval/freeze.json'
    if not freeze_path.exists():raise ValueError('Missing freeze manifest; no test inputs were read')
    freeze=json.loads(freeze_path.read_text())
    if freeze['source_sha256']!=source_fingerprint(root):raise ValueError('Code/config changed after freeze')
    if config['repeats']!=1:raise ValueError('Heldout permits one run, not repeated variance runs')
    ledger=root/'eval/heldout-run-started.json'
    try:
        with ledger.open('x') as handle:
            json.dump({'status':'started_do_not_rerun','freeze_commit':head.stdout.strip(),
                       'source_sha256':freeze['source_sha256']},handle,indent=2)
    except FileExistsError:raise ValueError('Heldout was already started; refusing another attempt') from None
    return ledger


def corpus_fingerprint(items):
    digest=hashlib.sha256()
    for item in items:
        digest.update(Path(item['_annotation_path']).read_bytes())
        for variant in item['variants']:digest.update(Path(variant['resolved_image']).read_bytes())
    return digest.hexdigest()
