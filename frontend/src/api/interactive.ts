import { isParseResult } from './parse'
import type { ContextClaims, Measurement, ParseResult } from './parse'
import { isDraftReview } from './review'
import type { DraftReview } from './review'

export type DemoModule = 'macro' | 'micro' | 'nano'
export interface InteractiveReport {
  schema_version: '1.0.0'; module: DemoModule; report_id: string
  draft_status: 'Synthetic demonstration — not for clinical use'; clinical_analysis_enabled: false
  parsed: ParseResult; engine_review: DraftReview
  generation: { requested_mode: 'AUTO'; used_mode: 'GROQ_AI' | 'STANDARD_TEMPLATES'; reason: string; attempts: number; accepted_comments: number; real_patient_transmission_enabled: false
    provider: 'GROQ' | null; model: 'openai/gpt-oss-120b' | null; eligible_wording_findings: number; output_validation: 'CLOSED_WORDING_AND_LOCAL_FACTS_V1' | 'GROUNDED_PLANNING_WORDING_V1' }
  wording_notice: string; summary: string; export_text: string; limitations: string[]
  observations: { tooth_ref: string; original_tooth: string; text: string; evidence_status: 'PARSED_SOURCE_ONLY'; measurements: Measurement[] }[]
  illustrations: { tooth_ref: string; original_tooth: string; label: string; text: string; origin: 'SIMULATED_DEMO'; clinical_status: 'NOT_EVALUATED' }[]
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

export async function requestInteractiveReview(module: DemoModule, rawText: string, context: ContextClaims, hash: string, receipt: string | null | undefined, signal: AbortSignal): Promise<InteractiveReport> {
  const response = await fetch('/api/v1/interactive/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, signal,
    body: JSON.stringify({ module, raw_text: rawText, raw_sha256: hash, source_claim: 'Unknown', context, synthetic_data_confirmed: true, ...(receipt ? { recovery_receipt: receipt } : {}) }) })
  if (!response.ok) throw new Error(response.status === 409 ? 'REPARSE_REQUIRED' : response.status === 422 ? 'PARSE_REQUIRED' : 'REVIEW_UNAVAILABLE')
  const data: unknown = await response.json()
  if (!isInteractiveReport(data) || data.module !== module || data.parsed.raw_sha256 !== hash || data.parsed.raw_text !== rawText) throw new Error('INVALID_RESPONSE')
  return data
}
