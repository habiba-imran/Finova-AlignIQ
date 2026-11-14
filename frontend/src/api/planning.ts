import { isAutomaticParseResult } from './parse'
import type { AutomaticParseResult, ContextClaims } from './parse'
import { isFinalDraftReport } from './report'
import type { CommentMode, FinalDraftReport, ReportComment } from './report'
import type { AssessmentQuestion } from './review'

export const DIMENSIONS = ['SAGITTAL', 'TRANSVERSE', 'VERTICAL', 'OTHER', 'UNAVAILABLE'] as const
export type Dimension = typeof DIMENSIONS[number]
export interface PlanningDraft {
  version: '1.0.0'; report: FinalDraftReport; export_text: string
  sections: { dimension: Dimension; comment_ids: string[]; explanation: string }[]
}
export interface DemoInput {
  demo_id: 'FINOVA-SYNTHETIC-1'; label: string; convention: string[]
  context: ContextClaims; parsed: AutomaticParseResult
}
const object = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v)
export function isPlanningDraft(v: unknown): v is PlanningDraft {
  if (!object(v) || v.version !== '1.0.0' || !isFinalDraftReport(v.report) || !Array.isArray(v.sections) || v.sections.length !== 5
    || typeof v.export_text !== 'string' || !v.export_text.endsWith(v.report.export_text)
    || (v.report.engine_review.evidence_domain === 'TEST_ONLY' && !v.export_text.includes('FINOVA SYNTHETIC DEMONSTRATION — TEST_ONLY'))) return false
  const comments = new Map(v.report.comments.map(c => [c.comment_id, c]))
  const seen = new Set<string>()
  return v.sections.every((s, i) => object(s) && s.dimension === DIMENSIONS[i] && typeof s.explanation === 'string'
    && Array.isArray(s.comment_ids) && s.comment_ids.every(id => {
      if (typeof id !== 'string' || seen.has(id) || !comments.has(id)) return false
      seen.add(id)
      return (s.dimension === 'UNAVAILABLE') === (comments.get(id)!.section === 'UNAVAILABLE')
    })) && seen.size === comments.size
}

async function post(url: string, body: unknown, signal: AbortSignal): Promise<unknown> {
  const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body), signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer' })
  if (!response.ok) throw new Error(response.status === 404 ? 'DEMO_DISABLED' : response.status === 409 ? 'REPARSE_REQUIRED' : 'REQUEST_FAILED')
  return response.json()
}

export async function requestDemoInput(signal: AbortSignal): Promise<DemoInput> {
  const v = await post('/api/v1/development/planning-demo/input', {}, signal)
  if (!object(v) || v.demo_id !== 'FINOVA-SYNTHETIC-1' || typeof v.label !== 'string'
    || !Array.isArray(v.convention) || !v.convention.every(c => typeof c === 'string') || !object(v.context)
    || !isAutomaticParseResult(v.parsed) || v.parsed.source.source_claim !== 'Unknown'
    || v.context.source_version !== 'FINOVA-DEMO-1'
    || JSON.stringify(v.context) !== JSON.stringify((v.parsed.source as unknown as Record<string, unknown>).context)) throw new Error('INVALID_RESPONSE')
  return v as unknown as DemoInput
}

export async function requestPlanning(raw: string, context: ContextClaims, hash: string, mode: CommentMode,
  questions: AssessmentQuestion[], signal: AbortSignal, demo: boolean, receipt?: string): Promise<PlanningDraft> {
  const body = demo ? { comment_mode: mode } : { raw_text: raw, source_claim: 'Unknown', context,
    synthetic_data_confirmed: true, requested_assessments: questions, comment_mode: mode,
    ...(receipt ? { recovery_receipt: receipt } : {}) }
  const v = await post(demo ? '/api/v1/development/planning-demo/draft' : '/api/v1/planning/draft', body, signal)
  if (!isPlanningDraft(v) || v.report.engine_review.raw_sha256 !== hash || v.report.generation.requested_mode !== mode
    || v.report.engine_review.source.source_claim !== 'Unknown'
    || Object.entries(context).some(([k, value]) => (v.report.engine_review.source.context as unknown as Record<string, unknown>)[k] !== value)
    || JSON.stringify([...v.report.engine_review.requested_assessments].sort()) !== JSON.stringify([...(demo ? [] : questions)].sort())
    || (demo ? v.report.engine_review.evidence_domain !== 'TEST_ONLY' : v.report.engine_review.evidence_domain === 'TEST_ONLY')) throw new Error('INVALID_RESPONSE')
  return v
}

export function eligibleComment(c: ReportComment): boolean {
  return c.section !== 'UNAVAILABLE' && c.measurements.length > 0 && ['VERIFIED', 'TEST_ONLY'].includes(c.evidence_status)
    && c.evaluation_statuses.every(s => s === 'OBSERVED') && !c.missing_required_fields.length && !c.abstain_reasons.length
}

export function selectedExport(report: FinalDraftReport, selected: ReadonlySet<string>): string {
  const comments = report.comments.filter(c => selected.has(c.comment_id) && eligibleComment(c))
  if (!comments.length) return ''
  return ['FINOVA ALIGNIQ — SELECTED DESCRIPTIVE DRAFT COMMENTS', report.draft_status,
    'Prototype — not for clinical use', `Evidence domain: ${report.engine_review.evidence_domain}`,
    report.engine_review.evidence_domain === 'TEST_ONLY' ? 'FINOVA SYNTHETIC DEMONSTRATION — TEST_ONLY; no patient or vendor validation.' : 'Descriptive programmed movements only; no clinical approval.',
    `Report: ${report.report_id}`, `Input SHA-256: ${report.engine_review.raw_sha256}`,
    `Rule set: ${report.engine_review.rule_set_version}`, 'Selected subset; omitted comments are not negative findings.', '',
    ...comments.flatMap(c => [c.text, `Comment: ${c.comment_id}`, `Rules: ${c.rules.map(r => `${r.rule_id} v${r.version}`).join(', ')}`,
      `Findings: ${c.finding_ids.join(', ')}`, `Input references: ${c.input_refs.join(', ')}`,
      `Evidence references: ${c.evidence_refs.join(', ')}`, `Evidence: ${c.evidence_status}; wording: ${c.wording_source}`, '']),
    'WITHHELD ASSESSMENTS / MISSING INFORMATION (complete for context)',
    ...report.comments.filter(c => c.section === 'UNAVAILABLE').flatMap(c => [c.text, `Findings: ${c.finding_ids.join(', ')}`, `Required: ${c.missing_required_fields.join(', ')}`, `Withheld: ${c.abstain_reasons.join(', ')}`]),
    '', 'LIMITATIONS', ...report.limitations, report.draft_status, 'No clinician approval or sign-off is recorded.', ''].join('\n')
}
