import PdfWorker from './reportPdf.worker?worker&inline'
import type { PdfKind } from './reportPdf'

/** Vite inlines the worker and all font/code assets: zero export-time requests.
 * Terminating the worker cancels work when the source draft changes/unmounts. */
export function createLocalPdf(kind: PdfKind, data: unknown, signal: AbortSignal): Promise<Uint8Array> {
  return new Promise((resolve, reject) => {
    if (signal.aborted) { reject(new Error('PDF_ABORTED')); return }
    const worker = new PdfWorker()
    function cleanup() { worker.terminate(); signal.removeEventListener('abort', abort) }
    function abort() { cleanup(); reject(new Error('PDF_ABORTED')) }
    signal.addEventListener('abort', abort, { once: true })
    worker.onmessage = (event: MessageEvent<{ bytes?: Uint8Array; error?: string }>) => {
      cleanup()
      if (event.data.bytes instanceof Uint8Array) resolve(event.data.bytes)
      else reject(new Error(event.data.error ?? 'PDF_EXPORT_FAILED'))
    }
    worker.onerror = () => { cleanup(); reject(new Error('PDF_EXPORT_FAILED')) }
    try { worker.postMessage({ kind, data }) }
    catch { cleanup(); reject(new Error('PDF_EXPORT_FAILED')) }
  })
}
