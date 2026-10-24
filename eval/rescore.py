"""Rebuild dev/adversarial tables from saved outputs; no model calls or heldout access."""
import argparse
import hashlib
import json
from pathlib import Path
from eval.protocol import load_set,corpus_fingerprint
from eval.scoring import VERSION,summarize,markdown


def output_hash(report):
    data=[{key:row.get(key) for key in ['sample','variant','repetition','reading','extraction','proposal','methods','language_usage_including_B1','extraction_usage']} for row in report['records']]
    return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def rescore(source,destination):
    if destination.exists():raise ValueError('Refusing to overwrite an artifact')
    report=json.loads(source.read_text())
    if report['set'] not in {'dev','adversarial'} or report['status']!='completed':
        raise ValueError('Only completed development experiments can be rescored here')
    before=output_hash(report)
    items=load_set(report['set']);annotations={item['id']:item for item in items}
    config=json.loads(Path(__file__).with_name('m4-config.json').read_text())
    if config['model']==report['config']['model']: report['cost_basis']=config['cost']
    report['initial_summary']=report['summary']
    report['initial_scorer_version']=report['scorer_version']
    report['scorer_version']=VERSION
    report['inference_corpus_sha256']=report['corpus_sha256']
    report['scoring_corpus_sha256']=corpus_fingerprint(items)
    report['scoring_revision']={'reason':'Explicit numeric-field absence is not a wrong numeric fact. Contact-name-only aliases omit a testing disclaimer, not contact facts. Static all-missing language bundles have vacuous numeric/glossary agreement.',
        'pipeline_changed':False,'model_calls_repeated':False,'original_artifact':str(source),
        'scoring_code_sha256':hashlib.sha256(Path(__file__).with_name('scoring.py').read_bytes()).hexdigest()}
    for row in report['records']:
        item=annotations[row['sample']]
        if item['expected']!=row['expected'] or item['expected_state']!=row['expected_state']:
            raise ValueError('Expected field values/states changed; manual audit required')
        row['expected_aliases']=item.get('expected_aliases',{})
    report['summary']=summarize(report['records'])
    assert output_hash(report)==before,'Model output changed during scoring'
    report['inference_output_sha256']=before
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    destination.with_suffix('.md').write_text(markdown(report))
    print(destination)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();rescore(args.input,args.out)
