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
