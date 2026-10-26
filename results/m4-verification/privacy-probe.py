from pathlib import Path
import io,json,os
import httpx
from PIL import Image,ImageDraw,ImageFont
checkout=Path('work/m4-audit-clean').resolve()
def inventory():
 result=[]
 for folder,dirs,names in os.walk(checkout):
  dirs[:]=[n for n in dirs if n not in {'.git','.venv','__pycache__','.pytest_cache','heldout'}]
  result.extend(str((Path(folder)/n).relative_to(checkout)) for n in names)
 return set(result)
before=inventory()
image=Image.new('RGB',(1000,400),'white');draw=ImageDraw.Draw(image)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
for n,line in enumerate(['SYNTHETIC INFORMATION PAGE','M4AUDITPRIVACYZZ91','This is an informational demonstration only.']):draw.text((35,35+n*80),line,font=font,fill='black')
data=io.BytesIO();image.save(data,format='PNG')
with httpx.Client(base_url='http://127.0.0.1:8010',timeout=60,trust_env=False) as client:
 health=client.get('/api/health');assert health.status_code==200
 read=client.post('/api/read',files={'image':('m4-audit-private-sentinel.png',data.getvalue(),'image/png')});assert read.status_code==200
 extracted=client.post('/api/extract',json={'text':read.json()['text'],'doc_type':'unknown','text_confirmed':True});assert extracted.status_code==200
 fields=extracted.json();assert all(x['status']=='missing' for x in fields['fields'].values())
 explained=client.post('/api/explain',json={'doc_type':'unknown','fields':fields['fields'],'today':fields['today'],'receipt':fields['receipt'],'language':'en'});assert explained.status_code==200
 private=['/.env','/backend/main.py','/.git/config','/results/reliability-dev.json','/eval/heldout/answers.docx']
 for path in private:assert client.get(path).status_code==404
 for r in [health,read,extracted,explained]:assert r.headers['cache-control']=='no-store'
 assert client.get('/').status_code==200
 assert inventory()==before
 print('Clean-clone app: shell/health/read/extract/explain HTTP 200; all APIs no-store; five private paths HTTP 404; no new persisted notice/storage files.')
 print('This success flow uses unknown-type/static explanations, no paid model request; live model behavior is tested separately by the eval runs.')
