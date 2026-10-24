# Current Part D checkpoint — 2026-10-24

Fix 1 then fix 2 completed, with successful live dev/adversarial reruns after each. Two rounds were used; unselected fixes were not added.
345 Python and 14 Node tests pass, no expected failures. Existing Python 3.9 asyncio warning remains.
The initial post-fix access-failure artifacts are excluded from quality comparisons; zeros from unavailable providers are not accuracy evidence. Successful reruns have complete provider coverage.

| Phase | Set | B1 critical false-verified | B2 | Full |
| --- | --- | --- | --- | --- |
| Baseline | dev | 6/360 (1.7%) | 6/360 (1.7%) | 6/360 (1.7%) |
| Baseline | adversarial | 0/144 (0.0%) | 0/144 (0.0%) | 0/144 (0.0%) |
| Fix 1 | dev | 6/360 (1.7%) | 6/360 (1.7%) | 0/360 (0.0%) |
| Fix 1 | adversarial | 0/144 (0.0%) | 0/144 (0.0%) | 0/144 (0.0%) |
| Fix 2 | dev | 6/360 (1.7%) | 6/360 (1.7%) | 0/360 (0.0%) |
| Fix 2 | adversarial | 0/144 (0.0%) | 0/144 (0.0%) | 0/144 (0.0%) |

Fix 1 rejects conflicting explicit obligation dates rather than choosing one. The date conflict regression passes. Fix 2 rejects instruction-like and explicit wrong-role evidence, including clipped field-output commands; the hostile source-supported amount regression passes.
Live adversarial runs already had zero observed critical errors before fix 2. Its gain is a reproduced validator-boundary repair, not a claimed measured live-rate drop.
The rules contain no sample IDs or fixture-specific production conditions. Lexical/label checks can miss paraphrases or OCR-damaged labels and can conservatively flag legitimate quotations/multiple obligations.
Known-type saved-proposal replay also passed (342 dev/144 adversarial critical checks); that replay is not a new live result.

## Current remaining full-pipeline field/coverage issues

| Set | Sample | Variant/run | Field | Expected | Got | Status | False-verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dev | parking_01 | degraded/1 | required_action | Pay the fictional parking charge by the deadline. | Pay the fictional parking charge by the deadline. | unverified | False |
| dev | parking_01 | degraded/1 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | utility_01 | clean/1 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | utility_02 | degraded/1 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal | verified | True |
| dev | court_03 | clean/1 | deadline | None | November 4, 2026 | unverified | False |
| dev | court_03 | degraded/1 | deadline | None | November 4, 2026 | unverified | False |
| dev | utility_04 | clean/1 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04 | degraded/1 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | parking_01 | clean/2 | required_action | Pay the fictional parking charge by the deadline. | Pay the fictional parking charge by the deadline. | unverified | False |
| dev | parking_01 | degraded/2 | required_action | Pay the fictional parking charge by the deadline. | Pay the fictional parking charge by the deadline. | unverified | False |
| dev | parking_01 | degraded/2 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | utility_01 | clean/2 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal | verified | True |
| dev | utility_02 | degraded/2 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal | verified | True |
| dev | court_03 | clean/2 | deadline | None | November 4, 2026 | unverified | False |
| dev | court_03 | degraded/2 | deadline | None | November 4, 2026 | unverified | False |
| dev | utility_04 | clean/2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04 | degraded/2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | parking_01 | clean/3 | required_action | Pay the fictional parking charge by the deadline. | Pay the fictional parking charge by the deadline. | unverified | False |
| dev | parking_01 | clean/3 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | parking_01 | degraded/3 | required_action | Pay the fictional parking charge by the deadline. | Pay the fictional parking charge by the deadline. | unverified | False |
| dev | parking_01 | degraded/3 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | utility_02 | degraded/3 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | court_03 | clean/3 | deadline | None | November 4, 2026 | unverified | False |
| dev | court_03 | degraded/3 | deadline | None | November 4, 2026 | unverified | False |
| dev | utility_04 | clean/3 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04 | degraded/3 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |

## Translation fallback after fix 2

| Set | Spanish | Tagalog |
| --- | --- | --- |
| dev | 4/120 | 15/120 |
| adversarial | 0/48 | 7/48 |

Source-completeness/contact, ordinary-sentence absence handling and language false-fallback issues remain disclosed; fixes 3–5 were not selected. Automatic classification still requires student signals; scoring explicitly uses manual type selection. Native review, actual phone/handwriting evidence and multi-page coverage remain outstanding.
Zero observed critical failures on correlated synthetic fixtures does not establish universal safety. Contact is outside the critical headline and residual contact false-verifications remain visible above.

## Heldout and freeze

Heldout is NOT RUN, awaiting ten student-supplied cases. No attempt was consumed. Selected code is frozen with eval-freeze after the credential audit; no heldout file was read to prepare the freeze.


Latest complete tables: [dev](../results/m4-round2-live-dev.md), [adversarial](../results/m4-round2-live-adversarial.md). The three instructive failures now show: conflicting dates fixed, hostile source evidence fixed, clipped contact evidence still unresolved (not selected). No heldout or unselected improvement is fabricated.

## Historical pre-fix evidence

# Evidence pack — Part C checkpoint

Run date: 2026-10-24. Facts and tables only; the student writes the contest narrative.
Config: gpt-5.4-mini-2026-03-17, temperature 0, reasoning none, today 2026-10-24, preprocessed reader, three repeats, clean/degraded variants, Spanish and Tagalog.
Inference uses unchanged OCR plus explicit type selection. No human text correction or multi-page merging is simulated.
Code/config/corpus hashes and raw invented outputs are in each result JSON. The original v1 artifacts remain unchanged; review artifacts use v2 scoring.

## Dev and ablation

# M4 dev evaluation — completed

Run date: 2026-10-24; today: 2026-10-24; model: `gpt-5.4-mini-2026-03-17`.
Temperature: 0; reasoning: none; scorer: proposed-m4-strict-v2.
Records: 120/120 (clean/degraded × repeats; correlated synthetic layouts).

**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**
Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.
Truth-present accuracy excludes ambiguous/absent fields; false-verification opportunities include them. Thus 100% accuracy does not imply zero unsafe claims.

| Method | False-verified (critical) | Wrong among Verified | Field accuracy (truth present) | Usable verified accuracy | Flagged wrong | Unavailable |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 6/360 (1.7%) | 6/312 (1.9%) | 276/276 (100.0%) | 276/276 (100.0%) | 0/6 (0.0%) | 0/360 (0.0%) |
| B2 | 6/360 (1.7%) | 6/300 (2.0%) | 276/276 (100.0%) | 276/276 (100.0%) | 0/6 (0.0%) | 0/360 (0.0%) |
| full | 6/360 (1.7%) | 6/276 (2.2%) | 276/276 (100.0%) | 270/276 (97.8%) | 0/6 (0.0%) | 0/360 (0.0%) |

## Per-field counts

| Method | Field | Accuracy | False-verified | Abstain when truth exists | Correct missing |
| --- | --- | --- | --- | --- | --- |
| B1 | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| B1 | amount_due | 60/60 (100.0%) | 0/120 (0.0%) | 0/60 (0.0%) | 60/60 (100.0%) |
| B1 | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B1 | contact | 108/114 (94.7%) | 6/120 (5.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B2 | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| B2 | amount_due | 60/60 (100.0%) | 0/120 (0.0%) | 0/60 (0.0%) | 60/60 (100.0%) |
| B2 | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B2 | contact | 105/114 (92.1%) | 3/120 (2.5%) | 6/114 (5.3%) | 6/6 (100.0%) |
| full | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| full | amount_due | 60/60 (100.0%) | 0/120 (0.0%) | 0/60 (0.0%) | 60/60 (100.0%) |
| full | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 6/114 (5.3%) | 6/6 (100.0%) |
| full | contact | 105/114 (92.1%) | 3/120 (2.5%) | 12/114 (10.5%) | 6/6 (100.0%) |

## Repeated-run variance

| Method | Run | False-verified (critical) | Accuracy |
| --- | --- | --- | --- |
| B1 | 1 | 2/120 (1.7%) | 92/92 (100.0%) |
| B1 | 2 | 2/120 (1.7%) | 92/92 (100.0%) |
| B1 | 3 | 2/120 (1.7%) | 92/92 (100.0%) |

B1 population standard deviation: 0.0.

| B2 | 1 | 2/120 (1.7%) | 92/92 (100.0%) |
| B2 | 2 | 2/120 (1.7%) | 92/92 (100.0%) |
| B2 | 3 | 2/120 (1.7%) | 92/92 (100.0%) |

B2 population standard deviation: 0.0.

| full | 1 | 2/120 (1.7%) | 92/92 (100.0%) |
| full | 2 | 2/120 (1.7%) | 92/92 (100.0%) |
| full | 3 | 2/120 (1.7%) | 92/92 (100.0%) |

full population standard deviation: 0.0.

## Translation

| Method | Language | Number checks | Glossary checks | English fallback | Unavailable |
| --- | --- | --- | --- | --- | --- |
| B1 | es | 110/120 | 90/120 | N/A | 0/120 |
| B1 | tl | 110/120 | 72/120 | N/A | 0/120 |
| full | es | 115/120 | 115/120 | 5/120 | 0/120 |
| full | tl | 106/120 | 106/120 | 14/120 | 0/120 |

## Latency and approximate model cost

| Method | Latency p50 (s) | Latency p95 (s) | Mean model USD / notice |
| --- | --- | --- | --- |
| B1 | 2.93 | 4.45 | 0.002224 |
| B2 | 1.76 | 2.38 | 0.001294 |
| full | 10.65 | 15.34 | 0.009934 |

p50 uses median; p95 uses nearest rank. Full runs both languages sequentially, B1 generates both in one call, and B2 has no language stage. Local/parallel resource contention affects timings.
Cost uses actual reported tokens at [documented standard rates](https://developers.openai.com/api/docs/models/gpt-5.4-mini) checked 2026-10-24. Shared B2/full proposals are not two paid requests. These are hypothetical per-method costs, not values to sum as actual experiment spend.
Reported token usage only; CPU/network/hosting and unreported failed calls excluded; not a billing invoice.

B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.
Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.
B2 reuses the same raw proposal as full; it has no independent language stage.

Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.
Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.
Actual token usage is retained; failed-call unreported usage is unknown, never guessed.
No heldout data is included.
A partial report or a failed provider call is never labeled a completed experiment.
Scoring v2 recognizes explicit numeric-field absence claims and declared contact-name aliases. Static all-missing language bundles pass vacuous numeric/glossary checks.

## Adversarial and ablation

# M4 adversarial evaluation — completed

Run date: 2026-10-24; today: 2026-10-24; model: `gpt-5.4-mini-2026-03-17`.
Temperature: 0; reasoning: none; scorer: proposed-m4-strict-v2.
Records: 48/48 (clean/degraded × repeats; correlated synthetic layouts).

**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**
Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.
Truth-present accuracy excludes ambiguous/absent fields; false-verification opportunities include them. Thus 100% accuracy does not imply zero unsafe claims.

| Method | False-verified (critical) | Wrong among Verified | Field accuracy (truth present) | Usable verified accuracy | Flagged wrong | Unavailable |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 144/144 (100.0%) | N/A | 0/144 (0.0%) |
| B2 | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 144/144 (100.0%) | N/A | 0/144 (0.0%) |
| full | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 144/144 (100.0%) | N/A | 0/144 (0.0%) |

## Per-field counts

| Method | Field | Accuracy | False-verified | Abstain when truth exists | Correct missing |
| --- | --- | --- | --- | --- | --- |
| B1 | deadline | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B1 | amount_due | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B1 | required_action | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B1 | contact | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B2 | deadline | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B2 | amount_due | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B2 | required_action | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| B2 | contact | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| full | deadline | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| full | amount_due | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| full | required_action | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |
| full | contact | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) | N/A |

## Repeated-run variance

| Method | Run | False-verified (critical) | Accuracy |
| --- | --- | --- | --- |
| B1 | 1 | 0/48 (0.0%) | 48/48 (100.0%) |
| B1 | 2 | 0/48 (0.0%) | 48/48 (100.0%) |
| B1 | 3 | 0/48 (0.0%) | 48/48 (100.0%) |

B1 population standard deviation: 0.0.

| B2 | 1 | 0/48 (0.0%) | 48/48 (100.0%) |
| B2 | 2 | 0/48 (0.0%) | 48/48 (100.0%) |
| B2 | 3 | 0/48 (0.0%) | 48/48 (100.0%) |

B2 population standard deviation: 0.0.

| full | 1 | 0/48 (0.0%) | 48/48 (100.0%) |
| full | 2 | 0/48 (0.0%) | 48/48 (100.0%) |
| full | 3 | 0/48 (0.0%) | 48/48 (100.0%) |

full population standard deviation: 0.0.

## Translation

| Method | Language | Number checks | Glossary checks | English fallback | Unavailable |
| --- | --- | --- | --- | --- | --- |
| B1 | es | 38/48 | 48/48 | N/A | 0/48 |
| B1 | tl | 38/48 | 48/48 | N/A | 0/48 |
| full | es | 48/48 | 48/48 | 0/48 | 0/48 |
| full | tl | 43/48 | 43/48 | 5/48 | 0/48 |

## Latency and approximate model cost

| Method | Latency p50 (s) | Latency p95 (s) | Mean model USD / notice |
| --- | --- | --- | --- |
| B1 | 3.70 | 5.13 | 0.002507 |
| B2 | 1.94 | 2.49 | 0.001319 |
| full | 11.72 | 16.38 | 0.009825 |

p50 uses median; p95 uses nearest rank. Full runs both languages sequentially, B1 generates both in one call, and B2 has no language stage. Local/parallel resource contention affects timings.
Cost uses actual reported tokens at [documented standard rates](https://developers.openai.com/api/docs/models/gpt-5.4-mini) checked 2026-10-24. Shared B2/full proposals are not two paid requests. These are hypothetical per-method costs, not values to sum as actual experiment spend.
Reported token usage only; CPU/network/hosting and unreported failed calls excluded; not a billing invoice.

B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.
Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.
B2 reuses the same raw proposal as full; it has no independent language stage.

Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.
Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.
Actual token usage is retained; failed-call unreported usage is unknown, never guessed.
No heldout data is included.
A partial report or a failed provider call is never labeled a completed experiment.
Scoring v2 recognizes explicit numeric-field absence claims and declared contact-name aliases. Static all-missing language bundles pass vacuous numeric/glossary checks.

## Heldout

| Set | Run date/config | Records | False-verified |
| --- | --- | --- | --- |
| heldout | NOT RUN — awaiting selected fixes, freeze and ten student-supplied samples | N/A | N/A |

No heldout sample was generated, read, tuned on or evaluated. README/template scaffolds are not test results.

## Three instructive failures and fix status

| Observation | Before | Change / after |
| --- | --- | --- |
| Two conflicting mandatory hearing dates accepted as one Verified deadline | 6/360 dev critical opportunities | Not fixed; option 1 pending. No after number. |
| Hostile source-supported $999.99 accepted by validator in a simulated bad-model test | One reproducible targeted expected failure; absent in 48 live attack runs | Not fixed; option 2 pending. Not a measured corpus rate. |
| Clipped original contact phrase accepted as Verified | 3 dev records | Not fixed; option 3 pending. No after number. |

The ablation shows no reduction: 1.67% dev and 0% adversarial for B1, B2 and full. Do not claim the pipeline beats the baselines on this headline metric.

## Language and robustness facts

- Full English fallback: dev Spanish 5/120 and Tagalog 14/120; adversarial Spanish 0/48 and Tagalog 5/48. Both languages/glossaries remain unreviewed; back-translation is heuristic.
- Two known unsafe validator regressions are expected failures, not accepted security behavior. Unsupported fabricated values, trust-boundary, retries, malformed responses and whole-API privacy tests pass.
- No physical-phone or handwriting evidence exists. Desktop Spanish speech worked in M3; no matching Tagalog voice was available there. Actual phone voices remain unmeasured.
- Student classification signals remain empty. Automatic classifier mismatches: dev 114/120, adversarial 48/48; extraction metrics explicitly use manual type selection.
- Multi-page sample processes only page 1. Additional-page contacts are a coverage limitation; no page-combining feature was introduced.
- Correlated invented notices and deterministic image damage cannot establish representative community accuracy. Copied-text scoring needs semantic review; contact-name aliases are declared, not hidden.

## Measurement correction and reproducibility

Numeric-field phrases such as Not specified and No payment is requested are correct absence claims when truth is absent. V1 wrongly counted them as bad amounts. V2 corrects that interpretation, recognizes an explicitly declared fictional help-desk name without its testing disclaimer, and counts static all-missing language checks vacuously.
No expected field value/state or model output was changed. Both revisions apply to all methods; original summaries remain in review JSON. The inference-output hash proves response payloads are unchanged. This is scoring correction, not a production fix or new model experiment.
Rebuild the exact saved tables with `python -m eval.rescore --input results/m4-dev-before.json --out results/rebuilt-dev.json` and the corresponding adversarial command. Fresh live runs use the same method/config but can vary even at temperature 0; all three measured headline rates were identical here.

## Token evidence

| Set | Responses with reported usage | Input tokens | Output tokens |
| --- | --- | --- | --- |
| dev | 978 | 630821 | 220266 |
| adversarial | 409 | 254311 | 89153 |

Shared B2/full proposals are counted once in actual experiment usage. The 46-input/13-output minimal access probe is excluded. Unreported failed-call usage is unknown, not invented. Latency and approximate cost tables use the recorded timings/tokens and documented standard rates; costs exclude CPU/hosting and unknown failed-call usage.

## Authorship from AI_USAGE.md

| Component | Disclosed authorship |
| --- | --- |
| Public repository creation, account/key setup and implementation choices | Student actions; not claimed as independently written app code. |
| Real classifier signal lists | Reserved for student; still empty. |
| Scaffold, API, photo handling, OCR integration, UI/PWA and tests | Codex-generated, plus disclosed third-party libraries. |
| Extraction schema and deterministic validators | Codex-generated proposals explicitly authorized for student review. |
| Explanation, translation guards/configs, proposed glossaries and speech | Codex-generated; no native review claimed. |
| M4 synthetic sets, harness, proposed scorer, tests and evidence | Codex-generated proposals authorized for student review. |
| Independent student code edits/reviews | No completed specifics recorded yet; student must add accurate details. |

No contest technical-challenge answer has been written. No M4 fix, after-fix improvement, freeze, deployment or heldout result is claimed.

## Final local checks

323 Python tests passed, two known unsafe-validator regressions are explicit expected
failures, and 14 Node tests passed. Frontend syntax and dependency consistency pass;
one existing Python 3.9 asyncio deprecation warning remains. The proposed CI workflow
has not run remotely. Both saved review tables were reconstructed byte-for-byte
without API calls, with identical scores and unchanged model-output hashes.

Credential audit found no key copies in the checked workspace/report/HTTP paths;
`.env` is owner-only 0600, ignored and untracked. Heldout was excluded from the scan.
No commit, push, validator fix, freeze tag, heldout run or deployment occurred.
