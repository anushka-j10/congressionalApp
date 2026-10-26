# Evaluation evidence — Milestone 5 Step 2

Updated 2026-10-25. The user selected the original cases/results for submission reporting. No new held-out inference, OCR, rescoring or answer-key edit was performed. The final implementation remains without an independent final-version held-out measurement. All numbers here come from saved reports; no new live run was needed for this documentation step.

## Release evidence — October 26

Application commit e25b3c1 is deployed at https://notice-decoder-ns5o.onrender.com. [Release checks](../results/release-2026-10-26/REPORT.md) record 12/12 public HTTP checks with ten matching asset hashes, 430 Python tests, 62 JavaScript tests, and actual browser English/Spanish/Tagalog output on one synthetic development notice before a copy-only selector update. Ten explicit CSS color pairs meet the normal-text contrast threshold; the earlier 63 phone-width layout checks remain scoped desktop evidence. These are deployment/implementation checks, not replacement accuracy measurements.

A separate real-photo diagnostic following AJ's iPhone report found critical OCR losses; full phone acceptance remains open. Deployed failure/fallback/offline and physical audio/installation checks are incomplete. The public release does not erase the original held-out or Northeast failure counts below. No new held-out run, answer-key change or retrospective rescoring was performed. [Release checklist](../RELEASE_CHECKLIST.md).

## Supplemental exploratory evidence — October 26, 2026

A separate [Northeast parking stress run](../results/northeast-stress/REPORT.md) executed 18 researched, assistant-authored notices × two image variants. Its key and image hashes were declared before model calls. This is not independent held-out evidence; sixteen layouts reconstruct official instructions and two use visually inspected official sample ticket stock. Original held-out artifacts were not rerun or changed.

| Measure | Result |
| --- | --- |
| Strict case pass | 10/36 |
| Correct extracted values, present truth | 92/128 |
| Strict false-verified, all four fields | 21/144 |
| Strict false-verified, critical fields | 15/108 |
| Abstain when truth exists | 59/128 |
| Correct and verified, present truth | 50/128 |
| Routing checks (11 links / 7 fallbacks) | 18/18 |
| Regression tests | 430 Python / 60 JavaScript pass |

The strict scorer counts six harmless extra-text/label differences among its 21 false-verifications. Genuine wrong dates/contacts remain; full error review and unchanged raw outputs are linked in the report. Human amount confirmation was not simulated. English consistency checks passed 36/36 but repeated erroneous verified facts. This run did not test Spanish/Tagalog, physical phones, or the deployed HTTP boundary. The earlier dev/adversarial/baseline/ablation and original held-out numbers below retain their original scope.

## Provenance and metric definitions

Critical fields are deadline, amount_due and required_action; contact is included in per-field/all-field tables. False-verified rate is a wrong verified field divided by every relevant field opportunity, including missing/ambiguous truth. Present accuracy measures correct proposed values among present answers regardless of verification status. Correct verified measures usable correct facts. Abstain-when-present counts missing/unverified output where the key contains a fact. Correct MISSING has its own denominator; zero denominators are N/A. All displayed fractions are exact.

B1 explains/translates the whole OCR notice and treats its returned fields as displayed facts. B2 bypasses validators in offline evaluation and shares the full pipeline's raw extraction proposal for known types; unknown-type abstention is separately bypassed in B2. Full uses production validation and explanation/translation guards. These are different language-output scopes, and shared proposals are not independent model samples or separately additive costs.

The current dev/adversarial live audit contains 20/8 synthetic source documents × two variants × one repetition (40/16 records). Its settings are pinned in each report: gpt-5.4-mini-2026-03-17, temperature 0, reasoning none, evaluation date 2026-10-24, local preprocessed reading, proposed-reliability-v3 scorer. Actual run date is 2026-10-25. One repetition cannot measure repeatability, and clean/degraded versions of a text are correlated.

The original ten-case held-out run was completed once on 2026-10-24 at eval-freeze commit 24d729a540ed3913ced09ee42af89765fd921c4b, using proposed-m4-strict-v2 and the earlier amount-review behavior. Only one original image per case was processed under the harness label clean. The user states the answers were handwritten independently of the app; their recorded expected strings/states remain unchanged. No final-version held-out rerun or retrospective v3 rescoring is reported. Subsequent repairs were informed by those failures, so the original ten cases are no longer independent of final development. Differences between current dev and original held-out results reflect different cases, code, coverage policy and scorer versions; they do not measure a controlled generalization gap or a proven repair gain.

## Baselines and full pipeline

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

B1/B2/full have zero unavailable methods in these reports. Original all-field full false verification is 5/40; current dev is 0/160 and adversarial is 0/64. Correct values can still be unverified; safety and coverage must be read together.

## Per-field scores

| Version / set | Method | Field | Present accuracy | Correct verified | False verified | Abstain when present | Correct MISSING |
|---|---|---|---|---|---|---|---|
| dev | B1 | deadline | 34/34 | 34/34 | 2/40 | 0/34 | 4/4 |
| dev | B1 | amount_due | 20/20 | 20/20 | 0/40 | 0/20 | 20/20 |
| dev | B1 | required_action | 38/38 | 38/38 | 0/40 | 0/38 | 2/2 |
| dev | B1 | contact | 36/38 | 36/38 | 2/40 | 0/38 | 2/2 |
| dev | B2 | deadline | 34/34 | 34/34 | 2/40 | 0/34 | 4/4 |
| dev | B2 | amount_due | 20/20 | 20/20 | 0/40 | 0/20 | 20/20 |
| dev | B2 | required_action | 38/38 | 38/38 | 0/40 | 0/38 | 2/2 |
| dev | B2 | contact | 36/38 | 36/38 | 0/40 | 2/38 | 2/2 |
| dev | full | deadline | 34/34 | 34/34 | 0/40 | 0/34 | 4/4 |
| dev | full | amount_due | 20/20 | 0/20 | 0/40 | 20/20 | 20/20 |
| dev | full | required_action | 38/38 | 38/38 | 0/40 | 0/38 | 2/2 |
| dev | full | contact | 36/38 | 35/38 | 0/40 | 3/38 | 2/2 |
| adversarial | B1 | deadline | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B1 | amount_due | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B1 | required_action | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B1 | contact | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B2 | deadline | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B2 | amount_due | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B2 | required_action | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | B2 | contact | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | full | deadline | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | full | amount_due | 16/16 | 0/16 | 0/16 | 16/16 | N/A |
| adversarial | full | required_action | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| adversarial | full | contact | 16/16 | 16/16 | 0/16 | 0/16 | N/A |
| heldout_original | B1 | deadline | 4/7 | 4/7 | 6/10 | 0/7 | 0/2 |
| heldout_original | B1 | amount_due | 6/7 | 6/7 | 2/10 | 0/7 | 2/3 |
| heldout_original | B1 | required_action | 1/10 | 1/10 | 9/10 | 0/10 | N/A |
| heldout_original | B1 | contact | 7/10 | 7/10 | 3/10 | 0/10 | N/A |
| heldout_original | B2 | deadline | 4/7 | 4/7 | 4/10 | 0/7 | 2/2 |
| heldout_original | B2 | amount_due | 6/7 | 6/7 | 1/10 | 0/7 | 3/3 |
| heldout_original | B2 | required_action | 7/10 | 7/10 | 3/10 | 0/10 | N/A |
| heldout_original | B2 | contact | 9/10 | 9/10 | 1/10 | 0/10 | N/A |
| heldout_original | full | deadline | 5/7 | 3/7 | 0/10 | 4/7 | 2/2 |
| heldout_original | full | amount_due | 6/7 | 4/7 | 1/10 | 2/7 | 3/3 |
| heldout_original | full | required_action | 7/10 | 7/10 | 3/10 | 0/10 | N/A |
| heldout_original | full | contact | 9/10 | 9/10 | 1/10 | 0/10 | N/A |

## Validator-group ablation

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

The ablation uses current checks with saved dev/adversarial proposals and refuses full-reference value/status/normalization drift. All reference records matched. No model/OCR calls are made. Schema checks, unknown-type abstention, null handling and later explanation guards are not disabled. Date parsing, equality, conflicting obligations and relative anchors are one named date-validation group; individual subchecks are not separately ablated.

Human amount-review removal raises current correct-verified critical coverage from 72/92 to 92/92 (dev) and 32/48 to 48/48 (adversarial). This is a counterfactual gate removal, not evidence of a person's review or corrected OCR. Source/money/context checks can overlap; an unchanged row is not proof of redundancy. Exact per-field and abstention tables, raw scores and the 16 new regression controls are linked in results/m4-ablations/REPORT.md.

## Translation outcomes

The following are recorded full-pipeline mechanical-check outcomes. They are not human translation ratings. Number/glossary passes can be vacuous on all-missing notices. Each cell counts requested outputs, not independent users/documents.

| Version / set | Spanish outputs accepted / requested | Spanish English fallback | Tagalog outputs accepted / requested | Tagalog English fallback |
|---|---|---|---|---|
| Current dev | 38/40 | 2/40 | 31/40 | 9/40 |
| Current adversarial | 16/16 | 0/16 | 16/16 | 0/16 |
| Original held-out | 7/10 | 3/10 | 7/10 | 3/10 |

Source tables: results/m4-verification/dev.md, results/m4-verification/adversarial.md and results/heldout-final.md. Glossaries remain unreviewed; a checked translation can faithfully repeat an extraction error.

## Verification evidence

| Claim | Evidence | Boundary |
|---|---|---|
| 407 Python tests pass | results/m4-ablations/clean-pytest.txt | Clean implementation checkout 81661e4; one dependency deprecation warning |
| 17 JavaScript tests pass | results/m4-ablations/clean-node.txt | Node/controller tests, not physical-phone acceptance |
| Fresh pinned install and app startup | results/m4-verification/install-arm.txt and commands.md | Fresh ARM Python 3.12.14 install; stopped Intel build not counted as success |
| Refactored clean app smoke passes | results/m4-ablations/app-smoke.txt | HTTP shell/read/extract/explain success, no-store, no new notice files; unknown-type/static output |
| Missing source remains unverified | tests/test_m4_audit.py::test_absent_source_snippet_can_never_verify | Five field types; generated synthetic cases |
| No deadline is invented in tested absent cases | tests/test_m4_audit.py | Includes issue-date-as-deadline rejection; not a universal semantic guarantee |
| Extra explanation number rejected | tests/test_explanation.py::test_bad_english_number_regenerates_once_then_template_fallback | Injected $999.00 rejected and excluded from returned template |
| Bad translation falls back to English | tests/test_explanation.py::test_bad_translation_number_falls_back_to_english | Synthetic mocked failure controls for es/tl |
| Application privacy paths tested | results/m4-verification/targeted-tests.txt and privacy-grep.txt; results/m4-ablations/privacy-grep.txt | 25 targeted cases; tested logs lack sentinel/filename; vendor/host/provider limits disclosed |
| Individual switches are isolated and unavailable to requests | tests/test_ablations.py | Seven validator groups and separate human gate; 16 tests including replay/refusal controls |

## Known limits

- **Handwriting:** no measured handwriting acceptance result. Printed synthetic documents do not establish handwriting reliability.
- **Poor photos:** dev uses generated clean/degraded variants; no representative real-phone capture or mobile-browser acceptance study. Blur, glare, cropping and tiny text can still produce plausible wrong OCR.
- **Classification:** all four production signal lists in `backend/classifier/signals.py` are empty. Automatic classification returns unknown; the measured pipeline uses explicit fixture type selection. This is not automatic type-classification accuracy.
- **Amounts:** current unattended evaluation withholds unreviewed amounts. All 20 present dev amounts and all 16 present adversarial amounts remain unverified. Human confirmation can still miss an OCR error; matching the text does not authenticate the photo or obligation.
- **Translation:** Spanish and Tagalog glossary files are unreviewed. Number/glossary/back-translation checks are mechanical safeguards, not native-speaker or legal-language approval. A correct translation can repeat a wrong extracted fact.
- **Read-aloud:** browser/device voices determine language availability. Desktop checks do not establish working Spanish/Tagalog voices on a judge's phone. Physical-phone testing remains outstanding.
- **Scope:** one page per request. Extra pages are not merged. English field-role, instruction and action-completeness rules are bounded heuristics; unsupported date formats and multiple obligations can cause abstention or missed distinctions.
- **Help and deployment:** local support-service configuration remains empty in `backend/languages/help.json`. Selected official parking routes are available separately. The October 26 HTTPS release passes 12 public checks and one synthetic language workflow; full phone acceptance and deployed fallback/offline checks remain incomplete. See `results/release-2026-10-26/REPORT.md`. Rate limits are process-local and not a dollar spend cap.
- **Privacy:** tested normal app paths use in-memory notice processing and no-store API responses; these tests do not prove secure RAM erasure, OS/library behavior, host-log policy or provider retention. Explicit synthetic evaluation reports intentionally persist test data outside the served frontend. Vendored HEIC diagnostics are disclosed in the privacy audit.

## Authoritative artifacts

- Current live records: [dev](../results/m4-verification/dev.json), [adversarial](../results/m4-verification/adversarial.json); matching .md files retain original printed outputs/settings.
- Current replay: [dev ablations](../results/m4-ablations/dev.json), [adversarial ablations](../results/m4-ablations/adversarial.json), [protocol and commands](../results/m4-ablations/REPORT.md).
- Original frozen run: [raw results](../results/heldout-final.json), [protocol](../results/heldout-protocol.json), [complete Step 1 results](../HELDOUT_RESULTS.md). Raw hashes were verified at Step 1 against the recorded protocol.
- Historical notes and superseded status statements are retained in docs/history. No new freeze tag, independent final held-out score, native review or full mobile acceptance is claimed. The later deployed release is documented separately below.


## 2026-10-26 phone OCR safety repair

New timing-corruption checks withhold deadline, amount and action when a numeric date is incomplete/invalid or a time limit contains confused letters. No automatic digit correction or OCR-engine switch. Targeted controls: 6 unsafe actions previously verified, now 0; 2 legible controls preserved. Fresh dev run: 0/120 critical false verifications; all-field present accuracy 128/130, verified-correct coverage 107/130, abstention 23/130. Adversarial: 0/48 critical false verifications. Python 452 passed; JavaScript 62 passed. These are development results; the original held-out evidence is unchanged. Full limits, failure outputs, baseline/ablation tables and commands: [phone OCR repair report](../results/phone-reading-fix/REPORT.md).
