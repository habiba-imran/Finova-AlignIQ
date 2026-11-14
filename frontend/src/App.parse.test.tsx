import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { EMPTY_CONTEXT } from './api/parse'
import fixture from './test/fixtures/synthetic-parse-result.json'

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers() })

function setup(raw = fixture.raw_text) {
  render(<App diagnostics />)
  const input = screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement
  const button = screen.getByRole('button', { name: 'Parse Table' })
  fireEvent.change(input, { target: { value: raw } })
  return { input, button }
}

function response(raw = fixture.raw_text, overrides = {}) {
  return { ok: true, status: 200, json: async () => ({ ...fixture, raw_text: raw, ...overrides }) }
}

describe('Explicit Phase 1 parsing', () => {
  it('enables parsing when text is present and does not transmit on typing, changing metadata, or loading a demo', () => {
    const fetch = vi.fn()
    vi.stubGlobal('fetch', fetch)
    const { button } = setup()
    expect(button).toBeEnabled()
    fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
    fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    expect(fetch).not.toHaveBeenCalled()
  })

  it('posts exact raw text and unverified claims only after Parse Table, then shows raw and lexical values', async () => {
    const raw = '  Tooth\tRotation (deg)\n\n13\t−1.2300 M  \n\n'
    const fetch = vi.fn().mockResolvedValue(response(raw))
    vi.stubGlobal('fetch', fetch)
    const { input, button } = setup(raw)
    expect(screen.getByText('Parse your TMT to see the structured table.')).toBeVisible()
    fireEvent.click(button)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    expect(screen.queryByText('Parse your TMT to see the structured table.')).not.toBeInTheDocument()
    const structured = screen.getByRole('region', { name: 'Structured TMT table' })
    expect(within(structured).getByRole('columnheader', { name: /Rotation \(deg\)/ })).toBeVisible()
    expect(within(structured).getByRole('rowheader', { name: /13/ })).toBeVisible()
    expect(within(structured).getByText('-1.2300')).toBeVisible()
    expect(fetch).toHaveBeenCalledTimes(1)
    const [url, options] = fetch.mock.calls[0]
    expect(url).toBe('/api/v1/tmt/parse')
    expect(options.method).toBe('POST')
    expect(options.cache).toBe('no-store')
    expect(options.credentials).toBe('omit')
    expect(JSON.parse(options.body)).toEqual({ raw_text: raw, source_claim: 'Unknown', context: EMPTY_CONTEXT, synthetic_data_confirmed: true })
    const measurements = screen.getByRole('region', { name: 'Parsed measurements' })
    expect(within(measurements).getByText('−1.2300 M')).toBeVisible()
    expect(within(measurements).getByText('-1.2300')).toBeVisible()
    expect(screen.getByText('Source verification: UNVERIFIED')).toBeVisible()
    expect(screen.getByText(/Canonical tooth IDs, axes, and physical directions are withheld/)).toBeVisible()
    expect(screen.getByText(/WARNING · SOURCE_UNVERIFIED/)).toBeInTheDocument()
    expect(input.value).toBe(raw)
    expect(screen.getByLabelText('Raw text preview').textContent).toBe(raw)
    expect(screen.getByRole('button', { name: 'Analyze' })).toBeDisabled()
  })

  it('shows loading and prevents duplicate requests', async () => {
    let finish!: (value: unknown) => void
    const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
    vi.stubGlobal('fetch', fetch)
    const { button } = setup()
    fireEvent.click(button)
    expect(screen.getByRole('button', { name: 'Parsing…' })).toBeDisabled()
    expect(screen.getByText('Parsing the submitted text structure…')).toBeVisible()
    fireEvent.click(button)
    expect(fetch).toHaveBeenCalledTimes(1)
    await act(async () => finish(response()))
    expect(screen.getByRole('button', { name: 'Parse Table' })).toBeEnabled()
  })

  it.each([413, 422, 500])('shows a safe HTTP %s error while preserving raw input', async status => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status, json: async () => ({ detail: '<script>unsafe server text</script>' }) }))
    const { input, button } = setup()
    fireEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent(/original text is preserved/i)
    expect(input.value).toBe(fixture.raw_text)
    expect(screen.queryByText(/unsafe server text/)).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Structured lexical preview' })).not.toBeInTheDocument()
  })

  it('handles network errors and retries only through another explicit action', async () => {
    const fetch = vi.fn().mockRejectedValueOnce(new Error('Do not display private transport diagnostics')).mockResolvedValueOnce(response())
    vi.stubGlobal('fetch', fetch)
    const { button } = setup()
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(screen.queryByText(/private transport diagnostics/)).not.toBeInTheDocument()
    expect(fetch).toHaveBeenCalledTimes(1)
    fireEvent.click(button)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(fetch).toHaveBeenCalledTimes(2)
  })

  it.each(['raw_text', 'measurements', 'source'])('rejects malformed or mismatched %s in a response', async key => {
    const bad = { ...fixture, [key]: key === 'raw_text' ? 'unrelated submission' : null }
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => bad }))
    const { button } = setup()
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(screen.queryByRole('heading', { name: 'Structured lexical preview' })).not.toBeInTheDocument()
  })

  it('ignores a late response after the raw text changes', async () => {
    let finish!: (value: unknown) => void
    const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
    vi.stubGlobal('fetch', fetch)
    const { input, button } = setup()
    fireEvent.click(button)
    const signal = fetch.mock.calls[0][1].signal as AbortSignal
    fireEvent.change(input, { target: { value: '  replacement\ttext\n' } })
    expect(signal.aborted).toBe(true)
    await act(async () => finish(response()))
    expect(screen.queryByRole('heading', { name: 'Structured lexical preview' })).not.toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(input.value).toBe('  replacement\ttext\n')
  })

  it.each(['version', 'context', 'clear', 'demo'])('invalidates results when %s changes', async change => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response()))
    const { button } = setup()
    fireEvent.click(button)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    if (change === 'version') fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
    if (change === 'context') {
      fireEvent.click(screen.getByRole('combobox', { name: 'Tooth notation claim' }))
      fireEvent.click(screen.getByRole('option', { name: 'FDI' }))
    }
    if (change === 'clear') fireEvent.click(screen.getByRole('button', { name: 'Clear' }))
    if (change === 'demo') fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    expect(screen.queryByRole('heading', { name: 'Structured lexical preview' })).not.toBeInTheDocument()
  })

  it('does not persist returned results and renders returned markup as inert text', async () => {
    const literal = '<script>window.synthetic = true</script>'
    const returned = { ...fixture, measurements: [{ ...fixture.measurements[0], raw_value: literal }] }
    const storage = vi.spyOn(Storage.prototype, 'setItem')
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => returned }))
    const { button } = setup()
    fireEvent.click(button)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    const region = screen.getByRole('region', { name: 'Parsed measurements' })
    expect(within(region).getByText(literal)).toBeVisible()
    expect(region.querySelector('script')).toBeNull()
    expect(storage).not.toHaveBeenCalled()
  })

  it('keeps unsupported and partial outcomes visible with clarification fields', async () => {
    const returned = { ...fixture, status: 'UNSUPPORTED', teeth: [], measurements: [], layout: { orientation: 'UNKNOWN', delimiter: null } }
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => returned }))
    const { button } = setup()
    fireEvent.click(button)
    await screen.findByText('Unsupported layout')
    expect(screen.getByText(/No measurement cells could be assigned/)).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Fields requiring clarification or verification' })).toBeVisible()
  })

  it('times out a stalled request without discarding input', async () => {
    vi.useFakeTimers()
    vi.stubGlobal('fetch', vi.fn().mockImplementation((_url, options) => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(new DOMException('aborted', 'AbortError')))
    })))
    const { input, button } = setup()
    fireEvent.click(button)
    await act(async () => { await vi.advanceTimersByTimeAsync(20_000) })
    expect(screen.getByRole('alert')).toHaveTextContent('timed out')
    expect(input.value).toBe(fixture.raw_text)
  })

  it('retains oversized input and makes no request', () => {
    const fetch = vi.fn()
    vi.stubGlobal('fetch', fetch)
    const raw = 'x'.repeat(100_001)
    const { input, button } = setup(raw)
    expect(button).toBeDisabled()
    expect(screen.getByRole('alert')).toHaveTextContent('100,000 characters')
    expect(input.value).toBe(raw)
    expect(fetch).not.toHaveBeenCalled()
  })

  it('sends optional metadata as claims without changing the raw text', async () => {
    const fetch = vi.fn().mockResolvedValue(response())
    vi.stubGlobal('fetch', fetch)
    const { input, button } = setup()
    fireEvent.click(screen.getByRole('combobox', { name: 'Tooth notation claim' }))
    fireEvent.click(screen.getByRole('option', { name: 'FDI' }))
    fireEvent.click(screen.getByRole('combobox', { name: 'Measurement basis claim' }))
    fireEvent.click(screen.getByRole('option', { name: 'Crown center' }))
    fireEvent.click(button)
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1))
    const request = JSON.parse(fetch.mock.calls[0][1].body)
    expect(request.context.notation).toBe('FDI')
    expect(request.context.reference_basis).toBe('CROWN_CENTER')
    expect(input.value).toBe(fixture.raw_text)
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
  })
})
