import { isAutomaticParseResult, isParseResult } from './parse'
import type { AutomaticParseResult, ContextClaims, ParseResult } from './parse'
import { isDraftReview } from './review'
import type { DraftReview } from './review'

export const SEQUENCE_SECTIONS = ['UPPER_ARCH', 'LOWER_ARCH', 'SEGMENTS', 'RIGHT_ANCHORAGE', 'LEFT_ANCHORAGE', 'UNAVAILABLE'] as const
export type SequenceSection = typeof SEQUENCE_SECTIONS[number]
export interface StageRecord { stage_id: string; index: number; arch: string; kind: string; evidence_ref: string }
export interface SequenceEntry {
  entry_id: string; section: SequenceSection; result_type: 'STRUCTURAL_OBSERVATION' | 'SUPPLIED_SYNTHETIC' | 'UNKNOWN' | 'WITHHELD' | 'DISABLED'
  origin: 'SUPPLIED_SCENARIO' | 'ENGINE_GUARD'; text: string; original_tooth_refs: string[]; original_tooth_tokens: string[]
  verified_tooth_refs: string[]; verified_arch: null; verified_segment: null; synthetic_arch_id: string | null; synthetic_segment_id: string | null
  side: 'RIGHT' | 'LEFT' | 'UNKNOWN'; evidence_status: 'UNVERIFIED' | 'TEST_ONLY'; movement_scope: string
  stage_window: { start_id: string; end_id: string } | null; stage_kinds: string[]; evidence_refs: string[]; measurement_refs: string[]
  finding_refs: string[]; missing_prerequisites: string[]; policy_id: null; approval_status: 'NOT APPROVED'; clinical_predicate_evaluated: false; review_status: 'DRAFT'
}
export interface SequencingDraft {
  schema_version: '1.0.0'; report_id: string; title: 'Finova AlignIQ — Sequencing Review'; draft_status: 'DRAFT — Requires Orthodontist Review'
  synthetic_notice: 'SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE' | null; evidence_domain: 'TEST_ONLY' | 'UNVERIFIED'; clinical_analysis_enabled: false
  parsed: ParseResult; engine_review: DraftReview
  stage_inspection: { status: 'MISSING' | 'SUPPLIED_SYNTHETIC_METADATA' | 'INVALID'; records: StageRecord[]; issues: string[]; evidence_ref: string | null; movement_binding: 'NO_STAGE_MOVEMENT_BINDING'; explanation: string }
  fictional_arches: { arch_id: string; label: string; role: 'UPPER' | 'LOWER' }[]
  fictional_segments: { segment_id: string; label: string; arch_id: string; side: 'RIGHT' | 'LEFT'; tooth_refs: string[] }[]
  entries: SequenceEntry[]; wording_source: 'DETERMINISTIC_TEMPLATES'; provider: null; provider_attempts: 0
  limitations: string[]; export_format: 'text/plain;charset=utf-8'; export_text: string
}
export interface SequencingDemoInput {
  demo_id: 'FINOVA-NANO-1'; label: string; convention: string[]; context: ContextClaims; parsed: AutomaticParseResult
}
const obj = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v)
const str = (v: unknown): v is string => typeof v === 'string'
const nullable = (v: unknown) => v === null || str(v)
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(str)
const hash = (v: unknown): v is string => str(v) && /^[a-f0-9]{64}$/.test(v)
const KINDS = ['BASELINE', 'ACTIVE', 'ACCOMMODATION', 'CORRECTION', 'OVERCORRECTION', 'PASSIVE']

export function isSequencingDraft(v: unknown): v is SequencingDraft {
  if (!obj(v) || v.schema_version !== '1.0.0' || !hash(v.report_id) || v.title !== 'Finova AlignIQ — Sequencing Review'
    || v.draft_status !== 'DRAFT — Requires Orthodontist Review' || v.clinical_analysis_enabled !== false || v.provider !== null || v.provider_attempts !== 0
    || v.wording_source !== 'DETERMINISTIC_TEMPLATES' || !['TEST_ONLY', 'UNVERIFIED'].includes(String(v.evidence_domain))
    || !isDraftReview(v.engine_review) || !isParseResult(v.parsed) || v.engine_review.evidence_domain !== v.evidence_domain || v.parsed.raw_sha256 !== v.engine_review.raw_sha256
    || (v.evidence_domain === 'TEST_ONLY' ? v.synthetic_notice !== 'SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE' : v.synthetic_notice !== null)
    || !strings(v.limitations) || !v.limitations.length || !str(v.export_text) || v.export_format !== 'text/plain;charset=utf-8'
    || ![v.report_id, v.draft_status, v.engine_review.raw_sha256, ...v.limitations, ...(v.synthetic_notice ? [String(v.synthetic_notice)] : [])].every(s => (v.export_text as string).includes(s))) return false
  const stage = v.stage_inspection
  if (!obj(stage) || !['MISSING', 'SUPPLIED_SYNTHETIC_METADATA', 'INVALID'].includes(String(stage.status)) || stage.movement_binding !== 'NO_STAGE_MOVEMENT_BINDING'
    || !str(stage.explanation) || !nullable(stage.evidence_ref) || !strings(stage.issues) || !Array.isArray(stage.records)
    || !stage.records.every(s => obj(s) && str(s.stage_id) && str(s.arch) && str(s.evidence_ref) && Number.isInteger(s.index) && Number(s.index) >= 0 && KINDS.includes(String(s.kind)))) return false
  const records = stage.records as unknown as StageRecord[]
  if (stage.status === 'MISSING' && records.length) return false
  if (stage.status === 'SUPPLIED_SYNTHETIC_METADATA') {
    if (!records.length || !stage.evidence_ref || stage.issues.length || new Set(records.map(s => s.stage_id)).size !== records.length) return false
    for (const arch of new Set(records.map(s => s.arch))) {
      const group = records.filter(s => s.arch === arch)
      if (new Set(group.map(s => s.index)).size !== group.length || group.some((s, i) => i > 0 && s.index < group[i - 1].index || s.index === 0 && s.kind !== 'BASELINE')) return false
    }
  }
  if (!Array.isArray(v.fictional_arches) || !v.fictional_arches.every(a => obj(a) && str(a.arch_id) && str(a.label) && ['UPPER', 'LOWER'].includes(String(a.role)))
    || !Array.isArray(v.fictional_segments) || !v.fictional_segments.every(s => obj(s) && str(s.segment_id) && str(s.label) && str(s.arch_id) && ['RIGHT', 'LEFT'].includes(String(s.side)) && strings(s.tooth_refs))) return false
  const arches = v.fictional_arches as SequencingDraft['fictional_arches'], segments = v.fictional_segments as SequencingDraft['fictional_segments']
  if (v.evidence_domain === 'UNVERIFIED' && (records.length || arches.length || segments.length)) return false
  const findings = new Set(v.engine_review.findings.map(f => f.finding_id)), measurements = new Set(v.parsed.measurements.map(m => m.id))
  const sourceScopes = new Set(v.engine_review.findings.flatMap(f => f.observed_measurements.flatMap(o => o.components.filter(c => c.name === 'scope').map(c => c.canonical_value))))
  const sourceContext = (v.parsed.source as unknown as Record<string, unknown>).context
  if (!obj(sourceContext)) return false
  const expectedScope = v.evidence_domain === 'TEST_ONLY' && sourceScopes.size === 1 && sourceScopes.has('TOTAL') ? 'TOTAL' : sourceContext.scope
  const teeth = new Map(v.parsed.teeth.map(t => [t.id, t.raw_identifier])), ids = new Set<string>(), sections = new Set<string>()
  if (!Array.isArray(v.entries) || v.entries.length < 6 || v.entries.length > 32) return false
  return v.entries.every(e => {
    if (!obj(e) || !hash(e.entry_id) || ids.has(e.entry_id) || !SEQUENCE_SECTIONS.includes(e.section as SequenceSection)
      || !['STRUCTURAL_OBSERVATION', 'SUPPLIED_SYNTHETIC', 'UNKNOWN', 'WITHHELD', 'DISABLED'].includes(String(e.result_type))
      || !['SUPPLIED_SCENARIO', 'ENGINE_GUARD'].includes(String(e.origin)) || !str(e.text) || !['UNVERIFIED', 'TEST_ONLY'].includes(String(e.evidence_status))
      || !['RIGHT', 'LEFT', 'UNKNOWN'].includes(String(e.side)) || !['TOTAL', 'CUMULATIVE', 'INCREMENTAL', 'UNKNOWN'].includes(String(e.movement_scope))
      || !['original_tooth_refs', 'original_tooth_tokens', 'verified_tooth_refs', 'stage_kinds', 'evidence_refs', 'measurement_refs', 'finding_refs', 'missing_prerequisites'].every(k => strings(e[k]))
      || (e.verified_tooth_refs as string[]).length || e.verified_arch !== null || e.verified_segment !== null || !nullable(e.synthetic_arch_id) || !nullable(e.synthetic_segment_id)
      || e.policy_id !== null || e.approval_status !== 'NOT APPROVED' || e.clinical_predicate_evaluated !== false || e.review_status !== 'DRAFT'
      || !(e.finding_refs as string[]).length || !(e.missing_prerequisites as string[]).length || !(e.finding_refs as string[]).every(id => findings.has(id))
      || !(e.measurement_refs as string[]).every(id => measurements.has(id)) || !(v.export_text as string).includes(e.entry_id) || !(v.export_text as string).includes(e.text)) return false
    ids.add(e.entry_id); sections.add(String(e.section))
    const originalRefs = e.original_tooth_refs as string[], originalTokens = e.original_tooth_tokens as string[]
    if (originalRefs.length !== originalTokens.length || originalRefs.some((id, i) => teeth.get(id) !== originalTokens[i])) return false
    if (e.synthetic_arch_id && !arches.some(a => a.arch_id === e.synthetic_arch_id) || e.synthetic_segment_id && !segments.some(s => s.segment_id === e.synthetic_segment_id)) return false
    if (e.movement_scope !== (e.evidence_status === 'UNVERIFIED' && originalRefs.length ? sourceContext.scope : expectedScope)) return false
    if (e.synthetic_arch_id) {
      const arch = arches.find(a => a.arch_id === e.synthetic_arch_id)!
      if ((e.section === 'UPPER_ARCH' && arch.role !== 'UPPER') || (e.section === 'LOWER_ARCH' && arch.role !== 'LOWER')) return false
      const allowed = new Set(segments.filter(s => s.arch_id === e.synthetic_arch_id && (e.side === 'UNKNOWN' || s.side === e.side)).flatMap(s => s.tooth_refs))
      if (originalRefs.some(id => !allowed.has(id))) return false
    }
    if (e.synthetic_segment_id) {
      const segment = segments.find(s => s.segment_id === e.synthetic_segment_id)!
      if (segment.arch_id !== e.synthetic_arch_id || segment.side !== e.side || originalRefs.some(id => !segment.tooth_refs.includes(id))) return false
    }
    if (e.section === 'RIGHT_ANCHORAGE' && e.side !== 'RIGHT' || e.section === 'LEFT_ANCHORAGE' && e.side !== 'LEFT') return false
    if (e.result_type === 'SUPPLIED_SYNTHETIC' ? e.origin !== 'SUPPLIED_SCENARIO' || e.evidence_status !== 'TEST_ONLY' || !(e.evidence_refs as string[]).length : e.origin !== 'ENGINE_GUARD') return false
    if (e.result_type === 'STRUCTURAL_OBSERVATION' && (stage.status !== 'SUPPLIED_SYNTHETIC_METADATA' || e.evidence_status !== 'TEST_ONLY')) return false
    if (v.evidence_domain === 'UNVERIFIED' && (e.evidence_status !== 'UNVERIFIED' || ['SUPPLIED_SYNTHETIC', 'STRUCTURAL_OBSERVATION'].includes(String(e.result_type)))) return false
    if (e.evidence_status === 'UNVERIFIED' && (e.synthetic_arch_id || e.synthetic_segment_id || e.stage_window)) return false
    if (['UNKNOWN', 'WITHHELD', 'DISABLED'].includes(String(e.result_type)) && (e.stage_window || (e.stage_kinds as string[]).length)) return false
    if (e.stage_window !== null) {
      if (!obj(e.stage_window) || !str(e.stage_window.start_id) || !str(e.stage_window.end_id) || stage.status !== 'SUPPLIED_SYNTHETIC_METADATA') return false
      const start = records.find(s => s.stage_id === (e.stage_window as Record<string, unknown>).start_id), end = records.find(s => s.stage_id === (e.stage_window as Record<string, unknown>).end_id)
      if (!start || !end || start.arch !== end.arch || start.arch !== e.synthetic_arch_id || start.index > end.index
        || JSON.stringify(e.stage_kinds) !== JSON.stringify([...new Set([start.kind, end.kind])])) return false
    }
    return true
  }) && sections.size === SEQUENCE_SECTIONS.length
}

async function post(path: string, body: unknown, signal: AbortSignal): Promise<unknown> {
  const response = await fetch(path, { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    signal, cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer' })
  if (!response.ok) throw new Error(response.status === 404 ? 'DEMO_DISABLED' : response.status === 409 ? 'REPARSE_REQUIRED' : 'REQUEST_FAILED')
  return response.json()
}
export async function requestSequencingDemoInput(signal: AbortSignal): Promise<SequencingDemoInput> {
  const v = await post('/api/v1/development/sequencer-demo/input', {}, signal)
  if (!obj(v) || v.demo_id !== 'FINOVA-NANO-1' || !str(v.label) || !strings(v.convention) || !obj(v.context) || !isAutomaticParseResult(v.parsed)
    || v.parsed.source.source_claim !== 'Unknown' || v.context.source_version !== 'FINOVA-DEMO-1'
    || JSON.stringify(v.context) !== JSON.stringify((v.parsed.source as unknown as Record<string, unknown>).context)) throw new Error('INVALID_RESPONSE')
  return v as unknown as SequencingDemoInput
}
export async function requestSequencingDraft(raw: string, context: ContextClaims, hash: string, demo: boolean, signal: AbortSignal, receipt?: string): Promise<SequencingDraft> {
  const v = await post(demo ? '/api/v1/development/sequencer-demo/draft' : '/api/v1/sequencing/draft', demo ? {} : {
    raw_text: raw, context, source_claim: 'Unknown', synthetic_data_confirmed: true, ...(receipt ? { recovery_receipt: receipt } : {}),
  }, signal)
  if (!isSequencingDraft(v) || v.engine_review.raw_sha256 !== hash || v.parsed.raw_text !== raw || v.evidence_domain !== (demo ? 'TEST_ONLY' : 'UNVERIFIED')
    || v.engine_review.source.source_claim !== 'Unknown' || Object.entries(context).some(([k, val]) => (v.engine_review.source.context as unknown as Record<string, unknown>)[k] !== val)) throw new Error('INVALID_RESPONSE')
  return v
}
