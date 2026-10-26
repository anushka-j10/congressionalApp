# Northeast parking-notice stress test

**Result: FAIL for unattended reliability. The run completed, but unsafe verified outputs remain.**

Two researched synthetic notices per state (CT, ME, MA, NH, NJ, NY, PA, RI, VT), each clean and degraded: **18 source notices / 36 image runs**. These are exploratory assistant-authored tests, not independent held-out evidence.

Sources checked October 26, 2026. Only the two Pennsylvania layouts were reconstructed after visual inspection of official sample tickets; the other sixteen are content reconstructions from official instructions, not exact replicas of unseen forms. All case identities/dates/sums are synthetic; public issuer/contact names are retained. Pittsburgh uses a historical 2018 sample.

## Results

| Measure | Recorded result |
| --- | --- |
| Strict case PASS | 10/36 (27.78%) |
| Strict case FAIL | 26/36 (72.22%) |
| Correct extracted values where truth is present | 92/128 (71.88%) |
| Correct values including expected missing/ambiguous | 103/144 (71.53%) |
| Strict false-verified, all four fields | 21/144 (14.58%) |
| Strict false-verified, deadline/amount/action | 15/108 (13.89%) |
| Strict mismatches among verified fields | 21/71 (29.58%) |
| MISSING or unverified, all field opportunities | 73/144 (50.69%) |
| Abstain when truth is present | 59/128 (46.09%) |
| Correct AND verified where truth is present | 50/128 (39.06%) |
| Correct missing (no value supplied) | 11/12 (91.67%) |
| Pipeline unavailable | 0/144 (0.00%) |

**Interpretation:** PASS means the four scored fields match the declared key (or its predeclared aliases) and the English explanation stage returns. It does not require every field to be verified. In particular, human amount confirmation was not simulated: all thirty present amounts remain unverified/missing by design.

The strict scorer checks normalized values, copied actions and declared contact aliases. It counts harmless extra source text/labels as failures. Six of the 21 strict false-verifications are supported extra text or label-only differences; they remain in the published counts. Other differences include minor OCR misspellings, conditional-deadline representation limits, and real wrong dates/contacts. Do not interpret 21/144 as 21 independently adjudicated harmful errors.

ME_02 correctly withholds a calendar date for its unsupported hours/weekend rule, but strict value scoring still marks its retained unverified rule wrong because the key is null. Similarly, safe refusal to normalize a relative deadline counts against coverage. Neither is a verified invented date.

## Highest-priority findings

1. **Date verification can preserve catastrophic OCR errors:** VT_01 clean verifies and displays November 25, **2926**, from a misread issue-year anchor. Expected: November 25, 2026.
2. **Inclusive counting is wrong:** VT_02 clean and degraded verify November **9**, although counting October 26 as day 1 makes the printed rule end November **8**.
3. **Contacts and timing inside actions inherit OCR errors:** ME_01 clean verifies `.ccm` instead of `.com`; NY_01 clean verifies `3C days` instead of `30 days` even while the standalone deadline is unverified.
4. **Complete instructions are not guaranteed:** ME_02 degraded drops the no-card/do-not-mail-cash sentences from its verified action.
5. **Conditional dates lose context:** PA_02 selects the real payment date as a single verified deadline despite a different contest deadline. The key explicitly requires abstention; this is a representation/policy failure rather than a fabricated date.
6. **Automatic classification is still unconfigured:** all 36 readings report unknown; this run explicitly selected parking_ticket. Issuing-agency strings also contain OCR corruption; agency is preserved in raw outputs but excluded from the historical four-field metric.

The English guard passed in all 36 runs with model-generated explanations and no reported guard failures. That checks consistency with extracted fields, not the truth of those fields: the bad year/date/contact survive into displayed English.

## Field results

| Field | Correct / truth present | Strict false-verified / all cases | Abstain / truth present |
| --- | --- | --- | --- |
| deadline | 12/26 (46.15%) | 5/36 (13.89%) | 17/26 (65.38%) |
| amount_due | 28/30 (93.33%) | 0/36 (0.00%) | 30/30 (100.00%) |
| required_action | 23/36 (63.89%) | 10/36 (27.78%) | 11/36 (30.56%) |
| contact | 29/36 (80.56%) | 6/36 (16.67%) | 1/36 (2.78%) |

## By state

| State | Cases passing | Value accuracy (present) | Strict false-verified |
| --- | --- | --- | --- |
| CT | 1/4 | 8/14 (57.14%) | 2/16 (12.50%) |
| MA | 0/4 | 11/16 (68.75%) | 0/16 (0.00%) |
| ME | 1/4 | 8/12 (66.67%) | 4/16 (25.00%) |
| NH | 1/4 | 10/12 (83.33%) | 2/16 (12.50%) |
| NJ | 4/4 | 14/14 (100.00%) | 0/16 (0.00%) |
| NY | 1/4 | 12/16 (75.00%) | 1/16 (6.25%) |
| PA | 0/4 | 9/14 (64.29%) | 4/16 (25.00%) |
| RI | 1/4 | 11/14 (78.57%) | 1/16 (6.25%) |
| VT | 1/4 | 9/16 (56.25%) | 7/16 (43.75%) |

## Clean versus degraded

| Variant | Value accuracy (present) | Strict false-verified |
| --- | --- | --- |
| clean | 45/64 (70.31%) | 12/72 (16.67%) |
| degraded | 47/64 (73.44%) | 9/72 (12.50%) |

Degradation sometimes changes OCR in a helpful direction; these correlated samples and one repetition do not establish that poor photos perform better.

## Each case

| Case | Issuer | Clean | Degraded | Routing with explicit state/issuer choice |
| --- | --- | --- | --- | --- |
| CT_01 | Hartford Parking Authority | PASS | FAIL | Official route: hartford |
| CT_02 | City of New Haven | FAIL | FAIL | Official route: new-haven |
| ME_01 | Freeport Police Department | FAIL | PASS | Unlisted issuer: fallback, no payment link |
| ME_02 | Maine Capitol Police | FAIL | FAIL | Unlisted issuer: fallback, no payment link |
| MA_01 | City of Boston Parking Clerk | FAIL | FAIL | Official route: boston |
| MA_02 | City of Cambridge Department of Transportation | FAIL | FAIL | Unlisted issuer: fallback, no payment link |
| NH_01 | City of Nashua Parking Department | FAIL | FAIL | Official route: nashua |
| NH_02 | Town of Hanover Parking Division | FAIL | PASS | Official route: hanover |
| NJ_01 | Jersey City Municipal Court | PASS | PASS | Official route: jersey-city |
| NJ_02 | Hoboken Municipal Court | PASS | PASS | Official route: nj-municipal |
| NY_01 | New York City Department of Finance | FAIL | FAIL | Official route: nyc |
| NY_02 | City of Kingston | FAIL | PASS | Unlisted issuer: fallback, no payment link |
| PA_01 | City and County of Philadelphia | FAIL | FAIL | Official route: philadelphia |
| PA_02 | Public Parking Authority of Pittsburgh | FAIL | FAIL | Unlisted issuer: fallback, no payment link |
| RI_01 | Providence Municipal Court | FAIL | FAIL | Official route: providence |
| RI_02 | City of Newport Parking Division | PASS | FAIL | Unlisted issuer: fallback, no payment link |
| VT_01 | City of Burlington Parking Services | FAIL | PASS | Official route: burlington |
| VT_02 | Town of Brattleboro Parking Enforcement | FAIL | FAIL | Unlisted issuer: fallback, no payment link |

Routing checks pass for **18/18** declared selections: **11/18** have a bundled route and **7/18** correctly fall back. The route checks execute the frontend selector function, not the external payment service. A person supplies the issuer; no OCR-based jurisdiction identification is claimed. Maine Capitol Police is not silently sent to the municipal portal, and Kingston is not sent to NYC.

## Reproduction and evidence

- Base application commit: `b5422683a713760cc5b6a6d6e2c339b577fd63d5`; application SHA-256: `e0c7594b6edf7a5a0da971e628da4217b133466ddd67693480a5bccedcf34674`. Backend/frontend files were unchanged throughout the run.
- Corpus manifest SHA-256 before calls: `280996a8f3a4956bd87f4b8423e02498017349c252d0dc666900d3e663e4b9bf`. All image/answer hashes still match.
- Started `2026-10-26T05:00:55.763880+00:00`; finished `2026-10-26T05:02:26.700762+00:00`.
- Local preprocessed reader; pinned `gpt-5.4-mini-2026-03-17` (the README/render.yaml model); temperature 0, reasoning none; reference date October 26, 2026; two workers; one measurement per image. These are pinned evaluation settings; HTTP/browser provider defaults were not measured. The ignored local env uses the unversioned `gpt-5.4-mini` alias, which this run does not override.
- Direct production component calls: image normalization → local OCR → extraction → deterministic validators → English explanation. No mocked reader or extractor. HTTP/CORS, deployed URL, mobile interaction, Spanish/Tagalog and read-aloud were not part of this stress run.
- OCR was confirmed unchanged; parking_ticket selected explicitly. No amount checkbox or human correction simulated. All fields, source snippets, raw OCR, proposals, explanation and token usage are retained in [results.json](results.json).
- [All failed cases in full](FAILURE_DETAILS.md), [qualitative review](qualitative-review.json), [visual gallery and provenance](gallery.html), [frozen manifest](../../eval/northeast_stress/corpus/manifest.json).
- Regression checks: **430 Python tests pass**, one existing Starlette/AnyIO deprecation warning; **60 JavaScript tests pass**. See [Python log](pytest.txt) and [JavaScript log](node.txt).
- Original held-out corpus, results and eval-freeze tag were neither rerun nor edited. This set cannot replace that independent evaluation. No production bug fixes or deployment are included.
- API key loaded only inside the process, sent only to the configured OpenAI API by existing clients, and checked against serialized synthetic results before writing. Keys, headers and provider error bodies are never logged. Synthetic test images/text are intentionally saved by this opt-in evaluation tool, not by the production upload path.

Exact commands, run from the repository:

```sh
../../work/m4-audit-venv/bin/python -m eval.northeast_stress.build
../../work/m4-audit-venv/bin/python -m eval.northeast_stress.run --dry-run
../../work/m4-audit-venv/bin/python -m eval.northeast_stress.run > ../../work/northeast-stress-run.log 2>&1
../../work/m4-audit-venv/bin/python -m pytest -q > results/northeast-stress/pytest.txt 2>&1
/opt/homebrew/bin/node --test tests/*.mjs > results/northeast-stress/node.txt 2>&1
../../work/m4-audit-venv/bin/python -m eval.northeast_stress.report
```

The build command refuses to overwrite an existing corpus; the live runner refuses a second run into the existing result directory. `--resume` processes only unfinished cases after matching hashes. On a new machine use the project dependencies plus python-dotenv (also used by the existing eval runner), Tesseract and a TrueType font. Report generation is offline and may be repeated.

## Source provenance

Each source describes a sample form or a local process. Synthetic case dates and amounts must not be used as real legal/payment guidance.

### CT_01: Hartford Parking Authority

Instruction-based reconstruction: citation includes a hearing date; payment and appeal are separate options.

- [Official source 1](https://hartfordparking.com/pay-or-appeal-citations/)
- [Official source 2](https://hartfordparking.com/wp-content/uploads/2024/11/Request-New-Hearing-Date__revised-11.2024.pdf)

### CT_02: City of New Haven

Official review-form content reconstructed; form layout was not visually inspected. No fine is supplied on this page.

- [Official source 1](https://www.newhavenct.gov/home/showpublisheddocument/2356/637744742739330000)

### ME_01: Freeport Police Department

State-hosted Freeport payment instructions identify ticket number at top and registration/state near the top; visual reconstruction.

- [Official source 1](https://apps1.web.maine.gov/cgi-bin/ePayment/online/disclaimer?sid=1937)

### ME_02: Maine Capitol Police

Instruction-based reconstruction: Capitol Police payment channel and 72-hour window excluding weekends; distinct from Augusta city tickets.

- [Official source 1](https://www11.maine.gov/dps/capitol-police/parking/paying-tickets)

### MA_01: City of Boston Parking Clerk

Reconstruction of a denied-appeal notice using official ten-day payment/hearing instructions; not a published letter specimen.

- [Official source 1](https://content.boston.gov/departments/parking-clerk/how-appeal-parking-ticket)

### MA_02: City of Cambridge Department of Transportation

Instruction-based reconstruction: pay/dispute within 21 days, fine schedule and separate transaction fee. Layout is synthetic.

- [Official source 1](https://www.cambridgema.gov/iwantto/payaparkingticket)

### NH_01: City of Nashua Parking Department

Reconstructed appeal acknowledgement based on official appeal form. The 21-business-day response is the agency response, not a resident deadline.

- [Official source 1](https://nashuanh.gov/DocumentCenter/View/14602/City-of-Nashua-Parking-Appeal-Form)
- [Official source 2](https://www.nashuanh.gov/978/Parking-Tickets-Violations)

### NH_02: Town of Hanover Parking Division

Instruction-based reconstruction: fourteen-day appeal/payment window and later fees; synthetic sums and absolute deadline.

- [Official source 1](https://www.hanovernh.org/785/Payments-and-Appeals)
- [Official source 2](https://www.hanovernh.org/m/faq?cat=23)

### NJ_01: Jersey City Municipal Court

Reconstruction from municipal/NJ Courts guidance: Court ID, ticket, payable amount and appearance condition; no visual-facsimile claim.

- [Official source 1](https://www.jerseycitynj.gov/CityHall/law/municipalcourt)
- [Official source 2](https://www.njcourts.gov/self-help/legal-reference-materials/your-day-court)

### NJ_02: Hoboken Municipal Court

Reconstruction of a parking-related summons with appearance required, based on the NJ Courts appearance distinction. No fine on the supplied page.

- [Official source 1](https://www.hobokennj.gov/resources/pay-a-parking-ticket)
- [Official source 2](https://www.njcourts.gov/self-help/legal-reference-materials/your-day-court)

### NY_01: New York City Department of Finance

Reconstruction from official parking ticket fields and thirty-day dispute guidance. Printed receipt layout is synthetic, not a camera notice.

- [Official source 1](https://www.nyc.gov/pl/main/services/parking-and-camera-tickets)
- [Official source 2](https://www.nyc.gov/site/finance/vehicles/dispute-web.page)

### NY_02: City of Kingston

Synthetic mailed parking notice using the city-specific payment-channel distinction. Official source does not publish the notice or fine schedule.

- [Official source 1](https://www.kingston-ny.gov/content/12525/12530.aspx)

### PA_01: City and County of Philadelphia

Visually inspected official stock, PDF page 8: blue-headed narrow thermal front and dense instruction reverse. Recreated side by side with invented ticket data and shortened original wording.

- [Official source 1](https://philapark.org/wp-content/uploads/RFP-No.-24-07-Addendum-3-12.30.24.pdf)

### PA_02: Public Parking Authority of Pittsburgh

Visually inspected 2018 not-valid sample: pink front/reverse, fine plus cost, total and escalating amounts. Historical layout, not a current fine/rule claim. Synthetic dates and shortened instructions.

- [Official source 1](https://www.pittsburghparking.com/files/sharedassets/public/v/1/about/documents/2049_parking_court_actual_enlarged_ticket_not_valid_for_web_3.16.18_ab.pdf)
- [Official source 2](https://www.pittsburghparking.com/About/Pittsburgh-Parking-Court?lang_update=639161161072708293)

### RI_01: Providence Municipal Court

Instruction-based reconstruction: fourteen/twenty-eight-day escalating parking fine schedule; ticket layout synthetic.

- [Official source 1](https://ppd.providenceri.gov/parking-ticket-payments/)
- [Official source 2](https://www.providenceri.gov/public-works/parkingfaqs/)

### RI_02: City of Newport Parking Division

Reconstructed parking violation/review notice using official review-before-payment option. No deadline has been added where the supplied notice has none.

- [Official source 1](https://www.newportri.gov/living-in-newport/parking-transportation/parkingviolationreview)
- [Official source 2](https://www.newportri.gov/en-us/living-in-newport/parking-transportation)

### VT_01: City of Burlington Parking Services

Instruction-based reconstruction: written/online appeal within thirty days; parking service contact. Layout and fine invented.

- [Official source 1](https://www.burlingtonvt.gov/m/faq?cat=40)
- [Official source 2](https://burlingtonvt.gov/314/Parking)

### VT_02: Town of Brattleboro Parking Enforcement

Instruction-based reconstruction of inclusive day counting: issue date is day one. The expected date is October 26 plus thirteen days, November 8.

- [Official source 1](https://brattleboro.gov/parking-citation-appeal-process)
