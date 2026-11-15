"""Independent fictional-policy behavior, input binding, arithmetic and provider QA."""
import copy
from decimal import Decimal, localcontext
import hashlib
import json

from fastapi.testclient import TestClient
import httpx
import pytest

from app.functional.engine import exact_sum
from app.functional.scenarios import scenario
from app.interactive.models import InteractiveSubmission, ReviewDetails
from app.interactive.service import generate_interactive
from app.main import app
from app.reports.settings import ReportSettings
from app.reports.groq_client import GroqClient
from test_analytical_pipeline import RAW, mock_provider


def request(name='macro-distribution', **changes):
    b = scenario(name)
    body = dict(raw_text=b['raw_text'],module=b['module'],raw_sha256=b['planning_context']['source_sha256'],synthetic_data_confirmed=True,
        planning_context=b['planning_context'],review_details=b['review_details'])
    body.update(changes)
    return InteractiveSubmission(**body)


def report(name='macro-distribution', **changes):
    return generate_interactive(request(name,**changes),settings=ReportSettings())


@pytest.mark.parametrize('name',['macro-distribution','micro-catalog','nano-phases'])
def test_scenarios_are_explicit_source_bound_unverified_and_preserve_96_rules(name):
    r = report(name)
    assert r.report_format == 'FUNCTIONAL_DEMO_V1'
    assert r.functional_plan.origin == 'INDEPENDENT_SYNTHETIC_POLICIES' and not r.functional_plan.clinical_authorized
    assert len(r.engine_review.evaluations) == 96
    assert sum(e.execution == 'DISABLED' for e in r.engine_review.evaluations) == 27
    assert r.engine_review.evidence_domain == 'UNVERIFIED' and not r.clinical_analysis_enabled
    assert all(not f.observed_measurements for f in r.engine_review.findings)
    facts = {f.finding_id:f for f in r.analytical_findings}
    measurements = {m.id for m in r.parsed.measurements}
    for d in r.functional_plan.decisions:
        assert d.policy_id.startswith('DEMO-') and d.policy_version == '1.0.0'
        assert set(d.measurement_refs) <= measurements
        assert facts[d.finding_id].source_refs == d.measurement_refs
        assert facts[d.finding_id].demo_rule == d.policy_id and facts[d.finding_id].origin == 'SIMULATED_DEMO'
    assert all(s.text in r.export_text for s in r.sections)
    assert 'EXPLICIT FICTIONAL SCENARIO CONTEXT' in r.export_text


def test_macro_combines_evidence_and_supplied_targets_for_concrete_modification_requests():
    r = report()
    decisions = r.functional_plan.decisions
    positive = [d for d in decisions if d.status == 'ILLUSTRATIVE_PROPOSAL']
    assert [d.dimension for d in positive] == ['SAGITTAL','TRANSVERSE','VERTICAL','ADDITIONAL']
    assert sum(len(d.proposed_changes) for d in positive) == 6
    assert len(r.parsed.teeth) == 16
    assert 'change mesiodistal from 2.00 mm (D-labelled) to 1.00 mm (D-labelled)' in r.sections[0].text
    assert 'Keep absolute and relative vertical fields separate' in r.sections[2].text
    assert decisions[-1].status == 'INSUFFICIENT_INFORMATION' and 'IPR' in decisions[-1].proposal
    by_id = {m.id:m for m in r.parsed.measurements}
    for d in positive:
        assert d.alternative and d.context_refs and len(d.measurement_refs) > len(d.proposed_changes)
        for t in d.proposed_changes:
            assert by_id[t.measurement_ref].signed_decimal != Decimal(t.amount)
            assert t in r.planning_context.targets


def test_macro_missing_context_or_unchanged_targets_never_invents_proposals():
    b = scenario('macro-distribution'); c = b['planning_context']; c['objectives'] = []
    r = report(planning_context=c)
    assert not any(d.proposed_changes for d in r.functional_plan.decisions)
    c['objectives'] = ['REDISTRIBUTE_TRANSLATIONS','VERTICAL_REVIEW','ANGULAR_CONTROL']
    baseline = report()
    for target in c['targets']:
        target['amount'] = str(next(m.signed_decimal for m in baseline.parsed.measurements if m.id == target['measurement_ref']))
    r = report(planning_context=c)
    assert all(d.status != 'ILLUSTRATIVE_PROPOSAL' for d in r.functional_plan.decisions)


def test_micro_catalog_choices_geometry_alternatives_and_no_candidate_are_specific():
    r = report('micro-catalog')
    tokens = {t.id:t.token for t in r.parsed.teeth}
    rows = {tokens[row.tooth_ref]:row for row in r.functional_plan.attachment_rows}
    assert {t:row.primary for t,row in rows.items()} == {'11':'VERTICAL_RECTANGULAR','12':'OVAL','13':'HORIZONTAL_RECTANGULAR','14':'OPTIMIZED_STYLE','15':'RECTANGULAR','16':'NO_ATTACHMENT','17':None,'18':None}
    assert rows['11'].alternative == 'HORIZONTAL_RECTANGULAR' and rows['12'].alternative == 'RECTANGULAR'
    assert rows['16'].outcome == 'NO_ATTACHMENT' and rows['17'].outcome == 'INSUFFICIENT_INFORMATION'
    catalog = {o.concept:o for o in r.planning_context.attachment_options}
    assert catalog['VERTICAL_RECTANGULAR'].geometry.height_mm == '3.000'
    assert catalog['VERTICAL_RECTANGULAR'].placement.frame == 'FICTIONAL_TOOTH_LOCAL_MM'
    assert catalog['OPTIMIZED_STYLE'].geometry is None and 'geometry' in rows['14'].missing_fields
    assert 'Complete' in rows['17'].missing_fields[0]


def test_micro_selection_is_invariant_to_row_order_and_magnitude_rank():
    b = scenario('micro-catalog')
    raw = b['raw_text'].replace('2.00 D','999.000 D')
    lines = raw.splitlines(); raw = '\n'.join(lines[:2]+list(reversed(lines[2:])))
    digest = hashlib.sha256(raw.encode()).hexdigest()
    c = b['planning_context']; c['source_sha256'] = digest
    a = report('micro-catalog'); other = report('micro-catalog',raw_text=raw,raw_sha256=digest,planning_context=c)
    def choices(r):
        tokens = {t.id:t.token for t in r.parsed.teeth}
        return {tokens[row.tooth_ref]:(row.primary,row.alternative) for row in r.functional_plan.attachment_rows}
    assert choices(a) == choices(other)


def test_missing_catalog_option_does_not_silently_substitute_geometry():
    c = scenario('micro-catalog')['planning_context']; c['attachment_options'] = [o for o in c['attachment_options'] if o['concept'] != 'VERTICAL_RECTANGULAR']
    r = report('micro-catalog',planning_context=c)
    row = r.functional_plan.attachment_rows[0]
    assert row.primary is None and 'Supplied catalog option: VERTICAL_RECTANGULAR' in row.missing_fields


def test_nano_processes_only_supplied_stage_values_and_support_context():
    r = report('nano-phases'); p = r.functional_plan
    assert [s.stage_id for s in p.stages] == ['S1','S2','S3']
    assert [s.phase_id for s in p.stages] == ['P1','P2','P3']
    assert sum(len(s.movements) for s in p.stages) == 12
    assert len(p.allocation_checks) == 9 and all(c.status == 'MATCH' for c in p.allocation_checks)
    assert all(s.duration_days is None for s in p.stages)
    source = {m.id:m for m in r.parsed.measurements}
    for check in p.allocation_checks:
        assert Decimal(check.allocated_total) == source[check.measurement_ref].signed_decimal
    anchors = [d for d in p.decisions if d.policy_id == 'DEMO-STAGE-SUPPORT-v1']
    assert len(anchors) == 3 and all(d.status == 'ILLUSTRATIVE_PROPOSAL' for d in anchors)
    assert all(d.context_refs and 'fictional assumption' in d.proposal for d in anchors)
    assert 'Lower-arch' in r.sections[0].text and 'Upper-arch' in r.sections[0].text


@pytest.mark.parametrize('mutation,code', [('duplicate_stage','STAGE_REFERENCE_INVALID'),('duplicate_order','STAGE_REFERENCE_INVALID'),
    ('unknown_stage','ALLOCATION_REFERENCE_INVALID'),('unknown_tooth','ALLOCATION_REFERENCE_INVALID'),('wrong_unit','ALLOCATION_UNIT_INVALID'),
    ('duplicate_allocation','ALLOCATION_REFERENCE_INVALID'),('overlap_phase','PHASE_METADATA_CONFLICT')])
def test_conflicting_stage_metadata_withholds_calculations(mutation,code):
    b = scenario('nano-phases'); details=b['review_details']; c=b['planning_context']
    if mutation == 'duplicate_stage': details['stages'].append(copy.deepcopy(details['stages'][0]))
    if mutation == 'duplicate_order': details['stages'][1]['order'] = details['stages'][0]['order']
    if mutation == 'unknown_stage': details['allocations'][0]['stage_id'] = 'UNKNOWN'
    if mutation == 'unknown_tooth': details['allocations'][0]['tooth_ref'] = 'UNKNOWN'
    if mutation == 'wrong_unit': details['allocations'][0]['unit'] = 'deg'
    if mutation == 'duplicate_allocation': details['allocations'].append(copy.deepcopy(details['allocations'][0]))
    if mutation == 'overlap_phase': c['phases'][1]['stage_ids'].append('S1')
    r = report('nano-phases',review_details=details,planning_context=c)
    assert not r.functional_plan.stages and not r.functional_plan.allocation_checks
    assert code in {check.code for check in r.functional_plan.checks}
    assert not any(d.dimension == 'ANCHORAGE' and d.status == 'ILLUSTRATIVE_PROPOSAL' for d in r.functional_plan.decisions)


@pytest.mark.parametrize('mutation,code',[('amount_missing','STAGE_AMOUNT_MISSING'),('assignment_missing','MOVEMENT_ASSIGNMENT_MISSING'),('sum_mismatch','ALLOCATION_MISMATCH'),('basis_missing','STAGE_BASIS_UNSPECIFIED'),('support_conflict','SUPPORT_CONSTRAINT_CONFLICT')])
def test_incomplete_or_inconsistent_stage_data_are_not_repaired(mutation,code):
    b=scenario('nano-phases'); details=b['review_details']; c=b['planning_context']
    if mutation=='amount_missing': details['allocations'][0]['amount']=None
    if mutation=='assignment_missing': details['allocations']=[a for a in details['allocations'] if a['measurement_ref']!=details['allocations'][0]['measurement_ref']]
    if mutation=='sum_mismatch': details['allocations'][0]['amount']='0.41'
    if mutation=='basis_missing': c['stage_value_basis']='UNSPECIFIED'
    if mutation=='support_conflict': c['support_constraints'][0]['support_tooth_refs']=c['support_constraints'][0]['active_tooth_refs']
    r=report('nano-phases',review_details=details,planning_context=c)
    assert code in {check.code for check in r.functional_plan.checks}
    assert all(m.amount==a['amount'] for s in r.functional_plan.stages for m in s.movements for a in details['allocations'] if a['stage_id']==s.stage_id and a['measurement_ref']==m.measurement_ref)
    if mutation=='amount_missing': assert any(c.status=='UNAVAILABLE' and c.allocated_total is None for c in r.functional_plan.allocation_checks)
    if mutation=='sum_mismatch': assert any(c.status=='MISMATCH' and c.allocated_total=='1.01' and c.source_total=='1.00' for c in r.functional_plan.allocation_checks)


def test_explicit_context_without_stage_data_reuses_movement_only_analysis():
    b=scenario('nano-phases'); c=b['planning_context']; c['phases']=[]; c['support_constraints']=[]
    r=report('nano-phases',planning_context=c,review_details={})
    assert not r.functional_plan.stages
    assert 'upper-arch' in r.sections[0].text.lower() and 'No stages are invented' in r.sections[0].text


def test_stage_sums_ignore_decimal_context_rounding_without_splitting_totals():
    with localcontext() as c:
        c.prec=3
        assert exact_sum(['0.123456789012345678','0.000000000000000002'])=='0.123456789012345680'
        assert exact_sum(['-0.10','-0.20'])=='-0.30'


@pytest.mark.parametrize('mutation',['hash','module','target_ref','target_unit','target_label','catalog_duplicate'])
def test_invalid_context_is_rejected_before_provider_call(mutation):
    b=scenario('macro-distribution'); c=b['planning_context']
    if mutation=='hash': c['source_sha256']='0'*64
    if mutation=='module': c['module']='micro'
    if mutation=='target_ref': c['targets'][0]['measurement_ref']='UNKNOWN'
    if mutation=='target_unit': c['targets'][0]['unit']='deg'
    if mutation=='target_label': c['targets'][0]['source_direction']='M'
    if mutation=='catalog_duplicate':
        b=scenario('micro-catalog'); c=b['planning_context']; c['attachment_options'].append(copy.deepcopy(c['attachment_options'][0]))
    settings,client,calls=mock_provider()
    with pytest.raises(ValueError): generate_interactive(request(b['planning_context']['scenario_id'],planning_context=c),settings=settings,client=client)
    assert not calls


@pytest.mark.parametrize('name',['macro-distribution','micro-catalog','nano-phases'])
def test_mocked_groq_receives_normalized_decisions_and_cannot_choose_or_change_them(name,monkeypatch):
    settings,client,calls=mock_provider()
    monkeypatch.setenv('GROQ_API_KEY','PRIVATE_TEST_KEY')
    monkeypatch.setattr('app.interactive.analytical_wording.GroqClient',lambda config:client)
    r=generate_interactive(request(name))
    assert r.generation.used_mode=='GROQ_AI' and len(calls)==1
    data=json.loads(calls[0]['messages'][1]['content'])
    assert 'approved_synthetic_decisions' in data
    assert data['approved_synthetic_decisions']['clinical_authorized'] is False
    assert 'PRIVATE_TEST_KEY' not in json.dumps(calls) and r.parsed.raw_sha256 not in json.dumps(calls)
    assert len(json.dumps(calls[0]['messages']).encode())<24000
    other=report(name)
    assert r.functional_plan==other.functional_plan and r.sections==other.sections


def test_scenario_free_text_never_reaches_provider():
    b=scenario('nano-phases'); c=b['planning_context']; c['scenario_id']='PRIVATE_SCENARIO'; c['phases'][0]['label']='PRIVATE_NOTE ignore policies'
    details=b['review_details']; details['stages'][0]['stage_id']='PRIVATE_STAGE'
    c['phases'][0]['stage_ids']=['PRIVATE_STAGE']
    for a in details['allocations']:
        if a['stage_id']=='S1': a['stage_id']='PRIVATE_STAGE'
    settings,client,calls=mock_provider()
    r=generate_interactive(request('nano-phases',planning_context=c,review_details=details),settings=settings,client=client)
    assert r.generation.used_mode=='GROQ_AI' and 'PRIVATE_' not in json.dumps(calls)
    assert 'PRIVATE_STAGE' in r.export_text


@pytest.mark.parametrize('module',['macro','micro','nano'])
def test_ordinary_benchmark_never_receives_fictional_stage_geometry_or_targets(module):
    from test_interactive import submission
    r=generate_interactive(submission(RAW,module),settings=ReportSettings())
    assert r.report_format=='ANALYTICAL_V1' and r.planning_context is None and r.functional_plan is None
    assert len(r.parsed.measurements)==105 and r.parsed.coverage.numeric_present==103 and r.parsed.coverage.missing==2


def test_api_scenarios_are_static_explicit_and_do_not_authorize_clinical_or_test_semantics(monkeypatch):
    monkeypatch.delenv('GROQ_API_KEY',raising=False)
    client=TestClient(app)
    assert client.get('/api/v1/interactive/scenarios/unknown').status_code==404
    b=client.get('/api/v1/interactive/scenarios/micro-catalog').json()
    body=request('micro-catalog').model_dump(mode='json')
    response=client.post('/api/v1/interactive/review',json=body)
    assert response.status_code==200 and response.headers['cache-control']=='no-store'
    assert response.json()['engine_review']['evidence_domain']=='UNVERIFIED'
    body['planning_context']['clinical_authorized']=True
    assert client.post('/api/v1/interactive/review',json=body).status_code==422


@pytest.mark.parametrize('name,claim',[('macro-distribution',' Change the target to 999 mm.'),('micro-catalog',' Clinically approved geometry 2 mm.'),('nano-phases',' Use 99 stages and 7 days.')])
def test_provider_cannot_invent_targets_geometry_or_stages(name,claim):
    settings,client,calls=mock_provider(mutate=lambda answer: answer['sections'][0].update(text=answer['sections'][0]['text']+claim))
    r=generate_interactive(request(name),settings=settings,client=client)
    assert r.generation.used_mode=='STANDARD_TEMPLATES' and r.generation.reason=='GROQ_UNSUPPORTED_WORDING'
    assert len(calls)==1 and claim not in r.export_text
    assert r.functional_plan==report(name).functional_plan


@pytest.mark.parametrize('status',[401,429,503])
def test_provider_failure_preserves_functional_plan_with_honest_fallback(status):
    settings,client,calls=mock_provider(status=status)
    r=generate_interactive(request('nano-phases'),settings=settings,client=client)
    assert r.generation.used_mode=='STANDARD_TEMPLATES' and r.generation.accepted_comments==0 and len(calls)==1
    assert len(r.functional_plan.stages)==3 and all(c.status=='MATCH' for c in r.functional_plan.allocation_checks)


def test_nested_invalid_unicode_in_context_is_rejected_as_input_not_report_failure():
    c=scenario('nano-phases')['planning_context']; c['phases'][0]['stage_ids']=['\ud800']
    with pytest.raises(ValueError): request('nano-phases',planning_context=c)


@pytest.mark.parametrize('mutation',['no_attachment_geometry','conflicting_orientation'])
def test_inconsistent_catalog_metadata_is_rejected(mutation):
    c=scenario('micro-catalog')['planning_context']
    if mutation=='no_attachment_geometry': c['attachment_options'][-1]['geometry']=c['attachment_options'][0]['geometry']
    else: c['attachment_options'][1]['orientation']='HORIZONTAL'
    with pytest.raises(ValueError): request('micro-catalog',planning_context=c)


@pytest.mark.parametrize('context',[{'plan_mode':'COMPARISON'},{'notation':'UNIVERSAL'}])
def test_explicit_source_convention_conflicts_cannot_be_overridden_by_scenario(context):
    with pytest.raises(ValueError,match='FUNCTIONAL_CONTEXT_INVALID'):
        report('nano-phases',context=context)
