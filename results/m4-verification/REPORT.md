# Milestone 4 verification audit

**Overall: FAIL — item 5 is a missing capability. Freeze is blocked.**

Audit date: 2026-10-25 (client America/New_York). Audited clean-checkout commit: `6c13e08925fa88643957d9dc777d65b6136a70ae`. Runtime-generated run dates are preserved in the raw JSON; evaluation today is deliberately pinned to 2026-10-24. No application feature or production behavior was changed during this audit. Eight proof tests were added, bringing 383 existing Python tests to 391 total; JavaScript remains 17.

| Item | PASS/FAIL | Evidence |
| --- | --- | --- |
| 1. Fresh install/run | PASS | install-arm.txt: successfully installed pinned requirements into a fresh ARM Python 3.12.14 venv. environment.txt: clean local clone at the audited commit, no copied .env. app-smoke.txt: shell/health/read/extract/explain HTTP 200. Exact commands below. |
| 2. All tests | PASS | pytest.txt: 383 existing pass; pytest-final.txt: 391 total pass. node.txt: 17 pass, zero failures. pip-check.txt: no broken requirements. |
| 3. Dev harness metrics | PASS | dev.json and dev.md: 40/40 records, 20 cases × clean/degraded, one repetition. Printed critical false-verification, per-field accuracy, abstain-when-truth-exists and correct-missing columns. |
| 4. B1/B2 same cases | PASS | dev.md/adversarial.md: B1, B2 and full share each record/ground truth/OCR. engine.py uses one reading, shared B2/full extraction proposal where applicable, and the same scorer. |
| 5. Each validator individually disabled | FAIL — capability gap | eval/engine.py ablation_fields only supports one validators boolean; m4-config.json defines B2 with validators=false. There are no leave-one-validator-out switches or measurements. All-off B2 is not individual-validator ablation. Not implemented under the no-feature instruction. |
| 6. Adversarial run | PASS | adversarial.json/adversarial.md: 16/16 records, eight cases × two variants. Raw outputs and all scored discrepancies are recorded; no unavailable methods. |
| 7. Source not found | PASS | tests/test_m4_audit.py::test_absent_source_snippet_can_never_verify: five field types, all unverified with no normalized value/span; explicit-proofs.txt. Matching here follows the documented normalized/letter-fuzzy policy, never digit repair. |
| 8. Absent fields/no deadline | PASS in the demonstrated regression cases | test_notice_with_no_deadline_does_not_infer_one_from_issued_date, test_bad_model_cannot_promote_issue_date_to_a_missing_deadline and test_all_absent_fields_stay_missing_without_added_values; explicit-proofs.txt. These prove the tested boundary behavior, not universal semantic correctness on every possible notice. |
| 9. Explanation extra number | PASS | tests/test_explanation.py::test_bad_english_number_regenerates_once_then_template_fallback: injected $999.00 is rejected twice and excluded from returned template; explicit-proofs.txt. |
| 10. Privacy | PASS for tested normal application requests | 25 targeted tests pass (targeted-tests.txt), runtime sentinel/filename grep returns no matches (privacy-grep.txt), real clean-server flow creates no notice files (app-smoke.txt). Static findings and vendor caveat below. |
| 11. Current failure/evidence documents | PASS | FAILURES.md and docs/EVIDENCE.md are rebuilt with this audit run's real counts and every scored discrepancy. Earlier records are archived under docs/history, not presented as current measurements. |
| 12. Freeze | FAIL — blocked by item 5 | No tag was created or moved. Existing eval-freeze remains 24d729a540ed3913ced09ee42af89765fd921c4b. No held-out evaluation was invoked in this audit. Prior held-out history is preserved, not overwritten or described as a new test. |

## Latest live results

One repetition was requested for this verification run; the earlier three-repetition experiments remain separate historical evidence. Zero standard deviation for this single run is not an estimate of reproducibility. B1 translates/explains the whole OCR text; full translates checked summaries. Human amount review is not simulated: amounts and money-bearing actions stay unverified, so safety must be read alongside coverage.

| Set | Mode | Critical false-verified | Present-field accuracy | Correct and Verified | Abstain with truth present |
| --- | --- | --- | --- | --- | --- |
| dev | B1 | 2/120 (1.7%) | 92/92 (100.0%) | 92/92 (100.0%) | 0/92 (0.0%) |
| dev | B2 | 2/120 (1.7%) | 92/92 (100.0%) | 92/92 (100.0%) | 0/92 (0.0%) |
| dev | full | 0/120 (0.0%) | 92/92 (100.0%) | 72/92 (78.3%) | 20/92 (21.7%) |
| adversarial | B1 | 0/48 (0.0%) | 48/48 (100.0%) | 48/48 (100.0%) | 0/48 (0.0%) |
| adversarial | B2 | 0/48 (0.0%) | 48/48 (100.0%) | 48/48 (100.0%) | 0/48 (0.0%) |
| adversarial | full | 0/48 (0.0%) | 48/48 (100.0%) | 32/48 (66.7%) | 16/48 (33.3%) |

## Privacy findings

- `backend/main.py` has three application logger calls: request ID, timing, enum document type and fixed error category only. `storage-code.txt` records the grep output. Image `open`/`save` calls in images.py operate on BytesIO in memory; multipart spools are bounded above the accepted upload size and closed in finally blocks.
- `browser-storage-code.txt` shows localStorage used only for the language code and a fixed service-worker shell allowlist. API responses are no-store; no notice localStorage/sessionStorage/IndexedDB path was found in application JS.
- The vendored HEIC decoder contains eight console diagnostic sites for decode errors/IDs (`vendor-diagnostics.json`). They are disclosed rather than falsely claiming zero console calls. No OCR text or notice persistence path was found in application code; tests/greps are bounded evidence, not a formal guarantee about every future vendor error payload.
- `rg` against server.txt and privacy-runtime.log found zero private sentinel/filename matches, exit code 1. The production read/extract/explain smoke flow left the checkout storage inventory unchanged. That flow uses unknown-type/static output; live-model behavior is separately covered by the harness.
- Synthetic fixtures and explicit evaluation reports intentionally persist invented test data outside the public frontend. This is separate from normal app-request retention; evaluation output is not evidence that user notices are saved by the app.
- The private API key stayed in the original ignored owner-only .env, which was referenced by path for live evals and never copied into the clean clone, displayed, or written to artifacts.

## Gaps listed rather than implemented

1. Item 5: individual-validator ablation switches and a results table are absent. Adding them would be a harness capability, not a demonstrated implementation bug.
2. Automatic classification remains unknown until student-owned signal lists are supplied. This audit explicitly uses fixture type selection, as the harness records.
3. No physical-phone, handwriting, native-speaker or generalization claim follows from these tests. Source matching can repeat OCR errors; the separate human amount attestation is not proof that a person noticed every error.
4. The initial default Intel Python 3.9 install started compiling OpenCV from source and was stopped after the successful ARM install; install.txt preserves that incomplete attempt. The final PASS is based on the separate fresh ARM environment, not the stopped attempt. One dependency deprecation warning remains; it is not a test failure.

## Evidence paths

`commands.md` contains exact setup, install, startup, test, live-eval and grep commands. install-arm.txt, pytest-final.txt, node.txt, app-smoke.txt, explicit-proofs.txt and privacy-grep.txt retain actual outputs; dev.json/adversarial.json retain raw results and dev.md/adversarial.md their printed tables. Audit source/test additions are disclosed in AI_USAGE.md.
