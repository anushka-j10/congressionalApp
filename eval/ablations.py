"""Offline leave-one-validator-group-out replay on saved dev/adversarial proposals.

No model calls, OCR reruns, credentials, or held-out input support. Calendar,
relative-anchor, and conflicting-date checks form one date-validation group.
Schema checks and unknown-type abstention remain mandatory in every mode.
Explanation guards are a later pipeline stage, not field validators.
"""
import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path

from backend.extraction import apply_amount_review
from backend.extraction_models import ProposedNotice
from backend.field_validation import VALIDATOR_GROUPS, _checked_field
from eval.protocol import FIELDS, source_fingerprint
from eval.scoring import VERSION, display, summarize

GROUPS = tuple(sorted(VALIDATOR_GROUPS)) + ('human_amount_review',)


def validate(proposed, text, today, disabled=None):
    if disabled is not None and disabled not in GROUPS:
        raise ValueError('Unknown validator group')
    fields = {name: _checked_field(name, getattr(proposed, name), text, today,
              frozenset({disabled}) if disabled in VALIDATOR_GROUPS else frozenset())
              for name in ('issuing_agency',) + FIELDS}
    if disabled != 'human_amount_review':
        apply_amount_review(fields, [], False)
    return {name: field.model_dump() for name, field in fields.items()}


def replay(source):
    if source.get('set') not in {'dev', 'adversarial'} or source.get('status') != 'completed':
        raise ValueError('Only completed development/adversarial reports may be replayed')
    rows = source['records']
    if not rows or len(rows) != source['planned_records']:
        raise ValueError('Incomplete report')
    today = date.fromisoformat(source['config']['today'])
    modes = ('full',) + tuple('without_' + group for group in GROUPS)
    outputs = {mode: [] for mode in modes}
    for row in rows:
        if row.get('error') or row['methods']['full'].get('error'):
            raise ValueError('Unavailable reference extraction')
        if row.get('human_amount_review') is not False:
            raise ValueError('Replay requires explicit unattended amount-review state')
        proposal = row.get('proposal')
        if proposal:
            # Typed document proposals include doc_type, which is not a fact field.
            proposal = {key: value for key, value in proposal.items() if key != 'doc_type'}
            proposal = ProposedNotice.model_validate(proposal)
        elif row['selected_type'] != 'unknown':
            raise ValueError('Missing saved extraction proposal')
        for mode in modes:
            fields = (validate(proposal, row['confirmed_text'], today,
                               None if mode == 'full' else mode.removeprefix('without_'))
                      if proposal else deepcopy(row['methods']['full']['fields']))
            if mode == 'full':
                # Refuse to silently compare a changed validator against old results.
                for name in FIELDS:
                    old = row['methods']['full']['fields'][name]
                    if any(fields[name].get(key) != old.get(key) for key in
                           ('value', 'status', 'normalized_value')):
                        raise ValueError('Reference replay drift; generate a new development report')
            copied = {key: deepcopy(row[key]) for key in
                      ('sample', 'variant', 'repetition', 'expected', 'expected_state')}
            copied['expected_aliases'] = row.get('expected_aliases', {})
            copied['methods'] = {'full': {'fields': fields, 'error': None}}
            outputs[mode].append(copied)
    results = {}
    for mode, records in outputs.items():
        results[mode] = {'summary': summarize(records)['full'], 'records': records}
    return {'set': source['set'], 'status': 'completed', 'scorer_version': VERSION,
            'source_sha256': source_fingerprint(), 'reference_source_sha256': source['code_sha256'],
            'record_count': len(rows), 'groups': list(GROUPS), 'model_calls': 0,
            'protocol': __doc__, 'results': results}


def markdown(report):
    lines = ['# Validator ablation: ' + report['set'], '',
             f"{report['record_count']} saved records; zero new model/OCR calls. Same proposals, text, truth, scorer and human-review state in every row.", '',
             'Each mode disables one named group; all other groups stay active. Schema and unknown-type abstention stay active. Date validation includes calendar parsing, source equality, conflicting dates and relative-anchor checks. Explanation guards are outside this field-only experiment.', '',
             '| Mode | Critical false verified | Present-field accuracy | Verified correct | Abstain when present | Correct MISSING |',
             '|---|---|---|---|---|---|']
    for mode, result in report['results'].items():
        metrics = result['summary']['headline_critical']
        keys = ('false_verified_rate', 'field_accuracy', 'usable_verified_accuracy',
                'abstain_when_truth_exists', 'correct_to_say_missing')
        lines.append('| ' + mode + ' | ' + ' | '.join(display(metrics[key]) for key in keys) + ' |')
    lines += ['', '| Mode | Field | Accuracy | False verified | Abstain when present |',
              '|---|---|---|---|---|']
    for mode, result in report['results'].items():
        for name, metrics in result['summary']['per_field'].items():
            lines.append('| ' + mode + ' | ' + name + ' | ' + ' | '.join(display(metrics[key]) for key in
                         ('field_accuracy', 'false_verified_rate', 'abstain_when_truth_exists')) + ' |')
    lines += ['', 'An unchanged row means other checks still blocked the saved proposals, or that this set did not exercise the disabled group. It does not prove that validator is unnecessary. Amount-review removal measures reduced abstention; it does not establish pixel-level OCR correctness.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    # Refuse held-out paths before opening files, even if their contents are relabeled.
    if any('heldout' in str(path.resolve()).lower() or 'held-out' in str(path.resolve()).lower()
           for path in (args.input, args.out)):
        parser.error('Held-out paths are not supported')
    if args.out.exists() or args.out.with_suffix('.md').exists():
        parser.error('Use a fresh output path')
    data = args.input.read_bytes()
    result = replay(json.loads(data))
    result['input_sha256'] = hashlib.sha256(data).hexdigest()
    result['input_report'] = str(args.input.resolve())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    rendered = markdown(result)
    args.out.with_suffix('.md').write_text(rendered)
    print(rendered)


if __name__ == '__main__':
    main()
