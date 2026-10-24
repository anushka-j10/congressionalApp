# AI usage disclosure

This log records AI assistance; it does not claim independent student authorship.
The student must review and understand all generated code and record their own
contributions separately. No extraction schema, deterministic validators, or eval
scoring logic has been generated in Milestone 0.

| Date | Assistant contribution | Files |
| --- | --- | --- |
| 2026-10-21 | Generated the Milestone 0 scaffold, environment template, and dependency pins. | `.gitignore`, `.env.example`, `requirements.txt` |
| 2026-10-21 | Generated the FastAPI health route, server-only configuration, and static file hosting. | `backend/main.py` |
| 2026-10-21 | Generated the responsive shell, connection check, PWA manifest, static-only service worker, and geometric notice icons. | `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`, `frontend/sw.js`, `frontend/manifest.webmanifest`, `frontend/icons/icon-192.png`, `frontend/icons/icon-512.png` |
| 2026-10-21 | Generated scaffold tests for health, environment handling, asset serving, private-file isolation, and the cache boundary. | `tests/test_app.py` |
| 2026-10-21 | Wrote setup, architecture, file explanations, phone verification steps, and this disclosure. | `README.md`, `AI_USAGE.md` |
| 2026-10-21 | Recorded successful automated checks and browser checks, including cached reload with the server stopped and API recovery after restart. | `README.md`, `AI_USAGE.md` |

## Milestone 1 assistant changes (2026-10-21)

- Generated `backend/images.py`: bounded in-memory multipart parsing, actual-image validation, HEIC decoding, EXIF orientation, metadata stripping, and JPEG normalization.
- Generated `backend/readers.py`: TextReader interface, local Tesseract stdin/stdout adapter, OpenAI vision adapter, and short/garbled-text warnings.
- Generated `backend/classifier/signals.py` with empty student TODO lists only; generated `backend/classifier/scoring.py` with weighted matching, ambiguity rejection, and documented heuristic confidence. Real signal lists and weights remain student-owned.
- Updated `backend/main.py`, `.env.example`, and `requirements.txt` for reader selection, `/api/read`, public reader/privacy configuration, no-store headers, sanitized metadata logging, and image dependencies.
- Generated `frontend/image-prep.js` and updated `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`, and `frontend/sw.js` for camera/library selection, client-side conversion/downscaling, preview, upload, results, errors, clear controls, reader disclosure, and static-only offline caching.
- Copied the unmodified third-party heic-to 1.6.6 CSP build and LGPL license from npm into `frontend/vendor/heic-to.js` and `frontend/vendor/heic-to.LICENSE`. These files are dependency code, not student or assistant original work.
- Generated `eval/generate_samples.py` plus eight synthetic PNG/JSON pairs under `eval/samples/` (parking_01/02, court_01/02, utility_01/02, school_01/02); fictional notices and future expected facts only, with no extraction schema or eval scoring implementation.
- Generated `tests/test_classifier.py`, `tests/test_read.py`, and `tests/test_integration.py`: toy-signal scoring tests, image/HEIC/orientation/privacy tests, mocked vision contract checks, and a real-reader eight-sample API table.
- Rewrote `README.md` with Milestone 1 setup, reader tradeoffs and provider-retention limits, architecture, scoring math, file-by-file explanations, synthetic sample roles, real verification results, and phone review steps; updated this disclosure.
- Generated a scratch synthetic orientation-tagged HEIC under workspace `work/` for browser QA; it is not user notice data or an additional evaluation sample. Captured the real integration table in `eval/milestone1-results.txt`.
- Added an API-level toy-signal test to `tests/test_read.py` to verify matched signals and confidence reach the response without adding real production signals. Recorded automated and browser verification, and its limits, in `README.md`.

## Milestone 2 / A1 assistant changes (2026-10-21)

- Refactored `eval/generate_samples.py` to share visible text and the original clean layout with ground-truth generation; no runtime reader, image-normalization, classifier, API, or frontend code was changed.
- Generated `eval/generate_reader_samples.py`: preserved M1 originals, clean reproductions, six separately labeled degradations plus combined phone effects, paired UTF-8 truths, and a fixed-parameter corpus manifest.
- Generated `eval/reader_bakeoff.py`: whitespace-normalized character error rate, exact-digit key-token recall, missing-token diagnostics, reader/condition aggregation, configurable TextReader factories, and explicit not-run/N/A states.
- Created `eval/samples/handwriting/README.md` with automatic paired-photo/truth discovery conventions; no handwriting photos or handwriting accuracy were invented.
- Generated `tests/test_reader_bakeoff.py` to check exact edit distance, digit-error rejection, repeated-token accounting, corpus labeling, unchanged clean fixtures, deterministic degradations, missing handwriting truths, failure accounting, and weighted aggregation.
- Kept the corpus manifest at `eval/reader-corpus.json`, outside the eight original expected-field JSON files, to preserve the M1 integration test's fixture boundary.
- Added the detected ground-truth token inventory and production/corpus fingerprints to bake-off reports; no raw OCR transcript is saved. Generated clean/degraded image-truth pairs and the eight original-image `.txt` ground truths under `eval/samples/`.
- Generated `DESIGN_NOTES.md` and updated `README.md` with metric definitions, normalization rules, actual baseline results, limitations, preservation evidence, new-file explanations, and the explicit A1 review boundary. Recorded real baseline metrics in `eval/reports/reader-baseline.json` and `eval/reports-a1-table.txt`; no model credentials were configured and no handwriting samples were fabricated.
- Generated `eval/reports/reader-baseline-analysis.md` with condition-level failures and every missed expected token, plus `eval/reports/A1_FILE_GUIDE.txt` with two-sentence explanations of all 146 A1-created files. Stopped at the requested A1 review checkpoint before reader fixes or extraction.

## Milestone 2 / A2 assistant changes (2026-10-21)

- Created a private ignored `.env` by copying blank placeholders from `.env.example`, without entering or printing credentials, and opened it for the user to configure.
- Added `backend/preprocessed_reader.py` with OpenCV grayscale conversion, median denoising, Hough-line deskew, upscaling, adaptive thresholding, and in-memory PNG output; pinned OpenCV/NumPy in `requirements.txt`.
- Added `backend/reader_tokens.py` and `backend/hybrid_reader.py` to keep actual cross-reader candidates, normalize cosmetic differences without fixing digits, and label agreement/disputes conservatively.
- Updated `backend/readers.py`, `backend/main.py`, and `.env.example` for explicitly selectable preprocessed/hybrid readers and optional candidate responses; kept `TEXT_READER=tesseract` as the default.
- Updated `eval/reader_bakeoff.py` for four-reader comparison, RAM-only component reuse, separate displayed-transcript and shown-candidate recall, one-to-one candidate scoring, new reader fingerprints, and an A2 report path that preserves the A1 baseline.
- Generated `frontend/token-review.js` and updated `frontend/app.js`, `frontend/index.html`, `frontend/styles.css`, and `frontend/sw.js` to show every actual hybrid alternative, distinguish agreement from verification, and highlight disputed tokens in the primary transcript. Added optional primary-reader metadata in `backend/readers.py`, `backend/hybrid_reader.py`, and `backend/main.py` so highlights use the correct source.
- Generated `tests/test_reader_comparison.py` for preprocessing, deskew direction, actual cross-reader candidate provenance, digit disputes, component failures, one-to-one candidate recall, API/UI payloads, RAM-only caching, and real preprocessed-request privacy.
- Added sanitized vision status categories in `backend/readers.py` and a RAM-cached one-image preflight in `eval/reader_bakeoff.py`, so invalid credentials/model access or quota failures stop provider comparisons without repeated failed requests or logged response contents.
- Added signed-amount disagreement and empty-local-transcript tests/fixes in `backend/reader_tokens.py`, `backend/hybrid_reader.py`, and `tests/test_reader_comparison.py`; added count-only progress output to `eval/reader_bakeoff.py` without notice contents.
- Generated `eval/reports/handwriting-cloud-options.md` with sourced dedicated-OCR cost/privacy comparisons and labeled setup estimates; configured none of those services. Created a clearly labeled synthetic renderer harness in workspace `work/a2-ui-review/` for browser QA, using actual hybrid code with test doubles rather than claiming a live vision result.
- Updated `README.md` and `DESIGN_NOTES.md` with the measured local improvement, 429-blocked provider comparison, algorithm choices, candidate accounting, new-file explanations, remaining A3/handwriting limitations, and pending reader selection. Captured the synthetic renderer QA screenshot at workspace `outputs/a2-candidate-ui-test.png`.
- Generated `eval/reports/reader-local-comparison.json`, `eval/reports-a2-local-table.txt`, `eval/reports/reader-comparison.json`, `eval/reports-a2-table.txt`, and `eval/reports/reader-comparison-analysis.md` from real local measurements and the single 429-blocked vision preflight; no vision/hybrid accuracy numbers were fabricated. Verified 111 passing tests, JavaScript syntax, dependency consistency, frozen corpus/original images, and unchanged `TEXT_READER=tesseract` default.

## Student contribution record

- Created the public GitHub repository.
- Planned student-owned work: extraction schema, deterministic validators, and evaluation scoring.
- Code review, edits, and independent implementation: record specifics here as completed.

## Verification limits

Automated and browser checks are reported in the milestone handoff. Installing on
a physical phone requires a separate device check. Contest eligibility and the
amount of individual contribution must be checked against the official rules;
this log alone does not establish eligibility.

## Milestone 2 / A3 assistant changes (2026-10-22)

- Updated `frontend/index.html`, `frontend/app.js`, and `frontend/styles.css` with an editable, bounded Check the text screen and explicit user confirmation. Editing invalidates confirmation; original OCR/candidate evidence stays unchanged, and clear/page leave removes both original and edited text from the UI and memory references.
- Updated `frontend/token-review.js` to highlight explicit unreadable/replacement-character markers alongside actual hybrid disputes, without correcting characters or claiming a handwriting detector. Updated `frontend/sw.js` shell version for the new static UI.
- No reader selection, extraction schema, deterministic field validators, API extraction call, or student-owned classification signals changed in this step; reader and ownership questions are pending.

## Milestone 2 / Part B proposed implementation (2026-10-22)

- The student explicitly selected the local preprocessed reader and authorized Codex to generate proposed extraction schemas and validators for review, changing the earlier implementation ownership boundary for this proposal. This authorization does not count the generated code as independent student work.
- Generated `backend/extraction_models.py` with strict per-document Pydantic models, nullable model-proposed fields, absolute/relative deadline evidence, confirmed-text requests, and server-owned checked-field statuses.
- Generated `backend/field_validation.py` with proposed plain-code date/amount parsing, source spans, tightly bounded OCR-letter fuzzy matches with exact numeric sequences, relative-deadline arithmetic, and conservative missing/unverified states.
- Generated `backend/extraction.py` with a strict JSON-schema Responses API adapter, untrusted-notice instructions, bounded retry, actual token-usage metadata, refusal/incomplete/malformed-output rejection, and validation orchestration. Consulted the official OpenAI Structured Outputs documentation; no model or key was hardcoded.
- Updated `backend/main.py` with bounded JSON-only `/api/extract`, sanitized validation/provider errors, injectable NJ-local today, unknown-type abstention, no-store responses, and metadata-only logging. Switched default/template and only the private `.env` reader entry to the explicitly selected `preprocessed` option; pinned the installed Pydantic version in `requirements.txt`.

- Generated `frontend/field-cards.js` for inert-text field cards, status labels, verified-only normalized values/days, and source/anchor highlighting with Python-to-JavaScript Unicode offset conversion.
- Updated `frontend/index.html`, `frontend/app.js`, `frontend/styles.css`, and `frontend/sw.js` for explicit user document-type selection, text-only extraction disclosure, confirm/extract requests, safe error states, stale-result invalidation, and the new static renderer allowlist entry. Unknown types abstain; no student classifier rules were generated.

- Added `tests/test_field_validation.py` (64 focused cases) and `tests/test_extract.py` for source/digit/sign safety, supported/unsupported dates, anchored relative deadlines, simulated bad model values/snippets, strict provider request/envelope handling, bounded retry, actual usage accumulation, API input limits, unknown-type abstention, and success/failure privacy.
- Added opt-in `eval/extraction_smoke.py` to run the eight original invented fixtures through real local reading and model extraction, printing expected/extracted/status comparisons. This integration check supplies each fixture’s known type explicitly, does not implement the general M4 scorer, and stops on provider unavailability rather than manufacturing results.
- Updated `tests/test_reader_comparison.py` to assert the now explicitly chosen preprocessed default. Added whole-number/ID/source-sign boundaries, rejection of competing numeric evidence inside a snippet, and strictly boolean text confirmation; these prevent matching a shorter value inside a larger or negative source token.
- The 2026-10-22 live integration attempt stopped on HTTP 429 after one fixture and one permitted retry. Saved `eval/reports/extraction-integration.txt` with NOT RUN/unmeasured field results; no live extraction accuracy or successful usage was claimed, and the remaining fixtures were not sent.
- Browser QA used a clearly labeled scratch synthetic extractor in workspace `work/m2-ui-review/server.py` with the actual app, real preprocessed OCR, and actual deterministic validators. Checked phone-width cards, source highlighting including a leading non-BMP emoji, inert script-looking source text, edit invalidation, and provider-error clearing; this is not live model or physical-phone evidence.

- Updated `README.md` and `DESIGN_NOTES.md` with the explicit student reader/ownership decisions, gate evidence, proposed schema/validator policies, new-file explanations (two sentences each), setup/flow, accurate quota-blocked integration results, browser test limits, and outstanding physical-phone acceptance. Earlier A1/A2 descriptions remain marked as historical.

- Updated `frontend/app.js` to abort active read/extract requests on Clear/page leave and ignore late preparation/read/extraction results via a request-generation guard. Clear remains available while a notice request is running; an old completion cannot repopulate cleared data or unlock a newer operation. Bumped the static shell version in `frontend/sw.js`.

- Generated `tests/test_frontend_state.mjs` to exercise actual frontend controller code with delayed transport/DOM doubles: Clear during reading, stale extraction during a newer read, page leave, and edit invalidation. All four race/privacy checks passed; no npm dependency or additional provider call was used.

- Final verification: 207 Python tests passed (one pre-existing Python 3.9 asyncio deprecation warning), four Node controller race tests passed, frontend JavaScript syntax checks passed, and pip reported no broken requirements. Cleared the synthetic browser notice after QA and stopped the scratch test server; live extraction and physical-phone acceptance remain incomplete due to API quota/no device measurement.

## Milestone 2 readiness fix — 2026-10-22

- Extended `tests/test_field_validation.py` and `tests/test_extract.py` with regression cases for parenthesized/accounting-style amounts, incomplete parentheses, Unicode minus and trailing signs, clipped snippets, positive controls, and the API's returned amount status. These test the newly found false-verification gap without adding sample-specific production rules.

- Fixed `backend/field_validation.py` to preserve/reject unsupported monetary context: parentheses (including incomplete ones), Unicode sign prefixes, trailing signs, and clipped money snippets. The rules abstain rather than turning signed/ambiguous evidence into a positive value; ordinary positive and zero amounts remain supported.
- Before the fix, the extended focused run reproduced 13 failing safety cases (including the API regression). These are targeted regression cases, not a representative false-verified-rate evaluation.

- Extended the clipped-snippet checks and regressions to digit-only money snippets as well as dollar-prefixed snippets. Source-span validation looks past an immediately preceding dollar mark so the model cannot hide a surrounding negative sign or parenthesis by quoting only the digits.

- Updated `DESIGN_NOTES.md` and `README.md` with the reproduced root cause, general sign/context policy, intentional conservative abstention tradeoff, regression evidence, and unchanged live-M2/M3 blockers. No new files, cloud services, credentials, classification rules, M3 code, or M4 scoring were generated in this correction.

- Final correction checks: 232 Python tests and four frontend controller tests passed; JavaScript syntax and dependency consistency passed. One pre-existing Python 3.9 asyncio deprecation warning remains. Refreshed the local preview to load the corrected validator; no additional paid model call was made while quota remains unresolved.

## M2 organization-invitation recheck — 2026-10-23

- Reran all existing checks after the student reported an organization invitation: 232 Python tests and four frontend controller tests passed, with one existing Python 3.9 asyncio warning.
- Reran the opt-in synthetic live integration check with the configured private `.env`; it stopped at the first fixture on an API rate/quota rejection, after the existing single retry. Saved `eval/reports/extraction-integration-2026-10-23.txt`; no live field accuracy was measured and remaining samples were not sent.
- Opened the existing ignored `.env` for the student to configure an API key from the credited organization's project; no credentials were printed, generated, or changed by Codex. An organization invitation does not reassign a previously created Personal-project key.
- Honored Milestone 3's explicit precondition stop: no M3 implementation or M4 work was started while live M2 extraction remains blocked.

## API credential security verification — 2026-10-23

- Audited the configured credential without printing it or recording a fragment/hash: `.env` is owner-only 0600, owned by the current user, Git-ignored and untracked. The current key was absent from every other checked repository file and all Git objects (this local repository currently has no objects/commits).
- Loaded the actual configured credential only in process memory for a one-request OpenAI Responses API access test; HTTP 200 confirmed working access. No real notice was sent, and no credential appeared in the returned response. The credential was not placed in prompts, reports, tool arguments, or command-line arguments.
- Checked 21 actual app HTTP responses, including the fixed public shell allowlist and private/dotfile/traversal probes. No checked response contained the key, every probed private path returned 404, and API paths remain outside the service worker cache allowlist.
- Added fake-credential regression tests in `tests/test_app.py`, `tests/test_extract.py`, and `tests/test_read.py` for public routes/assets, no-store headers, provider credential use only in Authorization headers to the fixed HTTPS endpoint, exclusion from prompts, sanitized auth/rate/server errors, and unexpected-exception logging. Tests never load the real credential.

- Completed fake-credential regressions: 239 Python tests and four Node controller tests passed, with the existing asyncio warning. Broadened the actual-key scan to the whole task workspace (excluding the sole `.env`, virtualenv and Git internals) and found no copies; macOS file metadata showed 0600 and no additional ACL entries.
- Ran `eval/extraction_smoke.py` with the working key on the eight original synthetic notices and saved `eval/reports/extraction-working-key-2026-10-23.txt`. Eight deadlines, eight actions and four numeric amounts were verified correctly; four absent amounts had no verified numeric value, with two missing and two conservatively unverified. Reported actual successful-response token usage; did not call the normalized-value comparison a complete status-accuracy metric.
- Updated `README.md` with the credential audit scope, new report explanation, live integration evidence and limits. Restarted the local preview so its server process reloads the new private key; no key was printed, added to any prompt, copied into frontend assets, or recorded in reports.

## M2 final absence handling / M3 start — 2026-10-23

- Updated `backend/field_validation.py` with general, source-matched labeled-absence handling for amounts/deadlines. Added six regressions in `tests/test_field_validation.py`; explicit absence becomes missing only when the marker and field label agree in both snippet and actual source, with no inferred value.
- Technical M2 preconditions are available: live original synthetic read/extract works, per-field statuses and source highlights exist, and automated checks pass. Physical-phone/handwriting checks remain unmeasured; student classification rules remain empty, with explicit user type selection.

- Generated `backend/languages/en.json`, `es.json`, `tl.json`, three matching glossary files and `help.json` for data-driven UI/month names/voice locales, fixed warnings/disclaimers, proposed unreviewed translations, and null TODO help contacts. No native reviews or real contact details were invented.
- Generated `backend/language_config.py`, `explanation_models.py`, `language_guards.py`, `explanation.py`, and `structured_model.py` for trusted language loading, strict bundles, verified-only English input, numeric/date/amount/status checks, protected translation facts, separate back-translation checks, bounded retry, template/English fallbacks and sanitized provider calls. Back-translation text similarity is a heuristic, not proof of semantic accuracy.
- Generated `backend/receipts.py` for short-lived HMAC receipts using a separate random in-memory server secret. These bind explanation requests to exact server-issued fields/statuses without storing notice data or exposing/deriving from the API key.

- Updated `backend/main.py` with `/api/languages`, bounded JSON-only `/api/explain`, localized fixed errors, exact receipt validation before model use, independent in-memory signing secret, and receipts on extraction responses. API no-store and metadata-only logging remain; no prompt, credential or notice text is added to logs.

- Generated `frontend/i18n.js`, `explanation.js`, `speech.js`, and static offline `frontend/en.json`; updated the HTML/controller/cards/token-review/styles/service-worker for data-driven UI language, device-only language preference, guarded explanation requests, translation confidence/fallback banners, original-English toggles, TODO help contacts and matching-voice-only play/pause/stop.
- Updated `tests/test_frontend_state.mjs` import doubles for the new controller integrations while retaining its actual-controller stale-response/privacy checks. Generated `tests/test_explanation.py` with 31 passing verified-only, corrupted-output, glossary/date/number/status/fallback, receipt integrity, privacy and credential-boundary tests before frontend integration.

- Generated `eval/translation_check.py` for opt-in real read/extract/explain/translation/back-translation calls on the eight original synthetic fixtures in Spanish and Tagalog, plus a plain raw-notice translation/back-translation baseline. It records actual raw synthetic outputs/usage (omitting receipts), table counts, honest unavailable rows, scope differences, and unfilled native-review sheets; it never reads held-out data or invents ratings.
- Added raw-baseline numeric/date/amount/glossary/disclaimer checks to `backend/language_guards.py`. These apply the requested M3 mechanical checks, not the student-owned M4 field/false-verified scoring logic.

- Generated `tests/test_language_ui.mjs` with real-controller delayed-response tests for Clear, language switching, page leave, partial-output failure, and matching-voice/alias selection. Adjusted logical RTL spacing/direction and disabled text-area autocomplete; extended language API privacy tests to forbid disk-backed temporary files.

- Added data-driven translations for reader warnings and refreshed dynamic reading labels when the language changes. Updated original OCR candidate highlights to convert Python code-point offsets correctly when a notice contains a non-BMP character; no OCR digits or text were repaired.

- Audited the live comparison metrics and corrected a measurement conflation in `plain_translation_checks`: retained ISO dates are now normalized alongside localized month-name dates before numeric/date comparison. Month-name formatting is reported separately, so a correct retained numeric date is not mislabeled as a changed number. Added three regressions and rescored saved actual outputs locally without rerunning or changing any model output.

- Extended numeric sequence guards in `backend/language_guards.py` and `backend/field_validation.py` to include Unicode decimal digits after NFKC, so an added non-ASCII number or changed contact digit cannot masquerade as harmless letter noise. Added regressions plus a temporary, data-only long-string/RTL language test; no additional language is shipped.


- Completed the live M3 comparison on eight original synthetic notices in Spanish and Tagalog. Saved real outputs and usage, a comparison table, and two unfilled native-review packets; 7/8 Spanish and 6/8 Tagalog translations were accepted, with 1/2 explicit English fallbacks. Both plain baselines preserved numeric/date facts in 8/8; different raw-notice versus verified-summary scopes prevent field-accuracy or linguistic-quality claims.
- The experiment recorded 98 successful responses with reported usage (54,194 input / 19,554 output tokens), excluding separate prototype/browser calls. No held-out data was opened, no student-owned M4 scorer was generated, and no native ratings/reviewer identities or phone evidence was invented.
- Real browser QA used an invented parking notice with live OCR/extraction/explanation. An incomplete model action snippet remained unverified and its value was withheld in Spanish/Tagalog; verified date/amount and one-tap original English were visible. Spanish play/pause/stop responded; no matching Tagalog voice was available, so the button was disabled with a message. This is desktop-only evidence.
- Browser language switching exposed stale status/help/photo metadata in the prior language. Updated `frontend/app.js`, `explanation.js`, `i18n.js`, `index.html`, all three language configs, the English bootstrap and service-worker version to refresh fixed strings and translated photo alt text; added a controller regression. Updated warning wording to match localized warning lists.
- Added an actual `token-review.js` renderer test for non-BMP offsets, unreadable markers and inert script-looking text. Extended final Node coverage to eleven tests; all 282 Python tests, eleven Node tests, frontend syntax and dependency consistency pass, with one existing Python 3.9 asyncio warning.
- Tested production renderer/CSS visually inside a labeled synthetic 390px RTL/long-string iframe in `work/m3-layout-qa/server.py`. Saved narrow-layout and actual Spanish/Tagalog screenshots outside the repo in task outputs; wrapping stayed within the frame, but the connector could not measure iframe document overflow. No physical-phone or native RTL-language acceptance was claimed.
- Updated `README.md` and `DESIGN_NOTES.md` with current M2/M3 state, new-file explanations, data/receipt/guard/privacy design, usage and measurement correction, actual results, review priorities and remaining acceptance. Retained earlier sections as explicitly historical snapshots. M3 code is ready for student review; M4 has not started.

- Final credential audit after M3: `.env` is owner-only 0600, current-user-owned, Git-ignored and untracked, with no extra ACL entries. The current key was absent from 258 other checked workspace files and from Git objects (none exist locally); 26 actual HTTP response probes found no key, all private-path probes returned 404, and API responses were no-store. No real credential was printed, copied into tests, included in a report, or sent in a prompt.
- Cleared the synthetic notice, stopped the scratch layout server and restarted the single-process local preview with final code. Reload retained the chosen Tagalog language but no photo, notice, fields or explanation. Left the clean preview open at http://127.0.0.1:8003; no commit, push or deployment was performed.

## M4 Part A / precondition check — 2026-10-24

- Re-read the repasted M4 request, DESIGN_NOTES.md and AI_USAGE.md; no AGENTS.md was found in the workspace tree. Rechecked M2/M3: 282 Python and 11 Node tests pass, with the existing asyncio warning. Physical-phone/native review remains unmeasured and empty student classifier signals still produce unknown.
- Asked whether Codex may generate the student-owned proposed M4 scorer; scoring implementation remains pending that answer. This does not block independent synthetic fixture generation or harness plumbing.
- Generated `eval/generate_m4.py` and `eval/m4/{dev,adversarial}/` with 20 dev notices (the eight original fixtures plus twelve additions, including unknown), eight hostile-body notices, deterministic clean/degraded images, one additional-page image, per-notice ground truth and manifests. Original M1/M2/M3 corpus files were not overwritten. No real people, contacts or agency logos were used.
- Created only the requested `eval/heldout/README.md` and `expected-fields.template.json`; did not search for, read or run any held-out sample. The README specifies a freeze gate and a run-start ledger; no held-out numbers are claimed.
- Corrected fixture annotations before evaluation: unknown has no contact; conflicting-date truth is explicitly ambiguous rather than absent. This is ground-truth preparation, not pipeline tuning. Dev counts are 5 parking, 5 court, 5 utility, 4 school and 1 unknown (20 total).
- Created `eval/m4-config.json` with a fixed same-family model snapshot, temperature 0, reasoning none, NJ today, three repeats, two languages and clean/degraded variants. Consulted official OpenAI model/parameter docs; the production `.env` and model settings are unchanged. Numeric temperature support will be verified before a large run; no silent model/temperature substitution is allowed.
- Created `eval/protocol.py` for safe declared-synthetic input loading, code/corpus fingerprints excluding heldout/credentials, and a freeze/tag/single-use ledger gate. Evaluation-only B2 flags are specified in config; no public API switch can disable production validators.
- The student explicitly authorized a generated proposed M4 scorer for review on 2026-10-24. It will be logged as Codex-generated, not student-authored.
- Added optional temperature/reasoning arguments to `ModelExtractor` and `StructuredModel` for fixed evaluation settings. Defaults omit both parameters exactly as before; production behavior/configuration is unchanged.
- Created `eval/engine.py` to invoke the actual reader/classifier/extraction/validation/explanation/translation components, capture raw synthetic outputs, and compare B1 with B2/full using shared extraction proposals. B2 bypasses validation only inside the offline evaluation module; public API receipts/status integrity remain enforced. Automatic classification, unchanged OCR confirmation, and first-page-only input are explicitly recorded.
- Generated `eval/scoring.py` as an explicitly proposed independent scorer: exact calendar/decimal normalization, conservative copied-text comparison, separate present/missing/ambiguous truth, explicit relative-rule aliases, critical-field false-verification and conditional wrong-among-verified denominators, coverage/abstention/unavailability, per-field counts and repeated-run variance. Provider failures are not credited as correctly flagged or correctly missing. Semantic paraphrases require manual review of the strict-copy metric.
- Created `eval/run.py` for one-command runs with incremental raw synthetic reports, code/config/corpus provenance, explicit diagnostic/resume modes, Markdown tables, and a freeze/single-use heldout gate before any test sample access. It refuses overwriting an experiment; heldout disallows resume/diagnostic/repeats. No actual heldout file was opened.
- Added thirteen initial `tests/test_m4_eval.py` checks for denominators, safe versus unsafe abstention, wrong-context amounts, calendar swaps, missing versus ambiguous truth, input integrity/path safety, heldout-gate refusal/fingerprinting, and fixed generation parameters without changing production defaults.
- One minimal live settings probe accepted the configured evaluation snapshot with temperature 0 and reasoning none (46 input / 13 output tokens). No secret appeared in output. The probe is outside experiment totals; no silent fallback of model/settings occurred.
- Added `tests/test_m4_robustness.py`: eight hostile-body trust-boundary tests and eight unsupported-value rejection tests, provider timeout/rate/malformed bounded retry, and whole-API success/failure log/temp-file checks. These deterministic doubles prove contracts, not live model immunity.
- Reproduced a source-supported hostile amount being Verified in a targeted simulated bad-model probe. Added an explicit strict expected-failure regression for that gap (currently 23 robustness tests pass and one xfails); did not alter production validation or claim adversarial acceptance is complete. This becomes a Part C fix option.
- Added three frontend failure-state tests and `.github/workflows/checks.yml` for Python/Node/adversarial contract/dry-run checks without credentials, paid API calls or heldout access. CI has not been run on GitHub because nothing has been committed/pushed; the known expected failure is printed rather than hidden.
- Added tests while the baseline experiment was running; evaluation/production runtime code and corpus were unchanged. Reports record the source fingerprint at each experiment's start; later test/documentation additions are not pipeline fixes.
- Added a second explicit strict expected-failure regression for the live conflicting-required-dates case. Source matching alone currently accepts one of the conflicting dates. Neither production gap was fixed before Part C selection.
- The first 48/48 adversarial records completed with no observed false-verified critical field. This does not invalidate the simulated source-supported attack regression or prove general prompt-injection immunity. Development data revealed actual wrong Verified hearing dates; the failure analysis will retain them.
- Early scoring audit identified absence phrases (for example `Not specified`) being mislabeled as wrong amounts and contact-name-only outputs requiring annotation clarification. These are measurement issues, not pipeline fixes; saved outputs will be rescored transparently without repeating model calls, retaining the original artifacts and documenting revisions.
- Added ignore rules for future student-supplied heldout inputs while retaining only the requested README/template. Workspace credential scans will exclude heldout entirely, so privacy auditing cannot accidentally inspect test contents during development.
- Completed the original experiments: 120 dev and 48 adversarial notice records across clean/degraded variants and three repetitions. Both original artifacts are retained. No production validator/prompt/classifier/UI fix was applied after observing results.
- Corrected the proposed scorer to v2: explicit numeric-field absence claims are not wrong numeric values when truth is absent; a declared contact-name alias drops only the synthetic testing disclaimer; static all-missing language bundles have vacuous number/glossary agreement. Added four regressions and clarified ambiguity/accuracy denominators. No expected field value/state or model output was changed.
- Updated only annotation aliases/generator scoring metadata, then created `eval/rescore.py` and review artifacts that preserve initial summaries, distinguish inference/scoring provenance and hash unchanged model outputs. No model call was repeated for scoring. Actual inference code/corpus hashes reflect the original experiment; later scoring/test/doc changes are disclosed separately.
- Headline: B1/B2/full each 6/360 dev critical false-verifications and 0/144 adversarial; all six live critical errors are conflicting required dates. Full has three additional clipped-contact false-verifications. Full verified critical usability is 270/276 versus 276/276 B1/B2; no headline improvement is claimed. Repeated headline variance is zero here, not asserted generally.
- Full translation English fallback: dev Spanish 5/120, Tagalog 14/120; adversarial Spanish 0/48, Tagalog 5/48. Actual experiment usage: dev 978 responses with reported usage, 630,821 input/220,266 output tokens; adversarial 409 responses, 254,311 input/89,153 output tokens. Shared proposals counted once. The separate 46/13 settings probe is excluded.
- Added latency p50/p95 and approximate standard-rate model costs from reported tokens and official model pricing checked 2026-10-24. Rates are $0.75/M input, $0.075/M cached input and $4.50/M output; local CPU/hosting and unknown unreported failures are excluded. Metadata distinguishes post-run cost estimation from original generation settings, and a regression checks shared-proposal/cached-token arithmetic.
- Generated FAILURES.md with 353 per-field/stage failure rows, grouped diagnostic causes and five ranked general options. Generated docs/EVIDENCE.md with factual dev/adversarial/ablation/variance/language/usage/cost tables, pending heldout/after-fix sections, limitations and disclosed authorship. Created eval/M4_FILE_GUIDE.md and updated README/DESIGN_NOTES; no contest narrative was written.
- Final Python check: 323 passed, two explicitly expected security failures, one existing asyncio deprecation warning. The extra test checks cost arithmetic and shared proposals. Node 26 rejected a legacy experimental module flag; removed that flag from the proposed CI command and verified the plain Node test command. No product runtime behavior changed.
- Exact saved-table rebuild checks reproduced both review Markdown files byte-for-byte, with matching summaries and unchanged inference-output hashes, without API calls. Fresh model runs may vary; saved-table reproducibility is verified independently of that variance.
- Credential audit: owner-only 0600, current-user-owned, ignored/untracked `.env`; no current-key copies in 368 other scanned workspace files or Git objects (none exist), 26 actual HTTP probes contained no key, private paths returned 404 and APIs were no-store. Heldout directories were excluded without enumeration or file reads. No credential was printed or put into prompts/reports.
- Final Node check: all 14 pass with the standard command. Updated current README/DESIGN_NOTES/EVIDENCE with 323 Python passes, two known expected security failures, exact saved-table reproduction, honest unresolved acceptance, and the Part C review pause. No Part D fix, commit/push, freeze/tag, heldout access or deployment occurred.

## M4 Part D round 1 — 2026-10-24

- User selected fix 1 followed by fix 2. Created a local baseline commit before fixes; the first staging-audit command used the system Python without dotenv, so the audit was rerun immediately with the project virtualenv against every committed file. Verified no key/heldout samples in that commit; nothing was pushed.
- Added general explicit-obligation-date conflict detection in backend/field_validation.py. Different dates under deadline/due/required-hearing/return/payment obligation labels force unverified; ordinary issue/received dates and repeated equivalent dates do not conflict. A one-card result conservatively flags even legitimate multiple obligations instead of selecting one silently.
- Converted the conflicting-date security regression from expected failure to required pass and added seven independent date-label/wrapping/equivalence controls. No sample ID or exact fixture text is used by production rules. Fix 2 has not started; the hostile source-supported amount regression remains expected failure.
