import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import { isInteractiveReport } from './api/interactive'
import input from './test/fixtures/interactive-input.json'
import micro from './test/fixtures/interactive-micro.json'
import nano from './test/fixtures/interactive-nano.json'
import suppliedMicro from './test/fixtures/interactive-micro-supplied.json'
import suppliedNano from './test/fixtures/interactive-nano-supplied.json'

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })

async function prepare(module: 'micro' | 'nano', report: unknown) {
  const fetch = vi.fn().mockResolvedValueOnce(ok(input)).mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: new RegExp(module.toUpperCase()) }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: input.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  await screen.findByRole('button', { name: module === 'micro' ? 'Run Attachment Review' : 'Run Sequencing Review' })
  return fetch
}

it.each([['micro', micro], ['nano', nano]] as const)('%s shows distinct unavailable findings without repeating movement paragraphs', async (module, report) => {
  const fetch = await prepare(module, report)
  fireEvent.click(screen.getByRole('button', { name: module === 'micro' ? 'Run Attachment Review' : 'Run Sequencing Review' }))
  const article = await screen.findByRole('article')
  const comments = within(article).getByLabelText('Module review comments')
  expect(within(comments).getAllByRole('heading', { level: 6 })).toHaveLength(4)
  expect(comments).not.toHaveTextContent('-2.7500')
  expect(within(comments).getAllByText('Unavailable', { exact: true })).toHaveLength(4)
  expect(comments).toHaveTextContent(module === 'micro' ? 'Supplied attachment choices' : 'Supplied movement allocations')
  expect(article).not.toHaveTextContent(/Illustrative|Groq|provider/i)
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('Micro submits exact supplied design values, keeps them unverified and invalidates the report when edited', async () => {
  const fetch = await prepare('micro', suppliedMicro)
  fireEvent.click(screen.getByText('Add supplied attachment details (optional)'))
  fireEvent.click(screen.getByRole('button', { name: 'Add attachment record' }))
  const row = suppliedMicro.review_details.attachments[0]
  fireEvent.change(screen.getByLabelText('Attachment 1 tooth'), { target: { value: row.tooth_ref } })
  fireEvent.change(screen.getByLabelText('Attachment 1 choice'), { target: { value: 'ATTACHMENT' } })
  for (const [name, value] of [['design', row.design], ['width (mm)', row.width_mm], ['height (mm)', row.height_mm], ['depth (mm)', row.depth_mm], ['surface', row.surface], ['orientation', row.orientation]]) {
    fireEvent.change(screen.getByLabelText('Attachment 1 ' + name), { target: { value } })
  }
  expect(fetch).toHaveBeenCalledTimes(1)
  fireEvent.click(screen.getByRole('button', { name: 'Run Attachment Review' }))
  const article = await screen.findByRole('article')
  expect(article).toHaveTextContent('1.2300 mm')
  expect(article).toHaveTextContent('Supplied · unverified')
  expect(article).toHaveTextContent('Independent attachment indication')
  expect(JSON.parse(fetch.mock.calls[1][1].body).review_details).toEqual(suppliedMicro.review_details)
  fireEvent.change(screen.getByLabelText('Attachment 1 width (mm)'), { target: { value: '1.5000' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Export PDF' })).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('Nano submits explicit stage amounts and notes instead of allocating TMT values automatically', async () => {
  const fetch = await prepare('nano', suppliedNano)
  fireEvent.click(screen.getByText('Add supplied sequencing details (optional)'))
  fireEvent.click(screen.getByRole('button', { name: 'Add stage record' }))
  const stage = suppliedNano.review_details.stages[0], allocation = suppliedNano.review_details.allocations[0], note = suppliedNano.review_details.anchorage_notes[0]
  fireEvent.change(screen.getByLabelText('Stage 1 ID'), { target: { value: stage.stage_id } })
  fireEvent.change(screen.getByLabelText('Stage 1 order'), { target: { value: String(stage.order) } })
  fireEvent.change(screen.getByLabelText('Stage 1 duration (days)'), { target: { value: String(stage.duration_days) } })
  fireEvent.click(screen.getByRole('button', { name: 'Add movement allocation' }))
  fireEvent.change(screen.getByLabelText('Allocation 1 stage'), { target: { value: allocation.stage_id } })
  fireEvent.change(screen.getByLabelText('Allocation 1 tooth'), { target: { value: allocation.tooth_ref } })
  fireEvent.change(screen.getByLabelText('Allocation 1 movement'), { target: { value: allocation.measurement_ref } })
  expect(screen.getByLabelText('Allocation 1 stage amount')).toHaveValue('')
  fireEvent.change(screen.getByLabelText('Allocation 1 stage amount'), { target: { value: allocation.amount } })
  fireEvent.click(screen.getByRole('button', { name: 'Add anchorage note' }))
  fireEvent.change(screen.getByLabelText('Anchorage 1 scope'), { target: { value: note.tooth_ref } })
  fireEvent.change(screen.getByLabelText('Anchorage 1 supplied note'), { target: { value: note.note } })
  fireEvent.click(screen.getByRole('button', { name: 'Run Sequencing Review' }))
  const article = await screen.findByRole('article')
  expect(article).toHaveTextContent('0.1250 mm')
  expect(article).toHaveTextContent(note.note)
  expect(JSON.parse(fetch.mock.calls[1][1].body).review_details).toEqual(suppliedNano.review_details)
})

it('invalid optional stage fields produce a focused, understandable error before a review call', async () => {
  const fetch = await prepare('nano', nano)
  fireEvent.click(screen.getByText('Add supplied sequencing details (optional)'))
  fireEvent.click(screen.getByRole('button', { name: 'Add stage record' }))
  fireEvent.click(screen.getByRole('button', { name: 'Run Sequencing Review' }))
  const alert = await screen.findByRole('alert')
  expect(alert).toHaveTextContent('Stage IDs and positive whole-number orders are required')
  expect(alert).toHaveFocus()
  expect(fetch).toHaveBeenCalledTimes(1)
})

it('rejects a forged module source reference or promoted clinical status', () => {
  const forged = structuredClone(suppliedNano)
  forged.sections[0].source_refs = ['review_details/stages/99']
  expect(isInteractiveReport(forged)).toBe(false)
  Object.assign(forged.sections[0], { source_refs: [], status: 'APPROVED' })
  expect(isInteractiveReport(forged)).toBe(false)
})

it('keeps an unchanged completed report in memory across module navigation without another request', async () => {
  const fetch = await prepare('micro', micro)
  fireEvent.click(screen.getByRole('button', { name: 'Run Attachment Review' }))
  await screen.findByRole('article')
  const nav = within(screen.getByRole('navigation', { name: 'Review purpose' }))
  fireEvent.click(nav.getByRole('button', { name: /NANO/ }))
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  fireEvent.click(nav.getByRole('button', { name: /MICRO/ }))
  expect(screen.getByRole('article')).toHaveTextContent('Supplied attachment choices')
  expect(fetch).toHaveBeenCalledTimes(2)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'changed source' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
})
