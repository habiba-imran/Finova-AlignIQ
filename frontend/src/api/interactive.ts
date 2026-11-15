import { isParseResult } from './parse'
import type { ContextClaims, Measurement, ParseResult } from './parse'
import { isDraftReview } from './review'
import type { DraftReview } from './review'
import { FUNCTIONAL_SECTIONS, isFunctionalContext, isFunctionalPlan } from './functional'
import type { FunctionalContext, FunctionalPlan } from './functional'

export type DemoModule = 'macro' | 'micro' | 'nano'
export interface AttachmentDetail {
  tooth_ref: string; choice: 'UNKNOWN' | 'ATTACHMENT' | 'NO_ATTACHMENT'; design: string | null
  width_mm: string | null; height_mm: string | null; depth_mm: string | null; surface: string | null; orientation: string | null
}
export interface SuppliedStage { stage_id: string; order: number; duration_days: number | null }
export interface SuppliedAllocation { stage_id: string; tooth_ref: string; measurement_ref: string; amount: string | null; unit: 'mm' | 'deg' | null }
export interface AnchorageNote { tooth_ref: string | null; note: string }
export interface ReviewDetails { attachments: AttachmentDetail[]; stages: SuppliedStage[]; allocations: SuppliedAllocation[]; anchorage_notes: AnchorageNote[] }
export const emptyReviewDetails = (): ReviewDetails => ({ attachments: [], stages: [], allocations: [], anchorage_notes: [] })
export interface ModuleSection { section_id: string; title: string; status: 'SOURCE_REPORTED' | 'SUPPLIED_UNVERIFIED' | 'UNAVAILABLE' | 'SIMULATED_DEMO'; text: string; source_refs: string[]; missing_fields: string[] }
export interface AnalyticalFinding { finding_id: string; section_id: string; kind: string; text: string; source_refs: string[]; selected_refs: string[]; demo_rule: string | null; origin: 'DESCRIPTIVE_COMPARISON' | 'SIMULATED_DEMO' }
export const ANALYTICAL_SECTIONS = {
  macro: { SAGITTAL: 'Sagittal / Mesiodistal movement', TRANSVERSE: 'Transverse / Buccolingual movement', VERTICAL: 'Vertical movement', ANGULAR: 'Additional angular observations', SUMMARY: 'Overall movement summary' },
  micro: { ANGULAR_FOCUS: 'Priority tooth profiles', ATTACHMENT_DEMO: 'Illustrative attachment considerations', ANGULAR_COVERAGE: 'Angular review coverage', ATTACHMENT_SCOPE: 'Attachment review scope' },
  nano: { DISTRIBUTION: 'Arch and tooth-group distribution', TRANSLATIONS: 'Translation concentrations', VERTICAL_PATTERNS: 'Vertical concentrations', MULTI_COMPONENT: 'Multiple notable components', SEQUENCE_REVIEW: 'Sequencing review considerations' },
}
export const MODULE_SECTIONS = {
  micro: { ATTACHMENT_RECORDS: 'Supplied attachment choices', ATTACHMENT_DESIGN: 'Design and dimensions', ATTACHMENT_PLACEMENT: 'Placement information', ATTACHMENT_LIMITS: 'Attachment review limits' },
  nano: { STAGE_RECORDS: 'Supplied stage information', STAGE_ALLOCATIONS: 'Supplied movement allocations', ANCHORAGE_RECORDS: 'Supplied anchorage notes', SEQUENCING_LIMITS: 'Sequencing review limits' },
}
export const TMT_SECTIONS = {
  micro: { ATTACHMENT_RECORDS: 'Rotation review', ATTACHMENT_DESIGN: 'Angulation and inclination review', ATTACHMENT_PLACEMENT: 'Movement coverage', ATTACHMENT_LIMITS: 'Attachment decisions' },
  nano: { STAGE_RECORDS: 'Movement context', STAGE_ALLOCATIONS: 'Translation review', ANCHORAGE_RECORDS: 'Vertical movement review', SEQUENCING_LIMITS: 'Sequencing decisions' },
}
export function sectionStatusLabel(section: ModuleSection): string {
  return section.status === 'SIMULATED_DEMO' ? 'Illustration only · unvalidated'
    : section.status === 'SOURCE_REPORTED' ? 'From TMT · unverified'
    : section.status === 'SUPPLIED_UNVERIFIED' ? 'Supplied · unverified'
      : section.section_id.endsWith('_LIMITS') && !section.missing_fields.length ? 'Not prescribed' : 'Unavailable'
}
export interface InteractiveReport {
  schema_version: '1.0.0'; module: DemoModule; report_id: string
  draft_status: 'Synthetic demonstration — not for clinical use'; clinical_analysis_enabled: false
  parsed: ParseResult; engine_review: DraftReview
  generation: { requested_mode: 'AUTO'; used_mode: 'GROQ_AI' | 'STANDARD_TEMPLATES'; reason: string; attempts: number; accepted_comments: number; real_patient_transmission_enabled: false
    provider: 'GROQ' | null; model: 'openai/gpt-oss-120b' | null; eligible_wording_findings: number; output_validation: 'CLOSED_WORDING_AND_LOCAL_FACTS_V1' | 'GROUNDED_PLANNING_WORDING_V1' | 'GROUNDED_MODULE_WORDING_V1' | 'GROUNDED_ANALYTICAL_WORDING_V1' }
  wording_notice: string; summary: string; export_text: string; limitations: string[]
  observations: { tooth_ref: string; original_tooth: string; text: string; evidence_status: 'PARSED_SOURCE_ONLY'; measurements: Measurement[] }[]
  illustrations: { tooth_ref: string; original_tooth: string; label: string; text: string; origin: 'SIMULATED_DEMO'; clinical_status: 'NOT_EVALUATED' }[]
  report_format?: 'MOVEMENT_PROFILE_V1' | 'MODULE_SPECIFIC_V1' | 'ANALYTICAL_V1' | 'FUNCTIONAL_DEMO_V1'
  planning_context?: FunctionalContext | null
  functional_plan?: FunctionalPlan | null
  analytical_findings?: AnalyticalFinding[]
  sections?: ModuleSection[]
  review_details?: ReviewDetails
}
const obj = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
export function isInteractiveReport(v: unknown): v is InteractiveReport {
  if (!obj(v) || v.schema_version !== '1.0.0' || !['macro', 'micro', 'nano'].includes(String(v.module))
    || !str(v.report_id) || !/^[a-f0-9]{64}$/.test(v.report_id) || v.clinical_analysis_enabled !== false
    || v.draft_status !== 'Synthetic demonstration — not for clinical use' || !isParseResult(v.parsed) || !isDraftReview(v.engine_review)
    || v.parsed.raw_sha256 !== v.engine_review.raw_sha256 || !obj(v.generation) || v.generation.requested_mode !== 'AUTO'
    || !['GROQ_AI', 'STANDARD_TEMPLATES'].includes(String(v.generation.used_mode)) || v.generation.real_patient_transmission_enabled !== false
    || !str(v.generation.reason) || !Number.isInteger(v.generation.attempts) || Number(v.generation.attempts) < 0
    || Number(v.generation.attempts) > 2 || !Number.isInteger(v.generation.accepted_comments)
    || !Array.isArray(v.observations) || !v.observations.length
    || (v.generation.output_validation === 'GROUNDED_PLANNING_WORDING_V1'
      ? v.generation.eligible_wording_findings !== v.observations.length
      : v.generation.output_validation === 'GROUNDED_MODULE_WORDING_V1'
        ? v.report_format !== 'MODULE_SPECIFIC_V1' || v.module === 'macro' || v.generation.eligible_wording_findings !== 4
        : v.generation.output_validation === 'GROUNDED_ANALYTICAL_WORDING_V1'
          ? !['ANALYTICAL_V1', 'FUNCTIONAL_DEMO_V1'].includes(String(v.report_format)) || !Array.isArray(v.sections) || v.generation.eligible_wording_findings !== v.sections.length
          : v.generation.output_validation !== 'CLOSED_WORDING_AND_LOCAL_FACTS_V1' || v.generation.eligible_wording_findings !== 4)
    || (Number(v.generation.attempts) > 0 ? v.generation.provider !== 'GROQ' || v.generation.model !== 'openai/gpt-oss-120b' : v.generation.provider !== null || v.generation.model !== null)
    || (v.generation.used_mode === 'GROQ_AI' ? v.generation.accepted_comments !== v.generation.eligible_wording_findings || Number(v.generation.attempts) < 1 || v.generation.reason !== 'GROQ_VALIDATED' : v.generation.accepted_comments !== 0)
    || !['wording_notice', 'summary', 'export_text'].every(k => str(v[k])) || !Array.isArray(v.limitations) || !v.limitations.every(str)
    || !Array.isArray(v.observations) || !v.observations.length || !Array.isArray(v.illustrations)) return false
  const parsed = v.parsed, observed: string[] = [], toothRefs = new Set<string>()
  if (!v.observations.every(o => {
    if (!obj(o) || !str(o.tooth_ref) || !str(o.original_tooth) || !str(o.text) || o.evidence_status !== 'PARSED_SOURCE_ONLY'
      || !parsed.teeth.some(t => t.id === o.tooth_ref && t.raw_identifier === o.original_tooth) || !Array.isArray(o.measurements) || !o.measurements.length) return false
    if (toothRefs.has(o.tooth_ref)) return false
    toothRefs.add(o.tooth_ref)
    return o.measurements.every(m => {
      if (!obj(m) || !str(m.id) || m.tooth_ref !== o.tooth_ref) return false
      const source = parsed.measurements.find(p => p.id === m.id)
      if (!source || JSON.stringify(source) !== JSON.stringify(m)) return false
      observed.push(m.id); return true
    })
  }) || new Set(observed).size !== observed.length || observed.length !== parsed.measurements.length) return false
  if (v.report_format !== 'FUNCTIONAL_DEMO_V1' && (v.planning_context != null || v.functional_plan != null)) return false
  if (v.report_format === 'ANALYTICAL_V1' || v.report_format === 'FUNCTIONAL_DEMO_V1') {
    const functional = v.report_format === 'FUNCTIONAL_DEMO_V1'
    if (v.illustrations.length || !Array.isArray(v.sections) || !isReviewDetails(v.review_details)
      || !functional && Object.values(v.review_details).some(rows => rows.length) || !Array.isArray(v.analytical_findings)
      || v.generation.output_validation !== 'GROUNDED_ANALYTICAL_WORDING_V1') return false
    const expected = (functional ? FUNCTIONAL_SECTIONS : ANALYTICAL_SECTIONS)[v.module as DemoModule] as Record<string, string>
    const knownRefs = new Set(parsed.measurements.map(m => m.id)), ids = new Set<string>()
    if (v.sections.length !== Object.keys(expected).length) return false
    if (!v.analytical_findings.every(f => {
      if (!obj(f) || !str(f.finding_id) || ids.has(f.finding_id) || !/^F\d{4}$/.test(f.finding_id)
        || !str(f.section_id) || !(f.section_id in expected) || !str(f.kind) || !str(f.text) || !f.text.trim()
        || !Array.isArray(f.source_refs) || !f.source_refs.every(ref => str(ref) && knownRefs.has(ref))
        || !Array.isArray(f.selected_refs) || !f.selected_refs.every(ref => str(ref) && (f.source_refs as unknown[]).includes(ref))
        || !['DESCRIPTIVE_COMPARISON', 'SIMULATED_DEMO'].includes(String(f.origin))
        || (f.origin === 'SIMULATED_DEMO' ? !str(f.demo_rule) || !/^DEMO-[A-Z-]+-v1$/.test(f.demo_rule) : f.demo_rule !== null)) return false
      ids.add(f.finding_id); return true
    })) return false
    const findings = v.analytical_findings as AnalyticalFinding[], seen = new Set<string>()
    if (functional && (!isFunctionalContext(v.planning_context) || v.planning_context.module !== v.module
      || !isFunctionalPlan(v.functional_plan, v.planning_context, parsed, v.review_details, findings))) return false
    if (!functional && (v.planning_context != null || v.functional_plan != null)) return false
    return v.sections.every(s => {
      if (!obj(s) || !str(s.section_id) || seen.has(s.section_id) || s.title !== expected[s.section_id]
        || !str(s.text) || !Array.isArray(s.source_refs) || !s.source_refs.every(ref => str(ref) && knownRefs.has(ref))
        || !Array.isArray(s.missing_fields) || !s.missing_fields.every(str)) return false
      const own = findings.filter(f => f.section_id === s.section_id)
      const status = functional || s.section_id === 'ATTACHMENT_DEMO' ? 'SIMULATED_DEMO' : own.some(f => f.source_refs.length) ? 'SOURCE_REPORTED' : 'UNAVAILABLE'
      if (s.status !== status || !own.length) return false
      const paragraphs = s.text.split(/\n\n/), expectedTexts = own.map(f => f.text)
      if (paragraphs.length !== expectedTexts.length || new Set(paragraphs).size !== paragraphs.length || paragraphs.some(p => !expectedTexts.includes(p))) return false
      if (JSON.stringify([...new Set(own.flatMap(f => f.source_refs))]) !== JSON.stringify(s.source_refs)) return false
      seen.add(s.section_id); return true
    })
  }
  if (v.report_format === 'MODULE_SPECIFIC_V1') {
    if (v.illustrations.length || !Array.isArray(v.sections) || !isReviewDetails(v.review_details)) return false
    const details = v.review_details, knownTeeth = new Set(parsed.teeth.map(tooth => tooth.id))
    if (details.attachments.some(row => !knownTeeth.has(row.tooth_ref)) || new Set(details.attachments.map(row => row.tooth_ref)).size !== details.attachments.length) return false
    const stages = new Set(details.stages.map(stage => stage.stage_id)), allocations = new Set<string>()
    if (stages.size !== details.stages.length || new Set(details.stages.map(stage => stage.order)).size !== details.stages.length) return false
    for (const row of details.allocations) {
      const movement = parsed.measurements.find(m => m.id === row.measurement_ref), key = JSON.stringify([row.stage_id, row.measurement_ref])
      if (!stages.has(row.stage_id) || !movement || movement.tooth_ref !== row.tooth_ref || allocations.has(key)
        || row.amount !== null && movement.unit !== null && row.unit !== movement.unit) return false
      allocations.add(key)
    }
    if (details.anchorage_notes.some(row => row.tooth_ref !== null && !knownTeeth.has(row.tooth_ref))) return false
    if (v.module === 'macro') return v.sections.length === 0 && Object.values(details).every(rows => rows.length === 0)
    if (v.module === 'micro' ? details.stages.length || details.allocations.length || details.anchorage_notes.length : details.attachments.length) return false
    if (v.generation.output_validation !== 'GROUNDED_MODULE_WORDING_V1' || v.sections.length !== 4) return false
    const module = v.module as 'micro' | 'nano'
    const automatic = Object.values(details).every(rows => rows.length === 0) && v.sections[0]?.title === Object.values(TMT_SECTIONS[module])[0]
    const expected = automatic ? TMT_SECTIONS[module] : MODULE_SECTIONS[module], seen = new Set<string>()
    const allowedRefs = new Set(['parsed/source/context', ...parsed.measurements.map(m => m.id), ...Object.entries(details).flatMap(([key, rows]) => rows.map((_: unknown, i: number) => `review_details/${key}/${i}`))])
    return v.sections.every(section => {
      if (!obj(section) || !str(section.section_id) || seen.has(section.section_id) || !(section.section_id in expected)
        || section.title !== expected[section.section_id as keyof typeof expected] || !str(section.text)
        || !(automatic ? ['SOURCE_REPORTED', 'UNAVAILABLE'] : ['SUPPLIED_UNVERIFIED', 'UNAVAILABLE']).includes(String(section.status))
        || section.section_id.endsWith('_LIMITS') && section.status !== 'UNAVAILABLE'
        || !Array.isArray(section.source_refs) || !section.source_refs.every(ref => str(ref) && allowedRefs.has(ref))
        || section.status === 'SOURCE_REPORTED' && !section.source_refs.length
        || !Array.isArray(section.missing_fields) || !section.missing_fields.every(str)) return false
      seen.add(section.section_id); return true
    })
  }
  if (v.report_format !== undefined && v.report_format !== 'MOVEMENT_PROFILE_V1') return false
  if (v.module === 'macro' && v.illustrations.length) return false
  if (v.module !== 'macro' && v.illustrations.length !== v.observations.length) return false
  const illustrated = new Set<string>(), module = v.module, observations = v.observations
  return v.illustrations.every(i => {
    if (!obj(i) || !str(i.tooth_ref) || illustrated.has(i.tooth_ref) || !str(i.original_tooth) || !str(i.text)
      || i.origin !== 'SIMULATED_DEMO' || i.clinical_status !== 'NOT_EVALUATED'
      || i.label !== (module === 'micro' ? 'Illustrative attachment example' : 'Illustrative sequencing example')
      || !observations.some(o => o.tooth_ref === i.tooth_ref && o.original_tooth === i.original_tooth)) return false
    illustrated.add(i.tooth_ref); return true
  })
}

function isReviewDetails(value: unknown): value is ReviewDetails {
  if (!obj(value) || !['attachments', 'stages', 'allocations', 'anchorage_notes'].every(key => Array.isArray(value[key]))) return false
  const exact = (row: unknown, keys: string[]): row is Record<string, unknown> => obj(row) && Object.keys(row).length === keys.length && keys.every(key => key in row)
  const text = (v: unknown, limit: number) => v === null || str(v) && v.length <= limit
  const scalar = (v: unknown, signed = false) => v === null || str(v) && v.length <= 24 && (signed ? /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/ : /^\+?(?:\d+(?:\.\d*)?|\.\d+)$/).test(v)
  if (Object.keys(value).length !== 4) return false
  return (value.attachments as unknown[]).length <= 32 && (value.attachments as unknown[]).every(row => exact(row, ['tooth_ref', 'choice', 'design', 'width_mm', 'height_mm', 'depth_mm', 'surface', 'orientation'])
    && str(row.tooth_ref) && ['UNKNOWN', 'ATTACHMENT', 'NO_ATTACHMENT'].includes(String(row.choice)) && text(row.design, 80)
    && scalar(row.width_mm) && scalar(row.height_mm) && scalar(row.depth_mm) && text(row.surface, 80) && text(row.orientation, 80)
    && (row.choice === 'ATTACHMENT' || [row.design, row.width_mm, row.height_mm, row.depth_mm, row.surface, row.orientation].every(v => v === null)))
    && (value.stages as unknown[]).length <= 64 && (value.stages as unknown[]).every(row => exact(row, ['stage_id', 'order', 'duration_days']) && str(row.stage_id) && row.stage_id.trim().length > 0 && row.stage_id.length <= 40 && Number.isInteger(row.order) && Number(row.order) >= 1 && (row.duration_days === null || Number.isInteger(row.duration_days) && Number(row.duration_days) >= 1))
    && (value.allocations as unknown[]).length <= 128 && (value.allocations as unknown[]).every(row => exact(row, ['stage_id', 'tooth_ref', 'measurement_ref', 'amount', 'unit']) && ['stage_id', 'tooth_ref', 'measurement_ref'].every(key => str(row[key])) && scalar(row.amount, true) && [null, 'mm', 'deg'].includes(row.unit as null | string) && (row.amount === null || row.unit !== null))
    && (value.anchorage_notes as unknown[]).length <= 32 && (value.anchorage_notes as unknown[]).every(row => exact(row, ['tooth_ref', 'note']) && text(row.tooth_ref, 80) && str(row.note) && row.note.trim().length > 0 && row.note.length <= 240)
}

export async function requestInteractiveReview(module: DemoModule, rawText: string, context: ContextClaims, hash: string, receipt: string | null | undefined, signal: AbortSignal, details: ReviewDetails = emptyReviewDetails(), planningContext: FunctionalContext | null = null): Promise<InteractiveReport> {
  const supplied = module === 'micro' ? { ...emptyReviewDetails(), attachments: details.attachments } : module === 'nano' ? { ...details, attachments: [] } : emptyReviewDetails()
  if (!isReviewDetails(supplied)) throw new Error('DETAILS_ERROR:' + (module === 'micro'
    ? 'Check attachment details. Use decimal numbers for dimensions in mm, or leave unknown dimensions blank.'
    : 'Check sequencing details. Stage IDs and positive whole-number orders are required; durations need whole days, amounts need decimal numbers and units, and anchorage notes need text.'))
  const response = await fetch('/api/v1/interactive/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, signal,
    body: JSON.stringify({ module, raw_text: rawText, raw_sha256: hash, source_claim: 'Unknown', context, synthetic_data_confirmed: true, ...(planningContext ? { planning_context: planningContext } : {}), ...(Object.values(supplied).some(rows => rows.length) ? { review_details: supplied } : {}), ...(receipt ? { recovery_receipt: receipt } : {}) }) })
  if (!response.ok) {
    if (response.status === 422) {
      const error = await response.json().catch(() => null)
      const messages: Record<string, string> = {
        FUNCTIONAL_CONTEXT_SOURCE_MISMATCH: 'The fictional scenario belongs to a different table. Reload a scenario or clear it before reviewing.',
        FUNCTIONAL_CONTEXT_MODULE_MISMATCH: 'Use the review module associated with the selected fictional scenario.',
        FUNCTIONAL_CONTEXT_INVALID: 'Check the supplied fictional scenario references, units and catalog options.',
        DETAILS_MODULE_MISMATCH: 'Use attachment details in Micro and stage details in Nano.',
        ATTACHMENT_REFERENCE_INVALID: 'Choose a current tooth for each attachment record, with one record per tooth.',
        ATTACHMENT_CHOICE_CONFLICT: 'Design and placement details require a supplied attachment choice.',
        STAGE_REFERENCE_INVALID: 'Give every stage a unique ID and a unique positive order number.',
        ALLOCATION_REFERENCE_INVALID: 'Each allocation needs an existing stage and a movement from the selected tooth. Remove duplicate allocations.',
        ALLOCATION_UNIT_INVALID: 'Choose an amount unit that matches the selected source movement.',
        ANCHORAGE_REFERENCE_INVALID: 'Enter text for every anchorage note and choose a current tooth or the overall plan.',
      }
      if (error?.detail in messages) throw new Error('DETAILS_ERROR:' + messages[error.detail])
    }
    throw new Error(response.status === 409 ? 'REPARSE_REQUIRED' : response.status === 422 ? 'PARSE_REQUIRED' : 'REVIEW_UNAVAILABLE')
  }
  const data: unknown = await response.json()
  if (!isInteractiveReport(data) || data.module !== module || data.parsed.raw_sha256 !== hash || data.parsed.raw_text !== rawText) throw new Error('INVALID_RESPONSE')
  if (data.report_format === 'MODULE_SPECIFIC_V1' || data.report_format === 'ANALYTICAL_V1' || data.report_format === 'FUNCTIONAL_DEMO_V1') {
    const canonical = (v: unknown): string => JSON.stringify(v, (_key, item: unknown) => obj(item) ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a.localeCompare(b))) : item)
    if (canonical(data.review_details) !== canonical(supplied)) throw new Error('INVALID_RESPONSE')
    if (canonical(data.planning_context ?? null) !== canonical(planningContext)) throw new Error('INVALID_RESPONSE')
  }
  return data
}
