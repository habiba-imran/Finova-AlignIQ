"""Recompute authorized findings, assemble local facts, optionally select bounded wording."""

from collections import defaultdict
from dataclasses import dataclass

from app.domain.models import RawTMTSubmission
from app.reports.groq_client import GroqClient
from app.reports.models import CommentMode, FinalDraftReport, GenerationInfo, ReportComment
from app.reports.prompt import build_prompt
from app.reports.settings import ReportSettings, load_settings
from app.reports.templates import ALTERNATIVES, literal, measurement_text, render_comment
from app.reports.validation import validate_wording
from app.review.models import AssessmentQuestion, DraftReview, Finding, RuleRef
from app.review.registry import RULE_BY_ID
from app.review.safeguards import context_key, values
from app.review.service import review_table
from app.review.context import TestRuleContext
from app.review.templates import TEMPLATES
from app.semantics.fixtures import CheckedFixture, digest_json
from app.semantics.models import required_components

REPORT_LIMITATIONS = (
    "DRAFT — Requires Orthodontist Review. No diagnosis, prescription, clinical validation or authorized sign-off is provided.",
    "Groq may select approved wording only. All facts, measurements, uncertainty, provenance and limitations are assembled locally.",
    "Real-patient transmission is disabled. Raw tables, identifiers, measurements, source claims and clinical records are never sent to Groq.",
    "Synthetic confirmation is not PHI detection. Use synthetic data only; application data remain in memory until an explicit local copy/download.",
)


@dataclass(frozen=True)
class CommentUnit:
    primary: Finding
    findings: tuple[Finding, ...]
    comment: ReportComment


def _eligible(f: Finding, review: DraftReview) -> bool:
    if f.status != "OBSERVED" or f.finding_type != "DESCRIPTIVE" or not f.evaluated or f.applicable is not True:
        return False
    if f.template_id not in ALTERNATIVES or not f.observed_measurements or f.abstain_reason or f.conflict_group or f.missing_required_fields:
        return False
    if f.message != TEMPLATES[f.template_id] or any(r.rule_id not in RULE_BY_ID or RULE_BY_ID[r.rule_id].execution != "ACTIVE"
                                                  or r.version != RULE_BY_ID[r.rule_id].version for r in f.triggering_rules):
        return False
    authority = "TEST_ONLY" if review.evidence_domain == "TEST_ONLY" else "VERIFIED"
    if review.evidence_domain == "UNVERIFIED":
        return False
    for o in f.observed_measurements:
        by_name = {c.name: c for c in o.components}
        v = values(o)
        if o.verification != authority or v.get("plan_mode") == "COMPARISON":
            return False
        if any(name not in by_name or by_name[name].status != authority for name in required_components(v)):
            return False
        if any(e.raw_sha256 != review.raw_sha256 for c in o.components for e in c.evidence):
            return False
        if authority == "TEST_ONLY" and v.get("source_application") != "TEST_ONLY":
            return False
    return True


def comment_units(review: DraftReview) -> tuple[CommentUnit, ...]:
    groups = defaultdict(list)
    for f in review.findings:
        if _eligible(f, review):
            section = "SUMMARY" if f.template_id == "distribution" else "TOOTH"
            key = (section, context_key(f.observed_measurements[0]))
            if section == "SUMMARY":
                key = (section, f.finding_id)
            groups[key].append(f)
        elif f.status in {"SEMANTICS_UNKNOWN", "CONTEXT_REQUIRED", "DISABLED", "SUPPRESSED", "PARSE_INVALID"}:
            # Identical unavailable propositions share wording while retaining every finding/rule/reference.
            groups[("UNAVAILABLE", f.template_id, f.status, f.missing_required_fields, f.abstain_reason)].append(f)
    units = []
    priority = {name: i for i, name in enumerate(("paired_difference", "co_programmed", "group_rotation", "group_extrusion", "group_intrusion", "molar_md", "angular", "bl", "md", "zero", "inventory", "distribution"))}
    for key, fs in groups.items():
        fs = tuple(sorted(fs, key=lambda f: f.finding_id))
        primary = min(fs, key=lambda f: (priority.get(f.template_id, 99), f.finding_id))
        obs = {o.measurement_id: o for f in fs for o in f.observed_measurements}
        ordered_obs = tuple(obs[mid] for mid in sorted(obs))
        text = render_comment(primary)
        # The primary can be a specialized observer; append any additional authorized sibling facts exactly once.
        included = {o.measurement_id for o in primary.observed_measurements}
        for o in ordered_obs:
            if o.measurement_id not in included:
                text += "\n" + measurement_text(o)
        ids = tuple(f.finding_id for f in fs)
        rules = tuple(RuleRef(rule_id=rid) for rid in sorted({r.rule_id for f in fs for r in f.triggering_rules}))
        comment = ReportComment(comment_id=digest_json({"finding_ids": ids}), finding_ids=ids, rules=rules, section=key[0],
                                tooth_id=primary.tooth_id, evidence_status="UNVERIFIED" if not obs else ordered_obs[0].verification,
                                text=text, measurements=ordered_obs,
                                input_refs=tuple(sorted({r for f in fs for r in f.input_refs})),
                                evidence_refs=tuple(sorted({e for f in fs for e in f.evidence_refs})),
                                missing_required_fields=tuple(sorted({m for f in fs for m in f.missing_required_fields})),
                                abstain_reasons=tuple(sorted({f.abstain_reason for f in fs if f.abstain_reason})),
                                evaluation_statuses=tuple(sorted({f.status for f in fs})))
        units.append(CommentUnit(primary, fs, comment))
    return tuple(sorted(units, key=lambda u: (u.comment.section, u.comment.comment_id)))


def _export_text(review: DraftReview, comments: tuple[ReportComment, ...], generation: GenerationInfo,
                 limitations: tuple[str, ...], report_id: str) -> str:
    lines = ["FINOVA ALIGNIQ", "Descriptive Planning Report", "DRAFT — Requires Orthodontist Review",
             "Prototype — not for clinical use", "", f"Report ID: {report_id}", f"Engine review: {review.report_id}",
             f"Source evidence domain: {review.evidence_domain}",
             f"Source platform claim (unverified): {literal(review.source.source_claim)}",
             f"Source version claim (unverified): {literal(review.source.context.source_version)}",
             "Verified source/mode/basis/scope: listed with each accepted observation; otherwise UNKNOWN.",
             f"Input SHA-256: {review.raw_sha256}",
             f"Versions: parser {review.parser_version}; semantics {review.normalization_version}; engine {review.engine_version}; rules {review.rule_set_version}",
             f"Wording mode: {generation.used_mode}; reason: {generation.reason}; provider attempts: {generation.attempts}",
             "", "AVAILABLE OBSERVATIONS", f"Eligible positions: {review.coverage.eligible_positions}/{review.coverage.declared_positions}; unavailable: {review.coverage.unavailable_positions}.",
             "Expected axis coverage: UNKNOWN. No finding is not a finding of no clinical concern."]
    for section, heading in (("TOOTH", "TOOTH-WISE DESCRIPTIVE COMMENTS"), ("SUMMARY", "DISTRIBUTION SUMMARY"), ("UNAVAILABLE", "UNAVAILABLE ASSESSMENTS / MISSING INFORMATION")):
        lines.extend(("", heading))
        selected = [c for c in comments if c.section == section]
        if not selected:
            lines.append("No authorized observations available." if section != "UNAVAILABLE" else "No additional unavailable assessment entries.")
        for c in selected:
            lines.extend(("", c.text, "Rules: " + ", ".join(f"{r.rule_id} v{r.version}" for r in c.rules),
                          "Findings: " + ", ".join(c.finding_ids), "Input references: " + (", ".join(c.input_refs) or "System control"),
                          "Evidence references: " + (", ".join(c.evidence_refs) or "No accepted measurement evidence"),
                          "Evaluation: " + ", ".join(c.evaluation_statuses), "Wording: " + c.wording_source))
    lines.extend(("", "RULE EVALUATION LEDGER"))
    lines.extend(f"{e.rule_id} v{e.version}: {e.status}; findings: {', '.join(e.finding_ids)}" for e in review.evaluations)
    lines.extend(("", "CLINICAL LIMITATIONS / SCOPE"))
    lines.extend("- " + limitation for limitation in limitations)
    lines.extend(("", "DRAFT — Requires Orthodontist Review", "No clinician approval or sign-off is recorded."))
    return "\n".join(lines) + "\n"


def _assemble(review: DraftReview, mode: CommentMode, settings: ReportSettings | None,
              client: GroqClient | None) -> FinalDraftReport:
    units = comment_units(review)
    eligible = tuple(u for u in units if u.comment.section != "UNAVAILABLE")
    reason = "STANDARD_TEMPLATES_SELECTED"
    attempts = 0
    accepted = {}
    if mode != "TEMPLATES":
        if not eligible:
            reason = "NO_ELIGIBLE_FINDINGS"
        elif review.evidence_domain != "TEST_ONLY":
            reason = "REAL_PATIENT_TRANSMISSION_DISABLED"
        else:
            try:
                settings = settings or load_settings()
            except ValueError:
                reason = "GROQ_CONFIGURATION_INVALID"
            else:
                if not settings.configured:
                    reason = "GROQ_NOT_CONFIGURED"
                elif len(eligible) > settings.max_wording_findings:
                    reason = "GROQ_FINDING_LIMIT"
                else:
                    messages, refs = build_prompt(tuple(u.primary for u in eligible))
                    result = (client or GroqClient(settings)).generate(messages)
                    attempts, reason = result.attempts, result.code
                    if result.content is not None:
                        accepted, reason = validate_wording(result.content, refs)
    comments = []
    for unit in units:
        base = unit.comment
        wording = accepted.get(unit.primary.finding_id)
        data = base.model_dump()
        if wording is not None:
            # Replace only the exact leading approved wording. Every local fact byte remains untouched.
            original = TEMPLATES[unit.primary.template_id]
            assert base.text.startswith(original)
            data.update(text=wording + base.text[len(original):], wording_source="GROQ_VALIDATED", wording_validation="ACCEPTED")
        elif unit in eligible and mode != "TEMPLATES":
            data.update(wording_validation="FALLBACK", fallback_reason=reason)
        comments.append(ReportComment.model_validate(data))
    used = "STANDARD_TEMPLATES" if not accepted else "GROQ_AI" if len(accepted) == len(eligible) else "MIXED"
    generation = GenerationInfo(requested_mode=mode, used_mode=used, reason=reason,
                                provider="GROQ" if attempts else None, model="openai/gpt-oss-120b" if attempts else None,
                                attempts=attempts, eligible_wording_findings=len(eligible), accepted_comments=len(accepted))
    limitations = tuple(dict.fromkeys(REPORT_LIMITATIONS + review.limitations))
    body = dict(engine_review=review, generation=generation, comments=tuple(comments), limitations=limitations)
    provisional = FinalDraftReport(report_id="0"*64, export_text="", **body)
    report_id = digest_json(provisional.model_dump(mode="json", exclude={"report_id", "export_text"}))
    return FinalDraftReport(report_id=report_id, export_text=_export_text(review, tuple(comments), generation, limitations, report_id), **body)


def generate_report(submission: RawTMTSubmission, *, mode: CommentMode = "AUTO",
                    requested_assessments: tuple[AssessmentQuestion, ...] = (), checked: CheckedFixture | None = None,
                    test_only: bool = False, settings: ReportSettings | None = None, client: GroqClient | None = None,
                    test_context: TestRuleContext | None = None) -> FinalDraftReport:
    """Only raw submissions enter HTTP. Fixture and mock-client injection is library-only."""
    if mode not in {"AUTO", "GROQ", "TEMPLATES"}:
        raise ValueError("UNSUPPORTED_COMMENT_MODE")
    review = review_table(submission, requested_assessments=requested_assessments, checked=checked, test_only=test_only,test_context=test_context)
    return _assemble(review, mode, settings, client)
