"""Public deployment smoke: no notices, credentials or model calls."""
import argparse,json
from pathlib import Path
from urllib.parse import urlsplit
import httpx
p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
u=urlsplit(args.url)
assert u.scheme=='https' and u.hostname and not u.query and not u.fragment and not u.username and not u.password
base=args.url.rstrip('/')
checks={}
with httpx.Client(base_url=base,timeout=90,trust_env=False,follow_redirects=True) as c:
 health=c.get('/api/health');checks['health_200']=health.status_code==200 and health.json().get('status')=='ok'
 shell=c.get('/');checks['page_https_200']=shell.status_code==200 and shell.url.scheme=='https'
 checks['mobile_viewport_present']='name="viewport"' in shell.text
 checks['legal_disclaimer_present']='not legal advice' in shell.text
 manifest=c.get('/manifest.webmanifest');data=manifest.json();checks['manifest_standalone']=manifest.status_code==200 and data['display']=='standalone'
 checks['manifest_icons_200']=all(c.get(icon['src']).status_code==200 for icon in data['icons'])
 sw=c.get('/sw.js');checks['service_worker_shell_v10']=sw.status_code==200 and 'notice-decoder-shell-v10' in sw.text
 checks['health_no_store']=health.headers.get('cache-control')=='no-store'
 checks['private_paths_404']=all(c.get(path).status_code==404 for path in ('/.env','/.git/config','/backend/main.py','/results/deployment/secret-audit.json'))
 wrong=c.post('/api/extract',headers={'Origin':'https://untrusted.example'},content='synthetic blocked request')
 checks['foreign_browser_origin_403']=wrong.status_code==403 and 'access-control-allow-origin' not in wrong.headers
 pre=c.options('/api/extract',headers={'Origin':base,'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type'})
 checks['exact_origin_preflight']=pre.status_code==200 and pre.headers.get('access-control-allow-origin')==base
r={'url':base,'checks':checks,'all_passed':all(checks.values()),'model_calls':0,'notice_uploads':0,'credential_access':False,'limits':'Does not establish analysis/translation, phone installation/read-aloud, offline handling, spend cap or container health beyond these requests.'}
args.out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2));assert r['all_passed']
