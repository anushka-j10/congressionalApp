# Held-out results — Step 1 checkpoint, 2026-10-25

**Step 1 status: BLOCKED for the final configuration. No new held-out run was performed.**

Preflight working tree: clean (git status --short produced no output). HEAD: `3f01f40584ce4a67ed7036ee8e40e44fe97e7158`. Existing `eval-freeze`: `24d729a540ed3913ced09ee42af89765fd921c4b`. The tag exists, but HEAD differs. The single-use ledger `eval/heldout-run-started.json` records an already-started run at the original freeze, and `results/heldout-protocol.json` records that run completed on 2026-10-24 with ten records and one repetition. The ledger was not reset and the tag was not moved.

The table below reports the **existing original frozen run**, not an evaluation of the repaired final code. Since the original cases/results informed subsequent development, running them again would be a regression measurement, not an independent held-out evaluation. A fresh independently labeled set and a separately versioned freeze/run protocol are needed to measure the final version honestly. No original image or answer-key document was reopened for this checkpoint; recorded answers and frozen scores were read from the existing result artifact.

The user states the answer key was written by hand independently of this app. This report preserves its previously packaged expected answers exactly; it does not change annotations, aliases, prompts, validators, configuration or scoring. No clearly established answer-key typo is identified in the recorded review. Wording differences and ambiguous obligations are not assumed to be typos.

## Recorded original run

Model: `gpt-5.4-mini-2026-03-17`; temperature 0; reasoning `none`; evaluation date `2026-10-24`; scorer `proposed-m4-strict-v2`. Ten original images, one variant per case labeled `clean`, one repetition. This is not a physical-phone or degraded-image trial. All methods completed. Automatic classification used fixture type selection; source matching relied on unchanged OCR text.

Fractions below are exact; no rounded percentages are used. Present-field accuracy excludes missing/ambiguous truth. False-verified rate includes all field opportunities. Abstain-when-present counts missing/unverified outputs where the answer key contains a fact. Correct MISSING is reported separately.

| Method | Critical false verified | Present accuracy, critical | Correct verified, critical | Abstain when present, critical | All-field false verified |
|---|---|---|---|---|---|
| B1 | 17/30 | 11/24 | 11/24 | 0/24 | 20/40 |
| B2 | 8/30 | 17/24 | 17/24 | 0/24 | 9/40 |
| full | 4/30 | 18/24 | 14/24 | 6/24 | 5/40 |

## Full-pipeline per-field results

| Field | Present accuracy | Correct verified | False verified | Abstain when present | Correct MISSING |
|---|---|---|---|---|---|
| deadline | 5/7 | 3/7 | 0/10 | 4/7 | 2/2 |
| amount_due | 6/7 | 4/7 | 1/10 | 2/7 | 3/3 |
| required_action | 7/10 | 7/10 | 3/10 | 0/10 | N/A (zero denominator) |
| contact | 9/10 | 9/10 | 1/10 | 0/10 | N/A (zero denominator) |

## Per-case PASS/FAIL (original run)

PASS here requires all four fields correct under the original frozen scorer, every present fact verified, and missing/ambiguous facts withheld. A correct but unverified fact therefore fails this strict end-to-end acceptance rule. This rule labels the recorded results; the scorer and its field scores were not rerun or changed.

| Case | PASS/FAIL | Correct values / 4 | False verified / 4 | Present-field abstentions | Failure fields |
|---|---|---|---|---|---|
| case_01 | FAIL | 4/4 | 0/4 | 1 | deadline |
| case_02 | FAIL | 4/4 | 0/4 | 1 | amount_due |
| case_03 | FAIL | 3/4 | 1/4 | 0 | amount_due |
| case_04 | FAIL | 2/4 | 1/4 | 1 | deadline, required_action |
| case_05 | FAIL | 3/4 | 0/4 | 0 | deadline |
| case_06 | FAIL | 3/4 | 1/4 | 0 | required_action |
| case_07 | FAIL | 3/4 | 1/4 | 0 | contact |
| case_08 | FAIL | 4/4 | 0/4 | 1 | deadline |
| case_09 | FAIL | 2/4 | 1/4 | 2 | amount_due, deadline, required_action |
| case_10 | PASS | 4/4 | 0/4 | 0 | none |

## Failures and abstentions in full

Every wrong field and every present-but-unverified field is shown below for all three methods. Expected answers, actual values, status, source snippets and validator reasons are reproduced without shortening. Null denotes an absent/ambiguous expected value; see its explicit state. These are strict scorer discrepancies; they are not all invented facts. The source artifact contains complete outputs for passing fields and explanations too.

### case_01 / B1 / required_action

```json
{
  "case": "case_01",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Pay the $52.00 fine or request a hearing on or before November 16, 2026.",
  "actual_scored_value": "Pay the fine or request a hearing before November 16, 2026.",
  "raw_value": "Pay the fine or request a hearing before November 16, 2026.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_01 / B1 / contact

```json
{
  "case": "case_01",
  "method": "B1",
  "field": "contact",
  "expected_state": "present",
  "expected": "Call (201) 555-0148 or visit 88 Quay Road, Suite 200, Harbor Point, NJ 07999.",
  "actual_scored_value": "(201) 555-0148 or 88 Quay Road, Suite 200, Harbor Point, NJ 07999",
  "raw_value": "(201) 555-0148 or 88 Quay Road, Suite 200, Harbor Point, NJ 07999",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_01 / full / deadline

```json
{
  "case": "case_01",
  "method": "full",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-16",
  "actual_scored_value": "November 16, 2026",
  "raw_value": "November 16, 2026",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": false,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "Pay the $52.00 fine or request a hearing on or before November 16, 2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_02 / B1 / required_action

```json
{
  "case": "case_02",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Pay the early payment amount of $35.00 by 11/09/2026.",
  "actual_scored_value": "Pay the early payment amount by 11/09/2026, or send a written request for a hearing if you want to contest the citation.",
  "raw_value": "Pay the early payment amount by 11/09/2026, or send a written request for a hearing if you want to contest the citation.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_02 / B1 / contact

```json
{
  "case": "case_02",
  "method": "B1",
  "field": "contact",
  "expected_state": "present",
  "expected": "Millbrook Township Traffic Division, 15 Elm Court, Millbrook, NJ 07998. Phone: (908) 555-0167.",
  "actual_scored_value": "Millbrook Township Traffic Division, 15 Elm Court, Millbrook, NJ 07998. Phone: (908) 555-0167. Website: tickets.millbrook-twp.example",
  "raw_value": "Millbrook Township Traffic Division, 15 Elm Court, Millbrook, NJ 07998. Phone: (908) 555-0167. Website: tickets.millbrook-twp.example",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_02 / full / amount_due

```json
{
  "case": "case_02",
  "method": "full",
  "field": "amount_due",
  "expected_state": "present",
  "expected": "35.00",
  "actual_scored_value": "$35.00",
  "raw_value": "$35.00",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": false,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "Pay the early payment amount of $35.00 by 11/09/2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_03 / B1 / deadline

```json
{
  "case": "case_03",
  "method": "B1",
  "field": "deadline",
  "expected_state": "missing",
  "expected": null,
  "actual_scored_value": "10/22/26",
  "raw_value": "10/22/26",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_03 / B1 / amount_due

```json
{
  "case": "case_03",
  "method": "B1",
  "field": "amount_due",
  "expected_state": "present",
  "expected": "75.00",
  "actual_scored_value": "$75.60",
  "raw_value": "$75.60",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_03 / B2 / amount_due

```json
{
  "case": "case_03",
  "method": "B2",
  "field": "amount_due",
  "expected_state": "present",
  "expected": "75.00",
  "actual_scored_value": "$75.60",
  "raw_value": "$75.60",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "CHARGE: $75.60",
  "reason": null
}
```

### case_03 / full / amount_due

```json
{
  "case": "case_03",
  "method": "full",
  "field": "amount_due",
  "expected_state": "present",
  "expected": "75.00",
  "actual_scored_value": "75.60",
  "raw_value": "$75.60",
  "normalized_value": "75.60",
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "CHARGE: $75.60",
  "reason": "Matches the confirmed text. Check that this is the right fact on your original notice."
}
```

### case_04 / B1 / deadline

```json
{
  "case": "case_04",
  "method": "B1",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-12-03",
  "actual_scored_value": "Thursday, December 3, 2026 at 9:00 AM",
  "raw_value": "Thursday, December 3, 2026 at 9:00 AM",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_04 / B1 / amount_due

```json
{
  "case": "case_04",
  "method": "B1",
  "field": "amount_due",
  "expected_state": "missing",
  "expected": null,
  "actual_scored_value": "Not stated; fines and costs, if any, will be determined after the hearing.",
  "raw_value": "Not stated; fines and costs, if any, will be determined after the hearing.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_04 / B1 / required_action

```json
{
  "case": "case_04",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "actual_scored_value": "Appear in person in Courtroom 2, bring this notice and any documents or witnesses you want the court to consider, and contact the Court Administrator before the hearing if you cannot attend.",
  "raw_value": "Appear in person in Courtroom 2, bring this notice and any documents or witnesses you want the court to consider, and contact the Court Administrator before the hearing if you cannot attend.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_04 / B2 / deadline

```json
{
  "case": "case_04",
  "method": "B2",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-12-03",
  "actual_scored_value": "Thursday, December 3, 2026",
  "raw_value": "Thursday, December 3, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "reason": null
}
```

### case_04 / B2 / required_action

```json
{
  "case": "case_04",
  "method": "B2",
  "field": "required_action",
  "expected_state": "present",
  "expected": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "actual_scored_value": "appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026",
  "raw_value": "appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "reason": null
}
```

### case_04 / full / deadline

```json
{
  "case": "case_04",
  "method": "full",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-12-03",
  "actual_scored_value": "Thursday, December 3, 2026",
  "raw_value": "Thursday, December 3, 2026",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": true,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_04 / full / required_action

```json
{
  "case": "case_04",
  "method": "full",
  "field": "required_action",
  "expected_state": "present",
  "expected": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "actual_scored_value": "appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026",
  "raw_value": "appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "You must appear in person in Courtroom 2 at 9:00 AM on Thursday, December 3, 2026.",
  "reason": "Matches the confirmed text. Check that this is the right fact on your original notice."
}
```

### case_05 / B1 / deadline

```json
{
  "case": "case_05",
  "method": "B1",
  "field": "deadline",
  "expected_state": "ambiguous",
  "expected": null,
  "actual_scored_value": "November 20, 2026",
  "raw_value": "November 20, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_05 / B1 / required_action

```json
{
  "case": "case_05",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Pay the total amount due by November 20, 2026 to avoid a court appearance, or appear in Courtroom A on December 8, 2026 at 1:30 PM.",
  "actual_scored_value": "Pay the total amount due by November 20, 2026 to avoid a court appearance, or appear in Courtroom A on December 8, 2026 at 1:30 PM to enter a plea.",
  "raw_value": "Pay the total amount due by November 20, 2026 to avoid a court appearance, or appear in Courtroom A on December 8, 2026 at 1:30 PM to enter a plea.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_05 / B2 / deadline

```json
{
  "case": "case_05",
  "method": "B2",
  "field": "deadline",
  "expected_state": "ambiguous",
  "expected": null,
  "actual_scored_value": "November 20, 2026",
  "raw_value": "November 20, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Pay the total amount due by November 20, 2026.",
  "reason": null
}
```

### case_05 / full / deadline

```json
{
  "case": "case_05",
  "method": "full",
  "field": "deadline",
  "expected_state": "ambiguous",
  "expected": null,
  "actual_scored_value": "November 20, 2026",
  "raw_value": "November 20, 2026",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": true,
  "false_verified": false,
  "abstain_when_truth_exists": false,
  "source_snippet": "Pay the total amount due by November 20, 2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_06 / B1 / deadline

```json
{
  "case": "case_06",
  "method": "B1",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-05",
  "actual_scored_value": "Within 14 calendar days of October 22, 2026",
  "raw_value": "Within 14 calendar days of October 22, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_06 / B1 / required_action

```json
{
  "case": "case_06",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "actual_scored_value": "File a written response with the Clerk's Office stating whether you agree or disagree with the complaint and why. You may file in person, by mail, or in the drop box outside Room 104.",
  "raw_value": "File a written response with the Clerk's Office stating whether you agree or disagree with the complaint and why. You may file in person, by mail, or in the drop box outside Room 104.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_06 / B2 / deadline

```json
{
  "case": "case_06",
  "method": "B2",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-05",
  "actual_scored_value": "within 14 calendar days of the date of this notice",
  "raw_value": "within 14 calendar days of the date of this notice",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "reason": null
}
```

### case_06 / B2 / required_action

```json
{
  "case": "case_06",
  "method": "B2",
  "field": "required_action",
  "expected_state": "present",
  "expected": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "actual_scored_value": "File a written response with the Clerk's Office",
  "raw_value": "File a written response with the Clerk's Office",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "reason": null
}
```

### case_06 / full / required_action

```json
{
  "case": "case_06",
  "method": "full",
  "field": "required_action",
  "expected_state": "present",
  "expected": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "actual_scored_value": "File a written response with the Clerk's Office",
  "raw_value": "File a written response with the Clerk's Office",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "File a written response with the Clerk's Office within 14 calendar days of the date of this notice.",
  "reason": "Matches the confirmed text. Check that this is the right fact on your original notice."
}
```

### case_07 / B1 / required_action

```json
{
  "case": "case_07",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Pay $142.37 by November 12, 2026 to avoid a late payment charge.",
  "actual_scored_value": "Pay $142.37 by November 12, 2026 to avoid a late payment charge. A late payment charge of $8.50 applies to any unpaid balance after the due date.",
  "raw_value": "Pay $142.37 by November 12, 2026 to avoid a late payment charge. A late payment charge of $8.50 applies to any unpaid balance after the due date.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_07 / B2 / contact

```json
{
  "case": "case_07",
  "method": "B2",
  "field": "contact",
  "expected_state": "present",
  "expected": "Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM. Write to PO Box 4410, Northfield, NJ 07994.",
  "actual_scored_value": "(800) 555-0155",
  "raw_value": "(800) 555-0155",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM.",
  "reason": null
}
```

### case_07 / full / contact

```json
{
  "case": "case_07",
  "method": "full",
  "field": "contact",
  "expected_state": "present",
  "expected": "Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM. Write to PO Box 4410, Northfield, NJ 07994.",
  "actual_scored_value": "(800) 555-0155",
  "raw_value": "(800) 555-0155",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Customer Service: (800) 555-0155, Monday to Friday, 7 AM to 7 PM.",
  "reason": "Matches the confirmed text. Check that this is the right fact on your original notice."
}
```

### case_08 / B1 / required_action

```json
{
  "case": "case_08",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Pay the total amount due of $111.35 by November 5, 2026.",
  "actual_scored_value": "Pay the total amount due of $111.35 by November 5, 2026 to avoid a $5.00 late fee and possible service interruption after November 19, 2026.",
  "raw_value": "Pay the total amount due of $111.35 by November 5, 2026 to avoid a $5.00 late fee and possible service interruption after November 19, 2026.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_08 / B1 / contact

```json
{
  "case": "case_08",
  "method": "B1",
  "field": "contact",
  "expected_state": "present",
  "expected": "Billing Office: (856) 555-0138, or visit 210 Spring Street, Clearwater, NJ 07993.",
  "actual_scored_value": "Billing Office: (856) 555-0138 or visit 210 Spring Street, Clearwater, NJ 07993.",
  "raw_value": "Billing Office: (856) 555-0138 or visit 210 Spring Street, Clearwater, NJ 07993.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_08 / full / deadline

```json
{
  "case": "case_08",
  "method": "full",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-05",
  "actual_scored_value": "November 5, 2026",
  "raw_value": "November 5, 2026",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": false,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "PAY BY NOVEMBER 5, 2026 TO AVOID A $5.00 LATE FEE.",
  "reason": "The value could not be checked against its source."
}
```

### case_09 / B1 / deadline

```json
{
  "case": "case_09",
  "method": "B1",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-06",
  "actual_scored_value": "Friday, November 6, 2026",
  "raw_value": "Friday, November 6, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_09 / B1 / required_action

```json
{
  "case": "case_09",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "actual_scored_value": "Return the signed permission slip and the $12.00 trip fee to Ms. Rivera. If your child is attending, also indicate permission for the trip.",
  "raw_value": "Return the signed permission slip and the $12.00 trip fee to Ms. Rivera. If your child is attending, also indicate permission for the trip.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_09 / B2 / deadline

```json
{
  "case": "case_09",
  "method": "B2",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-06",
  "actual_scored_value": "Friday, November 6, 2026",
  "raw_value": "Friday, November 6, 2026",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "reason": null
}
```

### case_09 / B2 / required_action

```json
{
  "case": "case_09",
  "method": "B2",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "actual_scored_value": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera",
  "raw_value": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "reason": null
}
```

### case_09 / full / deadline

```json
{
  "case": "case_09",
  "method": "full",
  "field": "deadline",
  "expected_state": "present",
  "expected": "2026-11-06",
  "actual_scored_value": "Friday, November 6, 2026",
  "raw_value": "Friday, November 6, 2026",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": true,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_09 / full / amount_due

```json
{
  "case": "case_09",
  "method": "full",
  "field": "amount_due",
  "expected_state": "present",
  "expected": "12.00",
  "actual_scored_value": "$12.00",
  "raw_value": "$12.00",
  "normalized_value": null,
  "status": "unverified",
  "wrong_under_frozen_scorer": false,
  "false_verified": false,
  "abstain_when_truth_exists": true,
  "source_snippet": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "reason": "The value could not be checked against its source."
}
```

### case_09 / full / required_action

```json
{
  "case": "case_09",
  "method": "full",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "actual_scored_value": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera",
  "raw_value": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": "Please return the signed permission slip and the $12.00 trip fee to Ms. Rivera by Friday, November 6, 2026.",
  "reason": "Matches the confirmed text. Check that this is the right fact on your original notice."
}
```

### case_10 / B1 / deadline

```json
{
  "case": "case_10",
  "method": "B1",
  "field": "deadline",
  "expected_state": "missing",
  "expected": null,
  "actual_scored_value": "Please contact the Attendance Office as soon as possible. Parent-teacher conferences will take place during the week of November 16–20, 2026.",
  "raw_value": "Please contact the Attendance Office as soon as possible. Parent-teacher conferences will take place during the week of November 16–20, 2026.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

### case_10 / B1 / required_action

```json
{
  "case": "case_10",
  "method": "B1",
  "field": "required_action",
  "expected_state": "present",
  "expected": "Please contact the Attendance Office as soon as possible to schedule a meeting.",
  "actual_scored_value": "Schedule a meeting with the Attendance Office and send a note for any absences with a medical or family reason so they can be excused.",
  "raw_value": "Schedule a meeting with the Attendance Office and send a note for any absences with a medical or family reason so they can be excused.",
  "normalized_value": null,
  "status": "verified",
  "wrong_under_frozen_scorer": true,
  "false_verified": true,
  "abstain_when_truth_exists": false,
  "source_snippet": null,
  "reason": null
}
```

## Interpretation retained from the original review

- case_03: the original OCR read $75.00 as $75.60 and the pipeline verified the wrong amount. This is a real numeric failure.
- case_04: the action dropped “You must”; the frozen strict scorer counts this wording difference. Weekday-prefixed dates also expose frozen canonicalizer limitations. Counts are preserved.
- cases_06 and 09: required actions dropped timing clauses and were verified. A separate date card does not undo those action failures.
- case_07: only the phone was returned, omitting the fuller keyed contact details. No fabricated phone is alleged.
- case_05: competing payment/appearance dates are marked ambiguous in the key. The full pipeline leaves its selected candidate unverified; it still counts wrong under the original ambiguous-value scoring.
- Source matching can repeat an OCR error. Unverified correct facts reduce usable coverage. Spanish and Tagalog each used English fallback in 3/10 original cases; mechanical translation checks are not native-speaker review.

## Provenance and commands

```sh
git status --short
git rev-parse HEAD
git rev-parse 'eval-freeze^{commit}'
cat eval/heldout-run-started.json
cat eval/freeze.json
cat results/heldout-protocol.json
```

No `python -m eval.run --set heldout` command was executed. No model call, image/OCR read, API-key access, tag movement, ledger reset, expected-answer edit or production change occurred. Original results and report hashes match their recorded protocol hashes.

Original raw JSON SHA-256: `f2187dcaaec2feb85b9bb4e5563c740490986f378b9eeecc46b5bd81f026a7e2`.

Authoritative artifacts: [raw frozen results](results/heldout-final.json), [original tables](results/heldout-final.md), [review](results/heldout-review.md), [provenance](results/heldout-protocol.json). The historical freeze manifest still says “not_started”; the separate ledger and completed report establish that this manifest status is stale. It was left unchanged.

Work stopped after Step 1 as requested. Steps 2–7 have not started.
