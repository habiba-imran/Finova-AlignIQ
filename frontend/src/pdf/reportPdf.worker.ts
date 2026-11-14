import { createReportPdf } from './reportPdf'
import type { PdfKind } from './reportPdf'

self.onmessage = async (event: MessageEvent<{ kind: PdfKind; data: unknown }>) => {
  try {
    const bytes = await createReportPdf(event.data.kind, event.data.data)
    self.postMessage({ bytes }, { transfer: [bytes.buffer as ArrayBuffer] })
  } catch (error) {
    const message = error instanceof Error && error.message.startsWith('PDF_UNSUPPORTED_GLYPH:') ? error.message : 'PDF_EXPORT_FAILED'
    self.postMessage({ error: message })
  }
}
