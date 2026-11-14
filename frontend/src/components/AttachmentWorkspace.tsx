import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Copy, Download, Layers } from 'lucide-react'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import { requestAttachmentDraft } from '../api/attachments'
import type { AttachmentDraft, AttachmentEntry } from '../api/attachments'

const LABELS: Record<AttachmentEntry['result_type'], string> = {
  CANDIDATE: 'Supplied candidate', ALTERNATIVE: 'Supplied alternative', NOT_INDICATED: 'Supplied no attachment', UNKNOWN: 'Unknown', WITHHELD: 'Withheld',
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
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'Recovery evidence expired or changed. Choose Parse Table again; your original text is preserved.'
          : 'Attachment review could not return a valid draft. Your original text is preserved; check the backend and retry.')
    } finally { window.clearTimeout(timer); if (current === revision.current) { pending.current = null; setLoading(false) } }
  }
  async function copy() {
    if (!draft) return
    const current = revision.current
    try { await navigator.clipboard.writeText(draft.export_text); if (current === revision.current) setStatus('Attachment DRAFT copied with supplied-decision labels, evidence and limitations.') }
    catch { if (current === revision.current) setStatus('Clipboard access is unavailable. Download the TXT or copy the export preview.') }
  }
  function download() {
    if (!draft) return
    try {
      const url = URL.createObjectURL(new Blob([draft.export_text], { type: draft.export_format }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-attachments-draft-${draft.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setStatus('Attachment DRAFT TXT download requested.')
    } catch { setStatus('Download is unavailable. Copy the DRAFT or use the export preview.') }
  }
  return <section className="panel mt-6" aria-labelledby="attachments-heading">
    <div className="panel-heading flex-wrap py-4"><h2 id="attachments-heading" className="flex items-center gap-2 font-semibold"><Layers size={19} aria-hidden="true" />Attachment Interface · Micro Review</h2><span className="text-xs text-muted">Clinician review prototype</span></div>
    <div className="p-5 sm:p-7">
      <p className="max-w-3xl text-sm leading-7 text-muted">Inspect the original table above, then prepare a tooth-indexed attachment review. Movement amounts alone cannot establish attachment need, design, omission or placement.</p>
      {demo ? <p className="mt-4 rounded-lg border border-brand/20 bg-brand-soft p-4 text-sm leading-7 text-brand">Synthetic demonstration — all candidate, alternative and no-attachment decisions are supplied fictional data. The engine and Groq do not select them.</p>
        : <p className="mt-4 rounded-lg border border-notice-line bg-notice p-4 text-sm leading-7 text-notice-ink">Vendor semantics and attachment policies are unapproved. Ordinary input receives unknown or withheld rows, with no invented attachment choices.</p>}
      <button type="button" className="button mt-5 bg-brand text-white disabled:opacity-60" disabled={loading} onClick={() => void review()} aria-describedby="attachment-privacy">{loading ? 'Preparing attachment review…' : 'Run Attachment Review'}<ArrowRight size={16} aria-hidden="true" /></button>
      <p id="attachment-privacy" className="mt-3 text-xs leading-6 text-muted">Explicit run only. The backend rechecks source evidence and existing safeguards. This module uses deterministic wording and makes no LLM call.</p>
      {loading && <p role="status" className="mt-3 text-sm text-muted">Checking attachment evidence and preparing the DRAFT…</p>}
      {error && <p role="alert" className="mt-4 text-sm text-notice-ink">{error}</p>}
      {!draft && !loading && !error && <p className="mt-6 rounded-lg bg-canvas p-5 text-sm text-muted">Your attachment review table will appear here after you run the review.</p>}
      {draft && <article aria-label="Attachment review draft" className="mt-7 border-t border-line pt-6">
        <h3 ref={heading} tabIndex={-1} className="text-2xl font-semibold tracking-tight">Attachment review draft</h3>
        <p className="mt-3 text-sm font-semibold text-notice-ink">{draft.draft_status}</p>
        <p className="mt-3 text-sm leading-7 text-muted">{draft.evidence_domain === 'TEST_ONLY' ? 'Finova Synthetic Attachment Demonstration — TEST_ONLY. Supplied choices are illustrative, not approved treatment policies.' : 'Unverified input — attachment recommendations unavailable.'}</p>
        <p className="mt-2 text-sm leading-7 text-muted">Unknown and withheld do not mean no attachment. A supplied no-attachment row is an explicit fictional decision, never an inference from missing or zero movement.</p>
        <div className="my-5 flex flex-wrap gap-2" aria-label="Attachment result summary">{(['CANDIDATE', 'ALTERNATIVE', 'NOT_INDICATED', 'UNKNOWN', 'WITHHELD'] as const).map(type => <span key={type} className="rounded-md border border-line bg-canvas px-3 py-2 text-xs">{LABELS[type]}: {draft.entries.filter(e => e.result_type === type).length}</span>)}</div>
        <div role="region" aria-label="Tooth-indexed attachment table" tabIndex={0} className="max-h-[40rem] overflow-auto rounded-xl border border-line">
          <table className="attachment-table w-full table-fixed text-left text-sm leading-6 sm:min-w-[850px]">
            <caption className="sr-only">Original tooth tokens, supplied synthetic attachment options or explicit unavailable states. All entries remain DRAFT and not clinically approved.</caption>
            <thead className="sticky top-0 z-10 bg-canvas text-xs text-muted"><tr><th scope="col" className="w-[13%] p-4">Original tooth</th><th scope="col" className="w-[22%] p-4">Review result</th><th scope="col" className="w-[25%] p-4">Option / supplied decision</th><th scope="col" className="w-[40%] p-4">Explanation & evidence</th></tr></thead>
            <tbody>{draft.entries.map((e, i) => <tr key={e.entry_id} className="border-t border-line align-top">
              <th scope="row" className="p-4 font-semibold"><span aria-hidden="true" className="sm:hidden">Original tooth </span><span className="raw-text">{e.original_tooth ?? 'Unresolved'}</span><span className="mt-1 block text-xs font-normal text-muted">{e.evidence_status === 'TEST_ONLY' ? 'Opaque demo identity' : 'Unverified token'}</span></th>
              <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted sm:hidden">Review result</span><span className={`inline-block rounded-md px-2 py-1 text-xs font-semibold ${e.decision_origin === 'SUPPLIED_SYNTHETIC' ? 'bg-brand-soft text-brand' : 'bg-notice text-notice-ink'}`}>{LABELS[e.result_type]}</span><p className="mt-2 text-xs text-muted">{e.decision_origin === 'SUPPLIED_SYNTHETIC' ? 'Supplied TEST_ONLY decision' : 'No attachment decision'}</p><p className="mt-1 text-xs text-muted">NOT APPROVED · DRAFT</p></td>
              <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted sm:hidden">Option / supplied decision</span><p className="font-medium">{e.design?.label ?? (e.result_type === 'NOT_INDICATED' ? 'No attachment — supplied demonstration decision' : 'No authorized option')}</p>{e.design && <p className="raw-text mt-2 text-xs text-muted">{e.design.design_id}</p>}{e.alternative_for && <p className="mt-2 text-xs text-muted">Alternative to {draft.entries.find(c => c.entry_id === e.alternative_for)?.design?.label ?? 'linked candidate'}; no superiority claim.</p>}</td>
              <td className="p-4"><span aria-hidden="true" className="mb-2 block text-xs font-semibold text-muted sm:hidden">Explanation & evidence</span><p className="text-xs leading-6">{e.explanation}</p><details className="mt-3 text-xs leading-6 text-muted"><summary className="cursor-pointer font-medium">Details & provenance · row {i + 1}</summary>
                <p className="mt-2">Verified tooth: {e.verified_tooth ?? 'UNKNOWN'}. Synthetic identity: {e.synthetic_tooth ?? 'UNAVAILABLE'}.</p>
                {e.design ? <><p className="raw-text">Category: {e.design.category_id}</p><p>Supplied shape: {e.design.shape ?? 'UNKNOWN'}; orientation: {e.design.orientation ?? 'UNKNOWN'}</p><p>{e.design.dimensions ? `Supplied dimensions: ${e.design.dimensions.x} × ${e.design.dimensions.y} × ${e.design.dimensions.z} mm` : 'Dimensions: UNKNOWN — no values inferred.'}</p></> : <p>Design, shape, dimensions and orientation: UNKNOWN or not applicable to the supplied no-attachment decision. No geometry inferred.</p>}
                <p>{e.placement ? `Supplied surface: ${e.placement.surface_id}; frame: ${e.placement.frame_id}; stage reference: ${e.placement.stage_ref ?? 'UNKNOWN'}. Illustrative only; no stage schedule or placement validation.` : 'Placement, surface and stage: UNKNOWN; no placement validation.'}</p>
                <p className="raw-text mt-2">Lexical measurement refs: {e.measurement_refs.join(', ') || 'None'}</p><p className="raw-text">Authorized observation refs: {e.observation_refs.join(', ') || 'None'}</p>
                <p className="raw-text">Evidence: {e.evidence_refs.join('; ') || 'No accepted attachment evidence'}</p><p className="raw-text">Safeguard finding refs (not candidate triggers): {e.finding_refs.join(', ')}</p><p className="raw-text">Missing prerequisites: {e.missing_prerequisites.join(', ')}</p><p className="raw-text">Entry: {e.entry_id}</p>
              </details></td>
            </tr>)}</tbody>
          </table>
        </div>
        <section aria-label="Clinician attachment review" className="my-6 rounded-xl border border-notice-line bg-notice p-5"><h4 className="font-semibold text-notice-ink">Clinician review required</h4><p className="mt-2 text-sm leading-7 text-notice-ink">Inspect identity, actual attachment plan, clinical indication and geometry independently. No sign-off is recorded here. A05/H08 still withhold clinical geometry and omission judgments; supplied toy dimensions do not override these safeguards.</p><p className="mt-2 text-xs leading-6 text-notice-ink">All 96 engine rules remain accounted for. A01–A04 and R15 remain disabled; A06 does not select a superior option.</p></section>
        <div className="flex flex-wrap gap-3"><button type="button" className="button button-example" onClick={() => void copy()}><Copy size={15} aria-hidden="true" />Copy attachment DRAFT</button><button type="button" className="button button-clear" onClick={download}><Download size={15} aria-hidden="true" />Download attachment DRAFT (TXT)</button></div>
        {status && <p role="status" className="mt-3 text-sm leading-6 text-brand">{status}</p>}
        <details className="technical-details"><summary>Attachment scope & limitations</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{draft.limitations.map(l => <li key={l}>{l}</li>)}</ul></details>
        <details className="technical-details"><summary>Engine findings & safeguard ledger ({draft.engine_review.evaluations.length} rules)</summary><ul className="mt-3 space-y-2 text-xs leading-6">{draft.engine_review.evaluations.map(e => <li key={e.rule_id}>{e.rule_id} · {e.status} · {e.execution ?? 'Legacy'} · {e.approval_status ?? 'UNKNOWN'}</li>)}</ul><pre tabIndex={0} aria-label="Attachment provenance JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs">{JSON.stringify(draft, null, 2)}</pre></details>
        <details className="technical-details"><summary>Complete attachment DRAFT TXT preview</summary><pre tabIndex={0} aria-label="Attachment export preview" className="raw-text mt-3 max-h-96 overflow-auto text-xs leading-6">{draft.export_text}</pre></details>
      </article>}
    </div>
  </section>
}
