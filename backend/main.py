"""Same-origin PWA and a bounded, non-persisting image-to-text endpoint."""

import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import time
import uuid
import secrets
from dataclasses import dataclass, field
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from pydantic import ValidationError
from backend.extraction_models import ExtractRequest
from backend.extraction import ExtractionError, ModelExtractor, extract_and_verify

from backend.explanation_models import ExplainRequest
from backend.explanation import explain_notice
from backend.language_config import public_languages, all_languages, message
from backend.structured_model import StructuredModel
from backend.receipts import issue_receipt, valid_receipt

from backend.images import read_upload, normalize_image
from backend.readers import ReaderError, make_reader, quality_warnings
from backend.classifier.scoring import classify
from backend.classifier.signals import SIGNALS

logger = logging.getLogger("notice_decoder")


@dataclass(frozen=True)
class Settings:
    # repr=False prevents accidental disclosure when debugging this object.
    api_key: str = field(repr=False)
    model: str
    reader: str = "preprocessed"
    tesseract_command: str = "tesseract"

    @classmethod
    def from_environment(cls):
        return cls(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            model=os.environ.get("OPENAI_MODEL", ""),
            reader=os.environ.get("TEXT_READER", "preprocessed").strip().lower(),
            tesseract_command=os.environ.get("TESSERACT_CMD", "tesseract"),
        )


app = FastAPI(title="Notice Decoder", docs_url=None, redoc_url=None)
app.state.settings = Settings.from_environment()
app.state.receipt_secret = secrets.token_bytes(32)


@app.middleware("http")
async def private_api_responses(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/api/health")
def health():
    # Do not expose secrets, configuration, or notice contents here.
    return {"status": "ok", "message": "Hello from Notice Decoder!"}


@app.get("/api/config")
def public_config():
    return {"reader": app.state.settings.reader,
            "external_processing": app.state.settings.reader in {"vision", "hybrid"},
            "classifier_ready": any(SIGNALS.values()),
            "extraction_external_processing": True}


def get_reader():
    try:
        return make_reader(app.state.settings)
    except ReaderError as exc:
        raise HTTPException(503, str(exc)) from None


def process_photo(raw, reader):
    reading = reader.read(normalize_image(raw))
    classification = classify(reading.text)
    notes = reading.warnings + quality_warnings(reading.text)
    if not any(SIGNALS.values()):
        notes.append("Document signals have not been configured yet. Type will be unknown.")
    elif classification.doc_type == "unknown":
        notes.append("Document type is uncertain. Check the original notice or ask someone for help.")
    result = {"text": reading.text, "doc_type": classification.doc_type,
            "doc_type_confidence": classification.confidence,
            "signals": classification.signals, "reader": reader.name, "warnings": notes}
    if reading.token_reviews:
        result["token_reviews"] = reading.token_reviews
        result["primary_reader"] = reading.primary_reader
    return result


@app.post("/api/read")
async def read_notice(request: Request, reader=Depends(get_reader)):
    request_id = uuid.uuid4().hex
    start = time.monotonic()
    doc_type, error = "unknown", "none"
    raw = None
    try:
        raw = await read_upload(request)
        result = await run_in_threadpool(process_photo, raw, reader)
        doc_type = result["doc_type"]
        return result
    except HTTPException as exc:
        error = f"http_{exc.status_code}"
        raise
    except ReaderError as exc:
        error = "reader_unavailable"
        raise HTTPException(503, str(exc)) from None
    except Exception:
        error = "processing_failed"
        raise HTTPException(500, "We could not read this photo. Please try again.") from None
    finally:
        raw = None
        logger.info("request_id=%s timing_ms=%d doc_type=%s error=%s",
                    request_id, int((time.monotonic() - start) * 1000), doc_type, error)


def get_extractor():
    settings = app.state.settings
    return ModelExtractor(settings.api_key, settings.model)


def get_today():
    # Injectable for tests; local dates must follow the app's NJ location.
    return datetime.now(ZoneInfo("America/New_York")).date()


@app.post("/api/extract")
async def extract_notice(request: Request, extractor=Depends(get_extractor), today=Depends(get_today)):
    start = time.monotonic()
    request_id = uuid.uuid4().hex
    error, doc_type = "none", "unknown"
    body = bytearray()
    parsed = None
    try:
        if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise HTTPException(415, "Send confirmed text as JSON.")
        # Bound the body before JSON/Pydantic parsing. The usual FastAPI 422 body
        # would echo private input, so errors here always use fixed messages.
        async for chunk in request.stream():
            if len(body) + len(chunk) > 150000:
                raise HTTPException(413, "This text is too long. Try one page at a time.")
            body.extend(chunk)
        try:
            parsed = ExtractRequest.model_validate(json.loads(body))
        except (ValueError, TypeError, ValidationError):
            raise HTTPException(422, "Check the text, document type, and text confirmation before extracting.") from None
        if not parsed.text.strip():
            raise HTTPException(422, "There is no text to extract. Check the reading first.")
        doc_type = parsed.doc_type
        result = await run_in_threadpool(extract_and_verify, parsed.text, doc_type, extractor, today)
        result['receipt'] = issue_receipt(app.state.receipt_secret, doc_type, result['fields'], result['today'])
        return result
    except HTTPException as exc:
        error = "http_" + str(exc.status_code)
        raise
    except ExtractionError as exc:
        error = "extraction_unavailable"
        raise HTTPException(503, str(exc)) from None
    except Exception:
        error = "extraction_failed"
        raise HTTPException(500, "We could not extract this notice. Check the text and try again.") from None
    finally:
        body.clear()
        parsed = None
        logger.info("request_id=%s timing_ms=%d doc_type=%s error=%s",
                    request_id, int((time.monotonic() - start) * 1000), doc_type, error)


@app.get("/api/languages")
def languages_config():
    return public_languages()


def get_language_model():
    settings = app.state.settings
    return StructuredModel(settings.api_key, settings.model)


@app.post("/api/explain")
async def explain(request: Request, model=Depends(get_language_model)):
    request_id, started = uuid.uuid4().hex, time.monotonic()
    code = request.headers.get("X-Notice-Language", "en")
    if code not in all_languages():
        code = "en"
    body, parsed = bytearray(), None
    error = "none"
    doc_type = "unknown"
    try:
        if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise HTTPException(415, message(code, 'explain_error'))
        async for chunk in request.stream():
            if len(body) + len(chunk) > 150000:
                raise HTTPException(413, message(code, 'explain_error'))
            body.extend(chunk)
        try:
            parsed = ExplainRequest.model_validate(json.loads(body))
        except (ValueError, TypeError, ValidationError):
            raise HTTPException(422, message(code, 'explain_error')) from None
        if parsed.language not in all_languages():
            raise HTTPException(422, message(code, 'explain_error'))
        code, doc_type = parsed.language, parsed.doc_type
        fields = {name: value.model_dump() for name, value in parsed.fields.items()}
        if not valid_receipt(app.state.receipt_secret, parsed.receipt, doc_type, fields, parsed.today):
            raise HTTPException(409, message(code, 'receipt_error'))
        return await run_in_threadpool(explain_notice, fields, doc_type, code, model)
    except HTTPException as exc:
        error = 'http_' + str(exc.status_code)
        raise
    except Exception:
        error = 'explanation_failed'
        raise HTTPException(500, message(code, 'explain_error')) from None
    finally:
        body.clear()
        parsed = None
        logger.info("request_id=%s timing_ms=%d doc_type=%s error=%s",
                    request_id, int((time.monotonic()-started)*1000), doc_type, error)


# Register API routes before mounting the browser files at /.
app.mount(
    "/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend", html=True),
    name="frontend",
)
