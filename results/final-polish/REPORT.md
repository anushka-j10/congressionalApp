# Final polish verification — October 26, 2026

Starting commit: `bbfb6c6`, branch `design/mobile-format-review`.

This pass clarifies the current app and prepares the [2.0 implementation prompt](../../NOTICE_DECODER_2_0_PROMPT.md). It does **not** fix or remeasure the Northeast extraction failures. It has not been deployed.

## Changes

- Welcome names the four supported notice categories. Tutorial and photo guidance specify one printed English page, manual text/type/amount review, English fallback and device-dependent read-aloud.
- API `verified` displays as **Text match**, with an explicit warning that reading errors, wrong dates and incomplete instructions can pass. **Not identified** does not mean the notice lacks the field. Source controls refer to reviewed English text, not an untouched original.
- Field uncertainty appears once in each card instead of repeating in a separate warning list. The explanation omits only an exact duplicate of the shared status definition; specific cautions and the disclaimer remain visible.
- Pending English field messages no longer insert a translated field name. UI labels and source controls carry their selected-language metadata; source buttons name their field for screen readers. The home target is at least 44px high; longer translated badges wrap within narrow screens.
- Internal API/TODO/student-configuration wording is replaced with usable explanations. Privacy copy explicitly mentions server OCR and OpenAI text processing; the footer directs users to verify with the issuer.
- English, Spanish and Tagalog catalogs are synchronized with new keys, and the offline English copy matches backend English. Translations remain proposed and unreviewed by native speakers.
- Service-worker shell cache advances to v19. Model instructions, validators, status enums, endpoint contracts, original held-out records and Northeast results are unchanged. Catalog wording also appears in deterministic explanation templates; no live model call was made to assess that wording.

## Checks and evidence

| Check | Result | Evidence |
|---|---|---|
| Python regressions | PASS — 430 passed, one existing Starlette/AnyIO deprecation warning | [pytest.txt](pytest.txt) |
| JavaScript regressions | PASS — 62 passed, zero failures | [node.txt](node.txt) |
| Phone-width layouts | PASS — 63 combinations; no horizontal overflow; all visible tested buttons, selects, links and summaries at least 44px in both dimensions | [phone-checks.json](phone-checks.json) |
| Source action | PASS — contact source opened, exact snippet highlighted, focus moved to source | `sourceCheck` in phone-checks.json |
| Visual inspection | PASS for the inspected welcome and compact result states at 390px | [welcome](welcome-390.png), [results](results-390.png) |
| Secret handling and historical integrity | PASS for the scoped checks recorded below | [integrity-security.json](integrity-security.json) |
| Live model/extraction accuracy | NOT RERUN — no new accuracy claim | Prior [stress report](../northeast-stress/REPORT.md) remains the evidence |
| Physical-phone / deployed acceptance | NOT RUN in this pass | Requires separate device and deployed-URL checks |

The browser matrix is seven states × three widths × three interface languages: welcome, tutorial steps 1–4, reader and synthetic results; 320/390/430px; English/Spanish/Tagalog. The frame height was 844px. These are desktop browser layout checks, not device emulation, native-speaker review or a WCAG conformance audit. Synthetic results use the real card renderer and include missing, unverified and checked fields. Example values remain English; translation generation is not mocked into a success claim.

The scoped visual pass did not upload a real notice or exercise camera permission, HEIC decoding, audio, offline installation, every expanded panel or a screen-reader session. Automated suites retain the existing checks for those code paths where available; physical-device behavior remains unmeasured.

## Commands

From the repository root, using the previously installed audit environment:

```sh
../../work/m4-audit-venv/bin/python -m pytest -q > results/final-polish/pytest.txt 2>&1
/opt/homebrew/bin/node --test tests/*.mjs > results/final-polish/node.txt 2>&1
git diff --check
```

The localhost inspection server was started with credentials disabled:

```sh
OPENAI_API_KEY='' OPENAI_MODEL='' APP_ENV=development RENDER=false \
  ../../work/m4-audit-venv/bin/python -m uvicorn backend.main:app \
  --host 127.0.0.1 --port 8023 --no-access-log
```

The separate scratch layout harness was `../../work/polish_preview.py` on `127.0.0.1:8024/__preview__`; it disables credentials, mounts the real app, and offers a clearly labeled synthetic-result fixture. Browser interactions used the Codex in-app browser. This pass reused an existing environment; it is not a new clean-install audit.

## Remaining work

The [2.0 prompt](../../NOTICE_DECODER_2_0_PROMPT.md) distinguishes current functions from known bugs, unmeasured behavior, future coverage and human review. Its highest priority is correcting suspicious date anchors, inclusive deadline counting, OCR-corrupted contacts and timing, omitted restrictions, and multiple obligations. It specifies acceptance tests and preserves the original held-out freeze and evidence. A friendlier interface does not make the app ready for unattended legal or payment decisions.
