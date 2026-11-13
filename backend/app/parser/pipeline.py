"""Deterministic-first intake, with an explicitly requested certified synthetic fallback."""

from app.domain.models import RawTMTSubmission
from app.parser.certification import certify_markdown, structural_prompt, validate_proposal
from app.parser.cloud import ParserSettings, load_parser_settings
from app.parser.contracts import Assistance, AssistedSubmission, AutomaticParseResult, PipelineInfo, StructuralProposal
from app.parser.detection import clarifications, detect_source
from app.parser.service import parse_table
from app.parser.synthetic import cloud_example_allowed
from app.reports.groq_client import GroqClient


def automatic_parse(submission: RawTMTSubmission, *, assisted: bool = False,
                    settings: ParserSettings | None = None, client: GroqClient | None = None) -> AutomaticParseResult:
    lexical = parse_table(submission)
    info = Assistance()
    # No network call on normal intake, including layouts that could be certified.
    try:
        settings = settings or load_parser_settings()
    except ValueError:
        info.reason = "PARSER_CONFIGURATION_INVALID"
        settings = ParserSettings()
    else:
        info.reason = "READY_FOR_EXPLICIT_CONSENT" if settings.configured else "CLOUD_DISABLED"
    needs_fallback = not lexical.measurements and lexical.status in {"UNSUPPORTED", "INVALID"}
    certificate = certify_markdown(submission.raw_text) if needs_fallback and len(submission.raw_text) <= 8_000 else None
    allowed = cloud_example_allowed(submission.raw_text)
    info.available = settings.configured and needs_fallback and certificate is not None and allowed
    if settings.configured and not info.available:
        info.reason = "DETERMINISTIC_RESULT_AVAILABLE" if not needs_fallback else "SYNTHETIC_CATALOG_ONLY" if not allowed else "STRUCTURE_NOT_CERTIFIABLE"
    if assisted:
        # Library calls, like HTTP, must carry actual affirmative consent.
        if not isinstance(submission, AssistedSubmission) or submission.cloud_synthetic_consent is not True:
            info.status, info.reason = "BLOCKED", "CLOUD_CONSENT_REQUIRED"
        elif not info.available:
            info.status = "BLOCKED"
        else:
            schema = {"type": "json_schema", "json_schema": {"name": "finova_structure_v1", "strict": True,
                      "schema": StructuralProposal.model_json_schema(mode="validation")}}
            response = (client or GroqClient(settings)).generate(structural_prompt(certificate), response_schema=schema)
            info.attempts, info.reason = response.attempts, response.code
            info.status = "FAILED"
            if response.content is not None:
                if validate_proposal(response.content, certificate):
                    lexical = parse_table(submission, certified_layout=certificate.layout, certified_rows=certificate.rows,
                                          separator_lines=frozenset({certificate.separator_line}))
                    info.status, info.reason = "ACCEPTED", "ALL_CELL_ASSOCIATIONS_CERTIFIED"
                    info.certificate, info.origin = "MARKDOWN_PIPE_V1", "GROQ_PROPOSAL_CERTIFIED"
                else:
                    info.status, info.reason = "REJECTED", "PROPOSAL_ASSOCIATIONS_INVALID"
    detected = detect_source(lexical)
    return AutomaticParseResult(**lexical.model_dump(), pipeline=PipelineInfo(
        detection=detected, assistance=info, clarifications=clarifications(lexical, detected)))
