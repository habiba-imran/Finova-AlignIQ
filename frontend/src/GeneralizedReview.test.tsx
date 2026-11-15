import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { useState } from 'react'
import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import { emptyReviewDetails, isInteractiveReport } from './api/interactive'
import type { DemoModule, InteractiveReport } from './api/interactive'
import { defaultPlanningOptions } from './api/planningOptions'
import type { PlanningOptions } from './api/planningOptions'
import { buildPdfPresentation } from './pdf/presentation'
import PlanningContextPanel from './components/PlanningContextPanel'
import parserFixture from './test/fixtures/interactive-input.json'

const modules: DemoModule[] = ['macro', 'micro', 'nano']
const samples = ['A', 'B', 'C', 'D'].flatMap(caseId => modules.map(module => ({ caseId, module,
  report: JSON.parse(readFileSync(resolve(process.cwd(), `../evidence/generalized-planning/${caseId}-${module}.json`), 'utf8')) as InteractiveReport })))
const actions = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })
const parsed = (report: InteractiveReport) => ({ ...report.parsed, pipeline: parserFixture.pipeline })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

it.each(samples)('$caseId/$module validates a source-driven report and preserves all findings in PDF/TXT', ({ report }) => {
  expect(isInteractiveReport(report)).toBe(true)
  expect(report.planning_context?.origin).toBe('INPUT_DRIVEN_POLICY_REVIEW')
  expect(report.planning_context?.scenario_id).toBeNull()
  const visible = buildPdfPresentation('interactive', report).blocks.flatMap(b => b.type === 'table' ? b.rows.flat() : [b.text]).join(' ')
  for (const finding of report.analytical_findings!) {
    expect(report.export_text).toContain(finding.text)
    expect(visible).toContain(finding.text)
  }
  expect(report.functional_plan?.stages).toHaveLength(0)
})

it.each(samples)('$caseId/$module generates directly from pasted input without loading an example', async ({ module, report }) => {
  const fetch = vi.fn().mockResolvedValueOnce(ok(parsed(report))).mockResolvedValueOnce(ok(report))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: report.parsed.raw_text } })
  expect(fetch).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  await screen.findByRole('region', { name: 'Structured TMT table' })
  fireEvent.click(screen.getByRole('button', { name: new RegExp(module.toUpperCase()) }))
  fireEvent.click(await screen.findByRole('button', { name: actions[module] }))
  const article = await screen.findByRole('article')
  expect(screen.queryByLabelText('Loaded synthetic example')).not.toBeInTheDocument()
  expect(article).not.toHaveTextContent('Explicit fictional scenario')
  const body = JSON.parse(fetch.mock.calls[1][1].body)
  expect(body.planning_context).toBeUndefined()
  expect(body.planning_options).toEqual(defaultPlanningOptions())
  expect(body.raw_text).toBe(report.parsed.raw_text)
  if (module === 'macro') expect(article).toHaveTextContent('Technician review:')
  if (module === 'micro') expect(within(article).getByRole('table')).toBeVisible()
  if (module === 'nano') expect(article).toHaveTextContent('Inspection topics, not treatment stages')
}, 15000)

it('editing optional context invalidates a result; a new table starts with clean module options', async () => {
  const a = samples.find(s => s.caseId === 'A' && s.module === 'macro')!.report
  const b = samples.find(s => s.caseId === 'B' && s.module === 'macro')!.report
  const fetch = vi.fn().mockResolvedValueOnce(ok(parsed(a))).mockResolvedValueOnce(ok(a)).mockResolvedValueOnce(ok(parsed(b))).mockResolvedValueOnce(ok(b))
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  const input = screen.getByRole('textbox', { name: 'Raw TMT text' })
  fireEvent.change(input, { target: { value: a.parsed.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  fireEvent.click(await screen.findByRole('button', { name: actions.macro }))
  await screen.findByRole('article')
  fireEvent.click(screen.getByText(/Planning context/, { selector: 'summary' }))
  fireEvent.change(screen.getByLabelText('Planning objective'), { target: { value: 'ANGULAR_CONTROL' } })
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
  expect(screen.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  fireEvent.click(screen.getByRole('button', { name: /MICRO/ }))
  fireEvent.click(screen.getByText(/Planning context/, { selector: 'summary' }))
  expect(screen.getByLabelText('Policy mode')).toHaveValue('SYNTHETIC_REVIEW')
  fireEvent.change(input, { target: { value: b.parsed.raw_text } })
  fireEvent.click(screen.getByRole('button', { name: /MACRO/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  fireEvent.click(await screen.findByRole('button', { name: actions.macro }))
  await screen.findByRole('article')
  expect(JSON.parse(fetch.mock.calls[3][1].body).planning_options).toEqual(defaultPlanningOptions())
}, 15000)

it('stage entry never fills source totals into stage amounts', () => {
  const sample = samples.find(s => s.caseId === 'C' && s.module === 'nano')!.report
  let current = emptyReviewDetails()
  function Harness() {
    const [options, setOptions] = useState(defaultPlanningOptions)
    const [details, setDetails] = useState(emptyReviewDetails)
    return <PlanningContextPanel module="nano" parsed={sample.parsed} options={options} details={details} onChange={(o, d) => { current = d; setOptions(o); setDetails(d) }} />
  }
  render(<Harness />)
  fireEvent.click(screen.getByText(/Planning context/, { selector: 'summary' }))
  fireEvent.click(screen.getByRole('button', { name: 'Add supplied stage' }))
  expect(current.allocations).toHaveLength(0)
  fireEvent.click(screen.getByRole('button', { name: 'Add supplied movement' }))
  expect(current.allocations[0].amount).toBeNull()
  expect(current.allocations[0].measurement_ref).toBe('')
  fireEvent.change(screen.getByLabelText('Movement 1 source'), { target: { value: sample.parsed.measurements[0].id } })
  expect(current.allocations[0].amount).toBeNull()
  fireEvent.change(screen.getByLabelText(/Movement 1 supplied amount/), { target: { value: '0.625' } })
  expect(current.allocations[0].amount).toBe('0.625')
})

it('catalog geometry is applied only after explicit complete input', () => {
  const sample = samples.find(s => s.caseId === 'B' && s.module === 'micro')!.report
  let current: PlanningOptions = defaultPlanningOptions()
  function Harness() {
    const [options, setOptions] = useState(defaultPlanningOptions)
    return <PlanningContextPanel module="micro" parsed={sample.parsed} options={options} details={emptyReviewDetails()} onChange={o => { current = o; setOptions(o) }} />
  }
  render(<Harness />)
  fireEvent.click(screen.getByText(/Planning context/, { selector: 'summary' }))
  fireEvent.click(screen.getByText('Supplied catalog specifications'))
  expect(current.attachment_options).toHaveLength(0)
  fireEvent.change(screen.getByLabelText('Width (mm)'), { target: { value: '1.234' } })
  fireEvent.click(screen.getByRole('button', { name: 'Apply catalog specification' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Supply all three positive dimensions')
  expect(current.attachment_options).toHaveLength(0)
  fireEvent.change(screen.getByLabelText('Height (mm)'), { target: { value: '2.345' } })
  fireEvent.change(screen.getByLabelText('Depth (mm)'), { target: { value: '0.456' } })
  fireEvent.click(screen.getByRole('button', { name: 'Apply catalog specification' }))
  expect(current.attachment_options[0].geometry).toEqual({ width_mm: '1.234', height_mm: '2.345', depth_mm: '0.456' })
  expect(current.attachment_options[0].placement).toBeNull()
})

it.each(['origin', 'outline', 'options', 'authority'])('rejects forged generalized %s metadata', change => {
  const report = structuredClone(samples.find(s => s.caseId === 'C' && s.module === 'nano')!.report)
  if (change === 'origin') report.planning_context!.scenario_id = 'pretend-example'
  if (change === 'outline') (report.functional_plan!.review_outline![0] as unknown as Record<string, unknown>).stage_allocations_generated = true
  if (change === 'options') report.planning_options!.source_sha256 = '0'.repeat(64)
  if (change === 'authority') (report.functional_plan as unknown as Record<string, unknown>).clinical_authorized = true
  expect(isInteractiveReport(report)).toBe(false)
})
