FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    OMP_THREAD_LIMIT=1 OPENBLAS_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
# Explicit allowlist: no .env, Git history, tests, results or held-out inputs.
COPY backend/ ./backend/
COPY frontend/ ./frontend/
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 10000
# One worker: receipts and demo request limits are process-local.
CMD ["sh", "-c", "exec python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1 --no-access-log --no-proxy-headers"]
