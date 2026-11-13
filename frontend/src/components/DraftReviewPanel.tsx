import { useEffect, useRef, useState } from 'react'
import { ASSESSMENT_OPTIONS, requestReview } from '../api/review'
import type { AssessmentQuestion, DraftReview, ReviewFinding } from '../api/review'
import type { ContextClaims, SourceClaim } from '../api/parse'
import FinalReportPanel from './FinalReportPanel'

function FindingCard({ finding }: { finding: ReviewFinding }) {
  return <li className="min-w-0 rounded-lg border border-line p-4 text-xs leading-6">
    <p className="font-semibold">{finding.triggering_rules.map(r => `${r.rule_id} v${r.version}`).join(' · ')} <span className="font-normal text-muted">/ {finding.status}</span></p>
    <p className="mt-1">{finding.message}</p>
    {Object.keys(finding.summary_counts).length > 0 && <p className="mt-2 text-muted">{Object.entries(finding.summary_counts).map(([key, count]) => `${key.replaceAll('_', ' ')}: ${count}`).join(' · ')}</p>}
    {finding.observed_measurements.map(o => {
      const v = Object.fromEntries(o.components.map(c => [c.name, c.canonical_value]))
      return <div key={o.measurement_id} className="mt-3 rounded-md bg-canvas p-3">
        <p className="font-medium">{v.tooth_identifier} · {v.axis} · {o.magnitude} {v.unit} · {v.direction}</p>
        <p>Source: {v.source_application} {v.source_version} · Evidence: {o.verification}</p>
        <p>Mode: {v.plan_mode} · Basis: {v.reference_basis} · Scope: {v.scope} · Stage: {v.stage_index ?? 'unavailable'} ({v.stage_kind ?? 'unavailable'}) · Frame: {v.coordinate_frame}</p>
        <p>Original tooth / label: <code className="raw-text">{o.raw_tooth_identifier} / {o.raw_label}</code></p>
        <p>Original cell: <code className="raw-text">{o.raw_value}</code> · Lexical scalar: {o.signed_decimal} · Original sign/direction: {o.raw_sign ?? '(unsigned)'} / {o.raw_direction ?? '(absent)'}</p>
        <p>Source locations: {o.source_spans.map(s => `L${s.line}:C${s.column_start}`).join(', ')}</p>
      </div>
    })}
    {finding.missing_required_fields.length > 0 && <p className="mt-2 text-muted">Required: {finding.missing_required_fields.join(', ')}</p>}
    {finding.abstain_reason && <p className="mt-1 text-muted">Withheld: {finding.abstain_reason}</p>}
    {finding.conflict_group && <p className="text-notice-ink">Conflict: {finding.conflict_group}</p>}
    <details className="mt-2"><summary className="cursor-pointer text-muted">Traceability</summary><p className="raw-text">Finding: {finding.finding_id}</p><p className="raw-text">Input: {finding.input_refs.join(', ') || 'System control'}</p><p className="raw-text">Evidence: {finding.evidence_refs.join(', ') || 'No accepted measurement evidence'}</p></details>
  </li>
}

export default function DraftReviewPanel({ rawText, source, context, rawHash, recoveryReceipt }: { rawText: string; source: SourceClaim; context: ContextClaims; rawHash: string; recoveryReceipt?: string }) {
  const [question, setQuestion] = useState<AssessmentQuestion | ''>('')
  const [report, setReport] = useState<DraftReview | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [limit, setLimit] = useState(25)
  const pending = useRef<AbortController | null>(null)
  const revision = useRef(0)
  useEffect(() => () => { revision.current += 1; pending.current?.abort() }, [])

  function invalidate() {
    revision.current += 1
    pending.current?.abort()
    pending.current = null
    setReport(null); setLoading(false); setError(null); setLimit(25)
  }

  async function review() {
    if (pending.current) return
    const controller = new AbortController()
    const current = ++revision.current
    pending.current = controller
    setReport(null); setError(null); setLoading(true); setLimit(25)
    const timeout = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const result = await requestReview(rawText, source, context, rawHash, question ? [question] : [], controller.signal, recoveryReceipt)
      if (current === revision.current) setReport(result)
    } catch (failure) {
      if (current !== revision.current) return
      const code = failure instanceof Error ? failure.message : ''
      setError(code === 'REPARSE_REQUIRED' ? 'Recovery evidence expired or changed. Choose Parse Table again; your raw input is preserved.' : controller.signal.aborted ? 'The draft review request timed out. Your raw input and parse results are preserved.'
        : code === 'SIZE_LIMIT' ? 'The review request exceeded the size limit. Your raw input and parse results are preserved.'
          : code === 'REQUEST_INVALID' ? 'The review request was rejected. Check the input and metadata. Your raw input and parse results are preserved.'
            : 'A valid draft review could not be returned. Check the local backend and retry. Your raw input and parse results are preserved.')
    } finally {
      window.clearTimeout(timeout)
      if (current === revision.current) { pending.current = null; setLoading(false) }
    }
  }

  const descriptions = report?.findings.filter(f => f.finding_type === 'DESCRIPTIVE' && f.status === 'OBSERVED') ?? []
  const unavailable = report?.findings.filter(f => ['SEMANTICS_UNKNOWN', 'CONTEXT_REQUIRED', 'DISABLED', 'SUPPRESSED', 'PARSE_INVALID'].includes(f.status)) ?? []
  return <section className="panel mt-6" aria-labelledby="review-heading">
    <div className="panel-heading flex-wrap"><h2 id="review-heading" className="font-semibold">Draft descriptive review</h2><span className="rounded-md bg-notice px-2 py-1 text-xs font-semibold text-notice-ink">DRAFT · CLINICIAN REVIEW</span></div>
    <div className="p-5 sm:p-6">
      <p id="review-hint" className="max-w-3xl text-sm leading-6 text-muted">Create draft review sends the unchanged synthetic text and claims to this app’s backend again. Vendor analysis remains unavailable. Clinical rules are disabled; a draft is not an approval or a treatment recommendation.</p>
      <label htmlFor="review-question" className="mb-2 mt-4 block text-sm font-medium">Requested assessment <span className="font-normal text-muted">(optional; reports why it is unavailable)</span></label>
      <select id="review-question" value={question} onChange={e => { invalidate(); setQuestion(e.target.value as AssessmentQuestion | '') }} className="w-full rounded-lg border border-field bg-white p-3 text-sm sm:max-w-lg">
        <option value="">Descriptive observations only</option>
        {ASSESSMENT_OPTIONS.map(([id, label]) => <option key={id} value={id}>{label}</option>)}
      </select>
      <div className="mt-4"><button type="button" onClick={review} disabled={loading} aria-describedby="review-hint" className="button border border-brand bg-brand text-white disabled:bg-canvas disabled:text-muted">{loading ? 'Creating draft…' : 'Create draft review'}</button></div>
      {loading && <p role="status" className="mt-3 text-sm text-muted">Checking review eligibility and preparing a draft…</p>}
      {error && <p role="alert" className="mt-3 text-sm text-notice-ink">{error}</p>}
      {report && <div className="mt-6" aria-label="Draft review results">
        <p role="status" className="rounded-lg border border-notice-line bg-notice p-4 text-sm leading-6 text-notice-ink">{report.notice}</p>
        <p className="raw-text mt-4 text-xs leading-6 text-muted">Evidence domain: {report.evidence_domain} · Source claim: {report.source.source_claim} · Version claim: {report.source.context.source_version ?? 'unavailable'} · Lexical source status: {report.source.verification_status}</p>
        <p className="my-3 text-xs text-muted">{report.coverage.eligible_positions} eligible / {report.coverage.declared_positions} declared positions · {report.coverage.unavailable_positions} unavailable · Expected axis coverage unknown</p>
        <h3 className="mb-3 mt-5 text-sm font-semibold">Descriptive findings</h3>
        {descriptions.length ? <ul className="space-y-3">{descriptions.map(f => <FindingCard key={f.finding_id} finding={f} />)}</ul> : <p className="rounded-lg bg-canvas p-4 text-sm">No authorized descriptive movement findings are available. This does not mean no clinical concern.</p>}
        <h3 className="mb-3 mt-6 text-sm font-semibold">Unavailable assessments</h3>
        <ul className="grid gap-3 lg:grid-cols-2">{unavailable.slice(0, limit).map(f => <FindingCard key={f.finding_id} finding={f} />)}</ul>
        {unavailable.length > limit && <button type="button" className="button button-clear mt-4" onClick={() => setLimit(limit + 25)}>Show more unavailable assessments ({unavailable.length - limit} remaining)</button>}
        <h3 className="mb-3 mt-6 text-sm font-semibold">Limitations</h3><ul className="list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{report.limitations.map(item => <li key={item}>{item}</li>)}</ul>
        <details className="mt-5 rounded-lg border border-line p-4"><summary className="cursor-pointer text-sm font-medium">Complete DRAFT findings and rule statuses (JSON, in memory)</summary><pre tabIndex={0} aria-label="Full draft review JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs">{JSON.stringify(report, null, 2)}</pre></details>
        <FinalReportPanel rawText={rawText} source={source} context={context} rawHash={rawHash} questions={question ? [question] : []} recoveryReceipt={recoveryReceipt} />
      </div>}
    </div>
  </section>
}
