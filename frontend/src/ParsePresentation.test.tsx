import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import ParseResults from './components/ParseResults'
import fixture from './test/fixtures/synthetic-parse-result.json'
import type { AutomaticParseResult, ParseResult } from './api/parse'

const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

function parse(response: unknown) {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(ok(response)))
  render(<App />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: fixture.raw_text } })
  fireEvent.click(screen.getByRole('checkbox', { name: /I confirm/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
}

describe('Part 2 parser presentation', () => {
  it('promotes parsed movements, keeps the raw preview available, and summarizes actual parser counts', async () => {
    parse(fixture)
    const summary = await screen.findByLabelText('Parse summary')
    expect(within(summary).getByText('Tooth token positions').parentElement).toHaveTextContent('Tooth token positions1')
    expect(within(summary).getByText('Movement positions').parentElement).toHaveTextContent('Movement positions1')
    expect(within(summary).getByText('Missing values').parentElement).toHaveTextContent('Missing values0')
    expect(within(summary).getByText('Issues requiring attention').parentElement).toHaveTextContent('Issues requiring attention3')

    const measurements = screen.getByRole('region', { name: 'Parsed measurements' })
    expect(measurements).toBeVisible()
    expect(within(measurements).getByText('−1.2300 M')).toBeVisible()
    expect(within(measurements).getByText('-1.2300')).toBeVisible()
    expect(within(measurements).getByText('Magnitude: 1.2300')).toBeVisible()

    const preview = screen.getByLabelText('Raw text preview')
    expect(preview.textContent).toBe(fixture.raw_text)
    const disclosure = preview.closest('details')
    expect(disclosure).not.toBeNull()
    expect(disclosure).not.toHaveAttribute('open')

    expect(screen.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Parsing warnings and errors' })).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Fields requiring clarification or verification' })).toBeVisible()
    expect(screen.getByText(/WARNING · SOURCE_UNVERIFIED/)).toBeInTheDocument()
    expect(screen.getByText(/Source verification: UNVERIFIED/)).toBeVisible()
  }, 15_000)

  it('keeps blocking parse errors visible and exposes row evidence on demand', async () => {
    const returned = structuredClone(fixture) as AutomaticParseResult
    returned.issues.push({ code: 'SYNTHETIC_BLOCKER', severity: 'ERROR', message: 'Synthetic blocking issue.', field: null, span: null })
    parse(returned)
    const blockers = await screen.findByRole('region', { name: 'Blocking parse issues' })
    expect(blockers).toBeVisible()
    expect(blockers).toHaveTextContent('Synthetic blocking issue.')

    const measurements = screen.getByRole('region', { name: 'Parsed measurements' })
    fireEvent.click(within(measurements).getByText('Row details'))
    expect(within(measurements).getByText(/Literal direction: M/)).toBeVisible()
    expect(within(measurements).getByText('Semantic verification: NOT VERIFIED.')).toBeVisible()
  })

  it('renders explicit zero and missing values as distinct states without changing precision', () => {
    const result = structuredClone(fixture) as ParseResult
    const base = result.measurements[0]
    result.measurements = [
      { ...base, id: 'measurement-zero', raw_value: '0.0000', signed_decimal: '0.0000', magnitude_decimal: '0.0000', numeric_status: 'EXPLICIT_ZERO', field_status: 'ACCEPTED' },
      { ...base, id: 'measurement-missing', raw_value: null, signed_decimal: null, magnitude_decimal: null, numeric_status: 'MISSING', field_status: 'MISSING', unit: null, raw_direction: null, span: null },
    ]
    render(<ParseResults result={result} />)
    const measurements = screen.getByRole('region', { name: 'Parsed measurements' })
    const zeroRow = within(measurements).getAllByText('0.0000')[0].closest('tr')!
    expect(within(zeroRow).getByText('explicit zero')).toBeVisible()
    const missingRow = within(measurements).getByText('(omitted cell)').closest('tr')!
    expect(within(missingRow).getAllByText('missing').length).toBeGreaterThan(0)
    expect(within(missingRow).getByText('Not accepted')).toBeVisible()
  })
})
