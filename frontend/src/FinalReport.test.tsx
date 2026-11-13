import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import FinalReportPanel from './components/FinalReportPanel'
import { EMPTY_CONTEXT } from './api/parse'
import { isFinalDraftReport } from './api/report'
import parseFixture from './test/fixtures/synthetic-parse-result.json'
import reviewFixture from './test/fixtures/synthetic-draft-review.json'
import fixture from './test/fixtures/synthetic-final-report.json'
import groqFixture from './test/fixtures/synthetic-groq-report.json'

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers() })
const ok = (data: unknown) => ({ ok: true, status: 200, json: async () => data })

function panel(fetch = vi.fn().mockResolvedValue(ok(fixture))) {
  vi.stubGlobal('fetch', fetch)
  render(<FinalReportPanel rawText={parseFixture.raw_text} source="Unknown" context={EMPTY_CONTEXT} rawHash={parseFixture.raw_sha256} questions={[]} />)
  return { fetch, button: screen.getByRole('button', { name: 'Create final report' }) }
}

describe('Phase 3 final DRAFT report workflow', () => {
  it('passes a recovery receipt with raw input, never browser-supplied findings', async () => {
    const fetch = vi.fn().mockResolvedValue(ok(fixture))
    vi.stubGlobal('fetch', fetch)
    render(<FinalReportPanel rawText={parseFixture.raw_text} source="Unknown" context={EMPTY_CONTEXT} rawHash={parseFixture.raw_sha256} questions={[]} recoveryReceipt="SYNTHETIC_RECEIPT" />)
    fireEvent.click(screen.getByRole('button', { name: 'Create final report' }))
    await screen.findByRole('article', { name: 'Final draft report results' })
    const body = JSON.parse(fetch.mock.calls[0][1].body)
    expect(body.recovery_receipt).toBe('SYNTHETIC_RECEIPT')
    expect(body).not.toHaveProperty('findings')
    expect(body.raw_text).toBe(parseFixture.raw_text)
  })

  it('asks for reparse after receipt expiry without discarding raw input', async () => {
    const { button } = panel(vi.fn().mockResolvedValue({ ok: false, status: 409 }))
    fireEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent('Choose Parse Table again')
  })
  it('sends raw input only on the explicit action and displays a complete abstention report', async () => {
    const { button, fetch } = panel()
    expect(fetch).not.toHaveBeenCalled()
    expect(screen.getByLabelText('Comment generation mode')).toHaveValue('AUTO')
    fireEvent.click(button)
    const article = await screen.findByRole('article', { name: 'Final draft report results' })
    const [url, options] = fetch.mock.calls[0]
    expect(url).toBe('/api/v1/reports/draft')
    expect(JSON.parse(options.body)).toEqual({ raw_text: parseFixture.raw_text, source_claim: 'Unknown', context: EMPTY_CONTEXT,
      synthetic_data_confirmed: true, requested_assessments: [], comment_mode: 'AUTO' })
    expect(options).toMatchObject({ cache: 'no-store', credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer' })
    expect(within(article).getByText('DRAFT — Requires Orthodontist Review', { exact: true })).toBeVisible()
    expect(within(article).getByText(/No eligible findings: Groq was not called/)).toBeVisible()
    expect(within(article).getByText('UNKNOWN — no authorized measurements.')).toBeVisible()
    expect(within(article).getByText('Unavailable assessments and missing information')).toBeVisible()
    expect(within(article).getByText('Clinical limitations and scope')).toBeVisible()
    expect(within(article).getByRole('button', { name: 'Copy Report' })).toBeEnabled()
    expect(screen.getByLabelText('Report export preview').textContent).toBe(fixture.export_text)
  })

  it('makes template selection explicit, invalidates prior exports and sends TEMPLATES', async () => {
    const { button, fetch } = panel(vi.fn().mockResolvedValueOnce(ok(fixture)).mockResolvedValueOnce(ok({ ...fixture,
      generation: { ...fixture.generation, requested_mode: 'TEMPLATES', reason: 'STANDARD_TEMPLATES_SELECTED' } })))
    fireEvent.click(button)
    await screen.findByRole('article')
    fireEvent.change(screen.getByLabelText('Comment generation mode'), { target: { value: 'TEMPLATES' } })
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Copy Report' })).not.toBeInTheDocument()
    fireEvent.click(button)
    await screen.findByRole('article')
    expect(JSON.parse(fetch.mock.calls[1][1].body).comment_mode).toBe('TEMPLATES')
    expect(screen.getByText(/Standard Templates selected. No provider call/)).toBeVisible()
  })

  it('shows loading and prevents duplicate requests', async () => {
    let finish!: (v: unknown) => void
    const { button, fetch } = panel(vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve })))
    fireEvent.click(button)
    expect(screen.getByRole('button', { name: 'Creating report…' })).toBeDisabled()
    fireEvent.click(button)
    expect(fetch).toHaveBeenCalledTimes(1)
    await act(async () => finish(ok(fixture)))
    expect(screen.getByRole('button', { name: 'Create final report' })).toBeEnabled()
  })

  it.each([413, 422, 500])('sanitizes HTTP %s failures without provider diagnostics', async status => {
    const { button } = panel(vi.fn().mockResolvedValue({ ok: false, status, json: async () => ({ detail: 'PRIVATE_PROVIDER_PAYLOAD' }) }))
    fireEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent(/preserved/)
    expect(screen.queryByText('PRIVATE_PROVIDER_PAYLOAD')).not.toBeInTheDocument()
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
  })

  it('handles network failure and retries only through another explicit action', async () => {
    const { button, fetch } = panel(vi.fn().mockRejectedValueOnce(new Error('PRIVATE_TRANSPORT')).mockResolvedValueOnce(ok(fixture)))
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(screen.queryByText('PRIVATE_TRANSPORT')).not.toBeInTheDocument()
    fireEvent.click(button)
    await screen.findByRole('article')
    expect(fetch).toHaveBeenCalledTimes(2)
  })

  it.each([
    { draft_status: 'APPROVED' }, { clinical_analysis_enabled: true }, { export_text: 'Missing disclaimers' },
    { engine_review: null }, { comments: null }, { report_version: 'future' },
    { generation: { ...fixture.generation, real_patient_transmission_enabled: true } },
    { generation: { ...fixture.generation, model: 'unapproved-model' } },
  ])('rejects an invalid or unsafe report boundary %j', async override => {
    const { button } = panel(vi.fn().mockResolvedValue(ok({ ...fixture, ...override })))
    fireEvent.click(button)
    await screen.findByRole('alert')
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
  })

  it('copies the exact server-rendered report including disclaimers and provenance', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', { clipboard: { writeText } })
    const { button } = panel()
    fireEvent.click(button)
    await screen.findByRole('article')
    fireEvent.click(screen.getByRole('button', { name: 'Copy Report' }))
    await screen.findByText('Report copied with draft status, limitations and provenance.')
    expect(writeText).toHaveBeenCalledExactlyOnceWith(fixture.export_text)
    expect(writeText.mock.calls[0][0]).toContain(fixture.engine_review.raw_sha256)
  })

  it('handles denied clipboard access with a local export fallback', async () => {
    vi.stubGlobal('navigator', { clipboard: { writeText: vi.fn().mockRejectedValue(new Error('Denied')) } })
    const { button } = panel()
    fireEvent.click(button)
    await screen.findByRole('article')
    fireEvent.click(screen.getByRole('button', { name: 'Copy Report' }))
    expect(await screen.findByText(/Clipboard access is unavailable/)).toBeVisible()
    expect(screen.getByRole('button', { name: 'Download Report (TXT)' })).toBeEnabled()
  })

  it('downloads a local TXT Blob with the exact report and a nonpatient filename', async () => {
    const create = vi.fn().mockReturnValue('blob:synthetic-local-report')
    const revoke = vi.fn()
    vi.stubGlobal('URL', Object.assign(class extends URL {}, { createObjectURL: create, revokeObjectURL: revoke }))
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) {
      expect(this.download).toBe(`finova-aligniq-draft-${fixture.report_id.slice(0, 12)}.txt`)
      expect(this.href).toBe('blob:synthetic-local-report')
    })
    const { button, fetch } = panel()
    fireEvent.click(button)
    await screen.findByRole('article')
    vi.useFakeTimers()
    fireEvent.click(screen.getByRole('button', { name: 'Download Report (TXT)' }))
    expect(click).toHaveBeenCalledTimes(1)
    const blob = create.mock.calls[0][0] as Blob
    expect(blob.type).toBe('text/plain;charset=utf-8')
    act(() => vi.advanceTimersByTime(1000))
    expect(revoke).toHaveBeenCalledExactlyOnceWith('blob:synthetic-local-report')
    vi.useRealTimers()
    const reader = new FileReader()
    const text = await new Promise<string>(resolve => { reader.onload = () => resolve(String(reader.result)); reader.readAsText(blob) })
    expect(text).toBe(fixture.export_text)
    expect(fetch).toHaveBeenCalledTimes(1) // export itself makes no HTTP request
  })

  it('shows mocked Groq success with TEST_ONLY status and exact measurements', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(ok(groqFixture)))
    render(<FinalReportPanel rawText="SYNTHETIC TEST_ONLY" source="Unknown" context={{ ...EMPTY_CONTEXT, source_version: 'TEST_ONLY-1' }} rawHash={groqFixture.engine_review.raw_sha256} questions={[]} />)
    fireEvent.click(screen.getByRole('button', { name: 'Create final report' }))
    const article = await screen.findByRole('article')
    expect(within(article).getByText('Groq AI · validated')).toBeVisible()
    expect(within(article).getByText(/Groq wording passed exact validation/)).toBeVisible()
    const tooth = groqFixture.comments.find(c => c.section === 'TOOTH')!
    expect(within(article).getByText(tooth.text, { normalizer: value => value })).toBeVisible()
    expect(tooth.text).toContain('1.2300')
    expect(tooth.text).toContain('−1.2300 M')
    expect(tooth.evidence_status).toBe('TEST_ONLY')
  })

  it('keeps literal markup inert and does not persist a generated report', async () => {
    const literal = '<script>window.reportInjection=true</script>'
    const returned = structuredClone(fixture)
    returned.comments[0].text += literal
    returned.export_text += returned.comments[0].text
    const storage = vi.spyOn(Storage.prototype, 'setItem')
    const { button } = panel(vi.fn().mockResolvedValue(ok(returned)))
    fireEvent.click(button)
    const article = await screen.findByRole('article')
    expect(article.querySelector('script')).toBeNull()
    expect(within(article).getByText(returned.comments[0].text, { normalizer: value => value })).toBeVisible()
    expect(storage).not.toHaveBeenCalled()
  })

  it('aborts stale requests when the mode changes and ignores their late responses', async () => {
    let finish!: (v: unknown) => void
    const fetch = vi.fn().mockImplementation(() => new Promise(resolve => { finish = resolve }))
    const { button } = panel(fetch)
    fireEvent.click(button)
    const signal = fetch.mock.calls[0][1].signal as AbortSignal
    fireEvent.change(screen.getByLabelText('Comment generation mode'), { target: { value: 'TEMPLATES' } })
    expect(signal.aborted).toBe(true)
    await act(async () => finish(ok(fixture)))
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
  })

  it('times out a stalled report request', async () => {
    vi.useFakeTimers()
    const { button } = panel(vi.fn().mockImplementation((_url, options) => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(new DOMException('abort', 'AbortError')))
    })))
    fireEvent.click(button)
    await act(async () => { await vi.advanceTimersByTimeAsync(30_000) })
    expect(screen.getByRole('alert')).toHaveTextContent('timed out')
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
  })

  it('bounds unavailable presentation while preserving full export data', async () => {
    const { button } = panel()
    fireEvent.click(button)
    await screen.findByRole('article')
    fireEvent.click(screen.getByRole('button', { name: /Show more report assessments/ }))
    expect(screen.getByLabelText('Report export preview').textContent).toBe(fixture.export_text)
  })

  it.each(['raw', 'version', 'context', 'clear', 'demo', 'consent', 'question'])('preserves raw input and removes the final report when %s changes', async change => {
    const fetch = vi.fn().mockResolvedValueOnce(ok(parseFixture)).mockResolvedValueOnce(ok(reviewFixture)).mockResolvedValueOnce(ok(fixture))
    vi.stubGlobal('fetch', fetch)
    render(<App />)
    const input = screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement
    fireEvent.change(input, { target: { value: parseFixture.raw_text } })
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
    await screen.findByRole('heading', { name: 'Structured lexical preview' })
    fireEvent.click(screen.getByRole('button', { name: 'Create draft review' }))
    await screen.findByLabelText('Draft review results')
    expect(fetch).toHaveBeenCalledTimes(2)
    fireEvent.click(screen.getByRole('button', { name: 'Create final report' }))
    await screen.findByRole('article')
    expect(input.value).toBe(parseFixture.raw_text)
    if (change === 'raw') fireEvent.change(input, { target: { value: '  replacement\ttext\n\n' } })
    if (change === 'version') fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
    if (change === 'context') fireEvent.change(screen.getByLabelText('Tooth notation claim'), { target: { value: 'FDI' } })
    if (change === 'clear') fireEvent.click(screen.getByRole('button', { name: 'Clear' }))
    if (change === 'demo') fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    if (change === 'consent') fireEvent.click(screen.getByRole('checkbox'))
    if (change === 'question') fireEvent.change(screen.getByLabelText(/Requested assessment/), { target: { value: 'ATTACHMENTS' } })
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Copy Report' })).not.toBeInTheDocument()
    expect(fetch).toHaveBeenCalledTimes(3)
  })

  it('accepts backend fixture contracts and rejects invented references or unverified measurements', () => {
    expect(isFinalDraftReport(fixture)).toBe(true)
    expect(isFinalDraftReport(groqFixture)).toBe(true)
    const invented = structuredClone(fixture)
    invented.comments[0].finding_ids = ['UNKNOWN_FINDING']
    expect(isFinalDraftReport(invented)).toBe(false)
    const mismatched = structuredClone(groqFixture)
    const comment = mismatched.comments.find(c => c.measurements.length)!
    comment.measurements[0].magnitude = '999'
    expect(isFinalDraftReport(mismatched)).toBe(false)
  })
})
