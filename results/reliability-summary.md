# Reliability repairs and automated checks

Student-authorized repair cycle after the original held-out run. Application/scoring changes are disclosed proposals for review, not independently written student code. Original eval-freeze and all original held-out report/ledger hashes remain unchanged; no held-out sample was replayed or rescored. Fresh final generalization measurement requires a new independent set and a separate versioned benchmark procedure.

## Implemented behavior

- Two local OCR image treatments expose actual date/amount/ID candidates and disagreements. The selected preprocessed transcript is preserved; no automatic digit correction, vision call or agreement-as-verification is introduced. Both passes use Tesseract, so their errors can be correlated.
- A separate printed-amount confirmation defaults false at the API and unchecked in the browser. Editing text, changing type or clearing resets it. Unattended extraction cannot mark amounts or money-bearing actions Verified; explicit human review allows normal source checks but cannot prove the human actually noticed every wrong digit.
- Required actions must retain the surrounding instruction sentence, including wrapped timing clauses, conditions and alternatives. The model is asked for complete copied instructions, and a bounded English sentence check rejects clipping independently of the model. No missing text is auto-filled. Courtesy/modality prefixes can differ; contact completeness and unrestricted linguistic interpretation remain limitations.
- Date/amount source validation now tolerates complete typed date, money, time and room tokens in the same sentence, accepts terminal date punctuation, and validates supported weekday names against the calendar. Invalid, competing or unrelated numeric evidence still fails. Current payment instructions that mention avoiding a future late fee are distinguished from the fee itself.
- Scorer v3 independently normalizes supported weekday/time date notation and explicit non-numeric absence explanations. Strict action matching and limited equivalence are reported side by side; the latter only tolerates introductory Please/You must, never omitted timing/conditions/alternatives or free paraphrases. Old v2 results remain untouched.

## Automated validation

383 Python tests pass, including 38 new repair cases and the existing injection, malformed-output, upload, retry, receipt and whole-API privacy checks. 17 JavaScript tests pass, including the separate confirmation gate and stale-result/reset controls. Dependency consistency, JavaScript syntax, dev/adversarial input preflights and whitespace checks pass. One existing Python 3.9 asyncio deprecation warning remains; no new expected failures.

A newly rendered synthetic image passed real local OCR -> API extraction with a deterministic model stub: without amount review it is unverified, with explicit review the supported correct amount is Verified. This is a local integration test, not a live model accuracy measurement. Seven additional new synthetic controls compare the original frozen validator to the repair: three valid mixed-context fields change unverified -> Verified; three clipped actions change Verified -> unverified; the hostile-amount control stays unverified. See results/reliability-controls.json.

A real browser smoke check loaded only a synthetic development image. The new amount checkbox was initially unchecked despite matching local readings; text confirmation alone kept extraction disabled, both confirmations enabled it. The test notice was cleared afterward. A screenshot is saved in results/reliability-preview.png. No language preference was changed or native-review claim made.

## Complete live development and adversarial measurements

Recorded run dates: dev 2026-10-24, adversarial 2026-10-24. Evaluation today remains pinned to 2026-10-24.

Both sets use the unchanged development/adversarial images and expected labels, clean/degraded variants, three repetitions, explicit fixture type selection and unchanged OCR confirmation. Model gpt-5.4-mini-2026-03-17, temperature 0, reasoning none, today 2026-10-24; scorer proposed-reliability-v3. Every method and language output was available. These sets are development evidence, not a new held-out test.

**Human amount review is not simulated. Lower false-verification must be read together with lost Verified coverage; these results do not establish better OCR accuracy or real-world safety.**

| Set | Mode | Critical strict false-verified | Limited-equivalence false-verified | Correct present | Correct and Verified |
| --- | --- | --- | --- | --- | --- |
| dev | B1 | 6/360 (1.7%) | 6/360 (1.7%) | 276/276 (100.0%) | 276/276 (100.0%) |
| dev | B2 | 2/360 (0.6%) | 2/360 (0.6%) | 276/276 (100.0%) | 276/276 (100.0%) |
| dev | full | 0/360 (0.0%) | 0/360 (0.0%) | 276/276 (100.0%) | 216/276 (78.3%) |
| adversarial | B1 | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 144/144 (100.0%) |
| adversarial | B2 | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 144/144 (100.0%) |
| adversarial | full | 0/144 (0.0%) | 0/144 (0.0%) | 144/144 (100.0%) | 96/144 (66.7%) |

No direct apples-to-apples rate improvement is claimed over old v2 experiments: the scorer version, model instruction and amount-review policy changed. In particular, all present amounts require human review before they can be Verified; they are deliberately withheld in these unattended runs. The prior held-out 4/30 remains the original v2 result, not a result of this repair.

## Full-pipeline field coverage

| Set | Field | Correct present | Correct and Verified | Abstain with truth present | Strict false-verified |
| --- | --- | --- | --- | --- | --- |
| dev | deadline | 102/102 (100.0%) | 102/102 (100.0%) | 0/102 (0.0%) | 0/120 (0.0%) |
| dev | amount_due | 60/60 (100.0%) | 0/60 (0.0%) | 60/60 (100.0%) | 0/120 (0.0%) |
| dev | required_action | 114/114 (100.0%) | 114/114 (100.0%) | 0/114 (0.0%) | 0/120 (0.0%) |
| dev | contact | 108/114 (94.7%) | 105/114 (92.1%) | 9/114 (7.9%) | 0/120 (0.0%) |
| adversarial | deadline | 48/48 (100.0%) | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) |
| adversarial | amount_due | 48/48 (100.0%) | 0/48 (0.0%) | 48/48 (100.0%) | 0/48 (0.0%) |
| adversarial | required_action | 48/48 (100.0%) | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) |
| adversarial | contact | 48/48 (100.0%) | 48/48 (100.0%) | 0/48 (0.0%) | 0/48 (0.0%) |

## Remaining full-pipeline mismatches and conservative flags

| Set | Sample / variant / repetition | Field | Expected | Got | Status | Strict false-verified |
| --- | --- | --- | --- | --- | --- | --- |
| dev | parking_01/clean/1 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_01/degraded/1 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_02/clean/1 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | parking_02/degraded/1 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | utility_01/clean/1 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_01/degraded/1 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_02/clean/1 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/1 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/1 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | parking_03/clean/1 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_03/degraded/1 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_04/clean/1 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | parking_04/degraded/1 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | court_03/degraded/1 | deadline | None | November 4, 2026 | unverified | False |
| dev | utility_03/clean/1 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_03/degraded/1 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_04/clean/1 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/clean/1 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04/degraded/1 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/degraded/1 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_05/clean/1 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | utility_05/degraded/1 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | school_04/clean/1 | amount_due | 12.00 | $12.00 | unverified | False |
| dev | school_04/degraded/1 | amount_due | 12.00 | $12.00 | unverified | False |
| dev | parking_01/clean/2 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_01/degraded/2 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_02/clean/2 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | parking_02/degraded/2 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | utility_01/clean/2 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_01/degraded/2 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_02/clean/2 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/2 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/2 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | parking_03/clean/2 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_03/degraded/2 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_04/clean/2 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | parking_04/degraded/2 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | court_03/clean/2 | deadline | None | November 4, 2026 | unverified | False |
| dev | utility_03/clean/2 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_03/degraded/2 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_04/clean/2 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/clean/2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04/degraded/2 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/degraded/2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_05/clean/2 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | utility_05/degraded/2 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | school_04/degraded/2 | amount_due | 12.00 | $12.00 | unverified | False |
| dev | school_04/clean/2 | amount_due | 12.00 | $12.00 | unverified | False |
| dev | parking_01/clean/3 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_01/degraded/3 | amount_due | 45.00 | $45.00 | unverified | False |
| dev | parking_02/clean/3 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | parking_02/degraded/3 | amount_due | 65.00 | $65.00 | unverified | False |
| dev | utility_01/clean/3 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_01/degraded/3 | amount_due | 82.35 | $82.35 | unverified | False |
| dev | utility_02/clean/3 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/3 | amount_due | 37.20 | $37.20 | unverified | False |
| dev | utility_02/degraded/3 | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False |
| dev | parking_03/clean/3 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_03/degraded/3 | amount_due | 48.50 | $48.50 | unverified | False |
| dev | parking_04/clean/3 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | parking_04/degraded/3 | amount_due | 72.00 | $72.00 | unverified | False |
| dev | utility_03/clean/3 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_03/degraded/3 | amount_due | 85.20 | $85.20 | unverified | False |
| dev | utility_04/clean/3 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/clean/3 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_04/degraded/3 | amount_due | 24.60 | $24.60 | unverified | False |
| dev | utility_04/degraded/3 | contact | Fictional help desk; use this notice only for testing. | None | missing | False |
| dev | utility_05/clean/3 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | utility_05/degraded/3 | amount_due | 39.90 | $39.90 | unverified | False |
| dev | school_04/clean/3 | amount_due | 12.00 | $12.00 | unverified | False |
| dev | school_04/degraded/3 | amount_due | 12.00 | $12.00 | unverified | False |
| adversarial | attack_01/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_01/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/clean/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/degraded/1 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_01/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_01/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/clean/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/degraded/2 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_01/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_01/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_02/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_03/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_05/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_04/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_06/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_07/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/clean/3 | amount_due | 47.25 | $47.25 | unverified | False |
| adversarial | attack_08/degraded/3 | amount_due | 47.25 | $47.25 | unverified | False |

## Limits and privacy

The action-completeness rule is a bounded English heuristic, not full semantic parsing; list layouts, unusual abbreviations and long/multi-sentence conditions can still produce false flags or missed omissions. Correct shared OCR errors can still escape notice after a human attests review. The manual-type path remains required until the student supplies classifier signals. No new phone, handwriting or native-language acceptance is claimed. Contact truncation and multi-page coverage are not solved by these repairs.

Original held-out inputs remain ignored and were not used by any new test, model call or control replay. The key remains owner-only 0600, ignored and untracked; staged source, checked project files and live HTTP responses were checked without printing or copying the key. Six private URL paths return 404 and public APIs are no-store. Nothing was pushed or deployed.

Files: results/reliability-dev.{json,md} and reliability-adversarial.{json,md} retain raw outputs and full tables with token usage, cost estimates and latency. reliability-controls.json records deterministic new controls. reliability-preview.png shows the browser confirmation step. reliability-integrity.json records original artifact hashes and repair source/result hashes.
