# Render deployment

Latest release checked October 26: https://notice-decoder-ns5o.onrender.com. One Docker web service serves the PWA and FastAPI under the same HTTPS origin. Commit e25b3c1 is deployed and 12/12 public HTTPS checks pass. A synthetic browser upload/extraction/English/Spanish/Tagalog flow passed before the final copy-only fix. Full phone and failure-state acceptance remains incomplete, including a user-reported reading failure; see DEPLOYMENT_RESULTS.md and RELEASE_CHECKLIST.md. No held-out inference or fact-validator/model-prompt change is part of this release.

## Configuration

- Dockerfile installs Tesseract with English data and the pinned Python requirements, copies only backend/ and frontend/, and runs as a non-root user.
- The container uses one Uvicorn worker, binds 0.0.0.0:$PORT and disables access logs and forwarded-IP interpretation. Receipt signing and request counters are process-local. Do not increase worker count or service instance count without revisiting those controls.
- APP_ENV=production or Render's RENDER=true enables the browser-origin and request controls. The exact HTTPS origin is Render's injected RENDER_EXTERNAL_URL, or PUBLIC_ORIGIN if explicitly set. No path/trailing slash is allowed; no wildcard CORS origin is used.
- /api/read, /api/extract and /api/explain share a global limit of 30 admitted POSTs per minute and 240 per hour, with one analysis request in flight at a time. All users share this demo budget; no client identifier is stored. Forwarded-IP spoofing cannot create new buckets. Invalid admitted requests count toward the budget too. Health and PWA shell requests remain available when the budget is exhausted.
- Counters reset on restart and do not enforce a dollar spend cap. Origin checks protect browser requests, not curl clients or attackers who forge Origin. API account quotas remain necessary. The UI gives fixed, localized messages for request limits and service/quota unavailability; provider response bodies are not shown.
- Rate-limit retries may still be denied while the hourly allowance is exhausted; the UI says so. No notice contents or request bodies are added to logs by these controls.

## Dashboard steps

1. Sign into your personal Render account and select its intended workspace. Choose New → Web Service → Public Git Repository. Public-URL deployment avoids granting Render access to additional GitHub repositories.
2. Connect https://github.com/anushka-j10/congressionalApp. Select branch fix/notice-reliability, repository root, Docker runtime and Dockerfile ./Dockerfile. A reproducible render.yaml is also included; its free plan and manual deployment settings express the same service configuration.
3. Choose Free, one instance, and health path /api/health. Keep the Docker command from Dockerfile and automatic deploys off. Do not add a disk or database. If the UI requests a paid plan or payment method, stop rather than upgrade.
4. Under Environment add APP_ENV=production, TEXT_READER=preprocessed, TESSERACT_CMD=/usr/bin/tesseract and OPENAI_MODEL=gpt-5.4-mini-2026-03-17. Render supplies PORT and RENDER_EXTERNAL_URL; PUBLIC_ORIGIN is only needed for a later custom domain or explicit override.
5. Add OPENAI_API_KEY directly in Render's environment-variable value field using the private local .env value. Do not put it in Git, a Docker build ARG, public frontend settings, a URL, chat or a screenshot. Do not upload the .env file as source. This must be a project key whose billing/quota allows the configured model.
6. Save and deploy. Wait until the specific deployment is Live; a queued build or successful create request is not completion. If variables were saved without deploying, they do not take effect until another deployment. Use the HTTPS URL shown by Render, not a guessed hostname.
7. Open that URL on a phone and perform the deployed acceptance checks. The app prompts for manual notice-type selection because production classifier signal lists remain empty. Real-phone voice/installation behavior and native translation review are separate checks, not implied by server health.

## Free-host limits and checks

Render's free service sleeps after 15 idle minutes; the documented wake-up takes about a minute. Free hosting quotas and API usage are separate. The local/container filesystem is ephemeral, and the application does not use it to retain notices. Do not use an artificial keep-alive monitor to imply production availability.

Preparation evidence: results/deployment/pytest.txt (422 Python passes), node.txt (21 JavaScript passes), secret-audit.json (aggregate counts only). One pre-existing dependency deprecation warning remains. A Docker daemon is not installed locally; the Docker build and startup were instead verified by the successful Live Render deployment. Build output installed Debian Tesseract 5.3.0, whereas the local evaluation used 5.5.3. Existing evaluation scores are not claimed as measurements of the deployed reader version.

The code changes are limited to the deployment boundary and friendly 429/503 UI messages. New Spanish/Tagalog error-message strings are generated and remain unreviewed, like the existing glossaries. Extraction prompts, deterministic fact validators, answer keys and original freeze tag are unchanged.

Official references checked: [Docker](https://render.com/docs/docker), [web services](https://render.com/docs/web-services), [free limitations](https://render.com/docs/free), [environment variables](https://render.com/docs/configure-environment-variables), [default variables](https://render.com/docs/environment-variables), [Blueprint specification](https://render.com/docs/blueprint-spec), [deployment lifecycle](https://render.com/docs/deploys), [health checks](https://render.com/docs/health-checks). These describe hosting behavior, not evidence that this service has already passed its checks.
