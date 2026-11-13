"""Synthetic, independently specified engineering oracles. No vendor/clinical approval."""
from collections import Counter
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.main import app
from app.domain.models import SourceContext
from app.parser.service import parse_table
from app.review.checks import provenance_errors, rule_eligibility
from app.review.clinical import REQUIREMENTS, MOVEMENT_REQUIREMENTS, IllustrativePolicy, preparation, simulate_test_only, inspect_candidate_inputs
from app.review.context import (ExpectedCoverage, PairedTeeth, StageRecord, TestRuleContext,
                               ToothContext, admit_test_context, input_digest, stage_errors)
from app.review.registry import RULES, RULE_BY_ID, CATALOG, execution_order
from app.review.service import review_table
from app.review.safeguards import apply_output_safeguards, values
from app.reports.service import generate_report, _assemble
from test_review import submission, synthetic_review, observed, by_rule, RAW
from test_reports import settings, successful_client

CASES=json.loads((Path(__file__).parent/'fixtures/phase5_rule_cases.json').read_text())
IDS=[f'{p}{i:02}' for p,n in [('G',18),('D',16),('R',16),('T',8),('A',6),('H',12),('L',6),('N',14)] for i in range(1,n+1)]

def context_for(raw=RAW, **kwargs):
    return TestRuleContext(input_digest=input_digest(submission(raw,context=SourceContext(source_version='TEST_ONLY-1'))),**kwargs)

def run_with(tmp_path, raw=RAW, overrides=None, **kwargs):
    _,checked=synthetic_review(tmp_path,raw=raw,overrides=overrides)
    s=submission(raw,context=SourceContext(source_version='TEST_ONLY-1'))
    return review_table(s,checked=checked,test_only=True,test_context=context_for(raw,**kwargs)),checked,s

@pytest.mark.parametrize('rid',IDS)
def test_every_rule_has_audited_identity_execution_and_ledger(rid):
    rule=RULE_BY_ID[rid]
    assert rule.rule_id==rid and rule.version=='2.0.0'
    expected='DISABLED' if rid in CASES['disabled'] else 'DEFERRED' if rid in CASES['deferred'] else 'ACTIVE'
    assert rule.execution==expected
    assert rule.purpose==CATALOG[rid]['audit_required'] and rule.source_locator
    assert rule.disposition==CATALOG[rid]['disposition']
    assert rule.threshold is None and rule.policy_id is None and rule.clinical_approver is None
    report=review_table(submission())
    ledger=next(e for e in report.evaluations if e.rule_id==rid)
    assert ledger.execution==expected and ledger.priority==rule.priority
    assert ledger.finding_ids and ledger.approval_status==rule.approval_status
    if expected!='ACTIVE':
        assert not ledger.evaluated and ledger.triggered is None
        assert ledger.missing_required_fields and ledger.abstain_reason
    if expected=='DISABLED': assert ledger.status=='DISABLED' and ledger.approval_status=='NOT APPROVED'

def test_catalog_exact_audit_counts_and_bound_sources():
    root=Path(__file__).parents[2]
    c=json.loads((root/'backend/app/review/catalog.json').read_text())
    assert Counter(r.disposition for r in RULES)=={'READY':49,'REVISE':5,'VALIDATE':13,'MORE DATA':15,'ADDITIONAL':14}
    assert c['source_hash_basis'].startswith('UTF8_DOCUMENT_TEXT_WITH_LF_NEWLINES')
    assert c['source_spec_sha256']==sha256((root/'docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md').read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert c['source_audit_sha256']==sha256((root/'docs/Orthodontic_TMT_Independent_Critical_Audit(2).md').read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert 'UNAVAILABLE_STANDALONE' in c['original_v1_document']
    assert set(CATALOG)==set(IDS)

def test_priority_topology_is_stable_and_input_gates_precede_descriptions():
    ids=[r.rule_id for r in execution_order()]
    assert execution_order()==execution_order(tuple(reversed(RULES)))
    for r in RULES:
        assert all(ids.index(d)<ids.index(r.rule_id) for d in r.dependencies)
    assert ids.index('G16')<ids.index('D01')<ids.index('D03')<ids.index('L01')
    assert ids.index('N05')<ids.index('D13')

@pytest.mark.parametrize('case',CASES['groups'])
def test_explicit_group_oracles(tmp_path,case):
    raw=f'# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t{case["value"]} M'
    r,_,_=run_with(tmp_path,raw,{'measurement-1':{'axis':case['axis'],'direction':case['direction']}},
        teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group=case['group'],status='PRESENT',movement_permitted=True,evidence_ref='TEST_ONLY:group-oracle'),))
    assert bool(observed(r,case['rule'])) is case['observed']
    if case['observed']:
        o=observed(r,case['rule'])[0].observed_measurements[0]
        assert str(o.magnitude)==case['value'] and o.tooth_group==case['group']
        assert o.additional_evidence_refs==('TEST_ONLY:group-oracle',)

def test_external_status_contradiction_is_local_and_zero_retained(tmp_path):
    r,_,_=run_with(tmp_path,teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group='CANINE',status='FIXED',movement_permitted=False,evidence_ref='TEST_ONLY:fixed'),))
    assert r.coverage.eligible_positions==1 and r.coverage.eligible_explicit_zero==1
    assert not observed(r,'D01')
    assert any('consistent_external_tooth_status' in f.missing_required_fields for f in by_rule(r,'D01'))
    assert any(f.status=='OBSERVED' for f in by_rule(r,'G14')) # explicit zero is permitted

def test_missing_group_does_not_invalidate_general_inventory(tmp_path):
    r,_=synthetic_review(tmp_path,overrides={'measurement-1':{'axis':'ROTATION'}})
    assert observed(r,'D01') and not observed(r,'D03')
    assert 'verified_tooth_group_map' in by_rule(r,'D03')[0].missing_required_fields

@pytest.mark.parametrize('case',CASES['paired_values'])
def test_pair_difference_requires_independent_equivalence_and_never_subtracts(tmp_path,case):
    raw=f'# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t{case["left"]} M\n23\t{case["right"]} M'
    overrides={f'measurement-{i}':{'axis':'ROTATION','direction':direction} for i,direction in [(1,'TOY_LEFT'),(2,'TOY_RIGHT')]}
    pair=PairedTeeth(left_id='TEST_TOOTH_tooth-1',right_id='TEST_TOOTH_tooth-2',axis='ROTATION',left_direction='TOY_LEFT',right_direction='TOY_RIGHT',equivalent_plan_basis_scope_frame=True,equivalent_direction_meaning=True,evidence_ref='TEST_ONLY:pair-oracle')
    r,_,_=run_with(tmp_path,raw,overrides,pairs=(pair,))
    assert bool(observed(r,'D13')) is case['observed']
    if case['observed']:
        f=observed(r,'D13')[0]
        assert {str(o.magnitude) for o in f.observed_measurements}=={case['left'],case['right']}
        assert all(o.pair_evidence_ref=='TEST_ONLY:pair-oracle' for o in f.observed_measurements)
        assert 'No subtraction, pathologic asymmetry or clinical conclusion is inferred.' in f.message

@pytest.mark.parametrize('field,value',[('reference_basis','OTHER_BASIS'),('plan_mode','DOCTOR_FINAL'),('coordinate_frame','OTHER_FRAME'),('unit','mm'),('direction','OTHER_DIRECTION'),('scope','INCREMENTAL')])
def test_incompatible_pair_context_never_compares(tmp_path,field,value):
    raw='# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t1 M\n23\t2 M'
    pair=PairedTeeth(left_id='TEST_TOOTH_tooth-1',right_id='TEST_TOOTH_tooth-2',axis='ROTATION',left_direction='TEST_DIRECTION_ALPHA',right_direction='TEST_DIRECTION_ALPHA',equivalent_plan_basis_scope_frame=True,equivalent_direction_meaning=True,evidence_ref='TEST_ONLY:pair')
    r,_,_=run_with(tmp_path,raw,{'measurement-1':{'axis':'ROTATION'},'measurement-2':{'axis':'ROTATION',field:value}},pairs=(pair,))
    assert not observed(r,'D13')
    assert next(e for e in r.evaluations if e.rule_id=='N05').status=='CONTEXT_REQUIRED'

@pytest.mark.parametrize('problem', ['duplicate','order','baseline'])
def test_stage_dataset_errors_have_no_total_scope_inference(tmp_path,problem):
    seq=[StageRecord(stage_id='s1',index=1,arch='TEST_ARCH',kind='ACTIVE',evidence_ref='TEST_ONLY:s1'),StageRecord(stage_id='s2',index=2,arch='TEST_ARCH',kind='PASSIVE',evidence_ref='TEST_ONLY:s2')]
    if problem=='duplicate': seq[1]=seq[1].model_copy(update={'index':1})
    elif problem=='order': seq.reverse()
    else: seq[0]=seq[0].model_copy(update={'index':0,'kind':'ACTIVE'})
    assert stage_errors(tuple(seq))
    r,_,_=run_with(tmp_path,stages=tuple(seq))
    assert next(e for e in r.evaluations if e.rule_id=='G15').status=='PARSE_INVALID'
    assert observed(r,'D01') # total field is independent

def test_stage_gaps_and_absent_baseline_are_not_fabricated():
    stages=tuple(StageRecord(stage_id=f's{i}',index=i,arch='TOY_ARCH',kind='ACTIVE',evidence_ref=f'TEST_ONLY:s{i}') for i in (1,3))
    assert stage_errors(stages)==()

def test_all_input_gate_positive_paths_use_explicit_toy_evidence(tmp_path):
    r,_,_=run_with(tmp_path,teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group='CANINE',status='PRESENT',movement_permitted=True,evidence_ref='TEST_ONLY:tooth'),),
        stages=(StageRecord(stage_id='baseline',index=0,arch='TEST_ARCH',kind='BASELINE',evidence_ref='TEST_ONLY:baseline'),))
    for rid in (f'G{i:02}' for i in range(1,19)):
        assert all(f.status=='OBSERVED' for f in by_rule(r,rid)),rid
    assert next(e for e in r.evaluations if e.rule_id=='N06').status=='OBSERVED'

@pytest.mark.parametrize('valid',[False,True])
def test_actual_stage_consistency_is_scope_local(tmp_path,valid):
    stages=(StageRecord(stage_id='s1',index=1,arch='TEST_ARCH',kind='ACTIVE',evidence_ref='TEST_ONLY:s1'),
            StageRecord(stage_id='s2',index=2 if valid else 1,arch='TEST_ARCH',kind='PASSIVE',evidence_ref='TEST_ONLY:s2'))
    r,_,_=run_with(tmp_path,overrides={'measurement-1':{'scope':'INCREMENTAL','stage_index':'1','stage_kind':'ACTIVE'}},stages=stages)
    assert bool(observed(r,'D01')) is valid
    assert r.coverage.eligible_explicit_zero==1 # unrelated total zero remains eligible
    assert next(e for e in r.evaluations if e.rule_id=='G15').status==('OBSERVED' if valid else 'PARSE_INVALID')
    if not valid:
        assert 'consistent_stage_dataset' in by_rule(r,'D01')[0].missing_required_fields

def test_verified_but_unsupported_mode_does_not_enable_descriptive_rule(tmp_path):
    r,_=synthetic_review(tmp_path,overrides={f'measurement-{i}':{'plan_mode':'UNSUPPORTED_TOY_MODE'} for i in (1,2)})
    assert r.coverage.eligible_positions==0
    assert not any(f.finding_type=='DESCRIPTIVE' and f.status=='OBSERVED' for f in r.findings)

@pytest.mark.parametrize('axis,expected',[('TEST_AXIS_measurement-1','OBSERVED'),('UNOBSERVED_AXIS','CONTEXT_REQUIRED')])
def test_independent_expected_coverage_does_not_infer_zeros(tmp_path,axis,expected):
    r,_,_=run_with(tmp_path,coverage=(ExpectedCoverage(canonical_tooth_id='TEST_TOOTH_tooth-1',expected_axes=(axis,),evidence_ref='TEST_ONLY:coverage'),))
    e=next(e for e in r.evaluations if e.rule_id=='N01')
    assert e.status==expected and r.coverage.eligible_explicit_zero==1

def test_extra_context_cannot_be_replayed_or_promoted(tmp_path):
    r,checked,s=run_with(tmp_path)
    ctx=context_for()
    assert admit_test_context(ctx,s,test_only=True,domain='TEST_ONLY')==ctx
    assert admit_test_context(ctx,s,test_only=False,domain='TEST_ONLY') is None
    assert admit_test_context(ctx,s,test_only=True,domain='AUTHORIZED_VENDOR') is None
    assert admit_test_context(ctx,s.model_copy(update={'raw_text':RAW+' '}),test_only=True,domain='TEST_ONLY') is None
    assert admit_test_context(ctx,s.model_copy(update={'source_claim':'ClinCheck'}),test_only=True,domain='TEST_ONLY') is None

@pytest.mark.parametrize('field', ['test_context','test_only','checked','policy_id','threshold','clinical_approver','clinical_analysis_enabled'])
@pytest.mark.parametrize('route',['/api/v1/tmt/observations','/api/v1/reports/draft'])
def test_no_public_rule_or_policy_authorization_fields(field,route):
    data={'raw_text':RAW,'synthetic_data_confirmed':True,field:True}
    assert TestClient(app).post(route,json=data).status_code==422

@pytest.mark.parametrize('rid',list(REQUIREMENTS))
def test_all_clinical_preparations_are_non_executable_and_rule_specific(rid):
    p=preparation(rid)
    assert p.required_fields==REQUIREMENTS[rid] and p.required_fields
    assert not p.production_enabled and p.approval_status=='NOT APPROVED'
    assert p.policy_id is p.clinical_approver is None
    if rid not in {'R14','A05','A06'}: assert p.unapproved_parameters
    with pytest.raises(ValidationError): type(p).model_validate({**p.model_dump(),'production_enabled':True})

@pytest.mark.parametrize('comparator,boundary,expected',[('GT','1.2300',False),('GE','1.2300',True),('GT','1.2299',True),('GE','1.2301',False)])
def test_illustrative_decimal_comparator_is_isolated_not_a_clinical_predicate(tmp_path,comparator,boundary,expected):
    r,_=synthetic_review(tmp_path)
    o=observed(r,'D01')[0].observed_measurements[0]
    policy=IllustrativePolicy(domain='TEST_ONLY',axis=values(o)['axis'],unit=values(o)['unit'],comparator=comparator,illustrative_boundary=Decimal(boundary))
    result=simulate_test_only('R01',o,policy)
    assert result.predicate_result is expected and result.production_enabled is False
    assert 'NOT_CLINICAL_VALIDATION' in result.reason
    assert next(e for e in r.evaluations if e.rule_id=='R01').status=='DISABLED'

def test_provenance_hash_and_individual_spans_independent():
    lexical=parse_table(submission())
    assert provenance_errors(lexical)==((),set())
    bad=lexical.model_copy(update={'raw_sha256':'0'*64})
    assert provenance_errors(bad)[0]==('RAW_HASH_MISMATCH',)
    m=lexical.measurements[0]
    bad=lexical.model_copy(update={'measurements':(m.model_copy(update={'raw_value':'WRONG'}),*lexical.measurements[1:])})
    assert provenance_errors(bad)==((),{m.id})

def test_global_provenance_failure_blocks_all_movement_facts(tmp_path,monkeypatch):
    _,checked=synthetic_review(tmp_path)
    lexical=parse_table(submission(context=SourceContext(source_version='TEST_ONLY-1')))
    monkeypatch.setattr('app.review.service.resolve',lambda _:lexical.model_copy(update={'raw_sha256':'0'*64}))
    r=review_table(submission(context=SourceContext(source_version='TEST_ONLY-1')),checked=checked,test_only=True)
    assert r.coverage.eligible_positions==0 and not any(f.observed_measurements for f in r.findings)
    assert next(e for e in r.evaluations if e.rule_id=='N04').status=='PARSE_INVALID'

def test_rule_local_mode_and_scope_metadata(tmp_path):
    r,_=synthetic_review(tmp_path)
    o=observed(r,'D01')[0].observed_measurements[0]
    assert rule_eligibility(RULE_BY_ID['D01'],o)==()
    assert rule_eligibility(RULE_BY_ID['D01'].model_copy(update={'allowed_modes':('OTHER',)}),o)==('rule_plan_mode',)
    assert rule_eligibility(RULE_BY_ID['D01'].model_copy(update={'allowed_scopes':('OTHER',)}),o)==('rule_movement_scope',)

@pytest.mark.parametrize('rid',list(MOVEMENT_REQUIREMENTS))
def test_clinical_structural_readiness_cannot_become_a_finding(tmp_path,rid):
    r,_=synthetic_review(tmp_path)
    o=observed(r,'D01')[0].observed_measurements[0]
    result=inspect_candidate_inputs(rid,o)
    assert result.predicate_result is None and not result.production_enabled
    assert 'orthodontist_approved_policy' in result.missing_required_fields
    assert 'independently_verified_tooth_group' in result.missing_required_fields
    axes,groups,directions=MOVEMENT_REQUIREMENTS[rid]
    components=tuple(c.model_copy(update={'canonical_value':axes[0] if c.name=='axis' else directions[0] if c.name=='direction' and directions else c.canonical_value}) for c in o.components)
    explicit=o.model_copy(update={'components':components,'tooth_group':groups[0],'additional_evidence_refs':('TEST_ONLY:explicit',)})
    positive=inspect_candidate_inputs(rid,explicit)
    assert positive.structural_fields_satisfied is (rid not in {'R05','R10'})
    assert positive.predicate_result is None and not positive.production_enabled

def test_typed_context_rejects_conflicting_pairs_and_empty_coverage():
    with pytest.raises(ValidationError): ExpectedCoverage(canonical_tooth_id='x',expected_axes=(),evidence_ref='TEST_ONLY:x')
    p=PairedTeeth(left_id='a',right_id='b',axis='x',left_direction='a',right_direction='b',equivalent_plan_basis_scope_frame=True,equivalent_direction_meaning=True,evidence_ref='TEST_ONLY:pair')
    with pytest.raises(ValidationError): context_for(pairs=(p,p))

def test_new_descriptive_pipeline_exact_report_and_mocked_wording(tmp_path):
    r,checked,s=run_with(tmp_path,overrides={'measurement-1':{'axis':'ROTATION'}},teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group='CANINE',evidence_ref='TEST_ONLY:group'),))
    assert observed(r,'D03')
    assert 'TEST_ONLY:group' in observed(r,'D03')[0].evidence_refs
    captures=[]
    result=_assemble(r,'GROQ',settings(),successful_client(captured=captures))
    assert result.draft_status=='DRAFT — Requires Orthodontist Review'
    assert '1.2300' in result.export_text and 'CANINE' in result.export_text
    assert 'D03' in result.export_text and not result.clinical_analysis_enabled
    assert all('CANINE' not in q.content.decode() and '1.2300' not in q.content.decode() for q in captures)
    templated=generate_report(s,checked=checked,test_only=True,test_context=context_for(teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group='CANINE',evidence_ref='TEST_ONLY:group'),)),mode='TEMPLATES')
    assert templated.engine_review.model_dump_json()==r.model_dump_json()

def test_forged_clinical_or_technical_finding_is_suppressed(tmp_path):
    r,_=synthetic_review(tmp_path)
    f=observed(r,'D01')[0]
    eligible={o.measurement_id:o for x in r.findings for o in x.observed_measurements}
    for rid in ('R01','T01','A01'):
        forged=f.model_copy(update={'rule_id':rid,'triggering_rules':(f.triggering_rules[0].model_copy(update={'rule_id':rid}),)})
        assert apply_output_safeguards((forged,),eligible)[0].status=='SUPPRESSED'
    forged=f.model_copy(update={'finding_type':'TECHNICAL','observed_measurements':()})
    assert apply_output_safeguards((forged,),eligible)[0].status=='SUPPRESSED'

def test_additional_schemas_match_contracts_and_are_not_http_activation():
    from app.review.clinical import ClinicalPreparation, CandidateInputReadiness
    from app.review.context import AdditionalInputRequirements
    root=Path(__file__).parents[2]/'schemas'
    for name,model,mode in [('clinical-preparation.v1.json',ClinicalPreparation,'serialization'),
        ('candidate-input-readiness.v1.json',CandidateInputReadiness,'serialization'),
        ('additional-input-requirements.v1.json',AdditionalInputRequirements,'serialization'),
        ('test-only-rule-context.v1.json',TestRuleContext,'validation')]:
        assert json.loads((root/name).read_text(encoding='utf-8'))==model.model_json_schema(mode=mode)
