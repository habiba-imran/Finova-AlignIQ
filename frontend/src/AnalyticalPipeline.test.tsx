import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import { isInteractiveReport } from './api/interactive'
import { buildPdfPresentation } from './pdf/presentation'
import { commentParagraphs } from './reviewPresentation'
import macro from '../../evidence/final-analysis-qa/macro.json'
import micro from '../../evidence/final-analysis-qa/micro.json'
import nano from '../../evidence/final-analysis-qa/nano.json'
import InteractiveWorkspace from './components/InteractiveWorkspace'
import type { InteractiveReport } from './api/interactive'
import type { AutomaticParseResult, ParseResult } from './api/parse'
import { EMPTY_CONTEXT } from './api/parse'
import { missingValuesParseLabel } from './api/parse'
import parseFixture from './test/fixtures/interactive-input.json'

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })

it.each([macro, micro, nano])('$module validates the actual analytical contract and keeps PDF/TXT findings identical', report => {
  expect(isInteractiveReport(report)).toBe(true)
  const presentation = buildPdfPresentation('interactive', report)
  for (const section of report.sections) {
    expect(report.export_text).toContain(section.text)
    expect(presentation.blocks).toContainEqual({ type: 'heading', text: section.title })
    for (const paragraph of commentParagraphs(section.text)) expect(presentation.blocks).toContainEqual({ type: 'text', text: paragraph })
  }
  expect(presentation.blocks.some(b => b.type === 'heading' && b.text === 'Source values')).toBe(false)
})

it.each([macro, micro, nano])('$module renders concise sections and reuses its cached result', async report => {
  const fetch = vi.fn().mockResolvedValueOnce(ok({ ...report.parsed, pipeline: parseFixture.pipeline })).mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  const nav = within(screen.getByRole('navigation', { name: 'Review purpose' }))
  fireEvent.click(nav.getByRole('button', { name: new RegExp(report.module.toUpperCase()) }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: report.parsed.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  const action = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }[report.module]!
  fireEvent.click(await screen.findByRole('button', { name: action }))
  const article = await screen.findByRole('article')
  for (const section of report.sections) {
    expect(within(article).getByRole('heading', { name: section.title })).toBeVisible()
    const card = within(article).getByRole('heading', { name: section.title }).closest('.comment-card') as HTMLElement
    for (const paragraph of commentParagraphs(section.text)) expect(within(card).getAllByText(paragraph, { exact: true })[0]).toBeVisible()
  }
  expect(within(article).getAllByRole('heading', { level: 6 })).toHaveLength(report.sections.length)
  expect(article).not.toHaveTextContent('original tooth token')
  fireEvent.click(nav.getByRole('button', { name: report.module === 'nano' ? /MACRO/ : /NANO/ }))
  fireEvent.click(nav.getByRole('button', { name: new RegExp(report.module.toUpperCase()) }))
  expect(screen.getByRole('article')).toBeVisible()
  expect(fetch).toHaveBeenCalledTimes(2)
}, 15000)

it('rejects promoted demo status, forged evidence, altered facts and missing sections', () => {
  const altered = structuredClone(micro)
  altered.sections[1].status = 'SOURCE_REPORTED'
  expect(isInteractiveReport(altered)).toBe(false)
  const ref = structuredClone(macro)
  ref.analytical_findings[0].selected_refs = ['M999999']
  expect(isInteractiveReport(ref)).toBe(false)
  const value = structuredClone(macro)
  value.sections[0].text = value.sections[0].text.replace('3.30', '99.99')
  expect(isInteractiveReport(value)).toBe(false)
  const missing = structuredClone(nano)
  missing.sections.pop()
  expect(isInteractiveReport(missing)).toBe(false)
})

it.each([true, false])('does not show empty source disclosures with sections=%s', sections => {
  const report = structuredClone(macro) as InteractiveReport
  report.observations = report.observations.map(o => ({ ...o, measurements: [] }))
  if (!sections) report.sections = []
  const parsed = { ...report.parsed, pipeline: parseFixture.pipeline } as AutomaticParseResult
  render(<InteractiveWorkspace module="macro" rawText={parsed.raw_text} context={EMPTY_CONTEXT} parsed={parsed}
    savedReport={report} onComplete={vi.fn()} />)
  expect(screen.queryByText('Source movement values', { exact: true })).not.toBeInTheDocument()
  expect(screen.queryByText('Source values', { exact: true })).not.toBeInTheDocument()
})

it('uses successful missing-value wording without changing parser status or hiding errors', () => {
  const result = structuredClone(macro.parsed) as unknown as ParseResult
  expect(missingValuesParseLabel(result)).toBe('Successfully parsed with 2 missing values')
  expect(result.status).toBe('PARTIAL')
  result.issues.push({ ...result.issues[0], severity: 'ERROR', code: 'UNIT_CONFLICT' })
  expect(missingValuesParseLabel(result)).toBeNull()
})
