# Notice Decoder 2.0 — implementation prompt

Prepared October 26, 2026. This is a brief for the **next development cycle**, not a claim that the work below is complete. Copy the prompt below into a coding session with this repository attached. Recheck the repository and deployment state before acting.

---

Improve Notice Decoder, a phone-first PWA that helps people understand notices. Preserve Anushka Jain’s direction and the existing app style. Prioritize correctness and understandable uncertainty before expanding coverage. Work in small, reviewable changes with evidence for every improvement. Do not deploy merely because tests pass.

## 1. Establish the starting point

Read README.md, DESIGN_NOTES.md, FAILURES.md, docs/EVIDENCE.md, HELDOUT_RESULTS.md, DEPLOYMENT_RESULTS.md, AI_USAGE.md and results/northeast-stress/REPORT.md. Inspect the actual code and branch; documents can describe earlier versions. Record the starting commit, clean/dirty state, dependencies, model configuration without secrets, and relevant file hashes.

The final-polish work changes interface copy and presentation. It **does not repair the extraction failures** listed below. The visible “Text match” badge still corresponds to the existing API status `verified`; historical “false-verified” measurements retain that name and definition. Renaming the badge is not a reliability improvement.

The historical review branch is `design/mobile-format-review`; deployment uses `fix/notice-reliability`. The known live URL is https://notice-decoder-ns5o.onrender.com. October 26 release e25b3c1 deployed the polished interface and a clearer manual type selector. Read `results/release-2026-10-26/REPORT.md` and `RELEASE_CHECKLIST.md`: hosting and one synthetic language flow passed, full phone/reliability acceptance did not. Verify the actual current commit before further work. Do not move the existing `eval-freeze` tag or rewrite historical evidence.

## 2. What the current app actually does

| Function | Current behavior | Boundary to communicate |
|---|---|---|
| Opening and tutorial | Manual Continue, welcome, state selection, four illustrated steps, notice reader; centered Our story dialog at the bottom | No timed dismissal; returning users can skip the tutorial |
| Notice input | One photograph of a printed English page; JPEG, PNG, WebP and HEIC preparation | No multi-page merge, PDF workflow or measured handwriting reliability |
| Text reading | Default server-side local preprocessed Tesseract, with reading differences highlighted | “Local” means our server, not offline/on-device OCR; matching readers can both be wrong |
| Human review | Editable transcript, notice-type choice, separate text and amount confirmations | Confirmation is a user assertion, not independent proof; users can miss errors |
| Document types | Parking ticket, court notice, utility bill, school letter | All four production signal lists are empty; automatic classification returns unknown. Users must choose the type |
| Extraction | A server-side model proposes issuing agency, deadline, amount, required action and contact, with source snippets | Field selection can be wrong even if every character occurs in the reviewed text |
| Checks and cards | Deterministic checks produce `verified`, `unverified`, `missing`; UI says Text match, Needs review, Not identified; source inspection is available | Not identified does not mean absent. Checked text is not the original image or proof of an obligation |
| Explanation | Uses fields that passed checks; checks generated numbers and facts, with a bounded fallback | It can faithfully repeat a wrong extracted fact. Passing language checks does not validate the original notice |
| Languages and speech | English, Spanish and Tagalog; failed translation checks fall back to English; matching browser/device voice reads the result | Glossary and UI translations remain unreviewed by native speakers; voice availability depends on the device |
| Parking resources | User chooses the issuing state and issuer; allowlisted official resources for 12 routes across CT, ME, MA, NH, NJ, NY, PA, RI and VT | Eleven of the 18 stress cases have a matching route; seven use a safe fallback. No complete state/city coverage, automatic jurisdiction determination, ticket lookup, payment or appeal submission |
| Privacy and operation | Normal request paths use memory/no-store, server-only secrets; language preference persists; online processing is required | Confirmed text goes to OpenAI; optional vision/hybrid sends images too. Do not promise provider retention control, secure RAM erasure or universal host/library logging behavior |

Keep those boundaries visible where they affect a decision. Do not turn the interface into a long disclaimer page. Keep detailed evidence in docs and concise guidance beside relevant controls.

## 3. Evidence that must remain intact

The exploratory Northeast run at `bbfb6c6` contains 18 assistant-authored synthetic notices, two per state, each clean and degraded: **36 runs**. The input/answer manifest was fixed before the run. Only two Pennsylvania layouts were based on inspected sample ticket PDFs; sixteen reconstruct official instructions. Do not describe all of them as exact replicas or representative real tickets. The assistant authored the corpus and key; this is not an independent held-out study.

Source of truth: `results/northeast-stress/results.json`, `run.json`, `records.jsonl`, `qualitative-review.json`, `FAILURE_DETAILS.md`, and `eval/northeast_stress/corpus/manifest.json`.

| Measure | Recorded result |
|---|---:|
| Strict four-field per-case PASS | 10/36 |
| Correct present fields, regardless of status | 92/128 |
| Strict false-verified / all four-field opportunities | 21/144 |
| Strict mismatches / verified fields | 21/71 |
| Abstain when a true field is present | 59/128 |
| Correct and verified / true present fields | 50/128 |
| Missing or unverified / all opportunities | 73/144 |
| Directory route/fallback assertions | 18/18 |

| Field | Correct / present | Strict false-verified / opportunities | Abstain / present |
|---|---:|---:|---:|
| Deadline | 12/26 | 5/36 | 17/26 |
| Amount | 28/30 | 0/36 | 30/30 |
| Required action | 23/36 | 10/36 | 11/36 |
| Contact | 29/36 | 6/36 | 1/36 |

Six of the 21 strict false-verified mismatches were manually identified as harmless extra supported text or labels. Preserve the original strict score and separate these notes; they are not an independently adjudicated replacement score. Other mismatches include actual wrong dates and contact details. Agency was returned but was not in the four-field scoring denominator. All 30 present amounts were withheld because this unattended run did not assert human amount review. Zero verified amount errors therefore does not demonstrate successful amount verification.

The run used explicit parking-ticket selection, unchanged OCR confirmation, `amounts_confirmed=false`, local preprocessed OCR, English explanations, one repetition and pinned model `gpt-5.4-mini-2026-03-17`. Recorded temperature/reasoning settings differ from unspecified production defaults; use `run.json`, not assumptions, for replication. It did not test deployed HTTP behavior, real phones, Spanish/Tagalog output quality or audio.

Earlier full dev results: critical false verification 0/120, correct verified 72/92, abstain 20/92. Original held-out result at the earlier freeze: critical false verification 4/30, present critical accuracy 18/24, correct verified 14/24, abstain 6/24. Different sets, code and scorer versions prevent a controlled before/after comparison. Do not collapse them into one accuracy claim.

## 4. Priority 0 — correctness failures

Fix these before expanding states or claiming the app is reliable. Read each full failure record and reproduce it with the saved OCR/model proposal first. Use generic policies, not hardcoded issuer names, test IDs, amounts or answers.

| Failure and evidence | Required repair | Acceptance evidence |
|---|---|---|
| October 26 iPhone report: a linked angled real ticket reproduced locally with a truncated deadline year, corrupted agency and **5 → S** in a contesting clause. Original-image OCR recovered the date but also missed the clause; generic quality heuristics gave no additional warning | Reproduce on privacy-safe, independently keyed synthetic captures of dense ticket tables and instructions. Improve reading or abstain on incomplete numeric clauses; do not silently pick one reader or hardcode this notice. Inspect cropped-page behavior | Source and screenshot variants, both local/deployed Tesseract versions, correct and corrupt controls; test retained conditions and source coverage. Measure false-verified rate and useful coverage, not just OCR character count. Keep real images/identifiers out of public fixtures |
| `VT_01` clean: issue year 2026 read as **2926**, producing a checked deadline of **2926-11-25** | Treat suspicious anchors as uncertain; introduce documented plausibility and anchor-review checks. Do not silently change 2926 to 2026. Define behavior for old notices and legitimate future dates | Corrupted and plausible controls; suspicious dates withheld from cards, countdown, explanation and speech until adequately resolved |
| `VT_02` both variants: issue day counts as day 1; correct deadline **2026-11-08**, output **2026-11-09** | Support explicit inclusive counting, including its source evidence, or abstain. OCR “day I” must not silently lose the qualifier | Explicit day-1, ordinary exclusive, unreadable convention, month/year rollover and leap-date cases; prove no off-by-one result is presented as checked |
| `ME_01` clean: `.com` becomes **`.ccm`** in an email and passes checks | Separate a copied contact string from independently confirmed contact information; retain photo comparison. Do not silently repair domains or turn unconfirmed strings into links | Valid-looking OCR typos, real unusual domains, line wrapping, phone extensions and malicious URL strings; unsupported contacts remain uncertain |
| `NY_01` clean: **“30 days” → “3C days”** in a checked action even though the separate deadline is unverified | Validate critical tokens inside actions and enforce consistent uncertainty across dependent fields | Letter/digit confusions, amount/date disagreement, and positive controls. Bad timing cannot survive inside action, explanation or speech merely because the standalone deadline was withheld |
| `ME_02` degraded: action drops **“No debit or credit cards are accepted. Do not mail cash.”** | Check completeness of material restrictions, exceptions and prohibitions across sentence boundaries | Multi-line instructions, negative clauses and conditional alternatives. Keep all required constraints or withhold the incomplete action |
| `PA_02` both variants: real payment date is selected as the sole deadline while contest timing differs | Represent payment and contest obligations separately, or abstain from a single deadline when ambiguous. Never imply paying is the only option | Different pay/appeal dates, hearing alternatives, early-discount vs full-rate schedules and conditional eligibility. Each displayed date remains tied to its action and source |

Additional checks:

- Preserve the invariant that an absent source snippet cannot pass source matching. Test Unicode, punctuation normalization, approximate matches and model-created snippets.
- A notice without a deadline must remain without one. Do not use an unrelated issue date, event date, jurisdiction default or current date as a substitute.
- Relative dates need an explicit, validated anchor and counting rule. Unsupported business-day, weekend, holiday, receipt/service-date and hour-based rules should abstain. Do not import legal rules from memory or silently add them to the notice.
- Separate “source-supported,” “human reviewed,” “field role checked” and “uncertain” in the data model. Do not call a value image-verified just because the user ticked a global checkbox or two OCR passes agree.
- Keep amounts withheld without the required review. Measure human-assisted and unattended paths separately, including a careless-confirmation scenario.
- Check agency extraction and add agency truth to a clearly versioned five-field scorer. Preserve comparable four-field results alongside it.
- English consistency checks and translation checks must reject unsupported numbers and preserve conditions/negations. A downstream language guard cannot compensate for a bad upstream fact.
- Treat every notice and source website as untrusted content. Instructions embedded in a photo or snippet cannot alter extraction policy, reveal secrets, choose URLs or bypass checks.

Preferred sequence: add reproducing tests, repair one general failure class, run focused tests plus existing regressions, then report accuracy **and** coverage. Stop at a defensible abstention if a reliable rule cannot be implemented. Do not improve the error metric by withholding everything without disclosing the coverage loss.

## 5. Priority 1 — user comprehension and access

Preserve the chosen visual direction: system sans-serif, cool palette, centered main headings, rounded photo actions, compact results, expandable sources and explanation, no decorative side/top tabs. Keep the manual title screen and bottom centered Our story dialog. Avoid repeated headings and excessive scrolling.

- Validate the review step with actual users. Can they distinguish original photo, OCR reading, edited text and model result? Can they tell that an omitted field might still be on the page? Test the meaning of “Text match” without coaching them.
- Investigate a focused photo/text comparison for critical tokens. This is a proposed improvement, not a current capability. Keep review usable without requiring users to understand OCR terminology.
- Keep type selection explicit while classifier signals are empty. `backend/classifier/signals.py` was reserved for AJ’s work. Ask for AJ’s signals or explicit authorization for a disclosed proposal; do not fabricate student authorship. Report classifier accuracy independently of manually supplied types.
- Have qualified/native reviewers assess Spanish and Tagalog UI, glossary and full output meaning, including deadlines, negation and alternatives. Record reviewer-approved wording and dates honestly. Do not mark machine-generated translations “reviewed.”
- Test iPhone Safari and Android Chrome: camera permission and cancellation, image orientation, HEIC, photo-library selection, text editing, long translated labels, keyboard navigation, large text, screen reader announcement/focus, 44px touch targets, contrast and reduced motion. Record browser/device versions and whether each result was physical-device or desktop emulation.
- Test language switching during an in-flight request, missing voices, pause/resume/stop, English fallback voice selection, page leave and clear. Never play stale-language audio after a new notice or language choice.
- Local help resources are currently unconfigured. Research and confirm real contacts and scope before adding them; do not invent a helpline or imply an organization has endorsed the app. Original-notice contact details remain useful but can be misread.

## 6. Priority 2 — coverage and operations

**Jurisdiction resources:** keep the issuer, not residence, as the routing decision. Maintain source URL, exact jurisdiction/issuer, supported notice category, checked date and fallback for every route. Recheck official sources before expanding. Private/campus/airport issuers and unlisted municipalities must never inherit a state’s generic payment portal. Do not navigate or submit payments automatically. Clearly distinguish official links from facts extracted from the notice. Add link-maintenance tests and an owner review procedure before considering all 50 states.

**Input expansion:** multi-page notices, PDFs, non-English source OCR and handwriting are separate proposals. Require representative data, privacy review and acceptance criteria before implementation. Do not advertise these simply because a library can accept the file.

**Deployment:** verify the actual deployed commit, HTTPS origin, static manifest/icons, service-worker updates, no caching of APIs, CORS, server-only credentials, quota errors and a complete synthetic notice flow. Check free-host cold starts and slow-network UX. A loaded homepage is not proof that extraction works.

**Budgets:** the current production `AnalysisBudget` is global per process: 30 analysis requests/minute, 240/hour, one concurrent request across `/api/read`, `/api/extract`, `/api/explain`. It resets on restart, requires a single worker and is not a dollar spend cap. Design a real cost-control strategy before scaling. Maintain fixed friendly quota/unavailable errors, no secret/provider error echoes, and bounded retries. Avoid adding user identifiers or request-body logging for convenience.

**Privacy:** keep .env ignored/untracked and mode 0600; secrets in host environment variables only. Never output a key or place it in client code, URLs, screenshots, fixtures or git history. Use safe synthetic credentials in tests. Check app, library and host logging separately. Keep notice images, text, receipts and results out of browser persistent storage and server logs on normal paths. Synthetic evaluation fixtures intentionally persist outside the served frontend; document the distinction. Do not claim secure memory erasure or control over provider retention.

## 7. Evaluation rules and release gates

1. Preserve the original held-out set, hand-written key, one-run ledger, tag and reports. **Do not run it again as a new held-out test.** Never alter an answer to make the app pass. Report suspected key typos to AJ.
2. Preserve the Northeast corpus, key and raw outputs. These seen cases may now be regression/development material. Write any new run to a new directory with a new run ID, configuration, hashes and versioned scorer. Do not overwrite `results/northeast-stress/`.
3. Keep answer keys fixed before model runs. Have an independent human create/review a fresh held-out set covering issuer/layout diversity, poor captures, missing fields, multiple obligations, conditional dates, restrictions, source-language limits and prompt injection. Freeze before that new study.
4. Run full/B1 plain-translate/B2 no-validator methods on the same declared cases and run settings. Replay ablations on the same proposals, disabling one validator group at a time. Record precisely what each baseline and ablation bypasses.
5. Report raw per-case output and full failures, per-field accuracy, strict false-verified/all opportunities, error fraction among checked fields, correct checked coverage, missing/abstain rate, unavailable rate, latency and usage when available. Include denominators, all repetitions and manual adjudication separately. Do not round up or silently average away catastrophic errors.
6. Explicitly distinguish a safe abstention, harmless wording mismatch, missed constraint, wrong fact and unavailable result. Do not change scoring rules after seeing outputs without retaining the original score and explaining the new version.
7. Require reproducing regressions to pass for every Priority 0 bug, no unsupported verification on the known adversarial/source/no-deadline cases, and a coverage report. Ask AJ to approve quantitative acceptance thresholds and the independent study plan before freezing the new release; do not retroactively choose thresholds to match results.
8. Update README, FAILURES, EVIDENCE and DESIGN_NOTES from actual runs only. Separate local tests, component integration, deployed endpoint checks and physical-phone testing. Leave unperformed checks visibly pending.
9. Maintain honest AI_USAGE and submission materials: Codex wrote much of the code under AJ’s direction. Only AJ can confirm personal design, writing, review and authorship specifics. Do not imply completion of empty classifier signals or unperformed human reviews.
10. Before release, provide a concrete reviewable diff, exact commands, test counts, changed behavior, unresolved risks, known deployment state and rollback plan. Deploy only with authorization for that release. Recheck the deployed URL afterward.

## 8. Expected deliverables

- A prioritized issue list distinguishing correctness bugs, unmeasured behavior, product scope and human decisions.
- Small changes with reproducing tests for the correctness failures; schema migration notes if multiple obligations are introduced.
- Updated phone UX that communicates evidence and uncertainty without adding repetitive warnings or decorative clutter.
- Versioned evaluation outputs with immutable historical evidence and honest comparisons.
- Deployment/physical-device acceptance records and an explicit release decision with remaining gaps.
- No claims that all states, handwriting, multilingual source documents, legal correctness or real-phone operation work without supporting measurements.

Start with the Priority 0 reproduction and repair plan. Do not start visual redesigns, account systems, payment handling, analytics or other unrelated features.
