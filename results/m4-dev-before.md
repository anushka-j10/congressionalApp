# M4 dev evaluation — completed

Run date: 2026-10-24; today: 2026-10-24; model: `gpt-5.4-mini-2026-03-17`.
Temperature: 0; reasoning: none; scorer: proposed-m4-strict-v1.
Records: 120/120 (clean/degraded × repeats; correlated synthetic layouts).

**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**
Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.

| Method | False-verified (critical) | Wrong among Verified | Field accuracy (truth present) | Usable verified accuracy | Flagged wrong | Unavailable |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 36/360 (10.0%) | 36/312 (11.5%) | 276/276 (100.0%) | 276/276 (100.0%) | 0/36 (0.0%) | 0/360 (0.0%) |
| B2 | 24/360 (6.7%) | 24/300 (8.0%) | 276/276 (100.0%) | 276/276 (100.0%) | 0/24 (0.0%) | 0/360 (0.0%) |
| full | 6/360 (1.7%) | 6/276 (2.2%) | 276/276 (100.0%) | 270/276 (97.8%) | 6/12 (50.0%) | 0/360 (0.0%) |

## Per-field counts

| Method | Field | Accuracy | False-verified | Abstain when truth exists | Correct missing |
| --- | --- | --- | --- | --- | --- |
| B1 | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| B1 | amount_due | 60/60 (100.0%) | 30/120 (25.0%) | 0/60 (0.0%) | 30/60 (50.0%) |
| B1 | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B1 | contact | 108/114 (94.7%) | 6/120 (5.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B2 | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| B2 | amount_due | 60/60 (100.0%) | 18/120 (15.0%) | 0/60 (0.0%) | 42/60 (70.0%) |
| B2 | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 0/114 (0.0%) | 6/6 (100.0%) |
| B2 | contact | 99/114 (86.8%) | 9/120 (7.5%) | 6/114 (5.3%) | 6/6 (100.0%) |
| full | deadline | 102/102 (100.0%) | 6/120 (5.0%) | 0/102 (0.0%) | 12/12 (100.0%) |
| full | amount_due | 60/60 (100.0%) | 0/120 (0.0%) | 0/60 (0.0%) | 54/60 (90.0%) |
| full | required_action | 114/114 (100.0%) | 0/120 (0.0%) | 6/114 (5.3%) | 6/6 (100.0%) |
| full | contact | 99/114 (86.8%) | 9/120 (7.5%) | 12/114 (10.5%) | 6/6 (100.0%) |

## Repeated-run variance

| Method | Run | False-verified (critical) | Accuracy |
| --- | --- | --- | --- |
| B1 | 1 | 12/120 (10.0%) | 92/92 (100.0%) |
| B1 | 2 | 12/120 (10.0%) | 92/92 (100.0%) |
| B1 | 3 | 12/120 (10.0%) | 92/92 (100.0%) |

B1 population standard deviation: 0.0.

| B2 | 1 | 7/120 (5.8%) | 92/92 (100.0%) |
| B2 | 2 | 7/120 (5.8%) | 92/92 (100.0%) |
| B2 | 3 | 10/120 (8.3%) | 92/92 (100.0%) |

B2 population standard deviation: 0.01178511301977579.

| full | 1 | 2/120 (1.7%) | 92/92 (100.0%) |
| full | 2 | 2/120 (1.7%) | 92/92 (100.0%) |
| full | 3 | 2/120 (1.7%) | 92/92 (100.0%) |

full population standard deviation: 0.0.

## Translation

| Method | Language | Number checks | Glossary checks | English fallback | Unavailable |
| --- | --- | --- | --- | --- | --- |
| B1 | es | 110/120 | 90/120 | N/A | 0/120 |
| B1 | tl | 110/120 | 72/120 | N/A | 0/120 |
| full | es | 109/120 | 109/120 | 5/120 | 0/120 |
| full | tl | 100/120 | 100/120 | 14/120 | 0/120 |

B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.
Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.
B2 reuses the same raw proposal as full; it has no independent language stage.

Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.
Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.
Cost table cut for time. Actual token usage is retained; failed-call unreported usage is unknown, never guessed.
No heldout data is included. A partial report or a failed provider call is never labeled a completed experiment.
