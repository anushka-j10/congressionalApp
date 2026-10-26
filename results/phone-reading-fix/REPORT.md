# Phone OCR safety fix — 2026-10-26

## What changed

The local OCR engine is unchanged. Numeric-looking dates with incomplete years or impossible dates, and time limits containing OCR-confused letters (for example `S days` or `3C days`), now trigger a retake/correct-text warning. The deadline, amount, and required action are all withheld until the suspect text is corrected from the photo. This conservative policy prevents a clean clipped snippet from hiding a damaged competing deadline elsewhere. Two OCR passes agreeing on damaged text does not remove uncertainty. Dates and duration candidates retain their original text and offsets; no digit is guessed.

This is a bounded rejection fix, not proof that arbitrary photographs can be read correctly. Four-digit but wrong years, valid-looking wrong digits, missing paragraphs, mistaken contact information, and the semantic choice between payment and contest deadlines remain possible. A two-digit date can be genuinely printed; the app deliberately withholds critical fields instead of guessing its century. Automatic notice-type signals remain empty: choose the type manually.

## Reproduction and checks

- `receipt_repro.py` uses only newly generated, fictional receipt layouts with different numbers and identities. Both clean and angled/compressed images preserve 3/3 tested tokens locally (amount, full due date, timing clause). These two images did **not** reproduce the real photograph's loss; they are positive image controls.
- Eight separately labeled simulated-OCR controls test the actual unsafe patterns. Against baseline commit `eccb39b`, 6/6 damaged action examples were verified; after the fix, 0/6 are verified. Both legible controls remain verified (8/8 expected statuses). Full inputs and before/after fields: [receipt-reproduction.json](receipt-reproduction.json).
- Python: **452 passed**, one pre-existing Starlette/AnyIO deprecation warning ([output](pytest.txt)). JavaScript: **62 passed**, zero failed ([output](node.txt)). The new regression module contains 22 tests, including clipped snippets, correcting text, and withholding suspect facts from the explanation model.
- Local OCR: Tesseract 5.5.3. Render uses its container OCR; local results are not an exact reproduction of the user's iPhone output. No real ticket photo, personal identifiers, or transcript is in this evidence folder.

## Fresh development results

One repetition, existing unchanged dev/adversarial corpora, selected fixture document types, unchanged OCR text, no simulated human amount confirmation. Model/config, corpus hashes and source hash are recorded in the JSON reports. This is development evaluation, not a new held-out evaluation.

| Set / method | Critical false verified | All-field false verified | Present values correct (all four fields) | Correct and verified | Abstain when present |
|---|---|---|---|---|---|
| Dev / full | 0/120 | 0/160 | 128/130 | 107/130 | 23/130 |
| Dev / B1 plain translate | 2/120 | 4/160 | 128/130 | 128/130 | 0/130 |
| Dev / B2 no validators | 2/120 | 2/160 | 128/130 | 128/130 | 2/130 |
| Adversarial / full | 0/48 | 0/64 | 64/64 | 48/64 | 16/64 |
| Adversarial / B1 | 0/48 | 0/64 | 64/64 | 64/64 | 0/64 |
| Adversarial / B2 | 0/48 | 0/64 | 64/64 | 64/64 | 0/64 |

40/40 dev records and 16/16 adversarial records completed, no unavailable field methods. Critical-field coverage remains 72/92 on dev and 32/48 on adversarial; all 20 and 16 present amounts respectively are withheld without human photo review. The guard caused no additional critical abstention on these dev cases. This corpus does not exercise the new damage patterns, so the separate targeted controls matter.

Dev per-field present-value accuracy: deadline 34/34; amount 20/20 (0 verified); action 38/38; contact 36/38. Of the contacts, 35/38 are verified, one correct proposal is withheld, and two are missing. The model proposes a deadline for both variants of the ambiguous `court_03`; the validator rejects both. All wrong or withheld full-system outputs are preserved in [full-abstentions-and-errors.json](full-abstentions-and-errors.json), including every withheld amount.

Translations: dev Spanish falls back to English 3/40, Tagalog 6/40; adversarial Spanish 0/16 and Tagalog 1/16. These failures are retained, not counted as successful translation. Glossaries still lack native-speaker review.

[Dev report](dev.md) · [Adversarial report](adversarial.md) · [Dev ablations](dev-ablations.md) · [Adversarial ablations](adversarial-ablations.md). Each ablation replays the same saved proposals with one validator group disabled, zero new model calls. Disabling date validation produces 2/120 dev critical false verifications; the unchanged readability ablation reflects this set's lack of the new damage patterns.

## Exact commands

Run in the repository root. The Python environment is task-local; production dependencies remain in `requirements.txt`. Credentials are loaded internally from the ignored `.env` only for the opt-in eval runner; none are arguments or printed.

```sh
OPENAI_API_KEY='' OPENAI_MODEL='' ../../work/m4-audit-venv/bin/python -m pytest -q > results/phone-reading-fix/pytest.txt 2>&1
/opt/homebrew/bin/node --test tests/*.mjs > results/phone-reading-fix/node.txt 2>&1
../../work/m4-audit-venv/bin/python results/phone-reading-fix/receipt_repro.py > results/phone-reading-fix/reproduction-console.txt 2>&1
../../work/m4-audit-venv/bin/python -m eval.run --set dev --repeats 1 --out results/phone-reading-fix/dev.json > results/phone-reading-fix/dev-console.txt 2>&1
../../work/m4-audit-venv/bin/python -m eval.run --set adversarial --repeats 1 --out results/phone-reading-fix/adversarial.json > results/phone-reading-fix/adversarial-console.txt 2>&1
../../work/m4-audit-venv/bin/python -m eval.ablations --input results/phone-reading-fix/dev.json --out results/phone-reading-fix/dev-ablations.json
../../work/m4-audit-venv/bin/python -m eval.ablations --input results/phone-reading-fix/adversarial.json --out results/phone-reading-fix/adversarial-ablations.json
../../work/m4-audit-venv/bin/python results/phone-reading-fix/audit-security.py
```

## Privacy and historical evidence

The configured key and credential-pattern scan found zero matches in tracked/unignored files and reachable Git blobs; `.env` is ignored, untracked and mode 0600. See [security.json](security.json) for scope/counts. Production processing still uses in-memory buffers; backend log calls contain request ID, elapsed time, document enum and fixed error code only. This folder deliberately contains synthetic opt-in test inputs and outputs; it is not served by the app.

`eval-freeze` remains `24d729a540ed3913ced09ee42af89765fd921c4b`. No original held-out run, answer key or historical evaluation report was changed or rerun. The earlier held-out failures remain relevant and are not superseded by this development result.


## Deployed verification

App commit `e6f9933818d055e436b157aff081aa08be0f962e` was pushed to `fix/notice-reliability` in AJ's `anushka-j10/congressionalApp` repository. Render deployment `dep-dbflrm6i0phs73b5j2u0` started October 26 at 10:04:08 AM EDT, completed in 1m05s, and showed **Deploy succeeded | Live**. [Deployment screenshot](render-live.png). Free plan and host secrets were not changed.

Public URL: https://notice-decoder-ns5o.onrender.com

- **PASS:** 12/12 public HTTPS/security checks, including exact matches for all 11 checked assets and service-worker shell v21. [Command output](https-smoke-console.txt), [hashes/results](https-smoke.json). Command: `../../work/m4-audit-venv/bin/python results/phone-reading-fix/https-smoke.py`.
- **PASS:** real browser file upload of `synthetic-receipt-clean.jpg`, client photo preparation, server OCR, manual Parking ticket selection, extraction and English explanation. Printed $146.00, November 29, 2027, and the complete 7-day instruction matched the generated source. [Reading DOM](live-reading-dom.txt), [English DOM](live-english-dom.txt).
- **PASS:** Tagalog receipt output displayed in the browser with dates/amount/timing intact and the unreviewed-translation warning. [DOM](live-tagalog-dom.txt), [screenshot](live-tagalog.png). This is an automated-check pass, not native-language approval.
- **FAIL translation / PASS safe fallback:** the receipt's Spanish translation did not pass its guard. The browser displayed English with a clear Spanish fallback notice. [Observed DOM](live-spanish-dom.txt). No retry was made to hide that failure.
- **PASS:** deliberately edited synthetic receipt text changed the year to `11/29/2` and the timing number to `S days`. Even with both confirmation boxes checked, the live UI withheld all three critical fields. The model returned a missing deadline; amount/action were unverified. [DOM](live-damaged-text-dom.txt), [screenshot](live-damaged-text.png). These corruptions were manually injected as a negative test; they are not claimed OCR output from the uploaded clean image.
- **9/10 API acceptance checks passed:** [complete requests/results without receipts](live-api.json) and [command output, including the nonzero assertion exit](live-api-console.txt). Command: `../../work/m4-audit-venv/bin/python results/phone-reading-fix/live_api_checks.py`. The public server returned blank text plus a retake warning for a newly generated white image; withheld critical facts for truncated years and damaged duration text; did not invent a missing deadline; returned a fixed 422 error for malformed input; and returned English with a warning when a reserved literal token triggered the translation guard. Simple English/Spanish controls passed. The simple Tagalog control **failed translation** after two attempts (`warning_preservation`) and fell back safely to English. It is retained as the tenth failed check, despite the separate receipt Tagalog success.
- **NOT VERIFIED on a physical iPhone:** the user's original photo, installation, camera, audible speech, screen reader and true offline behavior. Browser/HTTP tests do not replace those checks. The available browser tool cannot toggle the phone's connection. Existing local frontend tests exercise network/quota/error behavior; that is not a deployed offline pass.
- **GitHub CI pending:** release run [40336026004](https://github.com/anushka-j10/congressionalApp/actions/runs/40336026004) was queued at inspection ([snapshot](github-ci.json)). Local test results are reported separately.

Both a complex Spanish example and a simple Tagalog example fell back during live acceptance. No translation prompt, glossary, or validator was weakened to force a pass. Close and reopen the app before device retesting so the new shell can load.
