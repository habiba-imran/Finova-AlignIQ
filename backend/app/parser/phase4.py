"""Generic deterministic extraction -> quality gate -> authorized recovery -> lexical result."""

import re

from app.domain.models import ParseIssue
from app.parser.certification import certify_markdown
from app.parser.cloud import ParserSettings, load_parser_settings
from app.parser.contracts import Assistance, AutomaticParseResult, PipelineInfo, PipelineSubmission, QualityAssessment
from app.parser.detection import clarifications, detect_source
from app.parser.generated import authorized
from app.parser.receipts import issue
from app.parser.recovery import assemble, prompt, prove, validate, response_schema
from app.parser.service import parse_table
from app.reports.groq_client import GroqClient
from app.parser.values import parse_value


def deterministic(submission):
    result=parse_table(submission)
    if not result.measurements and len(submission.raw_text)<=8_000:
        cert=certify_markdown(submission.raw_text)
        if cert:
            return parse_table(submission,certified_layout=cert.layout,certified_rows=cert.rows,separator_lines=frozenset({cert.separator_line}))
    return result


def quality(raw,result,proofs):
    hostile=bool(re.search(r'<\s*(?:script|html|iframe|img)\b|\b(?:ignore (?:all |previous )?(?:instructions|safeguards)|send secrets)\b',raw,re.I))
    movement=bool(re.search(r'rotation|extrusion|intrusion|inclination|angulation|translation|buccolingual|mesiodistal|\brot\b',raw,re.I)) or bool(result.measurements) or bool(proofs.associations)
    tooth=bool(re.search(r'\b(?:tooth|teeth|movement)\b',raw,re.I)) or bool(result.teeth)
    known={m.span.start for m in result.measurements if m.span}
    new=[a for a in proofs.associations if proofs.cells[a[2]].span.start not in known]
    if hostile or not raw.strip() or not tooth: status='NOT_TMT'
    elif not movement: status='UNSUPPORTED_FORMAT'
    elif new: status='PARTIAL' if result.measurements else 'RECOVERABLE_STRUCTURE'
    elif result.measurements: status='PARTIAL' if any(i.code in {'ROW_ALIGNMENT_UNRESOLVED','SHORT_DELIMITED_ROW'} for i in result.issues) else 'STRUCTURALLY_RECOGNIZED'
    elif result.layout.orientation!='UNKNOWN' or re.search(r'\d',raw): status='AMBIGUOUS_STRUCTURE'
    else: status='UNSUPPORTED_FORMAT'
    viable=any(parse_value('candidate','tooth',proofs.cells[a[1]],proofs.cells[a[2]],result.source.context.decimal_separator)[0].numeric_status
               in {'PARSED','EXPLICIT_ZERO','MISSING'} for a in new)
    return {'classification':status,'recoverable_associations':len(new),'unresolved_lines':sorted(proofs.unresolved_lines),
            'cloud_candidate':bool(new) and viable and not hostile and status!='NOT_TMT'}


def parse_pipeline(submission: PipelineSubmission, *, settings=None, client=None):
    lexical=deterministic(submission)
    proofs=prove(submission.raw_text)
    q=quality(submission.raw_text,lexical,proofs)
    info=Assistance()
    receipt=None
    try: settings=settings or load_parser_settings()
    except ValueError:
        settings=ParserSettings(); info.reason='PARSER_CONFIGURATION_INVALID'
    is_authorized=authorized(submission.raw_text,submission.synthetic_fixture)
    if not q['cloud_candidate']: info.reason='NO_PROVABLE_STRUCTURAL_GAP'
    elif not is_authorized: info.reason='GENERATED_SYNTHETIC_AUTHORIZATION_REQUIRED'
    elif not settings.configured: info.reason='CLOUD_DISABLED'
    else:
        info.reason='AUTOMATIC_SYNTHETIC_RECOVERY'
        response=(client or GroqClient(settings)).generate(prompt(proofs),response_schema=response_schema(proofs))
        info.attempts,info.reason=response.attempts,response.code
        info.status='FAILED'
        if response.content is not None:
            accepted,rejected=validate(response.content,proofs)
            if accepted:
                lexical=assemble(submission,lexical,proofs,accepted)
                receipt=issue(submission,accepted)
                info.status='ACCEPTED'; info.reason='PARTIAL_ASSOCIATIONS_CERTIFIED' if rejected or len(accepted)<len(proofs.associations) else 'ALL_CELL_ASSOCIATIONS_CERTIFIED'
                info.certificate='SPAN_ASSOCIATIONS_V1'; info.origin='GROQ_PROPOSAL_CERTIFIED'
                if rejected or len(accepted)<len(proofs.associations):
                    lexical.status='PARTIAL'
                    lexical.issues.append(ParseIssue(code='ASSOCIATIONS_QUARANTINED',severity='WARNING',message='Some proposed or omitted positions could not be accepted. Only independently proven positions were retained.'))
            else: info.status='REJECTED'; info.reason='PROPOSAL_ASSOCIATIONS_INVALID'
    if q['classification'] in {'NOT_TMT','UNSUPPORTED_FORMAT','AMBIGUOUS_STRUCTURE'}:
        lexical.issues.append(ParseIssue(code=q['classification'],severity='WARNING',message={'NOT_TMT':'No usable Tooth Movement Table structure was identified. Embedded instructions are inert.',
            'UNSUPPORTED_FORMAT':'The input may be a TMT, but its structure is unsupported.','AMBIGUOUS_STRUCTURE':'Multiple or incomplete positional interpretations remain; clarify the source formatting.'}[q['classification']]))
    detected=detect_source(lexical)
    return AutomaticParseResult(**lexical.model_dump(),pipeline=PipelineInfo(detection=detected,assistance=info,
        clarifications=clarifications(lexical,detected),quality=QualityAssessment(**q),recovery_receipt=receipt))
