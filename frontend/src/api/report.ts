import type { ContextClaims, SourceClaim } from './parse'
import { isDraftReview } from './review'
import type { AssessmentQuestion, DraftReview, ReviewFinding } from './review'

export type CommentMode = 'AUTO' | 'GROQ' | 'TEMPLATES'
export interface ReportComment {
  comment_id: string; finding_ids: string[]; rules: { rule_id: string; version: '2.0.0' }[]
  section: 'TOOTH' | 'SUMMARY' | 'UNAVAILABLE'; tooth_id: string | null
  evidence_status: 'VERIFIED' | 'TEST_ONLY' | 'UNVERIFIED'; text: string
  wording_source: 'STANDARD_TEMPLATE' | 'GROQ_VALIDATED'; wording_validation: 'NOT_REQUESTED' | 'ACCEPTED' | 'FALLBACK'
  fallback_reason: string | null; measurements: ReviewFinding['observed_measurements']
  input_refs: string[]; evidence_refs: string[]; missing_required_fields: string[]; abstain_reasons: string[]; evaluation_statuses: string[]
}
export interface FinalDraftReport {
  schema_version: '1.0.0'; report_version: '0.3.0'; report_id: string
  title: 'Finova AlignIQ — Descriptive Planning Report'; draft_status: 'DRAFT — Requires Orthodontist Review'
  clinical_analysis_enabled: false; engine_review: DraftReview
  generation: {
    requested_mode: CommentMode; used_mode: 'STANDARD_TEMPLATES' | 'GROQ_AI' | 'MIXED'; reason: string
    provider: 'GROQ' | null; model: 'openai/gpt-oss-120b' | null; attempts: number; eligible_wording_findings: number
    accepted_comments: number; real_patient_transmission_enabled: false; output_validation: 'CLOSED_WORDING_AND_LOCAL_FACTS_V1'
  }
  comments: ReportComment[]; limitations: string[]; export_format: 'text/plain;charset=utf-8'; export_text: string
}

const obj = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(str)
const hash = (v: unknown) => str(v) && /^[a-f0-9]{64}$/.test(v)

export function isFinalDraftReport(v: unknown): v is FinalDraftReport {
  if (!obj(v) || v.schema_version !== '1.0.0' || v.report_version !== '0.3.0' || !hash(v.report_id)
    || v.title !== 'Finova AlignIQ — Descriptive Planning Report' || v.draft_status !== 'DRAFT — Requires Orthodontist Review'
    || v.clinical_analysis_enabled !== false || !isDraftReview(v.engine_review) || !strings(v.limitations)
    || !v.limitations.length || v.export_format !== 'text/plain;charset=utf-8' || !str(v.export_text)
    || !v.export_text.includes(v.draft_status) || !v.export_text.includes('Prototype — not for clinical use')
    || !v.export_text.includes(String(v.report_id)) || !v.export_text.includes(v.engine_review.raw_sha256)
    || !v.limitations.every(item => (v.export_text as string).includes(item))) return false
  const g = v.generation
  if (!obj(g) || !['AUTO', 'GROQ', 'TEMPLATES'].includes(String(g.requested_mode))
    || !['STANDARD_TEMPLATES', 'GROQ_AI', 'MIXED'].includes(String(g.used_mode)) || !str(g.reason)
    || !(g.provider === null || g.provider === 'GROQ') || !(g.model === null || g.model === 'openai/gpt-oss-120b')
    || g.real_patient_transmission_enabled !== false || g.output_validation !== 'CLOSED_WORDING_AND_LOCAL_FACTS_V1'
    || !['attempts', 'eligible_wording_findings', 'accepted_comments'].every(k => Number.isInteger(g[k]) && Number(g[k]) >= 0)
    || Number(g.attempts) > 2) return false
  const findings = new Map(v.engine_review.findings.map(f => [f.finding_id, f]))
  return Array.isArray(v.comments) && v.comments.every(c => {
    if (!obj(c) || !hash(c.comment_id) || !strings(c.finding_ids) || !c.finding_ids.length || !c.finding_ids.every(id => findings.has(id))
      || !['TOOTH', 'SUMMARY', 'UNAVAILABLE'].includes(String(c.section)) || !(c.tooth_id === null || str(c.tooth_id))
      || !['VERIFIED', 'TEST_ONLY', 'UNVERIFIED'].includes(String(c.evidence_status)) || !str(c.text)
      || !['STANDARD_TEMPLATE', 'GROQ_VALIDATED'].includes(String(c.wording_source))
      || !['NOT_REQUESTED', 'ACCEPTED', 'FALLBACK'].includes(String(c.wording_validation))
      || !(c.fallback_reason === null || str(c.fallback_reason))
      || !['input_refs', 'evidence_refs', 'missing_required_fields', 'abstain_reasons', 'evaluation_statuses'].every(k => strings(c[k]))
      || !Array.isArray(c.rules) || !c.rules.every(r => obj(r) && str(r.rule_id) && r.version === '2.0.0')
      || !Array.isArray(c.measurements)) return false
    const fs = c.finding_ids.map(id => findings.get(id)!)
    const allowedRules = new Set(fs.flatMap(f => f.triggering_rules.map(r => r.rule_id)))
    const sourceObservations = fs.flatMap(f => f.observed_measurements)
    if (!c.rules.every(r => allowedRules.has((r as { rule_id: string }).rule_id))) return false
    if (c.section === 'UNAVAILABLE' && c.measurements.length) return false
    if (c.section !== 'UNAVAILABLE' && (!c.measurements.length || fs.some(f => f.finding_type !== 'DESCRIPTIVE' || f.status !== 'OBSERVED'))) return false
    if (!c.measurements.every(o => sourceObservations.some(source => JSON.stringify(source) === JSON.stringify(o)))) return false
    return (v.export_text as string).includes(c.text) && c.finding_ids.every(id => (v.export_text as string).includes(id))
  })
}

export async function requestReport(rawText: string, source: SourceClaim, context: ContextClaims, rawHash: string,
  questions: AssessmentQuestion[], mode: CommentMode, signal: AbortSignal, recoveryReceipt?: string): Promise<FinalDraftReport> {
  const response = await fetch('/api/v1/reports/draft', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ raw_text: rawText, source_claim: source, context, synthetic_data_confirmed: true, requested_assessments: questions, comment_mode: mode,
      ...(recoveryReceipt ? { recovery_receipt: recoveryReceipt } : {}) }),
    signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer',
  })
  if (!response.ok) throw new Error(response.status === 409 ? 'REPARSE_REQUIRED' : response.status === 413 ? 'SIZE_LIMIT' : response.status === 422 ? 'REQUEST_INVALID' : 'REQUEST_FAILED')
  const result: unknown = await response.json()
  if (!isFinalDraftReport(result) || result.engine_review.raw_sha256 !== rawHash || result.engine_review.source.source_claim !== source
    || result.generation.requested_mode !== mode
    || JSON.stringify([...result.engine_review.requested_assessments].sort()) !== JSON.stringify([...questions].sort())
    || Object.entries(context).some(([key, value]) => (result.engine_review.source.context as unknown as Record<string, unknown>)[key] !== value)) throw new Error('INVALID_RESPONSE')
  return result
}
