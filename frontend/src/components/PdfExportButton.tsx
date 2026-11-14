import { useEffect, useRef, useState } from 'react'
import { FileDown } from 'lucide-react'
import { createLocalPdf } from '../pdf/pdfWorker'
import type { PdfKind } from '../pdf/reportPdf'

export default function PdfExportButton({ kind, data, reportId }: { kind: PdfKind; data: unknown; reportId: string }) {
  const [busy, setBusy] = useState(false), [message, setMessage] = useState('')
  const revision = useRef(0), pending = useRef(false)
  const controller = useRef<AbortController | null>(null)
  useEffect(() => { revision.current++; pending.current = false; setBusy(false); setMessage(''); return () => { revision.current++; controller.current?.abort() } }, [data])
  async function exportPdf() {
    if (pending.current) return
    pending.current = true; setBusy(true); setMessage('Preparing complete PDF locally…')
    const current = revision.current
    controller.current = new AbortController()
    try {
      const bytes = await createLocalPdf(kind, data, controller.current.signal)
      if (current !== revision.current) return
      const url = URL.createObjectURL(new Blob([new Uint8Array(bytes).buffer], { type: 'application/pdf' }))
      try {
        const a = document.createElement('a'); a.href = url; a.download = `finova-${kind}-draft-${reportId.slice(0, 12)}.pdf`
        document.body.append(a); a.click(); a.remove()
      } finally { window.setTimeout(() => URL.revokeObjectURL(url), 1000) }
      setMessage('Complete DRAFT PDF download requested.')
    } catch (error) {
      if (current !== revision.current) return
      setMessage(error instanceof Error && error.message.startsWith('PDF_UNSUPPORTED_GLYPH:')
        ? 'PDF could not preserve an unsupported character. Use the unchanged TXT export; no incomplete PDF was downloaded.'
        : 'PDF export is unavailable. Your draft is preserved; retry or use TXT/copy.')
    } finally { if (current === revision.current) { pending.current = false; setBusy(false) } }
  }
  return <>
    <button type="button" className="button button-clear" disabled={busy} onClick={() => void exportPdf()}>
      {busy ? <span className="button-spinner" aria-hidden="true" /> : <FileDown size={15} aria-hidden="true" />}{busy ? 'Preparing PDF…' : 'Export PDF'}
    </button>
    {message && <p role="status" className="motion-status w-full text-xs leading-6 text-muted">{message}</p>}
  </>
}
