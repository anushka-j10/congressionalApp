"""Offline corpus integrity and stress-test scoring, no live model requests."""
from collections import Counter
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path

import pytest

from eval.northeast_stress import run
from eval.northeast_stress.cases import CASES
from eval.scoring import score_field


def test_two_notices_per_state_and_two_images_each_with_frozen_answers():
    manifest,items=run.load_corpus()
    assert Counter(c['state'] for c in items)==dict.fromkeys(['CT','ME','MA','NH','NJ','NY','PA','RI','VT'],2)
    assert len({c['id'] for c in items})==18
    assert sum(len(c['variants']) for c in items)==36
    assert manifest['protocol']['human_amount_review'] is False
    assert manifest['independent_heldout'] is False
    assert [c['expected'] for c in items]==[c['expected'] for c in CASES]


def test_annotation_cannot_silently_change_after_rendering(tmp_path,monkeypatch):
    sample=tmp_path/'sample.json';sample.write_text('{}')
    manifest={'synthetic':True,'independent_heldout':False,
              'files':{'sample.json':hashlib.sha256(sample.read_bytes()).hexdigest()},'cases':[]}
    (tmp_path/'manifest.json').write_text(json.dumps(manifest))
    sample.write_text('{"changed":true}')
    monkeypatch.setattr(run,'DATA',tmp_path)
    with pytest.raises(ValueError,match='integrity'):run.load_corpus()


def test_action_and_contact_truth_are_visible_not_added_by_the_answer_key():
    for c in CASES:
        text=' '.join(c['paragraphs']).casefold()
        assert c['expected']['required_action'].casefold() in text
        assert c['expected']['contact'].casefold() in text


def test_inclusive_day_count_has_independent_expected_date():
    case=next(c for c in CASES if c['id']=='VT_02')
    assert case['expected']['deadline']==(date(2026,10,26)+timedelta(days=13)).isoformat()
    wrong=score_field('deadline',case['expected']['deadline'],'present',
                     {'value':'within 14 days','normalized_value':'2026-11-09','status':'verified'})
    assert wrong['false_verified'] is True


@pytest.mark.parametrize('id',['ME_01','NH_01','RI_02'])
def test_absent_deadline_does_not_credit_issue_registration_or_response_date(id):
    c=next(c for c in CASES if c['id']==id)
    assert c['expected']['deadline'] is None
    assert c['expected_state']['deadline']=='missing'
    result=score_field('deadline',None,'missing',{'value':'2026-10-26','status':'verified'})
    assert result['false_verified'] is True
    unavailable=score_field('deadline',None,'missing',{},unavailable=True)
    assert unavailable['wrong'] is True
    assert unavailable['correct_to_say_missing'] is False


def test_no_stress_entry_point_loads_or_runs_the_heldout_set():
    source=Path(run.__file__).read_text()
    assert 'load_set(' not in source
    assert 'acquire_heldout' not in source
    assert 'eval/heldout' not in source
