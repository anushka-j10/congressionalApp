# M4 adversarial evaluation — completed

Run date: 2026-10-24; today: 2026-10-24; model: `gpt-5.4-mini-2026-03-17`.
Temperature: 0; reasoning: none; scorer: proposed-m4-strict-v1.
Records: 48/48 (clean/degraded × repeats; correlated synthetic layouts).

**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**
Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.

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

B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.
Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.
B2 reuses the same raw proposal as full; it has no independent language stage.

Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.
Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.
Cost table cut for time. Actual token usage is retained; failed-call unreported usage is unknown, never guessed.
No heldout data is included. A partial report or a failed provider call is never labeled a completed experiment.
