import { expect, test, vi } from 'vitest'
import { createLocalPdf } from './pdfWorker'

interface WorkerDouble {
  onmessage: ((event: { data: { bytes?: Uint8Array; error?: string } }) => void) | null
  onerror: (() => void) | null
  postMessage: ReturnType<typeof vi.fn>
  terminate: ReturnType<typeof vi.fn>
}
const state = vi.hoisted(() => ({ workers: [] as WorkerDouble[] }))
vi.mock('./reportPdf.worker?worker&inline', () => ({ default: class {
  onmessage = null; onerror = null
  postMessage = vi.fn(); terminate = vi.fn()
  constructor() { state.workers.push(this) }
} }))

test('only explicit generation creates a local worker and it terminates on success', async () => {
  const data = { snapshot: 'in memory' }, controller = new AbortController()
  const result = createLocalPdf('macro', data, controller.signal), worker = state.workers.at(-1)!
  expect(worker.postMessage).toHaveBeenCalledExactlyOnceWith({ kind: 'macro', data })
  worker.onmessage!({ data: { bytes: new Uint8Array([37, 80]) } })
  await expect(result).resolves.toEqual(new Uint8Array([37, 80]))
  expect(worker.terminate).toHaveBeenCalledOnce()
})

test('source invalidation aborts and terminates PDF work without emitting bytes', async () => {
  const controller = new AbortController(), result = createLocalPdf('micro', {}, controller.signal)
  const worker = state.workers.at(-1)!
  controller.abort()
  await expect(result).rejects.toThrow('PDF_ABORTED')
  expect(worker.terminate).toHaveBeenCalledOnce()
})

test('already aborted input starts no worker', async () => {
  const count = state.workers.length, controller = new AbortController(); controller.abort()
  await expect(createLocalPdf('nano', {}, controller.signal)).rejects.toThrow('PDF_ABORTED')
  expect(state.workers).toHaveLength(count)
})

test.each(['message', 'crash'])('worker %s failure terminates it and preserves explicit retry', async failure => {
  const result = createLocalPdf('nano', {}, new AbortController().signal), worker = state.workers.at(-1)!
  if (failure === 'message') worker.onmessage!({ data: { error: 'PDF_UNSUPPORTED_GLYPH:U+1F9B7' } })
  else worker.onerror!()
  await expect(result).rejects.toThrow(failure === 'message' ? 'PDF_UNSUPPORTED_GLYPH:' : 'PDF_EXPORT_FAILED')
  expect(worker.terminate).toHaveBeenCalledOnce()
})
