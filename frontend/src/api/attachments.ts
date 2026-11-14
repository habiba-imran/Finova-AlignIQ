import { isAutomaticParseResult } from './parse'
import type { AutomaticParseResult, ContextClaims } from './parse'
import { isDraftReview } from './review'
import type { DraftReview } from './review'

export interface AttachmentDesign {
  design_id: string; category_id: string; label: string; shape: string | null
  dimensions: { x: string; y: string; z: string; unit: 'mm' } | null; orientation: string | null
}
export interface AttachmentEntry {
  entry_id: string; tooth_ref: string | null; original_tooth: string | null; verified_tooth: null; synthetic_tooth: string | null
  result_type: 'CANDIDATE' | 'ALTERNATIVE' | 'NOT_INDICATED' | 'UNKNOWN' | 'WITHHELD'
  decision_origin: 'SUPPLIED_SYNTHETIC' | 'WITHHOLDING_GUARD'; evidence_status: 'TEST_ONLY' | 'UNVERIFIED'
  design: AttachmentDesign | null; placement: { surface_id: string; frame_id: string; stage_ref: string | null } | null
  alternative_for: string | null; explanation: string; measurement_refs: string[]; observation_refs: string[]; evidence_refs: string[]
  finding_refs: string[]; missing_prerequisites: string[]; approval_status: 'NOT APPROVED'; review_status: 'DRAFT'
}
export interface AttachmentDraft {
  schema_version: '1.0.0'; report_id: string; title: 'Finova AlignIQ — Attachment Review'
  draft_status: 'DRAFT — Requires Orthodontist Review'; clinical_analysis_enabled: false; evidence_domain: 'TEST_ONLY' | 'UNVERIFIED'
  engine_review: DraftReview; entries: AttachmentEntry[]; wording_source: 'DETERMINISTIC_TEMPLATES'; provider: null; provider_attempts: 0
  limitations: string[]; export_format: 'text/plain;charset=utf-8'; export_text: string
}
export interface AttachmentDemoInput {
  demo_id: 'FINOVA-ATTACHMENTS-1'; label: string; convention: string[]; context: ContextClaims; parsed: AutomaticParseResult
}
const obj = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
const optional = (v: unknown) => v === null || str(v)
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(str)
const hash = (v: unknown): v is string => str(v) && /^[a-f0-9]{64}$/.test(v)
const dimension = (v: unknown) => str(v) && /^\d+(\.\d+)?$/.test(v) && Number(v) > 0 && Number.isFinite(Number(v))

export function isAttachmentDraft(v: unknown): v is AttachmentDraft {
  if (!obj(v) || v.schema_version !== '1.0.0' || !hash(v.report_id) || v.title !== 'Finova AlignIQ — Attachment Review'
    || v.draft_status !== 'DRAFT — Requires Orthodontist Review' || v.clinical_analysis_enabled !== false
    || !['TEST_ONLY', 'UNVERIFIED'].includes(String(v.evidence_domain)) || !isDraftReview(v.engine_review)
    || v.engine_review.evidence_domain !== v.evidence_domain || !v.engine_review.requested_assessments.includes('ATTACHMENTS')
    || v.provider !== null || v.provider_attempts !== 0 || v.wording_source !== 'DETERMINISTIC_TEMPLATES'
    || !strings(v.limitations) || !v.limitations.length || !str(v.export_text) || v.export_format !== 'text/plain;charset=utf-8'
    || ![v.draft_status, v.report_id, v.engine_review.raw_sha256, 'Prototype — not for clinical use', ...v.limitations].every(s => (v.export_text as string).includes(s))
    || (v.evidence_domain === 'TEST_ONLY' && !v.export_text.includes('FINOVA SYNTHETIC ATTACHMENT DEMONSTRATION — TEST_ONLY'))
    || !Array.isArray(v.entries) || !v.entries.length || v.entries.length > 512) return false
  const entries = v.entries
  const ids = new Set<string>()
  const findings = new Set(v.engine_review.findings.map(f => f.finding_id))
  const observations = v.engine_review.findings.flatMap(f => f.observed_measurements)
  if (!entries.every(e => {
    if (!obj(e) || !hash(e.entry_id) || ids.has(e.entry_id) || !optional(e.tooth_ref) || !optional(e.original_tooth)
      || e.verified_tooth !== null || !optional(e.synthetic_tooth) || !optional(e.alternative_for)
      || !['CANDIDATE', 'ALTERNATIVE', 'NOT_INDICATED', 'UNKNOWN', 'WITHHELD'].includes(String(e.result_type))
      || !['TEST_ONLY', 'UNVERIFIED'].includes(String(e.evidence_status)) || !['SUPPLIED_SYNTHETIC', 'WITHHOLDING_GUARD'].includes(String(e.decision_origin))
      || !str(e.explanation) || e.approval_status !== 'NOT APPROVED' || e.review_status !== 'DRAFT'
      || !['measurement_refs', 'observation_refs', 'evidence_refs', 'finding_refs', 'missing_prerequisites'].every(k => strings(e[k]))
      || !(e.finding_refs as string[]).length
      || !(e.finding_refs as string[]).every(id => findings.has(id)) || !(v.export_text as string).includes(e.explanation)
      || !(v.export_text as string).includes(e.entry_id)) return false
    ids.add(e.entry_id)
    const supplied = ['CANDIDATE', 'ALTERNATIVE', 'NOT_INDICATED'].includes(String(e.result_type))
    if (v.evidence_domain === 'UNVERIFIED' && (e.evidence_status !== 'UNVERIFIED' || supplied)) return false
    if (e.evidence_status === 'UNVERIFIED' && (e.synthetic_tooth !== null || (e.observation_refs as string[]).length)) return false
    if (e.evidence_status === 'TEST_ONLY' && (!e.synthetic_tooth || !(e.observation_refs as string[]).length || !(e.evidence_refs as string[]).length)) return false
    if (!(e.observation_refs as string[]).every(id => observations.some(o => o.measurement_id === id && (o as unknown as Record<string, unknown>).tooth_ref === e.tooth_ref && o.verification === 'TEST_ONLY'
      && o.components.some(c => c.name === 'tooth_identifier' && c.status === 'TEST_ONLY' && c.canonical_value === e.synthetic_tooth)))) return false
    if (supplied && (e.decision_origin !== 'SUPPLIED_SYNTHETIC' || e.evidence_status !== 'TEST_ONLY' || !e.synthetic_tooth || !(e.observation_refs as string[]).length || !(e.evidence_refs as string[]).length)) return false
    if (!supplied && (e.decision_origin !== 'WITHHOLDING_GUARD' || e.design !== null || e.placement !== null || e.alternative_for !== null || !(e.missing_prerequisites as string[]).length)) return false
    if (e.result_type === 'NOT_INDICATED' && (e.design !== null || e.placement !== null || e.alternative_for !== null)) return false
    if (['CANDIDATE', 'ALTERNATIVE'].includes(String(e.result_type)) && !obj(e.design)) return false
    if ((e.result_type === 'ALTERNATIVE') !== (e.alternative_for !== null)) return false
    if (e.design !== null) {
      const d = e.design
      if (!obj(d) || !str(d.design_id) || !str(d.category_id) || !str(d.label) || !optional(d.shape) || !optional(d.orientation)) return false
      if (d.dimensions !== null && (!obj(d.dimensions) || d.dimensions.unit !== 'mm' || !['x', 'y', 'z'].every(k => dimension((d.dimensions as Record<string, unknown>)[k])))) return false
    }
    return e.placement === null || (obj(e.placement) && str(e.placement.surface_id) && str(e.placement.frame_id) && optional(e.placement.stage_ref))
  })) return false
  return entries.every(e => !e.alternative_for || entries.some(c => c.entry_id === e.alternative_for && c.result_type === 'CANDIDATE' && c.tooth_ref === e.tooth_ref))
}

async function post(path: string, body: unknown, signal: AbortSignal): Promise<unknown> {
  const response = await fetch(path, { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer' })
  if (!response.ok) throw new Error(response.status === 404 ? 'DEMO_DISABLED' : response.status === 409 ? 'REPARSE_REQUIRED' : 'REQUEST_FAILED')
  return response.json()
}
export async function requestAttachmentDemoInput(signal: AbortSignal): Promise<AttachmentDemoInput> {
  const value = await post('/api/v1/development/attachment-demo/input', {}, signal)
  if (!obj(value) || value.demo_id !== 'FINOVA-ATTACHMENTS-1' || !str(value.label) || !strings(value.convention)
    || !obj(value.context) || !isAutomaticParseResult(value.parsed) || value.parsed.source.source_claim !== 'Unknown'
    || value.context.source_version !== 'FINOVA-DEMO-1'
    || JSON.stringify(value.context) !== JSON.stringify((value.parsed.source as unknown as Record<string, unknown>).context)) throw new Error('INVALID_RESPONSE')
  return value as unknown as AttachmentDemoInput
}
export async function requestAttachmentDraft(raw: string, context: ContextClaims, hash: string, demo: boolean, signal: AbortSignal, receipt?: string): Promise<AttachmentDraft> {
  const value = await post(demo ? '/api/v1/development/attachment-demo/draft' : '/api/v1/attachments/draft',
    demo ? {} : { raw_text: raw, source_claim: 'Unknown', context, synthetic_data_confirmed: true, ...(receipt ? { recovery_receipt: receipt } : {}) }, signal)
  if (!isAttachmentDraft(value) || value.engine_review.raw_sha256 !== hash || value.engine_review.source.source_claim !== 'Unknown'
    || Object.entries(context).some(([k, val]) => (value.engine_review.source.context as unknown as Record<string, unknown>)[k] !== val)
    || value.evidence_domain !== (demo ? 'TEST_ONLY' : 'UNVERIFIED')) throw new Error('INVALID_RESPONSE')
  return value
}
