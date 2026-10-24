"""Short-lived signatures bind explanations to server-checked field statuses."""
import hashlib
import hmac
import json
import time

TTL_SECONDS = 3600


def payload(doc_type, fields, today, issued):
    return json.dumps({'doc_type':doc_type, 'fields':fields, 'today':today, 'issued':issued},
                      sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def issue_receipt(secret, doc_type, fields, today, now=None):
    issued = int(time.time() if now is None else now)
    digest = hmac.new(secret, payload(doc_type, fields, today, issued), hashlib.sha256).hexdigest()
    return f'{issued}.{digest}'


def valid_receipt(secret, token, doc_type, fields, today, now=None):
    try:
        timestamp, supplied = token.split('.', 1)
        issued = int(timestamp)
        current = int(time.time() if now is None else now)
        if not 0 <= current - issued <= TTL_SECONDS:
            return False
        expected = issue_receipt(secret, doc_type, fields, today, now=issued)
        return hmac.compare_digest(expected, token)
    except (ValueError, TypeError, AttributeError):
        return False
