"""Closed-output validation, exact deduplication and visible conflict quarantine."""

from collections import defaultdict

from app.review.models import Finding, ObservedMeasurement, RuleRef
from app.review.registry import RULE_BY_ID
from app.review.templates import TEMPLATES
from app.semantics.fixtures import digest_json


def values(observed: ObservedMeasurement) -> dict[str, str | None]:
    return {c.name: c.canonical_value for c in observed.components}


def context_key(observed: ObservedMeasurement) -> tuple:
    v = values(observed)
    return tuple(v.get(k) for k in (
        "source_application", "source_version", "tooth_identifier", "notation", "dentition", "arch",
        "plan_mode", "reference_basis", "scope", "stage_index", "stage_kind", "coordinate_frame",
        "comparison_left_plan", "comparison_right_plan", "comparison_operation",
    ))


def suppress(finding: Finding, reason: str, *, conflict: str | None = None) -> Finding:
    data = finding.model_dump()
    data.update(status="SUPPRESSED", applicable=None, evaluated=False, finding_type="UNAVAILABLE",
                observed_measurements=(), tooth_id=None, abstain_reason=reason,
                template_id="conflict" if conflict else "suppressed", message=TEMPLATES["conflict" if conflict else "suppressed"],
                conflict_group=conflict, summary_counts={})
    return Finding.model_validate(data)


def _descriptive_contract(f: Finding) -> bool:
    """Output entailment rules use canonical facts, never raw English/vendor labels."""
    obs = f.observed_measurements
    if not obs:
        return False
    axes = {values(o).get("axis") for o in obs}
    templates = {"D01": "inventory", "D02": "co_programmed", "D10": "co_programmed", "D11": "co_programmed",
                 "D06": "angular", "D07": "bl", "D08": "md", "D12": "distribution", "D15": "zero"}
    if any(templates.get(r.rule_id) != f.template_id for r in f.triggering_rules):
        return False
    if f.template_id == "zero":
        return all(o.magnitude.is_zero() for o in obs) and len({context_key(o) for o in obs}) == 1
    if any(o.magnitude.is_zero() for o in obs):
        return False
    for ref in f.triggering_rules:
        if ref.rule_id == "D06" and not axes <= {"INCLINATION", "ANGULATION"}:
            return False
        if ref.rule_id == "D07" and axes != {"BUCCOLINGUAL"}:
            return False
        if ref.rule_id == "D08" and axes != {"MESIODISTAL"}:
            return False
        if ref.rule_id in {"D02", "D10", "D11"}:
            if len(axes) < 2 or len({context_key(o) for o in obs}) != 1 or values(obs[0]).get("scope") != "TOTAL":
                return False
            if ref.rule_id == "D10" and not ("ROTATION" in axes and axes & {"VERTICAL", "INTRUSION", "EXTRUSION"}):
                return False
            if ref.rule_id == "D11" and not (axes & {"INCLINATION", "ANGULATION"} and axes & {"BUCCOLINGUAL", "MESIODISTAL"}):
                return False
    if f.template_id == "distribution":
        contexts = {tuple(v for i, v in enumerate(context_key(o)) if i not in {2, 5}) for o in obs}
        expected = {"nonzero_positions": len(obs), "distinct_axes": len(axes),
                    "distinct_teeth": len({values(o).get("tooth_identifier") for o in obs}),
                    "distinct_arches": len({values(o).get("arch") for o in obs})}
        if len(contexts) != 1 or any(f.summary_counts.get(k) != v for k, v in expected.items()):
            return False
    return True


def apply_output_safeguards(findings: list[Finding], authorized: dict[str, ObservedMeasurement]) -> tuple[Finding, ...]:
    """Only exact engine-authorized snapshots may survive as descriptive output."""
    checked = []
    for f in findings:
        rule = RULE_BY_ID.get(f.rule_id)
        refs = {r.rule_id for r in f.triggering_rules}
        valid = (rule is not None and refs <= RULE_BY_ID.keys() and f.template_id in TEMPLATES
                 and f.message == TEMPLATES[f.template_id] and all(r.version == RULE_BY_ID[r.rule_id].version for r in f.triggering_rules))
        if f.status == "OBSERVED" and f.finding_type == "DESCRIPTIVE":
            valid = valid and rule.category == "DESCRIPTIVE" and rule.execution == "ACTIVE"
            valid = valid and all(o.measurement_id in authorized and o.model_dump_json() == authorized[o.measurement_id].model_dump_json()
                                  and set(o.input_refs) <= set(f.input_refs) for o in f.observed_measurements)
            valid = valid and _descriptive_contract(f)
            ids = {values(o).get("tooth_identifier") for o in f.observed_measurements if o.verification == "VERIFIED"}
            valid = valid and f.tooth_id == (next(iter(ids)) if len(ids) == 1 else None)
        # Disabled/deferred policies can never produce evaluated facts, including via an internal caller.
        if f.status == "OBSERVED" and any(RULE_BY_ID[r].execution != "ACTIVE" for r in refs if r in RULE_BY_ID):
            valid = False
        checked.append(f if valid else suppress(f, "OUTPUT_FACT_OR_PROVENANCE_NOT_AUTHORIZED"))

    # Conflicts on one semantic key are not resolved by arbitrary priority. Different bases never join.
    observations = defaultdict(list)
    for index, f in enumerate(checked):
        if f.status == "OBSERVED" and f.finding_type == "DESCRIPTIVE":
            for o in f.observed_measurements:
                observations[(context_key(o), values(o).get("axis"))].append((index, o))
    conflicts = {}
    for key, entries in observations.items():
        propositions = {(o.magnitude, values(o).get("unit"), values(o).get("direction"), values(o).get("sign")) for _, o in entries}
        if len(propositions) > 1:
            group = "conflict-" + digest_json({"key": key})[:16]
            for index, _ in entries:
                conflicts[index] = group
    checked = [suppress(f, "CONTRADICTORY_STRUCTURED_OBSERVATIONS", conflict=conflicts[i]) if i in conflicts else f for i, f in enumerate(checked)]

    # Exact same proposition only. Keep all rule IDs and source references. Never discard contradictions.
    merged = {}
    for f in checked:
        key = digest_json({"template": f.template_id, "status": f.status,
                           "observations": [o.model_dump(mode="json") for o in sorted(f.observed_measurements, key=lambda o: o.measurement_id)],
                           "counts": f.summary_counts}) if f.status == "OBSERVED" and f.finding_type == "DESCRIPTIVE" else f.finding_id
        if key in merged:
            prior = merged[key]
            data = prior.model_dump()
            data.update(triggering_rules=tuple(RuleRef(rule_id=rid) for rid in sorted({r.rule_id for r in prior.triggering_rules + f.triggering_rules})),
                        input_refs=tuple(sorted(set(prior.input_refs + f.input_refs))),
                        evidence_refs=tuple(sorted(set(prior.evidence_refs + f.evidence_refs))))
            merged[key] = Finding.model_validate(data)
        else:
            merged[key] = f
    return tuple(sorted(merged.values(), key=lambda f: (f.rule_id, f.finding_id)))
