# Public release verification — October 26, 2026

Live URL: https://notice-decoder-ns5o.onrender.com

**Hosting: PASS. Full phone/reliability acceptance: FAIL / incomplete.** This report distinguishes a working synthetic example from unresolved real-photo failures.

## Release identity

The review branch was fast-forwarded onto `fix/notice-reliability` and pushed. Render first deployed `7c93a869113a0ada59a3c6cffe33958f9bcfb574` as `dep-dbfeh6ss728c73f4v2gg` at 01:43:55 EDT; it reached Live. A small subsequent copy fix changed the initial type selector from “Unknown” to “Choose a notice type,” clarified manual selection, and advanced the shell cache to v20. It did not add classifier signals or change OCR/model/validator behavior.

The final application commit is **`e25b3c118fbe05b5680b76782cf88ac7acc7afbd`**, deployed as **`dep-dbferbg473hc73cto1f0`**, service `srv-dbfbm7dg1s2s73f6fk70`, personal My Workspace, Free Docker service. Render reports Deploy succeeded, deployed 02:05:34 EDT, duration 32.9 seconds, with its Live log at 02:06:07 EDT. [Dashboard evidence](render-copy-fix-live.png). Later documentation commits do not change the running application; deployments are manual.

## Results

| Check | Result | Evidence and limits |
|---|---|---|
| Public HTTPS, health, correct release assets | PASS | [https-smoke.json](https-smoke.json): 12/12 checks; ten frontend assets match local SHA-256 hashes at e25b3c1. Earlier release is separately retained in https-smoke-initial.json |
| Manifest, icons, shell cache | PASS for served assets | Standalone manifest/icons and cache v20 pass HTTP checks. Actual phone installation/offline behavior is not established |
| CORS/private paths/API cache | PASS | Exact-origin preflight succeeds, foreign-origin POST is 403, four private paths are 404, health is no-store |
| Server model configured and responding | PASS for one synthetic workflow | Live extraction and Spanish/Tagalog generation succeeded using the host configuration; no host secret was fetched or displayed |
| UI upload → OCR → manual review → extracted fields | PASS for development sample parking_01 | Actual browser photo chooser, client JPEG preparation, Read notice, type selection and both review checkboxes. Transcript matched visible content apart from whitespace; no edits were made. Four displayed matches: agency, deadline, amount and action. Placeholder contact withheld. [OCR](synthetic-ocr.txt), [English DOM](english-dom.txt), [screenshot](live-results.png). This was on 7c93a86, before the copy-only update |
| Spanish and Tagalog output visible | PASS for presentation | [Spanish DOM](spanish-dom.txt), [Tagalog DOM](tagalog-dom.txt). Date and amount were displayed in both. Both displayed unreviewed-translation cautions. No native-speaker approval or semantic-accuracy score is claimed |
| Read-aloud on a phone | FAIL — not verified | English Play and Stop were clicked on desktop, without auditory verification. Tagalog correctly displayed no matching voice on that desktop. No physical-phone audio pass was reported |
| English fallback on the deployed URL | FAIL — not exercised | Neither successful translation triggered fallback. Controlled guard/fallback tests pass in tests/test_explanation.py; they are not a deployed failure-injection check |
| Unreadable photo abstention on deployed URL | FAIL — not completed | Browser permission gate declined upload of the synthetic blank-page test. No alternate upload path was used. Local regression coverage remains separate |
| Offline/error UX on physical phone | FAIL — not verified | Manifest/service-worker delivery alone does not prove offline behavior. Browser automation exposed no offline control. Friendly rate/quota errors have controlled tests; live quota exhaustion was not forced |
| Phone-width/touch layout | PASS within earlier scope | 63 combinations at 320/390/430px, EN/ES/TL, in [prior layout evidence](../final-polish/phone-checks.json). Desktop browser frames, not physical-device testing; the later selector-copy change was not a repeat of that matrix |
| Text contrast | PASS within scoped calculation | [contrast.json](contrast.json): 10/10 explicit CSS text pairs meet 4.5:1, minimum 5.6315469693356635. This excludes all-state/composite/disabled-control and full WCAG audits |
| Screen-reader/device accessibility | FAIL — incomplete | Labels, focus/source actions and reduced-motion code have checks; no full VoiceOver or TalkBack session was performed |
| Local regressions after copy fix | PASS | [pytest.txt](pytest.txt): 430 passed, one existing dependency deprecation warning; [node.txt](node.txt): 62 passed, 0 failed |
| GitHub cloud CI | FAIL — not confirmed complete | At last read, e25b3c1 run 40277617639 and 7c93a86 run 40275730385 were queued; a prior run was in progress. [Status snapshot](github-ci.json). Do not substitute local success for cloud completion |
| Secret and historical integrity audit | PASS for recorded scope | [security.json](security.json): configured-key equality and long credential-like token checks; .env ignored, untracked, 0600; eval-freeze and historical evaluation records unchanged. Not a universal guarantee against every future exposure |

## iPhone report and real-photo diagnostic

AJ reported “Unknown” on an iPhone, then reported an additional incorrect result and supplied a public social-media ticket photo. The initial type label was an expected unconfigured-classifier state; e25b3c1 clarifies the selection step. That wording fix does not fix reading accuracy.

The linked original photo was inspected locally: 1536×2048, dense angled print, with the bottom instructions cropped by the source image. A local run using the unchanged normalization/preprocessed reader and Tesseract 5.5.3 produced 1,629 characters. Of five targeted presence checks, only amount digits and the contesting-section heading were intact; the full due date, full issuing-court name and “at least 5 days” clause were not. The generic quality_warnings function returned an empty list, although the reader's standard review warnings still apply. Original-image local OCR produced 1,523 characters and preserved the full due date, but also misread the contesting number. Therefore changing reader alone is not a demonstrated complete repair.

This is a **failed local reproduction of critical reading fidelity**, not a scored production benchmark or a confirmed account of the exact iPhone output. The iPhone browser/version and specific wrong result were not supplied. The host uses Debian Tesseract 5.3.0, so local results do not prove byte-identical hosted OCR. No model call, payment/appeal action, or external re-upload of that real ticket was made by the assistant. Its image, identifiers and full transcript are excluded from this repository; the incoming public image was downloaded locally for inspection. Only synthetic notice content is retained in the release screenshots/DOM files.

## Reproduction and boundaries

From the repository root:

```sh
git fetch origin
git switch fix/notice-reliability
git merge --ff-only design/mobile-format-review
git push origin fix/notice-reliability
OPENAI_API_KEY='' OPENAI_MODEL='' ../../work/m4-audit-venv/bin/python -m pytest -q > results/release-2026-10-26/pytest.txt 2>&1
/opt/homebrew/bin/node --test tests/*.mjs > results/release-2026-10-26/node.txt 2>&1
../../work/m4-audit-venv/bin/python results/release-2026-10-26/https-smoke.py
../../work/m4-audit-venv/bin/python results/release-2026-10-26/audit-security.py
git diff --check
```

After testing the selector wording, only its six application files were committed and pushed as e25b3c1. Both deployments used Render Dashboard → Manual Deploy → Deploy a specific commit with the full SHA. The API key remained server-side; no new credentials, paid resources or host settings were introduced. Public smoke has zero model calls; the separate browser synthetic workflow does make model requests, whose exact provider-internal count was not captured.

The original held-out run was not rerun/rescored, and its tag was not moved. No new overall accuracy claim follows from this release. The [2.0 prompt](../../NOTICE_DECODER_2_0_PROMPT.md) records the reliability work. The [release checklist](../../RELEASE_CHECKLIST.md) remains incomplete until the failed/unverified acceptance items are resolved.
