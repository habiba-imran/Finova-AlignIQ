"""Client-style arbitrary tables, reusable policy behavior and counterfactuals."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.interactive.models import InteractiveSubmission
from app.interactive.service import generate_interactive
from app.main import app
from app.parser.receipts import resolve
from app.reports.settings import ReportSettings
from test_analytical_pipeline import mock_provider

FIXTURES=Path(__file__).parent/'fixtures'
INPUTS={name:(FIXTURES/path).read_text(encoding='utf-8') for name,path in {
    'A':'analysis_15_tooth.md','B':'generalized_lower.md','C':'generalized_new.tsv','D':'generalized_sparse.tsv'}.items()}


def request(case='A',module='macro',raw=None,options=None,**extra):
    raw=INPUTS[case] if raw is None else raw
    return InteractiveSubmission(raw_text=raw,raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),module=module,
        synthetic_data_confirmed=True,planning_options={} if options is None else options,**extra)


def report(case='A',module='macro',**changes):
    return generate_interactive(request(case,module,**changes),settings=ReportSettings())


@pytest.mark.parametrize('case',['A','B','C','D'])
@pytest.mark.parametrize('module',['macro','micro','nano'])
def test_arbitrary_supported_inputs_need_no_scenario_id(case,module):
    submission=request(case,module); original=resolve(submission); r=report(case,module)
    assert r.parsed==original and r.planning_context.scenario_id is None
    assert r.planning_context.origin=='INPUT_DRIVEN_POLICY_REVIEW'
    assert r.functional_plan.source_sha256==original.raw_sha256 and not r.functional_plan.clinical_authorized
    assert r.sections and all(s.text and s.text in r.export_text for s in r.sections)
    assert len(r.engine_review.evaluations)==96
    assert sum(e.execution=='DISABLED' for e in r.engine_review.evaluations)==27
    assert r.engine_review.evidence_domain=='UNVERIFIED' and not r.clinical_analysis_enabled
    cells={m.id:m for m in original.measurements}
    for f,d in zip(r.analytical_findings,r.functional_plan.decisions):
        assert f.finding_id==d.finding_id and f.demo_rule==d.policy_id
        assert f.source_refs==d.measurement_refs and set(f.selected_refs)<=set(cells)
    assert 'INPUT-DRIVEN POLICY CONTEXT' in r.export_text
    assert all(not d.proposed_changes for d in r.functional_plan.decisions)
    assert not r.functional_plan.stages


@pytest.mark.parametrize('case,teeth,positions,missing',[('A',15,105,2),('B',16,112,3),('C',8,56,0),('D',3,6,3)])
def test_client_benchmark_coverage_is_exact(case,teeth,positions,missing):
    r=report(case)
    assert len(r.parsed.teeth)==teeth and len(r.parsed.measurements)==positions
    assert r.parsed.coverage.missing==missing
    for m in r.parsed.measurements:
        if m.span: assert r.parsed.raw_text[m.span.start:m.span.end]==m.raw_value


def rows(r):
    names={t.id:t.token for t in r.parsed.teeth}
    return {names[row.tooth_ref]:row for row in r.functional_plan.attachment_rows}


def test_lower_micro_distinguishes_profiles_ties_zero_unsupported_and_missing():
    r=report('B','micro'); selected=rows(r)
    expected={'37':'OVAL','36':'OPTIMIZED_STYLE','35':'RECTANGULAR','34':'HORIZONTAL_RECTANGULAR',
        '33':'OVAL','32':'HORIZONTAL_RECTANGULAR','31':'VERTICAL_RECTANGULAR','38':'NO_ATTACHMENT'}
    assert {t:selected[t].primary for t in expected}==expected
    assert selected['44'].outcome=='NO_CANDIDATE'
    assert all(selected[t].outcome=='INSUFFICIENT_INFORMATION' for t in ('45','46','47'))
    d=next(d for d in r.functional_plan.decisions if d.decision_id==selected['46'].decision_id)
    assert 'Explicit-zero angular profile' in d.rationale and d.missing_fields==['Unavailable fields: vertical']
    assert len({row.primary for row in selected.values() if row.primary})==6
    assert all(o.geometry is None and o.placement is None for o in r.planning_context.attachment_options)


def test_upper_micro_avoids_one_combined_angular_choice_for_every_tooth():
    r=report('A','micro')
    choices={row.primary for row in r.functional_plan.attachment_rows if row.primary}
    assert {'OVAL','HORIZONTAL_RECTANGULAR','OPTIMIZED_STYLE'}<=choices
    assert rows(r)['18'].primary is None


def test_micro_counterfactual_changes_only_the_affected_tooth():
    baseline=report('B','micro')
    changed=report('B','micro',raw=INPUTS['B'].replace('| 34 | 1.20 D | 3.40 M |','| 34 | 5.40 D | 3.40 M |'))
    a,b=rows(baseline),rows(changed)
    assert a['34'].primary=='HORIZONTAL_RECTANGULAR' and b['34'].primary=='OVAL'
    assert {t:(v.primary,v.alternative,v.outcome) for t,v in a.items() if t!='34'}=={t:(v.primary,v.alternative,v.outcome) for t,v in b.items() if t!='34'}


def test_macro_counterfactual_changes_only_relevant_dimension():
    before=report(); after=report(raw=INPUTS['A'].replace('0.40 L | 2.30 D','0.10 L | 2.30 D'))
    a,b=({s.section_id:s.text for s in r.sections} for r in (before,after))
    assert a['TRANSVERSE']!=b['TRANSVERSE']
    assert all(a[k]==b[k] for k in ('SAGITTAL','VERTICAL','ADDITIONAL'))
    assert 'Technician review:' in a['SAGITTAL'] and '3.30 mm' in a['SAGITTAL']


def test_nano_outline_is_input_specific_and_never_contains_stage_allocations():
    r=report('C','nano')
    assert len(r.functional_plan.review_outline)==3
    assert all(o.origin=='ILLUSTRATIVE_REVIEW_OUTLINE' and not o.stage_allocations_generated for o in r.functional_plan.review_outline)
    text=' '.join(s.text for s in r.sections)
    assert 'Upper-arch' in text and 'Lower-arch' in text and 'Sequencing review priority:' in text
    assert not r.functional_plan.stages and not r.review_details.allocations


@pytest.mark.parametrize('module',['macro','nano'])
def test_upper_half_boundary_keeps_all_seven_buccolingual_tokens_exactly_once(module):
    r=report('A',module)
    if module=='macro': finding=next(f for f in r.analytical_findings if f.section_id=='TRANSVERSE')
    else: finding=next(f for f in r.analytical_findings if f.text.startswith('Translation coupling review'))
    cells={m.id:m for m in r.parsed.measurements};teeth={t.id:t.token for t in r.parsed.teeth}
    selected=[teeth[cells[ref].tooth_ref] for ref in finding.selected_refs if cells[ref].recognized_label=='buccolingual']
    assert set(selected)=={'11','12','13','21','22','24','26'} and len(selected)==len(set(selected))==7


def target_options(case='C',module='macro'):
    submission=request(case,module); parsed=resolve(submission)
    m=next(m for m in parsed.measurements if m.recognized_label=='rotation' and m.signed_decimal and m.signed_decimal<0)
    return parsed,m,dict(source_sha256=parsed.raw_sha256,objectives=['ANGULAR_CONTROL'],source_convention='SOURCE_LABELS_AS_RECORDED',
        illustration='HALF_MAGNITUDE',illustration_measurement_ref=m.id)


def test_fictional_calculation_never_rounds_an_overlong_decimal_to_fit_the_contract():
    raw='Tooth\tRotation (deg)\n11\t0.0000000000000000000000007 D'
    original=resolve(request(raw=raw))
    options=dict(source_sha256=original.raw_sha256,objectives=['ANGULAR_CONTROL'],source_convention='SOURCE_LABELS_AS_RECORDED',
        illustration='HALF_MAGNITUDE',illustration_measurement_ref=original.measurements[0].id)
    r=report(raw=raw,options=options)
    assert r.parsed==original and not any(d.proposed_changes for d in r.functional_plan.decisions)
    assert 'No value is rounded or substituted' in r.sections[-1].text


def test_a_supplied_target_never_turns_a_missing_source_value_into_a_quantity():
    original=resolve(request('B'))
    tooth=next(t for t in original.teeth if t.token=='46')
    m=next(m for m in original.measurements if m.tooth_ref==tooth.id and m.recognized_label=='vertical')
    options=dict(source_sha256=original.raw_sha256,objectives=['VERTICAL_REVIEW'],source_convention='SOURCE_LABELS_AS_RECORDED',
        targets=[dict(measurement_ref=m.id,amount='0.10',unit='mm',source_direction=None)])
    settings,client,calls=mock_provider()
    with pytest.raises(ValueError,match='FUNCTIONAL_CONTEXT_INVALID'):
        generate_interactive(request('B',options=options),settings=settings,client=client)
    assert not calls and m.numeric_status=='MISSING' and m.signed_decimal is None


@pytest.mark.parametrize('remove',['objective','convention','mode','method'])
def test_fictional_numeric_example_requires_context_and_disappears_when_removed(remove):
    parsed,m,options=target_options()
    positive=report('C',options=options)
    changes=[t for d in positive.functional_plan.decisions for t in d.proposed_changes]
    assert len(changes)==1 and changes[0].amount=='-2.0625' and changes[0].source_direction=='M'
    if remove=='objective': options['objectives']=[]
    if remove=='convention': options['source_convention']='UNSPECIFIED'
    if remove=='mode': options['policy_mode']='EVIDENCE_REVIEW'
    if remove=='method': options['illustration']='NONE'
    after=report('C',options=options)
    assert not any(d.proposed_changes for d in after.functional_plan.decisions)


def test_stale_context_and_attempted_client_authority_are_rejected_before_provider():
    parsed,m,options=target_options(); settings,client,calls=mock_provider()
    with pytest.raises(ValueError,match='SOURCE_MISMATCH'):
        generate_interactive(request('C',raw=INPUTS['C']+'\n',options=options),settings=settings,client=client)
    assert not calls
    with pytest.raises(ValueError): request(options={'clinical_authorized':True})
    derived=report().planning_context
    with pytest.raises(ValueError,match='FUNCTIONAL_CONTEXT_INVALID'):
        generate_interactive(request(options=None).model_copy(update={'planning_options':None,'planning_context':derived}),settings=settings,client=client)


def test_custom_catalog_dimensions_are_supplied_not_calculated():
    baseline=report('B','micro')
    options=dict(source_sha256=baseline.parsed.raw_sha256,attachment_options=[dict(concept='OVAL',geometry=dict(width_mm='1.234',height_mm='2.345',depth_mm='0.456'))])
    r=report('B','micro',options=options)
    assert '1.234 × 2.345 × 0.456 mm' in r.sections[0].text
    oval=next(o for o in r.planning_context.attachment_options if o.concept=='OVAL')
    assert oval.geometry.width_mm=='1.234' and oval.placement is None
    options['catalog_policy']='SUPPLIED_OPTIONS_ONLY'
    limited=rows(report('B','micro',options=options))
    assert limited['37'].primary=='OVAL' and limited['34'].primary is None


@pytest.mark.parametrize('case',['A','B','C','D'])
@pytest.mark.parametrize('module',['macro','micro','nano'])
def test_new_tables_automatically_use_one_bounded_mock_wording_request(case,module):
    settings,client,calls=mock_provider()
    r=generate_interactive(request(case,module),settings=settings,client=client)
    assert len(calls)==r.generation.attempts==1 and r.generation.used_mode=='GROQ_AI'
    payload=json.dumps(calls)
    assert 'PRIVATE_TEST_KEY' not in payload and r.parsed.raw_sha256 not in payload and 'raw_text' not in payload
    assert len(json.dumps(calls[0]['messages']).encode())<24000
    assert r.functional_plan==report(case,module).functional_plan


def test_current_api_accepts_generalized_options_without_a_scenario(monkeypatch):
    monkeypatch.delenv('GROQ_API_KEY',raising=False)
    response=TestClient(app).post('/api/v1/interactive/review',json=request('B','micro').model_dump(mode='json'))
    assert response.status_code==200
    body=response.json()
    assert body['planning_context']['scenario_id'] is None and body['planning_context']['origin']=='INPUT_DRIVEN_POLICY_REVIEW'


def test_full_two_arch_table_uses_bounded_summary_without_skipping_provider(caplog):
    header='Tooth\tRotation (deg)\tAngulation (deg)\tInclination (deg)\tVertical (mm)\tRelative Ext / Int (mm)\tTranslation B / L (mm)\tTranslation M / D (mm)'
    raw='\n'.join([header]+[f'{q}{n}\t{n}.125 D\t0.625 M\t0.250 B\t0.375 I\t0.125 I\t0.500 L\t0.750 D' for q in (1,2,3,4) for n in range(1,9)])
    settings,client,calls=mock_provider()
    r=generate_interactive(request(raw=raw,module='micro'),settings=settings,client=client)
    assert len(r.parsed.measurements)==224 and len(calls)==1 and r.generation.used_mode=='GROQ_AI'
    assert len(json.dumps(calls[0]['messages']).encode())<24000
    payload=json.loads(calls[0]['messages'][1]['content'])
    assert payload['complete_evidence_retained_locally'] is True
    assert payload['source_summary']==dict(teeth=32,positions=224,numeric=224,unknown=0)


def test_evidence_only_micro_never_selects_toy_shapes():
    r=report('B','micro',options={'policy_mode':'EVIDENCE_REVIEW'})
    assert all(row.primary is None for row in r.functional_plan.attachment_rows)
    assert 'Combined angular profile' in r.sections[0].text


def staged_input():
    raw='Tooth\tRotation (deg)\tAngulation (deg)\tInclination (deg)\tVertical (mm)\tRelative Ext / Int (mm)\tTranslation B / L (mm)\tTranslation M / D (mm)\n11\t0.00\t0.00\t0.00\t0.00\t0.00\t0.60 L\t0.00\n21\t1.20 D\t0.00\t0.00\t0.00\t0.00\t0.00\t0.00'
    parsed=resolve(request(raw=raw,module='nano'))
    teeth={t.token:t.id for t in parsed.teeth}
    cells={(m.tooth_ref,m.recognized_label):m for m in parsed.measurements}
    details=dict(stages=[dict(stage_id='start',order=1),dict(stage_id='finish',order=2)],allocations=[
        dict(stage_id=s,tooth_ref=teeth[t],measurement_ref=cells[teeth[t],f].id,amount=a,unit=cells[teeth[t],f].unit)
        for s,t,f,a in [('start','11','buccolingual','0.60'),('finish','21','rotation','1.20'),('start','21','buccolingual','0.00'),('finish','11','rotation','0.00')]])
    options=dict(source_sha256=parsed.raw_sha256,stage_value_basis='INCREMENTS_MATCH_SOURCE_LABELS',
        phases=[dict(phase_id=p,label=p,stage_ids=[s]) for p,s in [('initial','start'),('final','finish')]],
        support_constraints=[dict(phase_id=p,support_tooth_refs=[teeth[support]],active_tooth_refs=[teeth[active]],assumption='STATIONARY_IN_FICTIONAL_SCENARIO')
            for p,support,active in [('initial','21','11'),('final','11','21')]])
    return raw,options,details


@pytest.mark.parametrize('mutation',['valid','mismatch','basis','missing','conflict','mode'])
def test_arbitrary_explicit_stages_and_constraints_use_existing_checks(mutation):
    raw,options,details=staged_input()
    if mutation=='mismatch': details['allocations'][0]['amount']='0.50'
    if mutation=='basis': options['stage_value_basis']='UNSPECIFIED'
    if mutation=='missing': details['allocations'][0]['amount']=None
    if mutation=='conflict': details['stages'][1]['order']=1
    if mutation=='mode': options['policy_mode']='EVIDENCE_REVIEW'
    r=report(module='nano',raw=raw,options=options,review_details=details)
    assert not r.functional_plan.review_outline
    support=[d for d in r.functional_plan.decisions if d.dimension=='ANCHORAGE']
    if mutation=='valid':
        assert len(r.functional_plan.stages)==2
        assert len(r.functional_plan.allocation_checks)==4 and all(c.status=='MATCH' for c in r.functional_plan.allocation_checks)
        assert all(d.status=='ILLUSTRATIVE_PROPOSAL' for d in support)
    else:
        assert all(d.status!='ILLUSTRATIVE_PROPOSAL' for d in support)
        assert any(c.status in {'CONFLICT','UNAVAILABLE'} for c in r.functional_plan.checks)
        if mutation=='conflict': assert not r.functional_plan.stages


@pytest.mark.parametrize('module',['macro','micro','nano'])
def test_unknown_custom_columns_do_not_trigger_known_movement_policies(module):
    raw='Tooth\tRotation (deg)\tUnmapped movement (mm)\n11\t0.00\t1.230\n21\t0.00\t0.00'
    r=report(raw=raw,module=module)
    assert not any(d.proposed_changes or d.attachment_primary for d in r.functional_plan.decisions)
    assert not r.functional_plan.review_outline and not r.functional_plan.stages


def test_comparison_source_does_not_authorize_numeric_modification_examples():
    _,_,options=target_options()
    r=report('C',options=options,context={'plan_mode':'COMPARISON'})
    assert r.sections and not any(d.proposed_changes for d in r.functional_plan.decisions)


def test_comparison_zeros_never_become_no_attachment_or_other_selected_shapes():
    r=report('B','micro',context={'plan_mode':'COMPARISON'})
    assert all(row.primary is None for row in r.functional_plan.attachment_rows)
    assert rows(r)['38'].outcome!='NO_ATTACHMENT'


def test_comparison_source_cannot_be_relabelled_as_stage_totals_by_user_options():
    raw,options,details=staged_input()
    r=report(module='nano',raw=raw,options=options,review_details=details,context={'plan_mode':'COMPARISON'})
    assert r.functional_plan.checks[0].code=='COMPARISON_NOT_STAGE_TOTAL'
    assert not r.functional_plan.stages and not r.functional_plan.allocation_checks
    assert not any(d.dimension=='ANCHORAGE' and d.status=='ILLUSTRATIVE_PROPOSAL' for d in r.functional_plan.decisions)
