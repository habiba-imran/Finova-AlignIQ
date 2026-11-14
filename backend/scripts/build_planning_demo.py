"""Rebuild only checked-in invented demonstration assets. Never runs on HTTP requests."""
import sys
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from app.domain.models import LexicalInput, SourceContext
from app.parser.service import parse_table
from app.semantics.models import Artifact, ExpectedComponent, ExpectedMeasurement, FixtureExpectedOutput, FixtureRecord

ROOT = Path(__file__).parents[1] / "app/planning/fixtures"
RAW = "# Finova Synthetic Demonstration — TEST_ONLY, no patient or vendor\nTooth\tRotation (deg)\tExtrusion (mm)\tMesiodistal (mm)\tBuccolingual (mm)\n11\t-\t-\t1.2300 D\t-\n12\t-\t-\t-\t0.4500 B\n13\t-\t0.200 E\t-\t-\n14\t2.500 M\t-\t-\t-\n15\t3.000 M\t-\t-\t-\n"
# Independently defined synthetic semantics, not inferred from lexical labels.
ASSERTIONS = (
    ("measurement-3", "DEMO_11", "MESIODISTAL", "mm", "DISTAL"),
    ("measurement-8", "DEMO_12", "BUCCOLINGUAL", "mm", "BUCCAL"),
    ("measurement-10", "DEMO_13", "EXTRUSION", "mm", "EXTRUSION"),
    ("measurement-13", "DEMO_14", "ROTATION", "deg", "DEMO_ROTATION_M"),
)


def build():
    context = SourceContext(source_version="FINOVA-DEMO-1")
    lexical = parse_table(LexicalInput(raw_text=RAW, context=context))
    measurements = []
    for mid, tooth, axis, unit, direction in ASSERTIONS:
        values = dict(source_application="TEST_ONLY", source_version="FINOVA-DEMO-1",
            tooth_identifier=tooth, notation="FINOVA_OPAQUE", dentition="SYNTHETIC", arch="DEMO_ARCH",
            axis=axis, unit=unit, sign="UNSIGNED_EXPLICIT_DIRECTION", direction=direction,
            plan_mode="TEST_PLAN_MODE", reference_basis="DEMO_CROWN_POINT", scope="TOTAL",
            coordinate_frame="FINOVA_LOCAL_AXES_V1")
        measurements.append(ExpectedMeasurement(measurement_id=mid, components=tuple(
            ExpectedComponent(name=k, value=v, evidence_locator=f"FINOVA-SYNTHETIC-1:{mid}:{k}") for k, v in values.items())))
    expected = FixtureExpectedOutput(kind="SYNTHETIC", lexical=lexical, measurements=tuple(measurements))
    raw_bytes, expected_bytes = RAW.encode("utf-8"), expected.model_dump_json(indent=2).encode("utf-8")
    record = FixtureRecord(fixture_id="FINOVA-SYNTHETIC-1", kind="SYNTHETIC", application="TEST_ONLY",
        source_version="FINOVA-DEMO-1", status="TEST_ONLY",
        raw=Artifact(path="table.txt", sha256=sha256(raw_bytes).hexdigest()),
        expected=Artifact(path="expected.json", sha256=sha256(expected_bytes).hexdigest()),
        submission_context=LexicalInput(raw_text="", context=context))
    ROOT.mkdir(exist_ok=True)
    (ROOT / "table.txt").write_bytes(raw_bytes)
    (ROOT / "expected.json").write_bytes(expected_bytes)
    (ROOT / "record.json").write_text(record.model_dump_json(indent=2), encoding="utf-8")
    print("Fixed TEST_ONLY demonstration artifacts rebuilt; no vendor release or clinical policy changed.")


if __name__ == "__main__":
    build()
    if "--frontend-fixtures" in sys.argv:
        from app.planning.demo import demo_input, demo_report
        output = ROOT.parents[3] / "frontend/src/test/fixtures"
        (output / "planning-demo-input.json").write_text(demo_input().model_dump_json(indent=2), encoding="utf-8")
        (output / "planning-demo-draft.json").write_text(demo_report("TEMPLATES").model_dump_json(indent=2), encoding="utf-8")
