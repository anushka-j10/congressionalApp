# Commands used — 2026-10-25

Run from `/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp` unless a different working directory is specified. These commands do not read .env or invoke a model. No held-out command was used.

```sh
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -q
node --test tests/*.mjs
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m eval.ablations --input results/m4-verification/dev.json --out results/m4-ablations/dev.json
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m eval.ablations --input results/m4-verification/adversarial.json --out results/m4-ablations/adversarial.json
git clone --no-local --branch fix/notice-reliability /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/outputs/congressionalApp /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-ablation-clean
```

In the clean clone:

```sh
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pip install --disable-pip-version-check --no-index -r requirements.txt
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m pytest -q
node --test tests/*.mjs
env -u OPENAI_API_KEY /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8011 --no-access-log
```

From the main repo, while the clean server runs:

```sh
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python results/m4-ablations/privacy-probe.py
rg -n 'M4ABLATIONPRIVACYZZ92|m4-audit-private-sentinel.png' results/m4-ablations/server.txt
```

Output redirections saved stdout to the correspondingly named .txt files in this directory. An initial exploratory dev replay was discarded before generating the final reports after all code/tests were complete. The server was stopped after the smoke check. Existing warning: dependency alias deprecation; pip's cache is unavailable in sandbox (requirements already satisfied, no downloads).
