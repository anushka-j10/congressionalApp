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
