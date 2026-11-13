export const MAX_TEXT_CHARACTERS = 100_000

export type SourceClaim = 'Unknown' | 'ClinCheck' | 'SureSmile'
export interface SyntheticFixture { recipe: string; seed: number }

export interface ContextClaims {
  source_version: string | null
  notation: 'UNKNOWN' | 'FDI' | 'UNIVERSAL' | 'PALMER'
  dentition: 'UNKNOWN' | 'PERMANENT' | 'PRIMARY' | 'MIXED'
  arch: 'UNKNOWN' | 'UPPER' | 'LOWER' | 'BOTH'
  plan_mode: 'UNKNOWN' | 'ALIGN_FINAL' | 'DOCTOR_FINAL' | 'COMPARISON'
  reference_basis: 'UNKNOWN' | 'CROWN_CENTER' | 'VIRTUAL_ROOT_APEX' | 'CUSP_TIP'
  scope: 'UNKNOWN' | 'TOTAL' | 'CUMULATIVE' | 'INCREMENTAL'
  stage_index: number | null
  coordinate_frame: string | null
  decimal_separator: 'DOT' | 'COMMA'
}

export const EMPTY_CONTEXT: ContextClaims = {
  source_version: null, notation: 'UNKNOWN', dentition: 'UNKNOWN', arch: 'UNKNOWN',
  plan_mode: 'UNKNOWN', reference_basis: 'UNKNOWN', scope: 'UNKNOWN', stage_index: null,
  coordinate_frame: null, decimal_separator: 'DOT',
}

interface Span { line: number; column_start: number }
interface Adapter { id: string; version: string; verified: false }

export interface Measurement {
  id: string
  tooth_ref: string
  raw_label: string
  recognized_label: string | null
  raw_value: string | null
  signed_decimal: string | null
  magnitude_decimal: string | null
  unit: string | null
  raw_direction: string | null
  numeric_status: string
  field_status: string
  semantics_verified: false
  span: Span | null
  clarification_fields: string[]
}

export interface ParseResult {
  schema_version: '1.0.0'
  status: 'PARSED_UNVERIFIED' | 'PARTIAL' | 'UNSUPPORTED' | 'INVALID'
  raw_text: string
  raw_sha256: string
  source: {
    source_claim: SourceClaim
    verification_status: 'UNVERIFIED'
    detected_claims: SourceClaim[]
    adapter: Adapter
    candidate_adapter: Adapter | null
  }
  layout: { orientation: string; delimiter: string | null }
  teeth: { id: string; raw_identifier: string; identifier_status: string; normalized_identifier: null }[]
  measurements: Measurement[]
  coverage: { explicit_zero: number; missing: number }
  issues: { code: string; severity: 'INFO' | 'WARNING' | 'ERROR'; message: string; field: string | null; span: Span | null }[]
  clarification_fields: string[]
}

export interface AutomaticParseResult extends ParseResult {
  pipeline: {
    version: '1.0.0'
    detection: {
      detected_source: SourceClaim
      verified_source: null
      status: 'UNKNOWN' | 'DETECTED_UNVERIFIED' | 'CONFLICT'
      notation_candidates: string[]
      layout_recognized: boolean
    }
    assistance: {
      available: boolean
      status: 'NOT_REQUESTED' | 'BLOCKED' | 'FAILED' | 'REJECTED' | 'ACCEPTED'
      reason: string
      attempts: number
      certificate: 'MARKDOWN_PIPE_V1' | 'SPAN_ASSOCIATIONS_V1' | null
      origin: 'DETERMINISTIC' | 'GROQ_PROPOSAL_CERTIFIED'
      real_patient_transmission_enabled: false
    }
    clarifications: { code: string; field: string; measurement_ids: string[]; message: string }[]
    quality?: { classification: string; recoverable_associations: number; unresolved_lines: number[]; cloud_candidate: boolean } | null
    recovery_receipt?: string | null
  }
}

const object = (value: unknown): value is Record<string, unknown> => typeof value === 'object' && value !== null
const string = (value: unknown): value is string => typeof value === 'string'
const nullableString = (value: unknown) => value === null || string(value)
const strings = (value: unknown) => Array.isArray(value) && value.every(string)
const span = (value: unknown) => value === null || (object(value) && Number.isInteger(value.line) && Number.isInteger(value.column_start))
const adapter = (value: unknown) => object(value) && string(value.id) && string(value.version) && value.verified === false

// Validate the fields used for rendering. Full authoritative contracts are exported JSON Schemas.
export function isParseResult(value: unknown): value is ParseResult {
  if (!object(value) || value.schema_version !== '1.0.0' || !string(value.raw_text)
    || !string(value.raw_sha256) || !/^[a-f0-9]{64}$/.test(value.raw_sha256)
    || !['PARSED_UNVERIFIED', 'PARTIAL', 'UNSUPPORTED', 'INVALID'].includes(String(value.status))) return false
  const source = value.source
  if (!object(source) || source.verification_status !== 'UNVERIFIED' || !adapter(source.adapter)
    || !['Unknown', 'ClinCheck', 'SureSmile'].includes(String(source.source_claim)) || !strings(source.detected_claims)
    || !(source.candidate_adapter === null || adapter(source.candidate_adapter))) return false
  if (!object(value.layout) || !string(value.layout.orientation) || !nullableString(value.layout.delimiter)
    || !object(value.coverage) || !Number.isInteger(value.coverage.explicit_zero) || !Number.isInteger(value.coverage.missing)
    || !strings(value.clarification_fields)) return false
  if (!Array.isArray(value.teeth) || !value.teeth.every(t => object(t) && string(t.id) && string(t.raw_identifier)
    && string(t.identifier_status) && t.normalized_identifier === null)) return false
  if (!Array.isArray(value.measurements) || !value.measurements.every(m => object(m)
    && ['id', 'tooth_ref', 'raw_label', 'numeric_status', 'field_status'].every(key => string(m[key]))
    && ['recognized_label', 'raw_value', 'signed_decimal', 'magnitude_decimal', 'unit', 'raw_direction'].every(key => nullableString(m[key]))
    && m.semantics_verified === false && span(m.span) && strings(m.clarification_fields))) return false
  return Array.isArray(value.issues) && value.issues.every(i => object(i) && string(i.code) && string(i.message)
    && ['INFO', 'WARNING', 'ERROR'].includes(String(i.severity)) && nullableString(i.field) && span(i.span))
}

export function isAutomaticParseResult(value: unknown): value is AutomaticParseResult {
  if (!isParseResult(value) || !object(value) || !object(value.pipeline)) return false
  const p = value.pipeline
  if (p.version !== '1.0.0' || !object(p.detection) || !object(p.assistance)) return false
  const d = p.detection, a = p.assistance
  return ['Unknown', 'ClinCheck', 'SureSmile'].includes(String(d.detected_source)) && d.verified_source === null
    && ['UNKNOWN', 'DETECTED_UNVERIFIED', 'CONFLICT'].includes(String(d.status))
    && strings(d.notation_candidates) && typeof d.layout_recognized === 'boolean'
    && typeof a.available === 'boolean' && ['NOT_REQUESTED', 'BLOCKED', 'FAILED', 'REJECTED', 'ACCEPTED'].includes(String(a.status))
    && string(a.reason) && Number.isInteger(a.attempts) && Number(a.attempts) >= 0
    && (a.certificate === null || a.certificate === 'MARKDOWN_PIPE_V1' || a.certificate === 'SPAN_ASSOCIATIONS_V1')
    && ['DETERMINISTIC', 'GROQ_PROPOSAL_CERTIFIED'].includes(String(a.origin)) && a.real_patient_transmission_enabled === false
    && (p.recovery_receipt === undefined || nullableString(p.recovery_receipt))
    && (p.quality === undefined || p.quality === null || (object(p.quality) && string(p.quality.classification)
      && Number.isInteger(p.quality.recoverable_associations) && Array.isArray(p.quality.unresolved_lines) && p.quality.unresolved_lines.every(Number.isInteger) && typeof p.quality.cloud_candidate === 'boolean'))
    && Array.isArray(p.clarifications) && p.clarifications.every(c => object(c) && string(c.code) && string(c.field) && strings(c.measurement_ids) && string(c.message))
}

export async function requestParse(rawText: string, sourceClaim: SourceClaim, context: ContextClaims, signal: AbortSignal, fixture?: SyntheticFixture): Promise<AutomaticParseResult> {
  const response = await fetch('/api/v1/tmt/parse', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ raw_text: rawText, source_claim: sourceClaim, context, synthetic_data_confirmed: true,
      ...(fixture ? { synthetic_fixture: fixture } : {}) }),
    signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer',
  })
  if (!response.ok) {
    if (response.status === 413) throw new Error('SIZE_LIMIT')
    if (response.status === 422) throw new Error('REQUEST_INVALID')
    throw new Error('REQUEST_FAILED')
  }
  const result: unknown = await response.json()
  if (!isAutomaticParseResult(result) || result.raw_text !== rawText || result.source.source_claim !== sourceClaim) throw new Error('INVALID_RESPONSE')
  return result
}
