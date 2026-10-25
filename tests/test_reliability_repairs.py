"""New development controls; never access or replay student held-out inputs."""
from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from backend.extraction_models import ProposedField, ProposedDeadline, ParkingTicket
from backend.field_validation import checked_field, parse_date
from backend.extraction import extract_and_verify, ExtractionResult
from backend.preprocessed_reader import PreprocessedReader
from backend.readers import Reading, ReaderError
from eval.scoring import score_field
from tests.test_extract import api, request, proposed_dict, TEXT

TODAY = date(2027, 2, 1)


def absolute(value, source):
    return ProposedDeadline(value=value,source_snippet=source,kind='absolute',relative_days=None,anchor_date=None,anchor_source_snippet=None)


@pytest.mark.parametrize('value,source',[
 ('February 18, 2027','Pay $68.40 on or before February 18, 2027.'),
 ('Thursday, February 18, 2027','Appear in Courtroom 7 at 10:15 AM on Thursday, February 18, 2027.'),
 ('02/18/2027','Send the $68.40 fee by 02/18/2027.'),
 ('2027-02-18','Due date: 2027-02-18.'),
])
def test_complete_labeled_date_context_allows_other_typed_values(value,source):
    field=checked_field('deadline',absolute(value,source),source,TODAY)
    assert field.status=='verified' and field.normalized_value=='2027-02-18'


@pytest.mark.parametrize('source',[
 'Deadline: February 18, 2027 or February 25, 2027.',
 'Deadline: February 18, 2027. Reference 887.',
 'Pay $68.O0 by February 18, 2027.',
 'Appear at 37:91 AM on February 18, 2027.',
 'Appear on Monday, February 18, 2027.',
])
def test_typed_context_does_not_ignore_invalid_or_unrelated_digits(source):
    assert checked_field('deadline',absolute('2027-02-18',source),source,TODAY).status=='unverified'


@pytest.mark.parametrize('source',[
 'Pay the current $68.40 balance by February 18, 2027.',
 'Pay the current $68.40 balance by 02/18/2027.',
])
def test_current_amount_may_share_its_sentence_with_a_date(source):
    f=checked_field('amount_due',ProposedField(value='$68.40',source_snippet=source),source,TODAY)
    assert f.status=='verified' and f.normalized_value=='68.40'


@pytest.mark.parametrize('source',[
 'Pay $68.40 or $99.00 by February 18, 2027.',
 'Amount due: $68.40; reference 887.',
 'Pay ($68.40) by February 18, 2027.',
 'Pay $68.40 by 02/1O/2027.',
])
def test_amount_context_still_rejects_competing_or_corrupted_numbers(source):
    assert checked_field('amount_due',ProposedField(value='$68.40',source_snippet=source),source,TODAY).status=='unverified'


@pytest.mark.parametrize('source,value',[
 ('Please send the signed waiver to Dr. Chen by February 18, 2027.', 'Please send the signed waiver to Dr. Chen'),
 ('File the response within 21 calendar days of the issue date.', 'File the response'),
 ('Pay the balance or request a review by February 18, 2027.', 'Pay the balance'),
 ('Return the form by\nFebruary 18, 2027.', 'Return the form'),
 ('If you dispute the charge, send a written response.', 'send a written response'),
 ('If you dispute the charge,\nsend a written response.', 'send a written response'),
])
def test_short_action_cannot_hide_clause_even_with_clipped_snippet(source,value):
    f=checked_field('required_action',ProposedField(value=value,source_snippet=value),source,TODAY)
    assert f.status=='unverified' and 'omit' in f.reason


@pytest.mark.parametrize('source,value',[
 ('Please send the signed waiver to Dr. Chen by February 18, 2027.', 'Please send the signed waiver to Dr. Chen by February 18, 2027.'),
 ('You must appear in Room 7 at 10:15 AM on February 18, 2027.', 'appear in Room 7 at 10:15 AM on February 18, 2027'),
 ('Required action:\nReturn the form by\nFebruary 18, 2027.', 'Return the form by February 18, 2027.'),
 ('Pay the charge.\nContact: Example Office', 'Pay the charge.'),
])
def test_complete_actions_and_only_optional_prefixes_are_supported(source,value):
    f=checked_field('required_action',ProposedField(value=value,source_snippet=value),source,TODAY)
    assert f.status=='verified'


def test_local_comparison_keeps_wrong_primary_and_actual_alternative(monkeypatch):
    monkeypatch.setattr('backend.preprocessed_reader.preprocess',lambda data:(b'processed',0))
    reader=PreprocessedReader()
    reader.engine=SimpleNamespace(read=Mock(side_effect=[Reading('Current balance: $68.48',[]),Reading('Current balance: $68.40',[])]))
    result=reader.read(b'original')
    assert result.text=='Current balance: $68.48'
    assert result.primary_reader=='preprocessed'
    assert result.token_reviews[0]['status']=='disputed'
    assert {c['value'] for c in result.token_reviews[0]['candidates']}=={'$68.48','$68.40'}
    assert [c.args[0] for c in reader.engine.read.call_args_list]==[b'processed',b'original']


def test_missing_local_comparison_is_disputed_not_agreement(monkeypatch):
    monkeypatch.setattr('backend.preprocessed_reader.preprocess',lambda data:(b'processed',0))
    reader=PreprocessedReader()
    reader.engine=SimpleNamespace(read=Mock(side_effect=[Reading('Amount due: $68.40',[]),ReaderError('safe')]))
    result=reader.read(b'original')
    assert result.token_reviews[0]['status']=='disputed'
    assert any('failed' in s for s in result.warnings)


def test_api_requires_separate_human_amount_review(api):
    client,_=api
    data=request(client,amounts_confirmed=False).json()
    assert data['fields']['amount_due']['status']=='unverified'
    assert data['fields']['amount_due']['normalized_value'] is None
    assert data['receipt']
    assert request(client,amounts_confirmed=True).json()['fields']['amount_due']['status']=='verified'


def test_omitted_amount_attestation_defaults_closed_and_cannot_be_string(api):
    client,_=api
    data=client.post('/api/extract',json={'text':TEXT,'doc_type':'parking_ticket','text_confirmed':True}).json()
    assert data['fields']['amount_due']['status']=='unverified'
    assert request(client,amounts_confirmed='true').status_code==422
    assert request(client,amounts_confirmed=1).status_code==422


def test_unreviewed_ocr_money_cannot_leak_as_verified_action():
    # Construct a fresh simulated reading/model failure, not a held-out replay.
    data=proposed_dict()
    data['required_action']={'value':'Pay $68.48 by February 18, 2027.','source_snippet':'Pay $68.48 by February 18, 2027.'}
    data['amount_due']={'value':'$68.48','source_snippet':'Amount due: $68.48'}
    source=TEXT.replace('Amount due: $45.00','Amount due: $68.48').replace('Pay the charge.',data['required_action']['value'])
    extractor=SimpleNamespace(extract=lambda *args:ExtractionResult(ParkingTicket.model_validate(data),{},1))
    result=extract_and_verify(source,'parking_ticket',extractor,TODAY)
    for name in ('amount_due','required_action'):assert result['fields'][name]['status']=='unverified'


@pytest.mark.parametrize('value',['Thursday, February 18, 2027','Thursday, February 18, 2027 at 10:15 AM'])
def test_scorer_normalizes_weekday_dates_without_using_validator(value):
    result=score_field('deadline','2027-02-18','present',{'value':value,'status':'verified'})
    assert not result['false_verified']
    assert score_field('deadline','2027-02-18','present',{'value':value.replace('Thursday','Monday'),'status':'verified'})['false_verified']


def test_scorer_separates_optional_wording_from_incomplete_actions():
    truth='You must mail the response by February 18, 2027.'
    equivalent=score_field('required_action',truth,'present',{'value':'mail the response by February 18, 2027.','status':'verified'})
    assert equivalent['false_verified'] and not equivalent['equivalence_false_verified']
    assert not equivalent['exact_wording_match'] and equivalent['equivalent_value_present']
    for value in ['mail the response.','mail the response by February 19, 2027.','You must mail the response or do nothing.']:
        assert score_field('required_action',truth,'present',{'value':value,'status':'verified'})['equivalence_false_verified']


def test_wrapped_condition_without_comma_is_not_discarded():
    source='Unless the review office grants an extension\nmail the signed form by February 18, 2027.'
    value='mail the signed form by February 18, 2027.'
    assert checked_field('required_action',ProposedField(value=value,source_snippet=value),source,TODAY).status=='unverified'


def test_avoid_late_fee_explanation_does_not_relabel_current_amount_as_future():
    source='Pay the current $68.40 balance by February 18, 2027 to avoid a late fee.'
    assert checked_field('amount_due',ProposedField(value='$68.40',source_snippet=source),source,TODAY).status=='verified'
    future='Possible late fee: $68.40'
    assert checked_field('amount_due',ProposedField(value='$68.40',source_snippet='$68.40'),future,TODAY).status=='unverified'


def test_scorer_explicit_absence_explanation_cannot_hide_numeric_demand():
    for value in ['Not provided; fees will be set after review.','Not specified; costs are decided at the hearing.']:
        assert not score_field('amount_due',None,'missing',{'value':value,'status':'verified'})['false_verified']
        assert score_field('amount_due','68.40','present',{'value':value,'status':'verified'})['false_verified']
    assert score_field('amount_due',None,'missing',{'value':'Not specified; costs will be set at $68.40.','status':'verified'})['false_verified']


def test_new_rendered_notice_through_real_local_read_and_amount_gate(tmp_path,monkeypatch,caplog):
    import io
    from PIL import Image,ImageDraw
    from eval.generate_samples import load_font
    from fastapi.testclient import TestClient
    from backend.main import app,get_reader,get_extractor,get_today
    image=Image.new('RGB',(1100,600),'white')
    draw=ImageDraw.Draw(image)
    lines=['SYNTHETIC TEST ONLY','Invented Repair Demonstration Office',
        'Deadline: February 18, 2027','Amount due: $68.40',
        'Pay the charge.','Contact: Example Office']
    for n,line in enumerate(lines):draw.text((45,45+n*70),line,font=load_font(size=30),fill='black')
    out=io.BytesIO();image.save(out,format='JPEG')
    data=proposed_dict()
    data['deadline']['value']='February 18, 2027';data['deadline']['source_snippet']=lines[2]
    data['amount_due']={'value':'$68.40','source_snippet':lines[3]}
    data['issuing_agency']={'value':lines[1],'source_snippet':lines[1]}
    data['contact']={'value':'Example Office','source_snippet':lines[5]}
    extractor=SimpleNamespace(extract=lambda *args:ExtractionResult(ParkingTicket.model_validate(data),{},1))
    app.dependency_overrides[get_reader]=lambda:PreprocessedReader()
    app.dependency_overrides[get_extractor]=lambda:extractor
    app.dependency_overrides[get_today]=lambda:TODAY
    monkeypatch.chdir(tmp_path)
    try:
        with TestClient(app) as client:
            read=client.post('/api/read',files={'image':('fresh-synthetic.jpg',out.getvalue(),'image/jpeg')})
            assert read.status_code==200
            result=read.json()
            assert '$68.40' in result['text'] and result['token_reviews']
            assert 'amounts_confirmed' not in result
            payload={'text':result['text'],'doc_type':'parking_ticket','text_confirmed':True}
            unreviewed=client.post('/api/extract',json=payload).json()
            assert unreviewed['fields']['amount_due']['status']=='unverified'
            reviewed=client.post('/api/extract',json={**payload,'amounts_confirmed':True}).json()
            assert reviewed['fields']['amount_due']['status']=='verified'
            assert reviewed['fields']['amount_due']['normalized_value']=='68.40'
            assert read.headers['cache-control']=='no-store'
        assert list(tmp_path.iterdir())==[]
        assert '$68.40' not in caplog.text and lines[1] not in caplog.text
    finally:
        app.dependency_overrides.clear()


def test_sentence_style_future_fee_cannot_bypass_role_check():
    source='After the due date a late fee of $16.20 will apply.'
    f=checked_field('amount_due',ProposedField(value='$16.20',source_snippet='$16.20'),source,TODAY)
    assert f.status=='unverified'
