"""Metric and fixture checks only; no production reader tuning."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from eval.generate_reader_samples import VARIANTS, degrade
from eval.generate_samples import SAMPLES, render_clean
from eval.reader_bakeoff import (
    Sample, discover_samples, edit_distance, evaluate_reader, key_tokens,
    score_text, summarize,
)

ROOT = Path(__file__).resolve().parents[1] / "eval/samples"


def test_exact_levenshtein_distance_and_layout_normalization():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3
    result = score_text("One\n two\tthree", "One two   three")
    assert result["cer"] == 0
    assert score_text("a", "aaaa")["cer"] == 3  # Insertion-heavy CER may exceed 100%.
    assert score_text("A", "a")["cer"] == 1  # Case remains significant for CER.


def test_extracts_dates_money_and_labeled_identifiers():
    truth = "Issued: 2026-10-21\nDeadline: 11/30/2026\nPay $1,234.50.\nCase No: DEMO-001\n"
    tokens = key_tokens(truth)
    assert [token.kind for token in tokens] == ["date", "date", "amount", "id"]
    assert tokens[2].value == "$1,234.50"
    result = score_text(truth, truth)
    assert result["key_tokens"] == result["key_tokens_matched"] == 4
    assert len(result["target_tokens"]) == 4
    assert result["cer"] == 0


@pytest.mark.parametrize("truth,output", [
    ("Deadline: 2026-10-29", "Deadline: 2026-10-28"),
    ("Deadline: 2026-10-29", "Deadline: 2026-1O-29"),
    ("Deadline: 11/30/2026", "Deadline: ll/30/2026"),
    ("Pay $45.00", "Pay $4S.00"),
    ("Pay $45.00", "Pay $45.0O"),
    ("Pay $45.00", "Pay $45.01"),
    ("Case: TEST-001", "Case: TEST-OO1"),
    ("Case: TEST-001", "Case: TEST-0012"),
    ("Case: TEST-001", "Case: PREFIXTEST-001"),
])
def test_digit_swaps_and_prefixes_never_get_credit(truth, output):
    result = score_text(truth, output)
    assert result["key_tokens"] == 1
    assert result["key_tokens_matched"] == 0
    assert result["key_token_recall"] == 0


def test_cosmetic_separators_and_lost_currency_symbol_can_match():
    truth = "Deadline: 2026-10-29\nPay $1,234.50\nReference: DEMO-001"
    output = "Deadline: 2026 - 10 - 29\nPay 1234.50\nReference: demo - 001"
    assert score_text(truth, output)["key_token_recall"] == 1


def test_month_name_dates_are_targets():
    result = score_text("Due: November 30, 2026", "Due: November 30, 2026")
    assert result["key_tokens"] == 1
    assert result["key_token_recall"] == 1


def test_repeated_ground_truth_tokens_require_repeated_output():
    result = score_text("Date: 11/30/2026\nAgain: 11/30/2026", "Date: 11/30/2026")
    assert result["key_token_recall"] == 0.5
    assert result["missed_tokens"][0]["missing_occurrences"] == 1


def test_two_money_regexes_do_not_count_one_occurrence_twice():
    result = score_text("Pay $45.00 and confirm $45.00", "Pay $45.00")
    assert result["key_token_recall"] == 0.5


def test_empty_ground_truth_is_an_error_and_no_targets_is_not_a_pass():
    with pytest.raises(ValueError):
        score_text(" \n", "hello")
    assert score_text("hello world", "hello world")["key_token_recall"] is None


def test_easy_boilerplate_does_not_hide_a_wrong_critical_digit():
    boilerplate = "This fictional notice has harmless repetitive words. " * 20
    result = score_text(boilerplate + "Pay $45.00", boilerplate + "Pay $45.01")
    assert result["cer"] < 0.01
    assert result["key_token_recall"] == 0


def write_pair(root, condition="handwriting", suffix=".txt"):
    folder = root / condition
    folder.mkdir(parents=True, exist_ok=True)
    image = folder / "synthetic.JPG"
    Image.new("RGB", (100, 100), "white").save(image)
    truth = image.with_name("synthetic" + suffix)
    truth.write_text("Deadline: 2026-10-29\nPay $45.00\nReference: DEMO-001")
    return image, truth


@pytest.mark.parametrize("suffix", [".txt", ".gt.txt"])
def test_handwriting_is_auto_discovered_only_with_ground_truth(tmp_path, suffix):
    assert discover_samples(tmp_path) == ([], [])
    image, truth = write_pair(tmp_path, suffix=suffix)
    samples, problems = discover_samples(tmp_path)
    assert not problems
    assert len(samples) == 1
    assert samples[0].condition == "handwriting"
    assert samples[0].truth == truth
    truth.unlink()
    assert discover_samples(tmp_path)[1]


@pytest.mark.parametrize("problem", ["empty", "duplicate", "orphan"])
def test_bad_pairs_are_explicit_instead_of_silently_excluded(tmp_path, problem):
    image, truth = write_pair(tmp_path)
    if problem == "empty":
        truth.write_text("")
    elif problem == "duplicate":
        image.with_name("synthetic.gt.txt").write_text(truth.read_text())
    else:
        image.unlink()
    assert discover_samples(tmp_path)[1]


def test_real_corpus_has_eight_clean_fifty_six_degraded_eight_legacy():
    samples, problems = discover_samples(ROOT)
    assert not problems
    assert sum(sample.condition == "clean" for sample in samples) == 8
    assert sum(sample.condition == "degraded" for sample in samples) == 56
    assert sum(sample.condition == "legacy_m1" for sample in samples) == 8
    assert {sample.variant for sample in samples if sample.condition == "degraded"} == set(VARIANTS)
    # Do not assert handwriting is absent: students should be able to add it.
    for sample in samples:
        if sample.condition != "handwriting":
            assert len(key_tokens(sample.truth.read_text())) in {3, 4}


def test_shared_renderer_preserves_original_clean_m1_images():
    for index, (name, _, title, deadline, amount, action, photo) in enumerate(SAMPLES):
        if photo:
            continue
        image, _ = render_clean(index, title, deadline, amount, action)
        with Image.open(ROOT / f"{name}.png") as original:
            assert image.tobytes() == original.tobytes()


@pytest.mark.parametrize("variant", VARIANTS)
def test_degradations_are_repeatable_for_a_fixed_seed(variant):
    image = Image.new("RGB", (120, 160), "white")
    first, second = degrade(image, variant, 42), degrade(image, variant, 42)
    assert first.tobytes() == second.tobytes()


def test_reader_failure_is_counted_and_does_not_leak_exception_contents(tmp_path):
    image, truth = write_pair(tmp_path, "clean")
    def fail(_):
        raise RuntimeError("PRIVATE PROVIDER RESPONSE")
    rows = evaluate_reader(SimpleNamespace(name="test", read=fail), [Sample(image, truth, "clean", "clean")])
    assert rows[0]["error"] == "read_failed"
    assert rows[0]["cer"] == 1
    assert rows[0]["key_token_recall"] == 0
    assert "PRIVATE PROVIDER" not in json.dumps(rows)
    summary = summarize(rows, "clean")
    assert summary["errors"] == 1
    assert summarize(rows, "handwriting")["cer"] is None


def test_aggregate_recall_weights_tokens_not_sample_averages():
    rows = [
        {"condition": "clean", "ground_truth_characters": 10, "character_edits": 0,
         "key_tokens": 1, "key_tokens_matched": 0, "error": None},
        {"condition": "clean", "ground_truth_characters": 90, "character_edits": 10,
         "key_tokens": 9, "key_tokens_matched": 9, "error": None},
    ]
    result = summarize(rows, "clean")
    assert result["cer"] == 0.1
    assert result["key_token_recall"] == 0.9
