import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Check, Copy, Download, FileCheck2, RotateCcw } from 'lucide-react'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import type { CommentMode, ReportComment } from '../api/report'
import { ASSESSMENT_OPTIONS } from '../api/review'
import type { AssessmentQuestion } from '../api/review'
import { eligibleComment, requestPlanning, selectedExport } from '../api/planning'
import type { Dimension, PlanningDraft } from '../api/planning'
import { ExportBar, ReportEmpty, ReportHeader, ReportSection, SummaryGrid, SummaryMetric } from './ReportPrimitives'
import PdfExportButton from './PdfExportButton'

const TITLES: Record<Dimension, string> = { SAGITTAL: 'Sagittal', TRANSVERSE: 'Transverse', VERTICAL: 'Vertical', OTHER: 'Other observations', UNAVAILABLE: 'Unavailable assessments' }
export const approvedAIComment = (comment: ReportComment) => eligibleComment(comment) && comment.wording_source === 'GROQ_VALIDATED' && comment.wording_validation === 'ACCEPTED'

function Comment({ comment, selected, onSelect, number }: { comment: ReportComment; selected: boolean; onSelect: () => void; number: number }) {
  return <li className="comment-card">
    <div className="flex items-start gap-3">
      {eligibleComment(comment) && <input type="checkbox" className="mt-1 h-5 w-5 shrink-0 accent-brand" aria-label={`Select comment ${number}`} checked={selected} onChange={onSelect} />}
      <div className="min-w-0 flex-1">
        <p className="whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{comment.text.split('\n')[0]}</p>
        {!!comment.measurements.length && <ul className="mt-3 space-y-2 rounded-lg border border-line bg-canvas p-3 text-xs leading-6">{comment.measurements.map(o => <li key={o.measurement_id} className="flex flex-wrap items-baseline gap-x-2 gap-y-1"><span className="font-semibold">{o.raw_tooth_identifier} · {o.raw_label}</span><code className="rounded bg-white px-1.5 py-0.5 text-[13px] font-semibold text-ink">{o.raw_value}</code><span className="text-muted">programmed value only</span></li>)}</ul>}
      </div>
    </div>
  </li>
}

export default function PlanningWorkspace({ rawText, context, parsed, demo, onComplete }: {
  rawText: string; context: ContextClaims; parsed: AutomaticParseResult; demo: boolean; onComplete: (complete: boolean) => void
}) {
  const [mode, setMode] = useState<CommentMode>('AUTO')
  const [question, setQuestion] = useState<AssessmentQuestion | ''>('')
  const [standard, setStandard] = useState<PlanningDraft | null>(null)
  const [enhanced, setEnhanced] = useState<PlanningDraft | null>(null)
  const [view, setView] = useState<'standard' | 'enhanced'>('standard')
  const [comparisonError, setComparisonError] = useState('')
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const pending = useRef<AbortController | null>(null)
  const revision = useRef(0)
  const output = useRef<HTMLHeadingElement>(null)
  const draft = view === 'standard' ? standard : enhanced
  const hasResults = !!(standard || enhanced)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (hasResults && !loading) output.current?.focus() }, [hasResults, loading])

  function invalidate() {
    revision.current++; pending.current?.abort(); pending.current = null
    setStandard(null); setEnhanced(null); setView('standard'); setComparisonError('')
    setSelected(new Set()); setLoading(false); setError(''); setNotice(''); onComplete(false)
  }
  async function run() {
    if (pending.current) return
    invalidate()
    const controller = new AbortController(), current = ++revision.current
    pending.current = controller; setLoading(true)
    const timer = window.setTimeout(() => controller.abort(), 30_000)
    const request = (wording: CommentMode) => requestPlanning(rawText, context, parsed.raw_sha256, wording, question ? [question] : [], controller.signal, demo, parsed.pipeline.recovery_receipt ?? undefined)
    try {
      const value = await request(mode)
      if (current !== revision.current) return
      if (value.report.comments.some(approvedAIComment)) {
        setEnhanced(value)
        // A second deterministic request provides the actual server template report.
        // It never invokes a wording provider and is unnecessary for template fallbacks.
        try {
          const templates = await request('TEMPLATES')
          if (current !== revision.current) return
          if (templates.report.comments.some(c => c.wording_source !== 'STANDARD_TEMPLATE') || JSON.stringify(templates.report.engine_review) !== JSON.stringify(value.report.engine_review)) throw new Error('COMPARISON_UNAVAILABLE')
          setStandard(templates)
        } catch {
          if (current !== revision.current) return
          setView('enhanced'); setComparisonError('The standard report is unavailable. Your enhanced report is preserved; retry the review to compare both views.')
        }
      } else if (value.report.comments.every(c => c.wording_source === 'STANDARD_TEMPLATE')) {
        setStandard(value)
      } else throw new Error('INVALID_RESPONSE')
      onComplete(true)
    } catch (e) {
      if (current !== revision.current) return
      setError(controller.signal.aborted ? 'The review timed out. Your original text is preserved; please retry.'
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'Read the table again with Parse Table, then retry the review. Your original text is preserved.'
          : 'The planning review could not be completed. Your original text is preserved; please retry.')
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
    catch { if (current === revision.current) setNotice('Clipboard access is unavailable. Use Export TXT.') }
  }
  function download() {
    if (!draft) return
    try {
      const url = URL.createObjectURL(new Blob([draft.export_text], { type: draft.report.export_format }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-planning-draft-${draft.report.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setNotice('Complete DRAFT TXT download requested.')
    } catch { setNotice('Download is unavailable. Copy the complete report.') }
  }
  const report = draft?.report
  const eligible = report?.comments.filter(c => eligibleComment(c) && (view === 'standard' || approvedAIComment(c))) ?? []
  const withheld = report?.comments.filter(c => c.section === 'UNAVAILABLE') ?? []
  const toggle = (id: string) => { setNotice(''); setSelected(old => { const next = new Set(old); next.has(id) ? next.delete(id) : next.add(id); return next }) }
  return <section className="panel" aria-labelledby="planning-heading">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><FileCheck2 size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="planning-heading" className="panel-title">Planning Assistant · Macro Review</h3></div>
    </div>
    <div className="p-5 sm:p-7">
      <p className="max-w-3xl text-sm leading-7 text-muted">Prepare descriptive planning comments from available evidence. Treatment changes and clinical suitability cannot be established from total movements alone.</p>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <div><label className="mb-2 block text-xs font-medium" htmlFor="planning-wording">Wording preference</label><select id="planning-wording" className="context-control" value={mode} onChange={e => { invalidate(); setMode(e.target.value as CommentMode) }}><option value="AUTO">Include AI-assisted wording when available</option><option value="TEMPLATES">Standard template wording only</option></select></div>
        {!demo && <div><label htmlFor="planning-question" className="mb-2 block text-xs font-medium">Clinical context to inspect (optional)</label><select id="planning-question" className="context-control" value={question} onChange={e => { invalidate(); setQuestion(e.target.value as AssessmentQuestion | '') }}><option value="">Descriptive observations only</option>{ASSESSMENT_OPTIONS.map(([id, label]) => <option key={id} value={id}>{label} · unavailable</option>)}</select></div>}
      </div>
      <p id="planning-privacy" className="mt-4 max-w-3xl text-xs leading-6 text-muted">AI assistance can select approved wording only when authorized. Original tables, tooth identifiers and measurements are not shared for wording. Review runs only when you choose below.</p>
      {hasResults ? (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center gap-2 rounded-lg border border-brand/25 bg-brand-soft px-3.5 py-2.5 text-[13px] font-semibold text-brand">
            <Check size={15} strokeWidth={2.5} aria-hidden="true" />
            Planning Review Generated
          </span>
          <button
            type="button"
            className="button button-secondary text-xs"
            onClick={() => void run()}
            disabled={loading}
          >
            <RotateCcw size={14} aria-hidden="true" />
            Re-run Planning Review
          </button>
        </div>
      ) : (
        <button
          type="button"
          className="button button-primary mt-4"
          onClick={() => void run()}
          disabled={loading}
          aria-describedby="planning-privacy"
        >
          {loading ? (
            <>
              <span className="button-spinner" aria-hidden="true" />
              Preparing planning draft…
            </>
          ) : (
            <>
              Run Planning Assistant
              <ArrowRight size={16} aria-hidden="true" />
            </>
          )}
        </button>
      )}
      {loading && <p role="status" className="motion-status mt-3 text-sm text-muted">Preparing your review…</p>}
      {error && <p role="alert" className="motion-status mt-4 text-sm text-notice-ink">{error}</p>}
      {!hasResults && !loading && !error && <ReportEmpty>Your planning review will appear here after you run the assistant.</ReportEmpty>}
      {hasResults && !loading && <article aria-label="Planning Assistant draft" className="motion-enter mt-8 overflow-hidden rounded-2xl border border-line bg-white shadow-panel">
        <ReportHeader eyebrow="Macro · Planning review" title="Planning review draft" headingRef={output} draftStatus={(standard || enhanced)!.report.draft_status}
          badges={[{ label: (standard || enhanced)!.report.engine_review.evidence_domain === 'TEST_ONLY' ? 'Verified synthetic demonstration only' : 'Unverified input', tone: 'brand' }]}
          summary={<p className="text-sm leading-7 text-muted">Programmed movements only. Missing fields are not zero. No findings does not mean no concern.</p>} />
        <div className="p-5 sm:p-7">
          <div className="grid gap-2 sm:grid-cols-2" role="group" aria-label="Report wording views">
            <button type="button" className={`button ${view === 'standard' ? 'button-accent' : 'button-secondary'}`} aria-pressed={view === 'standard'} onClick={() => { setView('standard'); setSelected(new Set()); setNotice('') }}>A. Standard Report — Template-Based</button>
            <button type="button" className={`button ${view === 'enhanced' ? 'button-accent' : 'button-secondary'}`} aria-pressed={view === 'enhanced'} onClick={() => { setView('enhanced'); setSelected(new Set()); setNotice('') }}>B. AI-Assisted Report — Enhanced Wording</button>
          </div>
          <h4 className="mt-6 text-lg font-semibold">{view === 'standard' ? 'Standard Report — Template-Based' : 'AI-Assisted Report — Enhanced Wording'}</h4>
          {comparisonError && <p role="status" className="mt-3 text-sm text-notice-ink">{comparisonError}</p>}
          {!draft && <p role="status" className="my-5 rounded-lg bg-canvas p-4 text-sm text-muted">{view === 'enhanced' ? 'AI-assisted wording is unavailable for this review. The standard report uses template wording.' : 'Standard template wording is unavailable for this review.'}</p>}
          {draft && report && <>
            <p className="mt-2 text-sm leading-7 text-muted">{view === 'standard' ? 'Deterministic comments from eligible findings.' : 'Only approved AI-assisted wording returned for this review is shown below. Facts and restrictions remain unchanged.'} {report.engine_review.coverage.eligible_positions} of {report.engine_review.coverage.declared_positions} positions eligible; {report.engine_review.coverage.unavailable_positions} unavailable.</p>
            {view === 'enhanced' && report.comments.some(c => eligibleComment(c) && !approvedAIComment(c)) && <p className="mt-2 text-sm text-notice-ink">Enhanced wording is available for some comments only. Other comments remain in the standard view; complete enhanced-report exports identify template fallback.</p>}
            <SummaryGrid label="Macro review summary">
              <SummaryMetric label="Eligible positions" value={report.engine_review.coverage.eligible_positions} />
              <SummaryMetric label="Unavailable positions" value={report.engine_review.coverage.unavailable_positions} tone="notice" />
              <SummaryMetric label="Available comments" value={eligible.length} />
              <SummaryMetric label="Withheld assessments" value={withheld.length} tone="notice" />
            </SummaryGrid>
            <div className="mt-5 grid gap-4 xl:grid-cols-3">{draft.sections.filter(s => ['SAGITTAL', 'TRANSVERSE', 'VERTICAL', 'OTHER'].includes(s.dimension)).map(s => {
              const comments = report.comments.filter(c => s.comment_ids.includes(c.comment_id) && (view === 'standard' || approvedAIComment(c)))
              return <ReportSection key={s.dimension} title={TITLES[s.dimension]} label={s.dimension === 'OTHER' ? 'Other observations' : `${TITLES[s.dimension]} review`} className={s.dimension === 'OTHER' ? 'xl:col-span-3' : ''}>
                {comments.length ? <ul className="space-y-3">{comments.map(c => <Comment key={c.comment_id} comment={c} number={report.comments.indexOf(c) + 1} selected={selected.has(c.comment_id)} onSelect={() => toggle(c.comment_id)} />)}</ul> : <p className="text-sm leading-6 text-muted">{view === 'enhanced' ? 'Enhanced wording unavailable for this dimension.' : 'No eligible findings for this dimension.'}</p>}
              </ReportSection>
            })}</div>
            <ReportSection title="Missing context & unavailable assessments" label="Missing context and withheld assessments" tone="notice" className="my-5" description="Clinical diagnosis, suitability, root and periodontal health, occlusion, attachments, IPR, anchorage and sequencing cannot be assessed from these total movements.">
              <p className="text-sm leading-6">{withheld.length} assessments withheld. Unavailable findings are not negative findings.</p>
              {!!withheld.length && <details className="mt-3"><summary className="cursor-pointer text-sm font-medium">Inspect withheld assessments ({withheld.length})</summary><ul className="mt-3 space-y-3">{[...new Set(withheld.map(c => c.text.split('\n')[0]))].map(text => <li key={text} className="text-sm leading-6">{text === 'This rule is disabled. No clinical predicate was evaluated.' ? 'Clinical assessment unavailable; it has not been evaluated.' : text}</li>)}</ul></details>}
            </ReportSection>
            <ExportBar label="Technician comment workspace" title="Export review comments" description={`Exporting ${view === 'standard' ? 'standard template' : 'enhanced wording'} report. Complete exports retain provenance, source values and limitations.`} notice={notice || undefined}>
              <div className="flex w-full flex-wrap items-center gap-2">
                <button className="button button-clear" disabled={!eligible.length} onClick={() => { setNotice(''); setSelected(new Set(eligible.map(c => c.comment_id))) }}>Select all eligible comments</button>
                <button className="button button-clear" disabled={!selected.size} onClick={() => { setNotice(''); setSelected(new Set()) }}>Clear selection</button>
                <p className="text-sm">{selected.size} selected of {eligible.length} eligible comments</p>
                <button className="button button-example" disabled={!selected.size} onClick={() => void copy(true)}><Copy size={15} aria-hidden="true" />Copy selected comments</button>
              </div>
              <button className="button button-secondary" onClick={() => void copy(false)}><Copy size={15} aria-hidden="true" />Copy</button>
              <button className="button button-secondary" onClick={download}><Download size={15} aria-hidden="true" />Export TXT</button>
              <PdfExportButton kind="macro" data={draft} reportId={report.report_id} />
            </ExportBar>
            <p className="mt-4 text-xs leading-6 text-muted">Complete TXT and PDF attachments include detailed findings and source evidence. No clinician approval is recorded.</p>
          </>}
        </div>
      </article>}
    </div>
  </section>
}
