import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Copy, Download, Layers } from 'lucide-react'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import { requestAttachmentDraft } from '../api/attachments'
import type { AttachmentDraft, AttachmentEntry } from '../api/attachments'
import { EvidenceDisclosure, ExportBar, ReportEmpty, ReportHeader, ReportSection, SummaryGrid, SummaryMetric } from './ReportPrimitives'
import PdfExportButton from './PdfExportButton'

const LABELS: Record<AttachmentEntry['result_type'], string> = {
  CANDIDATE: 'Supplied candidate', ALTERNATIVE: 'Supplied alternative', NOT_INDICATED: 'Supplied no attachment', UNKNOWN: 'Unknown', WITHHELD: 'Withheld',
}
const TONES: Record<AttachmentEntry['result_type'], string> = {
  CANDIDATE: 'report-badge-brand', ALTERNATIVE: 'report-badge-brand', NOT_INDICATED: 'report-badge-notice', UNKNOWN: 'report-badge-notice', WITHHELD: 'report-badge-notice',
}
const EXPLANATIONS: Record<AttachmentEntry['result_type'], string> = {
  CANDIDATE: 'Supplied fictional candidate. Clinical suitability is unassessed.',
  ALTERNATIVE: 'Supplied fictional alternative. No superiority or clinical suitability is asserted.',
  NOT_INDICATED: 'Supplied fictional no-attachment decision. Missing or zero movements do not establish omission.',
  UNKNOWN: 'Attachment need is unknown. Available movements do not establish indication or omission.',
  WITHHELD: 'Attachment review is withheld because identity, supporting evidence or clinical context is incomplete.',
}

export default function AttachmentWorkspace({ rawText, context, parsed, demo, onComplete }: {
  rawText: string; context: ContextClaims; parsed: AutomaticParseResult; demo: boolean; onComplete: (value: boolean) => void
}) {
  const [draft, setDraft] = useState<AttachmentDraft | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [status, setStatus] = useState('')
  const pending = useRef<AbortController | null>(null), revision = useRef(0)
  const heading = useRef<HTMLHeadingElement>(null)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (draft) heading.current?.focus() }, [draft])

  async function review() {
    if (pending.current) return
    const controller = new AbortController(), current = ++revision.current
    pending.current = controller; setDraft(null); setStatus(''); setError(''); setLoading(true); onComplete(false)
    const timer = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const result = await requestAttachmentDraft(rawText, context, parsed.raw_sha256, demo, controller.signal, parsed.pipeline.recovery_receipt ?? undefined)
      if (current === revision.current) { setDraft(result); onComplete(true) }
    } catch (e) {
      if (current === revision.current) setError(controller.signal.aborted ? 'Attachment review timed out. Your original text and parsed values are preserved. Retry when ready.'
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'Read the table again with Parse Table, then retry. Your original text is preserved.'
          : 'Attachment review could not return a valid draft. Your original text is preserved; please retry.')
    } finally { window.clearTimeout(timer); if (current === revision.current) { pending.current = null; setLoading(false) } }
  }
  async function copy() {
    if (!draft) return
    const current = revision.current
    try { await navigator.clipboard.writeText(draft.export_text); if (current === revision.current) setStatus('Attachment DRAFT copied with supplied-decision labels, evidence and limitations.') }
    catch { if (current === revision.current) setStatus('Clipboard access is unavailable. Use Export TXT.') }
  }
  function download() {
    if (!draft) return
    try {
      const url = URL.createObjectURL(new Blob([draft.export_text], { type: draft.export_format }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-attachments-draft-${draft.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setStatus('Attachment DRAFT TXT download requested.')
    } catch { setStatus('Download is unavailable. Copy the DRAFT.') }
  }
  const counts = draft ? (['CANDIDATE', 'ALTERNATIVE', 'NOT_INDICATED', 'UNKNOWN', 'WITHHELD'] as const).map(type => ({ type, count: draft.entries.filter(e => e.result_type === type).length })) : []
  return <section className="panel" aria-labelledby="attachments-heading">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><Layers size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="attachments-heading" className="panel-title">Attachment Interface · Micro Review</h3></div>
      <div className="flex items-center gap-3"><span className="text-xs font-medium text-muted">Clinician review prototype</span></div>
    </div>
    <div className="p-5 sm:p-7">
      <p className="max-w-3xl text-sm leading-7 text-muted">Inspect the original table above, then prepare a tooth-indexed attachment review. Movement amounts alone cannot establish attachment need, design, omission or placement.</p>
      {!demo && <p className="mt-3 text-sm leading-6 text-muted">Attachment choices are unavailable without verified supporting evidence.</p>}
      <button type="button" className="button button-primary mt-5" disabled={loading} onClick={() => void review()} aria-describedby="attachment-privacy">{loading ? <><span className="button-spinner" aria-hidden="true" />Preparing attachment review…</> : <>Run Attachment Review<ArrowRight size={16} aria-hidden="true" /></>}</button>
      <p id="attachment-privacy" className="mt-3 text-xs leading-6 text-muted">Supplied example decisions are shown as provided. No attachment choice is generated from movement amounts.</p>
      {loading && <p role="status" className="motion-status mt-3 text-sm text-muted">Checking attachment evidence and preparing the DRAFT…</p>}
      {error && <p role="alert" className="motion-status mt-4 text-sm text-notice-ink">{error}</p>}
      {!draft && !loading && !error && <ReportEmpty>Your attachment review table will appear here after you run the review.</ReportEmpty>}
      {draft && <article aria-label="Attachment review draft" className="motion-enter mt-8 overflow-hidden rounded-2xl border border-line bg-white shadow-panel">
        <ReportHeader
          eyebrow="Micro · Attachment review"
          title="Attachment review draft"
          headingRef={heading}
          draftStatus={draft.draft_status}
          badges={[
            { label: draft.evidence_domain === 'TEST_ONLY' ? 'Verified synthetic demonstration only' : 'Unverified input', tone: 'brand' },
            { label: 'Not approved', tone: 'notice' },
          ]}
          summary={<>
            <p className="text-sm leading-7 text-muted">{draft.evidence_domain === 'TEST_ONLY' ? 'Supplied fictional attachment choices only. Clinical suitability is unassessed.' : 'Unverified input — attachment recommendations unavailable.'}</p>
            <p className="mt-2 text-sm leading-7 text-muted">Unknown and withheld do not mean no attachment. A supplied no-attachment row is an explicit fictional decision, never an inference from missing or zero movement.</p>
            <SummaryGrid label="Attachment review summary">
              <SummaryMetric label="Supplied candidates" value={counts.find(c => c.type === 'CANDIDATE')?.count ?? 0} detail="Illustrative only" />
              <SummaryMetric label="Supplied alternatives" value={counts.find(c => c.type === 'ALTERNATIVE')?.count ?? 0} detail="No superiority claim" />
              <SummaryMetric label="Supplied no attachment" value={counts.find(c => c.type === 'NOT_INDICATED')?.count ?? 0} detail="Explicit fictional decision" tone="notice" />
              <SummaryMetric label="Unknown" value={counts.find(c => c.type === 'UNKNOWN')?.count ?? 0} detail="Not a negative decision" tone="notice" />
              <SummaryMetric label="Withheld" value={counts.find(c => c.type === 'WITHHELD')?.count ?? 0} detail="Safeguard withheld" tone="notice" />
            </SummaryGrid>
          </>}
        />
        <div className="p-5 sm:p-7">
          <div className="mb-3 flex flex-wrap items-end justify-between gap-3">
            <div>
              <h4 className="text-[17px] font-semibold tracking-[-0.01em]">Tooth-wise attachment review</h4>
              <p className="mt-1 text-xs leading-5 text-muted">Supplied fictional choices and unavailable findings are shown separately.</p>
            </div>
            <span className="report-badge">{draft.entries.length} entries</span>
          </div>
          <div role="region" aria-label="Tooth-indexed attachment table" tabIndex={0} className="attachment-scroll overflow-x-auto rounded-xl border border-line md:max-h-[60rem] md:overflow-auto">
            <table className="attachment-table w-full table-fixed text-left text-sm leading-6">
              <caption className="sr-only">Original tooth tokens, supplied synthetic attachment options or explicit unavailable states. All entries remain DRAFT and not clinically approved.</caption>
              <thead className="sticky top-0 z-10 bg-canvas text-xs text-muted"><tr><th scope="col" className="w-[13%] p-4">Original tooth</th><th scope="col" className="w-[22%] p-4">Review result</th><th scope="col" className="w-[25%] p-4">Supplied option / decision</th><th scope="col" className="w-[40%] p-4">Explanation & evidence</th></tr></thead>
              <tbody>{draft.entries.map((e, i) => <tr key={e.entry_id} className="border-t border-line align-top">
                <th scope="row" className="p-4 font-semibold"><span aria-hidden="true" className="mb-1 block text-xs font-semibold text-muted lg:hidden">Original tooth</span><span className="raw-text">{e.original_tooth ?? 'Unresolved'}</span><span className="mt-1 block text-xs font-normal text-muted">{e.evidence_status === 'TEST_ONLY' ? 'Opaque demo identity' : 'Unverified token'}</span></th>
                <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted lg:hidden">Review result</span><span className={`inline-block rounded-md border px-2 py-1 text-xs font-semibold ${TONES[e.result_type]}`}>{LABELS[e.result_type]}</span><p className="mt-2 text-xs text-muted">{e.decision_origin === 'SUPPLIED_SYNTHETIC' ? 'Supplied fictional decision' : 'No attachment decision'}</p></td>
                <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted lg:hidden">Supplied option / decision</span><p className="font-medium">{e.design?.label ?? (e.result_type === 'NOT_INDICATED' ? 'No attachment — supplied demonstration decision' : 'No authorized option')}</p>{e.alternative_for && <p className="mt-2 text-xs text-muted">Alternative to {draft.entries.find(c => c.entry_id === e.alternative_for)?.design?.label ?? 'linked candidate'}; no superiority claim.</p>}</td>
                <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted lg:hidden">Explanation & evidence</span><p className="text-xs leading-6">{EXPLANATIONS[e.result_type]}</p>
                  <EvidenceDisclosure summary={`Details & provenance · row ${i + 1}`}>
                    {e.design ? <><p>Supplied shape: {e.design.shape ?? 'Unknown'}; orientation: {e.design.orientation ?? 'Unknown'}</p><p>{e.design.dimensions ? `Supplied dimensions: ${e.design.dimensions.x} × ${e.design.dimensions.y} × ${e.design.dimensions.z} mm` : 'Dimensions unknown; no values inferred.'}</p></> : <p>Design and geometry unavailable.</p>}
                    <p>Placement and stage references are illustrative only. Clinical placement is not verified.</p>
                    {parsed.measurements.filter(m => e.measurement_refs.includes(m.id)).map(m => <p key={m.id}>{m.raw_label}: {m.raw_value ?? 'Missing'} — original source value</p>)}
                    <p>Complete provenance is included in exports.</p>
                  </EvidenceDisclosure>
                </td>
              </tr>)}</tbody>
            </table>
          </div>
          <ReportSection title="Clinician review required" label="Clinician attachment review" tone="notice" className="my-5" description="Attachment indication, design, geometry and placement require independent clinical review. Supplied fictional dimensions do not verify clinical suitability.">
            <p className="text-xs leading-6 text-notice-ink">Unknown and withheld results do not mean an attachment is unnecessary.</p>
          </ReportSection>

          <ExportBar label="Attachment export" title="Export" description="Copy or download the complete DRAFT with supplied-decision labels and limitations." notice={status || undefined}>
            <button type="button" className="button button-example" onClick={() => void copy()}><Copy size={15} aria-hidden="true" />Copy</button>
            <button type="button" className="button button-secondary" onClick={download}><Download size={15} aria-hidden="true" />Export TXT</button>
            <PdfExportButton kind="micro" data={draft} reportId={draft.report_id} />
          </ExportBar>

          <p className="mt-4 text-xs leading-6 text-muted">Complete exports retain supplied-decision labels, source evidence and clinical limitations.</p>
        </div>
      </article>}
    </div>
  </section>
}
