import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import StructuredPreview from './components/StructuredPreview'
import type { Measurement, ParseResult } from './api/parse'
import fixture from './test/fixtures/synthetic-parse-result.json'

const baseTooth = fixture.teeth[0]
const baseMeasurement = fixture.measurements[0] as Measurement

function tooth(id: string, rawIdentifier: string) {
  return { ...baseTooth, id, raw_identifier: rawIdentifier }
}

function measurement(overrides: Partial<Measurement> & Pick<Measurement, 'id' | 'tooth_ref'>): Measurement {
  return { ...baseMeasurement, ...overrides }
}

function result(teeth: ParseResult['teeth'], measurements: Measurement[]): ParseResult {
  return { ...fixture, status: 'PARTIAL', teeth, measurements } as ParseResult
}

const parsed: ParseResult = result(
  [tooth('tooth-1', '13'), tooth('tooth-2', '14'), tooth('tooth-3', '15')],
  [
    measurement({
      id: 'measurement-rotation', tooth_ref: 'tooth-1',
      raw_label: 'Rotation (deg)', recognized_label: 'rotation', unit: 'deg',
      raw_value: '−1.2300 M', signed_decimal: '-1.2300', magnitude_decimal: '1.2300',
      raw_direction: 'M', numeric_status: 'PARSED', field_status: 'SEMANTICS_UNKNOWN',
    }),
    measurement({
      id: 'measurement-extrusion', tooth_ref: 'tooth-2',
      raw_label: 'Extrusion (mm)', recognized_label: 'extrusion', unit: 'mm',
      raw_value: null, signed_decimal: null, magnitude_decimal: null, raw_direction: null,
      numeric_status: 'MISSING', field_status: 'NOT_PRESENT',
    }),
    measurement({
      id: 'measurement-unknown', tooth_ref: 'tooth-3',
      raw_label: 'Unknown label', recognized_label: null, unit: null,
      raw_value: 'invented entry', signed_decimal: null, magnitude_decimal: null, raw_direction: null,
      numeric_status: 'UNSUPPORTED', field_status: 'UNSUPPORTED',
    }),
  ],
)

describe('Structured TMT table', () => {
  it('shows the parse placeholder and keeps raw evidence closed before parsing', () => {
    render(<StructuredPreview result={null} rawText={'  unparsed\ttext\n'} loading={false} />)

    expect(screen.getByRole('heading', { name: 'Structured table' })).toBeVisible()
    expect(screen.getByText('Awaiting parse')).toBeVisible()
    expect(screen.getByText('Parse your TMT to see the structured table.')).toBeVisible()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()

    const preview = screen.getByLabelText('Raw text preview')
    expect(preview.textContent).toBe('  unparsed\ttext\n')
    const disclosure = preview.closest('details')
    expect(disclosure).not.toHaveAttribute('open')
  })

  it('marks a pending parse as busy without rendering a table', () => {
    render(<StructuredPreview result={null} rawText="" loading />)
    expect(screen.getByRole('region', { name: 'Structured table' })).toHaveAttribute('aria-busy', 'true')
    expect(screen.getByText('Parsing')).toBeVisible()
    expect(screen.getByText(/the table will appear after the response is validated/)).toBeVisible()
  })

  it('derives column headings, rows and values only from parser output', () => {
    render(<StructuredPreview result={parsed} rawText={fixture.raw_text} loading={false} />)
    const table = screen.getByRole('table', { name: /Structured TMT table from parser output/ })

    expect(within(table).getByRole('columnheader', { name: 'Tooth' })).toBeVisible()
    expect(within(table).getByRole('columnheader', { name: /Rotation \(deg\)/ })).toBeVisible()
    expect(within(table).getByRole('columnheader', { name: /Extrusion \(mm\)/ })).toBeVisible()
    const unknownHeader = within(table).getByRole('columnheader', { name: /Unknown label/ })
    expect(unknownHeader).toHaveTextContent('Unrecognized')

    const rotationRow = within(table).getByRole('rowheader', { name: /13/ }).closest('tr')!
    const rotationCells = within(rotationRow).getAllByRole('cell')
    expect(rotationCells[0]).toHaveAttribute('data-label', 'Rotation (deg)')
    expect(rotationCells[2]).toHaveAttribute('data-label', 'Unknown label · unrecognized')
    expect(within(rotationRow).getByText('-1.2300')).toBeVisible()
    expect(within(rotationRow).getByText('M')).toBeVisible()

    const missingRow = within(table).getByRole('rowheader', { name: /14/ }).closest('tr')!
    expect(within(missingRow).getAllByText('Missing')).toHaveLength(3)

    const unknownRow = within(table).getByRole('rowheader', { name: /15/ }).closest('tr')!
    expect(within(unknownRow).getByText('invented entry')).toBeVisible()
    expect(within(unknownRow).getByText('Not parsed')).toBeVisible()
  })

  it('keeps explicit zero, ambiguous and invalid values distinct without correcting them', () => {
    const statuses: ParseResult = result(
      [tooth('tooth-1', '13')],
      [
        measurement({ id: 'zero', tooth_ref: 'tooth-1', raw_label: 'Rotation (deg)', recognized_label: 'rotation', unit: 'deg', raw_value: '0.0000', signed_decimal: '0.0000', magnitude_decimal: '0.0000', raw_direction: null, numeric_status: 'EXPLICIT_ZERO', field_status: 'ACCEPTED' }),
        measurement({ id: 'ambiguous', tooth_ref: 'tooth-1', raw_label: 'Extrusion (mm)', recognized_label: null, unit: null, raw_value: '~0.2 E', signed_decimal: null, magnitude_decimal: null, raw_direction: null, numeric_status: 'AMBIGUOUS', field_status: 'AMBIGUOUS' }),
        measurement({ id: 'invalid', tooth_ref: 'tooth-1', raw_label: 'Buccolingual (mm)', recognized_label: null, unit: null, raw_value: '1.2.3 B', signed_decimal: null, magnitude_decimal: null, raw_direction: null, numeric_status: 'INVALID', field_status: 'PARSE_INVALID' }),
      ],
    )
    render(<StructuredPreview result={statuses} rawText={fixture.raw_text} loading={false} />)
    const table = screen.getByRole('table', { name: /Structured TMT table from parser output/ })

    expect(within(table).getByText('0.0000')).toBeVisible()
    expect(within(table).getByText('Ambiguous')).toBeVisible()
    expect(within(table).getByText('~0.2 E')).toBeVisible()
    expect(within(table).getByText('Invalid')).toBeVisible()
    expect(within(table).getByText('1.2.3 B')).toBeVisible()
  })

  it('keeps the exact submitted characters in a closed evidence disclosure', () => {
    const raw = '# SYNTHETIC\n\nTooth\tRotation (deg)\n  13 \t−1.2300 M  \n'
    render(<StructuredPreview result={parsed} rawText={raw} loading={false} />)

    const preview = screen.getByLabelText('Raw text preview')
    const disclosure = preview.closest('details')!
    expect(disclosure).not.toHaveAttribute('open')
    expect(preview.textContent).toBe(raw)

    fireEvent.click(within(disclosure).getByText('Raw preview · original TMT text'))
    expect(disclosure).toHaveAttribute('open')
    expect(within(disclosure).getByText(/faithful copy is kept only as evidence/)).toBeVisible()
  })

  it('reports when the parser returns no measurement positions', () => {
    render(<StructuredPreview result={result([tooth('tooth-1', '13')], [])} rawText={fixture.raw_text} loading={false} />)
    expect(screen.getByText('No measurement cells were returned.')).toBeVisible()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()
    expect(screen.getByLabelText('Raw text preview').textContent).toBe(fixture.raw_text)
  })
})
