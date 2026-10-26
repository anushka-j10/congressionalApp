# Notice Decoder

A mobile-first PWA project for a Congressional App Challenge entry in NJ-08,
starting with Jersey City / Hudson County. **Current checkpoint: Milestone 4 selected fixes 1–2 are
complete. Post-evaluation reliability repairs are implemented; the original held-out run is preserved.** Photograph a page, check and confirm
the text and every printed amount, explicitly select the document type, and inspect source-backed facts.
The app explains verified facts in English and offers guarded Spanish/Tagalog
translations, original-English toggles, and matching-voice read-aloud.

The configured API key now works. The live M3 comparison accepted 7/8 Spanish and
6/8 Tagalog translations; the other three displayed an explicit English fallback.
These are mechanical checks on eight invented notices, not measured real-world
accuracy or native-speaker approval. Physical-phone acceptance, handwriting, native
review, and student classifier signals remain outstanding. See M4 results below.
See the M3 checkpoint at the end; earlier sections are historical snapshots.

**The student's classification signal lists are intentionally empty.** The scoring
engine works, but every production document currently returns `unknown` with 0
confidence and a clear warning. Toy rules exist only in unit tests. This is not
proof of classification accuracy, and the eight-row table does not claim it is.

## Run

Requires Python 3.9+ and Tesseract with English language data. On macOS install the
engine with `brew install tesseract`; on Debian/Ubuntu install `tesseract-ocr` and
`tesseract-ocr-eng` using your package manager. These are system dependencies,
separate from Python packages.

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.main:app --env-file .env --reload --host 127.0.0.1 --port 8000 --no-access-log
```

If you already have `.env`, update its settings rather than overwriting it.
Open <http://localhost:8000>. Choose a photo, inspect its preview, and tap **Read
notice**. **Clear photo and results** releases the app's preview and clears the
text. Browser memory is used for preview/results. Only the chosen language code
is kept in localStorage; notices, explanations, translations and receipts are not
persisted in localStorage, IndexedDB or the service-worker cache. Reload after
frontend edits.

The server loads `.env` through Uvicorn. `.env` is ignored by Git, and only
`frontend/` is publicly served. Never put API keys in JavaScript or commit `.env`.

```dotenv
TEXT_READER=preprocessed
TESSERACT_CMD=tesseract
OPENAI_API_KEY=
OPENAI_MODEL=
```

Set `TESSERACT_CMD` to an absolute executable path if it is not on PATH. To try
vision, set `TEXT_READER=vision`, supply your key and a vision-capable model in
`OPENAI_MODEL`, then restart the server. There is no hardcoded model or automatic
provider fallback. Missing credentials produce a friendly configuration error.

## Reader decision

Both readers implement `TextReader.read(jpeg) -> Reading(text, warnings)`.

| Concern | Vision reader | Local Tesseract (initial default) |
| --- | --- | --- |
| Phone photos | Useful comparison candidate; can misread or infer text, especially when small or rotated. | Clear printed text works well; rotation, shadows, and blur need preprocessing and can cause mistakes. |
| Speed | Includes network and provider latency. | Uses server CPU without an external OCR request. |
| Cost | Usage-based image input and text output charges depend on the chosen model. | No per-request provider fee; server compute still costs resources. |
| Privacy | Sends the normalized photo to OpenAI. | Photo and OCR stay on the app server. |
| Explaining it | Small API adapter, but model transcription is less predictable. | Straightforward image preparation and OCR flow, with a system dependency. |

Neither reader is assumed to win on the user's photos; compare them using the
same samples. The interface allows the later eval harness to choose either.
Tesseract is the default because it keeps notices off an external AI service.

Vision calls use `store=false`, no Files API upload, and no background mode.
This does **not** guarantee zero provider retention: default abuse-monitoring
logs may contain content and are generally retained up to 30 days, subject to
exceptions. The UI discloses external processing before the user sends a photo.
See [OpenAI vision limitations](https://developers.openai.com/api/docs/guides/images-vision),
[OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data), and
[Tesseract quality guidance](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html).
No live OpenAI request was verified in this milestone; provider-contract tests
use synthetic mocked responses and do not establish account/model availability.

## Image handling and privacy

Preparation happens **before upload in the browser** to save mobile data. Native
image decoding applies EXIF orientation; if HEIC is unsupported natively, a
locally bundled heic-to/libheif decoder handles it. The canvas exports a JPEG with
long edge at most 1600 pixels, without enlarging small images. Do not apply a
second manual EXIF rotation to already oriented decoded pixels. The backend
independently decodes HEIC, applies EXIF normalization, and strips metadata too,
so direct API requests receive the same validation.

Limits: 25 MB original browser file; 60 million browser decoded pixels; 10 MB API
image; 40 million backend decoded pixels; one JPEG/PNG/WebP/HEIC still image. The
API bounds actual request bytes, including chunked uploads, to 10 MB plus 64 KB of
multipart overhead. It decodes file bytes instead of trusting MIME or filenames.
Malformed, truncated, animated, unsupported, and oversized images are rejected.

The upload parser's memory spool threshold is above the bounded request size;
it never rolls a valid request to disk. Spools close in `finally`, including on
incomplete parsing. Pillow uses byte streams; Tesseract receives stdin and returns
stdout; vision receives an in-memory data URL. No notice temp file, database,
image output, or text output is created. These guarantees concern application
storage, not secure RAM erasure, operating-system swap, or provider retention.

All API responses have `Cache-Control: no-store`. The service worker only caches
an explicit list of public shell assets, never API responses, photo blobs, or
notice text. Request logs contain generated request ID, elapsed milliseconds,
document type, and a fixed error code only. Notice contents, original filenames,
provider error bodies, and credentials are never intentionally logged; use the
`--no-access-log` startup command and do not enable HTTP wire/body logging.

Short text, mostly symbols, or `[unreadable]` produce retake warnings, not errors.
These are simple quality checks and cannot detect every incorrect transcription.
The app is an explanatory tool, not legal advice, and the user must compare the
reading with the original notice.

## Add your document signals

Edit **`backend/classifier/signals.py`**. For each document type, supply your own
`Signal(label=..., pattern=..., weight=...)` entries: readable label, Python regex,
and positive finite weight. The assistant left every real list empty as requested.
The unit tests demonstrate syntax with artificial `ALPHA`/`BETA` markers; they
are not real notice signals and are never loaded by the app.

The engine matches case-insensitively and adds each signal's weight at most once,
even if a phrase occurs repeatedly. It returns all matched signal labels and
weights, including evidence for competing types, without copying source text
into the signals list. Default acceptance requires best score >= 3 and relative
margin `(best - runner_up) / best >= 0.25`. Otherwise the type is `unknown`.

Confidence is a **heuristic**, not a probability or OCR accuracy measure:
`min(0.99, best / (best + 3) * relative_margin)`, rounded to three decimals.
Unknown results are capped at 0.49, and no evidence returns 0. No model fallback
for classification is included. Review thresholds against your own signals.

Restart after changing signals and run the table below. Unit tests cover weak
signals, repeated text, competing signals, ties, regex matches, and invalid
weights. The original ownership plan reserved the later extraction schema,
deterministic field validators, and eval scoring logic.

## Tests and eight-sample table

```sh
python -m pytest -q
python -m pytest -q -s tests/test_integration.py
node --input-type=module --check < frontend/app.js
node --input-type=module --check < frontend/image-prep.js
node --check frontend/sw.js
python -m pip check
```

The integration test really sends all eight images through `POST /api/read`,
using the configured reader. It does not substitute fixture text or expected
labels. With `TEXT_READER=vision`, it will send these synthetic images to OpenAI
and incur API usage. Keep local Tesseract as the default for repeatable tests.

To regenerate the eight tracked fictional sample pairs:

```sh
python eval/generate_samples.py
# If a standard font is not installed:
python eval/generate_samples.py --font /absolute/path/to/font.ttf
```

Each JSON records the expected type plus deadline, amount (decimal string or
null), action, and image effects. These are fixture annotations, not the student's
future extraction schema or an implemented field scorer. All documents are
explicitly marked synthetic; no real person, account, case, agency logo, or
contact information is used. Four samples have slight rotation, a lighting
gradient, and mild blur.

Local results on October 21, 2026: **53 tests passed**, with one Python 3.9 asyncio
deprecation warning. JavaScript syntax checks and `pip check` also passed. The
real reader was Tesseract 5.5.3. The sample output is saved in
`eval/milestone1-results.txt`:

| Sample | Expected | Predicted | Confidence | Reader | Signals |
| --- | --- | --- | ---: | --- | --- |
| court_01 | court_notice | unknown | 0.000 | tesseract | none |
| court_02 | court_notice | unknown | 0.000 | tesseract | none |
| parking_01 | parking_ticket | unknown | 0.000 | tesseract | none |
| parking_02 | parking_ticket | unknown | 0.000 | tesseract | none |
| school_01 | school_letter | unknown | 0.000 | tesseract | none |
| school_02 | school_letter | unknown | 0.000 | tesseract | none |
| utility_01 | utility_bill | unknown | 0.000 | tesseract | none |
| utility_02 | utility_bill | unknown | 0.000 | tesseract | none |

Privacy tests run from an empty directory with child TMPDIR redirected there,
forbid disk-backed Python temp files, and check for leftover files after a real
OCR request, malformed upload, invalid image, reader failure, and unexpected
failure. A >1 MB real image also verifies no default spool rollover. These tests
verify those request paths, not every OS/library behavior on every host.

## Phone acceptance check

Use the same trusted HTTPS setup as Milestone 0. For a same-Wi-Fi page preview,
change the host to `0.0.0.0` and open `http://YOUR-COMPUTER-LAN-IP:8000` on your
phone; installation/service-worker checks on the phone require HTTPS. Public
deployment is outside this milestone, and this work does not change hosting.

1. Open the app, refresh to update the shell, and tap **Take photo**. Confirm it
   offers the rear camera, photograph a printed page, and inspect the preview.
2. Tap **Read notice** and check the text, reader, type, confidence, warnings, and
   signals. Unknown is expected until you write your signal lists.
3. Choose a portrait HEIC from the library and check it stays upright. Try a JPEG
   with EXIF rotation and a dense page too; 1600px may lose very small text.
4. Try a blurry page, a blank page, and a non-image. Turn off connectivity before
   sending and confirm a short error and enabled retry controls.
5. Tap **Clear photo and results**, then verify the image and text disappear.
   Results should not return after reload. Offline mode opens only the shell;
   OCR always needs a connection to the backend.

The local browser flow was verified with a rotated/shaded synthetic PNG and an
orientation-tagged synthetic HEIC. Physical iPhone camera capture, Safari/Android
installation behavior, and broader real-photo quality remain manual checks.
One phone-style PNG's synthetic street number was misread, illustrating why the
text must remain checkable. No perfect OCR or classification accuracy is claimed.

## Every source and supporting file, explained

- **`.gitignore`** keeps local environments, caches, credentials, and certificate
  files out of Git. It deliberately allows the placeholder `.env.example`.
- **`.env.example`** documents the reader selector, local executable setting, and
  server-only API credentials. Copy its placeholders into a private `.env`.
- **`requirements.txt`** pins direct Python dependencies for the server, tests,
  image decoding, and multipart parsing. Starlette is explicitly pinned because
  the in-memory spool configuration is tested against that version.
- **`backend/main.py`** connects the PWA, public configuration, image reader, and
  classifier through FastAPI routes. It runs CPU/blocking work off the async event
  loop and returns sanitized errors and non-cacheable API responses.
- **`backend/images.py`** bounds incoming bytes and keeps multipart files in
  memory, closing spools even after parsing failures. It verifies actual image
  bytes, decodes HEIC, fixes orientation, strips metadata, and returns JPEG bytes.
- **`backend/readers.py`** defines the shared reader contract and implements
  Tesseract stdin/stdout and OpenAI vision adapters. It also supplies conservative
  text-quality warnings and fixed errors without exposing provider response bodies.
- **`backend/classifier/signals.py`** defines the Signal container and four empty
  lists marked for student implementation. You supply the real patterns and
  weights; the assistant has not filled them in.
- **`backend/classifier/scoring.py`** adds matched weights and checks the best
  score against both a threshold and its nearest competitor. It returns the type,
  heuristic confidence, and matched evidence while allowing `unknown`.
- **`frontend/index.html`** defines camera/library controls, preview, results,
  warnings, and the privacy/disclaimer copy. Its semantic headings and status
  regions make changes readable to assistive technology.
- **`frontend/styles.css`** provides responsive spacing, high-contrast colors,
  large controls, and visible keyboard focus. It also makes extracted text scroll
  without expanding the whole page indefinitely.
- **`frontend/app.js`** handles photo selection, reader configuration, upload,
  results, loading, errors, retries, and clearing. It uses textContent for OCR
  output so document text cannot become executable HTML.
- **`frontend/image-prep.js`** decodes photos on the device, falling back to the
  bundled HEIC decoder when needed. It creates an oriented JPEG at up to 1600px
  and releases canvas and object-URL resources afterward.
- **`frontend/sw.js`** caches only an explicit allowlist of public shell assets
  for offline opening. It excludes every API request and notice image, activates
  the new shell cache, and removes old Notice Decoder caches.
- **`frontend/manifest.webmanifest`** declares the name, icons, colors, and
  standalone launch preference. It supplies installation metadata to supporting
  browsers but does not perform installation itself.
- **`frontend/icons/icon-192.png`** is the small geometric notice icon from
  Milestone 0. Browsers can use it in installation and home-screen UI.
- **`frontend/icons/icon-512.png`** is the larger version of the same icon.
  It supplies a higher-resolution image for installation surfaces.
- **`frontend/vendor/heic-to.js`** is the unmodified CSP build of heic-to 1.6.6,
  copied from npm and loaded locally for HEIC fallback. It is third-party code,
  not student or assistant original work, and includes its libheif decoder.
- **`frontend/vendor/heic-to.LICENSE`** preserves the third-party LGPL license
  supplied by that package. Source and build details are available in the
  [heic-to repository](https://github.com/hoppergee/heic-to) and the
  [1.6.6 npm distribution](https://www.npmjs.com/package/heic-to/v/1.6.6).
- **`eval/generate_samples.py`** draws all eight fictional notices and matching
  annotations with Pillow. It deterministically adds photo-like effects to four
  samples so they can be regenerated without real resident data.
- **`eval/milestone1-results.txt`** contains the real local-reader integration
  table captured during verification. Its empty-signal note explains why the
  current predictions are unknown.
- **`tests/test_app.py`** retains Milestone 0 checks for health, settings, shell
  assets, icon dimensions, and private-file isolation. It also guards the static
  cache boundary.
- **`tests/test_classifier.py`** verifies scoring and ambiguity using artificial
  markers only. It deliberately does not author or substitute real notice rules.
- **`tests/test_read.py`** covers actual formats, HEIC and EXIF transforms,
  oversized and malformed uploads, privacy paths, and reader errors. It also tests
  the vision request contract using synthetic mocked HTTP responses.
- **`tests/test_integration.py`** runs all eight PNGs through the actual API and
  configured reader and prints expected versus predicted types. It verifies
  readable output and the response contract without implementing eval scoring.
- **`AI_USAGE.md`** discloses generated and changed files and separates dependency
  code from original work. Keep adding specific student contributions and AI
  changes as the project develops.
- **`README.md`** documents setup, decisions, limits, tests, and review steps.
  Its file explanations support a student-led walkthrough of the implementation.

The sample files have these individual roles:

| File under `eval/samples/` | Explanation |
| --- | --- |
| `parking_01.png` | Clean fictional parking ticket for OCR. It contains a $45 charge and October 29 deadline. |
| `parking_01.json` | Expected facts for the first parking fixture. It records the type, deadline, amount, action, and synthetic marker. |
| `parking_02.png` | Fictional parking citation with rotation, uneven lighting, and blur. It tests OCR on a photo-like page with a $65 charge. |
| `parking_02.json` | Expected facts for the second parking fixture. Its action is to request a fictional citation review. |
| `court_01.png` | Clean fictional court notice. It requests attendance at a demonstration hearing and specifies no amount. |
| `court_01.json` | Expected facts for the first court fixture. It preserves a null amount instead of inventing a fee. |
| `court_02.png` | Fictional court summons with photo-like effects. It asks for a response form by November 5. |
| `court_02.json` | Expected facts for the second court fixture. It records the response action, deadline, and absent amount. |
| `utility_01.png` | Clean fictional electric bill. It displays an $82.35 charge and November 4 due date. |
| `utility_01.json` | Expected facts for the electric fixture. Its amount remains an exact decimal string for later evaluation. |
| `utility_02.png` | Fictional water bill with rotation, shadows, and mild blur. It displays a $37.20 charge and November 6 deadline. |
| `utility_02.json` | Expected facts for the water fixture. It labels the type and intended action without deriving anything from OCR. |
| `school_01.png` | Clean fictional letter asking for a permission form. It has an October 30 deadline and no stated amount. |
| `school_01.json` | Expected facts for the permission-form fixture. It records an absent amount as null and preserves the action text. |
| `school_02.png` | Fictional school conference letter with photo-like effects. It asks for confirmation by November 7. |
| `school_02.json` | Expected facts for the conference fixture. It includes the conference action and the applied image effects. |

The ignored `.venv/` contains installed third-party packages, not project source.
The scratch synthetic HEIC used for browser QA is outside the repository under
`work/`; it contains no user notice data and is not a ninth eval sample.

## Review boundary

Review the student's empty signal lists first, then test camera capture and a
portrait HEIC on the phone. Milestone 1 plumbing is ready for review; meaningful
document identification still depends on student-authored signals. Stop here
before starting field extraction or translation.

## Milestone 2 checkpoint A1: reproduce and measure, no reader fixes

Run from the repo root using the existing virtual environment:

```sh
python -m eval.generate_reader_samples
python -m eval.reader_bakeoff
python -m pytest -q
```

The default bake-off measures local Tesseract and reports existing vision as
NOT RUN when credentials/model are absent. To use configured vision later,
explicitly load your private settings with `--env-file .env`; this sends the
synthetic samples to the provider and incurs usage. To measure any other
TextReader later, use `--factory your_local_module:create_reader`. No OpenCV
preprocessing, hybrid reader, text correction UI, or extraction was added in A1.

The generator preserves the eight existing M1 PNG/JSON pairs. Four already had
photo effects, so they are reported separately as legacy rather than clean.
It adds eight clean reproductions, 56 labeled degraded variants, and matching
UTF-8 ground truths. A fixed seed and severity parameters are recorded in
`eval/reader-corpus.json`; production code and original fixture fingerprints
were checked and remained unchanged.

Measured baseline on October 21, 2026, using Tesseract 5.5.3 / English / PSM 3:

| Reader | Condition | Measured pages | CER ↓ | Key-token recall ↑ |
| --- | --- | ---: | ---: | ---: |
| Tesseract M1 | Clean | 8 | 0.00% | 100.00% (28/28) |
| Tesseract M1 | Degraded | 56 | 29.09% | 64.29% (126/196) |
| Tesseract M1 | Handwriting | 0 | N/A | N/A |
| Tesseract M1 | Original M1 mixture | 8 | 0.05% | 100.00% (28/28) |
| Vision | Clean / degraded / handwriting | 0 | Not run | No configured key/model |

On the clean+degraded printed set, recall is **68.75% (154/224)**, below the
95% requirement. The old eight-page test alone did not reveal these weaknesses.
The formal chosen-reader gate is pending A2 comparison and student selection;
this baseline does not pass it, and Part B has not started.

Individual degraded variants retain 28 targets each: blur, noise, and compression
all score 28/28; rotation 22/28; perspective 20/28; shadow 0/28; combined phone
conditions 0/28. Detailed failures, CER denominators, settings, and full target
inventories are in `eval/reports/reader-baseline.json`. The screenshot-friendly
console table is `eval/reports-a1-table.txt`; the human analysis is
`eval/reports/reader-baseline-analysis.md`.

### Limitations: printed text and handwriting

There are no handwritten image/truth pairs yet, so handwriting accuracy is
**unmeasured**, not supported, not 0% CER, and not a gate pass. Add six photos of
invented handwritten notices under `eval/samples/handwriting/`, each with the same
base name and `.txt` or `.gt.txt` truth. The harness discovers them automatically;
missing, duplicate, empty, or orphan pairs are errors. See that folder's README.
Do not use real notices or actual personal information.

The corpus uses eight related texts and one font/layout with scripted effects.
Its aggregate does not estimate accuracy on all real phones or documents; browser
JPEG re-encoding and camera optics are not simulated. Key-token recall measures
presence, not field interpretation, precision, or calibrated confidence. The
metric's supported target formats and digit-preservation policy are documented
in `DESIGN_NOTES.md`; review the detected targets for any new handwriting formats.
No automatic handwriting-region detector or token-highlighting correction screen
has been implemented at this no-fixes checkpoint.

### New A1 source and report files, explained

- **`eval/generate_reader_samples.py`** creates the clean and degraded fixtures
  with fixed parameters and exact text pairs. It leaves the original images and
  expected-field JSON untouched and writes a reproducibility manifest.
- **`eval/reader_bakeoff.py`** computes exact edit-distance CER and whole-token
  recall on actual reader output, counting reader failures rather than skipping
  them. It prints condition tables, discovers handwriting pairs, and records
  missed tokens and fingerprints without saving whole OCR transcripts.
- **`tests/test_reader_bakeoff.py`** checks the metric's digit rejection, repeated
  token accounting, missing-data handling, and corpus consistency. It also checks
  deterministic degradations and preservation of the original clean renderer.
- **`DESIGN_NOTES.md`** explains the scoring definitions, corpus choices, privacy
  boundary, and gate result for the student to edit. It deliberately contains no
  Part B extraction schema or field-validator implementation.
- **`eval/reader-corpus.json`** records the fixed degradation parameters, random
  seed, font checksum, and source-image/truth hashes. It allows future runs to
  identify exactly which corpus was measured.
- **`eval/samples/handwriting/README.md`** explains how to add the six invented
  handwriting photo/truth pairs. It makes missing evidence and supported target
  formats explicit rather than claiming handwriting support.
- **`eval/reports/reader-baseline.json`** holds the real per-page and aggregate
  metrics plus target inventories and missed-token evidence. Its vision rows
  explicitly record that no provider run occurred.
- **`eval/reports-a1-table.txt`** is the measured console table suitable for a demo
  screenshot. It preserves the N/A handwriting and unconfigured-vision states.
- **`eval/reports/reader-baseline-analysis.md`** breaks failures down by image
  condition and lists the missed expected tokens with observed candidates. It
  separates baseline evidence from later reader-selection recommendations.
- **`eval/reports/A1_FILE_GUIDE.txt`** inventories every A1 generated data/report
  file with a two-sentence explanation. It makes the large repeated fixture set
  reviewable without repeating all of those entries in this README.

`eval/generate_samples.py` was refactored to share the original visible text and
clean renderer with truth generation. The original clean images still match the
shared renderer exactly; no production reading behavior was changed.

## Milestone 2 checkpoint A2: reader comparison

At the historical A2 checkpoint the app still defaulted to `tesseract`; selection was pending. Two new
explicit modes are `preprocessed` (OpenCV plus Tesseract) and `hybrid` (preprocessed
plus the environment-selected vision model). A hybrid API response adds actual
`token_reviews` and `primary_reader` metadata; the existing single-reader response
contract remains the same. The result screen shows every candidate and marks
primary-text disagreements. Agreement is never labeled verification.

```sh
# Reproduce the local comparison without any provider calls:
python -m eval.reader_bakeoff --readers tesseract preprocessed \
  --output eval/reports/reader-local-comparison.json

# Once the private .env has working API quota, run all four readers:
python -m eval.reader_bakeoff --env-file .env
```

The four-reader report now defaults to `eval/reports/reader-comparison.json`,
leaving the A1 baseline file untouched. One actual vision preflight is reused in
RAM and stops the provider comparison early on authentication/access/quota errors.
No ground-truth values enter the readers. Hybrid CER and text recall describe its
primary transcript; the separate shown-candidate recall counts only actual
alternatives returned to the UI, with one-to-one occurrence accounting.

The measured local result is:

| Reader | Condition | CER | Key-token recall |
| --- | --- | ---: | ---: |
| Original Tesseract | Clean | 0.00% | 100.00% (28/28) |
| Original Tesseract | Degraded | 29.09% | 64.29% (126/196) |
| OpenCV + Tesseract | Clean | 0.00% | 100.00% (28/28) |
| OpenCV + Tesseract | Degraded | 0.59% | 100.00% (196/196) |
| Every reader | Handwriting | N/A | No handwriting pairs supplied |
| Vision / hybrid | Printed | Not run | Initial API preflight returned rate/quota limit |

Preprocessing matches **224/224 printed key targets (100%)**, meeting the numerical
95% threshold on this frozen synthetic set. This is not a claim that all notice
text is correct or that handwriting works. The recommendation is to consider the
preprocessed local option for printed notices; it cannot be ranked against
unmeasured vision/hybrid, and final selection remains pending student review.

The native handwriting photos are still required for a handwriting conclusion.
A3's editable text-confirmation screen is not implemented yet. Part B extraction
has not started. Current source and test changes are recorded in `AI_USAGE.md`;
the detailed algorithm/scoring rules are in `DESIGN_NOTES.md`.

### A2 new files, explained

- **`backend/preprocessed_reader.py`** implements the fixed grayscale, denoise,
  deskew, upscale, and adaptive-threshold recipe in memory. It delegates final OCR
  to the original Tesseract adapter so the baseline stays comparable.
- **`backend/reader_tokens.py`** locates actual date, amount, and ID candidates and
  compares their normalized strings without correcting digits. It keeps source
  reader and text offsets so disagreements can be displayed and highlighted.
- **`backend/hybrid_reader.py`** runs the two components and returns their actual
  agreed or disputed values alongside a primary transcript. One-reader failures
  and blank local text are handled explicitly without inventing agreement.
- **`frontend/token-review.js`** renders all returned alternatives and highlights
  disputed spans in the matching primary text. It creates text nodes instead of
  executing markup from a notice.
- **`tests/test_reader_comparison.py`** checks image preprocessing, deskew direction,
  candidate provenance, failed components, signed amounts, and candidate recall.
  It also checks the API response and a real preprocessed request's privacy.
- **`eval/reports/reader-local-comparison.json`** records the actual local baseline
  and preprocessed-reader measurements on the frozen corpus. Its fingerprints
  and parameters identify the tested implementation without saving transcripts.
- **`eval/reports-a2-local-table.txt`** is the local comparison's console table for
  screenshots. It uses measured counts and keeps handwriting unmeasured.
- **`eval/reports/reader-comparison.json`** records the four-reader run, including
  explicit provider not-run reasons when quota blocks the initial preflight. It
  separates hybrid candidate recall from primary-transcript recall.
- **`eval/reports-a2-table.txt`** is the console table for that four-reader attempt.
  It never fills missing provider results with fabricated numbers.
- **`eval/reports/handwriting-cloud-options.md`** lists dedicated OCR services with
  sourced pricing/privacy evidence and labeled setup estimates. It configures
  none of them and makes no claim about their accuracy on this project's photos.
- **`eval/reports/reader-comparison-analysis.md`** summarizes measured local results,
  the quota-blocked provider comparison, and the provisional recommendation.
  It separates numerical threshold evidence from handwriting claims and final
  reader selection.

The scratch `work/a2-ui-review/` contains copies of the actual renderer/styles and
an HTML harness with labeled synthetic test doubles. It exists for browser QA,
not as app functionality or a live provider result.

If the system Python reports an old macOS compatibility version and pip attempts
a slow OpenCV source build, use `SYSTEM_VERSION_COMPAT=0 python -m pip install
--only-binary=:all: -r requirements.txt` on a compatible modern Mac. The pinned
OpenCV/NumPy combination was tested here with Python 3.9 on macOS; use a Python
version supported by those exact wheels rather than assuming all newer Pythons
have compatible binary packages.

## Milestone 2 / A3 and Part B review — 2026-10-22

The student selected `preprocessed` and explicitly authorized a Codex-generated
schema/validator proposal for review. The runtime default, template, and local
ignored `.env` reader entry now use that choice. The existing printed gate is
**224/224 key tokens (100%)**, above 95%; those are the same eight source texts
and their degraded variants, not independent real-phone evidence. Vision/hybrid
remain unmeasured, and handwriting has no supplied photos/truths (N/A).

### Try the flow

Restart with the Run command above. Choose/read a synthetic photo, compare the
original OCR with the photo, edit the textarea, and choose the document type.
The empty student classifier still predicts unknown; this explicit user selection
does not count as automated classification. Check the confirmation box, then tap
**Confirm text and extract facts**. This sends only the edited text to OpenAI,
using `OPENAI_API_KEY` and `OPENAI_MODEL` from server settings. Never paste a key
in chat or JavaScript. Local OCR can run without a key; model extraction cannot.

Successful extraction displays Issuing agency, Deadline, Amount due, What to do,
and Contact with Verified / Please double-check / Not found badges. Verified means
matching evidence in the confirmed text, not authenticated facts or independently
correct field selection. Missing is an extractor abstention, not proof the notice
contains no such fact. Every edit or type change removes prior cards and resets
confirmation. Clear/page leave aborts active notice requests, ignores late replies,
and removes photo, original text, edits, and cards
from the UI and application references; there is no notice persistence/cache.

**Show source** highlights actual offsets in the confirmed text, including both
the relative rule and issue-date anchor when applicable. Relative arithmetic uses
calendar days and a server-side America/New_York date; tests inject 2026-10-22.
Unverified fields never get computed dates or days remaining. Unknown document
types skip the model entirely and direct the user to choose a type or ask for help.

### Proposed validator policies to review first

Read `DESIGN_NOTES.md` and `backend/field_validation.py` together. Accepted dates
are ISO or common US month/day/year and English month-name forms with four-digit
years; numeric slash dates use US order. No two-digit years, incomplete dates,
relative guesses, OCR digit repairs, impossible dates, business-day calendars,
holidays, or receipt-date assumptions are accepted. Relative support is limited
to an explicit “within N [calendar] days of/after the issue date/date above/date
of this notice” rule and an independently source-matched labeled issue date.

Amounts use Decimal, valid thousands grouping, zero or two decimal places, and
an explicit conservative 0–1,000,000 USD bound. That bound is an editable app
policy, not a legal rule. Negative, OCR-confused, ambiguous multi-amount snippets
and incomplete numeric substrings remain unverified. Source matching first
normalizes case/whitespace/NFKC; long snippets may tolerate small letter errors
at ratio >= .94, but numeric sequences must match exactly. Short fuzzy snippets
are rejected. Text fields must be copied source phrases, not model paraphrases.

These checks cannot prove that a copied date is the correct deadline, distinguish
all original/late-fee associations, detect forged notices, or guarantee resistance
to model prompt injection. That semantic failure analysis and adversarial
evaluation remain Milestone 4 work. A user-confirmed OCR mistake can still be
source-matched; users must compare the original photo. No real-phone or
handwriting support claim is made. Literal unreadable/replacement markers and
hybrid disputes are highlighted, but this is not a calibrated confidence or
handwriting detector.

### Verification and live integration

```sh
python -m pytest -q
# Browser-controller race tests; requires Node.js (no npm packages):
node --test tests/test_frontend_state.mjs
# Opt-in live API calls on ONLY the eight original synthetic fixtures:
python -m eval.extraction_smoke --env-file .env
```

`eval/reports/extraction-integration.txt` records the actual 2026-10-22 attempt:
first fixture -> API quota limit, one retry, then stop; remaining samples NOT RUN.
The command supplies known fixture types explicitly, uses unedited real local OCR,
and compares existing expected deadline/amount/action values; it is a small M2
integration check, not the general student-owned M4 scorer. Failed-request token
usage/cost is unknown; zero accumulated successful-response usage is not zero cost.
Do not rerun until account quota/billing is ready. The model remains an environment
setting and temperature uses provider default; no determinism claim is made here.

Provider requests use strict JSON schema and `store=false` with no tools. The
adapter rejects malformed/incomplete output and refusals, retries transient or
malformed failures at most once after .5 seconds, and never releases partial
fields. API errors are fixed, calm English messages; translation is not built.
The bounded JSON endpoint suppresses validation-body echoes and logs only request
ID, elapsed time, type, and error category. Automated tests exercise successful
and failed privacy paths and prohibit Python disk-backed notice temp files.
`store=false` is not a claim of zero provider retention; see the provider links
in the original privacy discussion.

Phone-width browser QA used the actual frontend, real preprocessed OCR, and a
clearly labeled synthetic extractor in a scratch server. Cards, bad-digit
unverified status, source/Unicode highlights, literal script text, edit invalidation,
and provider failure with no old cards were checked. This is not live extraction
accuracy, handwriting evidence, or a physical-phone acceptance test.

### New-file explanations

- **`backend/extraction_models.py`** proposes strict Pydantic models for each of the
  four document types and absolute/relative evidence. It separates model proposals
  from server-owned status/output fields and rejects unconfirmed text requests.
- **`backend/field_validation.py`** proposes deterministic date, money, source-span,
  and relative-anchor checks. It computes normalized values and days only when
  those checks pass, with policy choices documented for student review.
- **`backend/extraction.py`** sends confirmed text to the configured model with a
  strict schema and fixed untrusted-input instructions. It discards failed/partial
  responses, tracks actual reported usage, and passes proposals to the validators.
- **`frontend/field-cards.js`** renders the five source-backed cards using inert text
  nodes and explicit status labels. Source buttons highlight original confirmed-text
  offsets, including Unicode and relative-deadline anchor spans.
- **`tests/test_field_validation.py`** checks the proposed parsing and verification
  policies against numeric changes, missing sources, malformed values, and relative
  anchors. It makes dangerous failure cases concrete for student review.
- **`tests/test_extract.py`** exercises the request/provider contracts with explicit
  doubles rather than claiming model accuracy. It checks malformed/refused/partial
  replies, retry limits, abstention, no partial verified data, and privacy paths.
- **`tests/test_frontend_state.mjs`** runs the actual browser controller with small
  DOM/network doubles and deliberately delayed responses. It checks that Clear,
  page leave, and text edits prevent stale verification from returning.
- **`eval/extraction_smoke.py`** runs the eight original invented image fixtures
  through real reading and extraction and prints expected/actual/status rows. It
  stops on provider failure and never opens or evaluates held-out data.

The student must review/edit this proposal and record actual individual changes
in `AI_USAGE.md`; generated schemas and validators are not student-authored work.
M2's real-model and physical-phone acceptance checks remain incomplete while API
quota is unavailable. M3/M4 work has not been started.

Final checkpoint checks: **207 Python tests passed**, **4 Node controller race tests
passed**, JavaScript syntax checks passed, and dependency consistency passed. The
Python run has one pre-existing asyncio deprecation warning. These green tests do
not remove the live-extraction or physical-phone acceptance gaps above.

### M2 signed-amount correction — 2026-10-22

The readiness audit found a false verification: `Amount due: ($45.00)` was
accepted as positive `$45.00`. The fix rejects parentheses, unsupported surrounding
signs and clipped dollar/digit-only evidence instead of stripping context. New
validator/API regressions assert Please double-check (`unverified`) with no
normalized positive amount, while supported positive/zero controls still pass.
This does not resolve API quota, finish live/physical-phone acceptance, or implement
M3. Parenthetical amount evidence is conservatively unverified, even if it could
have an innocent interpretation; see DESIGN_NOTES.md for the policy/tradeoff.

### Organization invitation recheck — 2026-10-23

After the organization invitation, the configured API key still failed the live
integration check with a rate/quota rejection. `eval/reports/extraction-integration-2026-10-23.txt`
records the attempt and why subsequent fixtures were not run. It contains no
live field-accuracy results; the integration's deterministic today remains pinned
to 2026-10-22 rather than being the run date. All 232 Python tests and four Node
controller tests passed. Configure a key from the API organization/project that
actually holds the grant before retrying; organization membership alone does not
change the existing key. Milestone 3 remains paused at its required M2 precondition.

### Working API credential and security checks — 2026-10-23

The privately configured key now succeeds: one minimal OpenAI Responses request
returned HTTP 200, followed by successful live read/extract calls on all eight
original synthetic notices. All eight deadlines, eight actions and four supplied
numeric amounts were verified correctly. Four fixtures lack an amount: two returned
missing, while two were conservatively unverified rather than missing; no amount
was presented as verified for those four. The smoke command's equality column
checks normalized values only, so its True entries are not a full status/field
accuracy metric. Real-phone, handwriting and M4 evaluation remain separate.

`eval/reports/extraction-working-key-2026-10-23.txt` records the live eight-fixture
integration table, provider-reported successful token totals and the pinned today
value (2026-10-22). It contains invented fixture outputs only and is not a general
M4 scorer or a held-out result.

Credential audit: `.env` has mode 0600, belongs to the current user, has no extra
ACL entries, is ignored by Git, and is untracked. The current key was absent from
all other checked workspace files and Git objects (the local repository currently
has no Git objects). Twenty-one public/private-path response checks found no key;
private/dotfile/traversal probes returned 404. API responses are no-store and stay
outside the service worker's static allowlist. Provider code sends credentials
only as an Authorization header to the fixed OpenAI HTTPS endpoint, not inside
model prompts. The configured key was never printed or saved in a report.

Dummy-credential regressions cover public assets/configuration, authentication,
rate/server failures, unexpected exceptions and logs. The real credential is not
loaded by tests. Final checks: 239 Python tests and four Node controller tests
pass, with the existing Python 3.9 asyncio warning. These checks establish no
exposure on the audited paths; they cannot guarantee zero risk from compromised
machines, editor backups outside this workspace, or future changes. Keep keys
server-side and never commit `.env`; no key rotation is indicated by these checks.


## Milestone 3 review checkpoint — 2026-10-23

M2's technical preconditions passed: the text-confirmation flow works, live
extraction returns per-field statuses, and the automated checks pass. Source-matched
`Amount due: not specified`/`Deadline: not specified` markers now become missing
only when the field label and absence phrase agree in both source and snippet.
The eight M3 extractions returned 36 verified and four missing fields; this is an
integration observation, not M4's student-owned field-accuracy score. A separate
browser upload produced an incomplete action snippet and correctly left that
action unverified, showing why synthetic fixture success is not a guarantee.

`POST /api/explain` uses only verified values and snippets to write a short English
explanation. Number/date/amount checks reject unsupported numeric facts, retry once,
and then use a deterministic field template. Missing/unverified values are withheld
from the model and remain flagged. Translation protects facts with per-field
placeholders, requires glossary terms and fixed warnings/disclaimers, and performs
a separate back-translation check; a second failure displays English with an
explicit notice in the requested language. These checks cannot establish semantic
truth, a measured sixth-grade reading level, or native-language quality.

Language files drive the picker, labels, month names, direction, voice locales and
proposed glossaries. Spanish and Tagalog are shipped; every proposed glossary entry
remains `reviewed=false`. The help panel is visibly TODO with no invented contacts.
Only the language preference persists. Read-aloud uses a matching voice for the
actually displayed language; it never substitutes an unrelated language voice.

Run the opt-in comparison from the repository root (uses paid API calls):

```sh
.venv/bin/python -m eval.translation_check --env-file .env
```

The command opens only the original eight synthetic fixtures, supplies their known
types as explicit selections, and writes synthetic outputs to the evaluation
reports/review sheets. Production APIs never write notice content to disk. The
current [comparison table](eval/reports/translation-comparison.md) and
[raw synthetic results](eval/reports/translation-comparison.json) record the actual
model, pinned date, outputs, failed checks, fallbacks and reported usage.

| Requested language | Accepted guarded translation | Explicit English fallback | Plain baseline numbers/dates | Plain baseline month-name dates |
| --- | --- | --- | --- | --- |
| Spanish | 7/8 | 1/8 | 8/8 | 0/8 |
| Tagalog | 6/8 | 2/8 | 8/8 | 0/8 |

The baseline translates the whole raw notice; the pipeline translates the verified
English summary. Their coverage differs. Baseline disclaimer failure is an expected
structural difference because the plain prompt receives no fixed disclaimer.
Correct ISO dates count as preserved numbers/dates, while month-name formatting is
scored separately. The saved outputs were rescored after correcting that distinction;
no output was changed and no call repeated to improve a score. Back-translation is
heuristic, and zero relevant glossary terms is a vacuous pass. The experiment
recorded 98 responses with usage: 54,194 input and 19,554 output tokens; this excludes
separate prototype/browser calls and is not a cost estimate.

All **282 Python tests**, **11 Node controller/voice/Unicode tests**, JavaScript
syntax checks and dependency consistency checks pass. One existing Python 3.9
asyncio deprecation warning remains. Real browser QA checked Spanish/Tagalog display,
English-source disclosure, unverified-action preservation, and Spanish play/pause/stop.
This desktop has a Spanish voice and no matching Tagalog voice; the latter is
explicitly disabled. A separate, labeled synthetic 390px iframe exercised the real
card renderer/CSS with long strings and RTL direction. This is visual layout QA,
not a physical-phone or Arabic-language acceptance test.

The key remains in the private ignored `.env`, mode 0600. Production requests send
it only in the Authorization header to OpenAI's fixed HTTPS endpoint; it is never
in frontend assets, prompts, reports or logs. The final audit scope/results are in
`AI_USAGE.md`. No audit can promise immunity from every future change or machine
compromise. No commit, push or deployment was performed.

**Review first:** the incomplete browser action source and its uncertainty flag;
`court_01`/`court_02` Tagalog warning-related fallbacks; and `school_02` Spanish
back-translation disagreement. Then review the proposed schemas/validators,
glossaries and fixed UI translations. Ask actual Spanish/Tagalog readers to fill in
[Spanish review](eval/native_review_es.md) and [Tagalog review](eval/native_review_tl.md),
and test photo-to-results/read-aloud on your phone. Ratings/reviewer identities are
blank. Fill in real help contacts separately. Stop here for student review before M4.

### M3 new-file guide

- **`backend/language_config.py`**: Loads and validates trusted language data and exposes safe public metadata. It caches only configuration, never notices or credentials.
- **`backend/receipts.py`**: Signs exact server-checked fields with a separate in-memory secret. Receipts expire after one hour and cannot turn client-edited statuses into verified facts.
- **`backend/structured_model.py`**: Calls the Responses API with strict structured output and bounded retry. It returns sanitized failures and actual usage without logging prompts or provider bodies.
- **`backend/explanation_models.py`**: Defines strict explanation, card and request structures. It bounds content and keeps the response contract separate from factual validation.
- **`backend/language_guards.py`**: Checks numbers, dates, amounts, glossary terms and fixed warnings. It also protects facts and compares back-translations, with documented heuristic limits.
- **`backend/explanation.py`**: Builds verified-only English explanations and guarded translations. It uses field templates or explicit English fallback after failed attempts.
- **`backend/languages/en.json`**: Defines English UI, date formatting and voice metadata. It is the reference key set for the other language files.
- **`backend/languages/es.json`**: Defines proposed Spanish UI, month names and voice metadata. Its strings require human review before claiming linguistic quality.
- **`backend/languages/tl.json`**: Defines proposed Tagalog UI, month names and Filipino/Tagalog voice aliases. Its strings also remain unreviewed.
- **`backend/languages/glossary_en.json`**: Provides the empty English glossary required by the common data contract. No translation or reviewer identity is invented.
- **`backend/languages/glossary_es.json`**: Scaffolds eleven proposed Spanish official-term translations. Every entry is explicitly unreviewed with no reviewer assigned.
- **`backend/languages/glossary_tl.json`**: Scaffolds eleven proposed Tagalog official-term translations. Notes request native/context review and every reviewed flag remains false.
- **`backend/languages/help.json`**: Stores the clearly labeled TODO help-contact configuration. Phone, address and URL values are null until real resources are supplied.
- **`frontend/en.json`**: Mirrors the backend English configuration for offline bootstrap. Keep it synchronized when editing English language data.
- **`frontend/i18n.js`**: Discovers language configs, applies UI text/direction and remembers only a language code. It translates fixed reader warnings without persisting notice content.
- **`frontend/speech.js`**: Selects only a matching configured voice and implements play/pause/stop. It disables unavailable languages and cancels speech on clear or page leave.
- **`frontend/explanation.js`**: Requests explanations and renders guarded results, confidence notes and help placeholders. Abort/generation checks prevent late replies from restoring cleared or wrong-language output.
- **`tests/test_explanation.py`**: Tests corrupt translations, numeric/status preservation, receipts, fallbacks and privacy. Deterministic doubles test failure behavior without pretending to measure model accuracy.
- **`tests/test_language_ui.mjs`**: Exercises the actual explanation controller with delayed transports and checks voice selection. It also checks Unicode OCR highlighting and inert script-looking source text.
- **`eval/translation_check.py`**: Runs the original eight synthetic notices in two languages with a plain-translate baseline. It records actual outputs/usage and produces honest comparison and blank native-review artifacts.
- **`eval/reports/translation-comparison.json`**: Records the live synthetic outputs, check metadata and actual reported token usage. It contains no receipts, credentials, native ratings or held-out results.
- **`eval/reports/translation-comparison.md`**: Presents the guarded-pipeline and plain-baseline counts in one screenshot-friendly table. It states scope differences, fallback counts and measurement limitations.
- **`eval/native_review_es.md`**: Provides each original notice, English explanation, displayed Spanish result or English fallback and source snippets. Real reviewers must fill in the blank ratings, comments, names and dates.
- **`eval/native_review_tl.md`**: Provides the corresponding Tagalog review packet with explicit fallback status. It deliberately leaves ratings and reviewer details blank.

## Milestone 4 in progress — 2026-10-24

The student authorized a generated proposed field scorer for review. The new
`eval/m4/dev` set has 20 synthetic notices (5 parking, 5 court, 5 utility, 4 school,
1 unknown) and `eval/m4/adversarial` has eight hostile-body notices. Both include
clean/degraded copies. The old corpus is unchanged. See
[each new file explained](eval/M4_FILE_GUIDE.md).

```sh
.venv/bin/python -m eval.run --set dev --out results/new-dev.json
.venv/bin/python -m eval.run --set adversarial --out results/new-adversarial.json
```

These commands use the ignored backend credential and paid calls, with the fixed
same-family snapshot, temperature 0, reasoning none and today in `eval/m4-config.json`.
The snapshot and accepted reasoning levels are documented by
[OpenAI](https://developers.openai.com/api/docs/models/gpt-5.4-mini); one minimal
live probe verified access/settings before the experiment. Production defaults and
the private `.env` are unchanged. Reports include exact configuration and actual
reported token usage. A run name cannot be overwritten silently; `--dry-run` uses
no API, and explicit `--resume` is only for dev/adversarial with unchanged inputs.

The evaluation confirms OCR unchanged and explicitly selects the fixture type;
it does not simulate human corrections or claim automatic classifier accuracy.
The multi-page case processes only page 1 because the app accepts one photo. B1
plainly explains/translates that same OCR text, with all reported values treated as
facts. B2 uses the same extraction proposal as full with validation bypassed in the
offline harness; its config flags never disable public API validation. Full runs
the real validators, explanation and both languages. Strict copied-text scoring
requires reviewing possible semantic-equivalence mismatches, not claiming they
are automatically dangerous errors.

No pipeline fix, freeze tag or held-out run is authorized before the Part C choice.
The held-out README/template are scaffolds only; ten student-supplied cases remain
pending. Do not inspect them during development. The known source-supported hostile
amount gap is captured as a visible expected-failure regression until a fix is
chosen. Do not describe that expected failure as passing adversarial acceptance.


### M4 Part C results and pause

The full pipeline did **not** beat either baseline on the headline metric:
all three had **6/360 (1.67%)** wrong Verified critical facts on dev and **0/144**
on adversarial. All six dev critical errors came from selecting one of two
conflicting hearing dates. There were also three clipped-contact verifications
outside the critical-field headline. These are repeated correlated synthetic cases,
not a population estimate. Full's usable verified critical accuracy was 270/276;
B1/B2 were 276/276. Ambiguous fields are outside that accuracy denominator but
inside the false-verification denominator, so 100% accuracy does not mean safety.

Use [dev table](results/m4-dev-review.md),
[adversarial table](results/m4-adversarial-review.md),
[FAILURES.md](FAILURES.md), and [evidence pack](docs/EVIDENCE.md) for review.
Original `*-before.json/.md` artifacts preserve initial scoring, including the
identified measurement issues. The `*-review` artifacts correct explicit absence
claims and declare contact-name aliases, preserving every model output. Rebuild
saved tables without API calls:

```sh
.venv/bin/python -m eval.rescore --input results/m4-dev-before.json --out results/rebuilt-dev.json
.venv/bin/python -m eval.rescore --input results/m4-adversarial-before.json --out results/rebuilt-adversarial.json
```

All 48 live adversarial notice runs retained the expected critical values. A
simulated hostile source-supported amount still bypasses the validator; live
success therefore does not establish injection immunity. Two strict expected-failure
security regressions remain visible pending fixes. `FAILURES.md` lists five ranked
general fix options; no app fix was made after observing these results. Stop here
for the student's Part C choice before Part D, commits, freeze or heldout.

Final local checks: **323 Python tests pass**, **two known unsafe-validator
regressions are expected failures**, and **14 Node tests pass**. Dependency and
frontend syntax checks pass, with the existing Python 3.9 asyncio warning. CI is
defined but has not run on GitHub. Saved dev/adversarial tables reproduce exactly
without API calls. API keys remain owner-only, ignored and absent from audited
reports/assets; heldout is excluded from even credential scans.




Selected fixes 1–2 pass local regressions; valid live post-fix evaluation is in progress. Initial post-fix provider-unavailable runs do not establish improvement. No heldout/freeze has happened.


## Part D selected fixes validated — 2026-10-24

Both selected fixes are complete, with successful full reruns in order and local
commits. Use the current FAILURES.md/docs/EVIDENCE.md sections and
[latest dev table](results/m4-round2-live-dev.md) /
[latest adversarial table](results/m4-round2-live-adversarial.md).
345 Python and 14 Node tests pass; no expected failures remain. Failed-access
attempts are retained but excluded from quality claims. Heldout remains untouched,
awaiting ten supplied cases after the code freeze. Residual contact/source and
language limitations are disclosed; no deployment or push was performed.


## Final held-out review checkpoint — 2026-10-24

Ten student-supplied images and their independent answer key were evaluated once with the original eval-freeze sources. The frozen scorer flags critical false-verifications of B1 17/30, B2 8/30 and full 4/30; full is worse than dev 0/360 and all providers were available. These exact-match counts include a genuine $75.00 → $75.60 OCR error, two incomplete actions and one harmless wording difference; the raw scores were not revised.

Review [the held-out analysis](results/heldout-review.md), [unchanged table](results/heldout-final.md) and [current evidence](docs/EVIDENCE.md). This closes the selected Part D run and stops for student review; no further tuning, new held-out attempt or Milestone 5 work was started. Earlier pending statements are historical.


## Reliability repairs after held-out review

The repaired version requires a separate amount-photo review, shows disagreements between two local OCR image treatments, and flags clipped action instructions. Supported date/amount context no longer fails merely because one sentence contains both types of number. See [current validation and limits](results/reliability-summary.md).

383 Python and 17 JavaScript checks pass; fresh live development/adversarial results and their deliberately reduced unattended amount coverage are recorded there. Original eval-freeze and held-out artifacts are preserved; no new held-out claim is made.
