import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import PlanningWorkspace from './components/PlanningWorkspace'
import AttachmentWorkspace from './components/AttachmentWorkspace'
import SequencingWorkspace from './components/SequencingWorkspace'
import planningInput from './test/fixtures/planning-demo-input.json'
import planningDraft from './test/fixtures/planning-demo-draft.json'
import attachmentInput from './test/fixtures/attachment-demo-input.json'
import attachmentDraft from './test/fixtures/attachment-demo-draft.json'
import sequencingInput from './test/fixtures/sequencer-demo-input.json'
import sequencingDraft from './test/fixtures/sequencer-demo-draft.json'
import type { DemoInput, PlanningDraft } from './api/planning'
import type { AttachmentDemoInput, AttachmentDraft } from './api/attachments'
import type { SequencingDemoInput } from './api/sequencing'

const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

it('Macro uses a prominent draft header, actual coverage counts and separate unavailable section', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(ok(planningDraft)))
  const input = planningInput as DemoInput
  render(<PlanningWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo onComplete={() => {}} />)
  fireEvent.change(screen.getByLabelText('Wording preference'), { target: { value: 'TEMPLATES' } })
  fireEvent.click(screen.getByRole('button', { name: 'Run Planning Assistant' }))
  const article = await screen.findByRole('article', { name: 'Planning Assistant draft' })
  const fixture = planningDraft as PlanningDraft
  expect(within(article).getByText('DRAFT · Prototype')).toBeVisible()
  expect(within(article).getByText('DRAFT — Requires Orthodontist Review')).toBeVisible()
  const summary = within(article).getByLabelText('Macro review summary')
  expect(within(summary).getByText('Eligible positions').parentElement).toHaveTextContent(String(fixture.report.engine_review.coverage.eligible_positions))
  expect(within(summary).getByText('Unavailable positions').parentElement).toHaveTextContent(String(fixture.report.engine_review.coverage.unavailable_positions))
  for (const dimension of ['Sagittal', 'Transverse', 'Vertical']) expect(within(article).getByRole('region', { name: `${dimension} review` })).toBeVisible()
  expect(within(article).getByRole('region', { name: 'Missing context and withheld assessments' })).toHaveTextContent('Inspect withheld assessments')
})

it('Micro keeps candidate, alternative, supplied-none, unknown and withheld states distinct in the main table', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(ok(attachmentDraft)))
  const input = attachmentInput as AttachmentDemoInput
  render(<AttachmentWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo onComplete={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: 'Run Attachment Review' }))
  const article = await screen.findByRole('article', { name: 'Attachment review draft' })
  const fixture = attachmentDraft as AttachmentDraft
  expect(within(article).getByText('DRAFT · Prototype')).toBeVisible()
  const summary = within(article).getByLabelText('Attachment review summary')
  expect(within(summary).getByText('Supplied candidates').parentElement).toHaveTextContent(String(fixture.entries.filter(e => e.result_type === 'CANDIDATE').length))
  const table = within(article).getByRole('table')
  expect(within(table).getAllByText('Supplied candidate')).toHaveLength(2)
  expect(within(table).getByText('Supplied alternative')).toBeVisible()
  expect(within(table).getByText('Supplied no attachment')).toBeVisible()
  expect(within(table).getByText('Unknown', { exact: true })).toBeVisible()
  expect(within(table).getByText('Withheld', { exact: true })).toBeVisible()
})

it('Nano separates supplied fictional notes from structural observations and arch/side sections', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(ok(sequencingDraft)))
  const input = sequencingInput as SequencingDemoInput
  render(<SequencingWorkspace rawText={input.parsed.raw_text} context={input.context} parsed={input.parsed} demo onComplete={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: 'Run Sequencing Review' }))
  const article = await screen.findByRole('article', { name: 'Sequencing review draft' })
  expect(within(article).getByText('SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE', { exact: true })).toBeVisible()
  expect(within(article).getByLabelText('Sequencing review summary')).toBeVisible()
  for (const title of ['Upper-arch sequencing', 'Lower-arch sequencing', 'Segments & tooth groups', 'Right-side anchorage', 'Left-side anchorage', 'Unavailable assessments']) expect(within(article).getByRole('region', { name: title })).toBeVisible()
  const upper = within(article).getByRole('region', { name: 'Upper-arch sequencing' })
  expect(within(upper).getByText('Supplied fictional statement')).toBeVisible()
  const unavailable = within(article).getByRole('region', { name: 'Unavailable assessments' })
  expect(within(unavailable).getByText('Structural metadata check · TEST_ONLY')).toBeVisible()
})
