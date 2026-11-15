"""One bounded Groq request over approved analytical evidence, immutable local facts.

Provider output may arrange whole-finding placeholders into paragraphs. It may
not author factual claims. No raw text, free-text identifiers or context leave.
Diagnostics use closed event names/codes and counters only.
"""
import json
import logging
import re

from app.interactive.models import AnalyticalGenerationInfo
from app.interactive.narrative import load_planning_settings
from app.reports.groq_client import GroqClient
from app.reports.validation import private_json

logger = logging.getLogger("finova.analysis")
REF = re.compile(r"\{(F\d{4})\}")
MAX_PROMPT_BYTES = 24_000


def analytical_wording(parsed, module, sections, findings, *, settings=None, client=None, functional_evidence=None):
    logger.info("analysis_ai_requested module=%s requested=True", module)
    reason, attempts, accepted = "GROQ_NOT_CONFIGURED", 0, 0
    chosen = sections
    try:
        settings = settings or load_planning_settings()
    except ValueError:
        reason = "GROQ_CONFIGURATION_INVALID"
    else:
        if settings.configured:
            tooth_aliases = {tooth.id: f"T{i:03d}" for i, tooth in enumerate(parsed.teeth, 1)}
            evidence_aliases = {m.id: f"E{i:04d}" for i, m in enumerate(parsed.measurements, 1)}
            # Shared evidence dictionary avoids resending all comparisons per finding.
            evidence = []
            for m in parsed.measurements:
                accepted_cell = m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} and m.field_status != "AMBIGUOUS"
                evidence.append([evidence_aliases[m.id], tooth_aliases[m.tooth_ref],
                    m.recognized_label if m.recognized_label in {"rotation", "angulation", "inclination", "mesiodistal", "buccolingual", "vertical", "relative_vertical", "intrusion", "extrusion"} else "unknown",
                    str(m.signed_decimal) if accepted_cell else None,
                    m.unit, m.raw_direction if m.raw_direction in {"D", "M", "B", "L", "E", "I"} else None,
                    m.numeric_status if m.field_status != "AMBIGUOUS" else "AMBIGUOUS"])
            comparison_sets = {}
            def comparison_ref(refs):
                key = tuple(refs)
                if key not in comparison_sets:
                    comparison_sets[key] = f"Q{len(comparison_sets)+1:03d}"
                return comparison_sets[key]
            payload = dict(module=module, evidence_columns=["ref", "tooth", "family", "exact_scalar", "unit", "source_label", "state"],
                evidence=evidence, sections=[dict(section_id=s.section_id,
                findings=[dict(ref=f.finding_id, kind=f.kind, origin=f.origin, demo_rule=f.demo_rule,
                    compared=comparison_ref(f.source_refs), selected='compared' if functional_evidence is not None and f.selected_refs == f.source_refs else [evidence_aliases[r] for r in f.selected_refs])
                    for f in findings if f.section_id == s.section_id]) for s in sections])
            payload["comparison_sets"] = {alias: [evidence_aliases[r] for r in refs] for refs, alias in comparison_sets.items()}
            if functional_evidence is not None:
                payload['approved_synthetic_decisions'] = functional_evidence
            # Grouping/selection was computed locally. Complete analytical claims
            # remain immutable locally, including tokens and exact scalar precision.
            messages = [dict(role="system", content=(
                "Compose concise professional analytical review wording from approved structured findings. "
                "Return JSON with sections: [{section_id, text}]. One item per supplied section. "
                "The evidence records and selected/compared references explain each approved finding; do not recompute them. "
                "A selected value of 'compared' means the same referenced comparison set. "
                "Use each own finding reference exactly once, in braces, e.g. {F0001}. Each becomes a complete immutable analytical sentence locally. "
                "Arrange these whole sentences into short paragraphs separated by two newlines. Output only placeholders and whitespace. "
                "Do not type facts, numbers, labels, conclusions, new advice or connective words outside placeholders. "
                "Retain all comparisons, unknowns, demo labels and scope findings in their own sections. "
                "SIMULATED_DEMO is illustrative only. No clinical predicates, attachment geometry or treatment schedules are authorized.")),
                dict(role="user", content=json.dumps(payload, separators=(",", ":")))]
            if len(json.dumps(messages).encode()) > MAX_PROMPT_BYTES:
                # The model orders sealed local findings; it never needs an
                # unbounded duplicate of all source cells or comparison members.
                # Keep the complete values, memberships and decisions in exports.
                compact = dict(module=module,scope='ORDER_IMMUTABLE_LOCAL_FINDINGS_ONLY',
                    complete_evidence_retained_locally=True,
                    source_summary=dict(teeth=len(parsed.teeth),positions=len(parsed.measurements),
                        numeric=sum(m.numeric_status in {'PARSED','EXPLICIT_ZERO'} and m.field_status!='AMBIGUOUS' for m in parsed.measurements),
                        unknown=sum(m.numeric_status not in {'PARSED','EXPLICIT_ZERO'} or m.field_status=='AMBIGUOUS' for m in parsed.measurements)),
                    sections=[dict(section_id=s.section_id,findings=[dict(ref=f.finding_id,kind=f.kind,policy=f.demo_rule)
                        for f in findings if f.section_id==s.section_id]) for s in sections])
                if functional_evidence is not None:
                    compact['policy_summary']=dict(origin=functional_evidence['origin'],clinical_authorized=False,
                        policy_set_version=functional_evidence['policy_set_version'],
                        catalog_concepts=[o['concept'] for o in functional_evidence['catalog']],
                        stages=len(functional_evidence['stages']),stage_basis=functional_evidence['stage_basis'])
                messages[1]['content']=json.dumps(compact,separators=(',',':'))
                logger.info('analysis_prompt_compacted module=%s scope=IMMUTABLE_FINDING_ORDER_ONLY findings=%d',module,len(findings))
            schema = {"type": "json_schema", "json_schema": {"name": "finova_analytical_wording_v1", "strict": True,
                "schema": {"type": "object", "properties": {"sections": {"type": "array", "items": {
                    "type": "object", "properties": {"section_id": {"type": "string"}, "text": {"type": "string"}},
                    "required": ["section_id", "text"], "additionalProperties": False}}}, "required": ["sections"], "additionalProperties": False}}}
            if len(json.dumps(messages).encode()) > MAX_PROMPT_BYTES:
                reason = "GROQ_PROMPT_LIMIT"
            else:
                config = settings.model_copy(update={"max_retries": 0, "max_completion_tokens": min(settings.max_completion_tokens, max(1024, len(findings)*24))})
                logger.info("analysis_groq_attempt module=%s requested=True attempted=True", module)
                result = (client or GroqClient(config)).generate(messages, response_schema=schema)
                attempts, reason = result.attempts, result.code
                logger.info("analysis_groq_result module=%s contacted=%s provider_responded=%s http_status=%s response_received=%s code=%s attempts=%d",
                    module, attempts > 0, result.http_status is not None, result.http_status, result.content is not None, reason, attempts)
                if result.content is not None:
                    validated = validate_analytical(result.content, sections, findings)
                    if validated is None:
                        reason = "GROQ_UNSUPPORTED_WORDING"
                    else:
                        chosen, accepted, reason = validated, len(sections), "GROQ_VALIDATED"
    logger.info("analysis_wording_complete module=%s requested=True attempted=%s contacted=%s succeeded=%s validated=%s fallback=%s code=%s attempts=%d",
        module, attempts > 0, attempts > 0, bool(accepted), bool(accepted), not bool(accepted), reason, attempts)
    return chosen, AnalyticalGenerationInfo(requested_mode="AUTO", used_mode="GROQ_AI" if accepted else "STANDARD_TEMPLATES",
        reason=reason, attempts=attempts, provider="GROQ" if attempts else None,
        model="openai/gpt-oss-120b" if attempts else None, eligible_wording_findings=len(sections), accepted_comments=accepted)


def validate_analytical(content, sections, findings):
    try:
        batch = private_json(content)
        if not isinstance(batch, dict) or set(batch) != {"sections"} or not isinstance(batch["sections"], list):
            return None
        expected = {s.section_id: s for s in sections}
        chosen = {}
        for row in batch["sections"]:
            if not isinstance(row, dict) or set(row) != {"section_id", "text"}:
                return None
            key, text = row["section_id"], row["text"]
            if not isinstance(key, str) or key not in expected or key in chosen or not isinstance(text, str) or len(text) > 6000:
                return None
            own = {f.finding_id: f.text for f in findings if f.section_id == key}
            refs = REF.findall(text)
            if len(refs) != len(own) or set(refs) != set(own) or REF.sub("", text).strip():
                return None
            # Each finding stays a separate paragraph even if the provider compacts
            # whitespace; this prevents another giant inventory from being accepted.
            chosen[key] = expected[key].model_copy(update={"text": "\n\n".join(own[ref] for ref in refs)})
        if set(chosen) != set(expected):
            return None
        return [chosen[s.section_id] for s in sections]
    except (ValueError, TypeError, KeyError, RecursionError):
        return None
