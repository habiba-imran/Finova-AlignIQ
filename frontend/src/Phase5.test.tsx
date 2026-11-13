import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import { isDraftReview } from './api/review'
import { EMPTY_CONTEXT } from './api/parse'
import DraftReviewPanel from './components/DraftReviewPanel'
import modern from './test/fixtures/synthetic-phase5-review.json'
import legacy from './test/fixtures/synthetic-draft-review.json'
import lexical from './test/fixtures/synthetic-parse-result.json'

afterEach(() => vi.unstubAllGlobals())

it('accepts real Phase 5 responses and historical Phase 2A responses', () => {
  expect(isDraftReview(modern)).toBe(true)
  expect(isDraftReview(legacy)).toBe(true)
  expect(modern.evaluations).toHaveLength(96)
})

it.each(['approval', 'execution', 'missing', 'duplicate', 'version', 'prerequisites'])('rejects unsafe or malformed %s ledger information', kind => {
  const bad = structuredClone(modern)
  if (kind === 'approval') bad.evaluations[0].approval_status = 'APPROVED'
  if (kind === 'execution') {
    const disabled = bad.evaluations.find(e => e.rule_id === 'R01')!
    disabled.evaluated = true
  }
  if (kind === 'missing') bad.evaluations.pop()
  if (kind === 'duplicate') bad.evaluations[1] = bad.evaluations[0]
  if (kind === 'version') bad.engine_version = '0.2.0'
  if (kind === 'prerequisites') Object.assign(bad.evaluations[0], { missing_required_fields: [{}] })
  expect(isDraftReview(bad)).toBe(false)
})

it('shows the 96-rule ledger, unavailability and draft boundary without changing raw input', async () => {
  const fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => modern })
  vi.stubGlobal('fetch', fetch)
  render(<DraftReviewPanel rawText={lexical.raw_text} source="Unknown" context={EMPTY_CONTEXT} rawHash={modern.raw_sha256} />)
  fireEvent.click(screen.getByRole('button', { name: 'Create draft review' }))
  const result = await screen.findByLabelText('Draft review results')
  expect(within(result).getByText('DRAFT — Requires Orthodontist Review')).toBeVisible()
  expect(within(result).getByText(/Unavailable or disabled rules do not indicate a normal result/)).toBeVisible()
  expect(within(result).getByText(/No authorized descriptive movement findings/)).toBeVisible()
  const ledger = within(result).getByText('Rule evaluation ledger (96 rules)')
  fireEvent.click(ledger)
  expect(within(result).getByText('R01 · DISABLED')).toBeVisible()
  expect(within(result).getByText('D16 · CONTEXT_REQUIRED')).toBeVisible()
  const request = JSON.parse(fetch.mock.calls[0][1].body)
  expect(request.raw_text).toBe(lexical.raw_text)
  expect(request).not.toHaveProperty('test_context')
  expect(request).not.toHaveProperty('test_only')
})
