"""A2 adapters, actual candidate provenance, candidate scoring, and privacy."""

import io
import tempfile
from pathlib import Path
from types import SimpleNamespace

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from backend.hybrid_reader import HybridReader
from backend.main import app, get_reader, Settings
from backend.preprocessed_reader import PreprocessedReader, preprocess, estimate_skew
from backend.reader_tokens import compare_candidates, candidates, normalize_candidate
from backend.readers import ReaderError, Reading, make_reader
from eval.reader_bakeoff import score_shown_candidates, score_text, MemoryReader


def stub(name, text=None, fail=False):
    def read(_):
        if fail:
            raise ReaderError("synthetic reader unavailable")
        return Reading(text or "", [])
    return SimpleNamespace(name=name, read=read)


@pytest.mark.parametrize("wrong", ["2026-10-28", "2026-1O-29", "2026-l0-29", "2026-10-2S"])
def test_wrong_date_digit_is_disputed_and_both_candidates_are_kept(wrong):
    left, right = "Deadline: 2026-10-29", "Deadline: " + wrong
    reading = HybridReader(stub("local", left), stub("vision", right)).read(b"synthetic")
    review = reading.token_reviews[0]
    assert review["status"] == ("disputed" if wrong == "2026-10-28" else "uncertain")
    assert {item["value"] for item in review["candidates"]} == {"2026-10-29", wrong}
    for item in review["candidates"]:
        source = left if item["reader"] == "local" else right
        assert source[item["start"]:item["end"]] == item["value"]


@pytest.mark.parametrize("left,right", [
    ("Pay $45.00", "Pay $45.01"),
    ("Pay $45.00", "Pay $4S.00"),
    ("Pay $45.00", "Pay -$45.00"),
    ("Case: TEST-001", "Case: TEST-OO1"),
])
def test_amount_and_id_disagreement_never_repairs_digits(left, right):
    reviews = compare_candidates(left, right, "local", "vision")
    assert reviews
    assert all(review["status"] == "disputed" for review in reviews)


def test_agreement_tolerates_formatting_but_is_not_field_verification():
    left = "Amount due: $1,234.50\nReference: DEMO-001\nDeadline: 2026-10-29"
    right = "Amount due: 1234.50\nReference: demo - 001\nDeadline: 2026 - 10 - 29"
    reviews = compare_candidates(left, right, "local", "vision")
    assert len(reviews) == 3
    assert all(review["status"] == "agreed" for review in reviews)
    assert all("verified" not in review.values() for review in reviews)


def test_duplicate_values_need_evidence_from_both_readers():
    reviews = compare_candidates("2026-10-29 again 2026-10-29", "2026-10-29", "local", "vision")
    assert [review["status"] for review in reviews].count("agreed") == 1
    assert [review["status"] for review in reviews].count("disputed") == 1


@pytest.mark.parametrize("local_fails", [True, False])
def test_failed_component_never_creates_agreement(local_fails):
    reader = HybridReader(stub("local", "Pay $45.00", fail=local_fails),
                          stub("vision", "Pay $45.00", fail=not local_fails))
    reading = reader.read(b"synthetic")
    assert all(review["status"] == "disputed" for review in reading.token_reviews)
    assert any("failed" in warning for warning in reading.warnings)
    assert reading.primary_reader == ("vision" if local_fails else "local")


def test_both_reader_failures_are_public_safe():
    with pytest.raises(ReaderError, match="Both text readers failed"):
        HybridReader(stub("local", fail=True), stub("vision", fail=True)).read(b"x")


def test_empty_local_transcript_does_not_hide_a_readable_vision_transcript():
    result = HybridReader(stub("local", ""), stub("vision", "Pay $45.00")).read(b"x")
    assert result.text == "Pay $45.00"
    assert result.primary_reader == "vision"
    assert all(review["status"] == "disputed" for review in result.token_reviews)


def test_candidate_recall_uses_alternative_actually_returned_for_display():
    truth, primary = "Pay $45.00", "Pay $45.01"
    reading = HybridReader(stub("local", primary), stub("vision", truth)).read(b"x")
    assert score_text(truth, reading.text)["key_token_recall"] == 0
    assert score_shown_candidates(truth, reading.token_reviews)["candidate_key_token_recall"] == 1
    assert score_shown_candidates(truth, [])["candidate_key_token_recall"] == 0


def test_one_candidate_group_cannot_cover_two_distinct_or_duplicate_targets():
    truth = "2026-10-29 and 2026-10-30"
    reviews = [{"kind": "date", "status": "disputed", "candidates": [{"value": "2026-10-29"}, {"value": "2026-10-30"}]}]
    assert score_shown_candidates(truth, reviews)["candidate_key_token_recall"] == 0.5
    duplicate = "2026-10-29 and 2026-10-29"
    assert score_shown_candidates(duplicate, reviews)["candidate_key_token_recall"] == 0.5


def test_memory_cache_is_shared_without_writing_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    calls = []
    reader = MemoryReader(SimpleNamespace(name="test", read=lambda data: calls.append(data) or Reading("synthetic", [])))
    assert reader.read(b"same").text == "synthetic"
    assert reader.read(b"same").text == "synthetic"
    assert len(calls) == 1
    assert list(tmp_path.iterdir()) == []
    reader.cache.clear()
    assert not reader.cache


def test_preprocessing_is_grayscale_binary_upscaled_and_in_memory():
    image = Image.new("RGB", (240, 120), "white")
    ImageDraw.Draw(image).text((20, 35), "Synthetic page", fill="black")
    out = io.BytesIO()
    image.save(out, "JPEG")
    png, _ = preprocess(out.getvalue())
    with Image.open(io.BytesIO(png)) as result:
        assert result.mode == "L"
        assert result.size == (520, 280)  # 2x plus 20px borders on each side.
        assert set(result.getdata()) <= {0, 255}


def test_deskew_sign_and_estimate_on_known_rotated_lines():
    image = Image.new("L", (800, 600), "white")
    draw = ImageDraw.Draw(image)
    for y in range(80, 520, 35):
        draw.line((80, y, 720, y), fill="black", width=3)
    rotated = image.rotate(3.5, resample=Image.Resampling.BICUBIC, fillcolor=255)
    angle = estimate_skew(np.asarray(rotated))
    assert -4.2 < angle < -2.8
    matrix = cv2.getRotationMatrix2D((400, 300), angle, 1)
    corrected = cv2.warpAffine(np.asarray(rotated), matrix, (800, 600), borderValue=255)
    assert abs(estimate_skew(corrected)) < 0.6


def test_blank_page_does_not_invent_a_skew():
    assert estimate_skew(np.full((150, 250), 255, dtype=np.uint8)) == 0


def test_bad_preprocessing_input_is_a_safe_error():
    with pytest.raises(ReaderError, match="preprocessing failed"):
        preprocess(b"not an image")


@pytest.mark.parametrize("mode", ["preprocessed", "hybrid"])
def test_readers_remain_selectable_with_student_chosen_default(mode):
    settings = Settings("", "", reader=mode)
    assert make_reader(settings).name == mode
    assert Settings("", "").reader == "preprocessed"


def test_hybrid_api_returns_all_candidates_and_no_store_headers():
    image = Image.new("RGB", (100, 100), "white")
    out = io.BytesIO()
    image.save(out, "JPEG")
    reader = HybridReader(stub("local", "Pay $45.01"), stub("vision", "Pay $45.00"))
    app.dependency_overrides[get_reader] = lambda: reader
    try:
        response = TestClient(app).post("/api/read", files={"image": ("synthetic.jpg", out.getvalue())})
        assert response.status_code == 200
        data = response.json()
        assert data["primary_reader"] == "local"
        assert {item["value"] for item in data["token_reviews"][0]["candidates"]} == {"$45.00", "$45.01"}
        assert data["token_reviews"][0]["status"] == "disputed"
        assert response.headers["cache-control"] == "no-store"
    finally:
        app.dependency_overrides.clear()


def test_real_preprocessed_ocr_leaves_no_notice_files(tmp_path, monkeypatch, caplog):
    sample = Path(__file__).resolve().parents[1] / "eval/samples/degraded/parking_01__shadow.jpg"
    data = sample.read_bytes()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    def forbid(*args, **kwargs):
        raise AssertionError("Unexpected disk-backed notice temp file")
    monkeypatch.setattr(tempfile, "TemporaryFile", forbid)
    monkeypatch.setattr(tempfile, "NamedTemporaryFile", forbid)
    app.dependency_overrides[get_reader] = lambda: PreprocessedReader()
    try:
        response = TestClient(app).post("/api/read", files={"image": ("private-photo.jpg", data)})
        assert response.status_code == 200
        assert response.json()["reader"] == "preprocessed"
        assert list(tmp_path.iterdir()) == []
        assert "Invented Resident" not in caplog.text
        assert "private-photo" not in caplog.text
    finally:
        app.dependency_overrides.clear()
