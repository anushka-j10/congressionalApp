from pathlib import Path
import subprocess,os,json
base=Path.cwd();checkout=base/'work/m4-audit-clean';python=base/'work/m4-audit-venv/bin/python'
logs=base/'work/m4-audit-logs';out=base/'outputs/congressionalApp/results/m4-verification';envfile=base/'outputs/congressionalApp/.env'
environment=os.environ.copy();environment.pop('OPENAI_API_KEY',None);environment['TESSERACT_CMD']='/opt/homebrew/bin/tesseract'
commands=[]
for name in ['dev','adversarial']:
 command=[str(python),'-m','eval.run','--set',name,'--repeats','1','--env-file',str(envfile),'--out',str(out/(name+'.json'))]
 commands.append(command)
 with (logs/(name+'-eval.txt')).open('w') as handle:
  result=subprocess.run(command,cwd=checkout,env=environment,stdout=handle,stderr=subprocess.STDOUT)
 print(name,'runner exit',result.returncode,flush=True)
 if result.returncode:raise SystemExit(result.returncode)
 r=json.loads((out/(name+'.json')).read_text())
 print(name,r['status'],len(r['records']),'/',r['planned_records'],flush=True)
 for mode in ['B1','B2','full']:
  print(mode,r['summary'][mode]['headline_critical']['false_verified_rate'],flush=True)
(logs/'eval-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
