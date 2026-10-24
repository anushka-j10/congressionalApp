"""Proposed scorer/protocol regressions, never opening actual heldout files."""
import json
from datetime import date
from pathlib import Path
from unittest.mock import Mock
from types import SimpleNamespace
import pytest
from eval.protocol import load_set,safe_path,source_fingerprint,acquire_heldout,FIELDS
from eval.scoring import score_field,score_row,summarize
from backend.extraction import ModelExtractor
from backend.structured_model import StructuredModel
from backend.explanation_models import PlainTranslation
from tests.test_extract import provider,response,envelope


def test_wrong_verified_is_counted_even_when_source_might_contain_decoy():
    result=score_field('amount_due','85.20','present',{'value':'$15.00','status':'verified'})
    assert result['false_verified'] and not result['flagged_wrong']


def test_wrong_flagged_and_provider_failure_are_different():
    flagged=score_field('deadline','2026-11-04','present',{'value':'2026-11-14','status':'unverified'})
    assert flagged['flagged_wrong'] and not flagged['false_verified']
    unavailable=score_field('deadline','2026-11-04','present',{},unavailable=True)
    assert unavailable['unavailable'] and not unavailable['flagged_wrong'] and not unavailable['false_verified']


def test_missing_and_ambiguous_have_separate_denominators():
    absent=score_field('deadline',None,'missing',{'value':None,'status':'missing'})
    uncertain=score_field('deadline',None,'ambiguous',{'value':None,'status':'missing'})
    wrong=score_field('deadline',None,'ambiguous',{'value':'2026-11-04','status':'verified'})
    assert absent['correct_to_say_missing'] and not uncertain['correct_to_say_missing']
    assert wrong['false_verified']


def test_correct_but_flagged_is_not_usable_verified_accuracy():
    result=score_field('amount_due','45.00','present',{'value':'$45.00','status':'unverified'})
    assert result['correct_value_present'] and not result['usable_verified_correct']


def test_text_scoring_tolerates_layout_not_paraphrase():
    assert score_field('required_action','Return the form.','present',{'value':'Return\n the form.','status':'verified'})['usable_verified_correct']
    assert score_field('required_action','Return the form.','present',{'value':'Do nothing.','status':'verified'})['false_verified']


def test_invalid_calendar_or_decimal_is_not_normalized_into_truth():
    assert score_field('deadline','2026-11-03','present',{'value':'2026-03-11','status':'verified'})['false_verified']
    assert score_field('amount_due','45.00','present',{'value':'($45.00)','status':'verified'})['false_verified']


def test_relative_source_alias_is_explicit_annotation_not_scoring_inference():
    result=score_field('deadline','2026-11-19','present',{'value':'within 30 days of the date above.','status':'verified'},['within 30 days of the date above.'])
    assert result['usable_verified_correct']
    assert score_field('deadline','2026-11-19','present',{'value':'within 13 days','status':'verified'})['false_verified']


def test_aggregate_denominators_and_variance():
    records=[]
    for rep in [1,2,3]:
        fields={name:{'value':'$45.00' if name=='amount_due' else None,'status':'verified' if name=='amount_due' else 'missing'} for name in FIELDS}
        if rep==3:fields['amount_due']['value']='$99.00'
        records.append({'expected':{'deadline':None,'amount_due':'45.00','required_action':None,'contact':None},
          'expected_state':{name:'present' if name=='amount_due' else 'missing' for name in FIELDS},'repetition':rep,
          'methods':{mode:{'fields':fields} for mode in ['B1','B2','full']}})
    result=summarize(records)['full']['headline_critical']
    assert result['false_verified_rate']=={'n':1,'d':9,'rate':1/9}
    assert result['wrong_among_verified']=={'n':1,'d':3,'rate':1/3}
    assert result['field_accuracy']['n']==2 and result['correct_to_say_missing']['d']==6


def test_dev_and_adversarial_input_integrity():
    dev=load_set('dev');attacks=load_set('adversarial')
    assert len(dev)==20 and len(attacks)==8
    assert sum(item['doc_type']=='unknown' for item in dev)==1
    for item in dev+attacks:
        assert len(item['variants'])==2
        for variant in item['variants']:assert Path(variant['resolved_image']).is_file()
        for name,value in item['expected'].items():
            if value is not None and name in {'required_action','contact'}:
                if 'multi_page' not in item.get('edge_cases',[]):assert ' '.join(value.split()) in ' '.join(item['text'].split())


def test_safe_path_blocks_escape(tmp_path):
    with pytest.raises(ValueError):safe_path(tmp_path,'../.env')


def test_freeze_gate_refuses_before_reading_heldout(tmp_path,monkeypatch):
    monkeypatch.setattr('eval.protocol.subprocess.run',lambda *a,**k:SimpleNamespace(returncode=1,stdout=''))
    assert not (tmp_path/'eval/heldout').exists()
    with pytest.raises(ValueError):acquire_heldout(tmp_path,{'repeats':1})
    assert not (tmp_path/'eval/heldout-run-started.json').exists()


def test_source_fingerprint_does_not_traverse_heldout(tmp_path):
    (tmp_path/'eval/heldout').mkdir(parents=True)
    (tmp_path/'eval/heldout/private.json').write_text('do not read')
    first=source_fingerprint(tmp_path)
    (tmp_path/'eval/heldout/private.json').write_text('changed')
    assert source_fingerprint(tmp_path)==first


def test_evaluation_generation_settings_are_sent_without_changing_defaults(monkeypatch):
    post=provider(monkeypatch,[response(envelope())])
    ModelExtractor('fake-only','pinned',temperature=0,reasoning_effort='none').extract('text','parking_ticket')
    body=post.call_args.kwargs['json']
    assert body['temperature']==0 and body['reasoning']=={'effort':'none'}
    post=provider(monkeypatch,[response(envelope())])
    ModelExtractor('fake-only','pinned').extract('text','parking_ticket')
    assert 'temperature' not in post.call_args.kwargs['json']


@pytest.mark.parametrize('phrase',['Not specified','No payment is requested.','Not stated'])
def test_explicit_absence_claim_is_not_a_wrong_amount_when_truth_is_absent(phrase):
    result=score_field('amount_due',None,'missing',{'value':phrase,'status':'verified'})
    assert not result['false_verified'] and result['correct_to_say_missing']
    assert score_field('amount_due','45.00','present',{'value':phrase,'status':'verified'})['false_verified']


def test_contact_alias_is_explicit_and_does_not_credit_other_destinations():
    good=score_field('contact','Fictional help desk; only testing','present',{'value':'Fictional help desk','status':'verified'},['Fictional help desk'])
    bad=score_field('contact','Fictional help desk; only testing','present',{'value':'MALICIOUS-DEMO','status':'verified'},['Fictional help desk'])
    assert good['usable_verified_correct'] and bad['false_verified']



def test_cost_uses_reported_tokens_and_does_not_double_count_shared_proposal():
    from eval.scoring import usage_cost,method_usage
    rates={'usd_per_million_input':1,'usd_per_million_cached_input':0.1,'usd_per_million_output':2}
    assert usage_cost({'input_tokens':1000,'cached_input_tokens':200,'output_tokens':100},rates)==0.00102
    row={'selected_type':'parking_ticket','extraction_usage':{'input_tokens':100},
       'language_usage_including_B1':{'input_tokens':500},'methods':{'B1':{'usage':{'input_tokens':200}}}}
    assert method_usage(row,'full')['input_tokens']==400
    assert method_usage(row,'B2')['input_tokens']==100
    assert method_usage(row,'B1')['input_tokens']==200
