"""Reproducible fictional scenarios; --mock/--live verify the real wording client."""
import argparse
import json
import logging
from pathlib import Path
import sys
import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
from app.functional.scenarios import scenario
from app.interactive.models import InteractiveSubmission
from app.interactive.service import generate_interactive
from app.interactive.narrative import load_planning_settings
from app.reports.settings import ReportSettings
from app.reports.groq_client import GroqClient


def request(bundle):
    return InteractiveSubmission(raw_text=bundle['raw_text'],module=bundle['module'],raw_sha256=bundle['planning_context']['source_sha256'],
        synthetic_data_confirmed=True,planning_context=bundle['planning_context'],review_details=bundle['review_details'])


def main():
    args = argparse.ArgumentParser()
    modes = args.add_mutually_exclusive_group()
    modes.add_argument('--mock',action='store_true'); modes.add_argument('--live',action='store_true')
    options = args.parse_args()
    output = ROOT/'evidence/functional-planning'
    output.mkdir(parents=True,exist_ok=True)
    settings = ReportSettings(api_key='SYNTHETIC_TEST_ONLY',synthetic_transmission_enabled=True) if options.mock else ReportSettings()
    if options.live:
        from app.development_env import load_development_env
        load_development_env(ROOT/'.env.local')
        settings = load_planning_settings()
    records = []
    for name in ('macro-distribution','micro-catalog','nano-phases'):
        b = scenario(name); calls = []
        def handler(req):
            data = json.loads(req.content); calls.append(len(json.dumps(data['messages']).encode()))
            prompt = json.loads(data['messages'][1]['content'])
            answer = dict(sections=[dict(section_id=s['section_id'],text='\n\n'.join('{'+f['ref']+'}' for f in s['findings'])) for s in prompt['sections']])
            return httpx.Response(200,json={'model':settings.model,'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(answer)}}]})
        client = GroqClient(settings,transport=httpx.MockTransport(handler)) if options.mock else None
        report = generate_interactive(request(b),settings=settings,client=client)
        suffix = '-mock' if options.mock else '-live' if options.live else ''
        (output/(b['module']+suffix+'.json')).write_text(report.model_dump_json(indent=2),encoding='utf-8')
        (output/(b['module']+suffix+'.txt')).write_text(report.export_text,encoding='utf-8')
        if not suffix:
            (output/(b['module']+'-input.json')).write_text(json.dumps(b,indent=2),encoding='utf-8')
        record = dict(module=b['module'],**report.generation.model_dump(),decisions=len(report.functional_plan.decisions))
        if options.mock:
            assert report.generation.used_mode == 'GROQ_AI' and len(calls) == 1
            record['prompt_bytes'] = calls[0]
        records.append(record)
    (output/(('mock' if options.mock else 'live' if options.live else 'offline')+'-summary.json')).write_text(json.dumps(records,indent=2),encoding='utf-8')
    print(json.dumps(records,indent=2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    main()
