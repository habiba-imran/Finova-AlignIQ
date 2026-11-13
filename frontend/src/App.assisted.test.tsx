import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { isAutomaticParseResult } from './api/parse'
import fixture from './test/fixtures/synthetic-phase4-recovery.json'
import example from './phase4Example.json'
import review from './test/fixtures/synthetic-draft-review.json'

const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })
afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers() })
function setup(fetch = vi.fn().mockResolvedValue(ok(fixture))) {
  vi.stubGlobal('fetch', fetch); render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Load generated recovery example' }))
  const input = screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement
  fireEvent.click(screen.getByRole('checkbox', { name: /I confirm/ }))
  return { fetch, input, button: screen.getByRole('button', { name: 'Parse Table' }) }
}
describe('Phase 4 automatic structural recovery', () => {
  it('does not transmit on loading or confirming and has no second permission action', () => {
    const { fetch, input } = setup()
    expect(input.value).toBe(example.raw_text)
    expect(fetch).not.toHaveBeenCalled()
    expect(screen.queryByRole('checkbox', { name: /I consent/ })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Try AI-assisted parsing' })).not.toBeInTheDocument()
  })
  it('uses one Parse Table request with generator identity and displays automatic recovery', async () => {
    const { fetch, input, button } = setup(); fireEvent.click(button)
    await screen.findByText(/AI-assisted structure recovery/)
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(fetch.mock.calls[0][0]).toBe('/api/v1/tmt/parse')
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toMatchObject({ raw_text: example.raw_text, synthetic_fixture: example.identity })
    expect(JSON.parse(fetch.mock.calls[0][1].body)).not.toHaveProperty('cloud_synthetic_consent')
    expect(screen.getByText(/Recovered original-text associations are rechecked/)).toBeVisible()
    expect(input.value).toBe(example.raw_text)
    expect(screen.getByLabelText('Raw text preview').textContent).toBe(example.raw_text)
  })
  it('keeps loading bounded and prevents duplicate parse actions', async () => {
    let finish!: (x: unknown) => void
    const { fetch, button } = setup(vi.fn().mockImplementation(() => new Promise(r => { finish = r })))
    fireEvent.click(button); fireEvent.click(button)
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(screen.getByRole('button', { name: 'Parsing…' })).toBeDisabled()
    await act(async () => finish(ok(fixture)))
    expect(screen.getByText(/AI-assisted structure recovery/)).toBeVisible()
  })
  it.each(['BLOCKED', 'FAILED', 'REJECTED'])('shows safe %s outcome without a second cloud action', async status => {
    const returned = structuredClone(fixture)
    Object.assign(returned.pipeline.assistance, { status, origin: 'DETERMINISTIC', certificate: null })
    Object.assign(returned, { status: 'UNSUPPORTED', measurements: [], teeth: [] })
    const { input, button } = setup(vi.fn().mockResolvedValue(ok(returned)))
    fireEvent.click(button); await screen.findByText('Unsupported input', { exact: true })
    expect(input.value).toBe(example.raw_text)
    expect(screen.queryByRole('button', { name: 'Try AI-assisted parsing' })).not.toBeInTheDocument()
  })
  it('clears generated authorization after any raw edit', async () => {
    const { fetch, input, button } = setup()
    fireEvent.change(input, { target: { value: example.raw_text + ' ' } })
    fireEvent.click(screen.getByRole('checkbox', { name: /I confirm/ })); fireEvent.click(button)
    await screen.findByRole('alert') // mocked response belongs to the earlier input and must reject.
    expect(JSON.parse(fetch.mock.calls[0][1].body)).not.toHaveProperty('synthetic_fixture')
  })
  it('retains raw input and sanitizes network errors', async () => {
    const { input, button } = setup(vi.fn().mockRejectedValue(new Error('PRIVATE_PROVIDER')))
    fireEvent.click(button); await screen.findByRole('alert')
    expect(input.value).toBe(example.raw_text)
    expect(screen.queryByText(/PRIVATE_PROVIDER/)).not.toBeInTheDocument()
  })
  it('ignores a late response after editing the input', async () => {
    let finish!: (x: unknown) => void
    const { input, button } = setup(vi.fn().mockImplementation(() => new Promise(r => { finish = r })))
    fireEvent.click(button); fireEvent.change(input, { target: { value: ' replacement\t\n' } })
    await act(async () => finish(ok(fixture)))
    expect(screen.queryByLabelText('Automatic detection and clarification')).not.toBeInTheDocument()
    expect(input.value).toBe(' replacement\t\n')
  })
  it('times out an automatic generated request while preserving raw input', async () => {
    vi.useFakeTimers()
    const { input, button } = setup(vi.fn().mockImplementation((_url, options) => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(new DOMException('aborted', 'AbortError')))
    })))
    fireEvent.click(button)
    await act(async () => { await vi.advanceTimersByTimeAsync(35_000) })
    expect(screen.getByRole('alert')).toHaveTextContent('timed out')
    expect(input.value).toBe(example.raw_text)
  })
  it('forwards only the opaque receipt to downstream review with original raw text', async () => {
    const fetch = vi.fn().mockResolvedValueOnce(ok(fixture)).mockResolvedValueOnce(ok(review))
    const { button } = setup(fetch); fireEvent.click(button)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    fireEvent.click(screen.getByRole('button', { name: 'Create draft review' }))
    await act(async () => {})
    const body = JSON.parse(fetch.mock.calls[1][1].body)
    expect(body.recovery_receipt).toBe(fixture.pipeline.recovery_receipt)
    expect(body.raw_text).toBe(example.raw_text)
    expect(body).not.toHaveProperty('measurements')
  })
  it.each(['verified_source', 'real_patient_transmission', 'version', 'clarification'])('rejects invalid %s contracts', field => {
    const returned = structuredClone(fixture)
    if (field === 'verified_source') Object.assign(returned.pipeline.detection, { verified_source: 'ClinCheck' })
    if (field === 'real_patient_transmission') Object.assign(returned.pipeline.assistance, { real_patient_transmission_enabled: true })
    if (field === 'version') Object.assign(returned.pipeline, { version: 'unknown' })
    if (field === 'clarification') Object.assign(returned.pipeline, { clarifications: [{ message: null }] })
    expect(isAutomaticParseResult(returned)).toBe(false)
  })
})
