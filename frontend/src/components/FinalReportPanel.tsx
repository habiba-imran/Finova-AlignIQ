import { useEffect, useRef, useState } from 'react'
import { Copy, Download, FileCheck2 } from 'lucide-react'
import { requestReport } from '../api/report'
import type { CommentMode, FinalDraftReport, ReportComment } from '../api/report'
import type { AssessmentQuestion } from '../api/review'
import type { ContextClaims, SourceClaim } from '../api/parse'

const REASONS: Record<string, string> = {
  NO_ELIGIBLE_FINDINGS: 'No eligible findings: Groq was not called. Standard abstention templates were used.',
  GROQ_NOT_CONFIGURED: 'Groq is not enabled on the backend. Standard Templates were used.',
  GROQ_CONFIGURATION_INVALID: 'Groq configuration is unavailable. Standard Templates were used.',
  REAL_PATIENT_TRANSMISSION_DISABLED: 'Real clinical information cannot be transmitted. Standard Templates were used.',
  STANDARD_TEMPLATES_SELECTED: 'Standard Templates selected. No provider call was made.',
  GROQ_VALIDATED: 'Groq wording passed exact validation. Facts and provenance were assembled locally.',
}

function CommentCard({ comment }: { comment: ReportComment }) {
  return <li className="min-w-0 rounded-lg border border-line p-4 sm:p-5">
    <div className="mb-2 flex flex-wrap items-center justify-between gap-2 text-xs text-muted"><span>{comment.rules.map(r => `${r.rule_id} v${r.version}`).join(' · ')}</span><span>{comment.evidence_status} · {comment.wording_source === 'GROQ_VALIDATED' ? 'Groq AI · validated' : 'Standard Template'}</span></div>
    <p className="whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{comment.text}</p>
    <details className="mt-3 text-xs leading-6 text-muted"><summary className="cursor-pointer font-medium">Rule IDs and source provenance</summary>
      <p className="raw-text">Findings: {comment.finding_ids.join(', ')}</p><p className="raw-text">Input: {comment.input_refs.join(', ') || 'System control'}</p>
      <p className="raw-text">Evidence: {comment.evidence_refs.join(', ') || 'No accepted measurement evidence'}</p>
      <p className="raw-text">Evaluation: {comment.evaluation_statuses.join(', ')}</p>
      {comment.fallback_reason && <p>Wording fallback: {comment.fallback_reason}</p>}
    </details>
  </li>
}

export default function FinalReportPanel({ rawText, source, context, rawHash, questions, recoveryReceipt }: {
  rawText: string; source: SourceClaim; context: ContextClaims; rawHash: string; questions: AssessmentQuestion[]; recoveryReceipt?: string
}) {
  const [mode, setMode] = useState<CommentMode>('AUTO')
  const [report, setReport] = useState<FinalDraftReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [exportStatus, setExportStatus] = useState<string | null>(null)
  const [limit, setLimit] = useState(10)
  const pending = useRef<AbortController | null>(null)
  const revision = useRef(0)
  useEffect(() => () => { revision.current += 1; pending.current?.abort() }, [])

  function invalidate() {
    revision.current += 1; pending.current?.abort(); pending.current = null
    setReport(null); setLoading(false); setError(null); setExportStatus(null); setLimit(10)
  }

  async function generate() {
    if (pending.current) return
    const controller = new AbortController(); const current = ++revision.current
    pending.current = controller
    setReport(null); setError(null); setExportStatus(null); setLoading(true); setLimit(10)
    const timeout = window.setTimeout(() => controller.abort(), 30_000)
    try {
      const result = await requestReport(rawText, source, context, rawHash, questions, mode, controller.signal, recoveryReceipt)
      if (current === revision.current) setReport(result)
    } catch (failure) {
      if (current !== revision.current) return
      const code = failure instanceof Error ? failure.message : ''
      setError(code === 'REPARSE_REQUIRED' ? 'Recovery evidence expired or changed. Choose Parse Table again; your raw input is preserved.' : controller.signal.aborted ? 'Report creation timed out. Your raw input and review are preserved.'
        : code === 'SIZE_LIMIT' ? 'The report request exceeded the size limit. Your input and review are preserved.'
          : code === 'REQUEST_INVALID' ? 'The report request was rejected. Check the input and metadata. Your input and review are preserved.'
            : 'A valid report could not be returned. Check the local backend and retry. Your input and review are preserved.')
    } finally {
      window.clearTimeout(timeout)
      if (current === revision.current) { pending.current = null; setLoading(false) }
    }
  }

  async function copy() {
    if (!report) return
    const current = revision.current
    try {
      await navigator.clipboard.writeText(report.export_text)
      if (current === revision.current) setExportStatus('Report copied with draft status, limitations and provenance.')
    } catch {
      if (current === revision.current) setExportStatus('Clipboard access is unavailable. Download the TXT report or copy the export preview.')
    }
  }

  function download() {
    if (!report) return
    try {
      const url = URL.createObjectURL(new Blob([report.export_text], { type: report.export_format }))
      const anchor = document.createElement('a')
      anchor.href = url; anchor.download = `finova-aligniq-draft-${report.report_id.slice(0, 12)}.txt`
      document.body.append(anchor); anchor.click(); anchor.remove()
      window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setExportStatus('TXT download requested with draft status, limitations and provenance.')
    } catch {
      setExportStatus('Download is unavailable. Copy the report or use the export preview.')
    }
  }

  const unavailable = report?.comments.filter(c => c.section === 'UNAVAILABLE') ?? []
  return <section aria-labelledby="final-report-heading" className="mt-7 min-w-0 border-t border-line pt-7">
    <div className="flex items-center gap-2 text-brand"><FileCheck2 size={19} aria-hidden="true" /><h3 id="final-report-heading" className="font-semibold">Final draft report</h3></div>
    <p id="report-privacy-hint" className="mt-3 max-w-3xl text-xs leading-6 text-muted">Create final report sends the unchanged synthetic text to this app’s backend again. Groq AI can select approved wording only when configured and findings are eligible. It receives no raw table, identifiers or measurements. Real-patient transmission is disabled.</p>
    <label htmlFor="comment-mode" className="mb-2 mt-4 block text-sm font-medium">Comment generation mode</label>
    <select id="comment-mode" value={mode} onChange={e => { invalidate(); setMode(e.target.value as CommentMode) }} className="context-control sm:max-w-lg">
      <option value="AUTO">Groq AI — automatic template fallback</option><option value="TEMPLATES">Standard Templates</option>
    </select>
    <div className="mt-4"><button type="button" onClick={generate} disabled={loading} aria-describedby="report-privacy-hint" className="button border border-brand bg-brand text-white disabled:bg-canvas disabled:text-muted">{loading ? 'Creating report…' : 'Create final report'}</button></div>
    {loading && <p role="status" className="mt-3 text-sm text-muted">Rechecking findings and assembling the final draft report…</p>}
    {error && <p role="alert" className="mt-3 text-sm text-notice-ink">{error}</p>}
    {report && <article aria-label="Final draft report results" className="mt-6 overflow-hidden rounded-xl border border-line bg-white">
      <header className="border-b border-line bg-brand-soft p-5 sm:p-7">
        <p className="text-sm font-semibold tracking-wide text-brand">FINOVA ALIGNIQ</p><h4 className="mt-2 text-xl font-semibold tracking-tight">Descriptive Planning Report</h4>
        <p className="mt-4 inline-block rounded-md border border-notice-line bg-notice px-3 py-2 text-sm font-semibold text-notice-ink">{report.draft_status}</p>
        <p className="mt-3 text-xs text-muted">Prototype — not for clinical use. No treatment recommendations or clinician approval.</p>
      </header>
      <div className="p-5 sm:p-7">
        <dl className="grid gap-4 text-xs leading-6 sm:grid-cols-2">
          <div><dt className="font-semibold">Source platform claim</dt><dd className="raw-text">{report.engine_review.source.source_claim} · version {report.engine_review.source.context.source_version ?? 'UNKNOWN'} (unverified)</dd></div>
          <div><dt className="font-semibold">Semantic evidence status</dt><dd>{report.engine_review.evidence_domain}</dd></div>
          <div><dt className="font-semibold">Verified plan mode, scope and basis</dt><dd>{report.comments.some(c => c.measurements.length) ? 'Listed with each accepted observation and its evidence status.' : 'UNKNOWN — no authorized measurements.'}</dd></div>
          <div><dt className="font-semibold">Wording used</dt><dd>{report.generation.used_mode === 'GROQ_AI' ? 'Groq AI · validated' : report.generation.used_mode === 'MIXED' ? 'Groq AI + Standard Templates' : 'Standard Templates'}</dd></div>
        </dl>
        <p className="mt-4 rounded-lg bg-canvas p-3 text-xs leading-6 text-muted">{REASONS[report.generation.reason] ?? 'Some or all wording was replaced by Standard Templates after provider or validation failure.'}</p>
        <h5 className="mb-3 mt-6 font-semibold">Available observations</h5>
        <p className="text-sm leading-6 text-muted">{report.engine_review.coverage.eligible_positions} eligible of {report.engine_review.coverage.declared_positions} declared positions; {report.engine_review.coverage.unavailable_positions} unavailable. Expected coverage remains unknown.</p>
        {(['TOOTH', 'SUMMARY'] as const).map(section => <div key={section} className="mt-6">
          <h5 className="mb-3 font-semibold">{section === 'TOOTH' ? 'Tooth-wise descriptive comments' : 'Movement distribution summary'}</h5>
          {report.comments.some(c => c.section === section) ? <ul className="space-y-3">{report.comments.filter(c => c.section === section).map(c => <CommentCard key={c.comment_id} comment={c} />)}</ul>
            : <p className="rounded-lg bg-canvas p-4 text-sm leading-6 text-muted">No authorized observations available. This does not mean no clinical concern.</p>}
        </div>)}
        <h5 className="mb-3 mt-6 font-semibold">Unavailable assessments and missing information</h5>
        <ul className="space-y-3">{unavailable.slice(0, limit).map(c => <CommentCard key={c.comment_id} comment={c} />)}</ul>
        {unavailable.length > limit && <button type="button" className="button button-clear mt-4" onClick={() => setLimit(limit + 10)}>Show more report assessments ({unavailable.length - limit} remaining)</button>}
        <h5 className="mb-3 mt-6 font-semibold">Clinical limitations and scope</h5><ul className="list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{report.limitations.map(item => <li key={item}>{item}</li>)}</ul>
        <p className="raw-text mt-5 text-[11px] leading-6 text-muted">Report: {report.report_id}<br />Input SHA-256: {report.engine_review.raw_sha256}<br />Rules: {report.engine_review.rule_set_version}</p>
        <div className="mt-5 flex flex-wrap gap-3"><button type="button" className="button button-example" onClick={copy}><Copy size={15} aria-hidden="true" />Copy Report</button><button type="button" className="button button-clear" onClick={download}><Download size={15} aria-hidden="true" />Download Report (TXT)</button></div>
        {exportStatus && <p role="status" className="mt-3 text-xs leading-6 text-muted">{exportStatus}</p>}
        <details className="mt-5 rounded-lg border border-line p-4"><summary className="cursor-pointer text-sm font-medium">Complete TXT export preview</summary><pre aria-label="Report export preview" tabIndex={0} className="raw-text mt-4 max-h-96 overflow-auto text-xs leading-6">{report.export_text}</pre></details>
        <details className="mt-3 rounded-lg border border-line p-4"><summary className="cursor-pointer text-sm font-medium">Full report contract (JSON, in memory)</summary><pre aria-label="Final report JSON" tabIndex={0} className="raw-text mt-4 max-h-96 overflow-auto text-xs leading-6">{JSON.stringify(report, null, 2)}</pre></details>
      </div>
    </article>}
  </section>
}
