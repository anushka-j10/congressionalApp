"""Provider-contract, bad-output, request-boundary, and privacy tests."""

import json
import logging
import tempfile
from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest
from fastapi.testclient import TestClient

from backend.extraction import ModelExtractor, ExtractionResult, ExtractionError
from backend.extraction_models import ParkingTicket, NOTICE_MODELS
from backend.main import app, get_extractor, get_today

TEXT = 'Fictional Office\nDeadline: 11/30/2026\nAmount due: $45.00\nPay the charge.\nContact: placeholder only.'


def proposed_dict(doc_type='parking_ticket'):
    def field(value, source):
        return dict(value=value, source_snippet=source)
    return dict(doc_type=doc_type, issuing_agency=field('Fictional Office', 'Fictional Office'),
        deadline=dict(value='11/30/2026', source_snippet='Deadline: 11/30/2026', kind='absolute',
                      relative_days=None, anchor_date=None, anchor_source_snippet=None),
        amount_due=field('$45.00', 'Amount due: $45.00'), required_action=field('Pay the charge.', 'Pay the charge.'),
        contact=field('placeholder only.', 'Contact: placeholder only.'))


def envelope(proposed=None, **updates):
    data = dict(status='completed', output=[{'type': 'message', 'content': [
        {'type': 'output_text', 'text': json.dumps(proposed or proposed_dict())}]}],
        usage={'input_tokens': 123, 'output_tokens': 45, 'input_tokens_details': {'cached_tokens': 10}})
    data.update(updates)
    return data


def provider(monkeypatch, responses):
    post = Mock(side_effect=responses)
    client = Mock()
    client.__enter__ = Mock(return_value=SimpleNamespace(post=post))
    client.__exit__ = Mock(return_value=False)
    monkeypatch.setattr('backend.extraction.httpx.Client', Mock(return_value=client))
    monkeypatch.setattr('backend.extraction.time.sleep', Mock())
    return post


def response(data, status=200):
    return httpx.Response(status, json=data, request=httpx.Request('POST', 'https://api.openai.com/v1/responses'))


@pytest.fixture
def api():
    stub = Mock()
    stub.extract.return_value = ExtractionResult(ParkingTicket.model_validate(proposed_dict()), {}, 1)
    app.dependency_overrides[get_extractor] = lambda: stub
    app.dependency_overrides[get_today] = lambda: date(2026, 10, 22)
    with TestClient(app) as client:
        yield client, stub
    app.dependency_overrides.clear()


def request(client, **changes):
    data = dict(text=TEXT, doc_type='parking_ticket', text_confirmed=True, amounts_confirmed=True)
    data.update(changes)
    return client.post('/api/extract', json=data)


def test_full_contract_and_injected_date(api):
    client, stub = api
    result = request(client)
    assert result.status_code == 200 and result.headers['cache-control'] == 'no-store'
    data = result.json()
    assert data['today'] == '2026-10-22'
    assert all(field['status'] == 'verified' for field in data['fields'].values())
    assert data['fields']['deadline']['days_remaining'] == 39
    stub.extract.assert_called_once_with(TEXT, 'parking_ticket')


@pytest.mark.parametrize('change', ['value', 'snippet'])
def test_simulated_bad_model_output_is_never_verified(api, change):
    client, stub = api
    proposed = proposed_dict()
    proposed['deadline']['value' if change == 'value' else 'source_snippet'] = '11/29/2026' if change == 'value' else 'Deadline: 11/29/2026'
    stub.extract.return_value.proposed = ParkingTicket.model_validate(proposed)
    field = request(client).json()['fields']['deadline']
    assert field['status'] == 'unverified' and field['days_remaining'] is None


def test_unknown_type_never_calls_model(api):
    client, stub = api
    data = request(client, doc_type='unknown').json()
    stub.extract.assert_not_called()
    assert data['attempts'] == 0 and data['usage'] is None
    assert all(field['status'] == 'missing' for field in data['fields'].values())


@pytest.mark.parametrize('change', [dict(text_confirmed=False), dict(text_confirmed=1), dict(text_confirmed='true'), dict(text=''), dict(text='   '),
    dict(text='x'*30001), dict(doc_type='bad-SENSITIVE'), dict(extra='SENSITIVE')])
def test_bad_requests_do_not_echo_private_inputs(api, change):
    client, stub = api
    result = request(client, **change)
    assert result.status_code == 422
    assert 'SENSITIVE' not in result.text
    stub.extract.assert_not_called()


def test_bounded_body_and_malformed_json(api):
    client, stub = api
    assert client.post('/api/extract', content=b'x'*150001, headers={'content-type':'application/json'}).status_code == 413
    result = client.post('/api/extract', content=b'{"private":"SENSITIVE",bad}', headers={'content-type':'application/json'})
    assert result.status_code == 422 and 'SENSITIVE' not in result.text
    assert client.post('/api/extract', content='private').status_code == 415
    stub.extract.assert_not_called()


@pytest.mark.parametrize('doc_type', list(NOTICE_MODELS))
def test_actual_provider_request_is_strict_text_only_and_no_store(monkeypatch, doc_type):
    post = provider(monkeypatch, [response(envelope(proposed_dict(doc_type)))])
    extracted = ModelExtractor('secret-test-only', 'configured-test-model').extract(TEXT, doc_type)
    payload = post.call_args.kwargs['json']
    assert payload['model'] == 'configured-test-model' and payload['store'] is False
    assert payload['input'][0]['content'] == [{'type':'input_text', 'text':TEXT}]
    assert payload['text']['format']['strict'] is True
    schema = payload['text']['format']['schema']
    for item in [schema, *schema['$defs'].values()]:
        assert item['additionalProperties'] is False
        assert set(item['required']) == set(item['properties'])
    assert 'status' not in schema['$defs']['ProposedField']['properties']
    assert extracted.usage['input_tokens'] == 123 and extracted.usage['cached_input_tokens'] == 10


@pytest.mark.parametrize('bad', [
    envelope(status='incomplete'), envelope(output=[]),
    envelope(output=[{'type':'message','content':[{'type':'output_text','text':'bad SENSITIVE JSON'}]}]),
    envelope(output='bad'), {'status':'completed', 'output':[None]},
])
def test_bad_provider_response_retries_once_then_fails_without_partial_output(monkeypatch, bad):
    post = provider(monkeypatch, [response(bad), response(bad)])
    with pytest.raises(ExtractionError) as exc:
        ModelExtractor('key', 'model').extract(TEXT, 'parking_ticket')
    assert post.call_count == 2 and 'SENSITIVE' not in str(exc.value)


@pytest.mark.parametrize('kind', ['timeout', 'rate', 'server', 'auth'])
def test_transient_errors_retry_once_auth_does_not(monkeypatch, kind):
    bad = httpx.ReadTimeout('SENSITIVE') if kind == 'timeout' else response({'private':'SENSITIVE'}, {'rate':429, 'server':500, 'auth':401}[kind])
    post = provider(monkeypatch, [bad, bad])
    with pytest.raises(ExtractionError) as exc:
        ModelExtractor('key','model').extract(TEXT,'parking_ticket')
    assert post.call_count == (1 if kind == 'auth' else 2)
    assert 'SENSITIVE' not in str(exc.value)


def test_refusal_not_shown_or_retried(monkeypatch):
    post = provider(monkeypatch, [response(envelope(output=[{'type':'message','content':[{'type':'refusal','refusal':'SENSITIVE'}]}]))])
    with pytest.raises(ExtractionError) as exc:
        ModelExtractor('key','model').extract(TEXT,'parking_ticket')
    assert post.call_count == 1 and 'SENSITIVE' not in str(exc.value)


def test_recovery_discards_partial_fields_and_reports_actual_attempt_usage(monkeypatch):
    post = provider(monkeypatch, [response(envelope(status='incomplete')), response(envelope())])
    result = ModelExtractor('key','model').extract(TEXT, 'parking_ticket')
    assert result.attempts == 2 and result.usage['input_tokens'] == 246
    assert result.proposed.amount_due.value == '$45.00'


@pytest.mark.parametrize('failure', [None, 'provider', 'unexpected', 'request'])
def test_extraction_keeps_text_out_of_logs_files_and_errors(api, tmp_path, monkeypatch, caplog, failure):
    client, stub = api
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('TMPDIR', str(tmp_path))
    def forbid(*args, **kwargs):
        raise AssertionError('Notice attempted a disk-backed temp file')
    monkeypatch.setattr(tempfile, 'TemporaryFile', forbid)
    monkeypatch.setattr(tempfile, 'NamedTemporaryFile', forbid)
    if failure in ['provider', 'unexpected']:
        stub.extract.side_effect = ExtractionError('Extraction unavailable.') if failure == 'provider' else RuntimeError('SENSITIVE')
    with caplog.at_level(logging.INFO):
        result = request(client, text=TEXT+'\nSENSITIVE', doc_type='SENSITIVE' if failure == 'request' else 'parking_ticket')
    assert result.status_code == {None:200, 'provider':503, 'unexpected':500, 'request':422}[failure]
    assert list(tmp_path.rglob('*')) == []
    assert 'SENSITIVE' not in caplog.text
    if failure:
        assert 'SENSITIVE' not in result.text and 'fields' not in result.json()


def test_parenthesized_source_amount_is_not_returned_as_verified(api):
    client, stub = api
    text = TEXT.replace('Amount due: $45.00', 'Amount due: ($45.00)')
    proposed = proposed_dict()
    proposed['amount_due']['source_snippet'] = 'Amount due: ($45.00)'
    stub.extract.return_value.proposed = ParkingTicket.model_validate(proposed)
    response = request(client, text=text)
    assert response.status_code == 200
    amount = response.json()['fields']['amount_due']
    assert amount['status'] == 'unverified'
    assert amount['normalized_value'] is None


@pytest.mark.parametrize('status', [401, 403, 429, 500])
def test_provider_credential_never_enters_prompt_public_errors_or_logs(monkeypatch, caplog, status):
    secret = 'synthetic-private-credential-for-provider-test'
    post = provider(monkeypatch, [response({'error': {'message': secret}}, status)] * 2)
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(ExtractionError) as exc:
            ModelExtractor(secret, 'configured-test-model').extract(TEXT, 'parking_ticket')
    assert secret not in str(exc.value)
    assert secret not in caplog.text
    for call in post.call_args_list:
        assert call.args[0] == 'https://api.openai.com/v1/responses'
        assert call.kwargs['headers']['Authorization'] == 'Bearer ' + secret
        assert secret not in json.dumps(call.kwargs['json'])


def test_unexpected_provider_exception_cannot_leak_credential_through_api(api, caplog):
    client, stub = api
    secret = 'synthetic-private-credential-for-exception-test'
    stub.extract.side_effect = RuntimeError(secret)
    with caplog.at_level(logging.DEBUG):
        response = request(client)
    assert response.status_code == 500
    assert secret not in response.text
    assert secret not in str(response.headers)
    assert secret not in caplog.text
