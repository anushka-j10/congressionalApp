# Notice Decoder — release checklist

**Live:** https://notice-decoder-ns5o.onrender.com · **App commit:** `e25b3c1` · **Checked:** October 26, 2026

**Hosting is available; submission and full phone acceptance are incomplete.** FAIL means a known failure or a required check without sufficient evidence; the reason is stated below.

| Release item | PASS / FAIL | Evidence or remaining action |
|---|---|---|
| App pushed and deployed over HTTPS | PASS | Render successful release; [12/12 public checks](results/release-2026-10-26/https-smoke.json), ten matching asset hashes |
| Existing automated tests | PASS | [430 Python](results/release-2026-10-26/pytest.txt), [62 JavaScript](results/release-2026-10-26/node.txt); one dependency warning |
| Synthetic live upload, extraction, EN/ES/TL display | PASS | [Live browser evidence](results/release-2026-10-26/REPORT.md); one development notice, not an accuracy study |
| Server-only key, exact-origin CORS and private-file isolation | PASS | [Security audit](results/release-2026-10-26/security.json) and public smoke; secret never retrieved from host |
| Analysis limits and quota-error handling | PASS within controlled scope | Shared 30/min, 240/hour, one concurrent request; regression tests. No hard dollar cap or live quota-exhaustion test |
| Original held-out evidence preserved | PASS | Once-run report and eval-freeze unchanged; dev/held-out/stress results distinguished |
| Phone-width layout, tested targets and basic contrast | PASS within scoped checks | 63 prior layout combinations; 10 contrast pairs. Does not certify every state or WCAG compliance |
| Real iPhone notice reading | FAIL | User-reported issue; local reproduction loses critical date/instruction text. Manual-selector wording fixed, OCR limitation remains |
| Physical-phone installation, camera, audio and screen reader | FAIL — pending | User opened site on iPhone; full flow and device/browser versions not verified |
| Deployed English fallback, unreadable-photo and offline scenarios | FAIL — incomplete | Fallback/offline not exercised; blank upload permission declined. Local tests are not deployed passes |
| Native Spanish/Tagalog review | FAIL — pending | Machine-generated catalogs/glossaries and outputs remain unreviewed |
| GitHub cloud CI completed | FAIL — pending | Last inspected release run queued; local tests passed |
| README, results/failures, 2.0 plan and submission/demo drafts | PASS as drafts | [Submission](SUBMISSION.md), [170-second shot list](DEMO_SCRIPT.md), [2.0 brief](NOTICE_DECODER_2_0_PROMPT.md) |
| AJ contribution review, final video and contest submission | FAIL — pending | Complete personal TODOs in [AI_USAGE.md](AI_USAGE.md), record/check video, review form requirements and submit |

Next: resolve the real-photo reading failure using a fresh development reproduction; complete the physical-device and deployed failure-state checks; have AJ confirm personal authorship statements and submit the final materials. Known reliability failures must stay visible. [Full release evidence and boundaries](results/release-2026-10-26/REPORT.md).
