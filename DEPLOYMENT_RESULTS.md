# Step 4 — Render deployment result

## Current release — October 26

The polished app and manual-type wording fix are now live at https://notice-decoder-ns5o.onrender.com, commit `e25b3c118fbe05b5680b76782cf88ac7acc7afbd`, Render deploy `dep-dbferbg473hc73cto1f0`. Hosting checks pass 12/12; local tests pass 430 Python and 62 JavaScript. The previous application commit completed an actual synthetic upload/extract/English/Spanish/Tagalog browser flow. The final change is copy and cache version only. See [current release evidence](results/release-2026-10-26/REPORT.md) and [checklist](RELEASE_CHECKLIST.md).

Full phone acceptance is **not passed**: the user's iPhone test exposed an unresolved reading issue, reproduced locally on the linked photo. Physical-device installation/audio, deployed English fallback, blank-image rejection and offline acceptance remain incomplete. No original held-out rerun or broad reliability claim is made. The historical first-deployment record below is retained for provenance; its old “pending Step 5” and test counts are not current release status.

## First deployment — October 25 (historical)

Checked 2026-10-25. **Hosting deployment: PASS. Full deployed functional/mobile acceptance: pending Step 5.**

Live app: https://notice-decoder-ns5o.onrender.com

Render service srv-dbfbm7dg1s2s73f6fk70, deployment dep-dbfbm7lg1s2s73f6fksg, status Live. Source: fix/notice-reliability commit 96911c952a3fb5ccc776ca038041c90d5588c29d. The personal My Workspace selected Free ($0/month). API-provider usage is separate from free hosting. The user entered OPENAI_API_KEY directly in Render and submitted; no secret value was retrieved from the dashboard.

| Item | Status | Evidence / boundary |
|---|---|---|
| One public HTTPS URL serves PWA + backend | PASS | Render Live; page and /api/health return 200 in https-smoke.json |
| Container builds and starts on host | PASS | Render deployment reached Live; health and static content respond |
| Key absent from client and reachable Git history | PASS for audited source/history | secret-audit.json: 428 reachable blobs, zero configured-key/credential-like matches; ignored/untracked .env is owner-only 0600 |
| Server secrets via host env | Configured by user | User entered key directly in Render; Dockerfile never copies .env or uses secret build ARGs. Valid model-backed inference remains Step 5 |
| CORS/browser origin locked to deployed origin | PASS | Exact-origin preflight allowed; foreign-origin POST rejected 403; no wildcard |
| Analysis endpoints rate limited | PASS in code/regression tests | /api/read, /api/extract, /api/explain share 30/minute and 240/hour global budgets, one in-flight analysis. tests/test_deployment.py passes. Live exhaustion was not forced |
| Clear limit/quota failure message | PASS in controlled tests | Fixed localized UI strings for 429/503; controller tests pass without displaying provider bodies. No hard dollar spend cap is claimed; counters reset on restart |
| Private files inaccessible | PASS | /.env, /.git/config, /backend/main.py and evaluation artifact path return 404 |
| Manifest, icons and service-worker asset | PASS for HTTP metadata/assets | Standalone manifest, icon requests and shell-v10 asset pass. Does not prove phone installation or offline completion |
| Local regressions | PASS | 422 Python, 21 JavaScript passes; existing dependency deprecation warning |
| GitHub cloud tests | PENDING at this check | Run 40258877041 still in progress; local passes are not substituted for remote success |
| Notice upload/model/Spanish/Tagalog/read-aloud/error scenarios | PENDING | No notice uploaded or model called during this hosting smoke; complete in Step 5 |

## Exact smoke command

From the repository root:

```sh
/Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/m4-audit-venv/bin/python /Users/anushkajain/Documents/Codex/2026-10-21/files-pasted-by-the-user-project/work/check_deployed_notice.py --url https://notice-decoder-ns5o.onrender.com --out results/deployment/https-smoke.json
```

The exact helper is retained byte-for-byte as results/deployment/https-smoke.py for reproducibility. All 11 booleans in the output are true. This command used no credentials, notices or model calls. Screenshot: results/deployment/live-app.png. Render identity/source: results/deployment/live-deployment.json. Original held-out inputs/results, prompts, fact validators and eval-freeze are unchanged.

## Operational limits

Free service can sleep after inactivity and take roughly a minute to wake. One process/instance is required by the in-memory receipt signing and request budgets. Rate limits are shared by all visitors, can reset on restarts, and are not a dollar spend cap or authentication. Forged Origin from non-browser clients does not establish trust; browser CORS is not authentication. No persistent notice storage or database was provisioned. Host request/log retention and provider retention are separate from application in-memory handling.

The container build installed Debian Tesseract 5.3.0; earlier local evaluation used 5.5.3. Held-out/dev numbers are not new production-environment OCR measurements. Classifier lists remain empty and require manual type selection. Glossaries and the new Spanish/Tagalog service-error strings remain unreviewed. Phone voice availability, camera capture, installation, target-language results and usable fallback behavior still require deployed acceptance.

Stopped after deployment as requested; AI disclosure has been deferred, and submission readiness is not claimed.
