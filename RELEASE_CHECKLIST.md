# Notice Decoder — release checklist

**Live:** https://notice-decoder-ns5o.onrender.com · **App commit:** `e6f9933` · **Checked:** October 26, 2026

**Hosting is available; submission and full phone acceptance are incomplete.** FAIL means a known failure or a required check without sufficient evidence; the reason is stated below.

| Release item | PASS / FAIL | Evidence or remaining action |
|---|---|---|
| App pushed and deployed over HTTPS | PASS | Render successful release; [12/12 public checks](results/phone-reading-fix/https-smoke.json), eleven matching asset hashes |
| Existing automated tests | PASS | [452 Python](results/phone-reading-fix/pytest.txt), [62 JavaScript](results/phone-reading-fix/node.txt); one dependency warning |
| Synthetic live upload and extraction | PASS | [Live browser evidence](results/phone-reading-fix/REPORT.md#deployed-verification); $146.00, full date and 7-day instruction correct |
| Live translation on every tested case | FAIL — safely withheld | Receipt EN/TL and simple EN/ES passed. Receipt ES and simple TL fell back. [API acceptance 9/10](results/phone-reading-fix/live-api.json); no failures hidden |
| Server-only key, exact-origin CORS and private-file isolation | PASS | [Security audit](results/phone-reading-fix/security.json) and public smoke; secret never retrieved from host |
| Analysis limits and quota-error handling | PASS within controlled scope | Shared 30/min, 240/hour, one concurrent request; regression tests. No hard dollar cap or live quota-exhaustion test |
| Original held-out evidence preserved | PASS | Once-run report and eval-freeze unchanged; dev/held-out/stress results distinguished |
| Phone-width layout, tested targets and basic contrast | PASS within scoped checks | 63 prior layout combinations; 10 contrast pairs. Does not certify every state or WCAG compliance |
| Timing-corruption safety fix | PASS within tested patterns | Six formerly verified damaged actions now withheld; live negative test withholds all critical fields. This does not repair underlying OCR |
| Real iPhone notice reading | FAIL — retest pending | User-reported issue; new guard tested on synthetic faults, original phone sample not revalidated |
| Physical-phone installation, camera, audio and screen reader | FAIL — pending | User opened site on iPhone; full flow and device/browser versions not verified |
| Deployed English fallback and unreadable-photo abstention | PASS within tested scope | Live browser/API fallback; public API blank photo returns no text and retake warning. [Evidence](results/phone-reading-fix/REPORT.md#deployed-verification) |
| Deployed offline scenario | FAIL — unverified | Actual phone offline behavior not exercised; local error tests are not a deployed offline pass |
| Native Spanish/Tagalog review | FAIL — pending | Machine-generated catalogs/glossaries and outputs remain unreviewed |
| GitHub cloud CI completed | FAIL — pending | Last inspected release run queued; local tests passed |
| README, results/failures, 2.0 plan and submission/demo drafts | PASS as drafts | [Submission](SUBMISSION.md), [170-second shot list](DEMO_SCRIPT.md), [2.0 brief](NOTICE_DECODER_2_0_PROMPT.md) |
| AJ contribution review, final video and contest submission | FAIL — pending | Complete personal TODOs in [AI_USAGE.md](AI_USAGE.md), record/check video, review form requirements and submit |

Next: retest the updated app on the original iPhone sample, complete installation/audio/screen-reader/offline checks, and review/record/submit the materials. Known OCR and translation failures remain visible. [Current release evidence and boundaries](results/phone-reading-fix/REPORT.md).
