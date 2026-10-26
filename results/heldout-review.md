# Final held-out checkpoint — 2026-10-24

The ten student-supplied cases were evaluated once after the eval-freeze tag. All ten records completed, with no unavailable extraction, baseline or explanation methods. No production code, evaluator, scorer, model settings, expected answers or aliases were changed after observing outcomes. The source fingerprint and HEAD still match the original freeze. Packaging took place after freeze, before inference; original images and student answer strings were retained. Notes in the answer key were not scored or sent to the model.

| Set / phase | B1 critical false-verified | B2 | Full |
| --- | --- | --- | --- |
| Final dev, 120 records | 6/360 (1.7%) | 6/360 (1.7%) | 0/360 (0.0%) |
| Final adversarial, 48 records | 0/144 (0.0%) | 0/144 (0.0%) | 0/144 (0.0%) |
| Held-out, 10 records once | 17/30 (56.7%) | 8/30 (26.7%) | 4/30 (13.3%) |

These are the unchanged frozen scorer's exact-match results, not a claim that every text mismatch is a dangerous factual error. Full has 4/18 wrong among Verified critical outputs, 18/24 truth-present critical values correct, and 14/24 correct and Verified. All-field false-verification is 5/40: the four critical mismatches plus an abbreviated contact. Full marks absent deadlines correctly in 2/2 cases and absent amounts in 3/3. It leaves 4/7 present deadlines and 2/7 present amounts unverified, illustrating the coverage cost of conservative validation.

Held-out is substantially worse than dev: 13.3% versus 0% on this headline. This suggests limited generalization from correlated development fixtures and possible overfitting to their formats. More varied layouts expose OCR errors and incomplete extraction; the strict scorer also penalizes semantically equivalent wording and unrecognized date formats. Ten cases and one run cannot separate or quantify those effects reliably. No revised metric, post-test scorer repair, tuning, or rerun is used to improve the headline.

## Review the actual failures first

| Case / field | Expected | Full output / status | Interpretation |
| --- | --- | --- | --- |
| case_03 amount | 75.00 | 75.60 / Verified | Genuine numeric error: OCR read CHARGE as $75.60. Source matching verified the incorrect OCR rather than the original pixels. The harness confirms OCR unchanged; it does not simulate a human correcting the text. |
| case_04 action | You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026. | appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026 / Verified | Same obligation, location and time; frozen exact-copy scorer flags omission of 'You must'. This is a wording mismatch, not an invented obligation. |
| case_06 action | File a written response with the Clerk's Office within 14 calendar days of the date of this notice. | File a written response with the Clerk's Office / Verified | Incomplete action: relative timing clause dropped. The separate deadline card correctly calculates 2026-11-05, which mitigates but does not change the scored action mismatch. |
| case_09 action | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026. | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera / Verified | Incomplete action: return-by clause dropped, while the separate correct deadline is unverified. This leaves actionable timing uncertain in the full output. |
| case_07 contact | Customer Service phone, hours and PO Box | (800) 555-0155 / Verified | Correct phone, incomplete contact compared with the student key. Hours and postal alternative are omitted; no fabricated phone. Outside the critical headline. |

## Conservative flags and scorer limitations

The full pipeline flags the ambiguous case_05 date rather than showing a selected date as Verified; B1/B2 both select November 20. That is a safety improvement, although the frozen scorer still calls the non-null unverified candidate wrong under an ambiguous truth state. Full abstains correctly on missing deadline cases_03/10 and missing amount cases_04/06/10.

Correct values are conservatively flagged: deadlines in cases_01/04/08/09, amounts in cases_02/09. Their generic validator reason is retained in raw output; a precise internal cause is not asserted without a separate future investigation. Weekday-prefixed dates in cases_04/09 are not recognized by the frozen scorer's canonicalizer; relative phrases in B1/B2 case_06 also do not equal an ISO date. B1 case_04's explicit prose that fines are not stated is counted wrong because this particular absence phrase is outside the frozen absence vocabulary. Many B1 action/contact discrepancies are paraphrases, supported additions or punctuation differences. All original counts remain unchanged.

These observations explain limits of interpretation, not retrospective ground-truth changes. Student answers were copied exactly, MISSING/AMBIGUOUS mapped to null plus explicit states, and no new acceptable aliases were added.

## Language, capture and protocol limits

Full Spanish and Tagalog each pass number/glossary checks in 7/10 cases and fall back to English in 3/10. Mechanical checks and back-translation are not native-speaker reviews; a correctly translated wrong field remains wrong. Full p50/p95 latency is 13.82/16.51 seconds and estimated mean model cost is $0.012555 per notice using recorded tokens and the frozen standard rates; CPU/hosting and unknown unreported failures are excluded. These rates were previously documented, not freshly priced for this held-out run.

One original image per case was processed, under the frozen harness label 'clean'; no new degraded copies or physical-phone test is claimed. Types are 3 parking, 3 court, 2 utility and 2 school. Automatic classification still yields unknown for all ten; evaluation uses the student's explicit type selection. There was one repetition only: the generated table's zero standard deviation is arithmetic for one observation, not measured repeatability. The generic clean/degraded caption in the raw report does not mean both variants were run.

Raw outputs and frozen tables: results/heldout-final.json and results/heldout-final.md. Detailed unchanged scorer discrepancies follow in results/heldout-review.md. Input hashes and post-run integrity checks are in results/heldout-protocol.json. Student input copies remain in the ignored eval/heldout folder. No key is copied there, no expected labels are provided to inference calls, and nothing was pushed or deployed.

This concludes the selected Part D evaluation. Stop for student review; do not start another fix round or reuse these ten cases as a fresh held-out benchmark. Native language reviews, real-phone checks and independent student contributions remain outstanding.

## Every frozen-scorer mismatch or present-field abstention

| Case | Mode | Field | Expected | Got | Status | False-verified |
| --- | --- | --- | --- | --- | --- | --- |
| case_01 | B1 | required_action | Pay the $52.00 fine or request a hearing on or before November 16, 2026. | Pay the fine or request a hearing before November 16, 2026. | verified | True |
| case_01 | B1 | contact | Call (201) 555-0148 or visit 88 Quay Road, Suite 200, Harbor Point, NJ 07999. | (201) 555-0148 or 88 Quay Road, Suite 200, Harbor Point, NJ 07999 | verified | True |
| case_01 | full | deadline | 2026-11-16 | November 16, 2026 | unverified | False |
| case_02 | B1 | required_action | Pay the early payment amount of $35.00 by 11/09/2026. | Pay the early payment amount by 11/09/2026, or send a written request for a hearing if you want to contest the citation. | verified | True |
| case_02 | B1 | contact | Millbrook Township Traffic Division, 15 Elm Court, Millbrook, NJ 07998. Phone: (908) 555-0167. | Millbrook Township Traffic Division, 15 Elm Court, Millbrook, NJ 07998. Phone: (908) 555-0167. Website: tickets.millbrook-twp.example | verified | True |
| case_02 | full | amount_due | 35.00 | $35.00 | unverified | False |
| case_03 | B1 | deadline | None | 10/22/26 | verified | True |
| case_03 | B1 | amount_due | 75.00 | $75.60 | verified | True |
| case_03 | B2 | amount_due | 75.00 | $75.60 | verified | True |
| case_03 | full | amount_due | 75.00 | 75.60 | verified | True |
| case_04 | B1 | deadline | 2026-12-03 | Thursday, December 3, 2026 at 9:00 AM | verified | True |
| case_04 | B1 | amount_due | None | Not stated; fines and costs, if any, will be determined after the hearing. | verified | True |
| case_04 | B1 | required_action | You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026. | Appear in person in Courtroom 2, bring this notice and any documents or witnesses you want the court to consider, and contact the Court Administrator before the hearing if you cannot attend. | verified | True |
| case_04 | B2 | deadline | 2026-12-03 | Thursday, December 3, 2026 | verified | True |
| case_04 | B2 | required_action | You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026. | appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026 | verified | True |
| case_04 | full | deadline | 2026-12-03 | Thursday, December 3, 2026 | unverified | False |
| case_04 | full | required_action | You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026. | appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026 | verified | True |
| case_05 | B1 | deadline | None | November 20, 2026 | verified | True |
| case_05 | B1 | required_action | Pay the total amount due by November 20, 2026 to avoid a court appearance, or appear in Courtroom A on December 8, 2026 at 1:30 PM. | Pay the total amount due by November 20, 2026 to avoid a court appearance, or appear in Courtroom A on December 8, 2026 at 1:30 PM to enter a plea. | verified | True |
| case_05 | B2 | deadline | None | November 20, 2026 | verified | True |
| case_05 | full | deadline | None | November 20, 2026 | unverified | False |
| case_06 | B1 | deadline | 2026-11-05 | Within 14 calendar days of October 22, 2026 | verified | True |
| case_06 | B1 | required_action | File a written response with the Clerk's Office within 14 calendar days of the date of this notice. | File a written response with the Clerk's Office stating whether you agree or disagree with the complaint and why. You may file in person, by mail, or in the drop box outside Room 104. | verified | True |
| case_06 | B2 | deadline | 2026-11-05 | within 14 calendar days of the date of this notice | verified | True |
| case_06 | B2 | required_action | File a written response with the Clerk's Office within 14 calendar days of the date of this notice. | File a written response with the Clerk's Office | verified | True |
| case_06 | full | required_action | File a written response with the Clerk's Office within 14 calendar days of the date of this notice. | File a written response with the Clerk's Office | verified | True |
| case_07 | B1 | required_action | Pay $142.37 by November 12, 2026 to avoid a late payment charge. | Pay $142.37 by November 12, 2026 to avoid a late payment charge. A late payment charge of $8.50 applies to any unpaid balance after the due date. | verified | True |
| case_07 | B2 | contact | Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM. Write to PO Box 4410, Northfield, NJ 07994. | (800) 555-0155 | verified | True |
| case_07 | full | contact | Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM. Write to PO Box 4410, Northfield, NJ 07994. | (800) 555-0155 | verified | True |
| case_08 | B1 | required_action | Pay the total amount due of $111.35 by November 5, 2026. | Pay the total amount due of $111.35 by November 5, 2026 to avoid a $5.00 late fee and possible service interruption after November 19, 2026. | verified | True |
| case_08 | B1 | contact | Billing Office: (856) 555-0138, or visit 210 Spring Street, Clearwater, NJ 07993. | Billing Office: (856) 555-0138 or visit 210 Spring Street, Clearwater, NJ 07993. | verified | True |
| case_08 | full | deadline | 2026-11-05 | November 5, 2026 | unverified | False |
| case_09 | B1 | deadline | 2026-11-06 | Friday, November 6, 2026 | verified | True |
| case_09 | B1 | required_action | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026. | Return the signed permission slip and the $12.00 trip fee to Ms. Rivera. If your child is attending, also indicate permission for the trip. | verified | True |
| case_09 | B2 | deadline | 2026-11-06 | Friday, November 6, 2026 | verified | True |
| case_09 | B2 | required_action | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026. | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera | verified | True |
| case_09 | full | deadline | 2026-11-06 | Friday, November 6, 2026 | unverified | False |
| case_09 | full | amount_due | 12.00 | $12.00 | unverified | False |
| case_09 | full | required_action | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026. | Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera | verified | True |
| case_10 | B1 | deadline | None | Please contact the Attendance Office as soon as possible. Parent-teacher conferences will take place during the week of November 16–20, 2026. | verified | True |
| case_10 | B1 | required_action | Please contact the Attendance Office as soon as possible to schedule a meeting. | Schedule a meeting with the Attendance Office and send a note for any absences with a medical or family reason so they can be excused. | verified | True |
