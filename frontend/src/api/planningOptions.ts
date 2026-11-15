import type { AttachmentOption, MovementTarget, FunctionalContext } from './functional'
import { isFunctionalContext } from './functional'

export interface PlanningOptions {
  policy_mode: 'SYNTHETIC_REVIEW' | 'EVIDENCE_REVIEW'
  source_sha256: string | null
  objectives: string[]
  source_convention: 'UNSPECIFIED' | 'SOURCE_LABELS_AS_RECORDED'
  illustration: 'NONE' | 'HALF_MAGNITUDE'
  illustration_measurement_ref: string | null
  targets: MovementTarget[]
  attachment_options: AttachmentOption[]
  catalog_policy: 'CONCEPTS_WITH_SUPPLIED_SPECS' | 'SUPPLIED_OPTIONS_ONLY'
  phases: FunctionalContext['phases']
  stage_value_basis: FunctionalContext['stage_value_basis']
  support_constraints: FunctionalContext['support_constraints']
}

export const defaultPlanningOptions = (): PlanningOptions => ({ policy_mode: 'SYNTHETIC_REVIEW', source_sha256: null, objectives: [], source_convention: 'UNSPECIFIED', illustration: 'NONE', illustration_measurement_ref: null, targets: [], attachment_options: [], catalog_policy: 'CONCEPTS_WITH_SUPPLIED_SPECS', phases: [], stage_value_basis: 'UNSPECIFIED', support_constraints: [] })

export function isPlanningOptions(value: unknown): value is PlanningOptions {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false
  const v = value as Record<string, unknown>
  return ['SYNTHETIC_REVIEW', 'EVIDENCE_REVIEW'].includes(String(v.policy_mode))
    && (v.source_sha256 === null || typeof v.source_sha256 === 'string' && /^[a-f0-9]{64}$/.test(v.source_sha256))
    && ['UNSPECIFIED', 'SOURCE_LABELS_AS_RECORDED'].includes(String(v.source_convention))
    && ['NONE', 'HALF_MAGNITUDE'].includes(String(v.illustration))
    && (v.illustration_measurement_ref === null || typeof v.illustration_measurement_ref === 'string' && v.illustration_measurement_ref.length <= 80)
    && ['CONCEPTS_WITH_SUPPLIED_SPECS', 'SUPPLIED_OPTIONS_ONLY'].includes(String(v.catalog_policy))
    && isFunctionalContext({ scenario_id: null, policy_version: '1.0.0', origin: 'INPUT_DRIVEN_POLICY_REVIEW', module: 'macro', source_sha256: v.source_sha256 ?? '0'.repeat(64), notation: 'UNVERIFIED', objectives: v.objectives, targets: v.targets, attachment_options: v.attachment_options, phases: v.phases, stage_value_basis: v.stage_value_basis, support_constraints: v.support_constraints })
}
