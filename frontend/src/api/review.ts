import type { ContextClaims, SourceClaim } from './parse'

export const ASSESSMENT_OPTIONS = [
  ['SUITABILITY', 'Clinical suitability'], ['PERIODONTAL', 'Periodontal condition'], ['ROOT_BONE', 'Root / bone assessment'],
  ['OCCLUSION', 'Occlusion'], ['IPR', 'IPR'], ['EXTRACTION_SURGERY', 'Extraction / surgery'],
  ['PROGNOSIS', 'Prognosis'], ['ATTACHMENTS', 'Attachments'], ['COLLISIONS', 'Collisions'],
  ['COMPLEX_INTERVENTION', 'Intervention appropriateness'],
] as const
export type AssessmentQuestion = typeof ASSESSMENT_OPTIONS[number][0]

interface Component { name: string; status: 'VERIFIED' | 'TEST_ONLY' | 'UNKNOWN' | 'CONFLICT' | 'INVALID'; canonical_value: string | null }
interface Observation {
  measurement_id: string; raw_tooth_identifier: string; raw_label: string; raw_value: string
  raw_number: string; raw_sign: string | null; raw_direction: string | null; signed_decimal: string; magnitude: string
  verification: 'VERIFIED' | 'TEST_ONLY'; components: Component[]; input_refs: string[]
  source_spans: { line: number; column_start: number }[]
}
export interface ReviewFinding {
  finding_id: string; rule_id: string; rule_version: '2.0.0'; triggering_rules: { rule_id: string; version: '2.0.0' }[]
  tooth_id: string | null; status: string; finding_type: string; message: string; review_status: 'DRAFT'
  evaluated: boolean; applicable: boolean | null; observed_measurements: Observation[]; input_refs: string[]
  missing_required_fields: string[]; evidence_refs: string[]; abstain_reason: string | null; conflict_group: string | null
  summary_counts: Record<string, number>
}
export interface DraftReview {
  schema_version: '1.0.0'; engine_version: '0.2.0'; rule_set_version: '2.0.0-phase2a'; report_id: string
  review_status: 'DRAFT'; intended_for: 'CLINICIAN_REVIEW'; clinical_analysis_enabled: false
  evidence_domain: 'UNVERIFIED' | 'AUTHORIZED_VENDOR' | 'TEST_ONLY'; raw_sha256: string; notice: string
  requested_assessments: AssessmentQuestion[]
  source: { source_claim: SourceClaim; verification_status: 'UNVERIFIED'; context: ContextClaims }
  coverage: { declared_positions: number; eligible_positions: number; unavailable_positions: number; eligible_explicit_zero: number; eligible_nonzero: number; expected_axes: null }
  findings: ReviewFinding[]; evaluations: { rule_id: string; status: string; finding_ids: string[] }[]; limitations: string[]
}
const obj = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
const nullable = (v: unknown) => v === null || str(v)
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(str)
const digest = (v: unknown) => str(v) && /^[a-f0-9]{64}$/.test(v)
const rule = (v: unknown) => str(v) && /^(G(0[1-9]|1[0-8])|D(0[1-9]|1[0-6])|R(0[1-9]|1[0-6])|T0[1-8]|A0[1-6]|H(0[1-9]|1[0-2])|L0[1-6]|N(0[1-9]|1[0-4]))$/.test(v)
const statuses = ['OBSERVED', 'SEMANTICS_UNKNOWN', 'CONTEXT_REQUIRED', 'DISABLED', 'SUPPRESSED', 'NOT_APPLICABLE', 'PARSE_INVALID']

// Validate every rendered field and the draft/clinical boundaries before displaying a response.
export function isDraftReview(v: unknown): v is DraftReview {
  if (!obj(v) || v.schema_version !== '1.0.0' || v.engine_version !== '0.2.0' || v.rule_set_version !== '2.0.0-phase2a'
    || v.review_status !== 'DRAFT' || v.intended_for !== 'CLINICIAN_REVIEW' || v.clinical_analysis_enabled !== false
    || !digest(v.report_id) || !digest(v.raw_sha256) || !str(v.notice)
    || !['UNVERIFIED', 'AUTHORIZED_VENDOR', 'TEST_ONLY'].includes(String(v.evidence_domain)) || !strings(v.limitations)
    || !strings(v.requested_assessments) || !v.requested_assessments.every(q => ASSESSMENT_OPTIONS.some(([id]) => id === q))) return false
  if (!obj(v.source) || v.source.verification_status !== 'UNVERIFIED' || !obj(v.source.context)
    || !['Unknown', 'ClinCheck', 'SureSmile'].includes(String(v.source.source_claim))) return false
  if (!obj(v.coverage) || v.coverage.expected_axes !== null || !['declared_positions', 'eligible_positions', 'unavailable_positions', 'eligible_explicit_zero', 'eligible_nonzero']
    .every(k => Number.isInteger(v.coverage && (v.coverage as Record<string, unknown>)[k]) && Number((v.coverage as Record<string, unknown>)[k]) >= 0)) return false
  if (!Array.isArray(v.findings) || !v.findings.every(f => {
    if (!obj(f) || !digest(f.finding_id) || !rule(f.rule_id) || f.rule_version !== '2.0.0' || f.review_status !== 'DRAFT'
      || !statuses.includes(String(f.status)) || !['TECHNICAL', 'DESCRIPTIVE', 'SAFETY', 'UNAVAILABLE', 'OUTPUT'].includes(String(f.finding_type))
      || !str(f.message) || !nullable(f.tooth_id) || !nullable(f.abstain_reason) || !nullable(f.conflict_group)
      || typeof f.evaluated !== 'boolean' || !(f.applicable === null || typeof f.applicable === 'boolean')
      || !['input_refs', 'missing_required_fields', 'evidence_refs'].every(k => strings(f[k]))
      || !obj(f.summary_counts) || !Object.values(f.summary_counts).every(n => Number.isInteger(n) && Number(n) >= 0)
      || !Array.isArray(f.triggering_rules) || !f.triggering_rules.length || !f.triggering_rules.every(r => obj(r) && rule(r.rule_id) && r.version === '2.0.0')
      || !Array.isArray(f.observed_measurements)) return false
    if (f.status !== 'OBSERVED' && (f.evaluated || f.observed_measurements.length || f.tooth_id !== null)) return false
    if (f.finding_type === 'DESCRIPTIVE' && f.status === 'OBSERVED' && (!String(f.rule_id).startsWith('D') || !f.observed_measurements.length)) return false
    if (f.observed_measurements.length && v.evidence_domain === 'UNVERIFIED') return false
    return f.observed_measurements.every(o => obj(o) && ['measurement_id', 'raw_tooth_identifier', 'raw_label', 'raw_value', 'raw_number', 'signed_decimal', 'magnitude'].every(k => str(o[k]))
      && nullable(o.raw_sign) && nullable(o.raw_direction) && ['VERIFIED', 'TEST_ONLY'].includes(String(o.verification)) && strings(o.input_refs)
      && o.verification === (v.evidence_domain === 'TEST_ONLY' ? 'TEST_ONLY' : 'VERIFIED')
      && /^[+-]?[0-9]+(?:\.[0-9]+)?$/.test(String(o.signed_decimal)) && /^[0-9]+(?:\.[0-9]+)?$/.test(String(o.magnitude))
      && Array.isArray(o.components) && o.components.every(c => obj(c) && str(c.name) && nullable(c.canonical_value) && ['VERIFIED', 'TEST_ONLY', 'UNKNOWN', 'CONFLICT', 'INVALID'].includes(String(c.status)))
      && ['source_application', 'source_version', 'tooth_identifier', 'notation', 'dentition', 'arch', 'axis', 'unit', 'sign', 'direction', 'plan_mode', 'reference_basis', 'scope', 'coordinate_frame']
        .every(name => (o.components as Component[]).some(c => c.name === name && c.status === o.verification && str(c.canonical_value)))
      && !(o.components as Component[]).some(c => c.name === 'plan_mode' && c.canonical_value === 'COMPARISON')
      && (v.evidence_domain !== 'TEST_ONLY' || (o.components as Component[]).some(c => c.name === 'source_application' && c.canonical_value === 'TEST_ONLY'))
      && Array.isArray(o.source_spans) && o.source_spans.every(s => obj(s) && Number.isInteger(s.line) && Number.isInteger(s.column_start)))
  })) return false
  const ids = new Set(v.findings.map(f => (f as ReviewFinding).finding_id))
  return Array.isArray(v.evaluations) && v.evaluations.every(e => obj(e) && rule(e.rule_id) && statuses.includes(String(e.status))
    && strings(e.finding_ids) && e.finding_ids.every(id => ids.has(id)))
}

export async function requestReview(rawText: string, source: SourceClaim, context: ContextClaims, rawHash: string,
  questions: AssessmentQuestion[], signal: AbortSignal, recoveryReceipt?: string): Promise<DraftReview> {
  const response = await fetch('/api/v1/tmt/observations', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ raw_text: rawText, source_claim: source, context, synthetic_data_confirmed: true, requested_assessments: questions,
      ...(recoveryReceipt ? { recovery_receipt: recoveryReceipt } : {}) }),
    signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer',
  })
  if (!response.ok) throw new Error(response.status === 409 ? 'REPARSE_REQUIRED' : response.status === 413 ? 'SIZE_LIMIT' : response.status === 422 ? 'REQUEST_INVALID' : 'REQUEST_FAILED')
  const result: unknown = await response.json()
  if (!isDraftReview(result) || result.raw_sha256 !== rawHash || result.source.source_claim !== source
    || JSON.stringify([...result.requested_assessments].sort()) !== JSON.stringify([...questions].sort())
    || Object.entries(context).some(([key, value]) => (result.source.context as unknown as Record<string, unknown>)[key] !== value)) throw new Error('INVALID_RESPONSE')
  return result
}
