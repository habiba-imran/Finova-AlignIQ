"""Only normalized fictional decision facts leave; no identifiers or free text."""
def provider_evidence(parsed, context, plan):
    teeth = {t.id:f'T{i:03d}' for i,t in enumerate(parsed.teeth,1)}
    cells = {m.id:f'E{i:04d}' for i,m in enumerate(parsed.measurements,1)}
    phases = {p.phase_id:f'P{i:03d}' for i,p in enumerate(context.phases,1)}
    stages = {s.stage_id:f'S{i:03d}' for i,s in enumerate(plan.stages,1)}
    def target(t):
        return dict(measurement=cells[t.measurement_ref],amount=t.amount,unit=t.unit,
            label=t.source_direction if t.source_direction in {'D','M','B','L','E','I'} else None)
    return dict(policy_set_version=plan.policy_set_version,origin=plan.origin,clinical_authorized=False,
        decisions=[dict(policy=d.policy_id,status=d.status,teeth=[teeth[t] for t in d.tooth_refs],
            source=[cells[r] for r in d.measurement_refs],targets=[target(t) for t in d.proposed_changes],
            attachment_primary=d.attachment_primary,attachment_alternative=d.attachment_alternative) for d in plan.decisions],
        catalog=[dict(concept=o.concept,dimensions=o.geometry.model_dump() if o.geometry else None,orientation=o.orientation,
            surface=o.surface,placement=o.placement.model_dump() if o.placement else None) for o in context.attachment_options],
        stage_basis=context.stage_value_basis,
        stages=[dict(stage=stages[s.stage_id],order=s.order,phase=phases.get(s.phase_id),duration_days=s.duration_days,
            values=[dict(tooth=teeth[m.tooth_ref],measurement=cells[m.measurement_ref],amount=m.amount,unit=m.unit,
                label=m.source_direction if m.source_direction in {'D','M','B','L','E','I'} else None) for m in s.movements]) for s in plan.stages],
        allocation_checks=[dict(measurement=cells[c.measurement_ref],source_total=c.source_total,allocated_total=c.allocated_total,unit=c.unit,status=c.status) for c in plan.allocation_checks],
        supports=[dict(phase=phases.get(c.phase_id),support=[teeth.get(r) for r in c.support_tooth_refs],active=[teeth.get(r) for r in c.active_tooth_refs],assumption=c.assumption) for c in context.support_constraints],
        checks=[dict(code=c.code,status=c.status) for c in plan.checks])
