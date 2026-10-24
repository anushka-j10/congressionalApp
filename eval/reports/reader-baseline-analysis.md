# A1 baseline failure analysis — unchanged M1 reader

This is the A1 measurement checkpoint, not a completed reader comparison. No reader fixes, handwriting-support claim, or extraction implementation were made.

## Current configuration

Tesseract 5.5.3; English; PSM 3; 35-second OCR timeout. M1 backend normalization applies EXIF orientation, at most 1600px long edge, and JPEG quality 90. No OpenCV preprocessing is present. Vision key/model are not configured in this checkout.

## Reader × condition

| Reader | Condition | Pages | CER | Key-token recall | Targets matched | Call errors |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| tesseract | clean | 8 | 0.00% | 100.00% | 28/28 | 0 |
| tesseract | degraded | 56 | 29.09% | 64.29% | 126/196 | 0 |
| tesseract | handwriting | 0 | N/A | N/A | 0/0 | 0 |
| tesseract | legacy_m1 | 8 | 0.05% | 100.00% | 28/28 | 0 |
| vision | clean | 0 | N/A | N/A | 0/0 | 0 |
| vision | degraded | 0 | N/A | N/A | 0/0 | 0 |
| vision | handwriting | 0 | N/A | N/A | 0/0 | 0 |
| vision | legacy_m1 | 0 | N/A | N/A | 0/0 | 0 |

Vision was NOT RUN because credentials/model are absent. Handwriting is unmeasured because no photo/truth pairs were provided. Zero call errors means OCR returned without an exception; it does not mean the output was correct.

## Printed threshold result

Clean plus degraded printed pages: **154/224 = 68.75% key-token recall**, with 25.45% CER. This is below the required 95%. The formal chosen-reader gate remains pending A2 comparison and student choice; **Part B must not begin on this baseline**.

The eight original M1 images are excluded from this printed aggregate to avoid double-counting their clean counterparts. All original PNG/JSON files and the measured production reader/normalization files retained their pre-run hashes.

## Failure conditions

| Variant | Pages | CER | Key-token recall | Matched / expected |
| --- | ---: | ---: | ---: | ---: |
| blur | 8 | 0.00% | 100.00% | 28/28 |
| compression | 8 | 0.00% | 100.00% | 28/28 |
| noise | 8 | 0.00% | 100.00% | 28/28 |
| perspective | 8 | 23.35% | 71.43% | 20/28 |
| phone_mix | 8 | 98.07% | 0.00% | 0/28 |
| rotation | 8 | 0.76% | 78.57% | 22/28 |
| shadow | 8 | 81.46% | 0.00% | 0/28 |

The shadow gradient makes the left side darker while the text remains visibly present. On the inspected synthetic parking page, the unchanged reader returned fragments from the brighter right side and omitted all critical tokens. This suggests a lighting/segmentation weakness worth testing in A2, rather than evidence that the source document contains no deadline or amount.

Perspective variants lost the issue-date token on all eight pages. Rotation lost six deadline tokens. These are observed missing/misread values; this checkpoint does not claim a particular algorithm will fix them.

## Exact missed targets

Candidate entries below are other actual recognized tokens of the same kind, ranked by string similarity. They are not inferred corrections, not aligned field values, and not hybrid candidates shown in the app.

| Sample | Kind | Missing expected value | Missing count | Other recognized tokens |
| --- | --- | --- | ---: | --- |
| court_01__perspective | date | `2026-10-21` | 1 | 2026-11-03 |
| court_01__phone_mix | date | `2026-10-21` | 1 | none detected |
| court_01__phone_mix | date | `2026-11-03` | 1 | none detected |
| court_01__phone_mix | id | `SYNTHETIC-ONLY-003` | 1 | none detected |
| court_01__rotation | date | `2026-11-03` | 1 | 2026-10-21 |
| court_01__shadow | date | `2026-10-21` | 1 | none detected |
| court_01__shadow | date | `2026-11-03` | 1 | none detected |
| court_01__shadow | id | `SYNTHETIC-ONLY-003` | 1 | none detected |
| court_02__perspective | date | `2026-10-21` | 1 | 2026-11-05 |
| court_02__phone_mix | date | `2026-10-21` | 1 | none detected |
| court_02__phone_mix | date | `2026-11-05` | 1 | none detected |
| court_02__phone_mix | id | `SYNTHETIC-ONLY-004` | 1 | none detected |
| court_02__rotation | date | `2026-11-05` | 1 | 2026-10-21 |
| court_02__shadow | date | `2026-10-21` | 1 | none detected |
| court_02__shadow | date | `2026-11-05` | 1 | none detected |
| court_02__shadow | id | `SYNTHETIC-ONLY-004` | 1 | none detected |
| parking_01__perspective | date | `2026-10-21` | 1 | 2026-10-29 |
| parking_01__phone_mix | date | `2026-10-21` | 1 | none detected |
| parking_01__phone_mix | date | `2026-10-29` | 1 | none detected |
| parking_01__phone_mix | amount | `$45.00` | 1 | none detected |
| parking_01__phone_mix | id | `SYNTHETIC-ONLY-001` | 1 | none detected |
| parking_01__shadow | date | `2026-10-21` | 1 | none detected |
| parking_01__shadow | date | `2026-10-29` | 1 | none detected |
| parking_01__shadow | amount | `$45.00` | 1 | none detected |
| parking_01__shadow | id | `SYNTHETIC-ONLY-001` | 1 | none detected |
| parking_02__perspective | date | `2026-10-21` | 1 | 2026-11-02 |
| parking_02__phone_mix | date | `2026-10-21` | 1 | none detected |
| parking_02__phone_mix | date | `2026-11-02` | 1 | none detected |
| parking_02__phone_mix | amount | `$65.00` | 1 | none detected |
| parking_02__phone_mix | id | `SYNTHETIC-ONLY-002` | 1 | none detected |
| parking_02__rotation | date | `2026-11-02` | 1 | 2026-10-21 |
| parking_02__shadow | date | `2026-10-21` | 1 | none detected |
| parking_02__shadow | date | `2026-11-02` | 1 | none detected |
| parking_02__shadow | amount | `$65.00` | 1 | none detected |
| parking_02__shadow | id | `SYNTHETIC-ONLY-002` | 1 | none detected |
| school_01__perspective | date | `2026-10-21` | 1 | 2026-10-30 |
| school_01__phone_mix | date | `2026-10-21` | 1 | none detected |
| school_01__phone_mix | date | `2026-10-30` | 1 | none detected |
| school_01__phone_mix | id | `SYNTHETIC-ONLY-007` | 1 | none detected |
| school_01__shadow | date | `2026-10-21` | 1 | none detected |
| school_01__shadow | date | `2026-10-30` | 1 | none detected |
| school_01__shadow | id | `SYNTHETIC-ONLY-007` | 1 | none detected |
| school_02__perspective | date | `2026-10-21` | 1 | 2026-11-07 |
| school_02__phone_mix | date | `2026-10-21` | 1 | none detected |
| school_02__phone_mix | date | `2026-11-07` | 1 | none detected |
| school_02__phone_mix | id | `SYNTHETIC-ONLY-008` | 1 | none detected |
| school_02__rotation | date | `2026-11-07` | 1 | 2026-10-21 |
| school_02__shadow | date | `2026-10-21` | 1 | none detected |
| school_02__shadow | date | `2026-11-07` | 1 | none detected |
| school_02__shadow | id | `SYNTHETIC-ONLY-008` | 1 | none detected |
| utility_01__perspective | date | `2026-10-21` | 1 | 2026-11-04 |
| utility_01__phone_mix | date | `2026-10-21` | 1 | none detected |
| utility_01__phone_mix | date | `2026-11-04` | 1 | none detected |
| utility_01__phone_mix | amount | `$82.35` | 1 | none detected |
| utility_01__phone_mix | id | `SYNTHETIC-ONLY-005` | 1 | none detected |
| utility_01__rotation | date | `2026-11-04` | 1 | 2026-10-21 |
| utility_01__shadow | date | `2026-10-21` | 1 | none detected |
| utility_01__shadow | date | `2026-11-04` | 1 | none detected |
| utility_01__shadow | amount | `$82.35` | 1 | none detected |
| utility_01__shadow | id | `SYNTHETIC-ONLY-005` | 1 | none detected |
| utility_02__perspective | date | `2026-10-21` | 1 | 2026-11-06 |
| utility_02__phone_mix | date | `2026-10-21` | 1 | none detected |
| utility_02__phone_mix | date | `2026-11-06` | 1 | none detected |
| utility_02__phone_mix | amount | `$37.20` | 1 | none detected |
| utility_02__phone_mix | id | `SYNTHETIC-ONLY-006` | 1 | none detected |
| utility_02__rotation | date | `2026-11-06` | 1 | 2026-10-21 |
| utility_02__shadow | date | `2026-10-21` | 1 | none detected |
| utility_02__shadow | date | `2026-11-06` | 1 | none detected |
| utility_02__shadow | amount | `$37.20` | 1 | none detected |
| utility_02__shadow | id | `SYNTHETIC-ONLY-006` | 1 | none detected |

## Options for the next checkpoint

1. Test the requested OpenCV preprocessing adapter against this same frozen corpus. It is the next local-only option and is not yet measured.
2. Configure the existing vision reader with a private environment key/model, then measure it on exactly the same images. Do not choose a winner from API capability claims alone.
3. After both are measured, implement and test the proposed hybrid agreement/dispute path. Only actual candidates displayed to the user may receive candidate-recall credit.
4. Add the six invented handwriting photo/truth pairs and re-run; no conclusion about handwriting can be drawn now.

Do not promote any of these options to the production default yet. Dedicated handwriting-OCR cloud options, cost/privacy/setup comparisons, and the editable text-check screen belong to the next requested checkpoints, not this no-fixes baseline.

## Limits and first review

Review the digit-normalization rules in DESIGN_NOTES.md, audit target_tokens in the JSON report, and visually inspect the shadow and combined samples first. The same eight source texts and a single font/layout are reused, so the images are correlated stress tests rather than an estimate for all real phones. The backend normalization is measured; the additional browser JPEG encode and actual camera optics are not simulated.

The full suite currently passes 86 tests, including M1 API privacy tests, with one pre-existing Python 3.9 asyncio deprecation warning. No full OCR transcripts or provider error responses are stored in the report.
