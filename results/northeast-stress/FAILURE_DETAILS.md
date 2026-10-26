# Full failure records

Original strict scores are retained; review notes do not change them. All content below is synthetic.

## CT_01 — degraded

[Input image](../../eval/northeast_stress/corpus/CT_01-degraded.jpg)

### Every strict field mismatch

**amount_due**: missing; false-verified=False

Expected: `45.00`

Observed: `None`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Hartford Parking Authority
PARKING NOTICE
Citation: DEMO-CT-001
Issued: October 26, 2026
Plate: DEMOCT / CT
Violation: Expired paid parking session
Fine: $45.00
Payment deadline: November 12, 2026
Hearing date: November 19, 2026 at 9:30 AM
Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to contest the citation.
A denied appeal may add a $15.00 hearing fee. This fee is not included in the current fine.
Questions: 860-757-0730.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VAUD -DO NOT PAY

breented case Cotets. No real dett or vencie.

HARTEORD PARKING AUTHORITY!

PARKING NOTICE

| Issued October 26, 2026 |
| bout : - DEMOCT/ CT
[Viotation Expired paid parking session

‘Fine = ~—~””—~SAHDSSC(CtC‘CSs~S

November 12, 2026

Hearing date November 19, 2026 at 9:30 AM

ee Ot

Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to

Payment deadline

contest the citation.
A denied appeal may add a $15.00 hearing fee. This fee is not included in the current fine.

Questions: 860-757-0730.

SYNTHETIC / CT_01 / SOFTWARE TEST ONLY

—.
ee
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "HARTEORD PARKING AUTHORITY",
      "source_snippet": "HARTEORD PARKING AUTHORITY!"
    },
    "deadline": {
      "value": "November 12, 2026",
      "source_snippet": "Payment deadline\n\nNovember 12, 2026",
      "kind": "absolute",
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to contest the citation.",
      "source_snippet": "Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to\n\ncontest the citation."
    },
    "contact": {
      "value": "860-757-0730",
      "source_snippet": "Questions: 860-757-0730."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "HARTEORD PARKING AUTHORITY",
        "source_snippet": "HARTEORD PARKING AUTHORITY!",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 86,
        "source_end": 113,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "November 12, 2026",
        "source_snippet": "Payment deadline\n\nNovember 12, 2026",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to contest the citation.",
        "source_snippet": "Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to\n\ncontest the citation.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "860-757-0730",
        "source_snippet": "Questions: 860-757-0730.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 561,
        "source_end": 585,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Required action: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 856,
      "output_tokens": 215,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "HARTEORD PARKING AUTHORITY",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "860-757-0730"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "HARTEORD PARKING AUTHORITY",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "860-757-0730"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "missing",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "HARTEORD PARKING AUTHORITY!",
    "deadline": "Payment deadline\n\nNovember 12, 2026",
    "amount_due": null,
    "required_action": "Pay the fine by November 12, 2026, or attend the scheduled hearing on November 19, 2026 at 9:30 AM to\n\ncontest the citation.",
    "contact": "Questions: 860-757-0730."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 692,
    "output_tokens": 213,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## CT_02 — clean

[Input image](../../eval/northeast_stress/corpus/CT_02-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-10`

Observed: `within 15 days of the ticket issue date`

**required_action**: verified; false-verified=True

Expected: `Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents.`

Observed: `Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.`

Review: Complete keyed action plus the printed mailing destination; strict scorer overcounts this as wrong.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of New Haven
PARKING NOTICE
Issue number: DEMO-CT-002
Ticket issued: October 26, 2026
Request type: Ticket review
Plate / State: TESTCT / CT
Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.
Explain why you believe the parking citation was issued in error and include supporting documents.
Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

CITY, OF NEW HAVEN)

PARKING NOTICE

Issue number DEMO-CT-002
Ticket issued October 26, 2026
Request type Ticket review
Plate / State TESTCT/CT

Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further
penalties while the review is pending.

Explain why you believe the parking citation was issued in error and include supporting documents.

Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.

SYNTHETIC / CT_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "City of New Haven",
      "source_snippet": "CITY, OF NEW HAVEN)"
    },
    "deadline": {
      "value": "within 15 days of the ticket issue date",
      "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
      "kind": "relative",
      "relative_days": 15,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Ticket issued October 26, 2026"
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
      "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further\npenalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507."
    },
    "contact": {
      "value": "City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507",
      "source_snippet": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "City of New Haven",
        "source_snippet": "CITY, OF NEW HAVEN)",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 89,
        "source_end": 108,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 15 days of the ticket issue date",
        "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 234,
        "source_end": 377,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
        "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further\npenalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 234,
        "source_end": 565,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507",
        "source_snippet": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 479,
        "source_end": 565,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 801,
      "output_tokens": 346,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Please double-check this with the agency.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Please double-check this with the agency.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
      "contact": "City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Please double-check this with the agency.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Please double-check this with the agency.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
      "contact": "City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "unverified",
    "deadline": "unverified",
    "amount_due": "missing",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITY, OF NEW HAVEN)",
    "deadline": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
    "amount_due": null,
    "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further\npenalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.",
    "contact": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 986,
    "output_tokens": 347,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## CT_02 — degraded

[Input image](../../eval/northeast_stress/corpus/CT_02-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-10`

Observed: `within 15 days of the ticket issue date`

**required_action**: verified; false-verified=True

Expected: `Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents.`

Observed: `Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,`

Review: Complete keyed action plus printed mailing destination, with final comma instead of period.

**contact**: missing; false-verified=False

Expected: `City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.`

Observed: `None`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of New Haven
PARKING NOTICE
Issue number: DEMO-CT-002
Ticket issued: October 26, 2026
Request type: Ticket review
Plate / State: TESTCT / CT
Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.
Explain why you believe the parking citation was issued in error and include supporting documents.
Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507.
```

### Full OCR text

```text
SYNTHETIC TEST -NOT VALIO - 00 NOT PAY

tveried case Ceteis. No real debt or vehucie.

[issue number

| Plate / State _

| Ticket issued a
Request type _ 7 ric
L

“DEMO-CT-00220202@€©€©60602.~C¢0~—~C———CS |

October 26, 2026

Ticket review

TESTCT/CT

Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further

penalties while the review is pending.

Explain why you believe the parking citation was issued in error and include supporting documents.

Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,

, SYNTHETIC / CT_02/ SOFTWARE TEST ONLY

a
——.
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "City of New Haven Parking Violation Center",
      "source_snippet": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,"
    },
    "deadline": {
      "value": "within 15 days of the ticket issue date",
      "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
      "kind": "relative",
      "relative_days": 15,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "October 26, 2026"
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
      "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,"
    },
    "contact": {
      "value": null,
      "source_snippet": null
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "City of New Haven Parking Violation Center",
        "source_snippet": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 498,
        "source_end": 584,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 15 days of the ticket issue date",
        "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 252,
        "source_end": 396,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
        "source_snippet": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 252,
        "source_end": 584,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 834,
      "output_tokens": 319,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,"
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice.",
      "Contact: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "City of New Haven Parking Violation Center",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
      "contact": "Contact: Not found. Check the original notice."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,"
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice.",
      "Contact: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "City of New Haven Parking Violation Center",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending. Explain why you believe the parking citation was issued in error and include supporting documents. Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
      "contact": "Contact: Not found. Check the original notice."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "missing",
    "required_action": "verified",
    "contact": "missing"
  },
  "original_snippets": {
    "issuing_agency": "Mail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
    "deadline": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.",
    "amount_due": null,
    "required_action": "Submit this review form with the parking ticket within 15 days of the ticket issue date to pause further penalties while the review is pending.\n\nExplain why you believe the parking citation was issued in error and include supporting documents.\n\nMail to: City of New Haven Parking Violation Center, PO Box 1941, New Haven, CT 06507,",
    "contact": null
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 953,
    "output_tokens": 330,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## MA_01 — clean

[Input image](../../eval/northeast_stress/corpus/MA_01-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-05`

Observed: `within 10 days of the date of this decision`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Boston Parking Clerk
PARKING NOTICE
Parking ticket: DEMO-MA-001
Original issue date: October 1, 2026
Date of this decision: October 26, 2026
Fine remaining: $50.00
Your parking ticket appeal has been denied.
Pay the fine or request a hearing within 10 days of the date of this decision.
Questions and hearing requests: 617-635-4410.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

‘CITYLORK,BOSTO 4

[PARKING NOTICE

Parking ticket: DEMO-MA-001
Onzginal issue date: October 1, 2026
Date of this decision: October 26, 2026

Fine remaining: $50.00

Your parking ticket appeal has been denied.
Pay the fine or request a hearing within 10 days of the date of this decision.

Questions and hearing requests: 617-635-4410.

SYNTHETIC / MA_01/ SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITYLORK,BOSTO 4",
      "source_snippet": "CITYLORK,BOSTO 4"
    },
    "deadline": {
      "value": "within 10 days of the date of this decision",
      "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "kind": "relative",
      "relative_days": 10,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Date of this decision: October 26, 2026"
    },
    "amount_due": {
      "value": "$50.00",
      "source_snippet": "Fine remaining: $50.00"
    },
    "required_action": {
      "value": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision."
    },
    "contact": {
      "value": "617-635-4410",
      "source_snippet": "Questions and hearing requests: 617-635-4410."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITYLORK,BOSTO 4",
        "source_snippet": "CITYLORK,BOSTO 4",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 90,
        "source_end": 106,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 10 days of the date of this decision",
        "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 299,
        "source_end": 377,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$50.00",
        "source_snippet": "Fine remaining: $50.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 231,
        "source_end": 253,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 299,
        "source_end": 377,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "617-635-4410",
        "source_snippet": "Questions and hearing requests: 617-635-4410.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 379,
        "source_end": 424,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 785,
      "output_tokens": 219,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 10 days of the date of this decision."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITYLORK,BOSTO 4",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "contact": "617-635-4410"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 10 days of the date of this decision."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITYLORK,BOSTO 4",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "contact": "617-635-4410"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITYLORK,BOSTO 4",
    "deadline": "Pay the fine or request a hearing within 10 days of the date of this decision.",
    "amount_due": "Fine remaining: $50.00",
    "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
    "contact": "Questions and hearing requests: 617-635-4410."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 743,
    "output_tokens": 214,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## MA_01 — degraded

[Input image](../../eval/northeast_stress/corpus/MA_01-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-05`

Observed: `within 10 days of the date of this decision`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Boston Parking Clerk
PARKING NOTICE
Parking ticket: DEMO-MA-001
Original issue date: October 1, 2026
Date of this decision: October 26, 2026
Fine remaining: $50.00
Your parking ticket appeal has been denied.
Pay the fine or request a hearing within 10 days of the date of this decision.
Questions and hearing requests: 617-635-4410.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

bverted case Cetais. No real debt or vehucie.

CTTN OE. BOSTON PARKING CLERK’

|
|
!
. |

Paking ticket: DEMO-MA-001
Onginal tssue date: October 1, 2026
Date of this decision: October 26, 2026

Fine remaining: $50.00

Your parking ticket appeal has been denied.
Pay the fine or request a hearing within 10 days of the date of this decision.
{

Questions and hearing requests: 617-635-4410.
|

, SYNTHETIC / MA_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "BOSTON PARKING CLERK",
      "source_snippet": "CTTN OE. BOSTON PARKING CLERK’"
    },
    "deadline": {
      "value": "within 10 days of the date of this decision",
      "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "kind": "relative",
      "relative_days": 10,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Date of this decision: October 26, 2026"
    },
    "amount_due": {
      "value": "$50.00",
      "source_snippet": "Fine remaining: $50.00"
    },
    "required_action": {
      "value": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision."
    },
    "contact": {
      "value": "617-635-4410",
      "source_snippet": "Questions and hearing requests: 617-635-4410."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "BOSTON PARKING CLERK",
        "source_snippet": "CTTN OE. BOSTON PARKING CLERK’",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 118,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 10 days of the date of this decision",
        "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 303,
        "source_end": 381,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$50.00",
        "source_snippet": "Fine remaining: $50.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 235,
        "source_end": 257,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "source_snippet": "Pay the fine or request a hearing within 10 days of the date of this decision.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 303,
        "source_end": 381,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "617-635-4410",
        "source_snippet": "Questions and hearing requests: 617-635-4410.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 385,
        "source_end": 430,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 792,
      "output_tokens": 224,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 10 days of the date of this decision."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "BOSTON PARKING CLERK",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "contact": "617-635-4410"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 10 days of the date of this decision."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "BOSTON PARKING CLERK",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
      "contact": "617-635-4410"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CTTN OE. BOSTON PARKING CLERK’",
    "deadline": "Pay the fine or request a hearing within 10 days of the date of this decision.",
    "amount_due": "Fine remaining: $50.00",
    "required_action": "Pay the fine or request a hearing within 10 days of the date of this decision.",
    "contact": "Questions and hearing requests: 617-635-4410."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 748,
    "output_tokens": 214,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## MA_02 — clean

[Input image](../../eval/northeast_stress/corpus/MA_02-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-16`

Observed: `within 21 days of the issue date`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Cambridge Department of Transportation
PARKING NOTICE
Ticket: DEMO-MA-002
Issue date: October 26, 2026
Plate: DEMOMA / MA
Violation: Expired meter
Fine now: $40.00
First late fee: $5.00
Second late fee: $10.00
Third late fee: $40.00
Pay the fine or dispute this parking ticket within 21 days of the issue date.
Card payments have a separate 2.95% service fee, with a minimum of $2.25.
Questions: 617-349-4700.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

Ticket DEMO-MA-002
issue date October 26, 2026
Plate DEMOMA / MA
Violation Expired meter
Fine now $40.00

First late fee $5.00

Second late fee $10.00

Third late fee $40.00

Pay the fine or dispute this parking ticket within 21 days of the issue date.
Card payments have a separate 2.95% service fee, with a minimum of $2.25.

Questions: 617-349-4700.

SYNTHETIC / MA_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": null,
      "source_snippet": null
    },
    "deadline": {
      "value": "within 21 days of the issue date",
      "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "kind": "relative",
      "relative_days": 21,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "issue date October 26, 2026"
    },
    "amount_due": {
      "value": "$40.00",
      "source_snippet": "Fine now $40.00"
    },
    "required_action": {
      "value": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    },
    "contact": {
      "value": "617-349-4700",
      "source_snippet": "Questions: 617-349-4700."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 21 days of the issue date",
        "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 264,
        "source_end": 341,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$40.00",
        "source_snippet": "Fine now $40.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 178,
        "source_end": 193,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 264,
        "source_end": 341,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "617-349-4700",
        "source_snippet": "Questions: 617-349-4700.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 417,
        "source_end": 441,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 795,
      "output_tokens": 192,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "contact": "617-349-4700"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "contact": "617-349-4700"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "missing",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": null,
    "deadline": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
    "amount_due": "Fine now $40.00",
    "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
    "contact": "Questions: 617-349-4700."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 724,
    "output_tokens": 227,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## MA_02 — degraded

[Input image](../../eval/northeast_stress/corpus/MA_02-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-16`

Observed: `within 21 days of the issue date`

**amount_due**: missing; false-verified=False

Expected: `40.00`

Observed: `None`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Cambridge Department of Transportation
PARKING NOTICE
Ticket: DEMO-MA-002
Issue date: October 26, 2026
Plate: DEMOMA / MA
Violation: Expired meter
Fine now: $40.00
First late fee: $5.00
Second late fee: $10.00
Third late fee: $40.00
Pay the fine or dispute this parking ticket within 21 days of the issue date.
Card payments have a separate 2.95% service fee, with a minimum of $2.25.
Questions: 617-349-4700.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - 00 NOT PAY

tverted case Cetets. No real dett or vehucte.

OFRAJTRANSPORTATION

CITY OF CAMBRIDGE DEPARTMEN

[Ticket DEMO-NAOO2

[wea QQ tober 26,2026 2«@2~C~*~*~—C—~—~—~—~—
[Pate ~~~~~—~—~—~—~—~—CiEMOMATMA
; Violation Expired meter
———— — QD
[Firstlatefee | $500 ~~

| Third tate fee — “$40000022@2«27~CO~™*” a

Pay the fine or dispute this parking ticket within 21 days of the issue date.

Card payments have a separate 2.95% service feo, with a minimum of $2.25.

Questions: 617-349-4700.
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITY OF CAMBRIDGE DEPARTMEN",
      "source_snippet": "CITY OF CAMBRIDGE DEPARTMEN"
    },
    "deadline": {
      "value": "within 21 days of the issue date",
      "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "kind": "relative",
      "relative_days": 21,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    },
    "contact": {
      "value": "617-349-4700",
      "source_snippet": "Questions: 617-349-4700."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITY OF CAMBRIDGE DEPARTMEN",
        "source_snippet": "CITY OF CAMBRIDGE DEPARTMEN",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 109,
        "source_end": 136,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 21 days of the issue date",
        "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 342,
        "source_end": 419,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "source_snippet": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 342,
        "source_end": 419,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "617-349-4700",
        "source_snippet": "Questions: 617-349-4700.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 496,
        "source_end": 520,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 849,
      "output_tokens": 183,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY OF CAMBRIDGE DEPARTMEN",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "contact": "617-349-4700"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or dispute this parking ticket within 21 days of the issue date."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY OF CAMBRIDGE DEPARTMEN",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
      "contact": "617-349-4700"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "missing",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITY OF CAMBRIDGE DEPARTMEN",
    "deadline": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
    "amount_due": null,
    "required_action": "Pay the fine or dispute this parking ticket within 21 days of the issue date.",
    "contact": "Questions: 617-349-4700."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 735,
    "output_tokens": 212,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## ME_01 — clean

[Input image](../../eval/northeast_stress/corpus/ME_01-clean.png)

### Every strict field mismatch

**required_action**: verified; false-verified=True

Expected: `Pay the parking fine using the ticket number and vehicle registration.`

Observed: `Pay the parking tine using the ticket number and vehicle registraticn.`

Review: OCR changed fine to tine and registration to registraticn; copied as verified.

**contact**: verified; false-verified=True

Expected: `jmaloy@freeportmaine.com`

Observed: `jmaloy@freeportmaine.ccm`

Review: The email ends in .ccm instead of the printed .com. It is also displayed in the English explanation.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Freeport Police Department
PARKING NOTICE
TICKET NUMBER: DEMO-ME-001
REGISTRATION: DEMOME / ME
Registration expires: April 30, 2027
Issued: 10/26/2026
Violation: Overtime parking
Fine: $30.00
Pay the parking fine using the ticket number and vehicle registration.
For help: jmaloy@freeportmaine.com
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetais No real debt or vehicle.

FREEPORTAPOLICEEDEPARTMENT,

[PARK INGENOTICE]

TICKET NUMBER: CEMO-ME-C91

REGISTRATION: DEMOME / ME

Registration expires: April 3C, 2027

Issucd: 10/26/2026

Violation: Overtime parking

Fine: $30.00

Pay the parking tine using the ticket number
and vehicle registraticn.

For helo: jmaloy@freeportmaine.ccm

SYNTHETIC / ME_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "FREEPORTAPOLICEEDEPARTMENT",
      "source_snippet": "FREEPORTAPOLICEEDEPARTMENT,"
    },
    "deadline": {
      "value": null,
      "source_snippet": null,
      "kind": null,
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$30.00",
      "source_snippet": "Fine: $30.00"
    },
    "required_action": {
      "value": "Pay the parking tine using the ticket number and vehicle registraticn.",
      "source_snippet": "Pay the parking tine using the ticket number\nand vehicle registraticn."
    },
    "contact": {
      "value": "jmaloy@freeportmaine.ccm",
      "source_snippet": "For helo: jmaloy@freeportmaine.ccm"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "FREEPORTAPOLICEEDEPARTMENT",
        "source_snippet": "FREEPORTAPOLICEEDEPARTMENT,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 115,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$30.00",
        "source_snippet": "Fine: $30.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 278,
        "source_end": 290,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the parking tine using the ticket number and vehicle registraticn.",
        "source_snippet": "Pay the parking tine using the ticket number\nand vehicle registraticn.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 292,
        "source_end": 362,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "jmaloy@freeportmaine.ccm",
        "source_snippet": "For helo: jmaloy@freeportmaine.ccm",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 364,
        "source_end": 398,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 785,
      "output_tokens": 172,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the parking tine using the ticket number and vehicle registraticn."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "FREEPORTAPOLICEEDEPARTMENT",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the parking tine using the ticket number and vehicle registraticn.",
      "contact": "jmaloy@freeportmaine.ccm"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the parking tine using the ticket number and vehicle registraticn."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "FREEPORTAPOLICEEDEPARTMENT",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the parking tine using the ticket number and vehicle registraticn.",
      "contact": "jmaloy@freeportmaine.ccm"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "missing",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "FREEPORTAPOLICEEDEPARTMENT,",
    "deadline": null,
    "amount_due": "Fine: $30.00",
    "required_action": "Pay the parking tine using the ticket number\nand vehicle registraticn.",
    "contact": "For helo: jmaloy@freeportmaine.ccm"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 735,
    "output_tokens": 209,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## ME_02 — clean

[Input image](../../eval/northeast_stress/corpus/ME_02-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `None`

Observed: `within 72 hours of issuance, excluding Saturday and Sunday`

**required_action**: verified; false-verified=True

Expected: `Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order. No debit or credit cards are accepted. Do not mail cash.`

Observed: `Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash.`

Review: OCR changed money to moncy; constraints are otherwise retained.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Maine Capitol Police
PARKING NOTICE
Ticket: DEMO-ME-002
Issued: October 23, 2026 at 9:00 AM
Plate: DEMO72 / ME
Fine: $20.00
Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.
No debit or credit cards are accepted. Do not mail cash.
Questions: 207-287-4357.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

Ticket: DEMO-ME-002

Issued: October 23, 2026 at 9:00 AM
Plate: DEMO72 / ME

Fine: $20.00

Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.
No debit or credit cards are accepted. Do not mail cash.

Questions: 207-287-4357.

SYNTHETIC / ME_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": null,
      "source_snippet": null
    },
    "deadline": {
      "value": "within 72 hours of issuance, excluding Saturday and Sunday",
      "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.",
      "kind": "relative",
      "relative_days": 72,
      "anchor_date": "October 23, 2026",
      "anchor_source_snippet": "Issued: October 23, 2026 at 9:00 AM"
    },
    "amount_due": {
      "value": "$20.00",
      "source_snippet": "Fine: $20.00"
    },
    "required_action": {
      "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash.",
      "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.\nNo debit or credit cards are accepted. Do not mail cash."
    },
    "contact": {
      "value": "207-287-4357",
      "source_snippet": "Questions: 207-287-4357."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 72 hours of issuance, excluding Saturday and Sunday",
        "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 180,
        "source_end": 283,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$20.00",
        "source_snippet": "Fine: $20.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 166,
        "source_end": 178,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash.",
        "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.\nNo debit or credit cards are accepted. Do not mail cash.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 180,
        "source_end": 340,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "207-287-4357",
        "source_snippet": "Questions: 207-287-4357.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 342,
        "source_end": 366,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 773,
      "output_tokens": 249,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash.",
      "contact": "207-287-4357"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order. No debit or credit cards are accepted. Do not mail cash.",
      "contact": "207-287-4357"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "missing",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": null,
    "deadline": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.",
    "amount_due": "Fine: $20.00",
    "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or moncy order.\nNo debit or credit cards are accepted. Do not mail cash.",
    "contact": "Questions: 207-287-4357."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 805,
    "output_tokens": 267,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## ME_02 — degraded

[Input image](../../eval/northeast_stress/corpus/ME_02-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `None`

Observed: `Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.`

**required_action**: verified; false-verified=True

Expected: `Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order. No debit or credit cards are accepted. Do not mail cash.`

Observed: `Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.`

Review: Verified action omits the printed no-cards and do-not-mail-cash sentences. The money-order option remains, but the mailing restriction is lost.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Maine Capitol Police
PARKING NOTICE
Ticket: DEMO-ME-002
Issued: October 23, 2026 at 9:00 AM
Plate: DEMO72 / ME
Fine: $20.00
Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.
No debit or credit cards are accepted. Do not mail cash.
Questions: 207-287-4357.
```

### Full OCR text

```text
SYNTHETIC TEST -NOT VALID -D0 NOT PAY

invented case cotats. No real dett of vehicle.

RIAINECAPITOOPOLICH
(PARKING NOTICE

Ticket: DEMO-ME-002

Issued: October 23, 2026 at 9:00 AM
Plate: DEMO72 / ME

Fine: $20.00

Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.

No debit or credit cards are accepted. Do not mail cash.

|

Questions: 207-287-4357. |
|

f
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "RIAINECAPITOOPOLICH",
      "source_snippet": "RIAINECAPITOOPOLICH\n(PARKING NOTICE"
    },
    "deadline": {
      "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
      "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
      "kind": "relative",
      "relative_days": 72,
      "anchor_date": "October 23, 2026",
      "anchor_source_snippet": "Issued: October 23, 2026 at 9:00 AM"
    },
    "amount_due": {
      "value": "$20.00",
      "source_snippet": "Fine: $20.00"
    },
    "required_action": {
      "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
      "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order."
    },
    "contact": {
      "value": "207-287-4357",
      "source_snippet": "Questions: 207-287-4357."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "RIAINECAPITOOPOLICH",
        "source_snippet": "RIAINECAPITOOPOLICH\n(PARKING NOTICE",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 87,
        "source_end": 122,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
        "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 215,
        "source_end": 318,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$20.00",
        "source_snippet": "Fine: $20.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 201,
        "source_end": 213,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
        "source_snippet": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 215,
        "source_end": 318,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "207-287-4357",
        "source_snippet": "Questions: 207-287-4357.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 381,
        "source_end": 405,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 776,
      "output_tokens": 248,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "RIAINECAPITOOPOLICH",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
      "contact": "207-287-4357"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "RIAINECAPITOOPOLICH",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
      "contact": "207-287-4357"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "RIAINECAPITOOPOLICH\n(PARKING NOTICE",
    "deadline": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
    "amount_due": "Fine: $20.00",
    "required_action": "Pay the fine within 72 hours of issuance, excluding Saturday and Sunday, by cash, check or money order.",
    "contact": "Questions: 207-287-4357."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 762,
    "output_tokens": 223,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NH_01 — clean

[Input image](../../eval/northeast_stress/corpus/NH_01-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `None`

Observed: `within 21 business days`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Nashua Parking Department
PARKING NOTICE
Citation: DEMO-NH-001
Citation date: October 20, 2026
Request received: October 26, 2026
Review status: Pending
Keep your appeal confirmation while the administrative review is pending.
The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.
Questions: parking@nashuanh.gov
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

CITY, OF, NASHUA PARKING DEPARTMENT,

PARKING NOTICE

Citation DEMO-NH-001
Citation date October 20, 2026
Request received October 26, 2026
Review status Pending

Keep your appeal confirmation while the administrative review is pending.

The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision
will explain your options.

Questions: parking@nashuanh.gov

SYNTHETIC / NH_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITY, OF, NASHUA PARKING DEPARTMENT",
      "source_snippet": "CITY, OF, NASHUA PARKING DEPARTMENT,"
    },
    "deadline": {
      "value": "within 21 business days",
      "source_snippet": "The Parking Department will respond within 21 business days.",
      "kind": "relative",
      "relative_days": 21,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Keep your appeal confirmation while the administrative review is pending.",
      "source_snippet": "Keep your appeal confirmation while the administrative review is pending."
    },
    "contact": {
      "value": "parking@nashuanh.gov",
      "source_snippet": "Questions: parking@nashuanh.gov"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITY, OF, NASHUA PARKING DEPARTMENT",
        "source_snippet": "CITY, OF, NASHUA PARKING DEPARTMENT,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 89,
        "source_end": 125,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 21 business days",
        "source_snippet": "The Parking Department will respond within 21 business days.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 327,
        "source_end": 387,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Keep your appeal confirmation while the administrative review is pending.",
        "source_snippet": "Keep your appeal confirmation while the administrative review is pending.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 252,
        "source_end": 325,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "parking@nashuanh.gov",
        "source_snippet": "Questions: parking@nashuanh.gov",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 463,
        "source_end": 494,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 781,
      "output_tokens": 167,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Keep your appeal confirmation while the administrative review is pending."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY, OF, NASHUA PARKING DEPARTMENT",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Keep your appeal confirmation while the administrative review is pending.",
      "contact": "parking@nashuanh.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Keep your appeal confirmation while the administrative review is pending."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY, OF, NASHUA PARKING DEPARTMENT",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Keep your appeal confirmation while the administrative review is pending.",
      "contact": "parking@nashuanh.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "missing",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITY, OF, NASHUA PARKING DEPARTMENT,",
    "deadline": "The Parking Department will respond within 21 business days.",
    "amount_due": null,
    "required_action": "Keep your appeal confirmation while the administrative review is pending.",
    "contact": "Questions: parking@nashuanh.gov"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 720,
    "output_tokens": 203,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NH_01 — degraded

[Input image](../../eval/northeast_stress/corpus/NH_01-degraded.jpg)

### Every strict field mismatch

**required_action**: verified; false-verified=True

Expected: `Keep your appeal confirmation while the administrative review is pending.`

Observed: `Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.`

Review: Adds the printed agency-response timeline and possible later decision; no invented resident deadline in this action.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Nashua Parking Department
PARKING NOTICE
Citation: DEMO-NH-001
Citation date: October 20, 2026
Request received: October 26, 2026
Review status: Pending
Keep your appeal confirmation while the administrative review is pending.
The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.
Questions: parking@nashuanh.gov
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALIO - 00 NOT PAY

twverted case cetais. No real debt or vehucie.

CITY, OF, NASHUA PARKING DEPAR

PARKING NOTICE

fr Citation FT EMONHOOI

|

October 20, 2026

Citation date

October 26, 2026

| Request received

‘

| Review status Pending

Keep your appeal confirmation while the administrative review is pending.
The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision

will explain your options.

Questions: parking@nashuanh.gov

Te ee.
Sa
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITY, OF, NASHUA PARKING DEPAR",
      "source_snippet": "CITY, OF, NASHUA PARKING DEPAR"
    },
    "deadline": {
      "value": null,
      "source_snippet": null,
      "kind": null,
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": null,
      "source_snippet": null
    },
    "required_action": {
      "value": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
      "source_snippet": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options."
    },
    "contact": {
      "value": "parking@nashuanh.gov",
      "source_snippet": "Questions: parking@nashuanh.gov"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITY, OF, NASHUA PARKING DEPAR",
        "source_snippet": "CITY, OF, NASHUA PARKING DEPAR",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 89,
        "source_end": 119,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
        "source_snippet": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 264,
        "source_end": 473,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "parking@nashuanh.gov",
        "source_snippet": "Questions: parking@nashuanh.gov",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 475,
        "source_end": 506,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 782,
      "output_tokens": 204,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY, OF, NASHUA PARKING DEPAR",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
      "contact": "parking@nashuanh.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Not found. Check the original notice.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Not found. Check the original notice."
    ],
    "cards": {
      "issuing_agency": "CITY, OF, NASHUA PARKING DEPAR",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Not found. Check the original notice.",
      "required_action": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
      "contact": "parking@nashuanh.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "missing",
    "amount_due": "missing",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITY, OF, NASHUA PARKING DEPAR",
    "deadline": null,
    "amount_due": null,
    "required_action": "Keep your appeal confirmation while the administrative review is pending. The Parking Department will respond within 21 business days. If the citation is upheld, a separate decision will explain your options.",
    "contact": "Questions: parking@nashuanh.gov"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 818,
    "output_tokens": 253,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NH_02 — clean

[Input image](../../eval/northeast_stress/corpus/NH_02-clean.png)

### Every strict field mismatch

**contact**: verified; false-verified=True

Expected: `603-640-3220`

Observed: `Questions: 603-640-3220.`

Review: Correct phone digits with the printed Questions label. Strict mismatch, not a wrong number.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Town of Hanover Parking Division
PARKING NOTICE
Ticket: DEMO-NH-002
Fine date: 10/26/2026
Plate: DEMONH / NH
Current fine: $30.00
First late fee after 14 days: $20.00
Additional late fee after 28 days: $40.00
Respond by: November 9, 2026
Pay this fine or file an appeal by November 9, 2026.
Use the ticket number and license plate to find this citation in the parking portal.
Questions: 603-640-3220.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

TOWN OF HANOVER PARKING DIVISION

Ticket DEMO-NH-002
Fine date 10/26/2026

Plate DEMONH / NH
Current fine $30.00

First late fee after 14 days $20.00

Additional late fee after 28 days $40.00

Respond by November 9, 2026

Pay this fine or file an appeal by November 9, 2026.
Use the ticket number and license plate to find this citation in the parking portal.

Questions: 603-640-3220.

SYNTHETIC / NH_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "TOWN OF HANOVER PARKING DIVISION",
      "source_snippet": "TOWN OF HANOVER PARKING DIVISION"
    },
    "deadline": {
      "value": "November 9, 2026",
      "source_snippet": "Respond by November 9, 2026",
      "kind": "absolute",
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$30.00",
      "source_snippet": "Current fine $30.00"
    },
    "required_action": {
      "value": "Pay this fine or file an appeal by November 9, 2026.",
      "source_snippet": "Pay this fine or file an appeal by November 9, 2026."
    },
    "contact": {
      "value": "Questions: 603-640-3220.",
      "source_snippet": "Questions: 603-640-3220."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "TOWN OF HANOVER PARKING DIVISION",
        "source_snippet": "TOWN OF HANOVER PARKING DIVISION",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 89,
        "source_end": 121,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "November 9, 2026",
        "source_snippet": "Respond by November 9, 2026",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 282,
        "source_end": 309,
        "normalized_value": "2026-11-09",
        "days_remaining": 14,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$30.00",
        "source_snippet": "Current fine $30.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 182,
        "source_end": 201,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay this fine or file an appeal by November 9, 2026.",
        "source_snippet": "Pay this fine or file an appeal by November 9, 2026.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 311,
        "source_end": 363,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "Questions: 603-640-3220.",
        "source_snippet": "Questions: 603-640-3220.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 450,
        "source_end": 474,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 804,
      "output_tokens": 187,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay this fine or file an appeal by November 9, 2026."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "TOWN OF HANOVER PARKING DIVISION",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay this fine or file an appeal by November 9, 2026.",
      "contact": "Questions: 603-640-3220."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay this fine or file an appeal by November 9, 2026."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "TOWN OF HANOVER PARKING DIVISION",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay this fine or file an appeal by November 9, 2026.",
      "contact": "Questions: 603-640-3220."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "TOWN OF HANOVER PARKING DIVISION",
    "deadline": "Respond by November 9, 2026",
    "amount_due": "Current fine $30.00",
    "required_action": "Pay this fine or file an appeal by November 9, 2026.",
    "contact": "Questions: 603-640-3220."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 757,
    "output_tokens": 203,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NY_01 — clean

[Input image](../../eval/northeast_stress/corpus/NY_01-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-25`

Observed: `within 3C days after the ticket was issued`

**required_action**: verified; false-verified=True

Expected: `Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.`

Observed: `Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties.`

Review: Verified action says 3C days instead of 30. The separate deadline field is unverified, but that does not suppress this action.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
New York City Department of Finance
PARKING NOTICE
Violation number: DEMO-NY-001
Plate / State: DEMONY / NY
Registration expires: 12/31/2027
Issue date: October 26, 2026
Time: 10:42 AM
Location: 100 Example Street
Violation: Expired meter
Fine: $65.00
Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.
Questions: NYC Department of Finance, 311.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetais No real debt or vehicle.

NEWRY ORKECITYBDEPARTMENTBOEME INANCE,

[PARK INGENOTICE]

Violation number: DEMO-NY-001
Plate / State: CEMONY / NY
Registration expires: 12/31/2C27
Issuc date: October 26, 2926
Time: 10:47 AM

Location: 100 Example Street
Violation: Expired meter

Fine: $65.00

Pay the fine or request a hearing within 3C
days after the ticket was issued to avoid late
penalties.

Questions: NYC Department of Finance, 311.

SYNTHETIC / NY_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE",
      "source_snippet": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE,"
    },
    "deadline": {
      "value": "within 3C days after the ticket was issued",
      "source_snippet": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties.",
      "kind": "relative",
      "relative_days": null,
      "anchor_date": "October 26, 2926",
      "anchor_source_snippet": "Issuc date: October 26, 2926"
    },
    "amount_due": {
      "value": "$65.00",
      "source_snippet": "Fine: $65.00"
    },
    "required_action": {
      "value": "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties.",
      "source_snippet": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties."
    },
    "contact": {
      "value": "NYC Department of Finance, 311.",
      "source_snippet": "Questions: NYC Department of Finance, 311."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE",
        "source_snippet": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 126,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 3C days after the ticket was issued",
        "source_snippet": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 351,
        "source_end": 452,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$65.00",
        "source_snippet": "Fine: $65.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 337,
        "source_end": 349,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties.",
        "source_snippet": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 351,
        "source_end": 452,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "NYC Department of Finance, 311.",
        "source_snippet": "Questions: NYC Department of Finance, 311.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 454,
        "source_end": 496,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 812,
      "output_tokens": 248,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties.",
      "contact": "NYC Department of Finance, 311."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or request a hearing within 3C days after the ticket was issued to avoid late penalties.",
      "contact": "NYC Department of Finance, 311."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "NEWRY ORKECITYBDEPARTMENTBOEME INANCE,",
    "deadline": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties.",
    "amount_due": "Fine: $65.00",
    "required_action": "Pay the fine or request a hearing within 3C\ndays after the ticket was issued to avoid late\npenalties.",
    "contact": "Questions: NYC Department of Finance, 311."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 784,
    "output_tokens": 230,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NY_01 — degraded

[Input image](../../eval/northeast_stress/corpus/NY_01-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-25`

Observed: `within 30 days after the ticket was issued`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
New York City Department of Finance
PARKING NOTICE
Violation number: DEMO-NY-001
Plate / State: DEMONY / NY
Registration expires: 12/31/2027
Issue date: October 26, 2026
Time: 10:42 AM
Location: 100 Example Street
Violation: Expired meter
Fine: $65.00
Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.
Questions: NYC Department of Finance, 311.
```

### Full OCR text

```text
. oe oe ee -
SYNTHETIC TEST -NOT VAUD - DO NOT PAY

Invented case coisas. No real ded! or vehicie.

PPARKINGENOT ICE}

Violation number: CDEMO-NY-0901

Plate / State: DEMONY / NY
Registration expires: 12/31/2027

Issue date: October 26, 2026
Time: 10:42 AM

Location: 100 Example Street

Violation: Expired meter
|

Fine: $65.00

|
Pay the fine or request a hearing within 30 |
days after the ticket was issued to avoid late |

t

penalties.
Questions: NYC Department of Finance, 311.

.
, SYNTHETIC / NY_01/ SOFTWARE TEST ONLY

en TT a
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "NYC Department of Finance",
      "source_snippet": "Questions: NYC Department of Finance, 311."
    },
    "deadline": {
      "value": "within 30 days after the ticket was issued",
      "source_snippet": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
      "kind": "relative",
      "relative_days": 30,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Issue date: October 26, 2026"
    },
    "amount_due": {
      "value": "$65.00",
      "source_snippet": "Fine: $65.00"
    },
    "required_action": {
      "value": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
      "source_snippet": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties."
    },
    "contact": {
      "value": "311",
      "source_snippet": "Questions: NYC Department of Finance, 311."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "NYC Department of Finance",
        "source_snippet": "Questions: NYC Department of Finance, 311.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 442,
        "source_end": 484,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 30 days after the ticket was issued",
        "source_snippet": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$65.00",
        "source_snippet": "Fine: $65.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 316,
        "source_end": 328,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
        "source_snippet": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "311",
        "source_snippet": "Questions: NYC Department of Finance, 311.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 442,
        "source_end": 484,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Required action: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 812,
      "output_tokens": 214,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "NYC Department of Finance",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "311"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "NYC Department of Finance",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "311"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "Questions: NYC Department of Finance, 311.",
    "deadline": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
    "amount_due": "Fine: $65.00",
    "required_action": "Pay the fine or request a hearing within 30 days after the ticket was issued to avoid late penalties.",
    "contact": "Questions: NYC Department of Finance, 311."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 681,
    "output_tokens": 206,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## NY_02 — clean

[Input image](../../eval/northeast_stress/corpus/NY_02-clean.png)

### Every strict field mismatch

**required_action**: unverified; false-verified=False

Expected: `Pay $35.00 by November 20, 2026 using the City of Kingston parking ticket service.`

Observed: `Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Kingston
PARKING NOTICE
Notice: DEMO-NY-002
Statement date: October 26, 2026
Registration expires: April 30, 2027
Parking fine: $35.00
Pay by: November 20, 2026
Pay $35.00 by November 20, 2026 using the City of Kingston parking ticket service.
This notice concerns a City of Kingston parking citation.
Questions: 845-331-0080.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

ICITYIOR, KINGSTON)
PARKING NOTICE

Notice: DEMO-NY-002

Statement date: October 26, 2026
Registration expires: April 30, 2027
Parking fine: $35.00

Pay by: November 20, 2026

Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.
This notice concems a City of Kingston parking citation.

Questions: 845-331-0080.

SYNTHETIC / NY_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "City of Kingston",
      "source_snippet": "This notice concems a City of Kingston parking citation."
    },
    "deadline": {
      "value": "November 20, 2026",
      "source_snippet": "Pay by: November 20, 2026",
      "kind": "absolute",
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$35.00",
      "source_snippet": "Parking fine: $35.00"
    },
    "required_action": {
      "value": "Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.",
      "source_snippet": "Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service."
    },
    "contact": {
      "value": "845-331-0080",
      "source_snippet": "Questions: 845-331-0080."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "City of Kingston",
        "source_snippet": "This notice concems a City of Kingston parking citation.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 347,
        "source_end": 403,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "November 20, 2026",
        "source_snippet": "Pay by: November 20, 2026",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 238,
        "source_end": 263,
        "normalized_value": "2026-11-20",
        "days_remaining": 25,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$35.00",
        "source_snippet": "Parking fine: $35.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 216,
        "source_end": 236,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.",
        "source_snippet": "Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 265,
        "source_end": 346,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "845-331-0080",
        "source_snippet": "Questions: 845-331-0080.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 405,
        "source_end": 429,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 792,
      "output_tokens": 195,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 20, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "City of Kingston",
      "deadline": "November 20, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "845-331-0080"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 20, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "City of Kingston",
      "deadline": "November 20, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "845-331-0080"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "This notice concems a City of Kingston parking citation.",
    "deadline": "Pay by: November 20, 2026",
    "amount_due": "Parking fine: $35.00",
    "required_action": "Pay $35.00 by November 20, 2026 using the City of Kingston parking tcket service.",
    "contact": "Questions: 845-331-0080."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 704,
    "output_tokens": 198,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## PA_01 — clean

[Input image](../../eval/northeast_stress/corpus/PA_01-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-10`

Observed: `within 15 calendar days of the issue date`

**contact**: verified; false-verified=True

Expected: `1-888-591-3636`

Observed: `ss philapark.org/violations`

Review: Correct printed URL prefixed by OCR garbage ss; URL itself is intact.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City and County of Philadelphia
PARKING NOTICE
Citation: DEMO-PA-001
Issued: October 26, 2026
Plate: DEMOPA / PA
Location: 100 Example Street
Violation: Overtime parking
Fine: $41.00
Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.
Online payment and appeal information: philapark.org/violations
Questions: 1-888-591-3636.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

GIN CODCCININ/CPGLIMINTGLI.

PARKING NOTICE
FRONT - CASE DETAILS REVERSE - RESPONSE OPTIONS
Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15
Issued: Cctober 26, 2026 calendar days of the issue date.

Plate: DEMOPA / PA Online payment and appeal information:
ss philapark.org/violations

Questions: 1-888-591-3636.

Location: 100 Example Street

Violation: Overtime parking

Fine: $41.06

SYNTHETIC / PA_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": null,
      "source_snippet": null
    },
    "deadline": {
      "value": "within 15 calendar days of the issue date",
      "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
      "kind": "relative",
      "relative_days": 15,
      "anchor_date": "Cctober 26, 2026",
      "anchor_source_snippet": "Issued: Cctober 26, 2026"
    },
    "amount_due": {
      "value": "$41.00",
      "source_snippet": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date."
    },
    "required_action": {
      "value": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
      "source_snippet": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date."
    },
    "contact": {
      "value": "ss philapark.org/violations",
      "source_snippet": "Online payment and appeal information:\nss philapark.org/violations"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 15 calendar days of the issue date",
        "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$41.00",
        "source_snippet": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "source_snippet": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "ss philapark.org/violations",
        "source_snippet": "Online payment and appeal information:\nss philapark.org/violations",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 334,
        "source_end": 400,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Amount due: not verified. Check the original notice or ask someone for help.",
      "Required action: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 808,
      "output_tokens": 243,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "ss philapark.org/violations"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "ss philapark.org/violations"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "missing",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": null,
    "deadline": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
    "amount_due": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
    "required_action": "Citation: DEMO-PA-C91 Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
    "contact": "Online payment and appeal information:\nss philapark.org/violations"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 693,
    "output_tokens": 231,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## PA_01 — degraded

[Input image](../../eval/northeast_stress/corpus/PA_01-degraded.jpg)

### Every strict field mismatch

**contact**: verified; false-verified=True

Expected: `1-888-591-3636`

Observed: `philapark.org/violations
Questions: 1-888-591-3636.`

Review: Both printed contact channels preserved, but combined differently from the predeclared aliases.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City and County of Philadelphia
PARKING NOTICE
Citation: DEMO-PA-001
Issued: October 26, 2026
Plate: DEMOPA / PA
Location: 100 Example Street
Violation: Overtime parking
Fine: $41.00
Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.
Online payment and appeal information: philapark.org/violations
Questions: 1-888-591-3636.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALIO - 00 NOT PAY

trverted case Cotets. No real cett or verucie.

FRONT - CASE DETAILS
Citation: CEMO-PA-001
Issued: October 26, 2026

Plate: DEMOPA / PA

Location: 100 Example Street
Violation: Overtime parking a
Fine: $41.00 Oe

, SYNTHETIC / PA_01 / SOFTWARE TEST ONLY

REVERSE - RESPONSE OPTIONS

Pay $41.00 or appeal this parking citation within 15
calendar days of the issue date.

Online payment and appeal information:
philapark.org/violations
Questions: 1-888-591-3636.
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": null,
      "source_snippet": null
    },
    "deadline": {
      "value": "within 15 calendar days of the issue date",
      "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
      "kind": "relative",
      "relative_days": 15,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Issued: October 26, 2026"
    },
    "amount_due": {
      "value": "$41.00",
      "source_snippet": "Fine: $41.00 Oe"
    },
    "required_action": {
      "value": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
      "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date."
    },
    "contact": {
      "value": "philapark.org/violations\nQuestions: 1-888-591-3636.",
      "source_snippet": "Online payment and appeal information:\nphilapark.org/violations\nQuestions: 1-888-591-3636."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 15 calendar days of the issue date",
        "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 324,
        "source_end": 409,
        "normalized_value": "2026-11-10",
        "days_remaining": 15,
        "anchor_source_snippet": "Issued: October 26, 2026",
        "anchor_start": 132,
        "anchor_end": 156
      },
      "amount_due": {
        "value": "$41.00",
        "source_snippet": "Fine: $41.00 Oe",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 237,
        "source_end": 252,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "source_snippet": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 324,
        "source_end": 409,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "philapark.org/violations\nQuestions: 1-888-591-3636.",
        "source_snippet": "Online payment and appeal information:\nphilapark.org/violations\nQuestions: 1-888-591-3636.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 411,
        "source_end": 501,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 799,
      "output_tokens": 234,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 10, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "November 10, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "philapark.org/violations\nQuestions: 1-888-591-3636."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 10, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "November 10, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "philapark.org/violations\nQuestions: 1-888-591-3636."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "missing",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": null,
    "deadline": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
    "amount_due": "Fine: $41.00 Oe",
    "required_action": "Pay $41.00 or appeal this parking citation within 15 calendar days of the issue date.",
    "contact": "Online payment and appeal information:\nphilapark.org/violations\nQuestions: 1-888-591-3636."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 753,
    "output_tokens": 231,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## PA_02 — clean

[Input image](../../eval/northeast_stress/corpus/PA_02-clean.png)

### Every strict field mismatch

**deadline**: verified; false-verified=True

Expected: `None`

Observed: `2026-11-05`

Review: Printed November 5 payment date is real; the key requires abstention because contesting has a different deadline. This is loss of conditional context, not an invented date.

**required_action**: unverified; false-verified=False

Expected: `Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket. Do not pay if you choose to contest. A hearing request after 10 days can still incur late fees.`

Observed: `Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Public Parking Authority of Pittsburgh
PARKING NOTICE
Ticket: DEMO-PA-002
Issue date: October 26, 2026
Plate: TESTPA / PA
Fine: $25.00
Cost: $30.50
Total due now: $55.50
If paid after November 5, 2026: $78.50
If paid after November 25, 2026: $93.50
Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.
Do not pay if you choose to contest. A hearing request after 10 days can still incur late fees.
Questions: 866-353-7151.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

PUBLIC PARKING AUTHORITY, OF, PITTSBURGH

PARKING NOTICE
FRONT - CASE DETAILS REVERSE - RESPONSE OPTIONS
Ticket: DEMO-PA-0C2 Pay the total due by November 5, 2026, or request
Issue date: October 26, 2926 a hearing within 20 days of the issue date to

. contest the ticket.
Plate: TESTPA / PA

Do not pay if you choose to contest. A hearing
request after 10 days can still incur late fees.

Questions: 866-353-7151.

Fine: $25.00

Cost: $30.50

Total due new: $55.50
If paid after November 5, 2026: $78.59
If paid after November 25, 2026: $93.50

SYNTHETIC / PA_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
      "source_snippet": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH"
    },
    "deadline": {
      "value": "November 5, 2026",
      "source_snippet": "Pay the total due by November 5, 2026, or request",
      "kind": "absolute",
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$55.50",
      "source_snippet": "Total due new: $55.50"
    },
    "required_action": {
      "value": "Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.",
      "source_snippet": "Pay the total due by November 5, 2026, or request\nIssue date: October 26, 2926 a hearing within 20 days of the issue date to\n\n. contest the ticket."
    },
    "contact": {
      "value": "866-353-7151",
      "source_snippet": "Questions: 866-353-7151."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
        "source_snippet": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 89,
        "source_end": 129,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "November 5, 2026",
        "source_snippet": "Pay the total due by November 5, 2026, or request",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 214,
        "source_end": 263,
        "normalized_value": "2026-11-05",
        "days_remaining": 10,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$55.50",
        "source_snippet": "Total due new: $55.50",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 533,
        "source_end": 554,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.",
        "source_snippet": "Pay the total due by November 5, 2026, or request\nIssue date: October 26, 2926 a hearing within 20 days of the issue date to\n\n. contest the ticket.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 214,
        "source_end": 361,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "866-353-7151",
        "source_snippet": "Questions: 866-353-7151.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 479,
        "source_end": 503,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Required action: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 863,
      "output_tokens": 240,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 5, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
      "deadline": "November 5, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "866-353-7151"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 5, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
      "deadline": "November 5, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "866-353-7151"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "PUBLIC PARKING AUTHORITY, OF, PITTSBURGH",
    "deadline": "Pay the total due by November 5, 2026, or request",
    "amount_due": "Total due new: $55.50",
    "required_action": "Pay the total due by November 5, 2026, or request\nIssue date: October 26, 2926 a hearing within 20 days of the issue date to\n\n. contest the ticket.",
    "contact": "Questions: 866-353-7151."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 728,
    "output_tokens": 207,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## PA_02 — degraded

[Input image](../../eval/northeast_stress/corpus/PA_02-degraded.jpg)

### Every strict field mismatch

**deadline**: verified; false-verified=True

Expected: `None`

Observed: `2026-11-05`

Review: Same conditional-context failure: a single verified deadline cannot represent both payment and hearing-request branches.

**required_action**: unverified; false-verified=False

Expected: `Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket. Do not pay if you choose to contest. A hearing request after 10 days can still incur late fees.`

Observed: `Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Public Parking Authority of Pittsburgh
PARKING NOTICE
Ticket: DEMO-PA-002
Issue date: October 26, 2026
Plate: TESTPA / PA
Fine: $25.00
Cost: $30.50
Total due now: $55.50
If paid after November 5, 2026: $78.50
If paid after November 25, 2026: $93.50
Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.
Do not pay if you choose to contest. A hearing request after 10 days can still incur late fees.
Questions: 866-353-7151.
```

### Full OCR text

```text
SYNTHETIC TEST -NOT VALID - 00 NOT PAY

Wrrerted case Cotate. No real debt or vehucie.

PUBLIC PARKING AUTHORITY, OF PITTSBURGH

PARKING NOTICE)

REVERSE - RESPONSE OPTIONS
Pay the total due by November 5, 2026, or request
~ a hearing within 20 days of the issue date to
— contest the ticket.

FRONT - CASE DETAILS
Ticket: DEMO-PA-0C2
Tssue date: October 26, 2026 a

Plate: TESTPA / PA

Fine: $35.00 iid So Do not pay if you choose to contest. A hearing '

oo eo request after 10 days can still incur late fees.

Cost: $30.50 . '
— Questions: 866-353-7151.

Total due now: $55.50 |
If paid after November 5, 2026: $78.50 | |
If paid after November 25, 2026: $93.50 |

, SYNTHETIC / PA_O2 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
      "source_snippet": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH"
    },
    "deadline": {
      "value": "November 5, 2026",
      "source_snippet": "Pay the total due by November 5, 2026, or request",
      "kind": "absolute",
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$55.50",
      "source_snippet": "Total due now: $55.50"
    },
    "required_action": {
      "value": "Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.",
      "source_snippet": "Pay the total due by November 5, 2026, or request\n~ a hearing within 20 days of the issue date to\n— contest the ticket."
    },
    "contact": {
      "value": "866-353-7151",
      "source_snippet": "Questions: 866-353-7151."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
        "source_snippet": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 127,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "November 5, 2026",
        "source_snippet": "Pay the total due by November 5, 2026, or request",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 173,
        "source_end": 222,
        "normalized_value": "2026-11-05",
        "days_remaining": 10,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$55.50",
        "source_snippet": "Total due now: $55.50",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 558,
        "source_end": 579,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the total due by November 5, 2026, or request a hearing within 20 days of the issue date to contest the ticket.",
        "source_snippet": "Pay the total due by November 5, 2026, or request\n~ a hearing within 20 days of the issue date to\n— contest the ticket.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 173,
        "source_end": 292,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "866-353-7151",
        "source_snippet": "Questions: 866-353-7151.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 532,
        "source_end": 556,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Required action: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 877,
      "output_tokens": 228,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 5, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
      "deadline": "November 5, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "866-353-7151"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "What to do: Please double-check this with the agency."
    ],
    "deadline_note": "Due date: November 5, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency.",
      "What to do: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
      "deadline": "November 5, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "What to do: Please double-check this with the agency.",
      "contact": "866-353-7151"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "unverified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "PUBLIC PARKING AUTHORITY, OF PITTSBURGH",
    "deadline": "Pay the total due by November 5, 2026, or request",
    "amount_due": "Total due now: $55.50",
    "required_action": "Pay the total due by November 5, 2026, or request\n~ a hearing within 20 days of the issue date to\n— contest the ticket.",
    "contact": "Questions: 866-353-7151."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 725,
    "output_tokens": 206,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## RI_01 — clean

[Input image](../../eval/northeast_stress/corpus/RI_01-clean.png)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-09`

Observed: `within 14 days of the issue date`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Providence Municipal Court
PARKING NOTICE
Ticket: DEMO-RI-001
Issue date: October 26, 2026
Plate: DEMORI / RI
Current fine: $50.00
After 14 days: $100.00
After 28 days: $150.00
Pay the current fine within 14 days of the issue date to avoid the higher amount.
Online payment adds a separate $3.50 convenience fee.
Questions: 401-243-6414.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

PROVIDENCE MUNICIPALSCOURT,

Ticket DEMO-RI-001
issue date October 26, 2026
Plate DEMORI/ RI
Current fine $50.00

After 14 days $100.00

After 28 days $150.00

Pay the current fine within 14 days of the issue date to avoid the higher amount.

Online payment adds a separate $3.50 convenience fee.

Questions: 401-243-6414.

SYNTHETIC / RI_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "PROVIDENCE MUNICIPALSCOURT",
      "source_snippet": "PROVIDENCE MUNICIPALSCOURT,"
    },
    "deadline": {
      "value": "within 14 days of the issue date",
      "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "kind": "relative",
      "relative_days": 14,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "issue date October 26, 2026"
    },
    "amount_due": {
      "value": "$50.00",
      "source_snippet": "Current fine $50.00"
    },
    "required_action": {
      "value": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    },
    "contact": {
      "value": "401-243-6414",
      "source_snippet": "Questions: 401-243-6414."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "PROVIDENCE MUNICIPALSCOURT",
        "source_snippet": "PROVIDENCE MUNICIPALSCOURT,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 89,
        "source_end": 116,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 14 days of the issue date",
        "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 249,
        "source_end": 330,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$50.00",
        "source_snippet": "Current fine $50.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 182,
        "source_end": 201,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 249,
        "source_end": 330,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "401-243-6414",
        "source_snippet": "Questions: 401-243-6414.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 387,
        "source_end": 411,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 784,
      "output_tokens": 210,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PROVIDENCE MUNICIPALSCOURT",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "contact": "401-243-6414"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "PROVIDENCE MUNICIPALSCOURT",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "contact": "401-243-6414"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "PROVIDENCE MUNICIPALSCOURT,",
    "deadline": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
    "amount_due": "Current fine $50.00",
    "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
    "contact": "Questions: 401-243-6414."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 741,
    "output_tokens": 214,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## RI_01 — degraded

[Input image](../../eval/northeast_stress/corpus/RI_01-degraded.jpg)

### Every strict field mismatch

**deadline**: unverified; false-verified=False

Expected: `2026-11-09`

Observed: `within 14 days of the issue date`

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Providence Municipal Court
PARKING NOTICE
Ticket: DEMO-RI-001
Issue date: October 26, 2026
Plate: DEMORI / RI
Current fine: $50.00
After 14 days: $100.00
After 28 days: $150.00
Pay the current fine within 14 days of the issue date to avoid the higher amount.
Online payment adds a separate $3.50 convenience fee.
Questions: 401-243-6414.
```

### Full OCR text

```text
Se a wee wi ee ee - -

SYNTHETIC TEST - NOT VALID - DO NOT PAY

lavented case cotats. No real dett or venicle.

i Ticket = s—itsti‘“‘éSOSCSC;C;*;#‘;#O@OEMORIQODOO!U!|!™)™©™)™)™OUOUO |
| Issue date October 26, 2026

be ; ~ DEMORITRI

[ Curren fine OO $50.00

jAttert4dys $1000.

cc 2days | $150.00

'
Pay the current fine within 14 days of the issue date to avoid the higher amount. |
Online payment adds a separate $3.50 convenience fee. |

Questions: 401-243-6414,
t

SYNTHETIC / RI_O1 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": null,
      "source_snippet": null
    },
    "deadline": {
      "value": "within 14 days of the issue date",
      "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "kind": "relative",
      "relative_days": 14,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Issue date October 26, 2026"
    },
    "amount_due": {
      "value": "$50.00",
      "source_snippet": "Curren fine OO $50.00"
    },
    "required_action": {
      "value": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    },
    "contact": {
      "value": "401-243-6414",
      "source_snippet": "Questions: 401-243-6414,"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 14 days of the issue date",
        "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 300,
        "source_end": 381,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$50.00",
        "source_snippet": "Curren fine OO $50.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 235,
        "source_end": 256,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "source_snippet": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 300,
        "source_end": 381,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "401-243-6414",
        "source_snippet": "Questions: 401-243-6414,",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 441,
        "source_end": 465,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 834,
      "output_tokens": 197,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "contact": "401-243-6414"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the current fine within 14 days of the issue date to avoid the higher amount."
    ],
    "deadline_note": "Deadline: Please double-check this with the agency.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Not found. Check the original notice.",
      "Deadline: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Not found. Check the original notice.",
      "deadline": "Deadline: Please double-check this with the agency.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
      "contact": "401-243-6414"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "missing",
    "deadline": "unverified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": null,
    "deadline": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
    "amount_due": "Curren fine OO $50.00",
    "required_action": "Pay the current fine within 14 days of the issue date to avoid the higher amount.",
    "contact": "Questions: 401-243-6414,"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 728,
    "output_tokens": 229,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## RI_02 — degraded

[Input image](../../eval/northeast_stress/corpus/RI_02-degraded.jpg)

### Every strict field mismatch

**contact**: verified; false-verified=True

Expected: `401-845-5718`

Observed: `Questions: 401-845-5718.`

Review: Correct phone digits with Questions label; harmless strict-format failure.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Newport Parking Division
PARKING NOTICE
Ticket: D-DEMO-RI-002
Issue date: October 26, 2026
Plate / State: TESTRI / RI
Violation: Parking beyond the permitted time
Fine: $25.00
Pay the fine or submit a parking violation review request.
If requesting review, provide a description and any supporting photographs before paying or requesting a court appearance.
Questions: 401-845-5718.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID -DO NOT PAY

tnvented case cetats. No real dett or vehicle.

CITY OF NEWPORT PARKING DIVISIO.

PARKING NOTICE)

. Ticket D-DEMO-RI-002 |
"Issue date — ” October 26, 2026 /
Plate / State —  TESTRITRI a

Violation Parking beyond the permitted time

|
:
|
|

:

ine $25.00

c
ba |

Pay the fine or submit a parking violation review request.

if requesting review, provide a description and any supporting photographs before paying or requesting a
court appearance.

Questions: 401-845-5718.

a a en

i.
en
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITY OF NEWPORT PARKING DIVISIO.",
      "source_snippet": "CITY OF NEWPORT PARKING DIVISIO."
    },
    "deadline": {
      "value": null,
      "source_snippet": null,
      "kind": null,
      "relative_days": null,
      "anchor_date": null,
      "anchor_source_snippet": null
    },
    "amount_due": {
      "value": "$25.00",
      "source_snippet": "ine $25.00"
    },
    "required_action": {
      "value": "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance.",
      "source_snippet": "Pay the fine or submit a parking violation review request.\n\nif requesting review, provide a description and any supporting photographs before paying or requesting a\ncourt appearance."
    },
    "contact": {
      "value": "Questions: 401-845-5718.",
      "source_snippet": "Questions: 401-845-5718."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITY OF NEWPORT PARKING DIVISIO.",
        "source_snippet": "CITY OF NEWPORT PARKING DIVISIO.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 120,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": null,
        "source_snippet": null,
        "status": "missing",
        "reason": "The extractor did not find this field. Check the photo.",
        "source_start": null,
        "source_end": null,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "amount_due": {
        "value": "$25.00",
        "source_snippet": "ine $25.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 286,
        "source_end": 296,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance.",
        "source_snippet": "Pay the fine or submit a parking violation review request.\n\nif requesting review, provide a description and any supporting photographs before paying or requesting a\ncourt appearance.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 306,
        "source_end": 488,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "Questions: 401-845-5718.",
        "source_snippet": "Questions: 401-845-5718.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 490,
        "source_end": 514,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Deadline: not verified. Check the original notice or ask someone for help.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 792,
      "output_tokens": 210,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITY OF NEWPORT PARKING DIVISIO.",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance.",
      "contact": "Questions: 401-845-5718."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance."
    ],
    "deadline_note": "Deadline: Not found. Check the original notice.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Deadline: Not found. Check the original notice.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITY OF NEWPORT PARKING DIVISIO.",
      "deadline": "Deadline: Not found. Check the original notice.",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the fine or submit a parking violation review request. if requesting review, provide a description and any supporting photographs before paying or requesting a court appearance.",
      "contact": "Questions: 401-845-5718."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "missing",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "CITY OF NEWPORT PARKING DIVISIO.",
    "deadline": null,
    "amount_due": "ine $25.00",
    "required_action": "Pay the fine or submit a parking violation review request.\n\nif requesting review, provide a description and any supporting photographs before paying or requesting a\ncourt appearance.",
    "contact": "Questions: 401-845-5718."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 801,
    "output_tokens": 242,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## VT_01 — clean

[Input image](../../eval/northeast_stress/corpus/VT_01-clean.png)

### Every strict field mismatch

**deadline**: verified; false-verified=True

Expected: `2026-11-25`

Observed: `2926-11-25`

Review: OCR anchor changes 2026 to 2926. Validator computes and verifies November 25, 2926; English repeats it.

**required_action**: verified; false-verified=True

Expected: `Pay the waiver fee or contest the parking ticket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.`

Observed: `Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.`

Review: OCR changes ticket to Licket; action remains understandable but is not an exact reproduction.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
City of Burlington Parking Services
PARKING NOTICE
Ticket: DEMO-VT-001
Issue date: October 26, 2026
Plate: DEMOVT / VT
Violation: Parking in a restricted area
Waiver fee: $75.00
Pay the waiver fee or contest the parking ticket within 30 days of the issue date.
Include the ticket and supporting documents with a written appeal.
Questions: parkingservices@burlingtonvt.gov
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetais No real debt or vehicle.

‘CITYROFABURLINGTONI PARKINGESERVICES

[PARK INGENOTICE]

Ticket: DEMO-VT-0C1

Issue date: October 26, 2926

Plate: DEMOVT / VT

Violation: Parking in a restricted area

Waiver fee: $75.00

Pay the waiver fee or contest the parking
Licket within 30 days of the issue date.

Include the ticket and supporting documents
with a written appeal.

Questions: parkingservices@burlingtonvt.gov

SYNTHETIC / VT_01 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "CITYROFABURLINGTONI PARKINGESERVICES",
      "source_snippet": "‘CITYROFABURLINGTONI PARKINGESERVICES"
    },
    "deadline": {
      "value": "within 30 days of the issue date",
      "source_snippet": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.",
      "kind": "relative",
      "relative_days": 30,
      "anchor_date": "October 26, 2926",
      "anchor_source_snippet": "Issue date: October 26, 2926"
    },
    "amount_due": {
      "value": "$75.00",
      "source_snippet": "Waiver fee: $75.00"
    },
    "required_action": {
      "value": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.",
      "source_snippet": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.\n\nInclude the ticket and supporting documents\nwith a written appeal."
    },
    "contact": {
      "value": "parkingservices@burlingtonvt.gov",
      "source_snippet": "Questions: parkingservices@burlingtonvt.gov"
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "CITYROFABURLINGTONI PARKINGESERVICES",
        "source_snippet": "‘CITYROFABURLINGTONI PARKINGESERVICES",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 88,
        "source_end": 125,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 30 days of the issue date",
        "source_snippet": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 278,
        "source_end": 360,
        "normalized_value": "2926-11-25",
        "days_remaining": 328748,
        "anchor_source_snippet": "Issue date: October 26, 2926",
        "anchor_start": 167,
        "anchor_end": 195
      },
      "amount_due": {
        "value": "$75.00",
        "source_snippet": "Waiver fee: $75.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 258,
        "source_end": 276,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.",
        "source_snippet": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.\n\nInclude the ticket and supporting documents\nwith a written appeal.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 278,
        "source_end": 428,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "parkingservices@burlingtonvt.gov",
        "source_snippet": "Questions: parkingservices@burlingtonvt.gov",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 430,
        "source_end": 473,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 793,
      "output_tokens": 251,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal."
    ],
    "deadline_note": "Due date: November 25, 2926.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITYROFABURLINGTONI PARKINGESERVICES",
      "deadline": "November 25, 2926",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.",
      "contact": "parkingservices@burlingtonvt.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal."
    ],
    "deadline_note": "Due date: November 25, 2926.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "CITYROFABURLINGTONI PARKINGESERVICES",
      "deadline": "November 25, 2926",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date. Include the ticket and supporting documents with a written appeal.",
      "contact": "parkingservices@burlingtonvt.gov"
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "‘CITYROFABURLINGTONI PARKINGESERVICES",
    "deadline": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.",
    "amount_due": "Waiver fee: $75.00",
    "required_action": "Pay the waiver fee or contest the parking Licket within 30 days of the issue date.\n\nInclude the ticket and supporting documents\nwith a written appeal.",
    "contact": "Questions: parkingservices@burlingtonvt.gov"
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 831,
    "output_tokens": 232,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## VT_02 — clean

[Input image](../../eval/northeast_stress/corpus/VT_02-clean.png)

### Every strict field mismatch

**deadline**: verified; false-verified=True

Expected: `2026-11-08`

Observed: `2026-11-09`

Review: Printed rule counts October 26 as day 1. November 8 is day 14, but validator verifies November 9.

**required_action**: verified; false-verified=True

Expected: `To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citation number and reason for the appeal.`

Observed: `To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal.`

Review: OCR changes citation to citahon; the day-1 condition is preserved in the action despite wrong date calculation.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Town of Brattleboro Parking Enforcement
PARKING NOTICE
Citation: DEMO-VT-002
Issue date: October 26, 2026
Plate: TESTVT / VT
Parking fine: $35.00
To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.
Include your name, contact information, citation number and reason for the appeal.
Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY

Invented case cetar’s. No real debt or vehkie,

TOWN, OR BRATTLEBORO PARKING ENFORCEMEN

[PARKING NOTICE

Citation: DEMO-VT-002
Issue date: October 26, 2026
Plate: TESTVT / VT
Parking fine: $35.00

To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.
Include your name, contact information, citahon number and reason for the appeal.

Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.

SYNTHETIC / VT_02 / SOFTWARE TEST ONLY
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "Brattleboro Parking Enforcement",
      "source_snippet": "TOWN, OR BRATTLEBORO PARKING ENFORCEMEN\n\n[PARKING NOTICE"
    },
    "deadline": {
      "value": "within 14 days of the issue date",
      "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.",
      "kind": "relative",
      "relative_days": 14,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Issue date: October 26, 2026"
    },
    "amount_due": {
      "value": "$35.00",
      "source_snippet": "Parking fine: $35.00"
    },
    "required_action": {
      "value": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal.",
      "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.\nInclude your name, contact information, citahon number and reason for the appeal."
    },
    "contact": {
      "value": "Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.",
      "source_snippet": "Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "Brattleboro Parking Enforcement",
        "source_snippet": "TOWN, OR BRATTLEBORO PARKING ENFORCEMEN\n\n[PARKING NOTICE",
        "status": "unverified",
        "reason": "The value could not be checked against its source.",
        "source_start": 89,
        "source_end": 145,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 14 days of the issue date",
        "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 239,
        "source_end": 351,
        "normalized_value": "2026-11-09",
        "days_remaining": 14,
        "anchor_source_snippet": "Issue date: October 26, 2026",
        "anchor_start": 169,
        "anchor_end": 197
      },
      "amount_due": {
        "value": "$35.00",
        "source_snippet": "Parking fine: $35.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 217,
        "source_end": 237,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal.",
        "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.\nInclude your name, contact information, citahon number and reason for the appeal.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 239,
        "source_end": 433,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.",
        "source_snippet": "Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 435,
        "source_end": 515,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 807,
      "output_tokens": 307,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Please double-check this with the agency.",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal.",
      "contact": "Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Issuing agency: Please double-check this with the agency.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "Issuing agency: Please double-check this with the agency.",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citahon number and reason for the appeal.",
      "contact": "Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "unverified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "TOWN, OR BRATTLEBORO PARKING ENFORCEMEN\n\n[PARKING NOTICE",
    "deadline": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.",
    "amount_due": "Parking fine: $35.00",
    "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.\nInclude your name, contact information, citahon number and reason for the appeal.",
    "contact": "Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 902,
    "output_tokens": 281,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```

## VT_02 — degraded

[Input image](../../eval/northeast_stress/corpus/VT_02-degraded.jpg)

### Every strict field mismatch

**deadline**: verified; false-verified=True

Expected: `2026-11-08`

Observed: `2026-11-09`

Review: Validator again verifies November 9 instead of November 8. OCR additionally misreads day 1 as day I.

**required_action**: verified; false-verified=True

Expected: `To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1. Include your name, contact information, citation number and reason for the appeal.`

Observed: `To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal.`

Review: The printed day 1 becomes day I and remains verified. This reinforces the need to verify the counting convention against the image.

**contact**: verified; false-verified=True

Expected: `Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.`

Observed: `Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301.`

Review: Street is misread as Suect; address number, street name, city, state and ZIP remain intact.

### Visible source text

```text
SYNTHETIC TEST - NOT VALID - DO NOT PAY
Town of Brattleboro Parking Enforcement
PARKING NOTICE
Citation: DEMO-VT-002
Issue date: October 26, 2026
Plate: TESTVT / VT
Parking fine: $35.00
To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day 1.
Include your name, contact information, citation number and reason for the appeal.
Contact: Brattleboro Parking Enforcement, 77 Flat Street, Brattleboro, VT 05301.
```

### Full OCR text

```text
SYNTHETIC TEST - NOT VALID -DO NOT PAY

lvented case Cotats. No real dett or vehicle.

TOWN OF. BRATTLEBORO PARKING ENFORCEMENT)

Citation: DEMO-VT-002
Issue date: October 26, 2026
Plate: TESTVT / VT
Parking fine: $35.00

To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I.
Include your name, contact information, citation number and reason for the appeal.

Contact: Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301.

ee ee

a

SYNTHETIC / VT_02 ! SOFTWARE TEST ONLY

- TO ST OS oe
```

### Complete proposed and checked fields

```json
{
  "proposal": {
    "issuing_agency": {
      "value": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT",
      "source_snippet": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT)"
    },
    "deadline": {
      "value": "within 14 days of the issue date",
      "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date.",
      "kind": "relative",
      "relative_days": 14,
      "anchor_date": "October 26, 2026",
      "anchor_source_snippet": "Issue date: October 26, 2026"
    },
    "amount_due": {
      "value": "$35.00",
      "source_snippet": "Parking fine: $35.00"
    },
    "required_action": {
      "value": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal.",
      "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I.\nInclude your name, contact information, citation number and reason for the appeal."
    },
    "contact": {
      "value": "Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301.",
      "source_snippet": "Contact: Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301."
    },
    "doc_type": "parking_ticket"
  },
  "extraction": {
    "doc_type": "parking_ticket",
    "today": "2026-10-26",
    "fields": {
      "issuing_agency": {
        "value": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT",
        "source_snippet": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT)",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 87,
        "source_end": 128,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "deadline": {
        "value": "within 14 days of the issue date",
        "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 222,
        "source_end": 303,
        "normalized_value": "2026-11-09",
        "days_remaining": 14,
        "anchor_source_snippet": "Issue date: October 26, 2026",
        "anchor_start": 152,
        "anchor_end": 180
      },
      "amount_due": {
        "value": "$35.00",
        "source_snippet": "Parking fine: $35.00",
        "status": "unverified",
        "reason": "Check every printed amount against the original photo before confirming amounts.",
        "source_start": 200,
        "source_end": 220,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "required_action": {
        "value": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal.",
        "source_snippet": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I.\nInclude your name, contact information, citation number and reason for the appeal.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 222,
        "source_end": 417,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      },
      "contact": {
        "value": "Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301.",
        "source_snippet": "Contact: Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301.",
        "status": "verified",
        "reason": "Matches the confirmed text. Check that this is the right fact on your original notice.",
        "source_start": 419,
        "source_end": 498,
        "normalized_value": null,
        "days_remaining": null,
        "anchor_source_snippet": null,
        "anchor_start": null,
        "anchor_end": null
      }
    },
    "warnings": [
      "Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.",
      "Printed amounts have not been separately checked against the original photo. Reader agreement is not verification."
    ],
    "usage": {
      "input_tokens": 811,
      "output_tokens": 299,
      "cached_input_tokens": 0,
      "responses_with_usage": 1
    },
    "attempts": 1
  }
}
```

### Complete displayed explanation

```json
{
  "english": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal.",
      "contact": "Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "localized": {
    "summary": "You selected: Parking ticket.",
    "what_happened": "The checked facts are shown below.",
    "what_to_do": [
      "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal."
    ],
    "deadline_note": "Due date: November 9, 2026.",
    "amount_note": "Amount due: Please double-check this with the agency.",
    "confidence_notes": [
      "Verified means matched to your confirmed text. Check the original notice; this does not guarantee the right fact was selected.",
      "Amount due: Please double-check this with the agency."
    ],
    "cards": {
      "issuing_agency": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT",
      "deadline": "November 9, 2026",
      "amount_due": "Amount due: Please double-check this with the agency.",
      "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I. Include your name, contact information, citation number and reason for the appeal.",
      "contact": "Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301."
    },
    "disclaimer": "This is an explanatory tool, not legal advice."
  },
  "requested_language": "en",
  "display_language": "en",
  "field_statuses": {
    "issuing_agency": "verified",
    "deadline": "verified",
    "amount_due": "unverified",
    "required_action": "verified",
    "contact": "verified"
  },
  "original_snippets": {
    "issuing_agency": "TOWN OF. BRATTLEBORO PARKING ENFORCEMENT)",
    "deadline": "To contest this citation, send a written appeal within 14 days of the issue date.",
    "amount_due": "Parking fine: $35.00",
    "required_action": "To contest this citation, send a written appeal within 14 days of the issue date. Count the issue date as day I.\nInclude your name, contact information, citation number and reason for the appeal.",
    "contact": "Contact: Brattleboro Parking Enforcement, 77 Flat Suect, Brattleboro, VT 05301."
  },
  "english_generation": {
    "method": "model",
    "attempts": 1,
    "failed_checks": []
  },
  "translation": {
    "fallback_to_english": false,
    "translation_confidence": "high",
    "attempts": 0,
    "failed_checks": [],
    "back_translation": null
  },
  "notice": "",
  "target_disclaimer": "This is an explanatory tool, not legal advice.",
  "usage": {
    "calls": 1,
    "input_tokens": 918,
    "output_tokens": 269,
    "cached_input_tokens": 0,
    "responses_with_usage": 1
  }
}
```
