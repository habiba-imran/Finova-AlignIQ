import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'
import PdfExportButton from './components/PdfExportButton'
import { createLocalPdf as createReportPdf } from './pdf/pdfWorker'

vi.mock('./pdf/pdfWorker', () => ({ createLocalPdf: vi.fn() }))
beforeEach(() => {
  Object.defineProperty(URL, 'createObjectURL', { configurable: true, value: vi.fn(() => 'blob:local-pdf') })
  Object.defineProperty(URL, 'revokeObjectURL', { configurable: true, value: vi.fn() })
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  vi.mocked(createReportPdf).mockReset()
})

test('exports only on explicit click, suppresses double click, and downloads PDF', async () => {
  let finish!: (bytes: Uint8Array) => void
  vi.mocked(createReportPdf).mockReturnValue(new Promise(resolve => { finish = resolve }))
  const data = { report: 'validated upstream' }
  render(<PdfExportButton kind="macro" data={data} reportId={'a'.repeat(64)} />)
  expect(createReportPdf).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: 'Export PDF' }))
  expect(screen.getByRole('button', { name: 'Preparing PDF…' })).toBeDisabled()
  await act(async () => finish(new Uint8Array([37, 80, 68, 70])))
  expect(createReportPdf).toHaveBeenCalledExactlyOnceWith('macro', data, expect.any(AbortSignal))
  expect(HTMLAnchorElement.prototype.click).toHaveBeenCalledOnce()
  expect(screen.getByRole('status')).toHaveTextContent('Complete DRAFT PDF download requested.')
  expect(screen.getByRole('button', { name: 'Export PDF' })).toBeEnabled()
})

test.each(['unmount', 'change'] as const)('draft %s prevents a stale pending PDF download', async mode => {
  let finish!: (bytes: Uint8Array) => void
  vi.mocked(createReportPdf).mockReturnValue(new Promise(resolve => { finish = resolve }))
  const { unmount, rerender } = render(<PdfExportButton kind="micro" data={{ version: 1 }} reportId={'a'.repeat(64)} />)
  fireEvent.click(screen.getByRole('button', { name: 'Export PDF' }))
  if (mode === 'unmount') unmount()
  else rerender(<PdfExportButton kind="micro" data={{ version: 2 }} reportId={'b'.repeat(64)} />)
  await act(async () => finish(new Uint8Array([37, 80, 68, 70])))
  expect(vi.mocked(createReportPdf).mock.calls[0][2].aborted).toBe(true)
  expect(URL.createObjectURL).not.toHaveBeenCalled()
  expect(HTMLAnchorElement.prototype.click).not.toHaveBeenCalled()
})

test.each(['PDF_UNSUPPORTED_GLYPH:U+1F9B7', 'other failure'])('PDF failure preserves TXT/copy fallback and supports explicit retry: %s', async message => {
  vi.mocked(createReportPdf).mockRejectedValueOnce(new Error(message)).mockResolvedValueOnce(new Uint8Array([37]))
  render(<PdfExportButton kind="nano" data={{}} reportId={'a'.repeat(64)} />)
  fireEvent.click(screen.getByRole('button', { name: 'Export PDF' }))
  await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent(/TXT/))
  expect(URL.createObjectURL).not.toHaveBeenCalled()
  fireEvent.click(screen.getByRole('button', { name: 'Export PDF' }))
  await waitFor(() => expect(URL.createObjectURL).toHaveBeenCalledOnce())
})
