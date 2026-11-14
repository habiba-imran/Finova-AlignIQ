import json,sys,httpx
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root/'backend'))
from app.development_env import load_development_env
from app.interactive.models import InteractiveSubmission
from app.interactive.narrative import load_planning_settings
from app.interactive.service import generate_interactive
from app.reports.groq_client import GroqClient
load_development_env(root/'.env.local')
settings=load_planning_settings();module=sys.argv[1] if len(sys.argv)>1 else 'micro'
source=json.loads((root/'evidence/planning-wording/user-synthetic-live-report.json').read_text(encoding='utf-8'))['parsed']
out=root/'evidence/deployed-wording-diagnosis';out.mkdir(exist_ok=True)
class DiagnosticTransport(httpx.BaseTransport):
 def __init__(self): self.inner=httpx.HTTPTransport()
 def handle_request(self,request):
  response=self.inner.handle_request(request)
  if response.status_code>=400:
   data=response.read()
   try:
    error=json.loads(data).get('error',{})
    message=str(error.get('message','')).replace(settings.api_key.get_secret_value(),'[redacted]')
    print(json.dumps({'http_status':response.status_code,'error_code':error.get('code'),'error_type':error.get('type'),'message':message[:800]}),flush=True)
   except ValueError: pass
  return response
 def close(self): self.inner.close()
class AuditClient(GroqClient):
 def generate(self,*args,**kwargs):
  result=super().generate(*args,**kwargs)
  print(json.dumps({'module':module,'http_status':result.http_status,'code':result.code,'seconds':result.elapsed_seconds,'prompt_tokens':result.prompt_tokens,'completion_tokens':result.completion_tokens}),flush=True)
  if result.content:(out/f'provider-fixed-{module}.json').write_text(result.content,encoding='utf-8')
  return result
request=InteractiveSubmission(raw_text=source['raw_text'],raw_sha256=source['raw_sha256'],module=module,synthetic_data_confirmed=True,context=source['source']['context'])
report=generate_interactive(request,settings=settings,client=AuditClient(settings,transport=DiagnosticTransport()))
(out/f'local-fixed-{module}.json').write_text(report.model_dump_json(indent=2),encoding='utf-8')
print(json.dumps({'generation':report.generation.model_dump(mode='json'),'openings':len({tuple(o.text.split()[:3]) for o in report.observations}),'sample':report.observations[7].text}),flush=True)
