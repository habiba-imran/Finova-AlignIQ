import type { AutomaticParseResult } from '../api/parse'

export default function ParserStatus({ result }: { result: AutomaticParseResult }) {
  const { detection, assistance, clarifications } = result.pipeline
  const classification = result.pipeline.quality?.classification
  const status = assistance.status === 'ACCEPTED' ? (result.status === 'PARTIAL' ? 'AI-assisted structure recovery · partially parsed' : 'AI-assisted structure recovery')
    : classification === 'NOT_TMT' ? 'Unsupported input · not a TMT'
      : classification === 'AMBIGUOUS_STRUCTURE' ? 'Needs clarification'
        : result.measurements.length ? (result.status === 'PARTIAL' ? 'Partially parsed' : 'Parsed successfully') : 'Unsupported input'
  return <section aria-label="Automatic detection and clarification" className="panel mt-6 p-5 text-sm leading-6 sm:p-6">
    <h2 className="font-semibold">Automatic detection</h2>
    <p className="my-2 font-medium">{status}</p>
    <p>Detected source: {detection.detected_source} · {detection.status.replaceAll('_', ' ')}</p>
    <p>Verified source: UNKNOWN. Recognized structure does not prove vendor compatibility.</p>
    <p className="text-muted">Numbering syntax candidates: {detection.notation_candidates.join(', ') || 'unknown'}. No numbering system or vendor conventions were selected.</p>
    {assistance.origin === 'GROQ_PROPOSAL_CERTIFIED' && <p className="mt-2 text-muted">Recovered original-text associations are rechecked by draft reviews and reports. Source semantics remain unverified.</p>}
    <details className="mt-2 text-xs text-muted"><summary className="cursor-pointer">Parsing details</summary><p>Structural assistance: {assistance.status} · {assistance.reason}. Provider attempts: {assistance.attempts}.</p></details>
    <details className="mt-3"><summary className="cursor-pointer font-medium">Targeted clarification requirements ({clarifications.length})</summary>
      <ul className="mt-3 max-h-80 space-y-3 overflow-auto text-xs">{clarifications.map((c, i) => <li key={`${c.code}-${i}`}><strong>{c.code} · {c.field}</strong><p>{c.message}</p>{c.measurement_ids.length > 0 && <p className="text-muted">Positions: {c.measurement_ids.join(', ')}</p>}</li>)}</ul>
    </details>
  </section>
}
