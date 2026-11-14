"""Purpose-specific, source-bound reports. Supplied details never grant authority."""
import json

from app.interactive.models import ModuleGenerationInfo, ModuleSection
from app.interactive.narrative import load_planning_settings, planning_wording


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def validate_details(parsed, submission):
    details = submission.review_details
    teeth = {tooth.id for tooth in parsed.teeth}
    movements = {movement.id: movement for movement in parsed.measurements}
    if submission.module != "micro" and details.attachments or submission.module != "nano" and (details.stages or details.allocations or details.anchorage_notes):
        raise ValueError("DETAILS_MODULE_MISMATCH")
    if any(row.tooth_ref not in teeth for row in details.attachments) or len({row.tooth_ref for row in details.attachments}) != len(details.attachments):
        raise ValueError("ATTACHMENT_REFERENCE_INVALID")
    for row in details.attachments:
        if row.choice != "ATTACHMENT" and any(value is not None for value in (row.design, row.width_mm, row.height_mm, row.depth_mm, row.surface, row.orientation)):
            raise ValueError("ATTACHMENT_CHOICE_CONFLICT")
    stages = {stage.stage_id: stage for stage in details.stages}
    if len(stages) != len(details.stages) or len({stage.order for stage in details.stages}) != len(details.stages) or any(not stage.stage_id.strip() for stage in details.stages):
        raise ValueError("STAGE_REFERENCE_INVALID")
    keys = set()
    for row in details.allocations:
        movement = movements.get(row.measurement_ref)
        key = (row.stage_id, row.measurement_ref)
        if row.stage_id not in stages or not movement or movement.tooth_ref != row.tooth_ref or key in keys:
            raise ValueError("ALLOCATION_REFERENCE_INVALID")
        if row.amount is not None and (row.unit is None or movement.unit is not None and row.unit != movement.unit):
            raise ValueError("ALLOCATION_UNIT_INVALID")
        keys.add(key)
    if any(row.tooth_ref is not None and row.tooth_ref not in teeth or not row.note.strip() for row in details.anchorage_notes):
        raise ValueError("ANCHORAGE_REFERENCE_INVALID")


def module_sections(parsed, submission, *, settings=None, client=None):
    validate_details(parsed, submission)
    details = submission.review_details
    teeth = {tooth.id: tooth.raw_identifier for tooth in parsed.teeth}
    movements = {movement.id: movement for movement in parsed.measurements}
    definitions = []

    def section(key, title, facts, refs=(), missing=(), supplied=False):
        definitions.append(dict(section_id=key, title=title, facts=facts, source_refs=list(refs),
            missing_fields=list(dict.fromkeys(missing)), status="SUPPLIED_UNVERIFIED" if supplied else "UNAVAILABLE"))

    if submission.module == "micro":
        rows = details.attachments
        refs = [f"review_details/attachments/{index}" for index in range(len(rows))]
        decisions, designs, placements = [], [], []
        design_missing, placement_missing = [], []
        for row in rows:
            tooth = quote(teeth[row.tooth_ref])
            choices = {"UNKNOWN": "no recorded attachment choice", "ATTACHMENT": "a user-supplied attachment choice", "NO_ATTACHMENT": "a user-supplied no-attachment choice"}
            decisions.append(f"{choices[row.choice]} for original tooth token {tooth}, without an independently assessed indication")
            if row.choice == "ATTACHMENT":
                dims = [f"{label} {value} mm" if value is not None else f"{label} unknown" for label, value in (("width", row.width_mm), ("height", row.height_mm), ("depth", row.depth_mm))]
                designs.append(f"a supplied design record for original tooth token {tooth}: name {quote(row.design) if row.design else 'unknown'}; " + "; ".join(dims))
                placements.append(f"a supplied placement record for original tooth token {tooth}: surface {quote(row.surface) if row.surface else 'unknown'}; orientation {quote(row.orientation) if row.orientation else 'unknown'}")
                if not row.design or any(value is None for value in (row.width_mm, row.height_mm, row.depth_mm)):
                    design_missing.append(f"Design and complete dimensions for tooth token {teeth[row.tooth_ref].strip()}")
                if not row.surface or not row.orientation:
                    placement_missing.append(f"Surface and orientation for tooth token {teeth[row.tooth_ref].strip()}")
        supplied = any(row.choice != "UNKNOWN" for row in rows)
        section("ATTACHMENT_RECORDS", "Supplied attachment choices", decisions or [f"an attachment review with no supplied attachment choices for the {len(teeth)} parsed tooth rows"], refs,
            ["Tooth-wise attachment choices"] if not supplied else (), supplied=supplied)
        section("ATTACHMENT_DESIGN", "Design and dimensions", designs or ["unavailable attachment design and geometry assessments because no attachment design records were supplied"], refs,
            design_missing or (["Attachment design and dimensions"] if not designs else []), supplied=bool(designs))
        section("ATTACHMENT_PLACEMENT", "Placement information", placements or ["unavailable attachment placement assessments because no surface or orientation records were supplied"], refs,
            placement_missing or (["Attachment surface and orientation"] if not placements else []), supplied=bool(placements))
        section("ATTACHMENT_LIMITS", "Attachment review limits", ["an unavailable independent attachment-indication assessment; TMT movement magnitudes alone do not establish attachment need, design or placement"],
            missing=["Independent attachment indication and suitability assessment"])
    else:
        stage_refs = [f"review_details/stages/{index}" for index in range(len(details.stages))]
        stage_facts = [f"a supplied stage {quote(stage.stage_id)} at reported order {stage.order}, with duration {str(stage.duration_days) + ' days' if stage.duration_days is not None else 'unknown'}" for stage in sorted(details.stages, key=lambda stage: stage.order)]
        if parsed.source.context.stage_index is not None:
            stage_facts.append(f"a source-context stage index of {parsed.source.context.stage_index}, which does not independently establish a stage sequence or movement allocation")
            stage_refs.append("parsed/source/context")
        section("STAGE_RECORDS", "Supplied stage information", stage_facts or ["a sequencing review with no supplied stage IDs, order or timing information"], stage_refs,
            ["Stage IDs and order"] if not details.stages else ["Duration for stage " + stage.stage_id for stage in details.stages if stage.duration_days is None], supplied=bool(stage_facts))
        allocation_facts = []
        for row in details.allocations:
            movement = movements[row.measurement_ref]
            amount = f"{row.amount} {row.unit}" if row.amount is not None else "unknown (the TMT value was not copied)"
            allocation_facts.append(f"a user-supplied allocation for original tooth token {quote(teeth[row.tooth_ref])}, source field {quote(movement.raw_label)}, stage {quote(row.stage_id)}: reported stage amount {amount}")
        section("STAGE_ALLOCATIONS", "Supplied movement allocations", allocation_facts or ["unavailable stage-specific movement allocations; the pasted TMT values have not been assigned to stages"],
            [f"review_details/allocations/{index}" for index in range(len(details.allocations))] + [row.measurement_ref for row in details.allocations],
            ["Explicit stage-to-movement allocations"] if not details.allocations else ["Stage amount for " + row.stage_id for row in details.allocations if row.amount is None], supplied=bool(allocation_facts))
        anchor_facts = [f"a user-supplied anchorage note for {'the overall plan' if row.tooth_ref is None else 'original tooth token ' + quote(teeth[row.tooth_ref])}: {quote(row.note)}; not an independently assessed requirement" for row in details.anchorage_notes]
        section("ANCHORAGE_RECORDS", "Supplied anchorage notes", anchor_facts or ["an unavailable anchorage review because no anchorage information was supplied"],
            [f"review_details/anchorage_notes/{index}" for index in range(len(details.anchorage_notes))], ["Supplied anchorage information"] if not anchor_facts else (), supplied=bool(anchor_facts))
        section("SEQUENCING_LIMITS", "Sequencing review limits", ["an unavailable independent sequencing-suitability assessment; no optimized order, stage count, force, timing or anchorage requirement is inferred from pasted TMT values"],
            missing=["Independent assessment of sequencing and anchorage suitability"])

    groups, substitutions, mapping, fallback = [], {}, {}, {}
    index = 0
    for number, definition in enumerate(definitions, 1):
        alias = f"T{number:03d}"
        facts, entries = {}, []
        for fact in definition["facts"]:
            index += 1
            ref = f"M{index:04d}"
            facts[ref] = fact
            # Free-text designs, notes, original tooth labels and stage IDs remain
            # local. Only a closed section kind/status reaches the provider.
            entries.append(dict(ref=ref, facts=[definition["section_id"], None, None, None, definition["status"]]))
        groups.append(dict(tooth_ref=alias, movements=entries))
        substitutions[alias], mapping[alias] = facts, definition["section_id"]
        fallback[definition["section_id"]] = ". ".join(fact[0].upper() + fact[1:] for fact in definition["facts"]) + "."
    if settings is None:
        try:
            settings = load_planning_settings()
        except ValueError:
            # Let the shared composer report the same safe configuration fallback.
            pass
    if settings is not None:
        settings = settings.model_copy(update={"max_completion_tokens": min(settings.max_completion_tokens, max(1024, index * 96 + 512))})
    wording, generation = planning_wording(parsed, module=submission.module, settings=settings, client=client,
        report_records=(groups, substitutions, mapping, fallback))
    sections = [ModuleSection(**{key: value for key, value in definition.items() if key != "facts"}, text=wording[definition["section_id"]]) for definition in definitions]
    return sections, ModuleGenerationInfo.model_validate(generation.model_dump(exclude={"output_validation"}))
