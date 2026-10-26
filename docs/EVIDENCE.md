# Current Milestone 4 evidence — verification audit

Audit date: 2026-10-25. Clean-checkout commit: 6c13e08925fa88643957d9dc777d65b6136a70ae. Overall FAIL: individual-validator leave-one-out ablation is absent. No production feature or behavior was changed; no new freeze tag or held-out run occurred.

391 Python tests (383 existing + eight audit proofs) and 17 JavaScript tests pass. Install, app startup, nine explicit proofs and 25 privacy-targeted cases passed in the clean ARM Python 3.12.14 environment. Exact commands/logs: results/m4-verification/commands.md and REPORT.md.

| Set | B1 critical false-verified | B2 | Full | Full present accuracy | Full correct and Verified |
| --- | --- | --- | --- | --- | --- |
| dev | 2/120 (1.7%) | 2/120 (1.7%) | 0/120 (0.0%) | 92/92 (100.0%) | 72/92 (78.3%) |
| adversarial | 0/48 (0.0%) | 0/48 (0.0%) | 0/48 (0.0%) | 48/48 (100.0%) | 32/48 (66.7%) |

Config: gpt-5.4-mini-2026-03-17, temperature 0, reasoning none, today 2026-10-24, local preprocessed/original comparison, clean/degraded, one repetition, scorer proposed-reliability-v3. Human amount review is not simulated; unreviewed amounts are withheld, so low false-verification is not evidence of corrected OCR or universal safety. Same cases/OCR/scorer are used for B1/B2/full. All methods/language outputs were available.

## Per-field latest results

| Set | Mode | Field | Accuracy | False-verified | Abstain with truth present | Correct missing |
| --- | --- | --- | --- | --- | --- | --- |
| dev | B1 | deadline | 34/34 (100.0%) | 2/40 (5.0%) | 0/34 (0.0%) | 4/4 (100.0%) |
| dev | B1 | amount_due | 20/20 (100.0%) | 0/40 (0.0%) | 0/20 (0.0%) | 20/20 (100.0%) |
| dev | B1 | required_action | 38/38 (100.0%) | 0/40 (0.0%) | 0/38 (0.0%) | 2/2 (100.0%) |
| dev | B1 | contact | 36/38 (94.7%) | 2/40 (5.0%) | 0/38 (0.0%) | 2/2 (100.0%) |
| dev | B2 | deadline | 34/34 (100.0%) | 2/40 (5.0%) | 0/34 (0.0%) | 4/4 (100.0%) |
| dev | B2 | amount_due | 20/20 (100.0%) | 0/40 (0.0%) | 0/20 (0.0%) | 20/20 (100.0%) |
| dev | B2 | required_action | 38/38 (100.0%) | 0/40 (0.0%) | 0/38 (0.0%) | 2/2 (100.0%) |
| dev | B2 | contact | 36/38 (94.7%) | 0/40 (0.0%) | 2/38 (5.3%) | 2/2 (100.0%) |
| dev | full | deadline | 34/34 (100.0%) | 0/40 (0.0%) | 0/34 (0.0%) | 4/4 (100.0%) |
| dev | full | amount_due | 20/20 (100.0%) | 0/40 (0.0%) | 20/20 (100.0%) | 20/20 (100.0%) |
| dev | full | required_action | 38/38 (100.0%) | 0/40 (0.0%) | 0/38 (0.0%) | 2/2 (100.0%) |
| dev | full | contact | 36/38 (94.7%) | 0/40 (0.0%) | 3/38 (7.9%) | 2/2 (100.0%) |
| adversarial | B1 | deadline | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B1 | amount_due | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B1 | required_action | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B1 | contact | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B2 | deadline | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B2 | amount_due | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B2 | required_action | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | B2 | contact | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | full | deadline | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | full | amount_due | 16/16 (100.0%) | 0/16 (0.0%) | 16/16 (100.0%) | N/A (zero denominator) |
| adversarial | full | required_action | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |
| adversarial | full | contact | 16/16 (100.0%) | 0/16 (0.0%) | 0/16 (0.0%) | N/A (zero denominator) |

## Audit limitations and provenance

Item 5 FAIL: only all-validator-on/off modes exist, not each validator off individually. This is a missing capability; it was listed rather than implemented under the no-feature instruction. Freeze remains blocked; the original eval-freeze still points to 24d729a540ed3913ced09ee42af89765fd921c4b.

No held-out set was run, reread or rescored in this audit. Earlier held-out results remain historical and unchanged. Native reviews, phone/handwriting evidence and student classifier signals remain separate outstanding work; no independent student coding claim is added. Raw outputs, translations, usage, timing, strict and limited-equivalence tables are in results/m4-verification/{dev,adversarial}.{json,md}.

Prior checkpoint history is archived intact in docs/history/EVIDENCE-before-verification.md and docs/history/FAILURES-before-verification.md. AI_USAGE.md identifies generated code/tests. This file reports only current measured numbers; no contest narrative is written.
