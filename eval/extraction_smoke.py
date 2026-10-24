"""Eight original synthetic fixtures through real read + model extraction APIs.

This is an opt-in integration check, not the student-owned M4 field scorer.
Only synthetic fixtures from eval/samples/*.json are read; never held-out data.
"""

import argparse
import json
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--out', type=Path, default=Path('eval/reports/extraction-integration.txt'))
    args = parser.parse_args()
    if args.env_file:
        from dotenv import load_dotenv
        load_dotenv(args.env_file, override=True)
    from backend.main import app, Settings, get_today
    settings = Settings.from_environment()
    if settings.reader != 'preprocessed':
        parser.error('This check requires the selected TEXT_READER=preprocessed.')
    app.state.settings = settings
    app.dependency_overrides[get_today] = lambda: date(2026, 10, 22)
    lines = ['M2 SYNTHETIC READ -> EXTRACT INTEGRATION',
             'Reader: preprocessed; model: ' + (settings.model or 'NOT CONFIGURED'),
             'Pinned today: 2026-10-22; temperature: provider default (not sent).',
             'Known fixture type is supplied as an explicit user selection; classifier remains unknown.',
             'No human text corrections in this run; printed reader gate is reported separately.',
             'Correct? checks these original fixture expectations only; not a general field scorer.', '',
             '| Sample | Field | Expected | Extracted | Status | Correct? |',
             '| --- | --- | --- | --- | --- | --- |']
    failed = False
    samples = Path(__file__).resolve().parent / 'samples'
    totals = {'input_tokens': 0, 'output_tokens': 0, 'cached_input_tokens': 0}
    try:
        with TestClient(app) as client:
            for expected_path in sorted(samples.glob('*.json')):
                expected = json.loads(expected_path.read_text())
                reading = client.post('/api/read', files={'image': (expected_path.stem + '.png', expected_path.with_suffix('.png').read_bytes(), 'image/png')})
                if reading.status_code != 200:
                    lines.append('STOPPED: reading unavailable (HTTP ' + str(reading.status_code) + '). Remaining samples NOT RUN.')
                    failed = True
                    break
                response = client.post('/api/extract', json={'text': reading.json()['text'], 'doc_type': expected['doc_type'], 'text_confirmed': True})
                if response.status_code != 200:
                    # Endpoint errors contain fixed public messages, never raw provider bodies.
                    lines.append('STOPPED: extraction HTTP ' + str(response.status_code) + ': ' + response.json().get('detail', 'unavailable'))
                    lines.append('No field accuracy measured; remaining samples NOT RUN. Mock tests are not live extraction evidence.')
                    failed = True
                    break
                result = response.json()
                for key in totals:
                    totals[key] += (result.get('usage') or {}).get(key, 0)
                for field, truth_key in [('deadline','deadline'), ('amount_due','amount'), ('required_action','action')]:
                    actual = result['fields'][field]
                    truth = expected[truth_key]
                    value = actual['normalized_value'] if field != 'required_action' else actual['value']
                    correct = value is None and truth is None if truth is None else ' '.join(str(value).split()) == ' '.join(truth.split())
                    lines.append('| ' + ' | '.join([expected_path.stem, field, str(truth), str(value), actual['status'], str(correct)]) + ' |')
                    if not correct:
                        failed = True
        lines.append('\nReported successful-response token totals only (failed-request usage/cost unknown): ' + json.dumps(totals))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text('\n'.join(lines) + '\n')
        print('\n'.join(lines))
    finally:
        app.dependency_overrides.pop(get_today, None)
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
