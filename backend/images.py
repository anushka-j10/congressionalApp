"""Bounded in-memory multipart uploads and image normalization."""

import io
import warnings

from fastapi import HTTPException, Request
from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartException, MultiPartParser

register_heif_opener()
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_REQUEST_BYTES = MAX_IMAGE_BYTES + 64 * 1024
MAX_PIXELS = 40_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS


async def read_upload(request: Request) -> bytes:
    """Accept one multipart file named image without Starlette's disk rollover."""
    if not request.headers.get("content-type", "").lower().startswith("multipart/form-data;"):
        raise HTTPException(415, "Choose a photo and try again.")
    # Bound actual bytes, even when Content-Length is missing or untrustworthy.
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > MAX_REQUEST_BYTES:
            raise HTTPException(413, "Photo is too large. Choose a photo under 10 MB.")
        body.extend(chunk)

    async def stream():
        yield bytes(body)

    parser = MultiPartParser(request.headers, stream(), max_files=1, max_fields=0,
                             max_part_size=MAX_REQUEST_BYTES)
    # Starlette 0.48's default rolls files over at 1 MB. Our already-bounded
    # request fits below this threshold, so the spool never touches disk.
    parser.spool_max_size = MAX_REQUEST_BYTES + 1
    form = None
    try:
        form = await parser.parse()
        upload = form.get("image")
        if len(form.multi_items()) != 1 or not isinstance(upload, UploadFile):
            raise HTTPException(400, "Choose one photo and try again.")
        data = await upload.read(MAX_IMAGE_BYTES + 1)
        if len(data) > MAX_IMAGE_BYTES:
            raise HTTPException(413, "Photo is too large. Choose a photo under 10 MB.")
        return data
    except (MultiPartException, ValueError):
        raise HTTPException(400, "Photo upload was incomplete. Choose it again.") from None
    finally:
        if form is not None:
            await form.close()
        # Also close incomplete spools if parsing failed before returning a form.
        for spool in parser._files_to_close_on_error:
            spool.close()
        body.clear()


def normalize_image(data: bytes) -> bytes:
    """Verify bytes, apply orientation once, and strip metadata from a JPEG."""
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413 if data else 415, "Choose a photo under 10 MB.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as probe:
                if probe.format not in {"JPEG", "PNG", "WEBP", "HEIF"}:
                    raise HTTPException(415, "Choose a JPEG, PNG, WebP, or HEIC photo.")
                if probe.width * probe.height > MAX_PIXELS:
                    raise HTTPException(413, "Photo dimensions are too large. Choose a smaller photo.")
                if getattr(probe, "n_frames", 1) != 1:
                    raise HTTPException(415, "Choose a single photo, not an animation.")
                probe.verify()
            with Image.open(io.BytesIO(data)) as source:
                source.load()
                oriented = ImageOps.exif_transpose(source)
                oriented.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                # A fresh image drops EXIF, GPS, comments, and other metadata.
                clean = Image.new("RGB", oriented.size, "white")
                if "A" in oriented.getbands():
                    rgba = oriented.convert("RGBA")
                    clean.paste(rgba, mask=rgba.getchannel("A"))
                else:
                    clean.paste(oriented.convert("RGB"))
                output = io.BytesIO()
                clean.save(output, format="JPEG", quality=90)
                return output.getvalue()
    except HTTPException:
        raise
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(413, "Photo dimensions are too large. Choose a smaller photo.") from None
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError):
        raise HTTPException(415, "That file is not a readable photo. Choose another image.") from None
