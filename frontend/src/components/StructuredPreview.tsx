import { Table2 } from 'lucide-react'
import type { Measurement, ParseResult } from '../api/parse'

const humanize = (value: string) => value.replaceAll('_', ' ').toLowerCase()

type Column = {
  key: string
  label: string
  unit: string | null
  recognized: boolean
  measurements: Measurement[]
}

// Missing cells can have no unit even under a unit-bearing header. Keep them in
// their source column; distinct raw headings must never collapse by axis alone.
const columnKey = (measurement: Measurement) => JSON.stringify([measurement.raw_label, measurement.recognized_label])

function buildColumns(measurements: Measurement[]): Column[] {
  const columns = new Map<string, Column>()
  for (const measurement of measurements) {
    const key = columnKey(measurement)
    const existing = columns.get(key)
    if (existing) {
      existing.measurements.push(measurement)
      if (!existing.unit && measurement.unit) existing.unit = measurement.unit
      continue
    }
    columns.set(key, {
      key,
      label: measurement.raw_label || (measurement.recognized_label ? humanize(measurement.recognized_label) : 'Unlabeled column'),
      unit: measurement.unit,
      recognized: measurement.recognized_label !== null,
      measurements: [measurement],
    })
  }
  return [...columns.values()]
}

function columnHeading(column: Column) {
  if (!column.unit || column.label.includes('(') || column.label.toLowerCase().includes(column.unit.toLowerCase())) return column.label
  return `${column.label} (${column.unit})`
}

function statusLabel(status: ParseResult['status']) {
  if (status === 'PARSED_UNVERIFIED') return 'Lexical · unverified'
  if (status === 'PARTIAL') return 'Partial parse'
  if (status === 'UNSUPPORTED') return 'Unsupported'
  return 'Invalid structure'
}

function CellValue({ measurements }: { measurements: Measurement[] }) {
  if (measurements.length === 0) return <span className="report-badge report-badge-notice">Missing</span>
  return <div className="space-y-1.5">{measurements.map(measurement => {
    if (measurement.numeric_status === 'MISSING' || measurement.numeric_status === 'NOT_PRESENT') {
      return <span key={measurement.id} className="report-badge report-badge-notice">Missing</span>
    }
    if (measurement.numeric_status === 'PARSED' || measurement.numeric_status === 'EXPLICIT_ZERO') {
      const value = measurement.signed_decimal ?? measurement.raw_value
      return <span key={measurement.id} className="structured-value">{value ?? 'Not supplied'}{measurement.raw_direction && <span className="ml-1 text-xs font-normal text-muted">{measurement.raw_direction}</span>}{measurement.field_status === 'AMBIGUOUS' && <span className="report-badge report-badge-notice ml-2">Ambiguous</span>}{!measurement.unit && <span className="mt-1 block text-xs font-normal text-muted">Unit unknown</span>}</span>
    }
    const label = measurement.numeric_status === 'AMBIGUOUS' ? 'Ambiguous' : measurement.numeric_status === 'INVALID' ? 'Invalid' : 'Not parsed'
    return <div key={measurement.id}>
      <span className={`report-badge ${measurement.numeric_status === 'AMBIGUOUS' ? 'report-badge-notice' : 'report-badge-danger'}`}>{label}</span>
      {measurement.raw_value !== null && measurement.raw_value !== '' && <code className="raw-text mt-1 block text-[11px] leading-5 text-muted">{measurement.raw_value}</code>}
    </div>
  })}</div>
}

export default function StructuredPreview({ result, rawText, loading, showRawEvidence = false }: {
  result: ParseResult | null
  rawText: string
  loading: boolean
  showRawEvidence?: boolean
}) {
  const columns = result ? buildColumns(result.measurements) : []
  const toothIds = result ? [...new Set([...result.teeth.map(tooth => tooth.id), ...result.measurements.map(measurement => measurement.tooth_ref)])] : []
  const teeth = new Map(result?.teeth.map(tooth => [tooth.id, tooth]) ?? [])
  const cells = new Map<string, Measurement[]>()
  for (const measurement of result?.measurements ?? []) {
    const key = `${measurement.tooth_ref}\u0000${columnKey(measurement)}`
    cells.set(key, [...(cells.get(key) ?? []), measurement])
  }
  const visibleToothIds = toothIds

  return <section aria-labelledby="structured-preview-heading" aria-busy={loading} className="panel flex min-w-0 flex-col">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><Table2 size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="structured-preview-heading" className="panel-title">Structured table</h3></div>
      <span className="rounded-md border border-line bg-canvas px-2 py-1 text-[11px] font-medium text-muted">{result ? statusLabel(result.status) : loading ? 'Parsing' : 'Awaiting parse'}</span>
    </div>
    <div className="flex flex-1 flex-col p-5 sm:p-6">
      {!result ? <div className="flex min-h-[240px] flex-1 flex-col items-center justify-center rounded-lg border border-dashed border-line bg-canvas px-6 py-10 text-center">
        <span className="mb-3 rounded-xl border border-line bg-white p-3 text-brand"><Table2 size={22} strokeWidth={1.5} aria-hidden="true" /></span>
        <p className="text-sm font-medium">Parse your TMT to see the structured table.</p>
        <p className="mt-2 max-w-64 text-xs leading-5 text-muted">{loading ? 'Parsing… the table will appear after the response is validated.' : 'The table will use only the parser’s returned structural fields. Nothing is inferred or corrected.'}</p>
      </div> : result.measurements.length === 0 ? <div className="rounded-lg border border-line bg-canvas p-4 text-sm leading-6">
        <p className="font-medium">No measurement cells were returned.</p>
        <p className="mt-1 text-xs leading-5 text-muted">Check the headings and row alignment in your original text, which remains editable.</p>
      </div> : <>
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div>
            <p className="text-xs leading-5 text-muted">{result.teeth.length} tooth {result.teeth.length === 1 ? 'row' : 'rows'} · {result.measurements.length} measurement {result.measurements.length === 1 ? 'position' : 'positions'}</p>
            <p className="mt-1 text-xs leading-5 text-muted">Parsed values with original direction tokens. Missing values are not zero. Tooth identity and movement conventions remain unverified.</p>
          </div>
        </div>
        <div role="region" aria-label="Structured TMT table" tabIndex={0} className="structured-table-scroll mt-3">
          <table className={`structured-table${columns.length > 3 ? ' structured-table-wide' : ''}`}>
            <caption className="sr-only">Structured TMT table from parser output. Values are lexical and unverified; missing, ambiguous and unrecognized cells are marked.</caption>
            <thead><tr>
              <th scope="col">Tooth</th>
              {columns.map(column => <th key={column.key} scope="col">
                <span>{columnHeading(column)}</span>
                {!column.recognized && <span className="report-badge report-badge-notice mt-1 block w-fit">Unrecognized</span>}
              </th>)}
            </tr></thead>
            <tbody>{visibleToothIds.map(toothId => {
              const tooth = teeth.get(toothId)
              return <tr key={toothId}>
                <th scope="row">
                  <code className="raw-text text-[13px] font-semibold text-ink">{tooth?.raw_identifier ?? 'Unresolved token'}</code>
                  <span className="tooth-status mt-1 block text-[11px] font-normal leading-4 text-muted">{humanize(tooth?.identifier_status ?? 'UNKNOWN')}</span>
                </th>
                {columns.map(column => <td key={column.key} data-label={`${columnHeading(column)}${column.recognized ? '' : ' · unrecognized'}`}><CellValue measurements={cells.get(`${toothId}\u0000${column.key}`) ?? []} /></td>)}
              </tr>
            })}</tbody>
          </table>
        </div>
      </>}

      {showRawEvidence && <details className="mt-4 rounded-lg border border-line bg-canvas p-3 text-xs leading-6 text-muted">
        <summary className="cursor-pointer font-medium text-ink">Raw preview · original TMT text</summary>
        <p className="mt-2">The editable source remains on the left. This faithful copy is kept only as evidence of the exact submitted characters.</p>
        <pre aria-label="Raw text preview" tabIndex={0} className="raw-text mt-2 max-h-72 min-h-24 overflow-auto rounded-lg border border-line bg-white p-3 text-[13px] leading-6">{rawText}</pre>
        <p className="mt-2">Spacing and line breaks are retained. Long rows wrap to fit.</p>
      </details>}
    </div>
  </section>
}
