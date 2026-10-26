# M4 heldout evaluation — completed

Run date: 2026-10-24; today: 2026-10-24; model: `gpt-5.4-mini-2026-03-17`.
Temperature: 0; reasoning: none; scorer: proposed-m4-strict-v2.
Records: 10/10 (clean/degraded × repeats; correlated synthetic layouts).

**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**
Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.
Truth-present accuracy excludes ambiguous/absent fields; false-verification opportunities include them. Thus 100% accuracy does not imply zero unsafe claims.

| Method | False-verified (critical) | Wrong among Verified | Field accuracy (truth present) | Usable verified accuracy | Flagged wrong | Unavailable |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 17/30 (56.7%) | 17/28 (60.7%) | 11/24 (45.8%) | 11/24 (45.8%) | 0/17 (0.0%) | 0/30 (0.0%) |
| B2 | 8/30 (26.7%) | 8/25 (32.0%) | 17/24 (70.8%) | 17/24 (70.8%) | 0/8 (0.0%) | 0/30 (0.0%) |
| full | 4/30 (13.3%) | 4/18 (22.2%) | 18/24 (75.0%) | 14/24 (58.3%) | 3/7 (42.9%) | 0/30 (0.0%) |

## Per-field counts

| Method | Field | Accuracy | False-verified | Abstain when truth exists | Correct missing |
| --- | --- | --- | --- | --- | --- |
| B1 | deadline | 4/7 (57.1%) | 6/10 (60.0%) | 0/7 (0.0%) | 0/2 (0.0%) |
| B1 | amount_due | 6/7 (85.7%) | 2/10 (20.0%) | 0/7 (0.0%) | 2/3 (66.7%) |
| B1 | required_action | 1/10 (10.0%) | 9/10 (90.0%) | 0/10 (0.0%) | N/A |
| B1 | contact | 7/10 (70.0%) | 3/10 (30.0%) | 0/10 (0.0%) | N/A |
| B2 | deadline | 4/7 (57.1%) | 4/10 (40.0%) | 0/7 (0.0%) | 2/2 (100.0%) |
| B2 | amount_due | 6/7 (85.7%) | 1/10 (10.0%) | 0/7 (0.0%) | 3/3 (100.0%) |
| B2 | required_action | 7/10 (70.0%) | 3/10 (30.0%) | 0/10 (0.0%) | N/A |
| B2 | contact | 9/10 (90.0%) | 1/10 (10.0%) | 0/10 (0.0%) | N/A |
| full | deadline | 5/7 (71.4%) | 0/10 (0.0%) | 4/7 (57.1%) | 2/2 (100.0%) |
| full | amount_due | 6/7 (85.7%) | 1/10 (10.0%) | 2/7 (28.6%) | 3/3 (100.0%) |
| full | required_action | 7/10 (70.0%) | 3/10 (30.0%) | 0/10 (0.0%) | N/A |
| full | contact | 9/10 (90.0%) | 1/10 (10.0%) | 0/10 (0.0%) | N/A |

## Repeated-run variance

| Method | Run | False-verified (critical) | Accuracy |
| --- | --- | --- | --- |
| B1 | 1 | 17/30 (56.7%) | 11/24 (45.8%) |

B1 population standard deviation: 0.0.

| B2 | 1 | 8/30 (26.7%) | 17/24 (70.8%) |

B2 population standard deviation: 0.0.

| full | 1 | 4/30 (13.3%) | 18/24 (75.0%) |

full population standard deviation: 0.0.

## Translation

| Method | Language | Number checks | Glossary checks | English fallback | Unavailable |
| --- | --- | --- | --- | --- | --- |
| B1 | es | 2/10 | 4/10 | N/A | 0/10 |
| B1 | tl | 2/10 | 4/10 | N/A | 0/10 |
| full | es | 7/10 | 7/10 | 3/10 | 0/10 |
| full | tl | 7/10 | 7/10 | 3/10 | 0/10 |

## Latency and approximate model cost

| Method | Latency p50 (s) | Latency p95 (s) | Mean model USD / notice |
| --- | --- | --- | --- |
| B1 | 3.66 | 6.36 | 0.002733 |
| B2 | 2.44 | 3.04 | 0.001733 |
| full | 13.82 | 16.51 | 0.012555 |

p50 uses median; p95 uses nearest rank. Full runs both languages sequentially, B1 generates both in one call, and B2 has no language stage. Local/parallel resource contention affects timings.
Cost uses actual reported tokens at [documented standard rates](https://developers.openai.com/api/docs/models/gpt-5.4-mini) checked 2026-10-24. Shared B2/full proposals are not two paid requests. These are hypothetical per-method costs, not values to sum as actual experiment spend.
Reported token usage only; CPU/network/hosting and unreported failed calls excluded; not a billing invoice.

B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.
Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.
B2 reuses the same raw proposal as full; it has no independent language stage.

Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.
Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.
Actual token usage is retained; failed-call unreported usage is unknown, never guessed.
Frozen heldout attempt; no retry or post-test tuning.
A partial report or a failed provider call is never labeled a completed experiment.
Scoring v2 recognizes explicit numeric-field absence claims and declared contact-name aliases. Static all-missing language bundles pass vacuous numeric/glossary checks.
