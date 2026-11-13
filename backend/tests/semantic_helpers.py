"""Neutral synthetic mechanics only. Never a ClinCheck/SureSmile oracle or human review."""

from hashlib import sha256
from pathlib import Path

from app.domain.models import LexicalInput, SourceContext
from app.parser.service import parse_table
from app.semantics.fixtures import verify_fixture
from app.semantics.models import Artifact, ExpectedComponent, ExpectedMeasurement, FixtureExpectedOutput, FixtureRecord

SYNTHETIC_RAW = '# SYNTHETIC TEST_ONLY — no vendor semantics\r\nTooth\tRotation (deg)\tExtrusion (mm)\r\n13\t−1.2300 M\t0.00 E\r\n'


def write_synthetic_fixture(root: Path, assertions=None, *, raw=SYNTHETIC_RAW, context=None):
    """Only tests write invented tmp_path assets. Production verifier is read-only."""
    context = context or SourceContext(source_version="TEST_ONLY-1")
    submission = LexicalInput(raw_text=raw, context=context)
    lexical = parse_table(submission)
    expected = FixtureExpectedOutput(
        kind="SYNTHETIC", lexical=lexical,
        measurements=tuple(ExpectedMeasurement(measurement_id=key, components=tuple(
            ExpectedComponent(name=name, value=value, evidence_locator=f"TEST_ONLY:{key}:{name}")
            if value is not None else ExpectedComponent(name=name)
            for name, value in values.items())) for key, values in (assertions or {}).items()),
    )
    raw_bytes, expected_bytes = raw.encode('utf-8'), expected.model_dump_json(indent=2).encode('utf-8')
    (root / 'synthetic.txt').write_bytes(raw_bytes)
    (root / 'synthetic.expected.json').write_bytes(expected_bytes)
    record = FixtureRecord(fixture_id="TEST_ONLY-fixture", kind="SYNTHETIC", application="TEST_ONLY", status="TEST_ONLY",
                           source_version="TEST_ONLY-1", raw=Artifact(path="synthetic.txt", sha256=sha256(raw_bytes).hexdigest()),
                           expected=Artifact(path="synthetic.expected.json", sha256=sha256(expected_bytes).hexdigest()),
                           submission_context=LexicalInput(raw_text="", context=context))
    return lexical, record, verify_fixture(record, root)


def toy_complete_components(**overrides):
    """Opaque toy IDs/axes/directions; no dental identity or vendor mapping is invented."""
    return {
        'source_application': 'TEST_ONLY', 'source_version': 'TEST_ONLY-1',
        'tooth_identifier': 'TEST_TOOTH_ALPHA', 'notation': 'TEST_NOTATION', 'dentition': 'TEST_DENTITION',
        'arch': 'TEST_ARCH', 'axis': 'TEST_AXIS_ALPHA', 'unit': 'deg', 'sign': 'TEST_SIGN_ALPHA',
        'direction': 'TEST_DIRECTION_ALPHA', 'plan_mode': 'TEST_PLAN_MODE', 'reference_basis': 'TEST_REFERENCE_A',
        'scope': 'TOTAL', 'coordinate_frame': 'TEST_FRAME_A', **overrides,
    }
