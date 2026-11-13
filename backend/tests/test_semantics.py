from dataclasses import replace
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from pydantic import ValidationError
import pytest

from app.domain.models import LexicalInput, RawTMTSubmission, SourceContext
from app.parser.service import parse_table
from app.semantics.fixtures import FixtureVerificationError, assert_fixture_matches, digest_json, load_manifest, verify_fixture
from app.semantics.models import (
    Artifact, COMPONENTS, ExpectedComponent, FixtureExpectedOutput, FixtureManifest, FixtureRecord,
    IndependentReview, SemanticAssessment, SemanticComponent,
)
from app.semantics.normalization import assess_semantics
from app.semantics.registry import DEFAULT_REGISTRY, EvidenceRegistry
from semantic_helpers import SYNTHETIC_RAW, toy_complete_components, write_synthetic_fixture


def components(assessment, index=0):
    return {field.name: field for field in assessment.measurements[index].components}


def test_production_catalog_has_no_authentic_fixtures_or_approved_releases():
    path = Path(__file__).resolve().parents[1] / 'vendor_verification/manifest.json'
    assert load_manifest(path).fixtures == ()
    assert DEFAULT_REGISTRY.approved == frozenset()
    lexical = parse_table(LexicalInput(raw_text=SYNTHETIC_RAW))
    result = assess_semantics(lexical)
    assert result.status == 'DISABLED'
    assert all(c.status == 'UNKNOWN' and c.canonical_value is None for m in result.measurements for c in m.components)
    assert all(m.canonical_magnitude is None and not m.canonical_measurement_ready for m in result.measurements)
    assert 'NUMBERING_AMBIGUOUS' in components(result)['notation'].abstain_reasons


@pytest.mark.parametrize('vendor', ['ClinCheck', 'SureSmile'])
@pytest.mark.parametrize('version', [None, '6.0', 'future-unrecognized-version'])
def test_vendor_claim_and_version_never_grant_authority(vendor, version):
    lexical = parse_table(LexicalInput(raw_text=SYNTHETIC_RAW, source_claim=vendor,
                                      context=SourceContext(source_version=version, notation='FDI', dentition='PERMANENT')))
    result = assess_semantics(lexical)
    assert result.status == 'DISABLED'
    assert 'SOURCE_VERSION_UNVERIFIED' in components(result)['source_version'].abstain_reasons
    assert components(result)['direction'].canonical_value is None
    assert components(result)['tooth_identifier'].canonical_value is None


def test_field_scoped_partial_evidence_cannot_verify_other_fields_or_vendor(tmp_path):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {
        'measurement-1': {'unit': 'deg'}, 'measurement-2': {'unit': 'mm', 'axis': 'TEST_AXIS_B'},
    })
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert result.status == 'TEST_ONLY'
    assert components(result)['unit'].status == 'TEST_ONLY'
    assert components(result)['direction'].status == 'UNKNOWN'
    assert components(result, 1)['axis'].canonical_value == 'TEST_AXIS_B'
    assert components(result)['axis'].canonical_value is None
    assert result.lexical.model_dump_json() == lexical.model_dump_json()
    assert lexical.measurements[0].canonical_axis is None
    assert not result.measurements[1].canonical_measurement_ready
    # Same invented proof is never accepted by the production default, even in an approval set.
    assert assess_semantics(lexical, checked).status == 'DISABLED'
    registry = EvidenceRegistry(approved=frozenset({checked.release_digest}))
    assert assess_semantics(lexical, checked, registry=registry).status == 'DISABLED'
    assert assess_semantics(lexical, checked, registry=registry, allow_test_only=True).status == 'TEST_ONLY'


def test_exact_raw_precision_and_source_provenance_are_retained(tmp_path):
    lexical, record, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}})
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert result.lexical.raw_text == SYNTHETIC_RAW
    assert result.lexical.raw_sha256 == sha256(SYNTHETIC_RAW.encode()).hexdigest()
    assert str(result.lexical.measurements[0].signed_decimal) == '-1.2300'
    field = components(result)['unit']
    for span in field.source_spans:
        assert SYNTHETIC_RAW[span.start:span.end] in {'−1.2300 M', 'Rotation (deg)', '13'}
    assert field.evidence[0].raw_sha256 == record.raw.sha256
    assert field.evidence[0].expected_sha256 == record.expected.sha256
    assert field.evidence[0].locator == 'TEST_ONLY:measurement-1:unit'
    assert 'measurements/measurement-1' in field.input_refs


@pytest.mark.parametrize('value', ['—', '', '?', 'NaN', '1e3'])
def test_missing_invalid_values_never_become_canonical_zero_or_direction(tmp_path, value):
    raw = f'# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t{value}'
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg', 'direction': 'TEST_DIRECTION_A'}}, raw=raw)
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert result.lexical.measurements[0].signed_decimal is None
    assert result.measurements[0].canonical_magnitude is None
    assert components(result)['direction'].canonical_value is None
    assert components(result)['unit'].status == 'TEST_ONLY'


@pytest.mark.parametrize('raw_sign', ['−', '-', '+', ''])
def test_literal_sign_does_not_imply_physical_direction(tmp_path, raw_sign):
    raw = f'# SYNTHETIC TEST_ONLY\nTooth\tRotation (deg)\n13\t{raw_sign}1.00 M'
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}}, raw=raw)
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['sign'].status == 'UNKNOWN'
    assert components(result)['direction'].status == 'UNKNOWN'
    assert lexical.measurements[0].raw_sign == (raw_sign or None)


@pytest.mark.parametrize('basis,expected', [('CROWN_CENTER', 'TEST_REFERENCE_B'), ('VIRTUAL_ROOT_APEX', 'CUSP_TIP'), ('CUSP_TIP', 'CROWN_CENTER')])
def test_incompatible_bases_abstain_without_converting_values(tmp_path, basis, expected):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'reference_basis': expected, 'axis': 'TEST_AXIS', 'unit': 'deg'}},
                                                 context=SourceContext(source_version='TEST_ONLY-1', reference_basis=basis))
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['reference_basis'].status == 'CONFLICT'
    assert components(result)['axis'].status == 'CONFLICT'
    assert components(result)['unit'].status == 'TEST_ONLY'
    assert str(result.lexical.measurements[0].signed_decimal) == '-1.2300'


def test_audited_vendor_context_conflict_is_not_silently_overridden(tmp_path):
    # No vendor mapping is supplied: this tests the negative audited claim guard only.
    raw = 'Source: SureSmile\nTooth\tRotation (deg)\n13\t0'
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'reference_basis': 'VIRTUAL_ROOT_APEX', 'unit': 'deg'}}, raw=raw,
                                                 context=SourceContext(reference_basis='VIRTUAL_ROOT_APEX'))
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['reference_basis'].status == 'CONFLICT'
    assert not result.measurements[0].canonical_measurement_ready


@pytest.mark.parametrize('unit', ['mm', 'cm', 'radians'])
def test_semantic_projection_does_not_silently_convert_units(tmp_path, unit):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': unit}})
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['unit'].status == 'CONFLICT'
    assert components(result)['unit'].canonical_value is None
    assert str(result.lexical.measurements[0].signed_decimal) == '-1.2300'


@pytest.mark.parametrize('notation', ['UNKNOWN', 'FDI', 'UNIVERSAL'])
def test_claimed_numbering_does_not_create_verified_tooth_identity(tmp_path, notation):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}},
                                                 context=SourceContext(notation=notation))
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['notation'].status == 'UNKNOWN'
    assert components(result)['tooth_identifier'].canonical_value is None
    assert result.lexical.teeth[0].normalized_identifier is None


def test_new_contract_rejects_forged_ready_or_verified_states(tmp_path):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}})
    assessment = assess_semantics(lexical, checked, allow_test_only=True)
    measurement = assessment.measurements[0]
    with pytest.raises(ValidationError):
        type(measurement).model_validate({**measurement.model_dump(), 'canonical_measurement_ready': True})
    with pytest.raises(ValidationError):
        SemanticAssessment.model_validate({**assessment.model_dump(), 'status': 'VERIFIED'})
    with pytest.raises(ValidationError):
        type(measurement).model_validate({**measurement.model_dump(), 'components': measurement.components[:-1]})


@pytest.mark.parametrize('change', ['raw', 'basis', 'mode', 'scope', 'stage', 'version', 'parser', 'adapter'])
def test_proofs_are_bound_to_exact_input_context_and_parser_versions(tmp_path, change):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}})
    altered = lexical.model_copy(deep=True)
    if change == 'raw': altered.raw_text += '\n'
    elif change == 'basis': altered.source.context.reference_basis = 'CROWN_CENTER'
    elif change == 'mode': altered.source.context.plan_mode = 'COMPARISON'
    elif change == 'scope': altered.source.context.scope = 'INCREMENTAL'
    elif change == 'stage': altered.source.context.stage_index = 0
    elif change == 'version': altered.source.context.source_version = 'TEST_ONLY-2'
    elif change == 'adapter': altered.source.adapter.version = '0.1.1'
    else: altered.source.adapter.id = 'different-parser'
    result = assess_semantics(altered, checked, allow_test_only=True)
    assert result.status == 'DISABLED'
    assert result.reasons == ('EVIDENCE_INPUT_OR_CONTEXT_MISMATCH',)


@pytest.mark.parametrize('scope', ['TOTAL', 'CUMULATIVE', 'INCREMENTAL', 'STAGE_SPECIFIC'])
def test_stage_semantics_require_explicit_proof_and_keep_stage_zero(tmp_path, scope):
    fields = toy_complete_components(scope=scope)
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': fields})
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert result.measurements[0].evidence_complete_for_test == (scope == 'TOTAL')
    assert not result.measurements[0].canonical_measurement_ready
    if scope != 'TOTAL':
        fields.update(stage_index='0', stage_kind='TEST_BASELINE')
        lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': fields})
        result = assess_semantics(lexical, checked, allow_test_only=True)
        assert components(result)['stage_index'].canonical_value == '0'
        assert result.measurements[0].evidence_complete_for_test
    assert str(result.lexical.measurements[0].signed_decimal) == '-1.2300'


@pytest.mark.parametrize('left,right', [(None, None), ('TEST_PLAN_A', 'TEST_PLAN_A'), ('TEST_PLAN_A', 'TEST_PLAN_B')])
def test_comparison_is_not_reinterpreted_as_absolute_or_computed(tmp_path, left, right):
    fields = toy_complete_components(plan_mode='COMPARISON', comparison_left_plan=left,
                                     comparison_right_plan=right, comparison_operation='TEST_SOURCE_REPORTED_DELTA')
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': fields})
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert result.measurements[0].evidence_complete_for_test == (left is not None and left != right)
    assert result.measurements[0].value_kind == 'UNKNOWN'
    assert str(result.lexical.measurements[0].signed_decimal) == '-1.2300'


def test_unclassified_plan_modes_do_not_default_to_absolute_movement(tmp_path):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': toy_complete_components(plan_mode='UNCLASSIFIED_NEW_MODE')})
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert not result.measurements[0].evidence_complete_for_test
    assert 'PLAN_MODE_UNKNOWN_OR_UNSUPPORTED' in result.measurements[0].abstain_reasons
    assert result.measurements[0].value_kind == 'UNKNOWN'


def test_zero_and_duplicate_positions_do_not_gain_unproven_directions(tmp_path):
    raw = 'Tooth\tRotation (deg)\tRot (deg)\n13\t0.00\t0.00'
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'direction': 'TEST_DIRECTION', 'unit': 'deg'}}, raw=raw)
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert components(result)['direction'].status == 'CONFLICT'
    assert components(result)['unit'].status == 'TEST_ONLY'
    assert lexical.measurements[0].numeric_status == 'EXPLICIT_ZERO'
    assert result.measurements[0].canonical_magnitude is None


@pytest.mark.parametrize('path', ['../secret.txt', '/absolute.txt', 'C:\\private.txt', 'https://example.org/input', '\\\\server\\share\\file'])
def test_fixture_paths_cannot_escape_authorized_local_root(tmp_path, path):
    _, record, _ = write_synthetic_fixture(tmp_path)
    hostile = record.model_copy(update={'raw': Artifact(path=path, sha256=record.raw.sha256)})
    with pytest.raises(FixtureVerificationError, match='UNSAFE_ARTIFACT_PATH'):
        verify_fixture(hostile, tmp_path)


@pytest.mark.parametrize('filename', ['synthetic.txt', 'synthetic.expected.json'])
def test_artifact_tampering_fails_without_echoing_input(tmp_path, filename):
    _, record, _ = write_synthetic_fixture(tmp_path)
    (tmp_path / filename).write_text('PRIVATE_TEST_MARKER', encoding='utf-8')
    with pytest.raises(FixtureVerificationError) as captured:
        assert_fixture_matches(record, tmp_path)
    assert str(captured.value) == 'ARTIFACT_HASH_MISMATCH'
    assert 'PRIVATE_TEST_MARKER' not in str(captured.value)


def test_changed_expected_output_requires_independent_oracle_match(tmp_path):
    _, record, _ = write_synthetic_fixture(tmp_path)
    data = json.loads((tmp_path / 'synthetic.expected.json').read_text(encoding='utf-8'))
    data['lexical']['measurements'][0]['signed_decimal'] = '-999.0'
    encoded = json.dumps(data).encode()
    (tmp_path / 'synthetic.expected.json').write_bytes(encoded)
    changed = record.model_copy(update={'expected': Artifact(path='synthetic.expected.json', sha256=sha256(encoded).hexdigest())})
    with pytest.raises(FixtureVerificationError, match='LEXICAL_ORACLE_MISMATCH'):
        verify_fixture(changed, tmp_path)


def test_no_mutated_or_revoked_proof_can_be_used(tmp_path):
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}})
    revoked = EvidenceRegistry(revoked=frozenset({checked.release_digest}))
    assert assess_semantics(lexical, checked, registry=revoked, allow_test_only=True).status == 'DISABLED'
    forged = replace(checked, release_digest='0' * 64)
    assert assess_semantics(lexical, forged, allow_test_only=True).status == 'DISABLED'
    forged = replace(checked, expected_json='{}')
    assert assess_semantics(lexical, forged, allow_test_only=True).status == 'DISABLED'


def test_synthetic_records_cannot_masquerade_as_vendor_evidence(tmp_path):
    _, record, _ = write_synthetic_fixture(tmp_path)
    for overrides in [{'application': 'ClinCheck'}, {'status': 'REVIEWED'}, {'kind': 'AUTHENTIC'}]:
        with pytest.raises(ValidationError):
            FixtureRecord.model_validate({**record.model_dump(), **overrides})
    # Pending real-vendor placeholders are valid but have no proofs, reviews, or expected semantics.
    pending = FixtureRecord(fixture_id='pending', kind='AUTHENTIC', application='ClinCheck')
    with pytest.raises(FixtureVerificationError, match='FIXTURE_NOT_REVIEWED'):
        verify_fixture(pending, tmp_path)
    with pytest.raises(ValidationError):
        FixtureRecord.model_validate({**pending.model_dump(), 'status': 'REVIEWED'})


@pytest.mark.parametrize('fault', ['duplicate_reviewer', 'capture_operator', 'no_orthodontist', 'rejected', 'stale_hash', 'before_capture'])
def test_deliberately_forged_review_claims_cannot_pass_review_gate(fault):
    # Adversarial in-memory metadata only: no authentic capture, review, or gold output is created.
    captured = datetime(2020, 1, 1, tzinfo=timezone.utc)
    review = dict(reviewer_id='TEST_REVIEWER_A', role='ORTHODONTIST', reviewed_at=captured + timedelta(days=1),
                  decision='APPROVE', raw_sha256='0' * 64, expected_sha256='0' * 64, source_evidence_sha256='0' * 64)
    other = {**review, 'reviewer_id': 'TEST_REVIEWER_B', 'role': 'INDEPENDENT_DATA_REVIEWER'}
    if fault == 'duplicate_reviewer': other['reviewer_id'] = review['reviewer_id']
    if fault == 'capture_operator': other['reviewer_id'] = 'TEST_CAPTURE_OPERATOR'
    if fault == 'no_orthodontist': review['role'] = 'INDEPENDENT_DATA_REVIEWER'
    if fault == 'rejected': other['decision'] = 'REJECT'
    if fault == 'stale_hash': other['expected_sha256'] = '1' * 64
    if fault == 'before_capture': other['reviewed_at'] = captured - timedelta(days=1)
    with pytest.raises(ValidationError):
        FixtureRecord(fixture_id='TEST_FORGED_CLAIMS_NOT_EVIDENCE', kind='AUTHENTIC', application='ClinCheck',
                      status='REVIEWED', source_version='TEST_FORGED_NOT_A_VENDOR_VERSION',
                      captured_by='TEST_CAPTURE_OPERATOR', captured_at=captured, consent_ref='TEST_NOT_AUTHORIZATION',
                      deidentification_ref='TEST_NOT_AUTHORIZATION', submission_context=LexicalInput(raw_text=''),
                      raw=Artifact(path='NOT_A_REAL_CAPTURE', sha256='0' * 64),
                      expected=Artifact(path='NOT_A_REAL_GOLD_OUTPUT', sha256='0' * 64),
                      source_evidence=Artifact(path='NOT_A_REAL_SOURCE_EVIDENCE', sha256='0' * 64),
                      reviews=(IndependentReview(**review), IndependentReview(**other)))


@pytest.mark.parametrize('value', ['UNKNOWN', ' unknown ', 'N/A', '?', 'UNVERIFIED'])
def test_unknowns_cannot_be_marked_as_canonical(value):
    with pytest.raises(ValidationError):
        ExpectedComponent(name='direction', value=value, evidence_locator='TEST_ONLY')
    with pytest.raises(ValidationError):
        SemanticComponent(name='direction', status='UNKNOWN', canonical_value='0')


def test_manifest_does_not_embed_captures_or_accept_duplicate_ids():
    record = FixtureRecord(fixture_id='pending', kind='AUTHENTIC', application='SureSmile')
    with pytest.raises(ValidationError):
        FixtureManifest(fixtures=(record, record))
    with pytest.raises(ValidationError):
        FixtureRecord(fixture_id='pending', kind='AUTHENTIC', application='SureSmile',
                      submission_context=LexicalInput(raw_text='DO_NOT_EMBED_CAPTURE'))


def test_offline_parser_input_is_distinct_from_http_confirmation():
    assert parse_table(LexicalInput(raw_text=SYNTHETIC_RAW)).measurements
    with pytest.raises(ValidationError):
        RawTMTSubmission(raw_text=SYNTHETIC_RAW)
    with pytest.raises(ValidationError):
        RawTMTSubmission(raw_text=SYNTHETIC_RAW, synthetic_data_confirmed=False)


def test_cli_no_authentic_samples_reports_not_verified():
    script = Path(__file__).resolve().parents[1] / 'scripts/verify_vendor_fixtures.py'
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=20)
    assert result.returncode == 2
    assert result.stdout.startswith('NO_AUTHENTIC_ORACLES: 0')
    assert result.stderr == ''


def test_new_schemas_match_contracts_and_old_schemas_remain_unchanged():
    directory = Path(__file__).resolve().parents[2] / 'schemas'
    for filename, model, mode in [
        ('vendor-fixture-manifest.v1.json', FixtureManifest, 'validation'),
        ('vendor-fixture-expected.v1.json', FixtureExpectedOutput, 'serialization'),
        ('semantic-assessment.v1.json', SemanticAssessment, 'serialization'),
    ]:
        assert json.loads((directory / filename).read_text(encoding='utf-8')) == model.model_json_schema(mode=mode)
    # Compare the original complete contracts independent of Git's platform newline conversion.
    assert digest_json(json.loads((directory / 'parse-request.v1.json').read_text(encoding='utf-8'))) == '25034f1cabeaabf46a09da8d7af932afb030310b088edd864cc184a965c6bd61'
    assert digest_json(json.loads((directory / 'parse-result.v1.json').read_text(encoding='utf-8'))) == '9d5d94e9d64736889f56f05c40f9db71fc6d7b6ac60576c358e7e2e533332a14'


def test_assessment_does_not_write_or_transmit_or_log_inputs(tmp_path, monkeypatch, caplog):
    import builtins
    import socket
    caplog.set_level('DEBUG')
    lexical, _, checked = write_synthetic_fixture(tmp_path, {'measurement-1': {'unit': 'deg'}})
    def forbidden(*args, **kwargs): raise AssertionError('Unexpected I/O')
    monkeypatch.setattr(builtins, 'open', forbidden)
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    result = assess_semantics(lexical, checked, allow_test_only=True)
    assert len(result.measurements[0].components) == len(COMPONENTS)
    assert SYNTHETIC_RAW not in caplog.text
