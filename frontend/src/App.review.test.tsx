import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { EMPTY_CONTEXT } from './api/parse'
import { isDraftReview } from './api/review'
import parseFixture from './test/fixtures/synthetic-parse-result.json'
import draftFixture from './test/fixtures/synthetic-draft-review.json'

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers() })
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })

async function parsed(fetch = vi.fn().mockResolvedValueOnce(ok(parseFixture))) {
  vi.stubGlobal('fetch', fetch)
  render(<App />)
  const input = screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement
  fireEvent.change(input, { target: { value: parseFixture.raw_text } })
  fireEvent.click(screen.getByRole('checkbox'))
  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  await screen.findByRole('heading', { name: 'Structured lexical preview' })
  fireEvent.click(screen.getByText('Advanced: separate engineering review & legacy report actions'))
  return { fetch, input, button: screen.getByRole('button', { name: 'Create draft review' }) }
}

describe('Phase 2A explicit draft review', () => {
  it('shows static reparse guidance when recovery evidence expired', async () => {
    const { button, input } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce({ ok: false, status: 409 }))
    fireEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent('Choose Parse Table again')
    expect(input.value).toBe(parseFixture.raw_text)
  })
  it('sends unchanged raw input only after the separate review action and shows explicit unavailability', async () => {
    const { fetch, input, button } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(draftFixture)))
    expect(fetch).toHaveBeenCalledTimes(1)
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    expect(fetch).toHaveBeenCalledTimes(2)
    const [url, options] = fetch.mock.calls[1]
    expect(url).toBe('/api/v1/tmt/observations')
    expect(JSON.parse(options.body)).toEqual({ raw_text: parseFixture.raw_text, source_claim: 'Unknown', context: EMPTY_CONTEXT, synthetic_data_confirmed: true, requested_assessments: [] })
    expect(options).toMatchObject({ cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer' })
    expect(screen.getByText(/No authorized descriptive movement findings/)).toBeVisible()
    expect(screen.getByText(/Evidence domain: UNVERIFIED/)).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Unavailable assessments' })).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Limitations' })).toBeVisible()
    expect(input.value).toBe(parseFixture.raw_text)
    expect(screen.getByLabelText('Raw text preview').textContent).toBe(parseFixture.raw_text)
    expect(screen.getByRole('button', { name: 'Analyze' })).toBeDisabled()
  })

  it('shows loading, prevents duplicate requests, and offers no automatic retry', async () => {
    let finish!: (v: unknown) => void
    const fetch = vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockImplementationOnce(() => new Promise(resolve => { finish = resolve }))
    const { button } = await parsed(fetch)
    fireEvent.click(button)
    expect(screen.getByRole('button', { name: 'Creating draft…' })).toBeDisabled()
    fireEvent.click(button)
    expect(fetch).toHaveBeenCalledTimes(2)
    await act(async () => finish(ok(draftFixture)))
    expect(screen.getByRole('button', { name: 'Create draft review' })).toBeEnabled()
  })

  it.each([413, 422, 500])('sanitizes HTTP %s errors and retains parsing results', async status => {
    const { button, input } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce({ ok: false, status, json: async () => ({ detail: '<script>private</script>' }) }))
    fireEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent(/raw input and parse results are preserved/i)
    expect(screen.queryByText(/<script>private/)).not.toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
    expect(input.value).toBe(parseFixture.raw_text)
  })

  it('handles network failure and explicit retry', async () => {
    const { fetch, button } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockRejectedValueOnce(new Error('private network details')).mockResolvedValueOnce(ok(draftFixture)))
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(fetch).toHaveBeenCalledTimes(2)
    expect(screen.queryByText('private network details')).not.toBeInTheDocument()
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    expect(fetch).toHaveBeenCalledTimes(3)
  })

  it.each(['raw', 'version', 'context', 'clear', 'demo', 'consent'])('invalidates the report when %s changes', async change => {
    const { button, input } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(draftFixture)))
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    if (change === 'raw') fireEvent.change(input, { target: { value: '  changed\ttext\n\n' } })
    if (change === 'version') fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
    if (change === 'context') fireEvent.change(screen.getByLabelText('Tooth notation claim'), { target: { value: 'FDI' } })
    if (change === 'clear') fireEvent.click(screen.getByRole('button', { name: 'Clear' }))
    if (change === 'demo') fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    if (change === 'consent') fireEvent.click(screen.getByRole('checkbox'))
    expect(screen.queryByLabelText('Draft review results')).not.toBeInTheDocument()
  })

  it('aborts and ignores a late response after editing the source input', async () => {
    let finish!: (v: unknown) => void
    const fetch = vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockImplementationOnce(() => new Promise(resolve => { finish = resolve }))
    const { button, input } = await parsed(fetch)
    fireEvent.click(button)
    const signal = fetch.mock.calls[1][1].signal as AbortSignal
    fireEvent.change(input, { target: { value: 'new\ttext' } })
    expect(signal.aborted).toBe(true)
    await act(async () => finish(ok(draftFixture)))
    expect(screen.queryByLabelText('Draft review results')).not.toBeInTheDocument()
    expect(input.value).toBe('new\ttext')
  })

  it('invalidates results when the requested assessment changes and sends the explicit question', async () => {
    const { button, fetch } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(draftFixture))
      .mockResolvedValueOnce(ok({ ...draftFixture, requested_assessments: ['ATTACHMENTS'] })))
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    fireEvent.change(screen.getByLabelText(/Requested assessment/), { target: { value: 'ATTACHMENTS' } })
    expect(screen.queryByLabelText('Draft review results')).not.toBeInTheDocument()
    expect(fetch).toHaveBeenCalledTimes(2)
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    expect(JSON.parse(fetch.mock.calls[2][1].body).requested_assessments).toEqual(['ATTACHMENTS'])
  })

  it.each([
    { review_status: 'APPROVED' }, { clinical_analysis_enabled: true }, { raw_sha256: 'f'.repeat(64) },
    { findings: null }, { coverage: null }, { source: null }, { schema_version: 'future' },
  ])('rejects invalid or unsafe response boundaries %j', async override => {
    const { button } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok({ ...draftFixture, ...override })))
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(screen.queryByLabelText('Draft review results')).not.toBeInTheDocument()
  })

  it('renders a clearly TEST_ONLY structured observation with original values and evidence as inert text', async () => {
    const literal = '<script>window.testOnly=true</script>'
    const fixture = structuredClone(draftFixture)
    fixture.evidence_domain = 'TEST_ONLY'
    const f = fixture.findings.find(f => f.rule_id === 'D01')!
    Object.assign(f, { status: 'OBSERVED', finding_type: 'DESCRIPTIVE', evaluated: true, applicable: true, missing_required_fields: [], abstain_reason: null,
      message: 'Source-reported programmed value in the stated mode, basis and scope. Achieved movement is not assessed.',
      observed_measurements: [{ measurement_id: 'measurement-1', raw_tooth_identifier: '13', raw_label: 'Rotation (deg)', raw_value: literal,
        raw_number: '−1.2300', raw_sign: '−', raw_direction: 'M', signed_decimal: '-1.2300', magnitude: '1.2300', verification: 'TEST_ONLY',
        components: Object.entries({ tooth_identifier: 'TEST_TOOTH_A', axis: 'TEST_AXIS_A', unit: 'deg', direction: 'TEST_DIRECTION_A',
          source_application: 'TEST_ONLY', source_version: 'TEST_ONLY-1', notation: 'TEST_NOTATION', dentition: 'TEST_DENTITION', arch: 'TEST_ARCH', sign: 'TEST_SIGN_A',
          plan_mode: 'TEST_PLAN_MODE', reference_basis: 'TEST_REFERENCE_A', scope: 'TOTAL', coordinate_frame: 'TEST_FRAME_A' })
          .map(([name, canonical_value]) => ({ name, canonical_value, status: 'TEST_ONLY' })), input_refs: ['measurements/measurement-1'], source_spans: [{ line: 3, column_start: 4 }] }] })
    const storage = vi.spyOn(Storage.prototype, 'setItem')
    const { button } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(fixture)))
    fireEvent.click(button)
    const results = await screen.findByLabelText('Draft review results')
    expect(within(results).getByText(/TEST_TOOTH_A · TEST_AXIS_A · 1.2300 deg · TEST_DIRECTION_A/)).toBeVisible()
    expect(within(results).getByText(literal)).toBeVisible()
    expect(results.querySelector('script')).toBeNull()
    expect(storage).not.toHaveBeenCalled()
    storage.mockRestore()
  })

  it('bounds unavailable display and exposes the full in-memory JSON', async () => {
    const { button } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(draftFixture)))
    fireEvent.click(button)
    await screen.findByLabelText('Draft review results')
    expect(screen.getByRole('button', { name: /Show more unavailable assessments/ })).toBeVisible()
    fireEvent.click(screen.getByRole('button', { name: /Show more unavailable assessments/ }))
    expect(screen.getByLabelText('Full draft review JSON').textContent).toContain('2.0.0-phase2a')
  })

  it('times out review without clearing input or parser results', async () => {
    const { button, input } = await parsed(vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockImplementationOnce((_url, options) => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(new DOMException('aborted', 'AbortError')))
    })))
    vi.useFakeTimers()
    fireEvent.click(button)
    await act(async () => { await vi.advanceTimersByTimeAsync(20_000) })
    expect(screen.getByRole('alert')).toHaveTextContent('timed out')
    expect(input.value).toBe(parseFixture.raw_text)
    expect(screen.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  })

  it('accepts the real synthetic backend fixture and rejects malformed rendered measurements', () => {
    expect(isDraftReview(draftFixture)).toBe(true)
    const bad = structuredClone(draftFixture)
    Object.assign(bad.findings[0], { observed_measurements: [{ raw_value: null }] })
    expect(isDraftReview(bad)).toBe(false)
  })
})
