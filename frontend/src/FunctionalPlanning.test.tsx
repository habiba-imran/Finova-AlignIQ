import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import { isInteractiveReport } from './api/interactive'
import { buildPdfPresentation } from './pdf/presentation'
import { commentParagraphs } from './reviewPresentation'
import macro from '../../evidence/functional-planning/macro.json'
import micro from '../../evidence/functional-planning/micro.json'
import nano from '../../evidence/functional-planning/nano.json'
import macroInput from '../../evidence/functional-planning/macro-input.json'
import microInput from '../../evidence/functional-planning/micro-input.json'
import nanoInput from '../../evidence/functional-planning/nano-input.json'
import parserFixture from './test/fixtures/interactive-input.json'
import unifiedMacro from '../../evidence/unified-synthetic-example/macro.json'
import unifiedMicro from '../../evidence/unified-synthetic-example/micro.json'
import unifiedNano from '../../evidence/unified-synthetic-example/nano.json'
import unifiedExample from '../../examples/functional-all-in-one.json'

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })
const cases = [[macro, macroInput], [micro, microInput], [nano, nanoInput]] as const

it.each(cases)('$0.module validates structured decisions and retains every finding in TXT/PDF', (report) => {
  expect(isInteractiveReport(report)).toBe(true)
  const pdf = buildPdfPresentation('interactive', report)
  const visible = pdf.blocks.flatMap(b => b.type === 'text' || b.type === 'heading' ? [b.text] : b.rows.flat()).join(' ')
  for (const section of report.sections) {
    expect(report.export_text).toContain(section.text)
    for (const paragraph of commentParagraphs(section.text)) expect(visible).toContain(paragraph)
  }
  expect(report.functional_plan.clinical_authorized).toBe(false)
})

it.each([unifiedMacro, unifiedMicro, unifiedNano])('$module uses the single shared example and exposes module-specific details', async (report) => {
  const input = unifiedExample.modules[report.module as keyof typeof unifiedExample.modules]
  const fetch = vi.fn().mockResolvedValueOnce(ok({ ...report.parsed, pipeline: parserFixture.pipeline })).mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: new RegExp(report.module.toUpperCase()) }))
  fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
  expect(fetch).not.toHaveBeenCalled()
  expect(screen.queryByText('Optional fictional planning scenarios')).not.toBeInTheDocument()
  expect(screen.getByLabelText('Loaded synthetic example')).toBeVisible()
  expect((screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement).value).toBe(input.raw_text)
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  fireEvent.click(await screen.findByRole('button', { name: { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }[report.module]! }))
  const article = await screen.findByRole('article')
  expect(article).toHaveTextContent('Explicit fictional scenario')
  expect(fetch).toHaveBeenCalledTimes(2)
  expect(JSON.parse(fetch.mock.calls[1][1].body).planning_context).toEqual(input.planning_context)
  if (report.module === 'macro') expect(article).toHaveTextContent('change mesiodistal from 3.10 mm')
  if (report.module === 'micro') {
    const table = within(article).getByRole('table')
    expect(table).toHaveTextContent('Vertical rectangular')
    expect(within(table).getAllByRole('row')).toHaveLength(16)
    fireEvent.click(within(article).getByText('Tooth 11 details'))
    expect(within(within(article).getByText('Tooth 11 details').parentElement!).getByText(/Fictional supplied dimensions: 2.000 × 3.000 × 1.000 mm/)).toBeVisible()
    expect(within(article).getAllByText('No supported candidate')).toHaveLength(1)
  }
  if (report.module === 'nano') {
    expect(article).toHaveTextContent('Remaining supplied movements · S3 · supplied order 3')
    fireEvent.click(within(article).getByText('Stage S1 movements and assumptions'))
    expect(article).toHaveTextContent('Tooth 11: 1.00 mm')
    fireEvent.click(within(article).getByText('Stage-to-total consistency'))
    expect(article).toHaveTextContent('3.10')
  }
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: input.raw_text + '\n' } })
  expect(screen.queryByLabelText('Loaded synthetic example')).not.toBeInTheDocument()
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
}, 15000)

it('loads once, shares the parse across tabs, and clears all example context on settings edits', async () => {
  const reports = [unifiedMacro, unifiedMicro, unifiedNano]
  const fetch = vi.fn().mockResolvedValueOnce(ok({ ...unifiedMacro.parsed, pipeline: parserFixture.pipeline }))
  for (const report of reports) fetch.mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  for (const report of reports) {
    fireEvent.click(screen.getByRole('button', { name: new RegExp(report.module.toUpperCase()) }))
    fireEvent.click(await screen.findByRole('button', { name: { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }[report.module]! }))
    await screen.findByRole('article')
    expect(screen.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(unifiedExample.raw_text)
  }
  expect(fetch).toHaveBeenCalledTimes(4)
  for (let i = 0; i < 3; i++) {
    const request = JSON.parse(fetch.mock.calls[i + 1][1].body)
    expect(request.module).toBe(reports[i].module)
    expect(request.planning_context.source_sha256).toBe(unifiedMacro.parsed.raw_sha256)
    expect(request.planning_context.module).toBe(reports[i].module)
  }
  fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
  expect(screen.queryByLabelText('Loaded synthetic example')).not.toBeInTheDocument()
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: /MACRO/ }))
  expect(screen.queryByLabelText('Loaded synthetic example')).not.toBeInTheDocument()
}, 15000)

it.each(['source', 'authority', 'candidate', 'target', 'stage', 'wording', 'legacy'])('rejects a forged functional %s result', change => {
  const report = structuredClone(change === 'stage' ? nano : change === 'target' ? macro : micro) as unknown as Record<string, any>
  if (change === 'source') report.planning_context.source_sha256 = '0'.repeat(64)
  if (change === 'authority') report.functional_plan.clinical_authorized = true
  if (change === 'candidate') report.functional_plan.attachment_rows[0].primary = 'OVAL'
  if (change === 'target') report.functional_plan.decisions[0].proposed_changes[0].amount = '999'
  if (change === 'stage') report.functional_plan.stages[0].movements[0].amount = '999'
  if (change === 'wording') report.sections[0].text += ' Clinically approved.'
  if (change === 'legacy') report.report_format = 'MODULE_SPECIFIC_V1'
  expect(isInteractiveReport(report)).toBe(false)
})
