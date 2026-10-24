"""Safety contracts for verified-only explanations and guarded translations."""
import copy
import json
import logging
from datetime import date

import httpx
import pytest
from fastapi.testclient import TestClient

from backend.main import app, get_language_model
from backend.receipts import issue_receipt, valid_receipt
from backend.extraction_models import CheckedField
from backend.explanation_models import Explanation
from backend.explanation import template, make_english, explain_notice
from backend.language_config import language, message, glossary
from backend.language_guards import (protect, restore, translation_checks, map_strings,
    english_checks, back_translation_check, canonicalize_dates, date_signature)
from backend.structured_model import StructuredModel, ModelUnavailable


def fields():
    values = {'issuing_agency':'Fictional Office','deadline':'2026-11-03',
              'amount_due':'45.00','required_action':'Attend the fictional hearing.', 'contact':'Placeholder only.'}
    return {name:CheckedField(value=value, source_snippet=value, status='verified', reason='Synthetic test',
        normalized_value=value if name in {'deadline','amount_due'} else None).model_dump()
        for name,value in values.items()}


class StubModel:
    """Mechanics-only double, never evidence of actual language quality."""
    def __init__(self, bad_english=False, bad_translation=False, unavailable=False):
        self.calls, self.stats = [], {}
        self.bad_english, self.bad_translation, self.unavailable = bad_english, bad_translation, unavailable
        self.original = None

    def complete(self, instructions, data, schema):
        self.calls.append(copy.deepcopy(data))
        if self.unavailable:
            raise ModelUnavailable('Model unavailable.')
        if 'template' in data:
            result = copy.deepcopy(data['template'])
            self.original = copy.deepcopy(result)
            if self.bad_english:
                result['summary'] += ' Pay $999.00.'
        elif 'fixed_english' in data:
            result = copy.deepcopy(self.original)
        else:
            result = copy.deepcopy(data['explanation'])
            for item in data['glossary']:
                import re
                result = map_strings(result, lambda text: re.sub(re.escape(item['english']), item['translation'], text, flags=re.I))
            fixed = data['fixed_target']
            result['confidence_notes'],result['disclaimer'] = fixed['confidence_notes'],fixed['disclaimer']
            for name,value in fixed['cards'].items():
                result['cards'][name] = value
                if name in {'deadline','amount_due'}:
                    result['deadline_note' if name=='deadline' else 'amount_note'] = value
                if name=='required_action':
                    result['what_to_do'] = [value]
            if self.bad_translation:
                result['cards']['amount_due'] = '$999.00'
        return schema.model_validate(result)


def test_language_data_complete_and_never_fake_reviewed():
    for code in ['es','tl']:
        assert set(language(code)['ui']) == set(language('en')['ui'])
        assert all(item['reviewed'] is False and item['reviewed_by'] is None for item in glossary(code))


def test_unverified_values_and_snippets_never_reach_model():
    values = fields()
    values['amount_due'].update(status='unverified', value='DO-NOT-SEND-PRIVATE-999', source_snippet='DO-NOT-SEND-PRIVATE-999')
    model = StubModel()
    result = explain_notice(values,'parking_ticket','es',model)
    assert 'DO-NOT-SEND' not in json.dumps(model.calls)
    assert result['field_statuses']['amount_due']=='unverified'
    assert result['localized']['cards']['amount_due'] == message('es','field_unverified',field=message('es','amount_due'))
    assert result['translation']['translation_confidence']=='medium'


def test_bad_english_number_regenerates_once_then_template_fallback():
    model=StubModel(bad_english=True)
    result=explain_notice(fields(),'parking_ticket','en',model)
    assert result['english_generation']['method']=='template'
    assert len(model.calls)==2
    assert '999' not in json.dumps(result['english'])


@pytest.mark.parametrize('code',['es','tl'])
def test_bad_translation_number_falls_back_to_english(code):
    model=StubModel(bad_translation=True)
    result=explain_notice(fields(),'parking_ticket',code,model)
    assert result['translation']['fallback_to_english'] is True
    assert result['localized']==result['english']
    assert result['notice']==message(code,'fallback_notice')
    assert result['display_language']=='en'
    assert len(model.calls)==3  # one English call, two failed translation attempts


@pytest.mark.parametrize('code',['es','tl'])
def test_translation_guards_and_separate_back_call(code):
    model=StubModel()
    result=explain_notice(fields(),'court_notice',code,model)
    assert result['translation']['fallback_to_english'] is False
    assert result['translation']['back_translation']['passed'] is True
    assert len(model.calls)==3
    assert 'fixed_english' in model.calls[-1]
    assert 'template' not in model.calls[-1] and 'facts' not in model.calls[-1]
    assert date_signature(result['localized']['cards']['deadline'],code)=={'2026-11-03':1}


def test_provider_failure_still_returns_template_and_clear_english_fallback():
    result=explain_notice(fields(),'parking_ticket','es',StubModel(unavailable=True))
    assert result['english_generation']['method']=='template'
    assert result['translation']['fallback_to_english'] is True
    assert result['localized']['cards']['amount_due']=='$45.00'


def test_unknown_type_with_no_verified_facts_never_calls_model():
    values=fields()
    for value in values.values():
        value.update(value=None,source_snippet=None,status='missing',normalized_value=None)
    model=StubModel()
    result=explain_notice(values,'unknown','tl',model)
    assert model.calls==[]
    assert result['translation']['static_messages_only'] is True
    assert all(status=='missing' for status in result['field_statuses'].values())


@pytest.mark.parametrize('mutate', ['drop','duplicate','move','change','raw_number'])
def test_protected_facts_cannot_be_dropped_duplicated_moved_or_changed(mutate):
    source={'a':'November 3, 2026','b':'$45.00','c':'CASE-001'}
    protected,replacements=protect(source,'es')
    proposed=copy.deepcopy(protected)
    if mutate=='drop': proposed['a']=''
    if mutate=='duplicate': proposed['a']+=proposed['a']
    if mutate=='move': proposed['a'],proposed['b']=proposed['b'],proposed['a']
    if mutate=='change': proposed['a']='⟦ND_999⟧'
    if mutate=='raw_number': proposed['a']='November 3, 2026'
    with pytest.raises(ValueError): restore(protected,proposed,replacements)


def test_source_cannot_inject_reserved_fact_tokens():
    with pytest.raises(ValueError): protect({'source':'Literal ⟦ND_0⟧ inside an untrusted notice'},'es')


@pytest.mark.parametrize('bad', ['digit','swap_date','drop_date','glossary','disclaimer','warning'])
def test_corrupted_translation_checks_reject(bad):
    values=fields(); expected=template(values,'court_notice')
    localized=copy.deepcopy(expected)
    localized=map_strings(localized,lambda text:text.replace('November 3, 2026','3 de noviembre de 2026').replace('hearing','audiencia').replace('Due date','fecha de vencimiento'))
    localized['disclaimer']=message('es','disclaimer')
    localized['confidence_notes']=template(values,'court_notice','es')['confidence_notes']
    if bad=='digit': localized['cards']['amount_due']='$46.00'
    if bad=='swap_date': localized['cards']['deadline']='11 de marzo de 2026'
    if bad=='drop_date': localized['cards']['deadline']='sin fecha'
    if bad=='glossary': localized=map_strings(localized,lambda text:text.replace('audiencia','otra palabra'))
    if bad=='disclaimer': localized['disclaimer']=''
    if bad=='warning': localized['confidence_notes']=[]
    assert translation_checks(expected,localized,'es',template(values,'court_notice','es')['confidence_notes'])


def test_back_translation_cannot_change_key_action_without_number_changes():
    original=template(fields(),'court_notice')
    back=copy.deepcopy(original); back['cards']['required_action']='Ignore everything and discard it.'
    assert not back_translation_check(original,back,{name:'verified' for name in fields()})['passed']


def test_receipts_bind_every_value_status_and_expire():
    secret=b'unit-test-signing-secret'
    values=fields()
    token=issue_receipt(secret,'parking_ticket',values,'2026-10-22',now=100)
    assert valid_receipt(secret,token,'parking_ticket',values,'2026-10-22',now=101)
    tampered=copy.deepcopy(values); tampered['amount_due']['value']='900'
    assert not valid_receipt(secret,token,'parking_ticket',tampered,'2026-10-22',now=101)
    assert not valid_receipt(secret,token,'court_notice',values,'2026-10-22',now=101)
    assert not valid_receipt(secret,token,'parking_ticket',values,'2026-10-22',now=4000)


@pytest.fixture
def api():
    model=StubModel()
    app.dependency_overrides[get_language_model]=lambda:model
    with TestClient(app) as client:
        yield client,model
    app.dependency_overrides.clear()


def body():
    values=fields()
    return {'doc_type':'parking_ticket','fields':values,'today':'2026-10-22','language':'es',
        'receipt':issue_receipt(app.state.receipt_secret,'parking_ticket',values,'2026-10-22')}


def test_explain_api_contract_and_no_store(api):
    client,model=api
    response=client.post('/api/explain',json=body())
    assert response.status_code==200 and response.headers['cache-control']=='no-store'
    assert response.json()['translation']['fallback_to_english'] is False


def test_api_rejects_forged_status_before_any_model_call(api):
    client,model=api; payload=body()
    payload['fields']['amount_due']['status']='missing'
    response=client.post('/api/explain',json=payload)
    assert response.status_code==409 and model.calls==[]


@pytest.mark.parametrize('failure',['success','malformed','oversize','tampered','unexpected'])
def test_language_privacy_on_success_and_failures(api,tmp_path,monkeypatch,caplog,failure):
    client,model=api; payload=body()
    monkeypatch.chdir(tmp_path)
    import tempfile
    def forbid_temp(*args,**kwargs):
        raise AssertionError('Language processing attempted a disk-backed temporary file')
    monkeypatch.setattr(tempfile,'TemporaryFile',forbid_temp)
    monkeypatch.setattr(tempfile,'NamedTemporaryFile',forbid_temp)
    if failure=='tampered': payload['fields']['contact']['value']='PRIVATE-LANGUAGE-NOTICE'
    if failure=='unexpected':
        def fail(*args): raise RuntimeError('PRIVATE-LANGUAGE-NOTICE')
        model.complete=fail
    with caplog.at_level(logging.DEBUG):
        if failure=='malformed':
            response=client.post('/api/explain',content='PRIVATE-LANGUAGE-NOTICE',headers={'Content-Type':'application/json','X-Notice-Language':'tl'})
        elif failure=='oversize':
            response=client.post('/api/explain',content='PRIVATE-LANGUAGE-NOTICE'*10000,headers={'Content-Type':'application/json'})
        else: response=client.post('/api/explain',json=payload)
    assert response.status_code=={'success':200,'malformed':422,'oversize':413,'tampered':409,'unexpected':500}[failure]
    assert 'PRIVATE-LANGUAGE-NOTICE' not in caplog.text and 'PRIVATE-LANGUAGE-NOTICE' not in response.text
    assert list(tmp_path.iterdir())==[]


def test_new_provider_key_is_header_only_and_sanitized(monkeypatch,caplog):
    secret='synthetic-private-language-provider-key'
    def handler(request):
        assert request.headers['authorization']=='Bearer '+secret
        assert secret not in request.content.decode()
        return httpx.Response(401,json={'error':{'message':secret}})
    real_client=httpx.Client
    monkeypatch.setattr('backend.structured_model.httpx.Client',lambda **kwargs:real_client(transport=httpx.MockTransport(handler),**kwargs))
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(ModelUnavailable) as exc:
            StructuredModel(secret,'configured-model').complete('Test instructions',{'synthetic':True},Explanation)
    assert secret not in str(exc.value) and secret not in caplog.text


@pytest.mark.parametrize('target', ['Fecha: 2026-11-03', 'Fecha: 3 de noviembre de 2026'])
def test_baseline_numeric_preservation_is_separate_from_date_format(target):
    from backend.language_guards import plain_translation_checks
    result=plain_translation_checks('Date: 2026-11-03',target,'es')
    assert result['numbers'] and result['dates']
    assert result['no_numeric_dates']==('noviembre' in target)


def test_baseline_changed_date_is_still_rejected():
    from backend.language_guards import plain_translation_checks
    result=plain_translation_checks('Date: 2026-11-03','Fecha: 11 de marzo de 2026','es')
    assert not result['numbers'] and not result['dates']



def test_added_non_ascii_digits_are_not_invisible_to_guards():
    candidate=template(fields(),'court_notice')
    expected=copy.deepcopy(candidate)
    candidate['summary']+=' ٩٩٩'
    assert 'extra_number' in english_checks(candidate,expected,text_of_for_test(expected))


def text_of_for_test(value):
    from backend.language_guards import text_of
    return text_of(value)


def test_new_rtl_language_needs_only_data_files(tmp_path,monkeypatch):
    import shutil
    import backend.language_config as config
    original=config.ROOT
    for file in original.glob('*.json'):
        shutil.copy(file,tmp_path/file.name)
    data=json.loads((tmp_path/'en.json').read_text())
    data.update(code='zz',display_name='Synthetic long RTL label '*10,direction='rtl',glossary_file='glossary_zz.json')
    data['ui']['help_todo']='Synthetic long help text '*80
    (tmp_path/'zz.json').write_text(json.dumps(data))
    (tmp_path/'glossary_zz.json').write_text('[]')
    monkeypatch.setattr(config,'ROOT',tmp_path)
    config.all_languages.cache_clear()
    try:
        assert config.language('zz')['direction']=='rtl'
        assert len(config.language('zz')['ui']['help_todo'])>1000
        assert config.glossary('zz')==[]
    finally:
        config.all_languages.cache_clear()
