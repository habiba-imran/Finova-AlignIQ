import re

from app.domain.models import AdapterInfo, LexicalInput, ParseIssue, RawCell, SourceInfo
from app.parser.adapters.clincheck import CLINCHECK
from app.parser.adapters.suresmile import SURESMILE
from app.parser.tokenize import Line

ADAPTERS = {adapter.platform: adapter for adapter in (CLINCHECK, SURESMILE)}


def source_info(submission: LexicalInput, source_lines: list[Line]) -> tuple[SourceInfo, list[ParseIssue], set[int]]:
    detected = []
    evidence = []
    signature_lines = set()
    for line in source_lines:
        match = re.fullmatch(r"\s*Source\s*:\s*(ClinCheck|SureSmile)\s*", line.text, re.IGNORECASE)
        if match:
            platform = next(name for name in ADAPTERS if name.lower() == match[1].lower())
            if platform not in detected:
                detected.append(platform)
            signature_lines.add(line.number)
            evidence.append(RawCell(raw=line.text, span=line.span))
    selected = submission.source_claim
    candidate = ADAPTERS.get(selected) if selected != "Unknown" else (ADAPTERS.get(detected[0]) if len(detected) == 1 else None)
    issues = [ParseIssue(code="SOURCE_UNVERIFIED", severity="WARNING", field="source",
                         message="No authentic clipboard fixtures have verified any vendor adapter. Results are lexical only.")]
    if len(detected) > 1 or (selected != "Unknown" and any(p != selected for p in detected)):
        issues.append(ParseIssue(code="SOURCE_CLAIM_CONFLICT", severity="ERROR", field="source_claim",
                                 message="The selected source and/or explicit source lines conflict. No source is verified."))
    if candidate:
        issues.append(ParseIssue(code="SOURCE_VERSION_UNVERIFIED", severity="WARNING", field="source_version",
                                 message="This candidate has no verified source versions; it cannot normalize vendor conventions."))
        for field in candidate.context_conflicts(submission.context):
            issues.append(ParseIssue(code="SOURCE_CONTEXT_CONFLICT", severity="ERROR", field=field,
                                     message="The claimed context is incompatible with the selected source's audited feature definitions."))
    context = submission.context
    if context.scope in {"CUMULATIVE", "INCREMENTAL"} and context.stage_index is None:
        issues.append(ParseIssue(code="STAGE_REQUIRED", severity="WARNING", field="stage_index",
                                 message="A stage identifier is needed to describe this claimed movement scope."))
    if context.scope == "TOTAL" and context.stage_index is not None:
        issues.append(ParseIssue(code="TOTAL_STAGE_NOT_EQUIVALENT", severity="WARNING", field="scope",
                                 message="A stage identifier does not make total and incremental/cumulative values equivalent."))
    if context.plan_mode == "COMPARISON":
        issues.append(ParseIssue(code="COMPARISON_NOT_ABSOLUTE", severity="WARNING", field="plan_mode",
                                 message="Comparison values are not an absolute prescription; no plan subtraction is performed."))
    return SourceInfo(source_claim=selected, detected_claims=detected, claim_evidence=evidence,
                      adapter=AdapterInfo(id="generic-lexical-grid", version="0.1.0"),
                      candidate_adapter=candidate.info() if candidate else None, context=context), issues, signature_lines
