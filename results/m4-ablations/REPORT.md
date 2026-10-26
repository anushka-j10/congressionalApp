# Milestone 4 ablation follow-up — 2026-10-25

The missing field-validator ablation capability is implemented and tested. This supersedes item 5 of the historical results/m4-verification/REPORT.md. All seven named field-validator groups are disabled one at a time, and the human amount-review gate is measured separately. Production/API callers cannot choose these switches.

## Results

| Mode | Dev critical false verified | Adversarial critical false verified |
|---|---|---|
| full | 0/120 | 0/48 |
| without_action_completeness | 0/120 | 0/48 |
| without_amount_validation | 0/120 | 0/48 |
| without_date_validation | 2/120 | 0/48 |
| without_evidence_context | 0/120 | 0/48 |
| without_readability | 0/120 | 0/48 |
| without_source_match | 0/120 | 0/48 |
| without_text_copy | 0/120 | 0/48 |
| without_human_amount_review | 0/120 | 0/48 |

40 dev records and 16 adversarial records were replayed from the latest completed live audit, using identical saved OCR/proposals/truth/scorer. Zero new model/OCR calls; no API-key read. The replay requires unchanged full-reference value/status/normalization. Full-reference replay matched every saved record. Full remains 0/120 and 0/48 critical false-verified, with 72/92 and 32/48 correct verified present fields. Removing date validation produces two false-verified dev deadlines (the ambiguity conflicts already recorded for B2). Amount-gate removal increases verified coverage to 92/92 and 48/48; it does not prove OCR reads amounts correctly. Every scored ablation failure is retained in dev.json/adversarial.json, with per-field tables in the matching Markdown files.

## Scope of each switch

- source_match: whether the snippet must be found in actual confirmed text. When disabled and absent, the proposed snippet supplies comparison text, but no source offsets are invented. Other checks remain on.
- evidence_context: instruction-like evidence and wrong-role checks, including issue-date/late-fee rejection.
- readability: unreadable/replacement-character rejection.
- date_validation: one cohesive date validator, including calendar/weekday parsing, typed source equality, conflicting obligations, relative rule/anchor validation and arithmetic. Subchecks are not individually measured.
- amount_validation: amount parsing/range/sign/context/equality checks. Human review still applies.
- text_copy: copied text whole-phrase membership and numeric equality. Action completeness still applies.
- action_completeness: whole instruction sentence, condition, alternative and timing coverage.
- human_amount_review: the separate human attestation gate. No claim of actual human review is added by this evaluation mode.

Schema validation, null/missing handling, unknown-type abstention and the later explanation guards remain mandatory/outside this field-validator experiment. The experiment is per validator group, not a claim to ablate every regex, parsing helper, language guard or schema restriction independently. Unchanged metric rows do not show a check is unnecessary: the existing proposals may not exercise it, or another active check may block them. Targeted isolation tests independently demonstrate that each field-validator group can change its intended failing case and that every other single-group switch leaves that case blocked.

## Checks and evidence

- Clean local clone at implementation commit 81661e4. Requirements unchanged; the earlier fresh ARM audit venv was reused and pinned requirements rechecked offline, not presented as a second fresh environment installation. Original fresh-environment installation evidence remains under results/m4-verification.
- 407 Python tests and 17 JavaScript tests pass in that clean checkout: clean-pytest.txt and clean-node.txt. Includes 16 new ablation regressions, all prior source-not-found/missing-deadline/extra-number/privacy tests, independent switch isolation and request bypass rejection. One existing dependency deprecation warning remains.
- Clean app startup and shell/health/read/extract/explain HTTP 200; no-store on APIs; five private paths 404; no new notice/storage files: app-smoke.txt, server.txt and privacy-probe.py. Smoke uses unknown-type/static outputs; live inference evidence is the earlier completed audit.
- Production defaults are unchanged. Public checked_field always passes an empty disabled set. The human gate is a shared helper with the same default-false behavior. Replay full-reference matching and the complete regression suite verify this refactor on the available cases.
- Previous checks 1–4 and 6–11 remain evidenced in results/m4-verification/REPORT.md, with the current regression/clean-app replay above. No new live model variance experiment was run.
- The original eval-freeze still points to 24d729a540ed3913ced09ee42af89765fd921c4b. Item 12 is not claimed as a new freeze: the historical tag and original one-use protocol are preserved. A versioned fresh freeze/held-out protocol is separate work; no tag was invented or moved.
- No held-out set was opened, replayed or model-run during this follow-up. The API key was not read, copied or used. No push or deployment.

Exact commands are in commands.md. Raw ablation JSON includes input and source hashes, every replayed field/status, every scored discrepancy and all denominators.
