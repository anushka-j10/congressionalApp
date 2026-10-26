# Current design notes — Milestone 5 Step 2

Updated 2026-10-25. This document describes the checked-in implementation. Earlier milestone snapshots are preserved at docs/history/DESIGN_NOTES-before-m5-step2.md. No feature or behavior was changed in this documentation step. The user selected existing original held-out results for reporting; there was no new inference, freeze-tag movement or answer-key change.

## Reading and human review

The browser orients/resizes a single image and the server independently validates bytes, image format, size and orientation in memory. The default preprocessed reader uses OpenCV median filtering, bounded deskew, upscaling and adaptive thresholding before Tesseract. The same local engine also reads the normalized original image; differences in dates/amounts/IDs become review candidates. The primary transcript is preserved. These two treatments are correlated and cannot independently authenticate a number.

The user can compare and edit the transcript, choose a type, confirm the text, and separately attest to printed amounts. The amount gate defaults closed at the API and in unattended evaluation; money-bearing actions also require that attestation. Agreement between readers never sets it. Production classifier SIGNALS currently contains four empty tuples. Unknown-type extraction returns missing and skips the model until a type is explicitly selected. Evaluation's fixture type selection is recorded, not called automatic classification success.

## Fact proposal and deterministic verification

The server sends confirmed text to a configured structured model. Strict nullable schemas distinguish absence from malformed output. The model proposes values and short source snippets; it cannot set verification status. Proposed schema, validators and evaluator were generated under user direction, as recorded in AI_USAGE.md; independent student authorship is not inferred from repository ownership.

The public checked_field entry point always enables every validator. Internal offline switches expose seven named groups only to the evaluation replay:

| Group | Policy | Limit |
|---|---|---|
| source_match | Whitespace/case/Unicode normalization, bounded letter-only fuzzy source lookup; digits must agree | A source match can repeat an OCR error; it does not establish the right field |
| evidence_context | Reject instruction-like/model-output directives and selected wrong-role contexts such as issue dates or future fees | English patterns and bounded lookback can miss new wording |
| readability | Reject unreadable/replacement markers | Cannot detect plausible wrong OCR |
| date_validation | Calendar/weekday parsing, typed source equality, conflicting obligations, supported relative rule/issue-date anchor arithmetic | These subchecks are one ablation group; unsupported formats or multiple legitimate obligations can abstain |
| amount_validation | Decimal parsing, configured range, sign/whole-token/context checks and source equality | Numeric correctness still depends on the text and human photo check |
| text_copy | Whole copied phrase and numeric agreement for text fields | Does not authenticate semantic role |
| action_completeness | Compare copied action to a bounded complete instruction sentence, preserving condition/alternative/timing | English sentence heuristic; no universal completeness guarantee |

The separate human_amount_review gate is the eighth ablation mode. Missing/null handling and strict schema enforcement stay active. An unverified field does not gain a normalized value merely to look usable. Explicit supported relative dates are computed only from a checked rule and printed issue-date anchor. Multiple conflicting obligation dates require abstention; the app currently has one deadline card.

## Explanation, translation and read-aloud

Only verified facts feed explanations. Server receipts bind checked fields and stop the public explanation endpoint accepting a client-forged verified status. English generation checks reject unsupported numbers, retry once and use a deterministic fallback if needed. Spanish/Tagalog use protected facts, number/glossary checks and separate back-translation checks. Failed target checks return labeled English fallback rather than unchecked target text. This is a mechanical guard, not human linguistic review.

Glossary review remains pending in the language data. Read-aloud uses browser speech synthesis and a matching available voice; absence of a matching voice is shown rather than silently reading in another language. Existing desktop/controller checks do not establish phone voice availability or real-device acceptance. External help resource configuration is still TODO.

## Privacy and operational boundary

Normal app request paths keep image/text processing in memory, bound request bytes and multipart spooling, close uploads, use API no-store responses and cache only public shell assets. Only the chosen language is intended for localStorage. Application logs use generated request ID, duration, enum type and fixed error categories. Existing privacy tests exercise success/error paths; they do not prove every host, OS, vendor or future diagnostic path.

The default OCR stays local, but text is sent externally for model extraction/explanation/translation; vision/hybrid also send image content. Model requests specify store=false; that is a request setting, not a guarantee of zero provider retention. Notice content must not be put in client source, environment debug output, wire logs or access/body logs. Synthetic evaluation files are a deliberate opt-in persistence exception and are outside the frontend served directory. API credentials are server environment values and .env is Git-ignored. No claim that Git history and a deployed host have passed the future deployment security audit is made here.

Current endpoints are /api/read, /api/extract and /api/explain, not a single /analyze route. No deployed HTTPS URL, host-environment secret setup, production rate-limit check, deployed origin check, spend-cap confirmation or phone acceptance is complete. Existing sanitized quota error handling is not evidence of an enforceable spend cap. These are Step 4–5 work.

## Evaluation design and measured outcome

Critical fields are deadline, amount_due and required_action; contact is included in per-field/all-field tables. False-verified rate is a wrong verified field divided by every relevant field opportunity, including missing/ambiguous truth. Present accuracy measures correct proposed values among present answers regardless of verification status. Correct verified measures usable correct facts. Abstain-when-present counts missing/unverified output where the key contains a fact. Correct MISSING has its own denominator; zero denominators are N/A. All displayed fractions are exact.

B1 explains/translates the whole OCR notice and treats its returned fields as displayed facts. B2 bypasses validators in offline evaluation and shares the full pipeline's raw extraction proposal for known types; unknown-type abstention is separately bypassed in B2. Full uses production validation and explanation/translation guards. These are different language-output scopes, and shared proposals are not independent model samples or separately additive costs.

The current dev/adversarial live audit contains 20/8 synthetic source documents × two variants × one repetition (40/16 records). Its settings are pinned in each report: gpt-5.4-mini-2026-03-17, temperature 0, reasoning none, evaluation date 2026-10-24, local preprocessed reading, proposed-reliability-v3 scorer. Actual run date is 2026-10-25. One repetition cannot measure repeatability, and clean/degraded versions of a text are correlated.

The original ten-case held-out run was completed once on 2026-10-24 at eval-freeze commit 24d729a540ed3913ced09ee42af89765fd921c4b, using proposed-m4-strict-v2 and the earlier amount-review behavior. Only one original image per case was processed under the harness label clean. The user states the answers were handwritten independently of the app; their recorded expected strings/states remain unchanged. No final-version held-out rerun or retrospective v3 rescoring is reported. Subsequent repairs were informed by those failures, so the original ten cases are no longer independent of final development. Differences between current dev and original held-out results reflect different cases, code, coverage policy and scorer versions; they do not measure a controlled generalization gap or a proven repair gain.

| Version / set | Records | Method | Critical false verified | Present accuracy | Correct verified | Abstain when present |
|---|---|---|---|---|---|---|
| dev | 40 | B1 | 2/120 | 92/92 | 92/92 | 0/92 |
| dev | 40 | B2 | 2/120 | 92/92 | 92/92 | 0/92 |
| dev | 40 | full | 0/120 | 92/92 | 72/92 | 20/92 |
| adversarial | 16 | B1 | 0/48 | 48/48 | 48/48 | 0/48 |
| adversarial | 16 | B2 | 0/48 | 48/48 | 48/48 | 0/48 |
| adversarial | 16 | full | 0/48 | 48/48 | 32/48 | 16/48 |
| heldout_original | 10 | B1 | 17/30 | 11/24 | 11/24 | 0/24 |
| heldout_original | 10 | B2 | 8/30 | 17/24 | 17/24 | 0/24 |
| heldout_original | 10 | full | 4/30 | 18/24 | 14/24 | 6/24 |

The real original held-out numeric error ($75.00 read/verified as $75.60), incomplete timed actions and conservative flags are kept in HELDOUT_RESULTS.md and FAILURES.md. Post-evaluation repairs exist, but there is no independent held-out measurement of those repairs. Zero false-verified values in current unattended dev/attack records partly comes from lower amount coverage; no general safety or fairness claim follows.

| Disabled validator group | Dev critical false verified | Adversarial critical false verified |
|---|---|---|
| full | 0/120 | 0/48 |
| without_action_completeness | 0/120 | 0/48 |
| without_amount_validation | 0/120 | 0/48 |
| without_date_validation | 2/120 | 0/48 |
| without_evidence_context | 0/120 | 0/48 |
| without_readability | 0/120 | 0/48 |
| without_source_match | 0/120 | 0/48 |
| without_text_copy | 0/120 | 0/48 |
| without_human_amount_review | 0/120 | 0/48 |

The replay uses identical captured text/proposals and answer states for each mode, no new model calls, and refuses a change in full-reference value/status/normalization. Targeted tests prove each switch changes its intended failing case while other switches leave it blocked. Unchanged experiment rows do not establish redundancy. Full replay/table/test artifacts are under results/m4-ablations; metrics and language fallbacks are detailed in docs/EVIDENCE.md.

## Limits and release checks

- **Handwriting:** no measured handwriting acceptance result. Printed synthetic documents do not establish handwriting reliability.
- **Poor photos:** dev uses generated clean/degraded variants; no representative real-phone capture or mobile-browser acceptance study. Blur, glare, cropping and tiny text can still produce plausible wrong OCR.
- **Classification:** all four production signal lists in `backend/classifier/signals.py` are empty. Automatic classification returns unknown; the measured pipeline uses explicit fixture type selection. This is not automatic type-classification accuracy.
- **Amounts:** current unattended evaluation withholds unreviewed amounts. All 20 present dev amounts and all 16 present adversarial amounts remain unverified. Human confirmation can still miss an OCR error; matching the text does not authenticate the photo or obligation.
- **Translation:** Spanish and Tagalog glossary files are unreviewed. Number/glossary/back-translation checks are mechanical safeguards, not native-speaker or legal-language approval. A correct translation can repeat a wrong extracted fact.
- **Read-aloud:** browser/device voices determine language availability. Desktop checks do not establish working Spanish/Tagalog voices on a judge's phone. Physical-phone testing remains outstanding.
- **Scope:** one page per request. Extra pages are not merged. English field-role, instruction and action-completeness rules are bounded heuristics; unsupported date formats and multiple obligations can cause abstention or missed distinctions.
- **Help and deployment:** configured external help resources remain TODO in `backend/languages/help.json`; no live HTTPS deployment is verified. Host secrets, request rate limiting, origin policy, deployed quota behavior and real-device acceptance remain later milestone checks.
- **Privacy:** tested normal app paths use in-memory notice processing and no-store API responses; these tests do not prove secure RAM erasure, OS/library behavior, host-log policy or provider retention. Explicit synthetic evaluation reports intentionally persist test data outside the served frontend. Vendored HEIC diagnostics are disclosed in the privacy audit.

The latest clean-checkout implementation check passed 407 Python tests and 17 JavaScript tests. It is documented at results/m4-ablations/REPORT.md, with exact setup and localhost smoke commands. Runtime/provider deployment and actual mobile use require separate acceptance. This Step 2 update consolidates documentation only; AI disclosure review, hosting, deployed checks, accessibility review and submission materials remain later steps, with a stop after each as requested.
