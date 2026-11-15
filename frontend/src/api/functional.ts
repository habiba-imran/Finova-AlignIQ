import type { ParseResult } from './parse'
import type { AnalyticalFinding, DemoModule, ReviewDetails } from './interactive'

export type Concept = 'RECTANGULAR' | 'VERTICAL_RECTANGULAR' | 'HORIZONTAL_RECTANGULAR' | 'OVAL' | 'OPTIMIZED_STYLE' | 'NO_ATTACHMENT'
export interface AttachmentOption { concept: Concept; geometry: { width_mm: string; height_mm: string; depth_mm: string } | null; orientation: 'VERTICAL' | 'HORIZONTAL' | 'UNSPECIFIED' | null; surface: 'BUCCAL' | 'LINGUAL' | null; placement: { frame: 'FICTIONAL_TOOTH_LOCAL_MM'; x_mm: string; y_mm: string; z_mm: string } | null }
export interface MovementTarget { measurement_ref: string; amount: string; unit: 'mm' | 'deg'; source_direction: string | null }
export interface FunctionalContext { scenario_id: string; policy_version: '1.0.0'; source_sha256: string; module: DemoModule; origin: 'EXPLICIT_SYNTHETIC_SCENARIO'; notation: 'FDI' | 'UNVERIFIED'; objectives: string[]; targets: MovementTarget[]; attachment_options: AttachmentOption[]; phases: { phase_id: string; label: string; stage_ids: string[] }[]; stage_value_basis: 'UNSPECIFIED' | 'INCREMENTS_MATCH_SOURCE_LABELS'; support_constraints: { phase_id: string; support_tooth_refs: string[]; active_tooth_refs: string[]; assumption: 'STATIONARY_IN_FICTIONAL_SCENARIO' }[] }
export interface Decision { decision_id: string; finding_id: string; policy_id: string; policy_version: '1.0.0'; dimension: string; status: 'ILLUSTRATIVE_PROPOSAL' | 'INSUFFICIENT_INFORMATION' | 'NOT_APPLICABLE' | 'CONFLICT'; tooth_refs: string[]; measurement_refs: string[]; context_refs: string[]; rationale: string; proposal: string; alternative: string | null; missing_fields: string[]; proposed_changes: MovementTarget[]; attachment_primary: Concept | null; attachment_alternative: Concept | null }
export interface Candidate { tooth_ref: string; decision_id: string; movement_refs: string[]; primary: Concept | null; alternative: Concept | null; outcome: 'CANDIDATE' | 'NO_ATTACHMENT' | 'INSUFFICIENT_INFORMATION'; missing_fields: string[] }
export interface StageMovement { tooth_ref: string; measurement_ref: string; amount: string | null; unit: 'mm' | 'deg' | null; source_direction: string | null }
export interface FunctionalPlan { policy_set_version: '1.0.0'; origin: 'INDEPENDENT_SYNTHETIC_POLICIES'; clinical_authorized: false; source_sha256: string; decisions: Decision[]; attachment_rows: Candidate[]; stages: { stage_id: string; order: number; phase_id: string | null; duration_days: number | null; movements: StageMovement[]; decision_ids: string[] }[]; allocation_checks: { measurement_ref: string; source_total: string | null; allocated_total: string | null; unit: 'mm' | 'deg' | null; status: 'MATCH' | 'MISMATCH' | 'UNAVAILABLE' | 'NOT_COMPARABLE' }[]; checks: { code: string; status: 'PASS' | 'CONFLICT' | 'UNAVAILABLE'; message: string; source_refs: string[] }[] }
export interface FunctionalScenario { label: string; module: DemoModule; raw_text: string; planning_context: FunctionalContext; review_details: ReviewDetails }
export const FUNCTIONAL_SECTIONS = {
  macro: { SAGITTAL: 'Sagittal proposals', TRANSVERSE: 'Transverse proposals', VERTICAL: 'Vertical proposals', ADDITIONAL: 'Additional considerations' },
  micro: { ATTACHMENT_OPTIONS: 'Tooth-wise attachment options', ATTACHMENT_SCOPE: 'Attachment assumptions and limits' },
  nano: { PHASES: 'Ordered phases and movements', STAGE_CHECKS: 'Stage consistency checks', ANCHORAGE: 'Illustrative anchorage review', SEQUENCE_SCOPE: 'Sequencing assumptions and limits' },
}
export const CONCEPT_LABELS: Record<Concept, string> = { RECTANGULAR: 'Rectangular', VERTICAL_RECTANGULAR: 'Vertical rectangular', HORIZONTAL_RECTANGULAR: 'Horizontal rectangular', OVAL: 'Ellipsoid / oval', OPTIMIZED_STYLE: 'Optimized-style category (geometry unspecified)', NO_ATTACHMENT: 'No attachment in this fictional scenario' }
export const SCENARIOS = [{ id: 'macro-distribution', label: 'Load Macro planning scenario' }, { id: 'micro-catalog', label: 'Load Micro attachment scenario' }, { id: 'nano-phases', label: 'Load Nano sequencing scenario' }]
const obj = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(str)
const scalar = (v: unknown) => str(v) && v.length <= 24 && /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(v)
const nullable = (v: unknown) => v === null || scalar(v)
const concept = (v: unknown): v is Concept => str(v) && Object.hasOwn(CONCEPT_LABELS, v)
const canonical = (v: unknown): string => JSON.stringify(v, (_key, item: unknown) => obj(item) ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a.localeCompare(b))) : item)
export const decisionText = (d: Decision) => [d.rationale, d.proposal, d.alternative ? 'Alternative: ' + d.alternative : '', d.missing_fields.length ? 'Information needed: ' + d.missing_fields.join('; ') + '.' : ''].filter(Boolean).map(s => s.trim()).join(' ')

export function isFunctionalContext(v: unknown): v is FunctionalContext {
  if (!obj(v) || v.policy_version !== '1.0.0' || v.origin !== 'EXPLICIT_SYNTHETIC_SCENARIO' || !str(v.scenario_id) || !/^[a-zA-Z0-9_-]{1,60}$/.test(v.scenario_id)
    || !str(v.source_sha256) || !/^[a-f0-9]{64}$/.test(v.source_sha256) || !['macro', 'micro', 'nano'].includes(String(v.module)) || !['FDI', 'UNVERIFIED'].includes(String(v.notation))
    || !strings(v.objectives) || !v.objectives.every(x => ['REDISTRIBUTE_TRANSLATIONS', 'ANGULAR_CONTROL', 'VERTICAL_REVIEW', 'STAGE_REVIEW'].includes(x))
    || new Set(v.objectives).size !== v.objectives.length || !['UNSPECIFIED', 'INCREMENTS_MATCH_SOURCE_LABELS'].includes(String(v.stage_value_basis))
    || !Array.isArray(v.targets) || v.targets.length > 64 || !v.targets.every(t => obj(t) && str(t.measurement_ref) && scalar(t.amount) && ['mm', 'deg'].includes(String(t.unit)) && (t.source_direction === null || str(t.source_direction)))
    || !Array.isArray(v.attachment_options) || v.attachment_options.length > 6 || !v.attachment_options.every(o => obj(o) && concept(o.concept)
      && (o.geometry === null || obj(o.geometry) && ['width_mm', 'height_mm', 'depth_mm'].every(k => scalar((o.geometry as Record<string, unknown>)[k]) && Number((o.geometry as Record<string, unknown>)[k]) > 0))
      && [null, 'VERTICAL', 'HORIZONTAL', 'UNSPECIFIED'].includes(o.orientation as null | string) && [null, 'BUCCAL', 'LINGUAL'].includes(o.surface as null | string)
      && (o.placement === null || obj(o.placement) && o.placement.frame === 'FICTIONAL_TOOTH_LOCAL_MM' && ['x_mm', 'y_mm', 'z_mm'].every(k => scalar((o.placement as Record<string, unknown>)[k]))))
    || !Array.isArray(v.phases) || v.phases.length > 16 || !v.phases.every(p => obj(p) && str(p.phase_id) && str(p.label) && strings(p.stage_ids) && p.stage_ids.length > 0)
    || !Array.isArray(v.support_constraints) || v.support_constraints.length > 16 || !v.support_constraints.every(c => obj(c) && str(c.phase_id) && strings(c.support_tooth_refs) && strings(c.active_tooth_refs) && c.assumption === 'STATIONARY_IN_FICTIONAL_SCENARIO')) return false
  const context = v as unknown as FunctionalContext
  return new Set(context.attachment_options.map(o => o.concept)).size === context.attachment_options.length
}

export function isFunctionalPlan(v: unknown, c: FunctionalContext, parsed: ParseResult, details: ReviewDetails, findings: AnalyticalFinding[]): v is FunctionalPlan {
  if (!obj(v) || v.policy_set_version !== '1.0.0' || v.origin !== 'INDEPENDENT_SYNTHETIC_POLICIES' || v.clinical_authorized !== false || v.source_sha256 !== parsed.raw_sha256
    || c.source_sha256 !== parsed.raw_sha256 || !['decisions', 'attachment_rows', 'stages', 'allocation_checks', 'checks'].every(k => Array.isArray(v[k]))) return false
  const teeth = new Set(parsed.teeth.map(t => t.id)), measurements = new Map(parsed.measurements.map(m => [m.id, m]))
  const ids = new Set<string>(), factMap = new Map(findings.map(f => [f.finding_id, f]))
  if (!(v.decisions as unknown[]).every(d => {
    if (!obj(d) || !str(d.decision_id) || ids.has(d.decision_id) || !str(d.finding_id) || !factMap.has(d.finding_id) || !str(d.policy_id)
      || !/^DEMO-(PLAN|ATT|STAGE)-[A-Z-]+-v1$/.test(d.policy_id) || d.policy_version !== '1.0.0'
      || !['ILLUSTRATIVE_PROPOSAL', 'INSUFFICIENT_INFORMATION', 'NOT_APPLICABLE', 'CONFLICT'].includes(String(d.status)) || !str(d.dimension)
      || !strings(d.tooth_refs) || !d.tooth_refs.every(t => teeth.has(t)) || !strings(d.measurement_refs) || !d.measurement_refs.every(r => measurements.has(r))
      || !strings(d.context_refs) || !d.context_refs.every(r => /^(planning_context|review_details)(\/|$)/.test(r))
      || !str(d.rationale) || !str(d.proposal) || !(d.alternative === null || str(d.alternative)) || !strings(d.missing_fields)
      || !(d.attachment_primary === null || concept(d.attachment_primary)) || !(d.attachment_alternative === null || concept(d.attachment_alternative))
      || !Array.isArray(d.proposed_changes) || !d.proposed_changes.every(t => c.targets.some(target => canonical(target) === canonical(t)))) return false
    const decision = d as unknown as Decision, f = factMap.get(decision.finding_id)!
    if (f.text !== decisionText(decision) || f.demo_rule !== d.policy_id || f.kind !== d.status || f.section_id !== d.dimension
      || canonical(f.source_refs) !== canonical(d.measurement_refs) || f.origin !== 'SIMULATED_DEMO') return false
    ids.add(d.decision_id); return true
  }) || ids.size !== findings.length) return false
  const catalog = new Set(c.attachment_options.map(o => o.concept)), seen = new Set<string>()
  if (!(v.attachment_rows as unknown[]).every(row => {
    if (!obj(row) || !str(row.tooth_ref) || seen.has(row.tooth_ref) || !teeth.has(row.tooth_ref) || !str(row.decision_id) || !ids.has(row.decision_id)
      || !strings(row.movement_refs) || !row.movement_refs.every(ref => measurements.get(ref)?.tooth_ref === row.tooth_ref) || !strings(row.missing_fields)
      || !(row.primary === null || concept(row.primary) && catalog.has(row.primary)) || !(row.alternative === null || concept(row.alternative) && catalog.has(row.alternative))
      || (row.outcome === 'CANDIDATE' ? row.primary === null || row.primary === 'NO_ATTACHMENT' : row.outcome === 'NO_ATTACHMENT' ? row.primary !== 'NO_ATTACHMENT' : row.outcome !== 'INSUFFICIENT_INFORMATION' || row.primary !== null)) return false
    const decision = (v.decisions as unknown as Decision[]).find(d => d.decision_id === row.decision_id)!
    if (row.primary !== decision.attachment_primary || row.alternative !== decision.attachment_alternative) return false
    seen.add(row.tooth_ref); return true
  }) || (c.module === 'micro' ? seen.size !== parsed.teeth.length : seen.size !== 0)) return false
  const stageIds = new Set<string>()
  if (!(v.stages as unknown[]).every(s => {
    if (!obj(s) || !str(s.stage_id) || stageIds.has(s.stage_id) || !Number.isInteger(s.order)
      || !details.stages.some(t => t.stage_id === s.stage_id && t.order === s.order && t.duration_days === s.duration_days)
      || !(s.phase_id === null || c.phases.some(p => p.phase_id === s.phase_id && p.stage_ids.includes(s.stage_id as string)))
      || !strings(s.decision_ids) || !s.decision_ids.every(id => ids.has(id)) || !Array.isArray(s.movements)) return false
    if (!s.movements.every(m => obj(m) && str(m.measurement_ref) && str(m.tooth_ref) && measurements.get(m.measurement_ref)?.tooth_ref === m.tooth_ref
      && nullable(m.amount) && [null, 'mm', 'deg'].includes(m.unit as null | string)
      && m.source_direction === (c.stage_value_basis === 'INCREMENTS_MATCH_SOURCE_LABELS' ? measurements.get(m.measurement_ref)?.raw_direction : null)
      && details.allocations.some(a => a.stage_id === s.stage_id && a.tooth_ref === m.tooth_ref && a.measurement_ref === m.measurement_ref && a.amount === m.amount && a.unit === m.unit))) return false
    stageIds.add(s.stage_id); return true
  })) return false
  return (v.allocation_checks as unknown[]).every(a => obj(a) && str(a.measurement_ref) && measurements.has(a.measurement_ref)
    && nullable(a.source_total) && nullable(a.allocated_total) && (a.source_total === null || a.source_total === measurements.get(a.measurement_ref)?.signed_decimal)
    && a.unit === measurements.get(a.measurement_ref)?.unit && ['MATCH', 'MISMATCH', 'UNAVAILABLE', 'NOT_COMPARABLE'].includes(String(a.status)))
    && (v.checks as unknown[]).every(check => obj(check) && str(check.code) && str(check.message) && ['PASS', 'CONFLICT', 'UNAVAILABLE'].includes(String(check.status)) && strings(check.source_refs) && check.source_refs.every(ref => measurements.has(ref)))
}

export async function requestFunctionalScenario(id: string, signal: AbortSignal): Promise<FunctionalScenario> {
  const response = await fetch(`/api/v1/interactive/scenarios/${encodeURIComponent(id)}`, { signal, cache: 'no-store' })
  if (!response.ok) throw new Error('SCENARIO_UNAVAILABLE')
  const data: unknown = await response.json()
  if (!obj(data) || !str(data.label) || !str(data.raw_text) || !isFunctionalContext(data.planning_context) || data.planning_context.scenario_id !== id
    || data.module !== data.planning_context.module || !obj(data.review_details) || !['attachments', 'stages', 'allocations', 'anchorage_notes'].every(k => Array.isArray((data.review_details as Record<string, unknown>)[k]))) throw new Error('INVALID_SCENARIO')
  return data as unknown as FunctionalScenario
}
