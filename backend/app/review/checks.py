"""Independent technical checks; no clinical policy or source-semantic guessing."""

from hashlib import sha256

from app.parser.tokenize import lines
from app.review.models import RuleDefinition
from app.review.safeguards import values


def provenance_errors(lexical):
    global_errors=[]; bad=set()
    if lexical.raw_sha256!=sha256(lexical.raw_text.encode('utf-8')).hexdigest(): global_errors.append('RAW_HASH_MISMATCH')
    if lexical.schema_version!='1.0.0' or not lexical.source.adapter.id or not lexical.source.adapter.version:
        global_errors.append('PROVENANCE_VERSION_MISSING')
    source_lines={line.number:line for line in lines(lexical.raw_text)}
    def matches(span,raw):
        if span is None or raw is None or not 0<=span.start<=span.end<=len(lexical.raw_text): return False
        line=source_lines.get(span.line)
        return (line is not None and lexical.raw_text[span.start:span.end]==raw and span.start==line.start+span.column_start-1
                and span.column_end-span.column_start==span.end-span.start)
    teeth={t.id:t for t in lexical.teeth}
    for m in lexical.measurements:
        tooth=teeth.get(m.tooth_ref)
        if tooth is None or not matches(tooth.span,tooth.raw_identifier) or not matches(m.header_span,m.raw_label): bad.add(m.id)
        if m.raw_value is not None and not matches(m.span,m.raw_value): bad.add(m.id)
        if m.signed_decimal is not None and m.span is None: bad.add(m.id)
    return tuple(global_errors),bad


def rule_eligibility(rule: RuleDefinition, observation):
    """Rule-local metadata eligibility, after common semantic authority is established."""
    v=values(observation); missing=[]
    domain='TEST_ONLY' if observation.verification=='TEST_ONLY' else 'AUTHORIZED_VENDOR'
    if rule.allowed_evidence and domain not in rule.allowed_evidence: missing.append('rule_evidence_domain')
    if rule.allowed_modes and v.get('plan_mode') not in rule.allowed_modes: missing.append('rule_plan_mode')
    if rule.allowed_scopes and v.get('scope') not in rule.allowed_scopes: missing.append('rule_movement_scope')
    return tuple(missing)
