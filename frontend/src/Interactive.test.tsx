import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import { isInteractiveReport } from './api/interactive'
import type { DemoModule, InteractiveReport } from './api/interactive'
import input from './test/fixtures/interactive-input.json'
import macro from './test/fixtures/interactive-macro.json'
import micro from './test/fixtures/interactive-micro.json'
import nano from './test/fixtures/interactive-nano.json'

const fixtures = { macro, micro, nano }
const actions = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

it.each<DemoModule>(['macro', 'micro', 'nano'])('%s accepts factual source-only reports and marks simulations', module => {
  expect(isInteractiveReport(fixtures[module])).toBe(true)
  expect(fixtures[module].observations.reduce((count, o) => count + o.measurements.length, 0)).toBe(12)
  expect(fixtures[module].engine_review.evaluations).toHaveLength(96)
})

it.each(['clinical', 'value', 'direction', 'missing', 'duplicate', 'illustration', 'hash', 'origin', 'provider'])('rejects unsafe or inconsistent %s response', change => {
  const value = structuredClone(micro) as unknown as InteractiveReport
  if (change === 'clinical') Object.assign(value, { clinical_analysis_enabled: true })
  if (change === 'value') value.observations[0].measurements[0].signed_decimal = '999'
  if (change === 'direction') value.observations[0].measurements[0].raw_direction = 'INVENTED'
  if (change === 'missing') value.observations[0].measurements.pop()
  if (change === 'duplicate') value.observations.push(value.observations[0])
  if (change === 'illustration') Object.assign(value.illustrations[0], { clinical_status: 'APPROVED' })
  if (change === 'hash') value.parsed.raw_sha256 = '0'.repeat(64)
  if (change === 'origin') Object.assign(value.illustrations[0], { origin: 'CLINICALLY_CALCULATED' })
  if (change === 'provider') Object.assign(value.generation, { used_mode: 'GROQ_AI', attempts: 0, accepted_comments: 4 })
  expect(isInteractiveReport(value)).toBe(false)
})

async function start(module: DemoModule, report: unknown = fixtures[module]) {
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  if (module !== 'macro') fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: new RegExp(module.toUpperCase()) }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: input.raw_text } })
  expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  fireEvent.click(await screen.findByRole('button', { name: actions[module] }))
  return { fetch, article: await screen.findByRole('article', { name: 'Generated synthetic report' }) }
}

it.each<DemoModule>(['macro', 'micro', 'nano'])('%s runs arbitrary input through the main UI without a fixed loader or AI selector', async module => {
  const { fetch, article } = await start(module)
  expect(fetch).toHaveBeenCalledTimes(2)
  expect(fetch.mock.calls[1][0]).toBe('/api/v1/interactive/review')
  const body = JSON.parse(fetch.mock.calls[1][1].body)
  expect(body).toMatchObject({ module, raw_text: input.raw_text, raw_sha256: input.raw_sha256, synthetic_data_confirmed: true })
  expect(body.comment_mode).toBeUndefined()
  expect(screen.queryByLabelText('Wording preference')).not.toBeInTheDocument()
  expect(within(article).getByLabelText('Factual tooth-wise observations')).toHaveTextContent('1.2300 D')
  expect(article).toHaveTextContent('Standard wording')
  expect(article).not.toHaveTextContent(/GROQ_|SEMANTICS_|R13|rule ledger|finding_id|raw_sha256/)
  expect(within(article).queryByLabelText('Illustrative demo content') !== null).toBe(module !== 'macro')
  for (const name of ['Copy', 'Export TXT', 'Export PDF']) expect(within(article).getByRole('button', { name })).toBeEnabled()
})

it.each<DemoModule>(['macro', 'micro', 'nano'])('%s shows approved automatic AI wording with one review request', async module => {
  const ai = structuredClone(fixtures[module])
  Object.assign(ai.generation, { used_mode: 'GROQ_AI', provider: 'GROQ', model: 'openai/gpt-oss-120b', attempts: 1, accepted_comments: 4, reason: 'GROQ_VALIDATED' })
  ai.wording_notice = 'AI-assisted wording generated with Groq; all measurements and examples assembled locally.'
  const { fetch, article } = await start(module, ai)
  expect(article).toHaveTextContent('AI-assisted wording')
  expect(article).not.toHaveTextContent('Groq')
  expect(fetch).toHaveBeenCalledTimes(2)
  expect(screen.queryByRole('group', { name: 'Report wording views' })).not.toBeInTheDocument()
})

it.each<DemoModule>(['macro', 'micro', 'nano'])('%s puts grounded paragraphs in the main report without provider or transmission details', async module => {
  const { article } = await start(module)
  expect(within(article).getByRole('heading', { name: module === 'macro' ? 'Planning comments' : module === 'micro' ? 'Attachment review comments' : 'Sequencing review comments' })).toBeVisible()
  expect(article).toHaveTextContent('The programmed movement record lists')
  expect(article).not.toHaveTextContent(/Groq|provider|transmission|shared with/i)
  const source = within(article).getAllByText('Source values')[0].closest('details')!
  expect(source).not.toHaveAttribute('open')
  fireEvent.click(within(source).getByText('Source values'))
  expect(within(source).getByText(/Rotation \(deg\)/)).toBeVisible()
})

it('rejects a grounded report with mismatched comment counts or inconsistent provenance', () => {
  const bad = structuredClone(macro) as InteractiveReport
  bad.generation.eligible_wording_findings++
  expect(isInteractiveReport(bad)).toBe(false)
  const promoted = structuredClone(micro) as InteractiveReport
  promoted.generation.accepted_comments = 1
  expect(isInteractiveReport(promoted)).toBe(false)
})

it('copies the exact full report and invalidates exports after editing', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined)
  vi.stubGlobal('navigator', { clipboard: { writeText } })
  const { article } = await start('micro')
  fireEvent.click(within(article).getByRole('button', { name: 'Copy' }))
  expect(writeText).toHaveBeenCalledWith(micro.export_text)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'edited' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Export PDF' })).not.toBeInTheDocument()
})

it('preserves parsed input when switching modules and removes the previous report', async () => {
  const { fetch } = await start('macro')
  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /MICRO/ }))
  expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(input.raw_text)
  expect(screen.getByRole('button', { name: actions.micro })).toBeEnabled()
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('aborts and suppresses a stale review after editing', async () => {
  let finish!: (value: unknown) => void
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockImplementationOnce(() => new Promise(resolve => { finish = resolve }))
  vi.stubGlobal('fetch', fetch); render(<App />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: input.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  fireEvent.click(await screen.findByRole('button', { name: actions.macro }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'edited' } })
  expect(fetch.mock.calls[1][1].signal.aborted).toBe(true)
  await act(async () => finish(ok(macro)))
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
})
