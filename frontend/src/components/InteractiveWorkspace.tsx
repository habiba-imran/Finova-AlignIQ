import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Check, Copy, Download, FileCheck2, RotateCcw } from 'lucide-react'
import { emptyReviewDetails, requestInteractiveReview, sectionStatusLabel } from '../api/interactive'
import type { DemoModule, InteractiveReport, ReviewDetails } from '../api/interactive'
import type { AutomaticParseResult, ContextClaims, ParseResult } from '../api/parse'
import PdfExportButton from './PdfExportButton'
import { commentParagraphs, moduleReviewPresentation } from '../reviewPresentation'
import FunctionalResults from './FunctionalResults'
import type { FunctionalContext } from '../api/functional'
import type { PlanningOptions } from '../api/planningOptions'

const TITLES = { macro: 'Planning', micro: 'Attachment', nano: 'Sequencing' }
const ACTIONS = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }

function partialParseExplanation(parsed: ParseResult): string {
  const unresolved = parsed.issues.some(issue => issue.severity === 'ERROR') || parsed.measurements.some(m =>
    m.field_status === 'AMBIGUOUS' || !['PARSED', 'EXPLICIT_ZERO', 'MISSING', 'NOT_PRESENT'].includes(m.numeric_status))
  if (unresolved) return 'Some entries could not be interpreted reliably. Review the marked table; unresolved values remain unknown and are not used as numerical findings.'
  const missingCount = parsed.coverage.missing
  const missingLabels = [...new Set(parsed.measurements.filter(m => m.numeric_status === 'MISSING' || m.numeric_status === 'NOT_PRESENT').map(m => m.raw_label.trim()))]
  const unrecognizedLabels = [...new Set(parsed.measurements.filter(m => !m.recognized_label).map(m => m.raw_label.trim()))]

  if (missingCount > 0 && unrecognizedLabels.length === 0) {
    const cols = missingLabels.length > 0 ? ` in ${missingLabels.slice(0, 3).join(', ')}${missingLabels.length > 3 ? '…' : ''}` : ''
    return `Successfully parsed with ${missingCount} missing value${missingCount === 1 ? '' : 's'}${cols}. Missing values remain unknown, not zero.`
  }

  if (unrecognizedLabels.length > 0 && missingCount === 0) {
    return `All recognized movement values were parsed successfully. Marked as partial because ${unrecognizedLabels.length === 1 ? 'a column heading was' : 'some column headings were'} unrecognized (${unrecognizedLabels.join(', ')}).`
  }

  if (missingCount > 0 && unrecognizedLabels.length > 0) {
    return `All available movement values were parsed successfully. Marked as partial because ${missingCount} cell${missingCount === 1 ? ' has a' : 's have'} missing value and some headings were unrecognized (${unrecognizedLabels.join(', ')}). Missing values are retained as unknown.`
  }

  return 'All available movement values were parsed successfully. Omitted or unassigned cells are preserved as unknown rather than assumed to be zero.'
}

export default function InteractiveWorkspace({ module, rawText, context, parsed, onComplete, reviewDetails = emptyReviewDetails(), savedReport = null, onReportChange = () => {}, planningContext = null, planningOptions = null }: {
  module: DemoModule; rawText: string; context: ContextClaims; parsed: AutomaticParseResult; onComplete: (complete: boolean) => void; reviewDetails?: ReviewDetails; onDetailsChange?: (details: ReviewDetails) => void; savedReport?: InteractiveReport | null; onReportChange?: (report: InteractiveReport | null) => void; planningContext?: FunctionalContext | null; planningOptions?: PlanningOptions | null
}) {
  const [report, setReport] = useState<InteractiveReport | null>(savedReport)
  const [loading, setLoading] = useState(false), [error, setError] = useState(''), [notice, setNotice] = useState('')
  const revision = useRef(0), pending = useRef<AbortController | null>(null), heading = useRef<HTMLHeadingElement>(null)
  const errorHeading = useRef<HTMLParagraphElement>(null)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (report) { onComplete(true); heading.current?.focus(); heading.current?.scrollIntoView?.({ block: 'start', behavior: 'instant' }) } }, [report])
  useEffect(() => { if (error) errorHeading.current?.focus() }, [error])
  const supported = !['INVALID', 'UNSUPPORTED'].includes(parsed.status) && parsed.measurements.length > 0
  const presentation = report ? moduleReviewPresentation(report) : null
  const sourceRows = report?.observations.filter(o => o.measurements.length > 0) ?? []
  async function run() {
    if (pending.current || !supported) return
    const current = ++revision.current, controller = new AbortController()
    pending.current = controller; setLoading(true); setError(''); setNotice(''); setReport(null); onReportChange(null); onComplete(false)
    const timer = window.setTimeout(() => controller.abort(), 55_000)
    try {
      const result = await requestInteractiveReview(module, rawText, context, parsed.raw_sha256, parsed.pipeline.recovery_receipt, controller.signal, reviewDetails, planningContext, planningOptions)
      if (revision.current === current) { setReport(result); onReportChange(result); onComplete(true) }
    } catch (e) {
      if (revision.current !== current) return
      setError(e instanceof Error && e.message.startsWith('DETAILS_ERROR:') ? e.message.slice('DETAILS_ERROR:'.length)
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'The input changed or parsing evidence expired. Parse Table again, then retry.'
        : controller.signal.aborted ? 'The review timed out. Your input is preserved; please retry.'
          : 'The review could not be generated. Your input is preserved; check the table and retry.')
    } finally {
      window.clearTimeout(timer)
      if (revision.current === current) { pending.current = null; setLoading(false) }
    }
  }
  async function copy() {
    if (!report) return
    const current = revision.current
    try { await navigator.clipboard.writeText(report.export_text); if (current === revision.current) setNotice('Complete report copied.') }
    catch { if (current === revision.current) setNotice('Clipboard unavailable. Use Export TXT.') }
  }
  function download() {
    if (!report) return
    try {
      const url = URL.createObjectURL(new Blob([report.export_text], { type: 'text/plain;charset=utf-8' }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-${module}-synthetic-${report.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setNotice('Complete TXT download requested.')
    } catch { setNotice('Download unavailable. Use Copy.') }
  }
  return <section className="panel" aria-label={`${TITLES[module]} synthetic review`}>
    <div className="panel-heading"><div className="flex items-center gap-2.5"><FileCheck2 size={17} className="text-brand" aria-hidden="true" /><h3 className="panel-title">{TITLES[module]} review</h3></div></div>
    <div className="p-5 sm:p-7">
      <p className="text-sm leading-7 text-muted">{module === 'macro' ? 'Prepare readable planning comments from the programmed movements in your table.' : module === 'micro' ? 'Generate attachment-review draft comments directly from the rotation, angulation and inclination recorded in your TMT.' : 'Generate sequencing-review draft comments directly from the translations, vertical movements and context recorded in your TMT.'}</p>
      {report ? (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center gap-2 rounded-lg border border-brand/25 bg-brand-soft px-3.5 py-2.5 text-[13px] font-semibold text-brand">
            <Check size={15} strokeWidth={2.5} aria-hidden="true" />
            Review Generated
          </span>
          <button
            type="button"
            className="button button-secondary text-xs"
            onClick={() => void run()}
            disabled={loading}
            title={`Re-run ${TITLES[module]} review with current parsed table`}
          >
            <RotateCcw size={14} aria-hidden="true" />
            Re-run {TITLES[module]} Review
          </button>
        </div>
      ) : (
        <button
          type="button"
          className="button button-primary mt-4"
          disabled={loading || !supported}
          onClick={() => void run()}
        >
          {loading ? (
            <>
              <span className="button-spinner" aria-hidden="true" />
              Generating review…
            </>
          ) : (
            <>
              {ACTIONS[module]}
              <ArrowRight size={16} aria-hidden="true" />
            </>
          )}
        </button>
      )}
      {!supported && <p role="alert" className="mt-3 text-sm text-notice-ink">A supported table with parsed measurement positions is required. Check the input and parse again.</p>}
      {loading && <p role="status" className="mt-3 text-sm text-muted">Preparing factual observations and report wording…</p>}
      {error && <p ref={errorHeading} tabIndex={-1} role="alert" className="mt-3 text-sm text-notice-ink">{error}</p>}
      {report && <article aria-label="Generated synthetic report" className="motion-enter mt-6 rounded-xl border border-line bg-white p-5 sm:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div><p className="text-xs font-semibold uppercase tracking-wider text-brand">{module} · Generated results</p><h4 ref={heading} tabIndex={-1} className="mt-2 text-xl font-semibold">{TITLES[module]} report</h4></div>
          <div className="flex flex-wrap items-center gap-2" role="group" aria-label="Export generated report">
            <button type="button" className="button button-secondary" onClick={() => void copy()}><Copy size={15} aria-hidden="true" />Copy</button>
            <button type="button" className="button button-secondary" onClick={download}><Download size={15} aria-hidden="true" />Export TXT</button>
            <PdfExportButton kind="interactive" data={report} reportId={report.report_id} />
            {notice && <p role="status" className="w-full text-xs text-muted">{notice}</p>}
          </div>
        </div>
        <p role="status" className="mt-4 text-sm text-brand"><span>{report.generation.used_mode === 'GROQ_AI' ? 'AI-assisted wording' : 'Standard wording'}</span>{report.generation.used_mode !== 'GROQ_AI' && <span className="text-muted"> · AI-assisted wording unavailable.</span>}</p>
        <p className="mt-3 text-sm leading-7">{report.summary}</p>
        {report.functional_plan && <FunctionalResults report={report} />}
        {report.parsed.status === 'PARTIAL' && (
          <div className="mt-3 rounded-lg border border-notice-line bg-notice/40 p-3.5 text-xs leading-6 text-notice-ink">
            <span className="font-semibold text-ink">Parse status note: </span>
            {partialParseExplanation(report.parsed)}
          </div>
        )}
        {!!report.sections?.length && <section aria-label="Module review comments" className="mt-6 space-y-4">
          <h5 className="text-base font-semibold">{module === 'macro' ? 'Planning comments' : module === 'micro' ? 'Attachment review comments' : 'Sequencing review comments'}</h5>
          {presentation?.sections.filter(section => !(report.functional_plan && (section.section_id === 'ATTACHMENT_OPTIONS' || section.section_id === 'PHASES' && (report.functional_plan.stages.length > 0 || (report.functional_plan.review_outline?.length ?? 0) > 0)))).map(section => <div key={section.section_id} className="comment-card">
            <div className="flex flex-wrap items-center justify-between gap-2"><h6 className="text-base font-semibold">{section.title}</h6>{report.planning_context?.origin !== 'INPUT_DRIVEN_POLICY_REVIEW' && <span className="rounded-md bg-canvas px-2 py-1 text-xs text-muted">{sectionStatusLabel(section)}</span>}</div>
            <div className="mt-3 space-y-3 text-sm leading-7 [overflow-wrap:anywhere]">{commentParagraphs(section.text).map((paragraph, index) => <p key={index} className="whitespace-pre-wrap">{paragraph}</p>)}</div>
            {!!section.missing_fields.length && <p className="mt-3 text-xs leading-6 text-notice-ink"><strong>Information needed:</strong> {section.missing_fields.join('; ')}.</p>}
          </div>)}
        </section>}
        {report.sections?.length ? (!!sourceRows.length && <details className="mt-5 text-sm text-muted"><summary className="cursor-pointer font-medium">Source movement values</summary><ul className="mt-3 space-y-3">{sourceRows.map(o => <li key={o.tooth_ref}><strong>Tooth {o.original_tooth.trim()}</strong><ul className="mt-1 text-xs leading-6">{o.measurements.map(m => <li key={m.id}>{m.raw_label.trim()}: {m.raw_value ?? 'Missing'}</li>)}</ul></li>)}</ul></details>) : <section aria-label="Factual tooth-wise observations" className="mt-6">
          <h5 className="text-base font-semibold">{module === 'macro' ? 'Planning comments' : module === 'micro' ? 'Attachment review comments' : 'Sequencing review comments'}</h5>
          <p className="mt-1 text-xs leading-6 text-muted">Programmed movements only. Missing values remain unknown; direction labels are preserved as supplied.</p>
          <ul className="mt-4 space-y-3">{report.observations.map(o => <li key={o.tooth_ref} className="comment-card">
            <h6 className="font-semibold">Tooth {o.original_tooth.trim()}</h6><p className="mt-2 whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{o.text}</p>
            {!!o.measurements.length && <details className="mt-3 text-xs leading-6 text-muted"><summary className="cursor-pointer font-medium">Source values</summary><ul className="mt-2 space-y-1">{o.measurements.map(m => <li key={m.id}>{m.raw_label.trim()}: {m.raw_value ?? 'Missing'}</li>)}</ul></details>}
          </li>)}</ul>
        </section>}
        {report.planning_context?.origin === 'INPUT_DRIVEN_POLICY_REVIEW' ? <p className="mt-5 text-xs leading-6 text-muted">Source conventions and anatomy remain unverified. Complete exports retain exact source values, policy references and optional inputs.</p> : presentation?.scope ? <aside aria-label="Report scope" className="mt-5 border-t border-line pt-4 text-xs leading-6 text-muted"><strong className="font-semibold">Report scope. </strong>{presentation.scope} Source conventions and anatomy remain unverified. Complete exports retain source values and provenance.</aside>
          : <p className="mt-5 text-xs leading-6 text-muted">Source conventions and anatomy remain unverified. No clinical suitability, attachment indication, stage schedule or anchorage prescription is established. Complete exports retain source values and provenance.</p>}
      </article>}
    </div>
  </section>
}
