"""Bounded strict-JSON calls for explanation/translation, never logging payloads."""
import time
import httpx
from pydantic import ValidationError


class ModelUnavailable(Exception):
    """Fixed public message only."""


class StructuredModel:
    def __init__(self, api_key, model, temperature=None, reasoning_effort=None):
        self.api_key, self.model = api_key, model
        self.generation = {}
        if temperature is not None: self.generation["temperature"] = temperature
        if reasoning_effort is not None: self.generation["reasoning"] = {"effort": reasoning_effort}
        self.stats = {'calls':0, 'input_tokens':0, 'output_tokens':0, 'cached_input_tokens':0,
                      'responses_with_usage':0}

    def complete(self, instructions, data, schema):
        if not self.api_key or not self.model:
            raise ModelUnavailable('Model unavailable.')
        import json
        body = {'model':self.model, 'store':False, 'max_output_tokens':6500,
                'instructions':instructions,
                'input':[{'role':'user','content':[{'type':'input_text','text':json.dumps(data, ensure_ascii=False)}]}],
                'text':{'format':{'type':'json_schema','name':'notice_language','strict':True,'schema':schema.model_json_schema()}}}
        body.update(self.generation)
        for attempt in range(2):
            retryable = True
            try:
                self.stats['calls'] += 1
                with httpx.Client(timeout=40, trust_env=False) as client:
                    response = client.post('https://api.openai.com/v1/responses',
                        headers={'Authorization':'Bearer '+self.api_key}, json=body)
                    response.raise_for_status()
                    envelope = response.json()
                usage = envelope.get('usage')
                if isinstance(usage, dict):
                    self.stats['responses_with_usage'] += 1
                    for name in ['input_tokens','output_tokens']:
                        count = usage.get(name)
                        if type(count) is int and count >= 0:
                            self.stats[name] += count
                    details = usage.get('input_tokens_details') or {}
                    if isinstance(details, dict) and type(details.get('cached_tokens')) is int:
                        self.stats['cached_input_tokens'] += max(0, details['cached_tokens'])
                if envelope.get('status') != 'completed':
                    raise ValueError('Incomplete output')
                parts = [part for item in envelope.get('output', []) if item.get('type') == 'message'
                         for part in item.get('content', [])]
                if any(part.get('type') == 'refusal' for part in parts):
                    raise ModelUnavailable('Model unavailable.')
                texts = [part['text'] for part in parts if part.get('type') == 'output_text']
                if len(texts) != 1:
                    raise ValueError('Missing output')
                return schema.model_validate_json(texts[0])
            except httpx.HTTPStatusError as exc:
                retryable = exc.response.status_code == 429 or exc.response.status_code >= 500
                # Billing errors cannot be fixed by retrying. Read only a code;
                # provider messages/headers never enter public errors or logs.
                if exc.response.status_code == 429:
                    try:
                        code = exc.response.json().get('error', {}).get('code')
                        if code in {'credit_balance_exhausted','insufficient_quota','project_spend_limit_exceeded',
                                    'organization_spend_limit_exceeded','organization_usage_limit_exceeded'}:
                            retryable = False
                    except (ValueError, TypeError, AttributeError):
                        pass
            except (httpx.HTTPError, ValueError, TypeError, KeyError, AttributeError, ValidationError):
                pass
            if not retryable or attempt:
                raise ModelUnavailable('Model unavailable.') from None
            time.sleep(0.5)
