"""Write only fixed fictional Nano assets; never calculate treatment strategies."""
import sys
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from app.parser.receipts import resolve
from app.planning.demo import fixed_input
from app.review.context import StageRecord
from app.sequencing.models import FictionalArch, FictionalSegment, ScenarioStatement, SequencingScenario, StageWindow


def build():
    submission, _ = fixed_input()
    scenario = SequencingScenario(input_sha256=resolve(submission).raw_sha256,
        arches=(FictionalArch(arch_id="DEMO_UPPER", label="Fictional upper arch", role="UPPER"), FictionalArch(arch_id="DEMO_LOWER", label="Fictional lower arch", role="LOWER")),
        segments=(FictionalSegment(segment_id="DEMO_U_A", label="Fictional upper segment A", arch_id="DEMO_UPPER", side="RIGHT", tooth_refs=("tooth-1",)),
                  FictionalSegment(segment_id="DEMO_U_B", label="Fictional upper segment B", arch_id="DEMO_UPPER", side="LEFT", tooth_refs=("tooth-2",)),
                  FictionalSegment(segment_id="DEMO_L_A", label="Fictional lower segment A", arch_id="DEMO_LOWER", side="RIGHT", tooth_refs=("tooth-3",)),
                  FictionalSegment(segment_id="DEMO_L_B", label="Fictional lower segment B", arch_id="DEMO_LOWER", side="LEFT", tooth_refs=("tooth-4",))),
        stages=tuple(StageRecord(stage_id=sid, index=index, arch=arch, kind=kind, evidence_ref=f"FINOVA-NANO-1:stages/{sid}") for sid, index, arch, kind in (
            ("DEMO_U_BASE", 0, "DEMO_UPPER", "BASELINE"), ("DEMO_U_A_RECORD", 1, "DEMO_UPPER", "ACTIVE"), ("DEMO_U_B_RECORD", 2, "DEMO_UPPER", "ACTIVE"),
            ("DEMO_L_BASE", 0, "DEMO_LOWER", "BASELINE"), ("DEMO_L_RECORD", 1, "DEMO_LOWER", "PASSIVE"))),
        statements=(
            ScenarioStatement(key="upper", section="UPPER_ARCH", arch_id="DEMO_UPPER", stage_window=StageWindow(start_id="DEMO_U_BASE", end_id="DEMO_U_B_RECORD"), text="Supplied fictional upper-arch example: segment U-A is listed before U-B in the authored illustration. This order is not calculated from TMT totals and is not a treatment recommendation."),
            ScenarioStatement(key="lower", section="LOWER_ARCH", arch_id="DEMO_LOWER", stage_window=StageWindow(start_id="DEMO_L_BASE", end_id="DEMO_L_RECORD"), text="Supplied fictional lower-arch example: a separate passive record is listed after its baseline. No movement timing, stage allocation or clinical adequacy follows from this example."),
            ScenarioStatement(key="segment-a", section="SEGMENTS", arch_id="DEMO_UPPER", segment_id="DEMO_U_A", side="RIGHT", stage_window=StageWindow(start_id="DEMO_U_A_RECORD", end_id="DEMO_U_A_RECORD"), text="Supplied fictional segment U-A note: this segment is associated with the scenario's U-A record. No displacement is allocated to that record."),
            ScenarioStatement(key="segment-b", section="SEGMENTS", arch_id="DEMO_UPPER", segment_id="DEMO_U_B", side="LEFT", stage_window=StageWindow(start_id="DEMO_U_B_RECORD", end_id="DEMO_U_B_RECORD"), text="Supplied fictional segment U-B note: its authored record follows U-A. The application does not choose this order or infer it from movement magnitude."),
            ScenarioStatement(key="right", section="RIGHT_ANCHORAGE", arch_id="DEMO_UPPER", side="RIGHT", text="Supplied fictional right-side anchorage note: the scenario records a separate right-side context for review. No force, device, auxiliary or anchorage requirement is specified."),
            ScenarioStatement(key="left", section="LEFT_ANCHORAGE", arch_id="DEMO_LOWER", side="LEFT", text="Supplied fictional left-side anchorage note: the scenario records a separate left-side context for review. Missing clinical information is not a finding that anchorage is unnecessary."),
        ))
    root = Path(__file__).parents[1] / "app/sequencing/fixtures"
    root.mkdir(exist_ok=True)
    data = scenario.model_dump_json(indent=2).encode("utf-8")
    (root / "scenario.json").write_bytes(data)
    (root / "scenario.sha256").write_text(sha256(data).hexdigest() + "\n", encoding="ascii")
    if "--frontend-fixtures" in sys.argv:
        from app.sequencing.demo import input_demo, draft_demo
        from app.sequencing.models import SequencingSubmission
        from app.sequencing.service import sequencing_review
        output = root.parents[3] / "frontend/src/test/fixtures"
        for name, result in (("sequencer-demo-input", input_demo()), ("sequencer-demo-draft", draft_demo()),
            ("sequencer-unverified-draft", sequencing_review(SequencingSubmission.model_validate(submission.model_dump())))):
            (output / f"{name}.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")
    print("Fixed fictional Nano scenario written; no clinical sequencing policy or vendor mapping changed.")


if __name__ == "__main__":
    build()
