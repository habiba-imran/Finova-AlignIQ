import { useState } from 'react'
import type { ParseResult } from '../api/parse'

const titles = { PARSED_UNVERIFIED: 'Structure parsed · semantics unverified', PARTIAL: 'Partial lexical parse', UNSUPPORTED: 'Unsupported layout', INVALID: 'Invalid structure' }
const humanize = (value: string) => value.replaceAll('_', ' ').toLowerCase()
const PAGE_SIZE = 25

export default function ParseResults({ result }: { result: ParseResult }) {
  const [page, setPage] = useState(0)
  const [issueLimit, setIssueLimit] = useState(50)
  const teeth = new Map(result.teeth.map(tooth => [tooth.id, tooth]))
  const visible = result.measurements.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)
  return <section aria-labelledby="structured-heading" className="panel mt-6">
    <div className="panel-heading flex-wrap py-4"><h2 id="structured-heading" className="font-semibold">Structured lexical preview</h2><span className="text-xs text-muted">{titles[result.status]}</span></div>
    <div className="p-5 sm:p-6">
      <div className="rounded-lg border border-notice-line bg-notice p-4 text-sm leading-6 text-notice-ink">
        <p className="font-semibold">Source verification: UNVERIFIED</p>
        <p>Source claim: {result.source.source_claim}. Parser: {result.source.adapter.id} v{result.source.adapter.version}.</p>
        {result.source.candidate_adapter && <p>Candidate: {result.source.candidate_adapter.id} v{result.source.candidate_adapter.version}. No vendor versions are verified.</p>}
        {result.source.detected_claims.length > 0 && <p>Explicit source text claims: {result.source.detected_claims.join(', ')}.</p>}
        <p>Canonical tooth IDs, axes, and physical directions are withheld. These are text parsing results, not clinical checks.</p>
      </div>
      <p className="my-4 text-sm leading-6 text-muted">{result.teeth.length} tooth token positions · {result.measurements.length} measurement positions · {result.coverage.explicit_zero} explicit zeros · {result.coverage.missing} missing positions</p>
      <p className="mb-4 text-xs text-muted">Layout: {humanize(result.layout.orientation)} · Delimiter: {result.layout.delimiter ? humanize(result.layout.delimiter) : 'unresolved'}</p>
      {result.measurements.length > 0 ? <>
        <div role="region" aria-label="Parsed measurements" tabIndex={0} className="overflow-x-auto rounded-lg border border-line">
          <table className="w-full min-w-[850px] text-left text-xs leading-5">
            <caption className="sr-only">Original tokens alongside lexical values. All source semantics remain unverified.</caption>
            <thead className="bg-canvas text-muted"><tr>{['Tooth token', 'Label / lexical alias', 'Raw cell', 'Lexical value / unit', 'Status / clarification'].map(title => <th key={title} scope="col" className="p-3 font-semibold">{title}</th>)}</tr></thead>
            <tbody>{visible.map(measurement => <tr key={measurement.id} className="border-t border-line align-top">
              <td className="p-3"><code className="raw-text">{teeth.get(measurement.tooth_ref)?.raw_identifier}</code><p className="mt-1 text-muted">{humanize(teeth.get(measurement.tooth_ref)?.identifier_status ?? 'UNKNOWN')}</p></td>
              <td className="max-w-52 p-3"><span className="raw-text">{measurement.raw_label}</span><p className="mt-1 text-muted">{measurement.recognized_label ? humanize(measurement.recognized_label) : 'Unsupported label'}</p></td>
              <td className="max-w-56 p-3"><code className="raw-text">{measurement.raw_value === null ? '(omitted cell)' : measurement.raw_value === '' ? '(empty cell)' : measurement.raw_value}</code><p className="mt-1 text-muted">{measurement.span ? `Line ${measurement.span.line}, column ${measurement.span.column_start}` : 'No cell supplied'}</p></td>
              <td className="p-3"><code>{measurement.signed_decimal ?? 'Not accepted'}</code> {measurement.unit ?? '(unit unresolved)'}<p className="mt-1 text-muted">Magnitude: {measurement.magnitude_decimal ?? '—'}</p><p className="text-muted">Literal direction: {measurement.raw_direction ?? 'not supplied'} (unverified)</p></td>
              <td className="max-w-56 p-3"><p className="font-medium">{humanize(measurement.numeric_status)}</p><p>{humanize(measurement.field_status)}</p><p className="mt-1 text-muted">{measurement.clarification_fields.map(humanize).join(', ')}</p></td>
            </tr>)}</tbody>
          </table>
        </div>
        <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-xs text-muted"><p>Showing {page * PAGE_SIZE + 1}–{Math.min((page + 1) * PAGE_SIZE, result.measurements.length)} of {result.measurements.length} positions</p>{result.measurements.length > PAGE_SIZE && <div className="flex gap-2"><button type="button" className="button button-clear" disabled={page === 0} onClick={() => setPage(page - 1)}>Previous measurements</button><button type="button" className="button button-clear" disabled={(page + 1) * PAGE_SIZE >= result.measurements.length} onClick={() => setPage(page + 1)}>Next measurements</button></div>}</div>
      </> : <p className="rounded-lg bg-canvas p-4 text-sm">No measurement cells could be assigned. Review the issues and retain the original text for clarification.</p>}
      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div><h3 className="mb-3 text-sm font-semibold">Parsing warnings and errors</h3><p className="mb-3 text-xs text-muted">{result.issues.length} issues. Severity describes parsing, not clinical risk.</p><ul className="max-h-80 space-y-3 overflow-auto text-xs leading-5">{result.issues.slice(0, issueLimit).map((issue, index) => <li key={`${issue.code}-${index}`} className="rounded-lg border border-line p-3"><p className="font-semibold">{issue.severity} · {issue.code}</p><p className="mt-1 text-muted">{issue.message}</p>{issue.span && <p className="text-muted">Line {issue.span.line}, column {issue.span.column_start}</p>}</li>)}</ul>{result.issues.length > issueLimit && <button type="button" className="button button-clear mt-3" onClick={() => setIssueLimit(issueLimit + 50)}>Show more issues ({result.issues.length - issueLimit} remaining)</button>}</div>
        <div><h3 className="mb-3 text-sm font-semibold">Fields requiring clarification or verification</h3><ul className="space-y-2 text-xs text-muted">{result.clarification_fields.map(field => <li key={field}>• {humanize(field)}</li>)}</ul><p className="mt-4 text-xs leading-5 text-muted">Metadata claims alone do not clear source verification. Omitted axes are not assumed to be zero.</p></div>
      </div>
      <details className="mt-6 rounded-lg border border-line p-4"><summary className="cursor-pointer text-sm font-medium">Full structured response (JSON, in memory)</summary><pre tabIndex={0} aria-label="Full parsing JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs leading-5">{JSON.stringify(result, null, 2)}</pre></details>
    </div>
  </section>
}
