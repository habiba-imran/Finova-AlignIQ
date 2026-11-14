"""Fixed authored decisions; not an attachment decision engine or public evidence importer."""
from hashlib import sha256
from pathlib import Path

from app.attachments.models import AttachmentDemoInput, SyntheticScenario
from app.attachments.service import assemble
from app.planning.demo import CONVENTION, demo_input, fixed_input
from app.parser.receipts import resolve
from app.review.service import review_table

ROOT = Path(__file__).with_name("fixtures")


def input_demo():
    source = demo_input()
    return AttachmentDemoInput(context=source.context, parsed=source.parsed, convention=CONVENTION + (
        "FINOVA-ATTACHMENTS-1 supplies independently authored fictional choices. They are not inferred from movements and are not approved clinical policies.",
        "DEMO_TILE IDs and toy prism/oval labels are original illustrative categories, not a commercial attachment library. Any dimensions, orientation, surface and stage labels are supplied TEST_ONLY data, not validated placement.",
        "The no-attachment entry is an explicit supplied synthetic decision. Unknown/withheld entries do not mean no attachment. No schedule or stage recommendation is produced.",))


def draft_demo():
    submission, checked = fixed_input()
    data = (ROOT / "scenario.json").read_bytes()
    expected_hash = (ROOT / "scenario.sha256").read_text(encoding="ascii").strip()
    if sha256(data).hexdigest() != expected_hash:
        raise ValueError("SYNTHETIC_SCENARIO_HASH_MISMATCH")
    scenario = SyntheticScenario.model_validate_json(data)
    parsed = resolve(submission)
    review = review_table(submission, requested_assessments=("ATTACHMENTS",), checked=checked, test_only=True)
    return assemble(parsed, review, scenario=scenario, evidence_ref=f"{scenario.scenario_id}:{expected_hash}")
