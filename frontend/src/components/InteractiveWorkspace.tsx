import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Check, Copy, Download, FileCheck2, RotateCcw } from 'lucide-react'
import { requestInteractiveReview } from '../api/interactive'
import type { DemoModule, InteractiveReport } from '../api/interactive'
import type { AutomaticParseResult, ContextClaims, ParseResult } from '../api/parse'
import PdfExportButton from './PdfExportButton'

const TITLES = { macro: 'Planning', micro: 'Attachment', nano: 'Sequencing' }
const ACTIONS = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }

function partialParseExplanation(parsed: ParseResult): string {
  const missingCount = parsed.coverage.missing
  const missingLabels = [...new Set(parsed.measurements.filter(m => m.numeric_status === 'MISSING' || m.numeric_status === 'NOT_PRESENT').map(m => m.raw_label.trim()))]
  const unrecognizedLabels = [...new Set(parsed.measurements.filter(m => !m.recognized_label).map(m => m.raw_label.trim()))]

  if (missingCount > 0 && unrecognizedLabels.length === 0) {
    const cols = missingLabels.length > 0 ? ` in ${missingLabels.slice(0, 3).join(', ')}${missingLabels.length > 3 ? '…' : ''}` : ''
    return `All available movement values were parsed successfully. Marked as partial because ${missingCount} cell${missingCount === 1 ? ' contains an' : 's contain'} omitted or missing value (e.g. "—")${cols}. Rather than guessing or assuming missing values are zero, Finova retains them as unknown.`
  }

  if (unrecognizedLabels.length > 0 && missingCount === 0) {
    return `All recognized movement values were parsed successfully. Marked as partial because ${unrecognizedLabels.length === 1 ? 'a column heading was' : 'some column headings were'} unrecognized (${unrecognizedLabels.join(', ')}).`
  }

  if (missingCount > 0 && unrecognizedLabels.length > 0) {
    return `All available movement values were parsed successfully. Marked as partial because ${missingCount} cell${missingCount === 1 ? ' has a' : 's have'} missing value and some headings were unrecognized (${unrecognizedLabels.join(', ')}). Missing values are retained as unknown.`
  }

  return 'All available movement values were parsed successfully. Omitted or unassigned cells are preserved as unknown rather than assumed to be zero.'
}

export default function InteractiveWorkspace({ module, rawText, context, parsed, onComplete }: {
  module: DemoModule; rawText: string; context: ContextClaims; parsed: AutomaticParseResult; onComplete: (complete: boolean) => void
}) {
  const [report, setReport] = useState<InteractiveReport | null>(null)
  const [loading, setLoading] = useState(false), [error, setError] = useState(''), [notice, setNotice] = useState('')
  const revision = useRef(0), pending = useRef<AbortController | null>(null), heading = useRef<HTMLHeadingElement>(null)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (report) { heading.current?.focus(); heading.current?.scrollIntoView?.({ block: 'start', behavior: 'instant' }) } }, [report])
  const supported = !['INVALID', 'UNSUPPORTED'].includes(parsed.status) && parsed.measurements.length > 0
  async function run() {
    if (pending.current || !supported) return
    const current = ++revision.current, controller = new AbortController()
    pending.current = controller; setLoading(true); setError(''); setNotice(''); setReport(null); onComplete(false)
    const timer = window.setTimeout(() => controller.abort(), 55_000)
    try {
      const result = await requestInteractiveReview(module, rawText, context, parsed.raw_sha256, parsed.pipeline.recovery_receipt, controller.signal)
      if (revision.current === current) { setReport(result); onComplete(true) }
    } catch (e) {
      if (revision.current !== current) return
      setError(e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'The input changed or parsing evidence expired. Parse Table again, then retry.'
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
      <p className="text-sm leading-7 text-muted">{module === 'macro' ? 'Prepare readable planning comments from the programmed movements in your table.' : module === 'micro' ? 'Prepare attachment-review comments from the recorded movements. Attachment choices and placement require separate supporting evidence.' : 'Prepare sequencing-review comments from the recorded movements. Stage order and anchorage require separate supporting evidence.'}</p>
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
      {error && <p role="alert" className="mt-3 text-sm text-notice-ink">{error}</p>}
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
        {report.parsed.status === 'PARTIAL' && (
          <div className="mt-3 rounded-lg border border-notice-line bg-notice/40 p-3.5 text-xs leading-6 text-notice-ink">
            <span className="font-semibold text-ink">Parse status note: </span>
            {partialParseExplanation(report.parsed)}
          </div>
        )}
        <section aria-label="Factual tooth-wise observations" className="mt-6">
          <h5 className="text-base font-semibold">{module === 'macro' ? 'Planning comments' : module === 'micro' ? 'Attachment review comments' : 'Sequencing review comments'}</h5>
          <p className="mt-1 text-xs leading-6 text-muted">Programmed movements only. Missing values remain unknown; direction labels are preserved as supplied.</p>
          <ul className="mt-4 space-y-3">{report.observations.map(o => <li key={o.tooth_ref} className="comment-card">
            <h6 className="font-semibold">Tooth token {o.original_tooth}</h6><p className="mt-2 whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{o.text}</p>
            <details className="mt-3 text-xs leading-6 text-muted"><summary className="cursor-pointer font-medium">Source values</summary><ul className="mt-2 space-y-1">{o.measurements.map(m => <li key={m.id}>{m.raw_label.trim()}: {m.raw_value ?? 'Missing'}</li>)}</ul></details>
          </li>)}</ul>
        </section>
        {!!report.illustrations.length && <section aria-label="Illustrative demo content" className="mt-6 rounded-xl border border-line bg-canvas p-4">
          <h5 className="font-semibold">{module === 'micro' ? 'Illustrative attachment examples' : 'Illustrative sequencing examples'}</h5>
          <p className="mt-2 text-sm leading-6 text-notice-ink">Simulated examples · not calculated findings or treatment recommendations.</p>
          <ul className="mt-4 space-y-4">{report.illustrations.map(i => <li key={i.tooth_ref} className="text-sm leading-7 [overflow-wrap:anywhere]"><strong>Tooth token {i.original_tooth}</strong><p>{i.text}</p></li>)}</ul>
        </section>}
        <p className="mt-5 text-xs leading-6 text-muted">Source conventions and anatomy remain unverified. No clinical suitability, attachment indication, stage schedule or anchorage prescription is established. Complete exports retain source values and provenance.</p>
      </article>}
    </div>
  </section>
}
