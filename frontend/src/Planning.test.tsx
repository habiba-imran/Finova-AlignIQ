import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import PlanningWorkspace from './components/PlanningWorkspace'
import { eligibleComment, isPlanningDraft, selectedExport } from './api/planning'
import type { PlanningDraft, DemoInput } from './api/planning'
import demoInputJson from './test/fixtures/planning-demo-input.json'
import demoDraftJson from './test/fixtures/planning-demo-draft.json'
import unverifiedReport from './test/fixtures/synthetic-final-report.json'
import unverifiedParse from './test/fixtures/synthetic-parse-result.json'

const input = demoInputJson as DemoInput
const fixture = demoDraftJson as PlanningDraft
const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers() })

function panel(fetch = vi.fn().mockResolvedValue(ok(fixture))) {
  vi.stubGlobal('fetch', fetch)
  const complete = vi.fn()
  render(<PlanningWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo onComplete={complete} />)
  fireEvent.change(screen.getByLabelText('Wording preference'), { target: { value: 'TEMPLATES' } })
  return { fetch, complete, run: screen.getByRole('button', { name: 'Run Planning Assistant' }) }
}
async function generated() {
  const state = panel()
  fireEvent.click(state.run)
  const article = await screen.findByRole('article', { name: 'Planning Assistant draft' })
  return { ...state, article }
}

it('accepts the real modern synthetic contract and accounts for every comment once', () => {
  expect(isPlanningDraft(fixture)).toBe(true)
  expect(new Set(fixture.sections.flatMap(s => s.comment_ids)).size).toBe(fixture.report.comments.length)
  expect(fixture.report.engine_review.evaluations).toHaveLength(96)
})
it.each(['missing-section', 'duplicate', 'unavailable-promotion', 'unknown-id', 'missing-comment', 'missing-export-context'])('rejects malformed planning contract: %s', change => {
  const value = structuredClone(fixture)
  if (change === 'missing-section') value.sections.pop()
  if (change === 'duplicate') value.sections[0].comment_ids.push(value.sections[0].comment_ids[0])
  if (change === 'unavailable-promotion') value.sections[0].comment_ids.push(value.sections[4].comment_ids.shift()!)
  if (change === 'unknown-id') value.sections[0].comment_ids[0] = '0'.repeat(64)
  if (change === 'missing-comment') value.sections[0].comment_ids.pop()
  if (change === 'missing-export-context') value.export_text = value.report.export_text
  expect(isPlanningDraft(value)).toBe(false)
})
it('runs once on explicit initiation, groups dimensions and keeps original exact values', async () => {
  const { fetch, run, complete } = panel()
  expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(run)
  const article = await screen.findByRole('article', { name: 'Planning Assistant draft' })
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/development/planning-demo/draft')
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ comment_mode: 'TEMPLATES' })
  expect(complete).toHaveBeenLastCalledWith(true)
  for (const dimension of ['Sagittal', 'Transverse', 'Vertical']) expect(within(article).getByRole('region', { name: `${dimension} review` })).toBeVisible()
  expect(within(article).getAllByText('1.2300 D', { exact: true }).length).toBeGreaterThan(0)
  expect(within(article).getByText(/4 of 20 positions eligible; 16 unavailable/)).toBeVisible()
  expect(within(article).getByText('DRAFT — Requires Orthodontist Review')).toBeVisible()
  expect(within(article).getByText(/Clinical diagnosis, suitability/)).toBeVisible()
  expect(within(article).getByText(/No provider call was made/)).toBeVisible()
})
it('copies only selected eligible comments with complete withholding context and provenance', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined)
  vi.stubGlobal('navigator', { clipboard: { writeText } })
  const { article } = await generated()
  const box = within(article).getAllByRole('checkbox')[0]
  fireEvent.click(box)
  expect(within(article).getByText('1 selected of 5 eligible comments')).toBeVisible()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy selected comments' }))
  await screen.findByText(/Selected comments copied/)
  const copied = writeText.mock.calls[0][0]
  const selected = fixture.report.comments.find(c => c.comment_id === fixture.sections[0].comment_ids[0])!
  expect(copied).toContain(selected.text)
  expect(copied).toContain(selected.finding_ids[0])
  expect(copied).toContain(selected.evidence_refs[0])
  expect(copied).toContain('DRAFT — Requires Orthodontist Review')
  expect(copied).toContain('FINOVA SYNTHETIC DEMONSTRATION — TEST_ONLY')
  expect(copied).toContain('WITHHELD ASSESSMENTS')
  expect(copied).toContain(fixture.report.engine_review.raw_sha256)
  for (const limitation of fixture.report.limitations) expect(copied).toContain(limitation)
  expect(copied).not.toContain('0.4500 B')
  fireEvent.click(within(article).getByRole('button', { name: 'Clear selection' }))
  expect(within(article).getByRole('button', { name: 'Copy selected comments' })).toBeDisabled()
})
it('selects all eligible comments and never offers unavailable assessments for selection', async () => {
  const { article } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Select all eligible comments' }))
  expect(within(article).getByText('5 selected of 5 eligible comments')).toBeVisible()
  expect(within(article).getAllByRole('checkbox')).toHaveLength(5)
  fireEvent.click(within(article).getByText(/^Inspect withheld assessments/))
  const unavailable = within(article).getByRole('region', { name: 'Missing context and withheld assessments' })
  expect(within(unavailable).queryByRole('checkbox')).not.toBeInTheDocument()
})
it('whole report copying preserves the exact complete dimension index and engine export', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined)
  vi.stubGlobal('navigator', { clipboard: { writeText } })
  const { article } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy complete DRAFT report' }))
  await screen.findByText(/Complete DRAFT report copied/)
  expect(writeText).toHaveBeenCalledWith(fixture.export_text)
})
it('reports clipboard failure without losing the usable draft', async () => {
  vi.stubGlobal('navigator', { clipboard: { writeText: vi.fn().mockRejectedValue(new Error()) } })
  const { article } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy complete DRAFT report' }))
  expect(await screen.findByText(/Clipboard access is unavailable/)).toBeVisible()
  expect(article).toBeVisible()
})
it('downloads the complete DRAFT as a local TXT Blob and revokes its URL', async () => {
  const create = vi.fn().mockReturnValue('blob:synthetic-export'), revoke = vi.fn()
  vi.stubGlobal('URL', { createObjectURL: create, revokeObjectURL: revoke })
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const { article, fetch } = await generated()
  vi.useFakeTimers()
  fireEvent.click(within(article).getByRole('button', { name: 'Download DRAFT (TXT)' }))
  expect(create.mock.calls[0][0]).toBeInstanceOf(Blob)
  expect(click).toHaveBeenCalledOnce()
  expect(fetch).toHaveBeenCalledOnce()
  act(() => vi.runOnlyPendingTimers())
  expect(revoke).toHaveBeenCalledWith('blob:synthetic-export')
})
it('does not copy unavailable or forged selections', () => {
  expect(selectedExport(fixture.report, new Set(['forged', fixture.sections[4].comment_ids[0]]))).toBe('')
  expect(fixture.report.comments.filter(eligibleComment)).toHaveLength(5)
})
it('aborts stale requests and clears selections/exports when wording changes', async () => {
  let finish!: (v: unknown) => void
  const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
  const { run } = panel(fetch)
  fireEvent.click(run)
  expect(screen.getByRole('button', { name: 'Preparing planning draft…' })).toBeDisabled()
  const signal = fetch.mock.calls[0][1].signal
  fireEvent.change(screen.getByLabelText('Wording preference'), { target: { value: 'AUTO' } })
  expect(signal.aborted).toBe(true)
  await act(async () => finish(ok(fixture)))
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Run Planning Assistant' })).toBeEnabled()
})
it('shows errors, preserves a retry action and never retries automatically', async () => {
  const { run, fetch } = panel(vi.fn().mockResolvedValue({ ok: false, status: 503 }))
  fireEvent.click(run)
  expect(await screen.findByRole('alert')).toHaveTextContent('original text is preserved')
  expect(fetch).toHaveBeenCalledOnce()
  expect(run).toBeEnabled()
})
it('loads a fixed demo only on explicit action; edits discard authority and stale output', async () => {
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockResolvedValueOnce(ok(fixture))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova planning demo' }))
  await screen.findByRole('button', { name: 'Run Planning Assistant' })
  const raw = screen.getByRole('textbox', { name: 'Raw TMT text' })
  expect(raw).toHaveValue(input.parsed.raw_text)
  expect(screen.getByLabelText('Raw text preview').textContent).toBe(input.parsed.raw_text)
  fireEvent.change(screen.getByLabelText('Wording preference'), { target: { value: 'TEMPLATES' } })
  fireEvent.click(screen.getByRole('button', { name: 'Run Planning Assistant' }))
  await screen.findByRole('article', { name: 'Planning Assistant draft' })
  fireEvent.change(raw, { target: { value: input.parsed.raw_text + 'edited' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Run Planning Assistant' })).not.toBeInTheDocument()
  expect(screen.getByRole('checkbox')).not.toBeChecked()
  expect(fetch).toHaveBeenCalledTimes(2)
})
it('Micro and Nano have distinct intake while original text is preserved', () => {
  const fetch = vi.fn(); vi.stubGlobal('fetch', fetch)
  render(<App />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'original synthetic text' } })
  const nav = screen.getByRole('navigation', { name: 'Review purpose' })
  fireEvent.click(within(nav).getByRole('button', { name: /MICRO/ }))
  expect(screen.getByRole('button', { name: 'Load Finova attachment demo' })).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Run Planning Assistant' })).not.toBeInTheDocument()
  fireEvent.click(within(nav).getByRole('button', { name: /NANO/ }))
  expect(screen.getByRole('button', { name: 'Load Finova sequencing demo' })).toBeVisible()
  fireEvent.click(within(nav).getByRole('button', { name: /MACRO/ }))
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue('original synthetic text')
  expect(fetch).not.toHaveBeenCalled()
})
it('a disabled demonstration is explained without replacing the current raw text', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 404 }))
  render(<App />)
  const raw = screen.getByRole('textbox', { name: 'Raw TMT text' })
  fireEvent.change(raw, { target: { value: 'retained synthetic input' } })
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova planning demo' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('disabled on this backend')
  expect(raw).toHaveValue('retained synthetic input')
})
it('ordinary unknown vendor input produces dimension-specific unavailability without selectable observations', async () => {
  const report = unverifiedReport as unknown as PlanningDraft['report']
  const value: PlanningDraft = { version: '1.0.0', report, export_text: report.export_text, sections: [
    ...(['SAGITTAL', 'TRANSVERSE', 'VERTICAL', 'OTHER'] as const).map(dimension => ({ dimension, comment_ids: [], explanation: 'No sufficiently authorized descriptions for this dimension.' })),
    { dimension: 'UNAVAILABLE', comment_ids: report.comments.map(c => c.comment_id), explanation: 'Withheld.' },
  ] }
  const fetch = vi.fn().mockResolvedValue(ok(value)); vi.stubGlobal('fetch', fetch)
  render(<PlanningWorkspace rawText={unverifiedParse.raw_text} context={{ ...input.context, source_version: null }} parsed={unverifiedParse as unknown as DemoInput['parsed']} demo={false} onComplete={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: 'Run Planning Assistant' }))
  const article = await screen.findByRole('article', { name: 'Planning Assistant draft' })
  expect(within(article).getAllByText('No sufficiently authorized descriptions for this dimension.')).toHaveLength(4)
  expect(within(article).getByRole('button', { name: 'Copy selected comments' })).toBeDisabled()
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/planning/draft')
  expect(JSON.parse(fetch.mock.calls[0][1].body)).not.toHaveProperty('test_only')
})
