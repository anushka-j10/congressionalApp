"""Toy markers exercise scoring without authoring the student's real signals."""

import pytest
from backend.classifier.scoring import classify
from backend.classifier.signals import Signal


def test_weighted_match_is_case_insensitive_and_scores_once():
    rules = {"parking_ticket": (Signal("toy alpha marker", r"\bALPHA\b", 4),),
             "court_notice": (Signal("toy beta marker", r"\bBETA\b", 2),)}
    result = classify("alpha ALPHA alphabet", rules)
    assert result.doc_type == "parking_ticket"
    assert result.confidence == 0.571
    assert result.signals == ["parking_ticket: toy alpha marker (+4)"]


@pytest.mark.parametrize("text,rules", [
    ("unrelated", {"school_letter": (Signal("marker", "ALPHA", 4),)}),
    ("ALPHA", {"school_letter": (Signal("weak marker", "ALPHA", 1),)}),
    ("ALPHA BETA", {"school_letter": (Signal("a", "ALPHA", 4),), "utility_bill": (Signal("b", "BETA", 4),)}),
    ("ALPHA BETA", {"school_letter": (Signal("a", "ALPHA", 4),), "utility_bill": (Signal("b", "BETA", 3.5),)}),
])
def test_no_match_weak_match_ties_and_ambiguity_are_unknown(text, rules):
    result = classify(text, rules)
    assert result.doc_type == "unknown"
    assert 0 <= result.confidence < 0.5


def test_pattern_and_all_competing_signals_are_reported():
    rules = {"court_notice": (Signal("toy numbered marker", r"ALPHA-\d{3}", 6),),
             "utility_bill": (Signal("toy beta", "BETA", 1),)}
    result = classify("ALPHA-123 BETA", rules)
    assert result.doc_type == "court_notice"
    assert len(result.signals) == 2


@pytest.mark.parametrize("weight", [-1, 0, float("inf"), float("nan")])
def test_invalid_weights_are_rejected(weight):
    with pytest.raises(ValueError):
        classify("ALPHA", {"school_letter": (Signal("toy", "ALPHA", weight),)})
