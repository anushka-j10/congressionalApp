# Current Milestone 4 failures — verification audit

Follow-up 2026-10-25: the missing validator-group ablation capability is now implemented. Full-reference replay remains 0/120 dev and 0/48 adversarial critical false-verified; disabling date validation produces 2/120 dev false-verified deadlines. Detailed ablation failures and coverage are in results/m4-ablations/{dev,adversarial}.{json,md}. The original freeze tag remains unchanged.

The table below is generated directly from the latest 40 dev / 16 adversarial live records, one repetition. Every scored wrong field for B1/B2/full is included; correct-but-unverified full fields are included to expose coverage costs. No unavailable call is counted as quality success. Strict copied-text scoring can penalize equivalent wording; the raw reports retain limited-equivalence flags separately.

| Set | Sample / variant | Mode | Field | Expected | Got | Status | False-verified | Reason/context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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
| dev | court_03/clean | B1 | deadline | None | November 4, 2026 | verified | True | Ambiguous truth: a single value must not be asserted. |
| dev | court_03/clean | B2 | deadline | None | November 4, 2026 | verified | True | Ambiguous truth: a single value must not be asserted. |
| dev | court_03/clean | full | deadline | None | November 4, 2026 | unverified | False | The value could not be checked against its source. |
| dev | court_03/degraded | B1 | deadline | None | November 4, 2026 / November 14, 2026 | verified | True | Ambiguous truth: a single value must not be asserted. |
| dev | court_03/degraded | B2 | deadline | None | November 4, 2026 | verified | True | Ambiguous truth: a single value must not be asserted. |
| dev | court_03/degraded | full | deadline | None | November 4, 2026 | unverified | False | The value could not be checked against its source. |
| dev | utility_03/clean | full | amount_due | 85.20 | $85.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_03/degraded | full | amount_due | 85.20 | $85.20 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/clean | B1 | contact | Fictional help desk; use this notice only for testing. | Contact information is on page 2. | verified | True | Strict scorer mismatch; inspect saved source/output; no unsupported causal claim. |
| dev | utility_04/clean | B2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False | Strict scorer mismatch; inspect saved source/output; no unsupported causal claim. |
| dev | utility_04/clean | full | amount_due | 24.60 | $24.60 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/clean | full | contact | Fictional help desk; use this notice only for testing. | None | missing | False | The extractor did not find this field. Check the photo. |
| dev | utility_04/degraded | B1 | contact | Fictional help desk; use this notice only for testing. | Contact information is on page 2. | verified | True | Strict scorer mismatch; inspect saved source/output; no unsupported causal claim. |
| dev | utility_04/degraded | B2 | contact | Fictional help desk; use this notice only for testing. | None | missing | False | Strict scorer mismatch; inspect saved source/output; no unsupported causal claim. |
| dev | utility_04/degraded | full | amount_due | 24.60 | $24.60 | unverified | False | Check every printed amount against the original photo before confirming amounts. |
| dev | utility_04/degraded | full | contact | Fictional help desk; use this notice only for testing. | None | missing | False | The extractor did not find this field. Check the photo. |
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

Total listed rows: 49. Explicit null expected values represent missing/ambiguous ground truth, not placeholders. Zero-denominator rates are N/A, not fabricated zero percentages.

Current result summaries and all per-field denominators: docs/EVIDENCE.md. Exact commands, PASS/FAIL checklist and grep findings: results/m4-verification/REPORT.md. Original historical failures are preserved in docs/history/FAILURES-before-verification.md; no held-out inference or rescoring was performed.


## Authorized ablation follow-up

| Mode | Dev critical false verified | Adversarial critical false verified |
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

Full tables, per-field accuracy, abstain/MISSING denominators, raw scored records, commands and current 407 Python / 17 JavaScript test outputs: results/m4-ablations/. These are deterministic replays of the latest saved live proposals, not new model runs. All seven field-validator groups plus the separate human-review gate are measured. The held-out set and historical freeze remain untouched.
