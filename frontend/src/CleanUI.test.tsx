import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import PlanningWorkspace from './components/PlanningWorkspace'
import StructuredPreview from './components/StructuredPreview'
import ParserStatus from './components/ParserStatus'
import { isPlanningDraft } from './api/planning'
import type { DemoInput, PlanningDraft } from './api/planning'
import type { AutomaticParseResult } from './api/parse'
import inputJSON from './test/fixtures/planning-demo-input.json'
import templateJSON from './test/fixtures/planning-demo-draft.json'

const input = inputJSON as DemoInput
const templates = templateJSON as PlanningDraft
const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

// Simulated approved wording response; no live provider is used by these tests.
function enhancedFixture() {
  const value = structuredClone(templates)
  const comment = value.report.comments.find(c => c.section === 'TOOTH')!
  const old = comment.text
  comment.text = 'The source reports programmed mesiodistal displacement. Anchorage, space closure and root movement are not assessed.' + old.slice(old.indexOf('\n'))
  comment.wording_source = 'GROQ_VALIDATED'; comment.wording_validation = 'ACCEPTED'
  value.report.export_text = value.report.export_text.replace(old, comment.text)
  value.export_text = value.export_text.replace(old, comment.text)
  Object.assign(value.report.generation, { requested_mode: 'AUTO', used_mode: 'MIXED', reason: 'GROQ_VALIDATED', attempts: 1, accepted_comments: 1, provider: 'GROQ', model: 'openai/gpt-oss-120b' })
  return value
}
function workspace(fetch: ReturnType<typeof vi.fn>) {
  vi.stubGlobal('fetch', fetch)
  render(<PlanningWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo onComplete={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: 'Run Planning Assistant' }))
}

it('keeps the normal workspace free of duplicate raw text, JSON and engineering actions', async () => {
  const fetch = vi.fn().mockResolvedValue(ok(input.parsed)); vi.stubGlobal('fetch', fetch)
  render(<App />)
  expect(fetch).not.toHaveBeenCalled()
  expect(screen.getByText(/Synthetic demonstration — not for clinical use/)).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Load Finova planning demo' })).not.toBeInTheDocument()
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: input.parsed.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  await screen.findByRole('button', { name: 'Run Planning Assistant' })
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(input.parsed.raw_text)
  expect(screen.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  expect(screen.queryByLabelText('Raw text preview')).not.toBeInTheDocument()
  expect(screen.queryByLabelText('Full parsing JSON')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Create draft review' })).not.toBeInTheDocument()
  expect(screen.queryByText(/Groq|rule ledger|Provider attempts/i)).not.toBeInTheDocument()
  expect(screen.queryByText('Verified synthetic demonstration only')).not.toBeInTheDocument()
})

it.each([404, 503])('disables unavailable demo after HTTP %s without exposing server details', async status => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status, json: async () => ({ detail: 'PRIVATE_CONFIG' }) }))
  render(<App diagnostics />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'retained original' } })
  const button = screen.getByRole('button', { name: 'Load Finova planning demo' })
  fireEvent.click(button)
  expect(await screen.findByRole('alert')).toHaveTextContent('unavailable in this session')
  expect(button).toBeDisabled()
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue('retained original')
  expect(screen.queryByText(/PRIVATE_CONFIG|FINOVA_ENVIRONMENT/)).not.toBeInTheDocument()
})

it('shows fallback as standard wording with an unavailable AI view and no comparison request', async () => {
  const fallback = structuredClone(templates)
  fallback.report.generation.requested_mode = 'AUTO'
  const fetch = vi.fn().mockResolvedValue(ok(fallback)); workspace(fetch)
  const article = await screen.findByRole('article')
  expect(within(article).getByRole('heading', { name: 'Standard Report — Template-Based' })).toBeVisible()
  expect(fetch).toHaveBeenCalledOnce()
  fireEvent.click(screen.getByRole('button', { name: /B. AI-Assisted Report/ }))
  expect(screen.getByText(/AI-assisted wording is unavailable/)).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Export PDF' })).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledOnce()
})

it('compares actual server template and approved AI wording, and exports the selected view exactly', async () => {
  const enhanced = enhancedFixture()
  expect(isPlanningDraft(enhanced)).toBe(true)
  const writeText = vi.fn().mockResolvedValue(undefined); vi.stubGlobal('navigator', { clipboard: { writeText } })
  const fetch = vi.fn().mockResolvedValueOnce(ok(enhanced)).mockResolvedValueOnce(ok(templates)); workspace(fetch)
  await screen.findByRole('article')
  expect(fetch).toHaveBeenCalledTimes(2)
  expect(fetch.mock.calls.map(call => JSON.parse(call[1].body).comment_mode)).toEqual(['AUTO', 'TEMPLATES'])
  fireEvent.click(screen.getByRole('button', { name: 'Copy' }))
  await screen.findByText(/Complete DRAFT report copied/)
  expect(writeText).toHaveBeenLastCalledWith(templates.export_text)
  fireEvent.click(screen.getByRole('button', { name: /B. AI-Assisted Report/ }))
  expect(screen.getByText(/Enhanced wording is available for some comments only/)).toBeVisible()
  expect(screen.getAllByRole('checkbox')).toHaveLength(1)
  expect(screen.getByText(enhanced.report.comments.find(c => c.wording_source === 'GROQ_VALIDATED')!.text.split('\n')[0])).toBeVisible()
  fireEvent.click(screen.getByRole('button', { name: 'Copy' }))
  await screen.findByText(/Complete DRAFT report copied/)
  expect(writeText).toHaveBeenLastCalledWith(enhanced.export_text)
  expect(fetch).toHaveBeenCalledTimes(2)
  expect(screen.queryByText(/GROQ|STANDARD_TEMPLATES|ledger|Provider attempts/)).not.toBeInTheDocument()
})

it('preserves approved wording when the independent template comparison is unavailable', async () => {
  workspace(vi.fn().mockResolvedValueOnce(ok(enhancedFixture())).mockResolvedValueOnce({ ok: false, status: 503 }))
  await screen.findByRole('article')
  expect(screen.getByText(/Your enhanced report is preserved/)).toBeVisible()
  expect(screen.getByRole('button', { name: 'Export TXT' })).toBeEnabled()
  fireEvent.click(screen.getByRole('button', { name: /A. Standard Report/ }))
  expect(screen.getByText('Standard template wording is unavailable for this review.')).toBeVisible()
})

it('ignores late comparison results after wording settings invalidate the run', async () => {
  let finish!: (value: unknown) => void
  const fetch = vi.fn().mockResolvedValueOnce(ok(enhancedFixture())).mockImplementationOnce(() => new Promise(resolve => { finish = resolve }))
  workspace(fetch)
  await act(async () => {})
  expect(fetch).toHaveBeenCalledTimes(2)
  fireEvent.change(screen.getByLabelText('Wording preference'), { target: { value: 'TEMPLATES' } })
  expect(fetch.mock.calls[1][1].signal.aborted).toBe(true)
  await act(async () => finish(ok(templates)))
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
})

it('keeps conflicting units, unknown units and duplicate cells visible without merging source columns', () => {
  const parsed = structuredClone(input.parsed)
  const base = parsed.measurements[0]
  parsed.measurements = [
    { ...base, id: 'mm', raw_label: 'Displacement (mm)', unit: 'mm', numeric_status: 'PARSED', signed_decimal: '1.23', field_status: 'AMBIGUOUS' },
    { ...base, id: 'deg', raw_label: 'Rotation (deg)', unit: 'deg', raw_value: '8', signed_decimal: '8' },
    { ...base, id: 'unknown', raw_label: 'Unknown unit', unit: null, numeric_status: 'PARSED', signed_decimal: '1.23' },
  ]
  render(<StructuredPreview result={parsed} rawText={parsed.raw_text} loading={false} />)
  expect(screen.getAllByRole('columnheader')).toHaveLength(4)
  expect(screen.getByText('Ambiguous')).toBeVisible()
  expect(screen.getByText('Unit unknown')).toBeVisible()
})

it('summarizes real parsing failures without raw issue codes or repetitive warning lists', () => {
  const parsed = structuredClone(input.parsed) as AutomaticParseResult
  parsed.issues = Array.from({ length: 20 }, () => ({ code: 'UNIT_CONFLICT', severity: 'ERROR', message: 'private technical wording', field: 'unit', span: null }))
  render(<ParserStatus result={parsed} />)
  expect(screen.getByRole('region', { name: 'Blocking parse issues' })).toHaveTextContent('Some cell units conflict with their column headings.')
  expect(screen.queryByText(/UNIT_CONFLICT|private technical wording/)).not.toBeInTheDocument()
  expect(screen.getAllByRole('listitem')).toHaveLength(1)
  expect(screen.getByText('Unverified input')).toBeVisible()
})

it('keeps a missing cell under its source heading when it has no parsed unit', () => {
  const parsed = structuredClone(input.parsed)
  const base = parsed.measurements[0]
  parsed.teeth = [parsed.teeth[0], { ...parsed.teeth[0], id: 'second-tooth', raw_identifier: '14' }]
  parsed.measurements = [
    { ...base, id: 'present', unit: 'deg', numeric_status: 'PARSED', signed_decimal: '1.2300', raw_value: '1.2300' },
    { ...base, id: 'absent', tooth_ref: 'second-tooth', unit: null, numeric_status: 'MISSING', signed_decimal: null, raw_value: '-' },
  ]
  render(<StructuredPreview result={parsed} rawText={parsed.raw_text} loading={false} />)
  expect(screen.getAllByRole('columnheader')).toHaveLength(2)
  expect(screen.getByText('1.2300')).toBeVisible()
  expect(screen.getByText('Missing')).toBeVisible()
})
