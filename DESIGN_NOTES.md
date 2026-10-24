# Design notes for student review — Milestones 2–3

These are editable notes for student review. A1/A2 below preserve historical
reader choices and measurements; the current A3/Part B proposal is appended.
Current M3 decisions are appended below; earlier checkpoint statements are historical.
The student authorized a generated schema/validator proposal on 2026-10-22,
but this does not count as independent student authorship or live acceptance.

## A1 baseline configuration (historical snapshot)

The checked-out default is `TEXT_READER=tesseract`, executable `tesseract`, English
language data, page segmentation mode 3, and a 35-second OCR timeout. Tesseract is
5.5.3 locally. The backend applies EXIF orientation, a maximum 1600px long edge,
and JPEG quality 90; it does not deskew, denoise, adaptively threshold, or upscale.
The browser also prepares JPEGs before upload; the A1 harness exercises the backend
normalization and reader directly and does not simulate that extra browser encode.

There is no `.env` file or configured API key/model in this checkout. The existing
vision adapter would use its environment model, high image detail, `store=false`,
and at most 12,000 output tokens; no live vision call was made. No reader, runtime
normalization, API, classifier, or frontend code changed during A1.

## Character error rate

CER is exact Levenshtein insertions + deletions + substitutions, divided by the
number of ground-truth characters. Unicode NFKC and collapsed whitespace remove
layout-only differences before scoring. Case, punctuation, spelling, and digits
still count. Corpus CER sums edit counts and reference lengths before division;
it does not average differently sized pages equally. CER can exceed 100% if the
reader inserts enough text. A failed reader call is empty text, not a skipped page.

## Key-token recall

The denominator is the count of dates, dollar-prefixed amounts, and labeled
reference/case/ID/citation/ticket/account values in the ground truth. Repeated
occurrences count repeatedly; one correct OCR occurrence cannot cover two missing
ones. We divide matched occurrences by expected occurrences across the corpus.
The report saves the detected target inventory so the student can audit coverage.
The scripted fixtures have a checked inventory: 16 dates, four amounts, and eight
reference IDs across eight source pages, or 28 target occurrences per variant.

These are measurement normalizations, not Part B field validators:

- Numeric dates retain digit order and leading zeroes while tolerating cosmetic
  spaces/separators. English month-name dates are supported as written; this does
  not equate abbreviated and full month names or convert US dates to ISO meaning.
- Amounts ignore currency marks, thousands commas, and spaces and compare exact
  decimal values to cents. An otherwise exact decimal without `$` may match.
  A broken digit is never repaired to make the amount match.
- IDs ignore letter case and cosmetic separators/spaces. All letters and digits
  must match; there is no `O→0`, `l→1`, `S→5`, fuzzy, or substring credit.
- Recall checks for a whole token anywhere in OCR text, independent of whether
  its label was recognized. It is not field association or proof that a date was
  interpreted as the right deadline.
- Extra hallucinated tokens do not lower recall; CER may reflect them. A high
  recall alone therefore cannot establish safe extraction or precision.

Future handwritten pages may contain formats the detector does not recognize.
Audit `target_tokens` before accepting their scores; a zero-token page has N/A
recall, not 100%. Missing/ambiguous/empty image-truth pairs stop the run. The
scoring implementation here was explicitly requested for A1; the student's later
field-evaluation scoring, extraction schema, and deterministic validators remain
separate and unimplemented.

## Corpus construction and preservation

Four M1 pages already had mild photo effects. Those eight original images and
JSON files are preserved byte-for-byte and reported as `legacy_m1`, not mislabeled
as eight clean pages. Clean counterparts use the same original content/layout.
Each has six separately labeled variants (rotation, perspective, blur, shadow,
noise, JPEG compression) and one combined `phone_mix`: 56 degraded images total.
All have exact visible-text ground truths generated from the same rendering source.

The fixed parameters live in `eval/reader-corpus.json`, including 3.5° rotation,
a fixed perspective transform, 1.3px Gaussian blur, a 105–245 light gradient,
seeded uniform noise up to about 16 levels, and JPEG quality 25. Combined effects
use 2.2° rotation, 0.85px blur, and JPEG quality 30 along with perspective, shadow,
and noise. Other individual variants use JPEG quality 90. Parameters were fixed
before the first run and were not adjusted to improve a reader's score.

This is a repeatable stress set, not a representative population of phone photos.
The same eight texts share one font and layout, so 64 printed images are not 64
independent documents. Real photographed, cropped, tiny-text, and handwritten
notices still need separate testing. No handwriting has been fabricated using a
font and reported as a measured human handwriting photo.

## Reports, privacy, and extensibility

`eval/reader_bakeoff.py` accepts built-in existing readers or a trusted local
`--factory module:function` that returns another TextReader. All receive the same
M1-normalized bytes. This permits the A2 comparison without changing the API just
for evaluation. Missing vision credentials are NOT RUN, never perfect scores.

Reports contain metrics, target tokens, actual transcribed candidate tokens for
misses, settings, and fingerprints. They do not save entire OCR transcripts or
provider error text. These reports concern invented evaluation data only; the
API still never writes notice images or text to disk. Tests verify the old API
privacy paths still pass. No real notice or personal data belongs in this corpus.

Hybrid agreement has not been implemented or scored. When A2 adds it, candidate
credit must come from both actual reader outputs and must cover only candidates
the UI really shows; appending ground-truth values or silently fixing digits would
invalidate the comparison. CER should describe the displayed transcript, while
candidate recall must be separately identified so it is not confused with exact
single-transcript accuracy. Agreement between two readers is not proof of truth.

## Gate and review

The unchanged baseline reaches 154/224 printed key tokens, or 68.75%, and fails
the 95% threshold. This is not a chosen-reader gate pass: reader selection and
A2/A3 remain pending. No Part B implementation should start on this evidence.
Review the normalization rules, the difficult images, and the missed-token list
before approving A2. Do not switch production defaults based on unmeasured vision
or preprocessing claims.

## A2 comparison — proposed readers, selection still pending

A2 adds `preprocessed` and `hybrid` behind the existing TextReader interface; it
does not select them as the production default. `TEXT_READER=tesseract` remains
the template/default. The A1 descriptions above are the historical baseline;
production adapters and candidate presentation now include the A2 work below.
Part B schemas, validators, and extraction are still absent.

### Local preprocessing decision

The separate OpenCV adapter decodes to grayscale, uses a 3px median filter,
estimates tilt from at least five long text-edge Hough segments within ±10°,
and deskews only when there is enough evidence. It upscales by up to 2x with a
3200px long-edge cap, applies Gaussian adaptive thresholding (51px neighborhood,
constant 15), adds a 20px white border, and passes an in-memory binary PNG to the
unchanged English/PSM-3 Tesseract engine. Parameters are recorded in the report.
No labeled condition or ground-truth text is available to the reader.

This single preprocessing recipe was chosen before scoring the full corpus; it
was not optimized separately for each fixture. The initial shadow smoke test
checked that the adapter worked, then the same recipe was used on all images.
On the frozen printed set, it recovers 224/224 key targets (100%), compared with
154/224 (68.75%) for M1. Degraded CER is 0.59%, compared with 29.09%. Remaining
non-key transcription errors still matter for future required-action extraction.

The numeric printed threshold is met by this measured local option, but final
reader selection is the student's decision. This evidence does not establish
handwriting support, confidence calibration, or real-phone generalization.

### Hybrid rules and actual candidate evidence

The hybrid runs preprocessed local OCR and the configured vision reader. The
local transcript is the primary transcript unless it is empty or unavailable,
in which case an available vision transcript is used. This is an explicit display
policy, not a claim that local OCR is always more accurate.

Candidate detection finds dates, dollar/labeled amounts, and labeled IDs from
actual reader text with source spans. It keeps likely OCR letter confusions
literally and never turns O into 0, l into 1, or S into 5. Signed amounts retain
their sign. Cosmetic separators/case and exact decimal amount formatting are
normalized for comparison; calendar meaning or field roles are not inferred.

Sequence alignment compares ordered candidate kinds and normalized values. Only
matched identical values get `agreed`; unmatched alternatives get `disputed`,
including one-reader failures. Each candidate retains its actual reader, text,
and offsets. All alternatives are returned by the API and shown in the browser;
primary-text disputed spans are highlighted. Neither label means `verified`.

Candidate recall is distinct from transcript recall/CER. A one-to-one matching
step gives each displayed review group credit for at most one expected occurrence,
so a list of alternatives cannot cover two missing fields at once. The scorer
uses exactly the candidate payload the UI renders; it never gives credit for a
correct token that is hidden in a transcript or invented from ground truth.

### Provider comparison and quota

The API key/model are configured privately by the user. The first synthetic
vision preflight returned HTTP 429 (rate/quota limit); the full provider run was
stopped without repeated failed calls. This does not establish a valid model
comparison, successful model access, or handwriting accuracy. Vision and hybrid
are explicitly NOT RUN while quota is unresolved.

The preflight's successful output, if available on a future run, stays in a
per-run RAM cache reused by both the vision and hybrid rows. Other matching
normalized images are also reused in RAM, reducing duplicate paid requests.
No transcripts are cached on disk, and no provider error body is included in
reports or request logs. Timing includes cache effects and evaluation overhead;
it should not be quoted as uncached user-facing latency.

### Privacy and UI checks

The original API privacy tests remain, plus a real preprocessed OCR request test
that forbids disk-backed Python notice temp files and checks for leftovers.
Unit tests cover changed digits, signs, duplicate values, missing readers, actual
candidate provenance, primary-reader choice, and one-to-one candidate scoring.
The browser renderer was checked at a 390px viewport with explicitly labeled
synthetic test doubles: both disputed amounts appear, the primary amount is
highlighted, and literal script-looking text is displayed without execution.
That renderer test is not a live vision result or a physical-phone test.

The editable “Check the text” screen and likely-handwriting/region confidence
work remain A3; the minimal A2 candidate display exists so candidate metrics refer
to values the user can actually see. This checkpoint adds no extraction endpoint,
translation, or deployment change. Dedicated OCR alternatives are listed only in
`eval/reports/handwriting-cloud-options.md`; no services were set up.

## A3 / Part B proposal — 2026-10-22

### Selection and gate

The student explicitly chose the measured local preprocessed reader. Default,
`.env.example`, and only the private `.env` reader entry now select it. The existing
224/224 printed key-token result passes the numerical gate; it does not establish
real-phone or handwriting performance. No handwriting fixtures were supplied;
confidence/handwriting detection remains limited to honest warnings and literal
unreadable markers, plus actual hybrid disputes if that mode is explicitly used.

### Data boundary and proposal ownership

The student explicitly authorized Codex to generate a proposed implementation of
the formerly student-owned schema and deterministic validators for review. The
student should edit the policies below and record their own contributions; no
authorship credit transfers merely by approval. Classification signals remain
empty and student-owned. The user chooses the document type explicitly in the
confirmation screen; unknown types abstain without a model request.

`ProposedNotice` defines five core evidence fields, inherited by four concrete
Pydantic document types. A model field has only nullable value/source keys;
deadlines also carry kind, days, and separate issue-date evidence. Nullable keys
are required so omissions/extra status flags fail schema validation. The model
cannot set `verified`; only `checked_field` does. `CheckedField` carries actual
source offsets, optional normalized values, computed days and anchor offsets.
This uniform core is a proposal, not a claim that all document types need the same
future domain rules. The student may refine individual classes after reviewing
real requirements.

### Source matching

Normalization uses NFKC, casefolding and collapsed whitespace, retaining original
Python code-point offsets for source highlights. Exact normalized matching is
preferred; longer snippets can match contiguous token windows at >= .94 similarity.
Fuzzy matching is limited to letter/layout noise: every digit sequence must be
identical, including leading zeroes. No O/0, l/1 or S/5 repair is allowed. Numeric
and ID boundaries prevent accepting a prefix inside a larger value or dropping
a negative sign. Short fuzzy evidence is rejected; uncertain evidence abstains.
The threshold is a conservative proposed policy, not calibrated confidence.
Frontend highlights convert Python offsets to Unicode code points before slicing,
so a preceding emoji does not shift extracted-source highlights.

### Dates and relative rules

Absolute dates accept US month/day/year, ISO dates, or English month names with
four-digit years, using calendar validation and leap-year rules. Numeric dates
are explicitly US order; two-digit years, missing years, unsupported strings,
impossible dates, and snippets containing competing numbers/dates abstain.
A parsed proposed date must equal the one parsed from both its own snippet and
the actual matched confirmed text. Calendar interpretation can normalize ISO and
US spellings, but source-snippet digits cannot differ from original source digits.

Relative support is intentionally narrow: “within N [calendar] days of/after the
issue date/date above/date of this notice,” 1–365 days, plus an explicitly labeled
Issued/Issue date/Date of notice anchor. Both the relative rule and anchor must
match the text; the model's day count must match the literal rule. Code, not the
model, adds days. Business days, receipt dates, holidays and missing/ambiguous
anchors abstain. `get_today` uses America/New_York and is injectable; tests pin
2026-10-22. Derived dates/days only appear after successful verification.

### Amounts and copied text

Amounts are Decimal USD values with valid comma grouping, optional dollar mark,
zero or two decimal places, no negatives, and range 0–1,000,000. The range is a
student-editable app sanity bound, not an official rule. Proposed value, snippet
and actual source must independently parse to the same amount. Multiple amounts,
extra competing numbers, malformed grouping and letter/digit confusions abstain.
Copied text fields must be whole phrases in their snippets; paraphrase is not
allowed to become verified merely because its topic is similar.

These checks establish source consistency only. They do not prove role/semantic
selection (e.g. issue date vs deadline or original charge vs late fee), authenticity,
complete extraction, legal interpretation, or general prompt-injection safety.
The UI makes this limitation explicit. M4 must measure wrong-field selection and
false verification independently; current tests cannot substitute for that work.

### Requests, failures, privacy and current evidence

`/api/extract` accepts bounded confirmed text, a known/unknown enum, and literal
boolean confirmation. It accepts no image, echoes no validation input on errors,
returns no-store headers, and logs only metadata. `ModelExtractor` uses the model
configured on the server, strict JSON Schema, `store=false`, no tools, and no
hardcoded temperature. Refusals/incomplete/malformed envelopes never reach the
cards. Transient/malformed failures get at most one retry with .5s backoff;
auth/config errors and refusals do not. Provider messages and exception contents
are never returned. No notice data is written to files/caches by these modules;
ordinary in-memory object lifetime is not secure RAM erasure.

The production design follows the official Responses Structured Outputs format:
https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses
Strict schema ensures structure, not truth; plain-code checks remain separate.
The actual 2026-10-22 live attempt returned 429, stopped after one fixture and one
retry, and left remaining samples NOT RUN in the integration report. Failed-call
usage/cost is unknown; no field accuracy was measured. Browser testing used an
explicit synthetic extractor with actual OCR/validators, not a live API result.

Review the schema and policies above first, then try the confirmed-text flow on
an invented phone photograph once API quota is available. M2 is not fully accepted
until live extraction and the physical-phone check work. No M3 or M4 work begins
at this checkpoint.

Clear/page leave aborts the browser fetch and advances a request generation.
Every async preparation/read/extraction completion checks that generation before
changing UI state; a late reply cannot restore data or unlock a newer operation.
The server may still finish processing an already transmitted request; cancellation
is not a claim of recalling data already sent. Four deterministic Node controller
tests cover late read/extract replies, page leave, and edit invalidation.

## M2 readiness correction: signed monetary evidence — 2026-10-22

An extra audit probe found `Amount due: ($45.00)` could be source-matched and
then incorrectly verified as positive `$45.00`: the money-token search discarded
the parentheses before calling the stricter numeric parser. New regression cases
reproduced this at both validator and API levels before the fix.

`one_amount` now rejects parentheses anywhere in a supplied/matched amount snippet,
including incomplete ones, rather than interpreting or deleting them. It also
checks surrounding Unicode-minus and trailing-sign context before parsing the
captured token. `whole_span` prevents both dollar-prefixed and digit-only snippets
from clipping adjacent signs/parentheses out of the evidence. These are general
rules; no sample ID or fixture-specific text is used. They deliberately leave even
potentially harmless parenthetical amount snippets unverified rather than guessing.
Ordinary positive and zero dollar values remain supported.

The regression cases check that unsupported evidence yields `unverified` and no
normalized positive value; the UI therefore uses its existing Please double-check
state. Passing these cases is not a measured corpus false-verified rate or proof
that every monetary/semantic ambiguity is covered. The live M2 extraction run
still needs API quota to be resolved, and M3's explicit precondition remains unmet.


## M3 implementation and review — 2026-10-23

### Preconditions and ownership

Live M2 read/extract and the text-confirmation/status flow now work; the chosen
reader remains local preprocessed Tesseract. Explicit source-matched absence labels
for amounts/deadlines now produce missing rather than an absence string proposed
as a value. Unicode decimal digits participate in exact numeric comparisons after
NFKC, preventing a changed non-ASCII contact number from passing as letter noise.
Physical-phone and handwriting evidence remains outstanding. Empty student classifier
signals still yield unknown; the user explicitly selects a type for extraction.
All generated schemas/validators and M3 mechanical checks are disclosed proposals;
no student-owned M4 field/false-verified evaluation was generated or run.

### Verified-only explanation and status integrity

The server creates a short-lived HMAC receipt over the exact document type, checked
fields (including statuses), today and issued timestamp. Its secret is independent
random in-memory bytes, never the API key. `/api/explain` rejects modified, expired
or restarted-server receipts before a model call. TTL is one hour; a server restart
requires re-extraction. Multiple independent workers would require a deliberately
shared signing secret or routing design before deployment; current local preview
uses one process. This stateless binding stores no notice history and provides no
account authentication or public-service rate limiting.

English generation receives verified values/snippets and fixed messages/statuses
for uncertain fields. Unverified/missing values AND snippets are withheld. The
model must return exact card facts, fixed confidence warnings and disclaimer; it
may simplify other prose but cannot add numeric facts. Number/date/amount guards
check against verified evidence, enforce deadline/amount notes and reject empty or
changed protected text. Failure retries once, then uses a deterministic template.
Plain language is prompted, not measured as a proven sixth-grade reading level;
non-numeric implications and semantic correctness still require review.

### Protected translation, back-translation and fallback

Full month-name dates, amounts, IDs/phone-like numeric compounds and other digits
become per-leaf placeholder tokens before translation. Deterministic restoration
rewrites dates using configured full month names and restores amounts/digits exactly.
Tokens must remain in their original leaf with exact multiplicity; moved, missing,
duplicated or changed tokens fail. Extra raw numbers, swapped/dropped dates,
glossary omissions and changed fixed uncertainty/disclaimer strings fail checks.
Warnings keep their status without restating unverified candidates. Numeric/date
counts are per-leaf multisets, not just document-wide unique numbers.

A separate model call back-translates accepted candidates. Comparison checks
numeric/date/amount agreement, exact fixed warnings/disclaimer and copied text-card
similarity at a 0.65 threshold. Similarity is a lexical heuristic, not an independent
semantic oracle: it can reject good paraphrases or miss errors. After one retry,
failure displays the English bundle plus an explicit notice in the requested
language. Confidence never exceeds medium while proposed glossaries lack native
review. This conservative policy produced three fallbacks in the live run; it does
not imply those three translations were linguistically incorrect.

Language config files specify UI text, dates/months, direction, aliases, voice
locales and a trusted glossary filename. Adding a language needs matching config/UI
keys and a glossary, not conditional code. All Spanish/Tagalog glossary entries are
reviewed=false with no reviewer identity. The single help entry is TODO with null
contact details. Existing source English is disclosed in per-card toggles; pending
or failed translation shows English explicitly, with flags still in the chosen UI
language. The UI can show multiple languages intentionally for original evidence.

### Privacy and browser lifetime

Only a language code enters localStorage. Notice photos/text, explanation bundles,
translations and receipts stay in memory; only fixed static assets are service-worker
cached. Clear/page leave abort fetches, invalidate generations, remove content and
stop speech. Language switching cancels prior explanation generation and cannot
show a late reply in the preceding language. Abort does not recall an already sent
request. Fixed status-message keys are retained for retranslation, never notice
strings. English offline bootstrap mirrors backend English data; other languages
are discovered from the API and are not persisted as notice history.

The explanation JSON body is bounded at 150,000 bytes, content validation failures
are sanitized, API responses are no-store, and logs contain only timing/request
ID/type/error metadata. The provider key is backend-only and is sent solely in the
Authorization header to the fixed HTTPS endpoint, never in prompts. `store=false`
is used; it does not assert zero provider retention. Production APIs do not write
content to disk. Opt-in evaluation deliberately saves only invented synthetic
fixture outputs, separate from production behavior.

### Live evidence and interpretation

`eval/reports/translation-comparison.md` compares eight original synthetic notices
in each target language with a plain raw-notice translation. Spanish accepted 7/8
and Tagalog 6/8 with one/two explicit English fallbacks, respectively. All sixteen
English explanations passed model generation. The eight unique extractions had
36 verified/four missing fields. Provider usage for this experiment totals 98
responses with reported usage, 54,194 input and 19,554 output tokens, excluding
separate prototypes and browser QA; no cost is guessed.

The baseline preserved numeric/date facts in 8/8 for both languages, but retained
numeric dates in all eight and lacked the fixed disclaimer. A metric audit found
that retained ISO dates had initially been conflated with number changes; saved
outputs were rescored without new model calls. Version
`m3-numeric-date-separation-v2` normalizes numeric and spelled month dates for fact
checks and scores month-name presentation separately. The model outputs themselves
were not changed. Guarded summaries and full raw notices have different coverage,
so these counts cannot show superior field accuracy or linguistic quality. Glossary
checks with no applicable source term pass vacuously and are identified in JSON.

Review fallbacks in `court_01`/`court_02` Tagalog (strict back-translated warning
preservation) and `school_02` Spanish (text-card similarity disagreement). A real
browser upload separately returned an incomplete source snippet for the action;
the validator left it unverified and the translation kept its uncertainty warning.
Do not add fixture-specific rules to hide this limitation. Native sheets include
fallback status and blank ratings; no native or physical-phone evidence is claimed.

### Verification and remaining acceptance

282 Python tests and 11 Node tests pass, including bad digits, date swaps/drops,
extra Unicode numbers, glossary/disclaimer/warning omission, retry/template/English
fallbacks, receipt tampering/expiry, stale responses, no wrong-language voices and
Unicode source highlighting. Frontend syntax and pip consistency pass. One existing
Python 3.9 asyncio warning remains. A temporary test-only RTL config establishes
language discovery/key parity without shipping another language.

Desktop browser QA exercised live Spanish/Tagalog results, source toggles and an
unverified action. Spanish play/pause/stop responded and Tagalog read-aloud disabled
with a matching-voice-unavailable message. A labeled synthetic 390px iframe rendered
production cards/CSS with long strings in RTL direction; visual wrapping stayed
within the frame. No direct overflow-width measurement was available in the browser
connector. This does not test an actual phone or assert Arabic translation support.
The student must still review the proposed code/UI/glossaries, obtain real native
ratings, add verified help resources and perform phone/read-aloud acceptance.
Stop at M3 review; M4 evaluation/failure analysis remains next.


## M4 Part C — evaluation design and findings (2026-10-24)

The student explicitly authorized a generated proposed scorer. `eval/scoring.py`
uses independent calendar/decimal parsing and strict copied-text comparisons,
explicit aliases, and present/missing/ambiguous truth states. Headline
false-verification is wrong Verified deadlines/amounts/actions divided by all three
field opportunities per record, with wrong among Verified separately reported.
Truth-present accuracy excludes absent/ambiguous fields; these remain in the safety
denominator. Safe abstentions, correct missing claims and provider unavailability
have distinct counts; provider failures do not receive correct-flag/missing credit.
Contacts are in the per-field/all-field metrics, outside the critical headline.

The eight original synthetic fixtures plus twelve additions form 20 dev documents;
eight hostile-body fixtures form adversarial. Both have deterministic clean/degraded
images and three repeated runs. Five parking/five court/five utility/four school/one
unknown satisfy 20 total while covering unknown. The multi-page sample has a second
page but only page 1 is processed, matching the current one-photo app. Type selection
is explicit; automatic classifier output is recorded as unknown, not overwritten
or scored as successful automatic classification. OCR text is harness-confirmed
unchanged; no human corrections or browser's extra JPEG encode are simulated.

Optional temperature/reasoning parameters were added to the two production model
adapters solely for fixed evaluation settings; absent arguments preserve production
payloads. The offline engine captures the actual extraction proposal, uses that
same proposal for B2 without validation and full with actual validation, and runs
actual explanation/translation code. Unknown abstention is separately ablated in B2.
B2 policy flags cannot be passed to a public endpoint. B1 requests plain explanation
and both translations of the same OCR notice plus fields for comparison; all its
field values are treated as displayed facts. It receives no source/status validator.
B2/full share costs and proposals, never double-counted as independent paid calls.

Inference pinned `gpt-5.4-mini-2026-03-17`, temperature 0, reasoning none, today
2026-10-24. Official snapshot/support documentation and the live settings probe are
linked in README. Temperature 0 does not guarantee deterministic API behavior;
three measured headline rates were identical here, not asserted universally.
Each raw report stores code/config/corpus provenance, raw invented outputs, timings
and actual usage. Tests/docs were added after inference started; production and
inference runtime were unchanged. No production notice-saving path was introduced.

A scoring audit corrected two interpretation issues after the original calls:
explicit absence claims are not wrong numeric facts when truth is absent, and a
fictional help-desk name without its testing disclaimer is an accepted contact
alias. Field truth values/states and model outputs were not changed. V2 also counts
static all-missing language bundles as vacuous number/glossary agreement. Original
artifacts/summaries remain; `eval/rescore.py` hashes model outputs, records revised
annotation/scorer provenance and refuses heldout rescoring. All aliases are scoring
data, never production sample-text rules. Exact-copy text mismatch still requires
semantic review before calling it a real-world harm.

Results: B1/B2/full each 6/360 critical false-verifications on dev and 0/144 on
adversarial. The six live errors are the conflicting mandatory hearing dates in
both variants across all three repetitions. Full additionally accepts a clipped
contact phrase in three dev records. Full verified critical usability is 270/276;
the six additional safe flags are correct actions with incomplete source evidence.
The ablation therefore does not establish a headline improvement. Original source
matching is necessary but insufficient for semantic field-role/conflict safety.

A targeted simulated bad model can copy $999.99 from attack_05's hostile body and
get Verified because the literal value/source exist. The live model did not do so
in these 48 attack records. Two strict expected failures retain that gap and the
conflicting-date gap; neither is claimed as accepted security behavior. Other tests
cover all eight adversarial trust boundaries, fabricated out-of-source amounts,
provider transient/malformed failures and whole-API success/failure log/temp privacy.
The CI definition uses no credentials/API/heldout and has not run remotely.

`FAILURES.md` includes every observed stage/field failure (including safe coverage
flags), grouped causes and five ranked general fixes. These are hypotheses/options,
not fixes or post-fix gains. `docs/EVIDENCE.md` contains factual tables, pending
heldout/after-fix sections, limitations and actual disclosed authorship. Part C
stops for the student choice; Part D is capped at three rounds. No freeze/tag/test
run or heldout input inspection has occurred. Future supplied heldout inputs are
Git-ignored; even credential audits skip that directory. A single-use run-start
ledger is created only after the freeze/tag/code gate, before test data is read.

Final local verification: 323 Python passes, two known expected security failures,
14 Node passes, syntax/dependency checks pass. Exact offline table reconstruction
is verified; remote CI is not. Latency p50/p95 and approximate standard-rate model
costs were included using actual reported tokens, with shared proposals counted
once and documented prices separated from original generation settings. User
selection of a Part C fix remains the next step.
