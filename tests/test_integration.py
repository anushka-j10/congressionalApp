"""Real OCR through POST /api/read; this is not the Milestone 4 eval scorer."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.classifier.signals import SIGNALS


def test_all_eight_synthetic_notices():
    samples = Path(__file__).resolve().parents[1] / "eval/samples"
    expected_files = sorted(samples.glob("*.json"))
    assert len(expected_files) == 8
    print("\nREAL READER — student signal lists " + ("present" if any(SIGNALS.values()) else "EMPTY; unknown predictions expected"))
    print(f"{'sample':<13} {'expected':<16} {'predicted':<16} {'confidence':<11} reader")
    print("-" * 78)
    with TestClient(app) as client:
        for expected_file in expected_files:
            expected = json.loads(expected_file.read_text())
            response = client.post("/api/read", files={"image": (expected_file.stem + ".png", expected_file.with_suffix(".png").read_bytes(), "image/png")})
            assert response.status_code == 200, response.text
            result = response.json()
            print(f"{expected_file.stem:<13} {expected['doc_type']:<16} {result['doc_type']:<16} {result['doc_type_confidence']:<11.3f} {result['reader']}")
            print("  signals: " + ("; ".join(result["signals"]) or "none"))
            assert len(result["text"]) > 100
            assert "SYNTHETIC" in result["text"].upper()
            assert 0 <= result["doc_type_confidence"] <= 1
            if not any(SIGNALS.values()):
                assert result["doc_type"] == "unknown"
                assert result["signals"] == []
