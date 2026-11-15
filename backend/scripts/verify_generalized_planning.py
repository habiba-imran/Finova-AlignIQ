"""Fresh client-style ordinary TMT evidence. --live calls Groq once per module."""
import argparse
import hashlib
import json
import logging
from pathlib import Path
import sys

import httpx

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
from app.interactive.models import InteractiveSubmission
from app.interactive.service import generate_interactive
from app.interactive.narrative import load_planning_settings
from app.reports.settings import ReportSettings
from app.reports.groq_client import GroqClient


def main():
    parser=argparse.ArgumentParser()
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--mock',action='store_true'); modes.add_argument('--live',action='store_true')
    args=parser.parse_args()
    output=ROOT/'evidence/generalized-planning';output.mkdir(exist_ok=True)
    fixtures=ROOT/'backend/tests/fixtures'
    inputs={case:(fixtures/name).read_text(encoding='utf-8') for case,name in {
        'A':'analysis_15_tooth.md','B':'generalized_lower.md','C':'generalized_new.tsv','D':'generalized_sparse.tsv'}.items()}
    (output/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
    settings=ReportSettings(api_key='SYNTHETIC_TEST_ONLY',synthetic_transmission_enabled=True) if args.mock else ReportSettings()
    if args.live:
        from app.development_env import load_development_env
        load_development_env(ROOT/'.env.local')
        settings=load_planning_settings()
    records=[]
    for case,raw in inputs.items():
        if args.live and case!='C': continue
        for module in ('macro','micro','nano'):
            sizes=[]
            def handler(req):
                messages=json.loads(req.content)['messages'];sizes.append(len(json.dumps(messages).encode()))
                payload=json.loads(messages[1]['content'])
                answer=dict(sections=[dict(section_id=s['section_id'],text='\n\n'.join('{'+f['ref']+'}' for f in s['findings'])) for s in payload['sections']])
                return httpx.Response(200,json=dict(model=settings.model,choices=[dict(finish_reason='stop',message=dict(role='assistant',content=json.dumps(answer)))]))
            client=GroqClient(settings,transport=httpx.MockTransport(handler)) if args.mock else None
            submission=InteractiveSubmission(raw_text=raw,raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),module=module,synthetic_data_confirmed=True,planning_options={})
            report=generate_interactive(submission,settings=settings,client=client)
            suffix='-mock' if args.mock else '-live' if args.live else ''
            stem=f'{case}-{module}{suffix}'
            (output/(stem+'.json')).write_text(report.model_dump_json(indent=2),encoding='utf-8')
            (output/(stem+'.txt')).write_text(report.export_text,encoding='utf-8')
            record=dict(case=case,module=module,**report.generation.model_dump(),decisions=len(report.functional_plan.decisions),
                review_topics=len(report.functional_plan.review_outline),stages=len(report.functional_plan.stages))
            if args.mock:
                assert len(sizes)==1 and report.generation.used_mode=='GROQ_AI'
                record['prompt_bytes']=sizes[0]
            records.append(record)
    (output/(('mock' if args.mock else 'live' if args.live else 'offline')+'-summary.json')).write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(records,indent=2))


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    main()
