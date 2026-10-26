"""Public release checks; no credentials, real notices, or model requests."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'https://notice-decoder-ns5o.onrender.com'
COMMIT = 'e6f9933818d055e436b157aff081aa08be0f962e'
checks, hashes = {}, {}
with httpx.Client(base_url=BASE, timeout=90, trust_env=False, follow_redirects=True) as c:
    health = c.get('/api/health')
    checks['health_200'] = health.status_code == 200 and health.json().get('status') == 'ok'
    shell = c.get('/')
    checks['https_page_200'] = shell.status_code == 200 and shell.url.scheme == 'https'
    checks['mobile_viewport'] = 'name="viewport"' in shell.text
    checks['disclaimer'] = 'not legal advice' in shell.text
    manifest = c.get('/manifest.webmanifest')
    checks['standalone_manifest'] = manifest.status_code == 200 and manifest.json()['display'] == 'standalone'
    checks['icons_200'] = all(c.get(i['src']).status_code == 200 for i in manifest.json()['icons'])
    sw = c.get('/sw.js')
    checks['shell_v21'] = 'notice-decoder-shell-v21' in sw.text
    checks['api_no_store'] = health.headers.get('cache-control') == 'no-store'
    checks['private_paths_404'] = all(c.get(p).status_code == 404 for p in ('/.env', '/.git/config', '/backend/main.py', '/results/deployment/secret-audit.json'))
    foreign = c.post('/api/extract', headers={'Origin': 'https://untrusted.example'}, content='synthetic blocked request')
    checks['foreign_origin_rejected'] = foreign.status_code == 403 and 'access-control-allow-origin' not in foreign.headers
    preflight = c.options('/api/extract', headers={'Origin': BASE, 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'content-type'})
    checks['exact_origin_allowed'] = preflight.status_code == 200 and preflight.headers.get('access-control-allow-origin') == BASE
    for name in ('index.html', 'app.js', 'styles.css', 'onboarding.js', 'field-cards.js', 'explanation.js', 'parking.js', 'parking-data.js', 'en.json', 'sw.js', 'token-review.js'):
        response = c.get('/' + name)
        local = hashlib.sha256((ROOT / 'frontend' / name).read_bytes()).hexdigest()
        remote = hashlib.sha256(response.content).hexdigest()
        hashes[name] = {'local': local, 'deployed': remote, 'match': response.status_code == 200 and local == remote}
    checks['eleven_deployed_assets_match_release'] = all(h['match'] for h in hashes.values())
    config = c.get('/api/config').json()
result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'url': BASE, 'commit': COMMIT, 'checks': checks, 'passed': sum(checks.values()), 'total': len(checks), 'asset_hashes': hashes, 'public_config': config, 'model_calls': 0, 'notice_uploads': 0, 'credential_access': False}
(OUT / 'https-smoke.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'asset_hashes'}, indent=2))
assert all(checks.values())
