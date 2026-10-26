"""Evaluation controls stay separate from production request behavior."""
from copy import deepcopy
from datetime import date
import json
from pathlib import Path

import pytest
from backend.extraction_models import ProposedNotice, ProposedField, ProposedDeadline, ExtractRequest
from backend.field_validation import VALIDATOR_GROUPS, _checked_field, checked_field
from eval.ablations import GROUPS, replay, validate
from pydantic import ValidationError

TODAY = date(2028, 1, 1)


def deadline(value, snippet):
    return ProposedDeadline(value=value, source_snippet=snippet, kind='absolute',
                            relative_days=None, anchor_date=None, anchor_source_snippet=None)


CASES = [
    ('source_match', 'contact', ProposedField(value='Example Desk', source_snippet='Example Desk'), 'Information only.'),
    ('evidence_context', 'deadline', deadline('March 2, 2028', 'Issued: March 2, 2028'), 'Issued: March 2, 2028'),
    ('readability', 'contact', ProposedField(value='[unreadable]', source_snippet='[unreadable]'), 'Contact: [unreadable]'),
    ('date_validation', 'deadline', deadline('February 30, 2028', 'Deadline: February 30, 2028'), 'Deadline: February 30, 2028'),
    ('amount_validation', 'amount_due', ProposedField(value='$26.45', source_snippet='Amount due: $27.45'), 'Amount due: $27.45'),
    ('text_copy', 'contact', ProposedField(value='Invented Desk', source_snippet='Contact: Example Desk'), 'Contact: Example Desk'),
    ('action_completeness', 'required_action', ProposedField(value='Mail the form', source_snippet='Mail the form'), 'Mail the form by Friday.'),
]


@pytest.mark.parametrize('group,name,proposal,text', CASES)
def test_each_switch_disables_only_its_check(group, name, proposal, text):
    assert checked_field(name, proposal, text, TODAY).status == 'unverified'
    for disabled in VALIDATOR_GROUPS:
        result = _checked_field(name, proposal, text, TODAY, frozenset({disabled}))
        assert result.status == ('verified' if disabled == group else 'unverified'), disabled


def test_human_gate_is_independent_and_production_default_stays_closed():
    absent = {'value': None, 'source_snippet': None}
    proposal = ProposedNotice.model_validate({
        'issuing_agency': absent, 'required_action': absent, 'contact': absent,
        'deadline': {**absent, 'kind': None, 'relative_days': None, 'anchor_date': None, 'anchor_source_snippet': None},
        'amount_due': {'value': '$26.45', 'source_snippet': 'Amount due: $26.45'}})
    for group in (None,) + GROUPS:
        fields = validate(proposal, 'Amount due: $26.45', TODAY, group)
        assert fields['amount_due']['status'] == ('verified' if group == 'human_amount_review' else 'unverified')


@pytest.mark.parametrize('key', ['disabled', 'validators', 'disabled_validators'])
def test_request_cannot_disable_validators(key):
    with pytest.raises(ValidationError):
        ExtractRequest.model_validate({'text': 'Info', 'doc_type': 'unknown', 'text_confirmed': True, key: ['source_match']})


def test_unknown_switch_rejected():
    with pytest.raises(ValueError):
        _checked_field('contact', ProposedField(value='Desk', source_snippet='Desk'), 'Desk', TODAY, frozenset({'typo'}))


def test_replay_keeps_missing_unknown_fields_and_reference_results():
    source = json.loads(Path('results/m4-verification/dev.json').read_text())
    result = replay(source)
    assert result['record_count'] == 40 and result['model_calls'] == 0
    for mode, data in result['results'].items():
        assert len(data['records']) == 40
        for row, original in zip(data['records'], source['records']):
            assert row['expected'] == original['expected']
            if original['selected_type'] == 'unknown':
                assert row['methods']['full']['fields'] == original['methods']['full']['fields']
    bad = deepcopy(source)
    bad['records'][0]['methods']['full']['fields']['contact']['status'] = 'mismatch'
    with pytest.raises(ValueError, match='drift'):
        replay(bad)


@pytest.mark.parametrize('set_name', ['heldout', 'other'])
def test_replay_refuses_non_development_sets(set_name):
    with pytest.raises(ValueError):
        replay({'set': set_name, 'status': 'completed'})


def test_source_ablation_handles_nullable_snippet_without_inventing_source_span():
    result = _checked_field('contact', ProposedField(value='Example Desk', source_snippet=None),
                            'Info only.', TODAY, frozenset({'source_match'}))
    assert result.status == 'unverified'  # Copy check remains enabled.
    assert result.source_start is None and result.source_snippet is None
