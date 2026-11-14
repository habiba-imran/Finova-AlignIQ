import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Copy, Download, FileCheck2 } from 'lucide-react'
import { requestInteractiveReview } from '../api/interactive'
import type { DemoModule, InteractiveReport } from '../api/interactive'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import PdfExportButton from './PdfExportButton'

const TITLES = { macro: 'Planning', micro: 'Attachment', nano: 'Sequencing' }
const ACTIONS = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }

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
    const timer = window.setTimeout(() => controller.abort(), 30_000)
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
      <p className="text-sm leading-7 text-muted">Generate tooth-wise observations from your synthetic table.{module !== 'macro' && ' Examples are illustrative simulations; treatment decisions cannot be derived from these values.'} AI wording is used automatically when available.</p>
      <button type="button" className="button button-primary mt-4" disabled={loading || !supported} onClick={() => void run()}>{loading ? <><span className="button-spinner" aria-hidden="true" />Generating review…</> : <>{ACTIONS[module]}<ArrowRight size={16} aria-hidden="true" /></>}</button>
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
        <p role="status" className="mt-4 text-sm text-brand">{report.wording_notice}</p>
        <p className="mt-3 text-sm leading-7">{report.summary}</p>
        {report.parsed.status === 'PARTIAL' && <p className="mt-3 text-sm text-notice-ink">Partial parse: unresolved content has not been interpreted. Review the marked table.</p>}
        <section aria-label="Factual tooth-wise observations" className="mt-6">
          <h5 className="text-base font-semibold">Factual observations</h5>
          <p className="mt-1 text-xs leading-6 text-muted">Parsed source values only. Missing values remain unknown; direction labels are preserved as supplied.</p>
          <ul className="mt-4 space-y-3">{report.observations.map(o => <li key={o.tooth_ref} className="comment-card">
            <h6 className="font-semibold">Tooth token {o.original_tooth}</h6><p className="mt-2 whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{o.text}</p>
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
