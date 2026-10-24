# M3 live synthetic translation comparison

Run date: 2026-10-23; model: `gpt-5.4-mini`; reader: preprocessed.
Pinned today: 2026-10-22; temperature: provider default (not sent).
Known fixture types are supplied as explicit user selections; automated classification is still unknown.
Pipeline checks the verified English explanation. Baseline checks the full raw notice; these are different coverage scopes, not field-accuracy scores.
No native-speaker ratings or physical-phone results are included. Back-translation is a heuristic.

| Language | Method | Runs | Numbers | Dates | Month names | Glossary | Disclaimer | All checks | Back-translation | English fallback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| es | pipeline | 8 | 7/8 | 7/8 | 7/8 | 7/8 | 7/8 | 7/8 | 7/8 | 1/8 |
| es | baseline | 8 | 8/8 | 8/8 | 0/8 | 6/8 | 0/8 | 0/8 | 8/8 | N/A |
| tl | pipeline | 8 | 6/8 | 6/8 | 6/8 | 6/8 | 6/8 | 6/8 | 6/8 | 2/8 |
| tl | baseline | 8 | 8/8 | 8/8 | 0/8 | 5/8 | 0/8 | 0/8 | 8/8 | N/A |

Unavailable rows: 0. No provider failures are counted as successful translations.
Pipeline all-check pass counts only accepted target-language translations; English fallbacks are reported separately.
The plain-translate baseline receives no glossary, fixed disclaimer or guarded-field bundle. Its disclaimer failure is therefore an expected structural difference, not evidence of poor linguistic quality.
Rows with no relevant glossary term pass that check vacuously; review per-sample used terms in the JSON report.
Actual token usage is recorded in JSON; no price or unreported failed-request cost is guessed.
