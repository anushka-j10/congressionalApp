"""Explicit synthetic production acceptance calls; no local credentials or photos.

Uses ordinary public endpoints and server-issued receipts, never test bypasses.
Receipts are kept in memory and omitted from the saved evidence.
"""
import json
import io
from datetime import datetime, timezone
from pathlib import Path
import httpx
from PIL import Image

BASE = 'https://notice-decoder-ns5o.onrender.com'
OUT = Path(__file__).resolve().parent
report = {'url': BASE, 'checked_at': datetime.now(timezone.utc).isoformat(),
          'deployed_commit': 'e6f9933818d055e436b157aff081aa08be0f962e',
          'synthetic_only': True, 'local_credentials_read': False, 'checks': {}, 'responses': {}}


def save():
    (OUT / 'live-api.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')


with httpx.Client(base_url=BASE, timeout=190, trust_env=False, headers={'Origin': BASE}) as client:
    blank = io.BytesIO()
    Image.new('RGB', (1000, 1300), 'white').save(blank, format='PNG')
    unreadable = client.post('/api/read', files={'image': ('synthetic-blank.png', blank.getvalue(), 'image/png')})
    reading = unreadable.json()
    report['responses']['blank_photo'] = {'http_status': unreadable.status_code, 'output': reading}
    report['checks']['blank_photo_no_guess_and_retake_warning'] = (unreadable.status_code == 200
        and not reading.get('text', '').strip() and reading.get('doc_type') == 'unknown'
        and any('Little readable text' in w for w in reading.get('warnings', [])))
    save()
    def extract(name, text):
        response = client.post('/api/extract', json={'text': text, 'doc_type': 'parking_ticket',
                               'text_confirmed': True, 'amounts_confirmed': True})
        data = response.json()
        report['responses'][name] = {'http_status': response.status_code, 'input': text,
            'output': {k: v for k, v in data.items() if k != 'receipt'}}
        save()
        response.raise_for_status()
        return data

    source = ('SYNTHETIC TEST ONLY\nFictional Demonstration Office\n'
              'Deadline: 11/29/2027\nAmount due: $146.00\nPay the charge.\n'
              'Contact: Example Office.')
    clean = extract('clean', source)
    report['checks']['clean_deadline_amount_action_verified'] = all(clean['fields'][n]['status']=='verified'
        for n in ('deadline','amount_due','required_action'))
    for code in ('en', 'es', 'tl'):
        response = client.post('/api/explain', json={k:clean[k] for k in ('doc_type','fields','today','receipt')} | {'language':code})
        data = response.json()
        report['responses']['simple_explanation_' + code] = {'http_status':response.status_code, 'output':data}
        report['checks']['simple_explanation_' + code] = (response.status_code==200
            and data.get('display_language')==code and bool(data.get('localized',{}).get('summary')))
        save()
    for label, text in [('truncated_year', source.replace('11/29/2027','11/29/2')),
                        ('damaged_duration', source + '\nIf you dispute this charge, notify the office at least S days before payment.')]:
        data = extract(label, text)
        report['checks'][label + '_critical_facts_withheld'] = all(data['fields'][n]['status'] != 'verified'
            for n in ('deadline','amount_due','required_action'))
    absent = extract('no_deadline', source.replace('Deadline: 11/29/2027\n',''))
    report['checks']['absent_deadline_not_invented'] = (absent['fields']['deadline']['status']=='missing'
                                                     and absent['fields']['deadline']['value'] is None)
    # A literal reserved token in an explicitly synthetic contact exercises the
    # deployed translation guard. It is data, not an instruction to the model.
    fallback = extract('reserved_token', source.replace('Example Office.','Example Office, reference ⟦ND_0⟧.'))
    response = client.post('/api/explain', json={k:fallback[k] for k in ('doc_type','fields','today','receipt')} | {'language':'es'})
    explanation = response.json()
    report['responses']['fallback_explanation'] = {'http_status': response.status_code, 'output': explanation}
    report['checks']['deployed_english_fallback'] = response.status_code == 200 and explanation.get('translation',{}).get('fallback_to_english') is True and explanation.get('display_language')=='en' and bool(explanation.get('notice'))
    malformed = client.post('/api/extract', json={'text':'SYNTHETIC-MALFORMED-INPUT'})
    report['responses']['malformed'] = {'http_status':malformed.status_code,'output':malformed.json()}
    report['checks']['malformed_request_safe_error'] = malformed.status_code==422 and 'SYNTHETIC-MALFORMED-INPUT' not in malformed.text
    report['passed'] = sum(report['checks'].values())
    report['total'] = len(report['checks'])
    save()
    print(json.dumps({'checks':report['checks'],'passed':report['passed'],'total':report['total']},indent=2))
    assert all(report['checks'].values())
