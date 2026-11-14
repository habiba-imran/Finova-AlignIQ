"""Project lexical references and existing guards; never infer attachment decisions."""
from app.attachments.models import AttachmentDraft, AttachmentEntry, AttachmentSubmission, SyntheticScenario
from app.domain.models import ParseResult
from app.parser.receipts import resolve
from app.review.models import DraftReview
from app.review.service import review_table
from app.review.safeguards import values
from app.semantics.fixtures import digest_json

GUARDS = {"A01", "A02", "A03", "A04", "A05", "A06", "R15", "H08", "G16", "G17", "N08", "N09", "N10", "N13"}
MISSING = ("verified_vendor_semantics", "actual_attachment_tooth_surface_stage_plan", "approved_attachment_policy", "validated_geometry_and_clinical_context")
LIMITATIONS = (
    "Prototype — not for clinical use. DRAFT — Requires Orthodontist Review. No clinician approval or sign-off is recorded.",
    "Candidates, alternatives and explicit no-attachment entries exist only as supplied TEST_ONLY demonstration decisions, never movement-derived prescriptions.",
    "Unknown and withheld are not no attachment. Missing values are not zero; large movements do not establish attachment indications.",
    "Illustrative dimensions, shapes, orientation, surfaces and stage references are supplied synthetic data; no clinical fit, geometry, force, superiority or placement validation is performed.",
    "A01–A04 and R15 remain disabled. A05/A06/H08 and N safeguards retain their withholding/claim-filter roles. No clinical attachment policy is activated.",
    "Synthetic data only. Processing is in memory; no raw data, identifiers or decisions are sent to an LLM. Copy/download is an explicit local export.",
)


def _entry(**body):
    entry = AttachmentEntry(entry_id="0" * 64, **body)
    return entry.model_copy(update={"entry_id": digest_json(entry.model_dump(mode="json", exclude={"entry_id"}))})


def _guards(review):
    return tuple(f.finding_id for f in review.findings if f.rule_id in GUARDS)


def unavailable_entries(parsed: ParseResult, review: DraftReview):
    refs = _guards(review)
    # A single explicit engineering-limit row instead of silently dropping teeth.
    teeth = parsed.teeth if len(parsed.teeth) <= 256 and len(parsed.measurements) <= 512 else []
    if not teeth:
        return (_entry(tooth_ref=None, original_tooth=None, result_type="WITHHELD", decision_origin="WITHHOLDING_GUARD",
            evidence_status="UNVERIFIED", explanation="Tooth-wise attachment review is withheld: no supported bounded tooth/movement dataset is available. No attachment decision was made.",
            measurement_refs=(), observation_refs=(), evidence_refs=(), finding_refs=refs,
            missing_prerequisites=MISSING + ("supported_table_with_at_most_256_tooth_tokens_and_512_positions",)),)
    entries = []
    for tooth in teeth:
        measurements = tuple(m for m in parsed.measurements if m.tooth_ref == tooth.id)
        present = any(m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} for m in measurements)
        entries.append(_entry(tooth_ref=tooth.id, original_tooth=tooth.raw_identifier,
            result_type="UNKNOWN" if present else "WITHHELD", decision_origin="WITHHOLDING_GUARD", evidence_status="UNVERIFIED",
            explanation="Attachment necessity, omission and design are unknown. Parsed values are unverified lexical information; no approved attachment policy or actual plan is available." if present else "Attachment review withheld: measurements are missing or unsupported, and clinical attachment prerequisites are absent.",
            measurement_refs=tuple(m.id for m in measurements), observation_refs=(), evidence_refs=(), finding_refs=refs,
            missing_prerequisites=MISSING + (() if present else ("available_measurements",))))
    return tuple(entries)


def supplied_entries(parsed: ParseResult, review: DraftReview, scenario: SyntheticScenario, evidence_ref: str):
    if review.evidence_domain != "TEST_ONLY" or parsed.raw_sha256 != scenario.input_sha256 or review.raw_sha256 != scenario.input_sha256:
        raise ValueError("SYNTHETIC_SCENARIO_BINDING_INVALID")
    teeth = {t.id: t for t in parsed.teeth}
    obs = {o.measurement_id: o for f in review.findings for o in f.observed_measurements}
    results, keys = [], {}
    for row in scenario.rows:
        tooth = teeth.get(row.tooth_ref)
        if not tooth or row.key in keys:
            raise ValueError("SYNTHETIC_TOOTH_OR_KEY_INVALID")
        observations = tuple(o for o in obs.values() if o.tooth_ref == tooth.id)
        canonical = {values(o).get("tooth_identifier") for o in observations}
        if row.synthetic_tooth is not None and (not canonical or canonical != {row.synthetic_tooth}):
            raise ValueError("SYNTHETIC_IDENTITY_NOT_AUTHORIZED")
        supplied = row.result_type in {"CANDIDATE", "ALTERNATIVE", "NOT_INDICATED"}
        if supplied and not row.synthetic_tooth:
            raise ValueError("SYNTHETIC_DECISION_IDENTITY_MISSING")
        if row.alternative_key and row.alternative_key not in keys:
            raise ValueError("SYNTHETIC_ALTERNATIVE_UNRESOLVED")
        explanation = {
            "CANDIDATE": "Supplied synthetic candidate for interface demonstration. Not selected by movement magnitude, the clinical engine or an LLM.",
            "ALTERNATIVE": "Supplied synthetic alternative to the linked candidate. No superiority, equivalence or clinical suitability is asserted.",
            "NOT_INDICATED": "Supplied demonstration decision: no attachment in this fictional scenario. Not inferred from zero, absent movements or an engine predicate.",
            "UNKNOWN": "Attachment need is unknown. Available synthetic movement evidence does not establish an attachment indication or omission.",
            "WITHHELD": "Attachment review is withheld. This synthetic token lacks authorized movement identity/evidence and clinical prerequisites.",
        }[row.result_type]
        entry = _entry(tooth_ref=tooth.id, original_tooth=tooth.raw_identifier, synthetic_tooth=row.synthetic_tooth,
            result_type=row.result_type, decision_origin="SUPPLIED_SYNTHETIC" if supplied else "WITHHOLDING_GUARD",
            evidence_status="TEST_ONLY" if row.synthetic_tooth else "UNVERIFIED", design=row.design, placement=row.placement,
            alternative_for=keys.get(row.alternative_key), explanation=explanation,
            measurement_refs=tuple(m.id for m in parsed.measurements if m.tooth_ref == tooth.id),
            observation_refs=tuple(sorted(o.measurement_id for o in observations)) if row.synthetic_tooth else (),
            evidence_refs=(f"{evidence_ref}:rows/{row.key}",) + tuple(sorted({f"{e.fixture_id}:{e.release_digest}:{e.locator}" for o in observations for c in o.components for e in c.evidence})) if row.synthetic_tooth else (),
            finding_refs=_guards(review), missing_prerequisites=MISSING if not supplied else ("clinical_validation_not_supplied_by_demo",))
        keys[row.key] = entry.entry_id
        results.append(entry)
    return tuple(results)


def _export(report: AttachmentDraft):
    review = report.engine_review
    lines = ["FINOVA ALIGNIQ — ATTACHMENT INTERFACE / MICRO REVIEW", report.draft_status, "Prototype — not for clinical use",
        "FINOVA SYNTHETIC ATTACHMENT DEMONSTRATION — TEST_ONLY; supplied illustrative decisions, not treatment policies." if report.evidence_domain == "TEST_ONLY" else "UNVERIFIED INPUT — attachment recommendations unavailable.",
        f"Report: {report.report_id}", f"Input SHA-256: {review.raw_sha256}", f"Engine report: {review.report_id}",
        f"Versions: parser {review.parser_version}; semantics {review.normalization_version}; engine {review.engine_version}; rules {review.rule_set_version}",
        "Wording: DETERMINISTIC_TEMPLATES; provider attempts: 0", "", "TOOTH-INDEXED ATTACHMENT REVIEW"]
    for e in report.entries:
        lines += ["", f"Original token: {e.original_tooth if e.original_tooth is not None else 'UNAVAILABLE'}; internal reference: {e.tooth_ref or 'UNAVAILABLE'}",
            f"Verified identity: {e.verified_tooth or 'UNKNOWN'}; synthetic identity: {e.synthetic_tooth or 'UNAVAILABLE'}",
            f"Result: {e.result_type}; origin: {e.decision_origin}; evidence: {e.evidence_status}", e.explanation,
            f"Approval: {e.approval_status}; status: {e.review_status}", f"Entry: {e.entry_id}"]
        if e.design:
            d = e.design
            lines += [f"Supplied demo design: {d.design_id}; category: {d.category_id}; label: {d.label}",
                f"Shape: {d.shape or 'UNKNOWN'}; orientation: {d.orientation or 'UNKNOWN'}",
                f"Dimensions: {d.dimensions.x} x {d.dimensions.y} x {d.dimensions.z} {d.dimensions.unit}" if d.dimensions else "Dimensions: UNKNOWN"]
        else:
            lines += ["Design / shape / dimensions / orientation: UNKNOWN or not applicable to a supplied no-attachment decision; no geometry inferred."]
        lines += [f"Surface: {e.placement.surface_id}; frame: {e.placement.frame_id}; stage reference: {e.placement.stage_ref or 'UNKNOWN'}" if e.placement else "Placement / surface / stage: UNKNOWN; no placement validation.",
            f"Alternative for: {e.alternative_for or 'None'}", "Lexical measurement references: " + (", ".join(e.measurement_refs) or "None"),
            "Authorized observation references: " + (", ".join(e.observation_refs) or "None"), "Evidence: " + (", ".join(e.evidence_refs) or "No accepted attachment evidence"),
            "Safeguard findings (not candidate triggers): " + ", ".join(e.finding_refs), "Missing prerequisites: " + ", ".join(e.missing_prerequisites)]
    lines += ["", "EXACT AUTHORIZED MOVEMENT EVIDENCE (not attachment indications)"]
    observations = {o.measurement_id: o for f in review.findings for o in f.observed_measurements}
    for o in observations.values():
        lines += [f"{o.measurement_id}; original token {o.raw_tooth_identifier}; label {o.raw_label}; original cell {o.raw_value}; scalar {o.signed_decimal}; magnitude {o.magnitude}; {o.verification}",
            "Source locations: " + ", ".join(f"L{s.line}:C{s.column_start}" for s in o.source_spans)]
    lines += ["", "RULE EVALUATION LEDGER"] + [f"{e.rule_id} v{e.version}: {e.status}; execution {e.execution}; approval {e.approval_status}; findings {', '.join(e.finding_ids)}; reason {e.abstain_reason or 'See finding'}" for e in review.evaluations]
    lines += ["", "LIMITATIONS"] + list(report.limitations) + [report.draft_status, "No clinician sign-off is recorded.", ""]
    return "\n".join(lines)


def assemble(parsed, review, *, scenario=None, evidence_ref=None):
    entries = supplied_entries(parsed, review, scenario, evidence_ref) if scenario else unavailable_entries(parsed, review)
    body = dict(evidence_domain=review.evidence_domain, engine_review=review, entries=entries,
                limitations=tuple(dict.fromkeys(LIMITATIONS + review.limitations)))
    provisional = AttachmentDraft(report_id="0" * 64, export_text="", **body)
    report_id = digest_json(provisional.model_dump(mode="json", exclude={"report_id", "export_text"}))
    report = AttachmentDraft(report_id=report_id, export_text="", **body)
    return report.model_copy(update={"export_text": _export(report)})


def attachment_review(submission: AttachmentSubmission):
    parsed = resolve(submission)
    review = review_table(submission, requested_assessments=("ATTACHMENTS",))
    return assemble(parsed, review)
