"""Audit IDs retained. No numerical policy or path to enable clinical predicates."""

from app.review.models import RuleDefinition

_GATES = (
    ("Non-empty structured input", ("lexical_structure",)),
    ("Reliable source identity", ("source_application", "source_version")),
    ("Tooth numbering convention", ("notation", "dentition", "arch")),
    ("Tooth ID validity", ("tooth_identifier", "notation", "dentition")),
    ("Arch association", ("arch",)),
    ("Duplicate tooth records", ("duplicate_scope",)),
    ("Canonical movement label mapping", ("axis",)),
    ("Numeric, unit and precision integrity", ("numeric_value", "unit")),
    ("Directional meaning verified", ("sign", "direction")),
    ("Missing versus zero", ("numeric_value",)),
    ("Reference basis: crown/root/cusp", ("reference_basis",)),
    ("Total versus stage mode", ("scope", "stage_index", "stage_kind")),
    ("Plan/comparison mode", ("plan_mode",)),
    ("Absent/unmovable teeth", ("verified_external_tooth_status",)),
    ("Stage ordering and identifiers", ("verified_stage_dataset",)),
    ("Schema version and original evidence", ("source_provenance",)),
    ("Conflict and unsupported input handling", ("field_semantic_eligibility",)),
    ("Recognized tooth types only", ("verified_tooth_group_map",)),
)
_DESCRIPTIONS = (
    "Movement inventory per tooth", "Co-programmed movement axes", "Rotation by tooth group",
    "Extrusion by tooth group", "Intrusion by tooth group", "Source inclination/angulation inventory",
    "Buccolingual displacement inventory", "Mesiodistal displacement inventory", "Molar mesial/distal movement",
    "Co-programmed rotation and vertical axes", "Co-programmed angular and translational axes",
    "Movement distribution summary", "Equivalent opposite-side comparison", "Requested context inventory",
    "All supported, observed axes are zero", "Historical plan difference",
)
_CLINICAL = (
    "Canine/premolar rotation review", "Rotation magnitude band by tooth type", "Anterior extrusion review",
    "Posterior extrusion review", "Lower incisor intrusion review", "Other intrusion review",
    "Incisor inclination/root-control review", "Mesiodistal angulation review", "Posterior transverse movement review",
    "Maxillary molar distalization review", "Molar mesialization review", "Movement combination review",
    "Staged versus total concern", "Context-sensitive assessment withheld", "Attachment strategy review", "Whole-case complexity",
)
_STAGING = (
    "Per-stage movement ceilings", "Cumulative/incremental consistency", "Observed configured constraint exceedance",
    "Sequential distalization pattern", "Movement overlap interaction", "Geometry interference", "IPR timing and quantity",
    "Anchorage/root balancing",
)
_ATTACHMENTS = (
    "Attachment presence audit", "Attachment-to-movement review", "Conflicting attachment preferences",
    "Attachment stage scheduling", "Exact attachment placement withheld", "Universal attachment superiority blocked",
)
_SAFETY = (
    "No suitability diagnosis", "Periodontal condition unavailable", "Root/bone assessment unavailable",
    "Occlusal contacts unavailable", "No unseen IPR planning", "No extraction/surgery recommendations",
    "No predicted probability/duration", "No attachment prescriptions", "No collision-free staging claim",
    "Draft and clinician inspection", "Context-dependent exclusions", "Privacy/data minimization",
)
_OUTPUT = (
    "Only structured template facts", "Measurement exactness", "Finding-to-source traceability",
    "Deduplication and explicit conflicts", "Localized uncertainty", "Draft-only review status",
)
_PROTECTIONS = (
    "Expected coverage remains unknown", "Unknown format/version abstention", "Single-capture identity isolation",
    "Raw Unicode evidence preservation", "Verified mirrored sign convention only", "External tooth status required",
    "Stage states required", "No unproven composition", "Field-scoped abstention", "Untrusted text cannot alter claims",
    "Immutable signed amendments", "Requested purpose separate from measurements", "Rule-dependent eligibility",
    "Incident and rollback workflow",
)


def _build_registry() -> tuple[RuleDefinition, ...]:
    rules = []
    for i, (name, fields) in enumerate(_GATES, 1):
        rid = f"G{i:02}"
        rules.append(RuleDefinition(rule_id=rid, name=name, category="TECHNICAL", disposition="REVISE" if i == 14 else "READY",
                                    execution="DEFERRED" if i in {14, 15, 18} else "ACTIVE", required_fields=fields,
                                    reason="CONSUMES_EXISTING_PARSER_AND_SEMANTIC_GATES" if i not in {14, 15, 18} else "VERIFIED_EXTERNAL_DATA_CONTRACT_REQUIRED"))
    for i, name in enumerate(_DESCRIPTIONS, 1):
        deferred = i in {3, 4, 5, 9, 13, 16}
        fields = ("verified_tooth_group_map",) if i in {3, 4, 5, 9} else ("verified_pair_map_and_mirror_operations",) if i == 13 else ("verified_baseline_geometry_and_operations",) if i == 16 else ("authorized_semantic_measurement",)
        rules.append(RuleDefinition(rule_id=f"D{i:02}", name=name, category="DESCRIPTIVE",
                                    disposition="REVISE" if i in {2, 10, 11, 16} else "READY",
                                    execution="DEFERRED" if deferred else "ACTIVE", required_fields=() if i == 14 else fields,
                                    dependencies=() if deferred or i in {1, 14} else ("D01",),
                                    allowed_evidence=("AUTHORIZED_VENDOR", "TEST_ONLY"), allowed_modes=("ALIGN_FINAL", "DOCTOR_FINAL", "TEST_PLAN_MODE"),
                                    allowed_scopes=("TOTAL",) if i in {2, 10, 11} else ("TOTAL", "CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"),
                                    reason="AUDIT_CORRECTED_DESCRIPTIVE_ONLY" if not deferred else "ADDITIONAL_VERIFIED_MAP_OR_GEOMETRY_REQUIRED"))
    for i, name in enumerate(_CLINICAL, 1):
        rules.append(RuleDefinition(rule_id=f"R{i:02}", name=name, category="SAFETY" if i == 14 else "CLINICAL",
                                    disposition="READY" if i == 14 else "MORE DATA" if i in {13, 16} else "VALIDATE",
                                    execution="ACTIVE" if i == 14 else "DISABLED",
                                    required_fields=("orthodontist_approved_policy", "policy_specific_verified_context") if i != 14 else ("requested_assessment_context",),
                                    reason="SUFFICIENCY_ABSTENTION_ONLY" if i == 14 else "NO_APPROVED_CLINICAL_POLICY"))
    for prefix, names, category in (("T", _STAGING, "STAGING"), ("A", _ATTACHMENTS, "ATTACHMENT")):
        for i, name in enumerate(names, 1):
            guard = prefix == "A" and i in {5, 6}
            rules.append(RuleDefinition(rule_id=f"{prefix}{i:02}", name=name, category="SAFETY" if guard else category,
                                        disposition="READY" if prefix == "A" and i == 6 else "MORE DATA",
                                        execution="ACTIVE" if guard else "DISABLED", required_fields=() if guard else ("approved_policy_and_verified_extra_data",),
                                        reason="GLOBAL_WITHHOLDING_GUARD_ONLY" if guard else "NO_POLICY_OR_EXTRA_DATA_MODULE"))
    for prefix, names, category in (("H", _SAFETY, "SAFETY"), ("L", _OUTPUT, "OUTPUT"), ("N", _PROTECTIONS, "PROTECTION")):
        for i, name in enumerate(names, 1):
            deferred = prefix == "N" and i in {11, 14}
            rules.append(RuleDefinition(rule_id=f"{prefix}{i:02}", name=name, category=category,
                                        disposition="ADDITIONAL" if prefix == "N" else "READY",
                                        execution="DEFERRED" if deferred else "ACTIVE",
                                        reason="FUTURE_AUTHORIZED_WORKFLOW_REQUIRED" if deferred else "PHASE2A_INVARIANT_ONLY"))
    return tuple(sorted(rules, key=lambda r: r.rule_id))


RULES = _build_registry()


def execution_order(rules: tuple[RuleDefinition, ...] = RULES) -> tuple[RuleDefinition, ...]:
    """Stable topological order; malformed registries never execute opportunistically."""
    remaining = {r.rule_id: r for r in rules}
    if len(remaining) != len(rules) or any(d not in remaining for r in rules for d in r.dependencies):
        raise ValueError("INVALID_RULE_DEPENDENCIES")
    ordered = []
    done = set()
    while remaining:
        ready = sorted(rid for rid, rule in remaining.items() if set(rule.dependencies) <= done)
        if not ready:
            raise ValueError("CYCLIC_RULE_DEPENDENCIES")
        for rid in ready:
            ordered.append(remaining.pop(rid))
            done.add(rid)
    return tuple(ordered)


RULE_BY_ID = {r.rule_id: r for r in RULES}
