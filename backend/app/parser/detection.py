"""Source indicators are hypotheses, never semantic evidence or selected adapters."""

import re

from app.domain.models import ParseResult, RawCell
from app.parser.contracts import Clarification, Detection, SourceIndicator
from app.parser.tokenize import lines


def detect_source(result: ParseResult) -> Detection:
    source_lines = lines(result.raw_text)
    indicators = []
    for platform in ("ClinCheck", "SureSmile"):
        evidence = [RawCell(raw=line.text, span=line.span) for line in source_lines
                    if re.search(r"\b" + platform + r"\b", line.text, re.IGNORECASE)]
        if evidence:
            indicators.append(SourceIndicator(candidate=platform, kind="EXPLICIT_BRAND", evidence=evidence))
    # Require co-occurring distinctive UI terms, not generic rotation/FDI headers.
    signatures = {
        "ClinCheck": (r"\bAlign\s+Final\b", r"\bDoctor\s+Final\b"),
        "SureSmile": (r"\bDisplacement\s+Type\b", r"\bCusp\s+Tip\b"),
    }
    for platform, patterns in signatures.items():
        matches = [[line for line in source_lines if re.search(pattern, line.text, re.IGNORECASE)] for pattern in patterns]
        if all(matches):
            evidence = {line.number: RawCell(raw=line.text, span=line.span) for group in matches for line in group}
            indicators.append(SourceIndicator(candidate=platform, kind="DOCUMENTED_SIGNATURE", evidence=list(evidence.values())))
    candidates = {i.candidate for i in indicators}
    notation = set()
    for tooth in result.teeth:
        value = tooth.token
        if re.fullmatch(r"[1-4][1-8]|[5-8][1-5]", value): notation.add("FDI_SYNTAX")
        if re.fullmatch(r"[1-9]|[12][0-9]|3[0-2]|[A-T]", value): notation.add("UNIVERSAL_SYNTAX")
        if re.fullmatch(r"(?:UR|UL|LR|LL)[1-8]|[1-8][┘└┐┌]", value, re.IGNORECASE): notation.add("QUADRANT_TOKEN_SYNTAX")
    return Detection(detected_source=next(iter(candidates)) if len(candidates) == 1 else "Unknown",
                     status="CONFLICT" if len(candidates) > 1 else "DETECTED_UNVERIFIED" if candidates else "UNKNOWN",
                     indicators=indicators, notation_candidates=sorted(notation),
                     layout_recognized=result.layout.orientation != "UNKNOWN")


def clarifications(result: ParseResult, detection: Detection) -> list[Clarification]:
    context = result.source.context
    messages = {
        "source_verification": "Authentic independently reviewed clipboard evidence is required; a detected indicator is not vendor verification.",
        "source_version": "Provide the exact source application/build/version with capture evidence.",
        "notation": "Confirm the numbering system and quadrant/arch context; numeric tooth tokens may fit multiple systems.",
        "dentition": "Confirm permanent, primary or mixed dentition from source evidence.",
        "arch": "Confirm the source arch; no arch is inferred from unknown numbering.",
        "plan_mode": "Identify original/final/comparison mode; comparison needs operand plans and the source-defined operation.",
        "reference_basis": "Confirm the reference point for each field (crown, root, cusp, bracket or other); bases are not interchangeable.",
        "scope": "Confirm total/cumulative/incremental scope and any stage identifiers/kinds; a setup revision is not an aligner stage.",
        "coordinate_frame": "Provide the source coordinate frame and independently verified sign/direction conventions.",
    }
    items = [Clarification(code="SOURCE_EVIDENCE_REQUIRED", field="source_verification", message=messages["source_verification"])]
    if detection.status == "CONFLICT":
        items.append(Clarification(code="SOURCE_INDICATORS_CONFLICT", field="source", message="Conflicting source indicators were found. No platform was chosen."))
    for field, message in messages.items():
        if field != "source_verification" and getattr(context, field, None) in {None, "UNKNOWN"}:
            items.append(Clarification(code="METADATA_REQUIRED", field=field, message=message))
    if not detection.layout_recognized or any(i.code == "ROW_ALIGNMENT_UNRESOLVED" for i in result.issues):
        items.append(Clarification(code="STRUCTURE_REQUIRED", field="layout", message="Provide explicit complete row/column delimiters. Ambiguous alignment cannot be reconstructed by guessing."))
    # Preserve field-specific warnings without manufacturing metadata from detected text.
    for issue in result.issues:
        if issue.measurement_ids or issue.severity == "ERROR":
            items.append(Clarification(code=issue.code, field=issue.field or "layout",
                                       measurement_ids=issue.measurement_ids, message=issue.message))
    return items
