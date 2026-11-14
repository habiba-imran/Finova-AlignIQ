"""Read-only exact synthetic oracle. Never accepts a user-supplied table or authority."""
from pathlib import Path

from app.domain.models import RawTMTSubmission
from app.parser.contracts import PipelineSubmission
from app.parser.phase4 import parse_pipeline
from app.planning.models import DemoInput, PlanningDraft
from app.planning.service import organize
from app.reports.models import CommentMode
from app.reports.service import generate_report
from app.semantics.fixtures import verify_fixture
from app.semantics.models import FixtureRecord

ROOT = Path(__file__).with_name("fixtures")
CONVENTION = (
    "Invented Finova convention FINOVA-DEMO-1, TEST_ONLY. Not ClinCheck, SureSmile or clinical evidence.",
    "Tokens 11–15 are opaque demonstration identities DEMO_11–DEMO_15, not FDI or Universal teeth. DEMO_ARCH has no anatomical claim.",
    "Linear units mm; rotation deg. Local synthetic point DEMO_CROWN_POINT and frame FINOVA_LOCAL_AXES_V1; no root geometry.",
    "For this fixed synthetic convention only: mesiodistal descriptions appear under Sagittal, buccolingual under Transverse, extrusion under Vertical. Rotation and mixed summaries remain Other. These are not dimensional clinical assessments.",
    "Unsigned magnitudes use explicit directions: D=distal, B=buccal, E=extrusion; M for rotation is the opaque DEMO_ROTATION_M direction. No mirrored-sign inference.",
    "Mode TEST_PLAN_MODE; TOTAL programmed movements only. No stages, achieved movement or treatment strategy. Dashes are missing, never zero.",
    "Token 15 deliberately lacks semantic evidence. Its findings abstain independently of the four authorized demonstration values.",
)


def fixed_input():
    record = FixtureRecord.model_validate_json((ROOT / "record.json").read_bytes())
    checked = verify_fixture(record, ROOT)
    # The checked fixed artifact is the only source. No browser text is compared/promoted.
    raw = (ROOT / record.raw.path).read_bytes().decode("utf-8")
    submission = RawTMTSubmission(raw_text=raw, synthetic_data_confirmed=True,
                                 context=record.submission_context.context)
    return submission, checked


def demo_input() -> DemoInput:
    submission, _ = fixed_input()
    parsed = parse_pipeline(PipelineSubmission.model_validate(submission.model_dump()))
    return DemoInput(convention=CONVENTION, context=submission.context, parsed=parsed)


def demo_report(mode: CommentMode) -> PlanningDraft:
    submission, checked = fixed_input()
    return organize(generate_report(submission, mode=mode, checked=checked, test_only=True))
