# Failures and coverage limits — Milestone 5 Step 2

Updated 2026-10-25. The original held-out failures remain part of the submission evidence. Current dev/adversarial safety numbers do not replace or erase them. The original set has not been rerun with the final code; no post-repair independent held-out accuracy is available.

## Public-release follow-up — October 26

Hosting passes 12/12 public checks, and one synthetic development notice completed live upload, extraction and EN/ES/TL display. **Full phone acceptance remains incomplete.** AJ's iPhone report led to a local reproduction on a publicly linked, angled ticket photo: preprocessing truncated a deadline year and corrupted a contesting-clause number. The original-image reader recovered the full date but still corrupted the clause; the generic quality heuristic added no poor-reading warning. These are not repaired by the new “Choose a notice type” selector wording. No extraction/model call was made on that real photo by the assistant, and its image/identifiers/full transcript are excluded from this public repository. The exact phone output/browser version remains unconfirmed.

Deployed English fallback, unreadable-image abstention and offline checks are incomplete; the browser permission gate declined the separate blank-image upload. Physical-device installation/audio and native-language review remain unverified. [Full release record](results/release-2026-10-26/REPORT.md) and [2.0 priorities](NOTICE_DECODER_2_0_PROMPT.md) retain the distinctions between observed failures, unperformed checks and future work. No held-out rerun occurred.

## Additional Northeast stress run — October 26, 2026

The new exploratory corpus has 18 assistant-authored notices, two per Northeast state, in clean/degraded versions. Its 36 runs have **21/144 strict all-field false-verifications**, including **15/108 critical false-verifications**; **10/36** cases pass strict value scoring. Six strict verification mismatches are harmless labels or supported extra text. The key, prompts and validators were not changed after observing the results.

The most serious findings are an OCR-corrupted year **2926** accepted as a verified deadline (VT_01 clean), a deadline **one day late** when the issue date counts as day one (both VT_02 variants), `.ccm` accepted instead of the printed `.com` (ME_01 clean), and `3C days` accepted in a verified action instead of `30 days` (NY_01 clean). Conditional deadlines and omitted payment restrictions also need attention. These bugs remain unfixed in this testing-only update.

[REPORT.md](results/northeast-stress/REPORT.md) distinguishes strict scoring from qualitative error severity and safe abstention. [FAILURE_DETAILS.md](results/northeast-stress/FAILURE_DETAILS.md) contains every failed case's full visible text, OCR, proposals, checked fields and English output. These results supplement, rather than replace, the original held-out evidence below.

## Original frozen held-out run

Full pipeline: 4/30 critical false-verified, 5/40 all-field false-verified, 18/24 present critical values correct, 14/24 correct and verified, and 6/24 present critical facts withheld. B1 was 17/30 critical false-verified; B2 was 8/30. These are original v2 scores, unchanged.

| Case / field | Recorded failure | Interpretation |
|---|---|---|
| case_03 / amount_due | Expected $75.00, verified $75.60 | Genuine OCR numeric error repeated by source matching |
| case_04 / required_action | Omitted “You must” from otherwise copied action | Strict wording mismatch; retained in original score |
| case_06 / required_action | Omitted “within 14 calendar days of the date of this notice” | Timing clause omitted and shortened action verified |
| case_09 / required_action | Omitted “by Friday, November 6, 2026” | Timing clause omitted and shortened action verified |
| case_07 / contact | Phone only instead of fuller keyed phone/hours/postal contact | Incomplete contact, not an invented phone |

[HELDOUT_RESULTS.md](HELDOUT_RESULTS.md) contains every baseline/full mismatch and present-field abstention with complete expected/actual values, source snippets, reasons, statuses and per-case PASS/FAIL. Cases 01–09 fail its strict four-field end-to-end rule; case 10 passes. Correct-but-unverified facts count as failures under that acceptance rule. Original date normalization/wording limitations and ambiguous case_05 remain documented, not silently corrected. No clearly established answer-key typo has been changed.

## Current dev and adversarial discrepancies

These are the latest live audit records (40 dev, 16 adversarial, scorer v3), distinct from the original held-out version. All wrong baseline/full fields and all present-but-unverified full fields follow. Null expected values carry missing/ambiguous states in the raw reports; they are not placeholders. Full has 0/120 and 0/48 critical false-verified, partly because all 20 dev and 16 adversarial present amounts are withheld.

| Set | Case / variant | Method | Field | Expected | Actual scored value | Status | False verified | Reason |
|---|---|---|---|---|---|---|---|---|
| dev | parking_01/clean | full | amount_due | 45.00 | $45.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_01/degraded | full | amount_due | 45.00 | $45.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_02/degraded | full | amount_due | 65.00 | $65.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_02/clean | full | amount_due | 65.00 | $65.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_01/clean | full | amount_due | 82.35 | $82.35 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_01/degraded | full | amount_due | 82.35 | $82.35 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_02/clean | full | amount_due | 37.20 | $37.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_02/degraded | full | amount_due | 37.20 | $37.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_02/degraded | full | contact | placeholder only; do not send money or personal data. | placeholder only; do not send money or personal data. | unverified | False | The value could not be checked against its source. |
| dev | parking_03/clean | full | amount_due | 48.50 | $48.50 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_03/degraded | full | amount_due | 48.50 | $48.50 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_04/clean | full | amount_due | 72.00 | $72.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | parking_04/degraded | full | amount_due | 72.00 | $72.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | court_03/clean | B1 | deadline | null | November 4, 2026 | verified | True | No validators in this baseline. |
| dev | court_03/clean | B2 | deadline | null | November 4, 2026 | verified | True | No validators in this baseline. |
| dev | court_03/clean | full | deadline | null | November 4, 2026 | unverified | False | The value could not be checked against its source. |
| dev | court_03/degraded | B1 | deadline | null | November 4, 2026 / November 14, 2026 | verified | True | No validators in this baseline. |
| dev | court_03/degraded | B2 | deadline | null | November 4, 2026 | verified | True | No validators in this baseline. |
| dev | court_03/degraded | full | deadline | null | November 4, 2026 | unverified | False | The value could not be checked against its source. |
| dev | utility_03/clean | full | amount_due | 85.20 | $85.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_03/degraded | full | amount_due | 85.20 | $85.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/clean | B1 | contact | Fictional help desk; use this notice only for testing. | Contact information is on page 2. | verified | True | No validators in this baseline. |
| dev | utility_04/clean | B2 | contact | Fictional help desk; use this notice only for testing. | null | missing | False | No validators in this baseline. |
| dev | utility_04/clean | full | amount_due | 24.60 | $24.60 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/clean | full | contact | Fictional help desk; use this notice only for testing. | null | missing | False | The extractor did not find this field. Check the photo. |
| dev | utility_04/degraded | B1 | contact | Fictional help desk; use this notice only for testing. | Contact information is on page 2. | verified | True | No validators in this baseline. |
| dev | utility_04/degraded | B2 | contact | Fictional help desk; use this notice only for testing. | null | missing | False | No validators in this baseline. |
| dev | utility_04/degraded | full | amount_due | 24.60 | $24.60 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/degraded | full | contact | Fictional help desk; use this notice only for testing. | null | missing | False | The extractor did not find this field. Check the photo. |
| dev | utility_05/clean | full | amount_due | 39.90 | $39.90 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_05/degraded | full | amount_due | 39.90 | $39.90 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | school_04/clean | full | amount_due | 12.00 | $12.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | school_04/degraded | full | amount_due | 12.00 | $12.00 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_01/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_01/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_02/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_02/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_03/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_03/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_04/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_04/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_05/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_05/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_06/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_06/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_07/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_07/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_08/clean | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| adversarial | attack_08/degraded | full | amount_due | 47.25 | $47.25 | unverified | False | Check every printed amount against the original photo before confirming amounts. |

Total listed current rows: 49. These records include two dev ambiguous-deadline false-verifications in each baseline and full contact/amount coverage limitations. Raw complete outputs: results/m4-verification/dev.json and adversarial.json.

## Ablation failures

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

Disabling date validation yields two false-verified deadlines on dev; full keeps them unverified. All other unchanged headline rows are limited to these saved proposals. Without text-copy validation, contact coverage changes; exact per-field tables retain that detail. Removing human amount review increases coverage without proving pixel correctness. Full ablation failures and field outputs remain in results/m4-ablations/{dev,adversarial}.json; the matching .md tables contain every denominator.

## Remaining limits and open acceptance checks

- **Handwriting:** no measured handwriting acceptance result. Printed synthetic documents do not establish handwriting reliability.
- **Poor photos:** dev uses generated clean/degraded variants; no representative real-phone capture or mobile-browser acceptance study. Blur, glare, cropping and tiny text can still produce plausible wrong OCR.
- **Classification:** all four production signal lists in `backend/classifier/signals.py` are empty. Automatic classification returns unknown; the measured pipeline uses explicit fixture type selection. This is not automatic type-classification accuracy.
- **Amounts:** current unattended evaluation withholds unreviewed amounts. All 20 present dev amounts and all 16 present adversarial amounts remain unverified. Human confirmation can still miss an OCR error; matching the text does not authenticate the photo or obligation.
- **Translation:** Spanish and Tagalog glossary files are unreviewed. Number/glossary/back-translation checks are mechanical safeguards, not native-speaker or legal-language approval. A correct translation can repeat a wrong extracted fact.
- **Read-aloud:** browser/device voices determine language availability. Desktop checks do not establish working Spanish/Tagalog voices on a judge's phone. Physical-phone testing remains outstanding.
- **Scope:** one page per request. Extra pages are not merged. English field-role, instruction and action-completeness rules are bounded heuristics; unsupported date formats and multiple obligations can cause abstention or missed distinctions.
- **Help and deployment:** local support-service configuration remains empty in `backend/languages/help.json`. Selected official parking routes are available separately. The October 26 HTTPS release passes 12 public checks and one synthetic language workflow; full phone acceptance and deployed fallback/offline checks remain incomplete. See `results/release-2026-10-26/REPORT.md`. Rate limits are process-local and not a dollar spend cap.
- **Privacy:** tested normal app paths use in-memory notice processing and no-store API responses; these tests do not prove secure RAM erasure, OS/library behavior, host-log policy or provider retention. Explicit synthetic evaluation reports intentionally persist test data outside the served frontend. Vendored HEIC diagnostics are disclosed in the privacy audit.

No prompt, validator, answer key or app behavior was changed in this documentation step. Any earlier milestone-local claim that held-out testing had not yet started, that repair had not yet happened, or that ablation was absent is a historical checkpoint, archived under docs/history rather than presented as current status.


## 2026-10-26 phone OCR safety repair

New timing-corruption checks withhold deadline, amount and action when a numeric date is incomplete/invalid or a time limit contains confused letters. No automatic digit correction or OCR-engine switch. Targeted controls: 6 unsafe actions previously verified, now 0; 2 legible controls preserved. Fresh dev run: 0/120 critical false verifications; all-field present accuracy 128/130, verified-correct coverage 107/130, abstention 23/130. Adversarial: 0/48 critical false verifications. Python 452 passed; JavaScript 62 passed. These are development results; the original held-out evidence is unchanged. Full limits, failure outputs, baseline/ablation tables and commands: [phone OCR repair report](results/phone-reading-fix/REPORT.md).
