import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Copy, Download, FileCheck2 } from 'lucide-react'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import type { CommentMode, ReportComment } from '../api/report'
import { ASSESSMENT_OPTIONS } from '../api/review'
import type { AssessmentQuestion } from '../api/review'
import { eligibleComment, requestPlanning, selectedExport } from '../api/planning'
import type { Dimension, PlanningDraft } from '../api/planning'
import { EvidenceDisclosure, ExportBar, ReportEmpty, ReportHeader, ReportSection, SummaryGrid, SummaryMetric } from './ReportPrimitives'
import PdfExportButton from './PdfExportButton'

const TITLES: Record<Dimension, string> = { SAGITTAL: 'Sagittal', TRANSVERSE: 'Transverse', VERTICAL: 'Vertical', OTHER: 'Other observations', UNAVAILABLE: 'Unavailable assessments' }

function Comment({ comment, selected, onSelect, number }: { comment: ReportComment; selected: boolean; onSelect: () => void; number: number }) {
  return <li className="comment-card">
    <div className="flex items-start gap-3">
      {eligibleComment(comment) && <input type="checkbox" className="mt-1 h-5 w-5 shrink-0 accent-brand" aria-label={`Select comment ${number}`} checked={selected} onChange={onSelect} />}
      <div className="min-w-0 flex-1">
        <div className="mb-2 flex flex-wrap items-center gap-1.5">
          <span className="report-badge report-badge-brand">{comment.evidence_status === 'TEST_ONLY' ? 'SYNTHETIC · TEST_ONLY' : comment.evidence_status}</span>
          <span className="report-badge">{comment.wording_source === 'GROQ_VALIDATED' ? 'GROQ WORDING' : 'TEMPLATE WORDING'}</span>
          <span className="report-badge">DRAFT · Not approved</span>
        </div>
        <p className="whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{comment.text.split('\n')[0]}</p>
        {!!comment.measurements.length && <ul className="mt-3 space-y-2 rounded-lg border border-line bg-canvas p-3 text-xs leading-6">{comment.measurements.map(o => <li key={o.measurement_id} className="flex flex-wrap items-baseline gap-x-2 gap-y-1"><span className="font-semibold">{o.raw_tooth_identifier} · {o.raw_label}</span><code className="rounded bg-white px-1.5 py-0.5 text-[13px] font-semibold text-ink">{o.raw_value}</code><span className="text-muted">programmed value only</span></li>)}</ul>}
        <EvidenceDisclosure summary="Source values & provenance">
          <p className="raw-text">Comment: {comment.comment_id}</p><p>Rules: {comment.rules.map(r => `${r.rule_id} v${r.version}`).join(', ')}</p>
          <p className="raw-text">Findings: {comment.finding_ids.join(', ')}</p><p className="raw-text">Evidence: {comment.evidence_refs.join(', ') || 'No accepted measurements'}</p>
          <p className="raw-text">Input: {comment.input_refs.join(', ')}</p>
          {comment.measurements.map(o => <div key={o.measurement_id} className="mt-2 rounded bg-white p-3"><p className="raw-text">Original token {o.raw_tooth_identifier} / {o.raw_label}: {o.raw_value}</p><p>Exact scalar {o.signed_decimal} · magnitude {o.magnitude}</p><p>{o.source_spans.map(s => `Line ${s.line}, column ${s.column_start}`).join('; ')}</p><p className="raw-text">{o.components.map(c => `${c.name}: ${c.canonical_value ?? 'UNKNOWN'} (${c.status})`).join(' · ')}</p></div>)}
          <p className="mt-3 whitespace-pre-wrap">Complete engine comment: {comment.text}</p>
          {!!comment.missing_required_fields.length && <p>Missing: {comment.missing_required_fields.join(', ')}</p>}
          {!!comment.abstain_reasons.length && <p>Withheld: {comment.abstain_reasons.join(', ')}</p>}
        </EvidenceDisclosure>
      </div>
    </div>
  </li>
}

export default function PlanningWorkspace({ rawText, context, parsed, demo, onComplete }: {
  rawText: string; context: ContextClaims; parsed: AutomaticParseResult; demo: boolean; onComplete: (complete: boolean) => void
}) {
  const [mode, setMode] = useState<CommentMode>('AUTO')
  const [question, setQuestion] = useState<AssessmentQuestion | ''>('')
  const [draft, setDraft] = useState<PlanningDraft | null>(null)
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [unavailableLimit, setUnavailableLimit] = useState(5)
  const pending = useRef<AbortController | null>(null)
  const revision = useRef(0)
  const output = useRef<HTMLHeadingElement>(null)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (draft) output.current?.focus() }, [draft])

  function invalidate() {
    revision.current++; pending.current?.abort(); pending.current = null
    setDraft(null); setSelected(new Set()); setLoading(false); setError(''); setNotice(''); onComplete(false)
  }
  async function run() {
    if (pending.current) return
    invalidate()
    const controller = new AbortController(), current = ++revision.current
    pending.current = controller; setLoading(true); setUnavailableLimit(5)
    const timer = window.setTimeout(() => controller.abort(), 30_000)
    try {
      const value = await requestPlanning(rawText, context, parsed.raw_sha256, mode, question ? [question] : [], controller.signal, demo, parsed.pipeline.recovery_receipt ?? undefined)
      if (current === revision.current) { setDraft(value); onComplete(true) }
    } catch (e) {
      if (current !== revision.current) return
      setError(controller.signal.aborted ? 'The request timed out. Your original text and parsed values are preserved. Retry when ready.'
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'Recovery evidence expired or changed. Choose Parse Table again; your original text is preserved.'
          : 'The Planning Assistant could not return a valid draft. Your original text is preserved; check the backend and retry.')
    } finally {
      window.clearTimeout(timer)
      if (current === revision.current) { setLoading(false); pending.current = null }
    }
  }
  async function copy(selectedOnly: boolean) {
    if (!draft) return
    const current = revision.current
    const text = selectedOnly ? selectedExport(draft.report, selected) : draft.export_text
    if (!text) return
    try { await navigator.clipboard.writeText(text); if (current === revision.current) setNotice(selectedOnly ? 'Selected comments copied with DRAFT context, withheld assessments and limitations.' : 'Complete DRAFT report copied with provenance and limitations.') }
    catch { if (current === revision.current) setNotice('Clipboard access is unavailable. Download the TXT report or copy the export preview.') }
  }
  function download() {
    if (!draft) return
    try {
      const url = URL.createObjectURL(new Blob([draft.export_text], { type: draft.report.export_format }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-planning-draft-${draft.report.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setNotice('Complete DRAFT TXT download requested.')
    } catch { setNotice('Download is unavailable. Copy the complete report or use the export preview.') }
  }
  const report = draft?.report
  const eligible = report?.comments.filter(eligibleComment) ?? []
  const withheld = report?.comments.filter(c => c.section === 'UNAVAILABLE') ?? []
  const toggle = (id: string) => { setNotice(''); setSelected(old => { const next = new Set(old); next.has(id) ? next.delete(id) : next.add(id); return next }) }
  return <section className="panel" aria-labelledby="planning-heading">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><FileCheck2 size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="planning-heading" className="panel-title">Planning Assistant · Macro Review</h3></div>
      <div className="flex items-center gap-3"><span className="text-xs font-medium text-muted">Descriptive review</span></div>
    </div>
    <div className="p-5 sm:p-7">
      <p className="max-w-3xl text-sm leading-7 text-muted">Inspect the parsed values above, then prepare an organized draft for your review. Clinical assessments, treatment changes, attachments and sequencing remain unavailable.</p>
      {demo && <p className="mt-3 rounded-lg border border-brand/20 bg-brand-soft p-3 text-sm font-medium text-brand">Finova Synthetic Demonstration — TEST_ONLY. This run uses only the fixed server example, never uploaded text.</p>}
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <div><label className="mb-2 block text-xs font-medium" htmlFor="planning-wording">Wording preference</label><select id="planning-wording" className="context-control" value={mode} onChange={e => { invalidate(); setMode(e.target.value as CommentMode) }}><option value="AUTO">Groq wording, when authorized · template fallback</option><option value="TEMPLATES">Deterministic templates · no provider call</option></select></div>
        {!demo && <div><label htmlFor="planning-question" className="mb-2 block text-xs font-medium">Clinical context to inspect (optional)</label><select id="planning-question" className="context-control" value={question} onChange={e => { invalidate(); setQuestion(e.target.value as AssessmentQuestion | '') }}><option value="">Descriptive observations only</option>{ASSESSMENT_OPTIONS.map(([id, label]) => <option key={id} value={id}>{label} · unavailable</option>)}</select></div>}
      </div>
      <p id="planning-privacy" className="mt-4 max-w-3xl text-xs leading-6 text-muted">This action rechecks unchanged synthetic input on this app’s backend. Groq can choose approved phrases only when authorized; raw tables, tooth identifiers and measurements are never sent for wording. No automatic run or retry.</p>
      <button type="button" className="button button-primary mt-4" onClick={() => void run()} disabled={loading} aria-describedby="planning-privacy">{loading ? <><span className="button-spinner" aria-hidden="true" />Preparing planning draft…</> : <>Run Planning Assistant<ArrowRight size={16} aria-hidden="true" /></>}</button>
      {loading && <p role="status" className="motion-status mt-3 text-sm text-muted">Rechecking evidence and preparing the descriptive DRAFT…</p>}
      {error && <p role="alert" className="motion-status mt-4 text-sm text-notice-ink">{error}</p>}
      {!draft && !loading && !error && <ReportEmpty>Your planning review will appear here after you run the assistant.</ReportEmpty>}
      {draft && report && <article aria-label="Planning Assistant draft" className="motion-enter mt-8 overflow-hidden rounded-2xl border border-line bg-white shadow-panel">
        <ReportHeader
          eyebrow="Macro · Planning review"
          title="Planning review draft"
          headingRef={output}
          draftStatus={report.draft_status}
          badges={[
            { label: report.engine_review.evidence_domain === 'TEST_ONLY' ? 'Synthetic · TEST_ONLY' : 'Unverified input', tone: 'brand' },
            { label: 'Not approved', tone: 'notice' },
          ]}
          summary={<>
            <p className="text-sm leading-7 text-muted">{report.engine_review.evidence_domain === 'TEST_ONLY' ? 'Synthetic demonstration evidence only.' : 'Vendor semantics remain unverified.'} {report.engine_review.coverage.eligible_positions} of {report.engine_review.coverage.declared_positions} positions eligible; {report.engine_review.coverage.unavailable_positions} unavailable. Missing fields are not zero.</p>
            <SummaryGrid label="Macro review summary">
              <SummaryMetric label="Eligible positions" value={report.engine_review.coverage.eligible_positions} detail={`of ${report.engine_review.coverage.declared_positions} declared`} />
              <SummaryMetric label="Unavailable positions" value={report.engine_review.coverage.unavailable_positions} detail="Withheld, not normal" tone="notice" />
              <SummaryMetric label="Authorized comments" value={eligible.length} detail="Available for selection" />
              <SummaryMetric label="Withheld assessments" value={withheld.length} detail="Unavailable, not negative" tone="notice" />
            </SummaryGrid>
          </>}
        >
          <div className="mt-4 rounded-lg border border-line bg-canvas p-3 text-xs leading-6 text-muted">
            <p>Wording: {report.generation.used_mode.replaceAll('_', ' ')}. {report.generation.attempts === 0 ? 'No provider call was made.' : 'Groq received approved wording choices only.'}</p>
            <details><summary className="cursor-pointer">Wording details</summary>
              <p>{report.generation.reason === 'NO_ELIGIBLE_FINDINGS' ? 'No authorized descriptive findings; abstention templates were used.' : report.generation.reason === 'GROQ_VALIDATED' ? 'Wording passed strict validation; exact facts remain locally assembled.' : report.generation.reason === 'STANDARD_TEMPLATES_SELECTED' ? 'Deterministic templates selected.' : 'Template fallback is available when Groq is disabled, unavailable or fails validation.'}</p>
              {report.generation.reason}
            </details>
          </div>
        </ReportHeader>

        <div className="p-5 sm:p-7">
          <p className="mb-5 text-xs leading-6 text-muted">Dimensions organize authorized descriptions; they do not assess a complete clinical dimension. No findings does not mean no concern. Mixed or incompatible observations remain separate.</p>
          <div className="grid gap-4 xl:grid-cols-3">{draft.sections.filter(s => ['SAGITTAL', 'TRANSVERSE', 'VERTICAL'].includes(s.dimension)).map(s => <ReportSection key={s.dimension} title={TITLES[s.dimension]} label={`${TITLES[s.dimension]} review`} description={s.explanation}>
            <ul className="space-y-3">{s.comment_ids.map(id => { const c = report.comments.find(c => c.comment_id === id)!; return <Comment key={id} comment={c} number={report.comments.indexOf(c) + 1} selected={selected.has(id)} onSelect={() => toggle(id)} /> })}</ul>
          </ReportSection>)}</div>
          {draft.sections.filter(s => s.dimension === 'OTHER').map(s => <ReportSection key={s.dimension} title="Other observations" label="Other observations" description={s.explanation} className="mt-4">
            <ul className="grid gap-3 lg:grid-cols-2">{s.comment_ids.map(id => { const c = report.comments.find(c => c.comment_id === id)!; return <Comment key={id} comment={c} number={report.comments.indexOf(c) + 1} selected={selected.has(id)} onSelect={() => toggle(id)} /> })}</ul>
          </ReportSection>)}
          <ReportSection title="Missing context & unavailable assessments" label="Missing context and withheld assessments" tone="notice" className="my-5" description="Clinical diagnosis, suitability, root and periodontal health, occlusion, attachments, IPR, anchorage and sequencing cannot be assessed from these total movements. Disabled rules are not negative clinical findings.">
            <details>
              <summary className="cursor-pointer text-sm font-medium">Inspect withheld assessments ({withheld.length})</summary>
              <ul className="mt-3 space-y-3">{withheld.slice(0, unavailableLimit).map(c => <Comment key={c.comment_id} comment={c} number={0} selected={false} onSelect={() => {}} />)}</ul>
              {withheld.length > unavailableLimit && <button className="button button-clear mt-3" onClick={() => setUnavailableLimit(v => v + 10)}>Show more withheld assessments</button>}
            </details>
          </ReportSection>

          <ExportBar
            label="Technician comment workspace"
            title="Export review comments"
            description="Select eligible descriptive comments to copy. Every export retains DRAFT status, evidence context and limitations. Copying does not approve a plan or send anything to CAD."
            notice={notice || undefined}
          >
            <div className="flex w-full flex-wrap items-center gap-2">
              <button className="button button-clear" disabled={!eligible.length} onClick={() => { setNotice(''); setSelected(new Set(eligible.map(c => c.comment_id))) }}>Select all eligible comments</button>
              <button className="button button-clear" disabled={!selected.size} onClick={() => { setNotice(''); setSelected(new Set()) }}>Clear selection</button>
              <p className="text-sm">{selected.size} selected of {eligible.length} eligible comments</p>
              <button className="button button-example disabled:opacity-50" disabled={!selected.size} onClick={() => void copy(true)}><Copy size={15} aria-hidden="true" />Copy selected comments</button>
            </div>
            <div className="flex w-full flex-wrap gap-2">
              <button className="button button-clear" onClick={() => void copy(false)}>Copy complete DRAFT report</button>
              <button className="button button-clear" onClick={download}><Download size={15} aria-hidden="true" />Download DRAFT (TXT)</button>
              <PdfExportButton kind="macro" data={draft} reportId={report.report_id} />
            </div>
          </ExportBar>

          <details className="technical-details"><summary>Clinical limitations & clinician-review notes</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{report.limitations.map(l => <li key={l}>{l}</li>)}</ul><p className="mt-3 text-xs text-muted">The clinician must independently assess clinical context. This prototype records no approval or sign-off.</p></details>
          <details className="technical-details"><summary>Detailed findings, provenance & rule ledger ({report.engine_review.evaluations.length})</summary><ul className="mt-3 space-y-2 text-xs leading-6">{report.engine_review.evaluations.map(e => <li key={e.rule_id}>{e.rule_id} · {e.status} · {e.execution ?? 'Legacy'} · {e.approval_status ?? 'Unknown'}</li>)}</ul><pre tabIndex={0} aria-label="Planning provenance JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs">{JSON.stringify(draft, null, 2)}</pre></details>
          <details className="technical-details"><summary>Complete DRAFT TXT preview</summary><pre tabIndex={0} aria-label="Planning export preview" className="raw-text mt-3 max-h-96 overflow-auto text-xs leading-6">{draft.export_text}</pre></details>
        </div>
      </article>}
    </div>
  </section>
}
