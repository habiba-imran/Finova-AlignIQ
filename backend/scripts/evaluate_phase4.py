"""Independent gold comparison. Default is explicitly oracle-mocked, NOT model accuracy.

--live 1..3 optionally measures the actual Groq model on fixed synthetic recipes.
Only counters/static codes/timing/usage print; no inputs, outputs or secrets print.
"""
import argparse
import json
import os
from pathlib import Path
import sys

import httpx

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.development_env import load_development_env  # noqa: E402
from app.parser.cloud import ParserSettings  # noqa: E402
from app.parser.contracts import PipelineSubmission, SyntheticFixture  # noqa: E402
from app.parser.generated import generate  # noqa: E402
from app.parser.phase4 import deterministic, parse_pipeline  # noqa: E402
from app.reports.groq_client import GroqClient  # noqa: E402


def correct_positions(result,gold):
    teeth={t.id:t for t in result.teeth}
    found={(teeth[m.tooth_ref].span.start,m.header_span.start,m.span.start):m for m in result.measurements if m.span}
    count=0
    for g in gold:
        key=tuple(g['spans'][role][0] for role in ('tooth','label','value'))
        m=found.get(key)
        if m and m.raw_value==g['value'] and m.raw_label==g['label'] and (str(m.signed_decimal) if m.signed_decimal is not None else None)==g['decimal'] and m.numeric_status!='AMBIGUOUS': count+=1
    return count


def evaluate():
    dataset=json.loads((Path(__file__).resolve().parents[2]/'examples/phase4-synthetic-dataset.json').read_text(encoding='utf-8'))
    totals=dict(fixtures=0,supported_fixtures=0,gold_positions=0,deterministic_correct_positions=0,hybrid_correct_positions=0,
                deterministic_complete_fixtures=0,hybrid_complete_fixtures=0,mocked_provider_calls=0,forbidden_input_calls=0)
    settings=ParserSettings(api_key='SYNTHETIC_MOCK',environment='development',synthetic_transmission_enabled=True)
    for record in dataset['fixtures']:
        sub=PipelineSubmission(raw_text=record['raw_text'],synthetic_data_confirmed=True,synthetic_fixture=SyntheticFixture(**record['identity']))
        gold=record['gold'];calls=[]
        def handler(req):
            calls.append(1)
            return httpx.Response(200,json={'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps({'associations':[g['association'] for g in gold]})}}]})
        baseline=deterministic(sub)
        hybrid=parse_pipeline(sub,settings=settings,client=GroqClient(settings,transport=httpx.MockTransport(handler)))
        d,h=correct_positions(baseline,gold),correct_positions(hybrid,gold)
        totals['fixtures']+=1;totals['gold_positions']+=len(gold)
        totals['deterministic_correct_positions']+=d;totals['hybrid_correct_positions']+=h
        totals['supported_fixtures']+=bool(gold)
        totals['deterministic_complete_fixtures']+=bool(gold) and d==len(gold)
        totals['hybrid_complete_fixtures']+=bool(gold) and h==len(gold)
        totals['mocked_provider_calls']+=len(calls)
        totals['forbidden_input_calls']+=len(calls) if not gold else 0
    return {'mode':'INDEPENDENT_GOLD_ORACLE_MOCK_NOT_MODEL_ACCURACY',**totals}


def live(count,recipes=('mixed_rows','wrapped','fragments')):
    if not os.environ.get('GROQ_API_KEY_2'): return [{'status':'SKIPPED','reason':'PARSER_KEY_NOT_CONFIGURED','attempts':0}]
    results=[]
    settings=ParserSettings(api_key=os.environ['GROQ_API_KEY_2'],environment='development',synthetic_transmission_enabled=True,timeout_seconds=15,max_completion_tokens=4096)
    class Measured(GroqClient):
        last=None
        def generate(self,*args,**kwargs):
            self.last=super().generate(*args,**kwargs);return self.last
    for recipe in recipes[:count]:
        identity=SyntheticFixture(recipe=recipe,seed=17);sample=generate(identity)
        sub=PipelineSubmission(raw_text=sample.raw_text,synthetic_fixture=identity,synthetic_data_confirmed=True)
        c=Measured(settings);r=parse_pipeline(sub,settings=settings,client=c)
        results.append({'recipe':recipe,'status':r.pipeline.assistance.status,'reason':r.pipeline.assistance.reason,
            'gold_positions':len(sample.gold),'correct_positions':correct_positions(r,sample.gold),'attempts':r.pipeline.assistance.attempts,
            'elapsed_seconds':c.last.elapsed_seconds,'http_status':c.last.http_status,'model_matches':c.last.model_matches,
            'prompt_tokens':c.last.prompt_tokens,'completion_tokens':c.last.completion_tokens,'total_tokens':c.last.total_tokens})
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live',type=int,choices=[0,1,2,3],default=0)
    parser.add_argument('--env-file',type=Path)
    parser.add_argument('--live-recipes',nargs='+',choices=['mixed_rows','wrapped','fragments'],default=['mixed_rows','wrapped','fragments'])
    args=parser.parse_args()
    if args.env_file: load_development_env(args.env_file)
    print(json.dumps({'deterministic_comparison':evaluate(),'optional_live_results':live(args.live,args.live_recipes) if args.live else []},indent=2))


if __name__=='__main__': main()
