"""SYNTHETIC TEST_ONLY rule oracles. No vendor mapping or purported clinical approval."""

from decimal import Decimal
import json
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.domain.models import RawTMTSubmission, SourceContext
from app.main import app
from app.parser.service import parse_table
from app.review.models import DraftReview, Finding, ReviewSubmission, RuleDefinition
from app.review.registry import RULES, RULE_BY_ID, execution_order
from app.review.safeguards import apply_output_safeguards, values
from app.review.service import review_table
from app.review.templates import CONTEXT_MATRIX, TEMPLATES
from app.semantics.fixtures import digest_json
from app.semantics.registry import DEFAULT_REGISTRY
from semantic_helpers import toy_complete_components, write_synthetic_fixture

RAW = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t−1.2300 M\t0.00 E\n'


def submission(raw=RAW, **kwargs):
    return RawTMTSubmission(raw_text=raw, synthetic_data_confirmed=True, **kwargs)


def synthetic_review(tmp_path, *, raw=RAW, overrides=None, context=None, omit=(), questions=()):
    """Explicit invented semantics apply only to these exact synthetic source positions."""
    lexical = parse_table(submission(raw, context=context or SourceContext(source_version='TEST_ONLY-1')))
    assertions = {}
    # These canonical names define toy observations, NOT translations of any vendor label/sign.
    for m in lexical.measurements:
        if m.id in omit:
            continue
        assertions[m.id] = toy_complete_components(unit=m.unit or 'deg', axis=f'TEST_AXIS_{m.id}',
                                                    tooth_identifier=f'TEST_TOOTH_{m.tooth_ref}')
        assertions[m.id].update((overrides or {}).get(m.id, {}))
    _, _, checked = write_synthetic_fixture(tmp_path, assertions, raw=raw, context=context)
    result = review_table(submission(raw, context=context or SourceContext(source_version='TEST_ONLY-1')),
                          checked=checked, test_only=True, requested_assessments=questions)
    return result, checked


def by_rule(report, rid):
    return [f for f in report.findings if rid in {r.rule_id for r in f.triggering_rules}]


def observed(report, rid):
    return [f for f in by_rule(report, rid) if f.status == 'OBSERVED' and f.finding_type == 'DESCRIPTIVE']


def test_catalog_retains_all_96_audit_ids_and_no_thresholds():
    assert len(RULES) == 96
    assert {r.rule_id for r in RULES} == {f'{prefix}{i:02}' for prefix, count in [('G',18),('D',16),('R',16),('T',8),('A',6),('H',12),('L',6),('N',14)] for i in range(1,count+1)}
    for rule in RULES:
        assert rule.threshold is None and rule.policy_id is None and rule.clinical_approver is None
        if rule.category == 'CLINICAL' or rule.rule_id.startswith('T') or rule.rule_id in {'A01','A02','A03','A04'}:
            assert rule.execution == 'DISABLED'
    assert RULE_BY_ID['R14'].category == 'SAFETY'
    assert DEFAULT_REGISTRY.approved == frozenset()


def test_dependencies_stable_and_order_independent():
    ordered = execution_order()
    assert ordered == execution_order(tuple(reversed(RULES)))
    ids = [r.rule_id for r in ordered]
    assert ids.index('D01') < ids.index('D02')


@pytest.mark.parametrize('kind', ['missing', 'cycle', 'duplicate'])
def test_bad_registry_dependencies_fail_closed(kind):
    one = RULE_BY_ID['D01']
    if kind == 'missing':
        rules = (one.model_copy(update={'dependencies': ('MISSING',)}),)
    elif kind == 'cycle':
        rules = (one.model_copy(update={'dependencies': ('D02',)}), RULE_BY_ID['D02'])
    else:
        rules = (one, one)
    with pytest.raises(ValueError):
        execution_order(rules)


@pytest.mark.parametrize('source', ['Unknown', 'ClinCheck', 'SureSmile'])
@pytest.mark.parametrize('version', [None, '6.0', 'future-version'])
def test_no_vendor_claim_can_enable_observation_or_clinical_predicate(source, version):
    r = review_table(submission(source_claim=source, context=SourceContext(source_version=version, notation='FDI', reference_basis='CROWN_CENTER', scope='TOTAL')))
    assert r.evidence_domain == 'UNVERIFIED'
    assert r.coverage.eligible_positions == 0
    assert not any(f.observed_measurements or f.tooth_id for f in r.findings)
    assert all(not f.evaluated for f in r.findings if f.rule_id.startswith('D'))
    assert not r.clinical_analysis_enabled
    assert len(r.evaluations) == 96


def test_unknown_fields_are_not_zero_and_verified_test_fields_are_independent(tmp_path):
    r, _ = synthetic_review(tmp_path, omit=('measurement-1',))
    assert r.evidence_domain == 'TEST_ONLY'
    assert r.coverage.eligible_positions == 1
    assert r.coverage.eligible_explicit_zero == 1
    assert not observed(r, 'D01')
    assert any(f.status == 'SEMANTICS_UNKNOWN' and f.input_refs == ('measurements/measurement-1',) for f in by_rule(r, 'D01'))
    assert not observed(r, 'D15')  # unknown sibling cannot become zero


@pytest.mark.parametrize('token', ['', '—', '?', 'N/A', 'NaN', '1e2', '<script>x</script>'])
def test_missing_or_invalid_numeric_never_yields_observed_zero(tmp_path, token):
    raw = f'# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t{token}'
    r, _ = synthetic_review(tmp_path, raw=raw)
    assert r.coverage.eligible_positions == 0
    assert not observed(r, 'D01') and not observed(r, 'D15')
    assert all(not f.observed_measurements for f in r.findings)


def test_exact_precision_provenance_and_draft_state(tmp_path):
    r, checked = synthetic_review(tmp_path)
    f = observed(r, 'D01')[0]
    o = f.observed_measurements[0]
    assert str(o.magnitude) == '1.2300' and str(o.signed_decimal) == '-1.2300'
    assert o.raw_value == '−1.2300 M' and o.raw_sign == '−' and o.raw_direction == 'M'
    assert o.verification == 'TEST_ONLY' and f.tooth_id is None
    assert all(RAW[s.start:s.end] in {'13','Rotation (deg)','−1.2300 M'} for s in o.source_spans)
    assert all(c.status == 'TEST_ONLY' for c in o.components if c.canonical_value is not None)
    assert any(checked.release_digest in e for e in f.evidence_refs)
    assert f.review_status == r.review_status == 'DRAFT'
    assert DraftReview.model_validate_json(r.model_dump_json()) == r


def test_explicit_zero_is_not_a_no_movement_or_no_concern_claim(tmp_path):
    r, _ = synthetic_review(tmp_path, raw='# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t−0.000 M')
    f = observed(r, 'D15')[0]
    assert f.message == TEMPLATES['zero']
    assert str(f.observed_measurements[0].signed_decimal) == '-0.000'
    assert r.coverage.eligible_nonzero == 0
    assert not observed(r, 'D01')
    assert 'Unlisted axes remain unknown' in f.message


def test_co_programming_merges_ids_without_concurrency_or_double_count(tmp_path):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t1 M\t2 E'
    r, _ = synthetic_review(tmp_path, raw=raw, overrides={'measurement-1': {'axis': 'ROTATION'}, 'measurement-2': {'axis': 'EXTRUSION'}})
    fs = observed(r, 'D02')
    assert len(fs) == 1
    assert {x.rule_id for x in fs[0].triggering_rules} == {'D02','D10'}
    assert 'Temporal overlap is unknown' in fs[0].message
    assert len(fs[0].observed_measurements) == 2
    assert next(e for e in r.evaluations if e.rule_id == 'D10').finding_ids == (fs[0].finding_id,)


def test_d11_shared_logic_uses_no_bodily_root_or_force_claim(tmp_path):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tInclination (deg)\tBuccolingual (mm)\n13\t1 B\t2 B'
    r, _ = synthetic_review(tmp_path, raw=raw, overrides={'measurement-1': {'axis': 'INCLINATION'}, 'measurement-2': {'axis': 'BUCCOLINGUAL'}})
    assert {x.rule_id for x in observed(r,'D02')[0].triggering_rules} == {'D02','D11'}
    assert observed(r,'D06') and observed(r,'D07')


@pytest.mark.parametrize('rid,axis,label', [('D06','ANGULATION','Angulation (deg)'), ('D07','BUCCOLINGUAL','Buccolingual (mm)'), ('D08','MESIODISTAL','Mesiodistal (mm)')])
def test_inventory_uses_only_explicit_canonical_test_semantics(tmp_path, rid, axis, label):
    raw = f'# SYNTHETIC TEST_ONLY\nTooth\t{label}\n13\t1.000 B'
    r, _ = synthetic_review(tmp_path, raw=raw, overrides={'measurement-1': {'axis': axis}})
    assert len(observed(r, rid)) == 1
    assert str(observed(r,rid)[0].observed_measurements[0].magnitude) == '1.000'


@pytest.mark.parametrize('field', ['notation','dentition','arch','axis','sign','direction','reference_basis','scope','plan_mode','source_version','coordinate_frame'])
def test_each_unknown_required_field_causes_local_abstention(tmp_path, field):
    r, _ = synthetic_review(tmp_path, overrides={'measurement-1': {field: None}})
    assert r.coverage.eligible_positions == 1
    assert not observed(r,'D01')
    assert field in by_rule(r,'D01')[0].missing_required_fields or any(field in f.missing_required_fields for f in by_rule(r,'D01'))


def test_incompatible_bases_never_combine_or_compare(tmp_path):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t1 M\t2 E'
    r, _ = synthetic_review(tmp_path, raw=raw, overrides={'measurement-2': {'reference_basis': 'TEST_REFERENCE_B'}})
    assert len(observed(r,'D01')) == 2
    assert not observed(r,'D02')
    assert len(observed(r,'D12')) == 2
    assert by_rule(r,'D13')[0].status == 'CONTEXT_REQUIRED'
    assert by_rule(r,'D16')[0].status == 'CONTEXT_REQUIRED'


def test_comparison_values_do_not_become_absolute_plans(tmp_path):
    extra = {'plan_mode':'COMPARISON','comparison_left_plan':'TEST_PLAN_A','comparison_right_plan':'TEST_PLAN_B','comparison_operation':'TEST_REPORTED_DELTA'}
    r, _ = synthetic_review(tmp_path, overrides={'measurement-1':extra,'measurement-2':extra})
    assert r.coverage.eligible_positions == 0
    assert not observed(r,'D01') and not observed(r,'D12')
    assert all(f.abstain_reason == 'COMPARISON_NOT_ABSOLUTE' for f in by_rule(r,'D01'))


@pytest.mark.parametrize('scope', ['CUMULATIVE','INCREMENTAL','STAGE_SPECIFIC'])
@pytest.mark.parametrize('stage_kind', ['PASSIVE','ACCOMMODATION','OVERCORRECTION'])
def test_single_stage_values_preserve_stage_zero_and_kind_without_sequence_claims(tmp_path, scope, stage_kind):
    extra={'scope':scope,'stage_index':'0','stage_kind':stage_kind}
    r, _ = synthetic_review(tmp_path, overrides={'measurement-1':extra,'measurement-2':extra})
    assert len(observed(r,'D01')) == 1
    assert values(observed(r,'D01')[0].observed_measurements[0])['stage_index'] == '0'
    assert values(observed(r,'D01')[0].observed_measurements[0])['stage_kind'] == stage_kind
    assert not observed(r,'D02')
    assert any(f.abstain_reason == 'TOTAL_CO_PROGRAMMING_ONLY' for f in by_rule(r,'D02'))
    assert all(by_rule(r,f'T{i:02}')[0].status == 'DISABLED' for i in range(1,9))


def test_missing_stage_semantics_abstain_without_dividing_total(tmp_path):
    r, _ = synthetic_review(tmp_path, overrides={'measurement-1': {'scope':'INCREMENTAL'}})
    assert not observed(r,'D01')
    withheld = next(f for f in by_rule(r,'D01') if f.input_refs == ('measurements/measurement-1',))
    assert {'stage_index','stage_kind'} <= set(withheld.missing_required_fields)
    total = review_table(submission(context=SourceContext(scope='TOTAL')))
    assert by_rule(total,'G15')[0].status == 'NOT_APPLICABLE'


@pytest.mark.parametrize('same', [True,False])
def test_duplicate_source_positions_never_summed_or_last_wins(tmp_path, same):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tRot (deg)\n13\t1 M\t' + ('1 M' if same else '2 M')
    r,_ = synthetic_review(tmp_path,raw=raw)
    assert r.coverage.eligible_positions == 0
    assert not observed(r,'D01')
    assert all(f.status != 'OBSERVED' for f in by_rule(r,'G06'))


def test_distribution_counts_never_add_degrees_and_millimeters(tmp_path):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t10 M\t2 E'
    r,_ = synthetic_review(tmp_path,raw=raw)
    counts=observed(r,'D12')[0].summary_counts
    assert counts == {'nonzero_positions':2,'distinct_axes':2,'distinct_teeth':1,'distinct_arches':1,'eligible_positions_in_context':2}
    assert 'sum' not in counts and 'risk' not in counts


def test_no_missing_clinical_context_laundry_list_for_descriptive_only_request(tmp_path):
    r,_=synthetic_review(tmp_path)
    assert by_rule(r,'D14')[0].status == by_rule(r,'R14')[0].status == 'NOT_APPLICABLE'
    assert all(by_rule(r,rid)[0].status == 'NOT_APPLICABLE' for rid,_,_ in CONTEXT_MATRIX.values())


@pytest.mark.parametrize('question', sorted(CONTEXT_MATRIX))
def test_requested_clinical_conclusions_explicitly_withheld(tmp_path,question):
    r,_=synthetic_review(tmp_path,questions=(question,))
    rid,template,fields=CONTEXT_MATRIX[question]
    f=by_rule(r,rid)[0]
    assert f.status == 'CONTEXT_REQUIRED' and not f.evaluated and not f.observed_measurements
    assert f.template_id == template and set(f.missing_required_fields) == set(fields)
    assert by_rule(r,'R14')[0].status == 'CONTEXT_REQUIRED'
    assert len([f for f in by_rule(r,'D14') if f.missing_required_fields]) == 1


def test_proof_requires_exact_input_context_and_explicit_test_only_switch(tmp_path):
    r,checked=synthetic_review(tmp_path)
    assert r.coverage.eligible_positions == 2
    assert review_table(submission(context=SourceContext(source_version='TEST_ONLY-1')),checked=checked).coverage.eligible_positions == 0
    assert review_table(submission(RAW+'\n',context=SourceContext(source_version='TEST_ONLY-1')),checked=checked,test_only=True).coverage.eligible_positions == 0
    assert review_table(submission(context=SourceContext(source_version='TEST_ONLY-2')),checked=checked,test_only=True).coverage.eligible_positions == 0
    assert review_table(submission(source_claim='ClinCheck',context=SourceContext(source_version='TEST_ONLY-1')),checked=checked,test_only=True).coverage.eligible_positions == 0


def test_deterministic_complete_report_and_content_digest(tmp_path):
    r,checked=synthetic_review(tmp_path)
    replay=review_table(submission(context=SourceContext(source_version='TEST_ONLY-1')),checked=checked,test_only=True)
    assert replay.model_dump_json() == r.model_dump_json()
    assert digest_json(r.model_dump(mode='json',exclude={'report_id'})) == r.report_id
    assert all(e.finding_ids for e in r.evaluations)
    changed=review_table(submission(context=SourceContext(source_version='TEST_ONLY-1')),checked=checked,test_only=True,requested_assessments=('PROGNOSIS',))
    assert changed.report_id != r.report_id and changed.review_status == 'DRAFT'


def test_output_guard_rejects_mutated_numbers_directions_templates_and_clinical_claims(tmp_path):
    r,_=synthetic_review(tmp_path)
    f=observed(r,'D01')[0]; o=f.observed_measurements[0]
    authorized={o.measurement_id:o}
    mutations=[f.model_copy(update={'message':'Treatment will succeed'}),
               f.model_copy(update={'observed_measurements':(o.model_copy(update={'magnitude':Decimal('999')}),)}),
               f.model_copy(update={'observed_measurements':(o.model_copy(update={'magnitude':Decimal('1.23')}),)}),
               f.model_copy(update={'observed_measurements':(o.model_copy(update={'raw_direction':'UNSUPPORTED'}),)}),
               f.model_copy(update={'input_refs':()}),
               f.model_copy(update={'rule_id':'R01','triggering_rules':(f.triggering_rules[0].model_copy(update={'rule_id':'R01'}),)})]
    for candidate in mutations:
        final=apply_output_safeguards([candidate],authorized)[0]
        assert final.status == 'SUPPRESSED' and not final.observed_measurements and final.tooth_id is None
        assert final.abstain_reason == 'OUTPUT_FACT_OR_PROVENANCE_NOT_AUTHORIZED'


def test_exact_duplicate_propositions_merge_all_triggering_ids(tmp_path):
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t1 M\t2 E'
    r,_=synthetic_review(tmp_path,raw=raw,overrides={'measurement-1':{'axis':'ROTATION'},'measurement-2':{'axis':'EXTRUSION'}})
    f=observed(r,'D02')[0]
    first=f.model_copy(update={'triggering_rules':(f.triggering_rules[0],)})
    other=f.model_copy(update={'finding_id':'a'*64,'rule_id':'D10','triggering_rules':(f.triggering_rules[1],)})
    final=apply_output_safeguards([first,other],{o.measurement_id:o for o in f.observed_measurements})
    assert len(final) == 1
    assert {ref.rule_id for ref in final[0].triggering_rules} == {'D02','D10'}


def test_real_conflicting_propositions_are_both_visible_and_suppressed(tmp_path):
    r,_=synthetic_review(tmp_path)
    f=observed(r,'D01')[0]; o=f.observed_measurements[0]
    # Synthetic conflict injection into the output-control unit, never vendor evidence.
    other=o.model_copy(update={'measurement_id':'TEST_CONFLICT_POSITION','magnitude':Decimal('2')})
    second=f.model_copy(update={'finding_id':'b'*64,'observed_measurements':(other,)})
    final=apply_output_safeguards([f,second],{o.measurement_id:o,other.measurement_id:other})
    assert len(final) == 2
    assert all(x.status == 'SUPPRESSED' and x.conflict_group for x in final)
    assert final[0].conflict_group == final[1].conflict_group


@pytest.mark.parametrize('change', [{'review_status':'APPROVED'}, {'status':'SEMANTICS_UNKNOWN'}, {'observed_measurements':()}])
def test_invalid_finding_states_rejected(tmp_path,change):
    r,_=synthetic_review(tmp_path)
    data=observed(r,'D01')[0].model_dump()
    data.update(change)
    with pytest.raises(ValidationError):
        Finding.model_validate(data)


def test_internal_rule_engine_does_not_log_or_mutate_submission(tmp_path,caplog):
    caplog.set_level('DEBUG')
    request=submission(); before=request.model_dump_json()
    result=review_table(request)
    assert request.model_dump_json() == before
    assert RAW not in caplog.text
    assert result.source.adapter.verified is False


client=TestClient(app)


def test_api_is_raw_only_unverified_draft_and_private(caplog):
    caplog.set_level('DEBUG')
    response=client.post('/api/v1/tmt/observations',json={**submission().model_dump(mode='json'),'requested_assessments':['ATTACHMENTS']})
    assert response.status_code == 200
    r=DraftReview.model_validate_json(response.content)
    assert r.evidence_domain == 'UNVERIFIED' and r.review_status == 'DRAFT'
    assert r.coverage.eligible_positions == 0
    assert by_rule(r,'H08')[0].status == 'CONTEXT_REQUIRED'
    assert response.headers['cache-control'] == 'no-store' and response.headers['x-content-type-options'] == 'nosniff'
    assert RAW not in caplog.text


@pytest.mark.parametrize('extra', [{'test_only':True},{'checked':{}},{'semantics_verified':True},{'clinical_analysis_enabled':True},
                                   {'requested_assessments':['ANYTHING']},{'requested_assessments':['IPR','IPR']},
                                   {'synthetic_data_confirmed':False},{'synthetic_data_confirmed':1},{'context':{'verified':True}},
                                   {'raw_text':'x'*100001}])
def test_api_rejects_trust_injection_and_invalid_input_without_echo(extra):
    response=client.post('/api/v1/tmt/observations',json={**submission().model_dump(mode='json'),**extra})
    assert response.status_code == 422
    assert 'raw_text' not in response.text and 'semantics_verified' not in response.text and 'x'*100 not in response.text


@pytest.mark.parametrize('raw', ['', 'nonsense', 'Tooth\tRotation (deg)\n13\t<script>attack()</script>'])
def test_api_bad_structure_still_returns_safe_draft(raw):
    response=client.post('/api/v1/tmt/observations',json=submission(raw).model_dump(mode='json'))
    assert response.status_code == 200
    r=DraftReview.model_validate_json(response.content)
    assert not r.clinical_analysis_enabled and r.coverage.eligible_positions == 0
    assert not any(f.observed_measurements for f in r.findings)


def test_request_size_and_invalid_json_are_sanitized():
    for content,status in [(b'x'*1048577,413),(b'{"raw_text":"DO_NOT_ECHO",',422)]:
        response=client.post('/api/v1/tmt/observations',content=content,headers={'Content-Type':'application/json'})
        assert response.status_code == status and 'DO_NOT_ECHO' not in response.text
        assert response.headers['cache-control'] == 'no-store'


def test_review_schemas_match_exported_contracts():
    root=Path(__file__).resolve().parents[2]/'schemas'
    for name,model,mode in [('review-request.v1.json',ReviewSubmission,'validation'),('draft-review.v1.json',DraftReview,'serialization'),('rule-definition.v1.json',RuleDefinition,'serialization')]:
        assert json.loads((root/name).read_text(encoding='utf-8')) == model.model_json_schema(mode=mode)


def test_large_lexical_input_has_compact_explicit_review_abstention():
    raw = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n' + ''.join(f'{i}\t1 M\n' for i in range(513))
    request = submission(raw)
    assert len(parse_table(request).measurements) == 513  # parser functionality unchanged
    report = review_table(request)
    assert len(report.findings) == 96 and report.coverage.declared_positions == 513
    assert report.coverage.eligible_positions == 0
    assert by_rule(report,'D01')[0].abstain_reason == 'REVIEW_POSITION_ENGINEERING_LIMIT'
    assert report.review_status == 'DRAFT'


@pytest.mark.parametrize('field,value', [('raw_text',RAW+'\n'),('source_claim','ClinCheck'),('context',{'scope':'INCREMENTAL','stage_index':0})])
def test_content_change_produces_new_draft_identity(field,value):
    baseline = submission().model_dump(mode='json')
    a=review_table(RawTMTSubmission.model_validate(baseline))
    baseline[field]=value
    b=review_table(RawTMTSubmission.model_validate(baseline))
    assert a.report_id != b.report_id and b.review_status == 'DRAFT'


def test_reordered_source_rows_preserve_toy_observation_meaning(tmp_path):
    first = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t1 M\n14\t2 M'
    second = '# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n14\t2 M\n13\t1 M'
    a,_=synthetic_review(tmp_path,raw=first,overrides={'measurement-1':{'axis':'TEST_AXIS','tooth_identifier':'TEST_A'},'measurement-2':{'axis':'TEST_AXIS','tooth_identifier':'TEST_B'}})
    b,_=synthetic_review(tmp_path,raw=second,overrides={'measurement-1':{'axis':'TEST_AXIS','tooth_identifier':'TEST_B'},'measurement-2':{'axis':'TEST_AXIS','tooth_identifier':'TEST_A'}})
    facts=lambda r: {(values(o)['tooth_identifier'],str(o.magnitude),values(o)['direction']) for f in observed(r,'D01') for o in f.observed_measurements}
    assert facts(a) == facts(b)
    assert a.raw_sha256 != b.raw_sha256  # provenance legitimately differs
