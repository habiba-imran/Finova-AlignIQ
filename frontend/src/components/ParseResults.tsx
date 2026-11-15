import { useState } from 'react'
import { Braces, ChevronDown } from 'lucide-react'
import type { Measurement, ParseResult } from '../api/parse'
import { missingValuesParseLabel } from '../api/parse'

const titles = { PARSED_UNVERIFIED: 'Structure parsed · semantics unverified', PARTIAL: 'Partial lexical parse', UNSUPPORTED: 'Unsupported layout', INVALID: 'Invalid structure' }
const humanize = (value: string) => value.replaceAll('_', ' ').toLowerCase()
const PAGE_SIZE = 25

function rawCell(measurement: Measurement) {
  if (measurement.raw_value === null) return '(omitted cell)'
  if (measurement.raw_value === '') return '(empty cell)'
  return measurement.raw_value
}

function numericTone(status: string) {
  if (status === 'EXPLICIT_ZERO') return 'report-badge-brand'
  if (status === 'MISSING' || status === 'INVALID' || status === 'UNSUPPORTED') return 'report-badge-notice'
  return ''
}

export default function ParseResults({ result }: { result: ParseResult }) {
  const [page, setPage] = useState(0)
  const [issueLimit, setIssueLimit] = useState(50)
  const teeth = new Map(result.teeth.map(tooth => [tooth.id, tooth]))
  const visible = result.measurements.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)
  const errors = result.issues.filter(issue => issue.severity === 'ERROR').length
  const warnings = result.issues.filter(issue => issue.severity === 'WARNING').length
  const information = result.issues.filter(issue => issue.severity === 'INFO').length

  return <section aria-labelledby="structured-heading" className="panel motion-enter mt-4">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><Braces size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="structured-heading" className="panel-title">Structured lexical preview</h3></div>
      <span className="report-badge">{missingValuesParseLabel(result) ?? titles[result.status]}</span>
    </div>
    <div className="p-5 sm:p-6">
      <div className="rounded-xl border border-notice-line bg-notice p-4 text-sm leading-6 text-notice-ink">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="font-semibold">Source verification: UNVERIFIED</p>
            <p>Source claim: {result.source.source_claim}. No vendor versions are verified.</p>
          </div>
          <span className="report-badge report-badge-notice">Lexical values only</span>
        </div>
        <p className="mt-2">Canonical tooth IDs, axes, and physical directions are withheld. These are text parsing results, not clinical checks.</p>
        <details className="mt-3 rounded-lg border border-notice-line/70 bg-white/60 p-3 text-xs leading-6">
          <summary className="cursor-pointer font-medium">Source evidence & parser metadata</summary>
          <div className="mt-2 space-y-1">
            <p>Parser: {result.source.adapter.id} v{result.source.adapter.version}. Verified source: UNKNOWN.</p>
            {result.source.candidate_adapter && <p>Candidate adapter: {result.source.candidate_adapter.id} v{result.source.candidate_adapter.version}. Not selected or verified.</p>}
            {result.source.detected_claims.length > 0 && <p>Explicit source text claims: {result.source.detected_claims.join(', ')}.</p>}
            <p>Layout: {humanize(result.layout.orientation)} · delimiter: {result.layout.delimiter ? humanize(result.layout.delimiter) : 'unresolved'}.</p>
            <p className="raw-text">Input SHA-256: {result.raw_sha256}</p>
          </div>
        </details>
      </div>

      {result.measurements.length > 0 ? <>
        <div className="mt-5 flex flex-wrap items-end justify-between gap-3">
          <div>
            <h4 className="text-[15px] font-semibold">Parsed movements</h4>
            <p className="mt-0.5 text-xs leading-5 text-muted">Original cells beside accepted lexical values. Missing, empty and explicit-zero cells remain distinct.</p>
          </div>
          <div className="flex flex-wrap gap-2 text-xs text-muted">
            <span className="report-badge">Lexical parse</span>
            <span className="report-badge">Semantics unverified</span>
          </div>
        </div>
        <div role="region" aria-label="Parsed measurements" tabIndex={0} className="movement-scroll mt-3">
          <table className="movement-table">
            <caption className="sr-only">Original tokens alongside lexical values. All source semantics remain unverified, and missing values are not zero.</caption>
            <thead><tr>
              <th scope="col">Tooth token</th>
              <th scope="col">Movement label</th>
              <th scope="col">Source cell</th>
              <th scope="col" className="text-right">Lexical value & unit</th>
              <th scope="col">Parse status</th>
              <th scope="col">Details</th>
            </tr></thead>
            <tbody>{visible.map(measurement => {
              const tooth = teeth.get(measurement.tooth_ref)
              return <tr key={measurement.id}>
                <th scope="row" className="p-3 text-left align-top font-normal">
                  <code className="raw-text text-[13px] font-semibold text-ink">{tooth?.raw_identifier ?? 'Unresolved token'}</code>
                  <p className="mt-1 text-xs text-muted">{humanize(tooth?.identifier_status ?? 'UNKNOWN')}</p>
                </th>
                <td className="max-w-52">
                  <span className="raw-text text-[13px] text-ink">{measurement.raw_label}</span>
                  <p className="mt-1 text-xs text-muted">{measurement.recognized_label ? humanize(measurement.recognized_label) : 'Unsupported label'}</p>
                </td>
                <td className="max-w-56">
                  <code className="raw-text text-[13px] text-ink">{rawCell(measurement)}</code>
                  <p className="mt-1 text-xs text-muted">{measurement.span ? `Line ${measurement.span.line}, column ${measurement.span.column_start}` : 'No cell supplied'}</p>
                </td>
                <td className="text-right">
                  <code className="movement-value">{measurement.signed_decimal ?? 'Not accepted'}</code>
                  <span className="ml-1.5 inline-block text-xs text-muted">{measurement.unit ?? '(unit unresolved)'}</span>
                  <p className="mt-1 text-xs text-muted movement-number">Magnitude: {measurement.magnitude_decimal ?? '—'}</p>
                </td>
                <td className="max-w-56">
                  <span className={`report-badge ${numericTone(measurement.numeric_status)}`}>{humanize(measurement.numeric_status)}</span>
                  <p className="mt-1.5 text-xs text-muted">{humanize(measurement.field_status)}</p>
                </td>
                <td className="max-w-56">
                  <details className="rounded-lg border border-line bg-canvas p-2.5 text-xs leading-5 text-muted">
                    <summary className="flex cursor-pointer items-center gap-1 font-medium text-ink">Row details <ChevronDown size={13} aria-hidden="true" /></summary>
                    <div className="mt-2 space-y-1">
                      <p>Literal direction: {measurement.raw_direction ?? 'not supplied'} (unverified).</p>
                      <p>Semantic verification: NOT VERIFIED.</p>
                      <p>Clarification fields: {measurement.clarification_fields.length ? measurement.clarification_fields.map(humanize).join(', ') : 'None'}</p>
                      <p className="raw-text">Measurement: {measurement.id}</p>
                    </div>
                  </details>
                </td>
              </tr>
            })}</tbody>
          </table>
        </div>
        <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-xs text-muted">
          <p>Showing {page * PAGE_SIZE + 1}–{Math.min((page + 1) * PAGE_SIZE, result.measurements.length)} of {result.measurements.length} positions</p>
          {result.measurements.length > PAGE_SIZE && <div className="flex gap-2"><button type="button" className="button button-clear" disabled={page === 0} onClick={() => setPage(page - 1)}>Previous measurements</button><button type="button" className="button button-clear" disabled={(page + 1) * PAGE_SIZE >= result.measurements.length} onClick={() => setPage(page + 1)}>Next measurements</button></div>}
        </div>
      </> : <p className="mt-5 rounded-xl bg-canvas p-4 text-sm">No measurement cells could be assigned. Review the issues and retain the original text for clarification.</p>}

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <section aria-labelledby="warnings-heading" className="diagnostic-panel">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 id="warnings-heading" className="text-sm font-semibold">Parsing warnings and errors</h3>
            <span className="report-badge">{result.issues.length} issues</span>
          </div>
          <p className="mt-2 text-xs leading-5 text-muted">{errors} errors · {warnings} warnings · {information} informational. Severity describes parsing, not clinical risk.</p>
          {result.issues.length > 0 ? <details className="diagnostic-disclosure">
            <summary>Review all parser issues ({result.issues.length})</summary>
            <ul className="diagnostic-list">{result.issues.slice(0, issueLimit).map((issue, index) => <li key={`${issue.code}-${index}`} className="rounded-lg border border-line bg-white p-3">
              <p className="font-semibold">{issue.severity} · {issue.code}</p>
              <p className="mt-1 text-muted">{issue.message}</p>
              {issue.span && <p className="text-muted">Line {issue.span.line}, column {issue.span.column_start}</p>}
            </li>)}</ul>
            {result.issues.length > issueLimit && <button type="button" className="button button-clear mt-3" onClick={() => setIssueLimit(issueLimit + 50)}>Show more issues ({result.issues.length - issueLimit} remaining)</button>}
          </details> : <p className="mt-3 rounded-lg border border-line bg-white p-3 text-xs text-muted">No parser issues were returned for this response.</p>}
        </section>

        <section aria-labelledby="clarification-heading" className="diagnostic-panel">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 id="clarification-heading" className="text-sm font-semibold">Fields requiring clarification or verification</h3>
            <span className="report-badge">{result.clarification_fields.length} fields</span>
          </div>
          {result.clarification_fields.length > 0 ? <>
            <p className="mt-2 text-xs leading-5 text-muted">{result.clarification_fields.length} field types remain unresolved in the lexical preview.</p>
            <details className="diagnostic-disclosure">
              <summary>Review unresolved fields ({result.clarification_fields.length})</summary>
              <ul className="mt-3 space-y-2 text-xs text-muted">{result.clarification_fields.map(field => <li key={field}>• {humanize(field)}</li>)}</ul>
            </details>
          </> : <p className="mt-2 text-xs leading-5 text-muted">No field-level clarification flags were returned. This does not verify the source semantics.</p>}
          <p className="mt-4 text-xs leading-5 text-muted">Metadata claims alone do not clear source verification. Omitted axes are not assumed to be zero.</p>
        </section>
      </div>

      <details className="technical-details"><summary>Full structured response (JSON, in memory)</summary><pre tabIndex={0} aria-label="Full parsing JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs leading-5">{JSON.stringify(result, null, 2)}</pre></details>
    </div>
  </section>
}
