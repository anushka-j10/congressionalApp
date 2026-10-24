"""Adversarial plumbing and privacy; mocks are not evidence of live model immunity."""
import json
import logging
import tempfile
from datetime import date
from unittest.mock import Mock
from pathlib import Path
import httpx
import pytest
from fastapi.testclient import TestClient
from backend.main import app,get_reader,get_extractor,get_today,get_language_model
from backend.readers import Reading
from backend.extraction import ModelExtractor,ExtractionResult,ExtractionError
from backend.extraction_models import NOTICE_MODELS
from backend.field_validation import verify_notice
from backend.structured_model import StructuredModel,ModelUnavailable
from backend.explanation_models import PlainTranslation
from eval.protocol import load_set
from tests.test_extract import provider,response,envelope
from tests.test_explanation import StubModel

ATTACKS=load_set('adversarial')


def proposal(item):
    def field(value,snippet):return {'value':value,'source_snippet':snippet}
    return {'doc_type':item['doc_type'],
      'issuing_agency':field('Invented Civic Demonstration Office','Invented Civic Demonstration Office'),
      'deadline':{**field('November 20, 2026','Deadline: November 20, 2026'),'kind':'absolute',
         'relative_days':None,'anchor_date':None,'anchor_source_snippet':None},
      'amount_due':field('$47.25','Amount due: $47.25'),
      'required_action':field(item['expected']['required_action'],'What to do: '+item['expected']['required_action']),
      'contact':field(item['expected']['contact'],'Contact: '+item['expected']['contact'])}


@pytest.mark.parametrize('item',ATTACKS,ids=lambda item:item['id'])
def test_hostile_body_stays_in_untrusted_user_input_and_status_is_server_owned(monkeypatch,item):
    post=provider(monkeypatch,[response(envelope(proposal(item)))])
    result=ModelExtractor('fake-test-key','test-model').extract(item['text'],item['doc_type'])
    payload=post.call_args.kwargs['json']
    assert item['hostile_text'] not in payload['instructions']
    assert payload['input'][0]['role']=='user'
    assert item['hostile_text'] in payload['input'][0]['content'][0]['text']
    assert 'status' not in payload['text']['format']['schema']['$defs']['ProposedField']['properties']
    checked,_=verify_notice(result.proposed,item['text'],date(2026,10,24))
    assert checked['deadline'].normalized_value=='2026-11-20'
    assert checked['amount_due'].normalized_value=='47.25'


@pytest.mark.parametrize('item',ATTACKS,ids=lambda item:item['id'])
def test_fabricated_unsupported_amount_is_never_verified(item):
    raw=proposal(item);raw['amount_due']['value']='$123456.78'
    checked,_=verify_notice(NOTICE_MODELS[item['doc_type']].model_validate(raw),item['text'],date(2026,10,24))
    assert checked['amount_due'].status=='unverified'
    assert checked['amount_due'].normalized_value is None


def test_hostile_source_supported_amount_must_not_be_verified():
    item=ATTACKS[4];raw=proposal(item)
    raw['amount_due']={'value':'$999.99','source_snippet':item['hostile_text']}
    checked,_=verify_notice(NOTICE_MODELS[item['doc_type']].model_validate(raw),item['text'],date(2026,10,24))
    assert checked['amount_due'].status!='verified'


@pytest.mark.parametrize('kind',['timeout','rate','malformed'])
def test_language_provider_failure_retries_once_without_partial_output(monkeypatch,kind,caplog):
    private='PRIVATE-M4-PROVIDER-SENTINEL'
    if kind=='timeout':bad=httpx.ReadTimeout(private)
    elif kind=='rate':bad=response({'error':{'message':private,'code':'rate_limit_exceeded'}},429)
    else:bad=httpx.Response(200,text='{'+private,request=httpx.Request('POST','https://api.openai.com/v1/responses'))
    post=provider(monkeypatch,[bad,bad])
    # httpx is the same imported module for both adapters; mocked Client stays isolated.
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(ModelUnavailable) as error:
            StructuredModel('fake-only','test-model').complete('Fixed instructions',{'text':private},PlainTranslation)
    assert post.call_count==2
    assert private not in str(error.value) and private not in caplog.text


@pytest.mark.parametrize('fail_at',[None,'read','extract','explain'])
def test_entire_api_flow_leaves_no_notice_translation_or_explanation_on_disk_or_logs(tmp_path,monkeypatch,caplog,fail_at):
    item=ATTACKS[0];private='PRIVATE-M4-CONTENT-SENTINEL'
    text=item['text']+'\n'+private
    reader=Mock();reader.name='mock';reader.read.return_value=Reading(text,[])
    if fail_at=='read':reader.read.side_effect=RuntimeError(private)
    extractor=Mock();extractor.extract.return_value=ExtractionResult(NOTICE_MODELS[item['doc_type']].model_validate(proposal(item)),{},1)
    if fail_at=='extract':extractor.extract.side_effect=RuntimeError(private)
    model=StubModel()
    if fail_at=='explain':model.complete=Mock(side_effect=RuntimeError(private))
    app.dependency_overrides[get_reader]=lambda:reader
    app.dependency_overrides[get_extractor]=lambda:extractor
    app.dependency_overrides[get_today]=lambda:date(2026,10,24)
    app.dependency_overrides[get_language_model]=lambda:model
    def forbidden(*args,**kwargs):raise AssertionError('Disk-backed notice temp file forbidden')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(tempfile,'TemporaryFile',forbidden)
    monkeypatch.setattr(tempfile,'NamedTemporaryFile',forbidden)
    try:
        with TestClient(app) as client,caplog.at_level(logging.DEBUG):
            photo=Path(item['variants'][0]['resolved_image']).read_bytes()
            read=client.post('/api/read',files={'image':('synthetic.png',photo,'image/png')})
            if fail_at=='read':assert read.status_code==500 and private not in read.text
            else:
                extracted=client.post('/api/extract',json={'text':read.json()['text'],'doc_type':item['doc_type'],'text_confirmed':True})
                if fail_at=='extract':assert extracted.status_code==500 and private not in extracted.text
                else:
                    data=extracted.json()
                    explained=client.post('/api/explain',headers={'X-Notice-Language':'es'},json={
                      'doc_type':data['doc_type'],'fields':data['fields'],'today':data['today'],'receipt':data['receipt'],'language':'es'})
                    assert explained.status_code==(500 if fail_at=='explain' else 200)
                    if fail_at=='explain':
                        assert private not in explained.text
                        assert explained.json()['detail']!='explanation_failed'
        assert private not in caplog.text
        assert item['text'] not in caplog.text
        assert not list(tmp_path.rglob('*'))
    finally:app.dependency_overrides.clear()


def test_conflicting_required_dates_must_not_produce_a_verified_choice():
    item=next(value for value in load_set('dev') if 'conflicting_dates' in value['edge_cases'])
    raw=proposal(item)
    raw['deadline']['value']='November 4, 2026'
    raw['deadline']['source_snippet']='Mandatory hearing date: November 4, 2026'
    checked,_=verify_notice(NOTICE_MODELS[item['doc_type']].model_validate(raw),item['text'],date(2026,10,24))
    assert checked['deadline'].status!='verified'
