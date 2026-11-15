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

it.each([['micro', micro], ['nano', nano]] as const)('%s generates TMT comments without extra forms', async (module, report) => {
  const fetch = await prepare(module, report)
  fireEvent.click(screen.getByRole('button', { name: module === 'micro' ? 'Run Attachment Review' : 'Run Sequencing Review' }))
  const article = await screen.findByRole('article')
  const comments = within(article).getByLabelText('Module review comments')
  expect(within(comments).getAllByRole('heading', { level: 6 })).toHaveLength(4)
  expect(comments).toHaveTextContent(module === 'micro' ? '-2.7500' : '1.2300')
  expect(within(comments).getAllByText('From TMT · unverified', { exact: true }).length).toBeGreaterThanOrEqual(2)
  expect(comments).toHaveTextContent(module === 'micro' ? 'Rotation review' : 'Translation review')
  expect(screen.queryByLabelText('Supplied review details')).not.toBeInTheDocument()
  expect(comments).not.toHaveTextContent(/because no|no supplied|Information needed/)
  expect(article).not.toHaveTextContent(/Illustrative|Groq|provider/i)
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('retains validation of older supplied-detail exports', () => {
  expect(isInteractiveReport(suppliedMicro)).toBe(true)
  expect(isInteractiveReport(suppliedNano)).toBe(true)
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
  expect(screen.getByRole('article')).toHaveTextContent('Rotation review')
  expect(fetch).toHaveBeenCalledTimes(2)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: 'changed source' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
})
