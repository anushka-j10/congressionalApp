# Exact Milestone 4 audit commands

Working source: `/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp`. Clean clone: `/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean`. This is a local clone of the latest unpushed branch, not a claim that GitHub already contains it. Tesseract was already installed at /opt/homebrew/bin/tesseract; Node 26 and the ARM Python runtime were also pre-existing prerequisites.

```sh
git clone --no-local --branch fix/notice-reliability /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean
cd /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean
/Users/anushkajain/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m venv /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python --version
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/install-arm.txt 2>&1
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pip check > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/pip-check.txt 2>&1
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -q -rx > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/pytest.txt 2>&1
node --test tests/*.mjs > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/node.txt 2>&1
git fetch origin fix/notice-reliability
git merge --ff-only origin/fix/notice-reliability
git status --porcelain
git rev-parse HEAD
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -q -rx > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/pytest-final.txt 2>&1
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -v tests/test_m4_audit.py tests/test_explanation.py::test_bad_english_number_regenerates_once_then_template_fallback > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/explicit-proofs.txt 2>&1
```

The first full suite ran at fc24651 (383 tests); the fast-forward added only eight audit proofs and their disclosure, and the final clean suite at 6c13e08925fa88643957d9dc777d65b6136a70ae passed 391. git status was empty before the final tests. No production code was changed.

App startup (long-running terminal, no copied credentials):

```sh
cd /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010 --no-access-log > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/server.txt 2>&1
```

The in-memory HTTP smoke script is retained as `privacy-probe.py` beside this file. It runs shell/health/read/extract/explain checks, no-store/private-path assertions and a before/after storage inventory; it makes no model call.

```sh
cd /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python work/m4_audit_privacy_probe.py > work/m4-audit-logs/app-smoke.txt 2>&1
```

Live commands executed sequentially by the recorded runner; the .env path contains no key value in the command line:

```sh
cd /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean
env -u OPENAI_API_KEY TESSERACT_CMD=/opt/homebrew/bin/tesseract /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m eval.run --set dev --repeats 1 --env-file /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp/.env --out /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp/results/m4-verification/dev.json
env -u OPENAI_API_KEY TESSERACT_CMD=/opt/homebrew/bin/tesseract /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m eval.run --set adversarial --repeats 1 --env-file /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp/.env --out /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp/results/m4-verification/adversarial.json
```

Each command's stdout/stderr was captured to dev-eval.txt/adversarial-eval.txt. The runner is retained as `audit-runner.py`. No held-out command was executed.

Privacy commands from the clean checkout:

```sh
rg -n --glob '*.py' 'open\(|write|save\(|logger\.|tempfile' backend > ../m4-audit-logs/storage-code.txt
rg -n --glob '*.js' --glob '!**/vendor/**' 'localStorage|sessionStorage|indexedDB|console\.|caches\.' frontend > ../m4-audit-logs/browser-storage-code.txt
rg -n 'M4AUDITPRIVACYZZ91|PRIVATE-M4-CONTENT-SENTINEL|SENSITIVE-NOTICE-CONTENT|private-notice-filename|m4-audit-private-sentinel' ../m4-audit-logs/server.txt ../m4-audit-logs/privacy-runtime.log
```

The final rg exited 1: no matches. The captured privacy log was generated with:

```sh
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -v tests/test_field_validation.py::test_text_values_need_actual_source_phrases tests/test_field_validation.py::test_missing_is_missing_not_a_guessed_value tests/test_explanation.py::test_bad_english_number_regenerates_once_then_template_fallback tests/test_read.py::test_no_notice_data_left_on_disk tests/test_extract.py::test_extraction_keeps_text_out_of_logs_files_and_errors tests/test_explanation.py::test_language_privacy_on_success_and_failures tests/test_m4_robustness.py::test_entire_api_flow_leaves_no_notice_translation_or_explanation_on_disk_or_logs --log-file=/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/privacy-runtime.log --log-file-level=INFO > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/targeted-tests.txt 2>&1
```

Earlier default-Python attempt, retained in install.txt and stopped during the OpenCV source build (not the successful audit environment):

```sh
cd /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-clean
python3 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt > /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-logs/install.txt 2>&1
```
