from hashlib import sha256
from pathlib import Path

from app.parser.receipts import resolve
from app.planning.demo import CONVENTION, demo_input, fixed_input
from app.review.context import TestRuleContext, input_digest
from app.review.service import review_table
from app.sequencing.models import SequencingDemoInput, SequencingScenario
from app.sequencing.service import assemble

ROOT = Path(__file__).with_name("fixtures")


def input_demo():
    source = demo_input()
    return SequencingDemoInput(context=source.context, parsed=source.parsed, convention=CONVENTION + (
        "FINOVA-NANO-1: SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE. All sequencing and anchorage statements are supplied fictional content.",
        "DEMO_UPPER/DEMO_LOWER, segments and sides are independently authored scenario identities, not anatomy inferred from opaque source tokens. The engine's original DEMO_ARCH evidence is unchanged.",
        "Separate fictional stage records contain IDs, indices and kinds only. They have no stage-bound movement values; TOTAL TMT does not supply a schedule, stage allocation or force plan.",
        "G15 checks supplied metadata only; N07 remains not applicable to TOTAL movement values. No sum, composition or clinical rule executes.",))


def fixed_scenario():
    data = (ROOT / "scenario.json").read_bytes()
    digest = (ROOT / "scenario.sha256").read_text(encoding="ascii").strip()
    if sha256(data).hexdigest() != digest:
        raise ValueError("SEQUENCING_SCENARIO_HASH_MISMATCH")
    return SequencingScenario.model_validate_json(data), digest


def draft_demo():
    submission, checked = fixed_input()
    scenario, digest = fixed_scenario()
    parsed = resolve(submission)
    if parsed.raw_sha256 != scenario.input_sha256:
        raise ValueError("SEQUENCING_SCENARIO_INPUT_MISMATCH")
    context = TestRuleContext(input_digest=input_digest(submission), stages=scenario.stages)
    review = review_table(submission, checked=checked, test_only=True, test_context=context,
        requested_assessments=("COLLISIONS", "COMPLEX_INTERVENTION"))
    return assemble(parsed, review, scenario=scenario, evidence_ref=f"{scenario.scenario_id}:{digest}")
