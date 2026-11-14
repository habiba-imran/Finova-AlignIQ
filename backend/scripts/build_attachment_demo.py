"""Author fixed illustrative decisions. Does not derive indications from movements."""
import sys
from hashlib import sha256
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from app.attachments.models import AttachmentDesign, Dimensions, Placement, ScenarioRow, SyntheticScenario
from app.planning.demo import fixed_input
from app.parser.receipts import resolve


def build():
    submission, _ = fixed_input()
    # The explicit choices below are independently authored fictional inputs, not policies.
    # Tokens/IDs match the earlier fixed synthetic evidence, not vendor tooth anatomy.
    scenario = SyntheticScenario(input_sha256=resolve(submission).raw_sha256, rows=(
        ScenarioRow(key="candidate-a", tooth_ref="tooth-1", synthetic_tooth="DEMO_11", result_type="CANDIDATE",
            design=AttachmentDesign(design_id="DEMO_TILE_A", category_id="FINOVA_ILLUSTRATIVE_TILE", label="Illustrative tile A",
                shape="DEMO_PRISM", dimensions=Dimensions(x=Decimal("2.000"), y=Decimal("1.250"), z=Decimal("0.500")), orientation="DEMO_LONG_AXIS"),
            placement=Placement(surface_id="DEMO_SURFACE_A", frame_id="DEMO_SCHEMATIC_V1", stage_ref="DEMO_WINDOW_A")),
        ScenarioRow(key="alternative-b", tooth_ref="tooth-1", synthetic_tooth="DEMO_11", result_type="ALTERNATIVE", alternative_key="candidate-a",
            design=AttachmentDesign(design_id="DEMO_TILE_B", category_id="FINOVA_ILLUSTRATIVE_TILE", label="Illustrative tile B", shape="DEMO_OVAL")),
        ScenarioRow(key="candidate-c", tooth_ref="tooth-2", synthetic_tooth="DEMO_12", result_type="CANDIDATE",
            design=AttachmentDesign(design_id="DEMO_TILE_C", category_id="FINOVA_ILLUSTRATIVE_TILE", label="Illustrative tile C")),
        ScenarioRow(key="supplied-none", tooth_ref="tooth-3", synthetic_tooth="DEMO_13", result_type="NOT_INDICATED"),
        ScenarioRow(key="unknown", tooth_ref="tooth-4", synthetic_tooth="DEMO_14", result_type="UNKNOWN"),
        ScenarioRow(key="withheld", tooth_ref="tooth-5", synthetic_tooth=None, result_type="WITHHELD"),
    ))
    root = Path(__file__).parents[1] / "app/attachments/fixtures"
    root.mkdir(exist_ok=True)
    data = scenario.model_dump_json(indent=2).encode("utf-8")
    (root / "scenario.json").write_bytes(data)
    (root / "scenario.sha256").write_text(sha256(data).hexdigest() + "\n", encoding="ascii")
    if "--frontend-fixtures" in sys.argv:
        from app.attachments.demo import input_demo, draft_demo
        output = root.parents[3] / "frontend/src/test/fixtures"
        (output / "attachment-demo-input.json").write_text(input_demo().model_dump_json(indent=2), encoding="utf-8")
        (output / "attachment-demo-draft.json").write_text(draft_demo().model_dump_json(indent=2), encoding="utf-8")
        from app.attachments.models import AttachmentSubmission
        from app.attachments.service import attachment_review
        ordinary = AttachmentSubmission.model_validate(submission.model_dump())
        (output / "attachment-unverified-draft.json").write_text(attachment_review(ordinary).model_dump_json(indent=2), encoding="utf-8")
    print("Fixed TEST_ONLY attachment scenario generated; no clinical policy or vendor mapping changed.")


if __name__ == "__main__":
    build()
