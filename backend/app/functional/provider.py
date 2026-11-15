"""Only normalized fictional decision facts leave; no identifiers or free text."""
from collections import Counter

def provider_evidence(parsed, context, plan):
    teeth = {t.id:f'T{i:03d}' for i,t in enumerate(parsed.teeth,1)}
    cells = {m.id:f'E{i:04d}' for i,m in enumerate(parsed.measurements,1)}
    phases = {p.phase_id:f'P{i:03d}' for i,p in enumerate(context.phases,1)}
    stages = {s.stage_id:f'S{i:03d}' for i,s in enumerate(plan.stages,1)}
    def target(t):
        return dict(measurement=cells[t.measurement_ref],amount=t.amount,unit=t.unit,
            label=t.source_direction if t.source_direction in {'D','M','B','L','E','I'} else None)
    payload = dict(policy_set_version=plan.policy_set_version,origin=plan.origin,clinical_authorized=False,
        # Policy, status and source refs already accompany each finding in sections.
        # Send only additional choices here, linked to that same finding.
        decisions=[dict(finding=d.finding_id,targets=[target(t) for t in d.proposed_changes],
            attachment_primary=d.attachment_primary,attachment_alternative=d.attachment_alternative)
            for d in plan.decisions if d.proposed_changes or d.attachment_primary or d.attachment_alternative],
        catalog=[dict(concept=o.concept,dimensions=o.geometry.model_dump() if o.geometry else None,orientation=o.orientation,
            surface=o.surface,placement=o.placement.model_dump() if o.placement else None) for o in context.attachment_options],
        stage_basis=context.stage_value_basis,
        # Tooth/family/label are referenced through the shared evidence dictionary.
        stage_value_columns=['measurement','amount','unit'],
        stages=[dict(stage=stages[s.stage_id],order=s.order,phase=phases.get(s.phase_id),duration_days=s.duration_days,
            values=[[cells[m.measurement_ref],m.amount,m.unit] for m in s.movements]) for s in plan.stages],
        allocation_check_columns=['measurement','source_total','allocated_total','unit','status'],
        allocation_checks=[[cells[c.measurement_ref],c.source_total,c.allocated_total,c.unit,c.status] for c in plan.allocation_checks],
        supports=[dict(phase=phases.get(c.phase_id),support=[teeth.get(r) for r in c.support_tooth_refs],active=[teeth.get(r) for r in c.active_tooth_refs],assumption=c.assumption) for c in context.support_constraints],
        checks=[dict(code=c.code,status=c.status) for c in plan.checks])
    if sum(len(s.movements) for s in plan.stages) > 32:
        # Wording only arranges immutable local findings. Large stage datasets use
        # bounded metadata/counts; complete values and checks remain in the report.
        payload.update(stage_detail_scope='METADATA_ONLY_COMPLETE_FINDINGS_RETAINED_LOCALLY',
            stage_value_columns=[],stages=[dict(stage=stages[s.stage_id],order=s.order,
                phase=phases.get(s.phase_id),duration_days=s.duration_days,
                records=len(s.movements),unknown_amounts=sum(m.amount is None or m.unit is None for m in s.movements)) for s in plan.stages],
            allocation_check_scope='COUNTS_ONLY_COMPLETE_CHECKS_RETAINED_LOCALLY',
            allocation_check_columns=[],allocation_checks=[],
            allocation_check_counts=dict(Counter(c.status for c in plan.allocation_checks)))
    return payload
