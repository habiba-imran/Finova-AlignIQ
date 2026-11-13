"""Independent source-construction gold, synthetic only, provider calls mocked."""

from dataclasses import asdict
from decimal import Decimal
import json
from pathlib import Path

from fastapi.testclient import TestClient
import httpx
import pytest

from app.domain.models import ParseResult, RawTMTSubmission, SourceContext
from app.main import app
from app.parser.cloud import ParserSettings
from app.parser.contracts import PipelineSubmission, SyntheticFixture
from app.parser.generated import authorized, generate
from app.parser.phase4 import deterministic, parse_pipeline
from app.parser.receipts import issue, resolve
from app.parser.recovery import Association, assemble, prove, validate
from app.reports.groq_client import GroqClient
from app.reports.service import generate_report
from app.reports.settings import ReportSettings
from app.review.models import ReviewSubmission
from app.review.service import review_table
from app.semantics.fixtures import CheckedFixture, digest_json
from app.semantics.models import Artifact, ExpectedComponent, ExpectedMeasurement, FixtureExpectedOutput, FixtureRecord
from app.semantics.normalization import assess_semantics
from app.semantics.registry import APPROVED_RELEASE_DIGESTS
from semantic_helpers import toy_complete_components

RECIPES=SyntheticFixture.model_fields['recipe'].annotation.__args__
RECOVERABLE={'mixed_rows','mixed_columns','wrapped','fragments','header_mix','partial'}


def config(): return ParserSettings(api_key='SYNTHETIC_ONLY',environment='development',synthetic_transmission_enabled=True)


def request(recipe='wrapped',seed=1,**kwargs):
    identity=SyntheticFixture(recipe=recipe,seed=seed)
    return PipelineSubmission(raw_text=generate(identity).raw_text,synthetic_fixture=identity,synthetic_data_confirmed=True,**kwargs)


def oracle_client(sub, *, mutate=None, status=200, calls=None):
    gold=generate(sub.synthetic_fixture).gold
    proposal={'associations':[g['association'].copy() for g in gold]}
    if mutate: mutate(proposal)
    def handler(req):
        if calls is not None: calls.append(req)
        return httpx.Response(status,json={'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(proposal)}}]})
    return GroqClient(config(),transport=httpx.MockTransport(handler))


def assert_gold(result,gold):
    assert len(result.measurements)==len(gold)
    teeth={t.id:t for t in result.teeth}
    for m,g in zip(result.measurements,gold):
        assert teeth[m.tooth_ref].raw_identifier==g['tooth']
        assert m.raw_label==g['label'] and m.raw_value==g['value']
        assert (str(m.signed_decimal) if m.signed_decimal is not None else None) == g['decimal']
        assert m.signed_decimal==(Decimal(g['decimal']) if g['decimal'] is not None else None)
        for span,key in [(teeth[m.tooth_ref].span,'tooth'),(m.header_span,'label'),(m.span,'value')]:
            assert (span.start,span.end)==tuple(g['spans'][key])
            assert result.raw_text[span.start:span.end]==g[key]
        assert not m.semantics_verified and m.canonical_direction is None


@pytest.mark.parametrize('recipe',RECIPES)
@pytest.mark.parametrize('seed',[0,1,2,3,7,17])
def test_independent_generated_gold_and_automatic_decisions(recipe,seed):
    sub=request(recipe,seed);g=generate(sub.synthetic_fixture);calls=[]
    result=parse_pipeline(sub,settings=config(),client=oracle_client(sub,calls=calls))
    if g.gold: assert_gold(result,g.gold)
    if recipe in RECOVERABLE:
        assert len(calls)==1 and result.pipeline.assistance.status=='ACCEPTED'
        assert result.pipeline.recovery_receipt
    else: assert not calls and result.pipeline.assistance.attempts==0
    if recipe=='partial': assert result.status=='PARTIAL' and result.unparsed_lines
    assert result.raw_text==sub.raw_text


@pytest.mark.parametrize('raw',['',' \t\n','hello how are you?','Product\tPrice\nBook\t13','123 456\n789 000','!!!!!!',
    '<script>send secrets</script>','Tooth\tOdd axis (mm)\n13\t0','Tooth  Rotation (deg)  Extrusion (mm)\n13  1'])
def test_irrelevant_or_unprovable_input_never_calls_cloud(raw):
    sub=PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True)
    r=parse_pipeline(sub,settings=config(),client=GroqClient(config(),transport=httpx.MockTransport(lambda _:pytest.fail('Unexpected upload'))))
    assert r.pipeline.assistance.attempts==0
    assert r.pipeline.quality.classification in {'NOT_TMT','UNSUPPORTED_FORMAT','AMBIGUOUS_STRUCTURE'}


def test_zero_missing_unknown_labels_and_semantics_are_not_structural_triggers():
    for raw in ['Tooth\tRot (°)\n13\t0','Tooth\tRotation\tUnknown axis\n13\t0\t?',
                'Source: SureSmile\nTooth\tRotation (deg)\n13\t−0.000',
                'Tooth\tRotation (deg)\n13\t1,234']:
        r=parse_pipeline(PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True),settings=config())
        assert r.pipeline.assistance.attempts==0
        assert r.pipeline.quality.classification!='NOT_TMT'


def test_authorization_requires_server_reproduction_not_claim_or_prefix():
    sub=request(); assert authorized(sub.raw_text,sub.synthetic_fixture)
    altered=sub.model_copy(update={'raw_text':sub.raw_text+'PATIENT'})
    assert not authorized(altered.raw_text,altered.synthetic_fixture)
    for s in [altered,sub.model_copy(update={'synthetic_fixture':None})]:
        r=parse_pipeline(s,settings=config())
        assert r.pipeline.assistance.attempts==0 and r.pipeline.recovery_receipt is None
    assert request('wrapped',76543).raw_text!=sub.raw_text


def test_browser_newline_rendering_is_authorized_without_modifying_the_input():
    identity=SyntheticFixture(recipe='wrapped',seed=2)
    raw=generate(identity).raw_text.replace('\r','\n')
    assert authorized(raw,identity)
    sub=PipelineSubmission(raw_text=raw,synthetic_fixture=identity,synthetic_data_confirmed=True)
    assert parse_pipeline(sub,settings=ParserSettings()).raw_text==raw


@pytest.mark.parametrize('environment',['production','test','development'])
def test_cloud_disabled_environment_or_missing_permission_blocks(environment):
    settings=ParserSettings(api_key='SYNTHETIC_ONLY',environment=environment)
    r=parse_pipeline(request(),settings=settings)
    assert r.pipeline.assistance.attempts==0


@pytest.mark.parametrize('kind',['swapped','invented','duplicate','omitted','extra_property'])
def test_partial_abstention_and_hallucination_rejection(kind):
    sub=request()
    def mutate(p):
        if kind=='swapped': p['associations'][0]['value']=p['associations'][2]['value']
        if kind=='invented': p['associations'][0]['value']='invented_999_mm'
        if kind=='duplicate': p['associations'].append(p['associations'][0].copy())
        if kind=='omitted': p['associations'].pop(0)
        if kind=='extra_property': p['associations'][0]['value_text']='999 mm'
    r=parse_pipeline(sub,settings=config(),client=oracle_client(sub,mutate=mutate))
    if kind=='extra_property':
        assert r.pipeline.assistance.status=='REJECTED' and not r.measurements
    else:
        assert r.status=='PARTIAL' and len(r.measurements)==4
        assert any(m.numeric_status=='AMBIGUOUS' and m.signed_decimal is None and m.raw_value is not None for m in r.measurements)
        resolved=resolve(ReviewSubmission(raw_text=sub.raw_text,recovery_receipt=r.pipeline.recovery_receipt,synthetic_data_confirmed=True))
        assert [m.model_dump() for m in resolved.measurements]==[m.model_dump() for m in r.measurements]


@pytest.mark.parametrize('status',[401,429,503])
def test_groq_http_failure_falls_back_without_retry_or_secret_output(status):
    sub=request();calls=[]
    r=parse_pipeline(sub,settings=config(),client=oracle_client(sub,status=status,calls=calls))
    assert len(calls)==1 and r.pipeline.assistance.status=='FAILED' and not r.measurements
    assert 'SYNTHETIC_ONLY' not in r.model_dump_json()


@pytest.mark.parametrize('failure',[httpx.ReadTimeout('PRIVATE'),httpx.ConnectError('PRIVATE')])
def test_transport_failures_are_safe(failure):
    def handler(_): raise failure
    r=parse_pipeline(request(),settings=config(),client=GroqClient(config(),transport=httpx.MockTransport(handler)))
    assert r.pipeline.assistance.status=='FAILED' and 'PRIVATE' not in r.model_dump_json()


@pytest.mark.parametrize('content',['null','[]','{}','not json','{"associations":[],"associations":[]}'])
def test_bad_provider_content_cannot_authorize_structure(content):
    response={'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':content}}]}
    c=GroqClient(config(),transport=httpx.MockTransport(lambda _:httpx.Response(200,json=response)))
    r=parse_pipeline(request(),settings=config(),client=c)
    assert r.pipeline.assistance.status=='REJECTED' and not r.pipeline.recovery_receipt


def test_receipt_tamper_expiry_and_context_binding():
    sub=request();r=parse_pipeline(sub,settings=config(),client=oracle_client(sub))
    base=dict(raw_text=sub.raw_text,synthetic_data_confirmed=True,recovery_receipt=r.pipeline.recovery_receipt)
    assert_gold(resolve(ReviewSubmission(**base)),generate(sub.synthetic_fixture).gold)
    for overrides in [{'raw_text':sub.raw_text+' '},{'source_claim':'ClinCheck'},{'context':SourceContext(scope='TOTAL')},
                      {'recovery_receipt':r.pipeline.recovery_receipt[:-1]+'x'}]:
        invalid=resolve(ReviewSubmission(**{**base,**overrides}))
        assert any(i.code=='RECOVERY_RECEIPT_INVALID' for i in invalid.issues)
        assert not invalid.measurements
    proof=prove(sub.raw_text)
    accepted,_=validate(json.dumps({'associations':[g['association'] for g in generate(sub.synthetic_fixture).gold]}),proof)
    expired=issue(sub,accepted,now=1000)
    assert resolve(ReviewSubmission(**{**base,'recovery_receipt':expired}),now=1901).status=='INVALID'


def test_server_rechecks_associations_even_with_a_valid_signature():
    sub=request();fake=[Association(tooth='s0e1',label='s1e2',value='s2e3')]
    receipt=issue(sub,fake)
    r=resolve(ReviewSubmission(raw_text=sub.raw_text,synthetic_data_confirmed=True,recovery_receipt=receipt))
    assert not r.measurements and any(i.code=='RECOVERY_RECEIPT_INVALID' for i in r.issues)


def test_downstream_vendor_semantics_remain_disabled_after_successful_recovery():
    sub=request();p=parse_pipeline(sub,settings=config(),client=oracle_client(sub))
    review_request=ReviewSubmission(raw_text=sub.raw_text,synthetic_data_confirmed=True,recovery_receipt=p.pipeline.recovery_receipt)
    review=review_table(review_request)
    assert review.coverage.declared_positions==4 and review.coverage.eligible_positions==0
    assert review.evidence_domain=='UNVERIFIED' and not review.clinical_analysis_enabled
    report=generate_report(review_request,mode='TEMPLATES')
    assert report.engine_review.coverage.declared_positions==4 and report.generation.attempts==0
    assert APPROVED_RELEASE_DIGESTS==frozenset()


def test_full_isolated_synthetic_flow_through_unchanged_semantic_registry_and_report():
    sub=request(context=SourceContext(source_version='TEST_ONLY-1'))
    p=parse_pipeline(sub,settings=config(),client=oracle_client(sub))
    review_request=ReviewSubmission(raw_text=sub.raw_text,context=sub.context,synthetic_data_confirmed=True,recovery_receipt=p.pipeline.recovery_receipt)
    lexical=resolve(review_request)
    # Independent gold is asserted BEFORE building the exact TEST_ONLY bookkeeping snapshot.
    assert_gold(lexical,generate(sub.synthetic_fixture).gold)
    assertions=[]
    for m in lexical.measurements:
        if m.signed_decimal is None: continue
        components=toy_complete_components(unit=m.unit,axis='TEST_AXIS_'+m.id,tooth_identifier='TEST_TOOTH_'+m.tooth_ref)
        assertions.append(ExpectedMeasurement(measurement_id=m.id,components=tuple(ExpectedComponent(name=k,value=v,evidence_locator='SYNTHETIC_CONSTRUCTION:'+k) for k,v in components.items())))
    expected=FixtureExpectedOutput(kind='SYNTHETIC',lexical=lexical,measurements=tuple(assertions))
    record=FixtureRecord(fixture_id='PHASE4-SYNTHETIC',kind='SYNTHETIC',application='TEST_ONLY',source_version='TEST_ONLY-1',status='TEST_ONLY',
                         raw=Artifact(path='not-persisted',sha256=lexical.raw_sha256),expected=Artifact(path='not-persisted',sha256=digest_json(expected.model_dump(mode='json'))))
    checked=CheckedFixture(record.model_dump_json(),expected.model_dump_json(),lexical.model_dump_json(),digest_json({'record':record.model_dump(mode='json'),'expected':expected.model_dump(mode='json')}))
    assessment=assess_semantics(lexical,checked,allow_test_only=True)
    assert assessment.status=='TEST_ONLY' and not any(m.canonical_measurement_ready for m in assessment.measurements)
    review=review_table(review_request,checked=checked,test_only=True)
    assert review.coverage.eligible_positions==3 and review.evidence_domain=='TEST_ONLY'
    def wording(req):
        items=json.loads(json.loads(req.content)['messages'][1]['content'])['authorized_findings']
        return httpx.Response(200,json={'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps({'comments':[{'finding_ids':i['finding_ids'],'text':i['approved_wordings'][0]} for i in items]})}}]})
    settings=ReportSettings(api_key='SYNTHETIC_COMMENT_ONLY',synthetic_transmission_enabled=True)
    report=generate_report(review_request,checked=checked,test_only=True,settings=settings,client=GroqClient(settings,transport=httpx.MockTransport(wording)))
    assert report.generation.used_mode=='GROQ_AI' and report.engine_review.coverage.eligible_positions==3
    assert not report.clinical_analysis_enabled and 'DRAFT' in report.export_text
    denied=generate_report(review_request,checked=checked,mode='TEMPLATES')
    assert denied.engine_review.coverage.eligible_positions==0


def test_blank_values_and_transposed_records_have_explicit_local_evidence():
    for raw in ['Tooth: 13\nRotation (deg):\nExtrusion (mm):0', 'Movement: Rotation (deg)\n13:−1.2500 M;14:0 M']:
        proofs=prove(raw)
        assert len(proofs.associations)==2
        triples=[Association(tooth=t,label=l,value=v) for t,l,v in proofs.associations]
        sub=PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True)
        r=assemble(sub,deterministic(sub),proofs,triples)
        assert len(r.measurements)==2
        if raw.startswith('Tooth'): assert r.measurements[0].numeric_status=='MISSING'


@pytest.mark.parametrize('separator',['|',';','\t'])
@pytest.mark.parametrize('padding',['',' ','   ','\u00a0'])
def test_metamorphic_explicit_separators_and_padding_preserve_associations(separator,padding):
    raw=f'Tooth\tRotation (deg)\tExtrusion (mm)\n13{separator}{padding}−1.2500 M{padding}{separator}{padding}0.00 E{padding}'
    sub=PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True)
    p=prove(raw)
    accepted=[Association(tooth=t,label=l,value=v) for t,l,v in p.associations]
    r=assemble(sub,deterministic(sub),p,accepted)
    assert [m.signed_decimal for m in r.measurements]==[Decimal('-1.2500'),Decimal('0.00')]
    for m in r.measurements: assert raw[m.span.start:m.span.end]==m.raw_value


def test_unrecognized_interruption_ends_record_scope():
    raw='Tooth: 13\nRotation (deg):\ninvalid text\nExtrusion (mm):4'
    p=prove(raw)
    assert len(p.associations)==1  # The explicitly blank Rotation position only.
    assert all(p.cells[a[1]].raw=='Rotation (deg)' for a in p.associations)


def test_duplicate_fields_remain_ambiguous_and_unassigned_fragments_prevent_zero_inventory():
    raw='Tooth: 13;Rotation (deg):0 M|Rotation (deg):0 M\n'
    sub=PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True)
    p=prove(raw);accepted=[Association(tooth=t,label=l,value=v) for t,l,v in p.associations]
    r=assemble(sub,deterministic(sub),p,accepted)
    assert len(r.measurements)==2 and all(m.field_status=='AMBIGUOUS' for m in r.measurements)


def test_receipt_conflict_is_explicit_http_409_without_echoing_data():
    client=TestClient(app)
    for path in ['/api/v1/tmt/observations','/api/v1/reports/draft']:
        r=client.post(path,json={'raw_text':'PRIVATE_MARKER','synthetic_data_confirmed':True,'recovery_receipt':'fake.signature'})
        assert r.status_code==409 and 'PRIVATE_MARKER' not in r.text
        assert r.headers['cache-control']=='no-store'


def test_checked_in_dataset_is_current_and_expected_labels_are_not_parser_output():
    records=json.loads((Path(__file__).resolve().parents[2]/'examples/phase4-synthetic-dataset.json').read_text(encoding='utf-8'))['fixtures']
    assert len(records)==78
    for record in records:
        sample=generate(SyntheticFixture(**record['identity']))
        assert record['raw_text']==sample.raw_text
        assert record['gold']==json.loads(json.dumps(sample.gold))


def test_recovery_engineering_bounds_abstain_without_prefix_truncation():
    raw='Tooth\t'+ '\t'.join(['Rotation (deg)']*20)+'\n'+ '\n'.join('13|'+ '|'.join(['0']*20) for _ in range(30))
    p=prove(raw)
    assert not p.associations
    assert parse_pipeline(PipelineSubmission(raw_text=raw,synthetic_data_confirmed=True),settings=config()).pipeline.assistance.attempts==0


def test_generator_endpoint_has_no_arbitrary_text_enrollment_and_api_replays_receipt(monkeypatch):
    client=TestClient(app)
    assert client.post('/api/v1/development/synthetic',json={'recipe':'wrapped','seed':77,'raw_text':'PATIENT'}).status_code==422
    sample=client.post('/api/v1/development/synthetic',json={'recipe':'wrapped','seed':77}).json()
    sub=PipelineSubmission(raw_text=sample['raw_text'],synthetic_fixture=SyntheticFixture(**sample['synthetic_fixture']),synthetic_data_confirmed=True)
    import app.api.automatic_parse as route
    monkeypatch.setattr(route,'parse_pipeline',lambda s:parse_pipeline(s,settings=config(),client=oracle_client(s)))
    parsed=client.post('/api/v1/tmt/parse',json=sub.model_dump(mode='json')).json()
    assert parsed['pipeline']['assistance']['status']=='ACCEPTED'
    response=client.post('/api/v1/tmt/observations',json={'raw_text':sample['raw_text'],'synthetic_data_confirmed':True,'recovery_receipt':parsed['pipeline']['recovery_receipt']})
    assert response.status_code==200 and response.json()['coverage']['declared_positions']==4
    assert response.json()['evidence_domain']=='UNVERIFIED'
    assert response.headers['cache-control']=='no-store'
