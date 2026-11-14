import { act, fireEvent, render, screen, within, waitFor } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import SequencingWorkspace from './components/SequencingWorkspace'
import { isSequencingDraft } from './api/sequencing'
import type { SequencingDemoInput, SequencingDraft } from './api/sequencing'
import inputJson from './test/fixtures/sequencer-demo-input.json'
import reportJson from './test/fixtures/sequencer-demo-draft.json'
import ordinaryJson from './test/fixtures/sequencer-unverified-draft.json'

const input = inputJson as SequencingDemoInput, fixture = reportJson as SequencingDraft
const ok = (v: unknown) => ({ ok: true, status: 200, json: async () => v })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers() })
function panel(fetch = vi.fn().mockResolvedValue(ok(fixture)), demo = true) {
  vi.stubGlobal('fetch', fetch)
  render(<SequencingWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo={demo} onComplete={() => {}} />)
  return { fetch, run: screen.getByRole('button', { name: 'Run Sequencing Review' }) }
}
async function generated() {
  const state = panel(); fireEvent.click(state.run)
  return { ...state, article: await screen.findByRole('article', { name: 'Sequencing review draft' }) }
}
it('validates actual synthetic and ordinary unavailable Nano reports', () => {
  expect(isSequencingDraft(fixture)).toBe(true)
  expect(isSequencingDraft(ordinaryJson)).toBe(true)
})
it.each(['side', 'policy', 'verified', 'token', 'window', 'stage-order', 'stage-kind', 'duplicate', 'missing-section', 'provider', 'missing-context', 'arch', 'segment-side', 'scope'])('rejects invalid or promoted Nano contracts: %s', change => {
  const body = structuredClone(fixture)
  if (change === 'side') body.entries.find(e => e.section === 'RIGHT_ANCHORAGE')!.side = 'LEFT'
  if (change === 'policy') Object.assign(body.entries[0], { policy_id: 'APPROVED' })
  if (change === 'verified') Object.assign(body.entries[0], { result_type: 'VERIFIED_OBSERVATION' })
  if (change === 'token') body.entries[0].original_tooth_tokens[0] = '99'
  if (change === 'window') body.entries[0].stage_window!.end_id = 'MISSING'
  if (change === 'stage-order') [body.stage_inspection.records[1], body.stage_inspection.records[2]] = [body.stage_inspection.records[2], body.stage_inspection.records[1]]
  if (change === 'stage-kind') body.stage_inspection.records[0].kind = 'UNKNOWN'
  if (change === 'duplicate') body.entries.push(body.entries[0])
  if (change === 'missing-section') body.entries = body.entries.filter(e => e.section !== 'LEFT_ANCHORAGE')
  if (change === 'provider') Object.assign(body, { provider: 'GROQ', provider_attempts: 1 })
  if (change === 'missing-context') body.export_text = 'Report without DRAFT context'
  if (change === 'arch') body.entries[0].synthetic_arch_id = 'DEMO_LOWER'
  if (change === 'segment-side') body.entries[2].synthetic_segment_id = 'DEMO_U_B'
  if (change === 'scope') body.entries[0].movement_scope = 'INCREMENTAL'
  expect(isSequencingDraft(body)).toBe(false)
})
it('runs only on explicit initiation and separates arch, segment and side notes with supplied origin', async () => {
  const { fetch, run } = panel(); expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(run)
  const article = await screen.findByRole('article', { name: 'Sequencing review draft' })
  await waitFor(() => expect(within(article).getByRole('heading', { name: 'Sequencing review draft' })).toHaveFocus())
  expect(fetch).toHaveBeenCalledOnce()
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/development/sequencer-demo/draft')
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({})
  for (const title of ['Upper-arch sequencing', 'Lower-arch sequencing', 'Segments & tooth groups', 'Right-side anchorage', 'Left-side anchorage', 'Unavailable assessments']) expect(within(article).getByRole('region', { name: title })).toBeVisible()
  expect(within(article).getByText('SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE', { exact: true })).toBeVisible()
  const upper = within(article).getByRole('region', { name: 'Upper-arch sequencing' })
  expect(within(upper).getByText(fixture.entries[0].text)).toBeVisible()
  fireEvent.click(within(upper).getByText('Evidence & source details'))
  expect(within(upper).getByText(/Supplied stage window IDs: DEMO_U_BASE/)).toBeVisible()
  expect(within(upper).getByText(/Evidence: FINOVA-NANO-1:/)).toBeVisible()
  expect(within(upper).getByText(/1.2300 D/)).toBeVisible()
})
it('normal input keeps missing stages and anchorage unknown, never invents a schedule', async () => {
  const { fetch, run } = panel(vi.fn().mockResolvedValue(ok(ordinaryJson)), false)
  fireEvent.click(run)
  const article = await screen.findByRole('article', { name: 'Sequencing review draft' })
  expect(within(article).getByRole('heading', { name: 'Actual stage data unavailable' })).toBeVisible()
  expect(within(article).queryByText('Supplied fictional statement', { exact: true })).not.toBeInTheDocument()
  const right = within(article).getByRole('region', { name: 'Right-side anchorage' })
  expect(within(right).getByText('Unknown', { exact: true })).toBeVisible()
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/sequencing/draft')
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ raw_text: input.parsed.raw_text, context: input.context, source_claim: 'Unknown', synthetic_data_confirmed: true })
})
it('copies exact complete server text with supplied origins, missing prerequisites and DRAFT notice', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined); vi.stubGlobal('navigator', { clipboard: { writeText } })
  const { article, fetch } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy sequencing DRAFT' }))
  await screen.findByText(/Sequencing DRAFT copied/)
  expect(writeText).toHaveBeenCalledWith(fixture.export_text)
  expect(fetch).toHaveBeenCalledOnce()
})
it('clipboard failure leaves the usable DRAFT and export preview', async () => {
  vi.stubGlobal('navigator', { clipboard: { writeText: vi.fn().mockRejectedValue(new Error()) } })
  const { article } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy sequencing DRAFT' }))
  expect(await screen.findByText(/Clipboard access is unavailable/)).toBeVisible()
  expect(article).toBeVisible()
})
it('downloads a local TXT Blob and revokes its URL without a provider/backend request', async () => {
  const create = vi.fn().mockReturnValue('blob:synthetic-nano'), revoke = vi.fn()
  vi.stubGlobal('URL', { createObjectURL: create, revokeObjectURL: revoke })
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const { article, fetch } = await generated(); vi.useFakeTimers()
  fireEvent.click(within(article).getByRole('button', { name: 'Download sequencing DRAFT (TXT)' }))
  expect(create.mock.calls[0][0]).toBeInstanceOf(Blob)
  act(() => vi.runOnlyPendingTimers()); expect(revoke).toHaveBeenCalledWith('blob:synthetic-nano')
  expect(fetch).toHaveBeenCalledOnce()
})
it('handles loading, duplicate clicks, errors and explicit retry without automatic calls', async () => {
  let finish!: (v: unknown) => void
  const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
  const { run } = panel(fetch); fireEvent.click(run)
  expect(screen.getByRole('button', { name: 'Preparing sequencing review…' })).toBeDisabled()
  fireEvent.click(run); expect(fetch).toHaveBeenCalledOnce()
  await act(async () => finish({ ok: false, status: 503 }))
  expect(await screen.findByRole('alert')).toHaveTextContent('original text is preserved')
  expect(run).toBeEnabled()
})
it.each(['input', 'context', 'consent', 'purpose'])('invalidates Nano output and exports after %s changes', async change => {
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockResolvedValueOnce(ok(fixture)); vi.stubGlobal('fetch', fetch)
  render(<App />)
  const nav = screen.getByRole('navigation', { name: 'Review purpose' })
  fireEvent.click(within(nav).getByRole('button', { name: /NANO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova sequencing demo' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Run Sequencing Review' }))
  await screen.findByRole('article', { name: 'Sequencing review draft' })
  if (change === 'input') fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'changed synthetic' } })
  if (change === 'context') fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'other' } })
  if (change === 'consent') fireEvent.click(screen.getByRole('checkbox', { name: /I confirm/ }))
  if (change === 'purpose') fireEvent.click(within(nav).getByRole('button', { name: /MICRO/ }))
  expect(screen.queryByRole('article', { name: 'Sequencing review draft' })).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Copy sequencing DRAFT' })).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})
it('aborts and suppresses a late Nano draft after input changes', async () => {
  let finish!: (v: unknown) => void
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockImplementationOnce(() => new Promise(resolve => { finish = resolve }))
  vi.stubGlobal('fetch', fetch); render(<App />)
  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /NANO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova sequencing demo' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Run Sequencing Review' }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'changed input' } })
  expect(fetch.mock.calls[1][1].signal.aborted).toBe(true)
  await act(async () => finish(ok(fixture)))
  expect(screen.queryByRole('article', { name: 'Sequencing review draft' })).not.toBeInTheDocument()
})
it('explains disabled demo access and retains current input', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 404 })); render(<App />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'retained synthetic text' } })
  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /NANO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova sequencing demo' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('disabled on this backend')
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue('retained synthetic text')
})
