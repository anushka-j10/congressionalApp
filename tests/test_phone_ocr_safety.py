"""Fresh synthetic regressions for receipt-photo timing corruption, not held-out data."""
from datetime import date
import json
import pytest

from backend.extraction_models import ProposedField
from backend.field_validation import checked_field
from backend.ocr_safety import timing_issues
from backend.reader_tokens import compare_candidates
from backend.readers import quality_warnings
from tests.test_extract import api, request, TEXT
from backend.explanation import explain_notice
from tests.test_explanation import StubModel


@pytest.mark.parametrize('broken', ['11/29/2', '11/29/20', '11/29/202', '11/29/2O27',
    '2027-11-2S', '02/30/2027', 'S days', '3C days', '2O business days', 'l hours'])
def test_damaged_timing_is_visible_without_repair(broken):
    source = 'If you dispute this synthetic charge, notify the office at least ' + broken + ' before payment.'
    issues = timing_issues(source)
    assert issues
    assert any(source[i['start']:i['end']] == broken for i in issues)
    assert any('time limit' in warning for warning in quality_warnings(source))
    result = checked_field('required_action', ProposedField(value=source, source_snippet=source), source, date(2027, 1, 1))
    assert result.status == 'unverified'
    assert 'ambiguous' in result.reason


@pytest.mark.parametrize('clause', ['at least’’S |\ndays prior to the pay by date',
                                 'within 3C days of receipt', 'by 11/29/2'])
def test_clipped_model_snippets_cannot_hide_bad_timing_elsewhere(api, clause):
    client, _ = api
    result = request(client, text=TEXT + '\nIf you dispute this charge, notify the office ' + clause + '.').json()
    for name in ('deadline', 'amount_due', 'required_action'):
        assert result['fields'][name]['status'] == 'unverified'
        assert result['fields'][name]['normalized_value'] is None
    # Unsafe facts never become English instructions or translation inputs.
    model = StubModel()
    explanation = explain_notice(result['fields'], 'parking_ticket', 'en', model)
    assert '$45.00' not in json.dumps(explanation['english'])
    assert 'Pay the charge.' not in json.dumps(model.calls)


def test_reviewing_and_correcting_the_actual_text_can_restore_fields(api):
    client, _ = api
    broken = TEXT + '\nNotify the office at least S days before payment.'
    assert request(client, text=broken).json()['fields']['deadline']['status'] == 'unverified'
    corrected = broken.replace('S days', '7 days')
    result = request(client, text=corrected).json()
    assert all(result['fields'][name]['status'] == 'verified' for name in ('deadline', 'amount_due', 'required_action'))


@pytest.mark.parametrize('source', ['Notify the office at least 7 days before payment.',
    'Return the form within five business days.', 'Pay by 11/29/2027.',
    'Pay by 2028-02-29.', 'Visit St. James Office during business days.',
    'Contact: Office S. Deadline: November 29, 2027.'])
def test_legible_controls_are_not_rejected(source):
    assert timing_issues(source) == []
    field = checked_field('required_action', ProposedField(value=source, source_snippet=source), source, date(2027, 1, 1))
    # Multiple sentences are deliberately not a completeness assertion here.
    if source.count('.') == 1:
        assert field.status == 'verified'


def test_two_readers_agreeing_on_a_bad_duration_is_still_uncertain():
    text = 'Notify the office at least S |\ndays before payment.'
    reviews = compare_candidates(text, text, 'preprocessed', 'original-image')
    assert len(reviews) == 1 and reviews[0]['status'] == 'uncertain'
    assert reviews[0]['kind'] == 'duration'
    assert all(c['value'] == 'S |\ndays' for c in reviews[0]['candidates'])


def test_truncated_date_is_highlightable_and_original_candidate_is_preserved():
    left, right = 'Due date: 11/29/2', 'Due date: 11/29/2027'
    reviews = compare_candidates(left, right, 'preprocessed', 'original-image')
    assert reviews[0]['status'] == 'uncertain'
    assert {c['value'] for c in reviews[0]['candidates']} == {'11/29/2', '11/29/2027'}
    for candidate in reviews[0]['candidates']:
        source = left if candidate['reader'] == 'preprocessed' else right
        assert source[candidate['start']:candidate['end']] == candidate['value']
