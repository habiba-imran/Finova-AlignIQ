import { AlertTriangle, ScanLine } from 'lucide-react'
import type { AutomaticParseResult } from '../api/parse'

const humanize = (value: string) => value.replaceAll('_', ' ').toLowerCase()

export default function ParserStatus({ result }: { result: AutomaticParseResult }) {
  const { detection, assistance, clarifications } = result.pipeline
  const classification = result.pipeline.quality?.classification
  const status = assistance.status === 'ACCEPTED' ? (result.status === 'PARTIAL' ? 'AI-assisted structure recovery · partially parsed' : 'AI-assisted structure recovery')
    : classification === 'NOT_TMT' ? 'Unsupported input · not a TMT'
      : classification === 'AMBIGUOUS_STRUCTURE' ? 'Needs clarification'
        : result.measurements.length ? (result.status === 'PARTIAL' ? 'Partially parsed' : 'Parsed successfully') : 'Unsupported input'
  const errors = result.issues.filter(issue => issue.severity === 'ERROR')
  const attentionCount = result.issues.filter(issue => issue.severity !== 'INFO').length
  const structureState = result.status === 'PARSED_UNVERIFIED' ? 'Structure recognized'
    : result.status === 'PARTIAL' ? 'Structure partially recognized'
      : result.status === 'UNSUPPORTED' ? 'Structure not recognized'
        : 'Structure invalid'
  const metrics = [
    { label: 'Tooth token positions', value: result.teeth.length, detail: 'Original identifiers retained' },
    { label: 'Movement positions', value: result.measurements.length, detail: 'Lexical cells assigned' },
    { label: 'Missing values', value: result.coverage.missing, detail: 'Never treated as zero' },
    { label: 'Explicit zeros', value: result.coverage.explicit_zero, detail: 'Declared zero values only' },
    { label: 'Issues requiring attention', value: attentionCount, detail: `${result.issues.length} total parse issues` },
    { label: 'Clarification fields', value: result.clarification_fields.length, detail: 'Field types still unresolved' },
  ]

  return <section aria-label="Automatic detection and clarification" className="panel">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><ScanLine size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 className="panel-title">Input assessment</h3></div>
      <span className="report-badge">Structural parse only</span>
    </div>
    <div className="p-5 sm:p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted">Parse outcome</p>
          <p className="mt-1 text-xl font-semibold tracking-[-0.02em]">{status}</p>
          <p className="mt-2 text-sm leading-6">Detected source: {detection.detected_source} · {detection.status.replaceAll('_', ' ')}</p>
          <p className="text-sm leading-6 text-muted">Verified source: UNKNOWN. Recognized structure does not prove vendor compatibility.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="report-badge report-badge-notice">Source UNVERIFIED</span>
          <span className="report-badge">Not a clinical check</span>
        </div>
      </div>
      <p className="mt-3 text-xs leading-5 text-muted">{structureState}. Table structure and lexical values are presented separately from vendor semantics and clinical eligibility.</p>

      <dl aria-label="Parse summary" className="summary-grid mt-5">
        {metrics.map(metric => <div key={metric.label} className="summary-metric">
          <dt className="summary-label">{metric.label}</dt>
          <dd className="summary-value">{metric.value}</dd>
          <dd className="summary-detail">{metric.detail}</dd>
        </div>)}
      </dl>

      {errors.length > 0 && <section aria-label="Blocking parse issues" className="mt-5 rounded-xl border border-danger-line bg-danger-soft p-4 text-sm leading-6 text-danger">
        <div className="flex items-start gap-2">
          <AlertTriangle size={17} className="mt-0.5 shrink-0" aria-hidden="true" />
          <div className="min-w-0">
            <p className="font-semibold">{errors.length} parse {errors.length === 1 ? 'error blocks' : 'errors block'} a complete structural result.</p>
            <ul className="mt-2 space-y-2">{errors.slice(0, 3).map((issue, index) => <li key={`${issue.code}-${index}`}><span className="font-semibold">{issue.severity} · {issue.code}</span> — {issue.message}{issue.span && <span className="text-danger/80"> Line {issue.span.line}, column {issue.span.column_start}.</span>}</li>)}</ul>
            {errors.length > 3 && <p className="mt-2 text-xs">The remaining errors are listed with all parser issues below.</p>}
          </div>
        </div>
      </section>}

      <p className="mt-4 text-xs leading-5 text-muted">Numbering syntax candidates: {detection.notation_candidates.join(', ') || 'unknown'}. No numbering system or vendor conventions were selected.</p>
      {assistance.origin === 'GROQ_PROPOSAL_CERTIFIED' && <p className="mt-2 text-xs leading-5 text-muted">Recovered original-text associations are rechecked by draft reviews and reports. Source semantics remain unverified.</p>}

      <details className="mt-4 rounded-lg border border-line bg-canvas p-3 text-xs leading-6 text-muted">
        <summary className="cursor-pointer font-medium text-ink">Parsing details</summary>
        <div className="mt-2 space-y-1">
          <p>Structure state: {humanize(result.status)} · layout recognized: {detection.layout_recognized ? 'yes' : 'no'}.</p>
          <p>Structural assistance: {assistance.status} · {assistance.reason}. Provider attempts: {assistance.attempts}.</p>
          <p>Parser: {result.source.adapter.id} v{result.source.adapter.version}. Verified source remains unknown.</p>
        </div>
      </details>
      <details className="mt-2 rounded-lg border border-line bg-canvas p-3 text-xs leading-6 text-muted">
        <summary className="cursor-pointer font-medium text-ink">Targeted clarification requirements ({clarifications.length})</summary>
        {clarifications.length > 0 ? <ul className="mt-3 max-h-80 space-y-3 overflow-auto">{clarifications.map((clarification, index) => <li key={`${clarification.code}-${index}`}><strong>{clarification.code} · {clarification.field}</strong><p>{clarification.message}</p>{clarification.measurement_ids.length > 0 && <p>Positions: {clarification.measurement_ids.join(', ')}</p>}</li>)}</ul>
          : <p className="mt-2">No targeted clarification requirements were returned for this response.</p>}
      </details>
    </div>
  </section>
}
