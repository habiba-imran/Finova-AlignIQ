import { act, fireEvent, render, screen, within, waitFor } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import AttachmentWorkspace from './components/AttachmentWorkspace'
import { isAttachmentDraft } from './api/attachments'
import type { AttachmentDraft, AttachmentDemoInput } from './api/attachments'
import inputJson from './test/fixtures/attachment-demo-input.json'
import draftJson from './test/fixtures/attachment-demo-draft.json'
import unverifiedJson from './test/fixtures/attachment-unverified-draft.json'

const input = inputJson as AttachmentDemoInput, fixture = draftJson as AttachmentDraft
const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers() })
function panel(fetch = vi.fn().mockResolvedValue(ok(fixture)), demo = true) {
  vi.stubGlobal('fetch', fetch)
  render(<AttachmentWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo={demo} onComplete={() => {}} />)
  return { fetch, run: screen.getByRole('button', { name: 'Run Attachment Review' }) }
}
async function generated() {
  const state = panel(); fireEvent.click(state.run)
  return { ...state, article: await screen.findByRole('article', { name: 'Attachment review draft' }) }
}
it('validates real demo and ordinary attachment contracts', () => {
  expect(isAttachmentDraft(fixture)).toBe(true)
  expect(isAttachmentDraft(unverifiedJson)).toBe(true)
  expect(fixture.entries.filter(e => e.result_type === 'CANDIDATE')).toHaveLength(2)
})
it.each(['approval', 'verified-identity', 'missing-evidence', 'wrong-observation', 'unknown-geometry', 'no-attachment-geometry', 'bad-alternative', 'duplicate', 'provider', 'missing-draft'])('rejects unsafe attachment response: %s', change => {
  const body = structuredClone(fixture)
  if (change === 'approval') Object.assign(body.entries[0], { approval_status: 'APPROVED' })
  if (change === 'verified-identity') Object.assign(body.entries[0], { verified_tooth: '13' })
  if (change === 'missing-evidence') body.entries[0].evidence_refs = []
  if (change === 'wrong-observation') body.entries[0].observation_refs = ['measurement-8']
  if (change === 'unknown-geometry') body.entries[4].design = body.entries[0].design
  if (change === 'no-attachment-geometry') body.entries[3].design = body.entries[0].design
  if (change === 'bad-alternative') body.entries[1].alternative_for = body.entries[2].entry_id
  if (change === 'duplicate') body.entries.push(body.entries[0])
  if (change === 'provider') Object.assign(body, { provider: 'GROQ', provider_attempts: 1 })
  if (change === 'missing-draft') body.export_text = 'Report without context'
  expect(isAttachmentDraft(body)).toBe(false)
})
it('runs only after explicit initiation and presents candidates, alternatives, supplied none, unknown and withheld', async () => {
  const { fetch, run } = panel()
  expect(fetch).not.toHaveBeenCalled()
  expect(screen.getByText(/Your attachment review table will appear/)).toBeVisible()
  fireEvent.click(run)
  const article = await screen.findByRole('article', { name: 'Attachment review draft' })
  await waitFor(() => expect(within(article).getByRole('heading', { name: 'Attachment review draft' })).toHaveFocus())
  expect(fetch).toHaveBeenCalledOnce()
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/development/attachment-demo/draft')
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({})
  const table = within(article).getByRole('table')
  expect(within(table).getAllByText('Supplied candidate')).toHaveLength(2)
  expect(within(table).getByText('Supplied alternative')).toBeVisible()
  expect(within(table).getByText('Supplied no attachment')).toBeVisible()
  expect(within(table).getByText('Unknown', { exact: true })).toBeVisible()
  expect(within(table).getByText('Withheld', { exact: true })).toBeVisible()
  fireEvent.click(within(table).getByText('Details & provenance · row 1'))
  expect(within(table).getByText(/Supplied dimensions: 2.000 × 1.250 × 0.500 mm/)).toBeVisible()
  expect(within(table).getByText(/Supplied surface: DEMO_SURFACE_A/)).toBeVisible()
  expect(within(table).getByText(/Evidence: FINOVA-ATTACHMENTS-1:.*rows\/candidate-a/)).toBeVisible()
  expect(within(within(article).getByRole('region', { name: 'Clinician attachment review' })).getByText(/A01–A04 and R15 remain disabled/)).toBeVisible()
})
it('ordinary input only submits raw/context/receipt and never accepts demonstration authority', async () => {
  const { fetch, run } = panel(vi.fn().mockResolvedValue(ok(unverifiedJson)), false)
  fireEvent.click(run)
  const article = await screen.findByRole('article', { name: 'Attachment review draft' })
  expect(within(article).getByText(/Unverified input — attachment recommendations unavailable/)).toBeVisible()
  expect(within(article).queryByText('Supplied candidate', { exact: true })).not.toBeInTheDocument()
  const body = JSON.parse(fetch.mock.calls[0][1].body)
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/attachments/draft')
  expect(body).toEqual({ raw_text: input.parsed.raw_text, context: input.context, source_claim: 'Unknown', synthetic_data_confirmed: true })
  expect(body).not.toHaveProperty('test_only')
})
it('copies the exact full server export with all DRAFT and evidence context', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined); vi.stubGlobal('navigator', { clipboard: { writeText } })
  const { article, fetch } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy attachment DRAFT' }))
  expect(await screen.findByText(/Attachment DRAFT copied/)).toBeVisible()
  expect(writeText).toHaveBeenCalledWith(fixture.export_text)
  expect(fetch).toHaveBeenCalledOnce()
  expect(fixture.export_text).toContain('NOT_INDICATED; origin: SUPPLIED_SYNTHETIC')
})
it('keeps a usable draft after clipboard failure', async () => {
  vi.stubGlobal('navigator', { clipboard: { writeText: vi.fn().mockRejectedValue(new Error()) } })
  const { article } = await generated()
  fireEvent.click(within(article).getByRole('button', { name: 'Copy attachment DRAFT' }))
  expect(await screen.findByText(/Clipboard access is unavailable/)).toBeVisible()
  expect(article).toBeVisible()
})
it('downloads a local UTF-8 Blob and revokes its URL without another request', async () => {
  const create = vi.fn().mockReturnValue('blob:synthetic-attachment'), revoke = vi.fn()
  vi.stubGlobal('URL', { createObjectURL: create, revokeObjectURL: revoke })
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const { article, fetch } = await generated()
  vi.useFakeTimers()
  fireEvent.click(within(article).getByRole('button', { name: 'Download attachment DRAFT (TXT)' }))
  expect(create.mock.calls[0][0]).toBeInstanceOf(Blob)
  act(() => vi.runOnlyPendingTimers())
  expect(revoke).toHaveBeenCalledWith('blob:synthetic-attachment')
  expect(fetch).toHaveBeenCalledOnce()
})
it('shows loading, prevents duplicate requests and permits explicit retry after failure', async () => {
  let finish!: (v: unknown) => void
  const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
  const { run } = panel(fetch)
  fireEvent.click(run)
  expect(screen.getByRole('button', { name: 'Preparing attachment review…' })).toBeDisabled()
  fireEvent.click(run); expect(fetch).toHaveBeenCalledOnce()
  await act(async () => finish({ ok: false, status: 503 }))
  expect(await screen.findByRole('alert')).toHaveTextContent('original text is preserved')
  expect(run).toBeEnabled()
})
it.each(['input', 'context', 'consent', 'purpose'])('clears attachment output and demo authority after %s changes', async change => {
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockResolvedValueOnce(ok(fixture))
  vi.stubGlobal('fetch', fetch); render(<App />)
  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /MICRO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova attachment demo' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Run Attachment Review' }))
  await screen.findByRole('article', { name: 'Attachment review draft' })
  if (change === 'input') fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'changed synthetic' } })
  if (change === 'context') fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'other' } })
  if (change === 'consent') fireEvent.click(screen.getByRole('checkbox', { name: /I confirm/ }))
  if (change === 'purpose') fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /MACRO/ }))
  expect(screen.queryByRole('article', { name: 'Attachment review draft' })).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Copy attachment DRAFT' })).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})
it('suppresses a late demo response after purpose changes', async () => {
  let finish!: (v: unknown) => void
  const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
  vi.stubGlobal('fetch', fetch); render(<App />)
  const nav = screen.getByRole('navigation', { name: 'Review purpose' })
  fireEvent.click(within(nav).getByRole('button', { name: /MICRO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Load Finova attachment demo' }))
  fireEvent.click(within(nav).getByRole('button', { name: /MACRO/ }))
  expect(fetch.mock.calls[0][1].signal.aborted).toBe(true)
  await act(async () => finish(ok(input)))
  expect(screen.queryByRole('button', { name: 'Run Attachment Review' })).not.toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue('')
})
