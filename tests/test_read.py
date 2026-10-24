"""Image, provider-contract, upload, and no-leftover-data regression tests."""

import io
import logging
import os
import random
import tempfile
from pathlib import Path
from unittest.mock import Mock

import httpx
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
from pillow_heif import from_pillow

from backend import images, readers
from backend.main import app, get_reader, Settings
from backend.readers import Reading, ReaderError, TesseractReader, VisionReader, quality_warnings

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def photo_bytes(fmt="JPEG", orientation=None):
    image = Image.new("RGB", (240, 120), "white")
    ImageDraw.Draw(image).rectangle((0, 0, 70, 50), fill="red")
    out = io.BytesIO()
    exif = Image.Exif()
    if orientation:
        exif[274] = orientation
        exif[270] = "synthetic metadata must disappear"
    if fmt == "HEIF":
        from_pillow(image).save(out, quality=90, exif=exif.tobytes())
    else:
        image.save(out, format=fmt, exif=exif)
    return out.getvalue()


@pytest.fixture
def fake_reader():
    reader = Mock(name="test reader")
    reader.name = "test-only"
    reader.read.return_value = Reading("Synthetic readable page with enough words for a useful notice transcription.", [])
    app.dependency_overrides[get_reader] = lambda: reader
    yield reader
    app.dependency_overrides.clear()


@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "WEBP", "HEIF"])
def test_real_formats_are_decoded_and_reencoded_without_metadata(fmt):
    output = images.normalize_image(photo_bytes(fmt))
    with Image.open(io.BytesIO(output)) as image:
        assert image.format == "JPEG"
        assert image.size == (240, 120)
        assert not image.getexif()


@pytest.mark.parametrize("orientation", [2, 3, 4, 5, 6, 7, 8])
def test_exif_rotation_and_mirroring(orientation):
    from PIL import ImageOps
    raw = photo_bytes(orientation=orientation)
    with Image.open(io.BytesIO(raw)) as original:
        expected = ImageOps.exif_transpose(original).convert("RGB")
    with Image.open(io.BytesIO(images.normalize_image(raw))) as actual:
        assert actual.size == expected.size
        # Sample centers of all four quadrants, away from compression edges.
        for x in [actual.width // 4, actual.width * 3 // 4]:
            for y in [actual.height // 4, actual.height * 3 // 4]:
                assert max(abs(a - b) for a, b in zip(actual.getpixel((x, y)), expected.getpixel((x, y)))) < 25
        assert not actual.getexif()


def test_heic_orientation_is_applied_once():
    output = images.normalize_image(photo_bytes("HEIF", orientation=6))
    with Image.open(io.BytesIO(output)) as image:
        assert image.size == (120, 240)
        assert image.getpixel((90, 35))[0] > 180  # Red marker rotates to top right.
        assert image.getpixel((90, 35))[1] < 100


def test_server_downscales_large_dimensions():
    out = io.BytesIO()
    Image.new("RGB", (2400, 1200), "white").save(out, "PNG")
    with Image.open(io.BytesIO(images.normalize_image(out.getvalue()))) as image:
        assert image.size == (1600, 800)


@pytest.mark.parametrize("data", [b"not an image", b"<svg xmlns='http://www.w3.org/2000/svg'/>", b"\xff\xd8truncated"])
def test_fake_images_are_rejected(data):
    with pytest.raises(HTTPException) as error:
        images.normalize_image(data)
    assert error.value.status_code == 415


def test_pixel_bomb_is_rejected(monkeypatch):
    monkeypatch.setattr(images, "MAX_PIXELS", 100)
    with pytest.raises(HTTPException) as error:
        images.normalize_image(photo_bytes())
    assert error.value.status_code == 413


def test_animated_file_is_rejected():
    out = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(out, "WEBP", save_all=True,
        append_images=[Image.new("RGB", (100, 100), "black")], duration=100, loop=0)
    with pytest.raises(HTTPException) as error:
        images.normalize_image(out.getvalue())
    assert error.value.status_code == 415


def test_upload_contract_and_no_cache(fake_reader):
    response = client.post("/api/read", files={"image": ("synthetic.jpg", photo_bytes(), "image/jpeg")})
    assert response.status_code == 200
    assert set(response.json()) == {"text", "doc_type", "doc_type_confidence", "signals", "reader", "warnings"}
    assert response.json()["reader"] == "test-only"
    assert response.headers["cache-control"] == "no-store"


def test_mime_and_filename_do_not_override_actual_bytes(fake_reader):
    response = client.post("/api/read", files={"image": ("fake.jpg", b"not a photo", "image/jpeg")})
    assert response.status_code == 415
    fake_reader.read.assert_not_called()


def test_api_returns_matched_signals_from_test_only_rules(fake_reader, monkeypatch):
    from backend.classifier.signals import SIGNALS, Signal
    # Monkeypatch restores the empty student list after this test.
    monkeypatch.setitem(SIGNALS, "parking_ticket", (Signal("toy alpha marker", r"\bALPHA\b", 4),))
    fake_reader.read.return_value = Reading("ALPHA is an artificial marker on this synthetic readable testing page.", [])
    response = client.post("/api/read", files={"image": ("synthetic.jpg", photo_bytes())})
    assert response.status_code == 200
    assert response.json()["doc_type"] == "parking_ticket"
    assert response.json()["doc_type_confidence"] == 0.571
    assert response.json()["signals"] == ["parking_ticket: toy alpha marker (+4)"]


def test_missing_extra_files_and_malformed_uploads(fake_reader):
    assert client.post("/api/read", files={"wrong": ("x.jpg", photo_bytes())}).status_code == 400
    assert client.post("/api/read", files=[("image", ("a.jpg", photo_bytes())), ("image", ("b.jpg", photo_bytes()))]).status_code == 400
    assert client.post("/api/read", content=b"bad", headers={"content-type": "multipart/form-data; boundary=wrong"}).status_code == 400
    assert client.post("/api/read", content=b"", headers={"content-type": "text/plain"}).status_code == 415


def test_oversized_and_chunked_request_are_rejected(fake_reader, monkeypatch):
    monkeypatch.setattr(images, "MAX_IMAGE_BYTES", 100)
    assert client.post("/api/read", files={"image": ("x.jpg", photo_bytes())}).status_code == 413
    monkeypatch.setattr(images, "MAX_REQUEST_BYTES", 150)
    response = client.post("/api/read", content=iter([b"a" * 80, b"b" * 80]),
                           headers={"content-type": "multipart/form-data; boundary=x"})
    assert response.status_code == 413


@pytest.mark.parametrize("text", ["", "hi", "$$$ %%% ### 1234 !!!!!", "[unreadable] page"])
def test_unreadable_text_is_a_warning_not_an_error(text, fake_reader):
    fake_reader.read.return_value = Reading(text, [])
    response = client.post("/api/read", files={"image": ("photo.jpg", photo_bytes())})
    assert response.status_code == 200
    assert any("Retake" in warning for warning in response.json()["warnings"])


def test_readable_text_has_no_quality_warning():
    assert quality_warnings("This is a synthetic school letter with several clearly readable words.") == []


@pytest.mark.parametrize("failure", [None, "reader", "unexpected", "bad-image", "multipart"])
def test_no_notice_data_left_on_disk(tmp_path, monkeypatch, caplog, failure):
    # Run from an empty directory, direct child temp files here, and forbid Python
    # disk-backed temporary files. Check both files AND captured application logs.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    def forbid_disk(*args, **kwargs):
        raise AssertionError("Notice processing attempted a disk-backed temporary file")
    monkeypatch.setattr(tempfile, "TemporaryFile", forbid_disk)
    monkeypatch.setattr(tempfile, "NamedTemporaryFile", forbid_disk)
    before = set(tmp_path.rglob("*"))
    data = (ROOT / "eval/samples/parking_01.png").read_bytes()
    if failure:
        reader = Mock()
        reader.name = "test-only"
        reader.read.side_effect = ReaderError("Reader unavailable.") if failure == "reader" else RuntimeError("SENSITIVE-NOTICE-CONTENT")
        app.dependency_overrides[get_reader] = lambda: reader
    try:
        with caplog.at_level(logging.INFO, logger="notice_decoder"):
            if failure == "multipart":
                response = client.post("/api/read", content=b"--x\r\nContent-Disposition: form-data; name=\"image\"; filename=\"private.jpg\"\r\n\r\nincomplete",
                                       headers={"content-type": "multipart/form-data; boundary=x"})
            else:
                response = client.post("/api/read", files={"image": ("private-notice-filename.png", b"not image" if failure == "bad-image" else data)})
        assert response.status_code == {None: 200, "reader": 503, "unexpected": 500, "bad-image": 415, "multipart": 400}[failure]
        assert set(tmp_path.rglob("*")) == before
        logs = " ".join(record.getMessage() for record in caplog.records if record.name == "notice_decoder")
        assert "request_id=" in logs
        for private in ["Invented Resident", "SENSITIVE-NOTICE-CONTENT", "private-notice-filename", "2026-10-29"]:
            assert private not in logs
        assert "SENSITIVE-NOTICE-CONTENT" not in response.text
    finally:
        app.dependency_overrides.clear()


def test_upload_larger_than_default_spool_limit_stays_in_memory(fake_reader, monkeypatch):
    def forbid_disk(*args, **kwargs):
        raise AssertionError("Unexpected spool rollover")
    monkeypatch.setattr(tempfile, "TemporaryFile", forbid_disk)
    pixels = random.Random(42).randbytes(800 * 800 * 3)
    out = io.BytesIO()
    Image.frombytes("RGB", (800, 800), pixels).save(out, "PNG")
    assert len(out.getvalue()) > 1024 * 1024
    response = client.post("/api/read", files={"image": ("noise.png", out.getvalue())})
    assert response.status_code == 200


def test_vision_request_contract_and_store_false(monkeypatch):
    captured = {}
    def handler(request):
        import json
        captured.update(json.loads(request.content))
        return httpx.Response(200, json={"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "Synthetic transcription"}]}]})
    real_client = httpx.Client
    monkeypatch.setattr(readers.httpx, "Client", lambda **kwargs: real_client(transport=httpx.MockTransport(handler), **kwargs))
    result = VisionReader("fake-test-key", "model-from-environment").read(b"synthetic-image")
    assert result.text == "Synthetic transcription"
    assert captured["store"] is False
    assert captured["model"] == "model-from-environment"
    assert captured["input"][0]["content"][0]["type"] == "input_image"


def test_vision_errors_are_sanitized_and_missing_key_is_clear(monkeypatch):
    with pytest.raises(ReaderError, match="not configured"):
        VisionReader("", "").read(b"x")
    real_client = httpx.Client
    monkeypatch.setattr(readers.httpx, "Client", lambda **kwargs: real_client(transport=httpx.MockTransport(
        lambda request: httpx.Response(429, text="SENSITIVE-NOTICE-CONTENT")), **kwargs))
    with pytest.raises(ReaderError, match="unavailable") as error:
        VisionReader("test", "test").read(b"x")
    assert "SENSITIVE" not in str(error.value)


def test_reader_environment_selection(monkeypatch):
    monkeypatch.setenv("TEXT_READER", "vision")
    assert isinstance(readers.make_reader(Settings.from_environment()), VisionReader)
    monkeypatch.setenv("TEXT_READER", "tesseract")
    assert isinstance(readers.make_reader(Settings.from_environment()), TesseractReader)
    monkeypatch.setenv("TEXT_READER", "invalid")
    with pytest.raises(ReaderError):
        readers.make_reader(Settings.from_environment())


def test_vision_credential_is_header_only_and_errors_do_not_disclose_it(monkeypatch, caplog):
    import json
    secret = 'synthetic-private-credential-for-vision-test'
    def handler(request):
        assert str(request.url) == 'https://api.openai.com/v1/responses'
        assert request.headers['authorization'] == 'Bearer ' + secret
        assert secret not in json.dumps(json.loads(request.content))
        return httpx.Response(401, json={'error': {'message': secret}})
    real_client = httpx.Client
    monkeypatch.setattr(readers.httpx, 'Client', lambda **kwargs: real_client(transport=httpx.MockTransport(handler), **kwargs))
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(ReaderError) as exc:
            VisionReader(secret, 'configured-test-model').read(b'synthetic-photo')
    assert secret not in str(exc.value)
    assert secret not in caplog.text
