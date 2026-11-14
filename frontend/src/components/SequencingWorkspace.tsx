import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Copy, Download, ListOrdered } from 'lucide-react'
import type { AutomaticParseResult, ContextClaims } from '../api/parse'
import { requestSequencingDraft, SEQUENCE_SECTIONS } from '../api/sequencing'
import type { SequenceEntry, SequenceSection, SequencingDraft } from '../api/sequencing'
import { EvidenceDisclosure, ExportBar, ReportHeader, ReportSection, SummaryGrid, SummaryMetric } from './ReportPrimitives'

const TITLES: Record<SequenceSection, string> = { UPPER_ARCH: 'Upper-arch sequencing', LOWER_ARCH: 'Lower-arch sequencing', SEGMENTS: 'Segments & tooth groups', RIGHT_ANCHORAGE: 'Right-side anchorage', LEFT_ANCHORAGE: 'Left-side anchorage', UNAVAILABLE: 'Unavailable assessments' }
const LABELS: Record<SequenceEntry['result_type'], string> = { SUPPLIED_SYNTHETIC: 'Supplied fictional statement', STRUCTURAL_OBSERVATION: 'Structural metadata check · TEST_ONLY', UNKNOWN: 'Unknown', WITHHELD: 'Withheld', DISABLED: 'Disabled clinical decision' }

function Note({ note, report }: { note: SequenceEntry; report: SequencingDraft }) {
  const arch = note.synthetic_arch_id ? report.fictional_arches.find(a => a.arch_id === note.synthetic_arch_id) : null
  return <li className="min-w-0 rounded-lg border border-line bg-white p-4">
    <div className="mb-2 flex flex-wrap items-center gap-1.5">
      <span className={`report-badge ${note.result_type === 'SUPPLIED_SYNTHETIC' ? 'report-badge-brand' : note.result_type === 'UNKNOWN' || note.result_type === 'WITHHELD' || note.result_type === 'DISABLED' ? 'report-badge-notice' : ''}`}>{LABELS[note.result_type]}</span>
      {arch && <span className="report-badge">{arch.label}</span>}
      {note.side !== 'UNKNOWN' && <span className="report-badge">{note.side === 'RIGHT' ? 'Right side' : 'Left side'}</span>}
      <span className="report-badge">DRAFT · Not approved</span>
    </div>
    <p className="whitespace-pre-wrap text-sm leading-7 [overflow-wrap:anywhere]">{note.text}</p>
    {note.synthetic_segment_id && <p className="mt-2 text-xs text-muted">Fictional segment: {report.fictional_segments.find(s => s.segment_id === note.synthetic_segment_id)?.label}</p>}
    <EvidenceDisclosure summary="Evidence & source details">
      <p>Origin: {note.origin} · {note.evidence_status} · NOT APPROVED · DRAFT</p>
      <p>Verified arch / segment / tooth: UNKNOWN. Supplied fictional arch: {note.synthetic_arch_id ?? 'None'}; segment: {note.synthetic_segment_id ?? 'None'}; side: {note.side}.</p>
      <p>Original tooth tokens: {note.original_tooth_tokens.join(', ') || 'No anatomical assignment'}.</p>
      <p>Movement scope: {note.movement_scope}. Stage kinds: {note.stage_kinds.join(', ') || 'UNKNOWN'}.</p>
      <p>{note.stage_window ? `Supplied stage window IDs: ${note.stage_window.start_id} → ${note.stage_window.end_id}. No movement allocation or clinical schedule.` : 'Stage window unavailable. No order or simultaneous movement inferred.'}</p>
      {report.parsed.measurements.filter(m => note.measurement_refs.includes(m.id)).map(m => <p key={m.id} className="raw-text">{m.id} · {m.raw_label}: {m.raw_value ?? '(omitted cell)'}; lexical scalar {m.signed_decimal ?? 'unavailable'}; {m.numeric_status}. These values are not stage allocations.</p>)}
      <p className="raw-text mt-2">Evidence: {note.evidence_refs.join('; ') || 'No accepted sequencing evidence'}</p><p className="raw-text">Safeguard finding refs (not strategy triggers): {note.finding_refs.join(', ')}</p>
      <p className="raw-text">Missing prerequisites: {note.missing_prerequisites.join(', ')}</p><p className="raw-text">Entry: {note.entry_id}</p>
    </EvidenceDisclosure>
  </li>
}

export default function SequencingWorkspace({ rawText, context, parsed, demo, onComplete }: {
  rawText: string; context: ContextClaims; parsed: AutomaticParseResult; demo: boolean; onComplete: (value: boolean) => void
}) {
  const [report, setReport] = useState<SequencingDraft | null>(null), [loading, setLoading] = useState(false)
  const [error, setError] = useState(''), [status, setStatus] = useState('')
  const pending = useRef<AbortController | null>(null), revision = useRef(0), heading = useRef<HTMLHeadingElement>(null)
  useEffect(() => () => { revision.current++; pending.current?.abort() }, [])
  useEffect(() => { if (report) heading.current?.focus() }, [report])
  async function run() {
    if (pending.current) return
    const controller = new AbortController(), current = ++revision.current
    pending.current = controller; setReport(null); setError(''); setStatus(''); setLoading(true); onComplete(false)
    const timer = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const result = await requestSequencingDraft(rawText, context, parsed.raw_sha256, demo, controller.signal, parsed.pipeline.recovery_receipt ?? undefined)
      if (current === revision.current) { setReport(result); onComplete(true) }
    } catch (e) {
      if (current === revision.current) setError(controller.signal.aborted ? 'Sequencing review timed out. Your original text and parsed values are preserved. Retry when ready.'
        : e instanceof Error && e.message === 'REPARSE_REQUIRED' ? 'Recovery evidence expired or changed. Choose Parse Table again; your original text is preserved.'
          : 'Sequencing review could not return a valid draft. Your original text is preserved; check the backend and retry.')
    } finally { window.clearTimeout(timer); if (current === revision.current) { pending.current = null; setLoading(false) } }
  }
  async function copy() {
    if (!report) return
    const current = revision.current
    try { await navigator.clipboard.writeText(report.export_text); if (current === revision.current) setStatus('Sequencing DRAFT copied with statement origins, evidence and all limitations.') }
    catch { if (current === revision.current) setStatus('Clipboard access is unavailable. Download the TXT or copy the export preview.') }
  }
  function download() {
    if (!report) return
    try {
      const url = URL.createObjectURL(new Blob([report.export_text], { type: report.export_format }))
      const a = document.createElement('a'); a.href = url; a.download = `finova-sequencing-draft-${report.report_id.slice(0, 12)}.txt`
      document.body.append(a); a.click(); a.remove(); window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setStatus('Sequencing DRAFT TXT download requested.')
    } catch { setStatus('Download is unavailable. Copy the DRAFT or use the export preview.') }
  }
  const supplied = report?.entries.filter(e => e.result_type === 'SUPPLIED_SYNTHETIC').length ?? 0
  const structural = report?.entries.filter(e => e.result_type === 'STRUCTURAL_OBSERVATION').length ?? 0
  const withheld = report?.entries.filter(e => ['UNKNOWN', 'WITHHELD', 'DISABLED'].includes(e.result_type)).length ?? 0
  return <section className="panel" aria-labelledby="sequencing-heading">
    <div className="panel-heading">
      <div className="flex min-w-0 items-center gap-2.5"><ListOrdered size={17} className="shrink-0 text-brand" aria-hidden="true" /><h3 id="sequencing-heading" className="panel-title">Sequencer · Nano Review</h3></div>
      <div className="flex items-center gap-3"><span className="text-xs font-medium text-muted">Sequencing & anchorage context</span></div>
    </div>
    <div className="p-5 sm:p-7">
      <p className="max-w-3xl text-sm leading-7 text-muted">Inspect the original values above, then review available sequencing and anchorage context. Total movements do not establish a movement order, stage schedule, simultaneous movement or force plan.</p>
      <p className="mt-4 rounded-lg border border-notice-line bg-notice p-4 text-sm leading-7 text-notice-ink">{demo ? 'The fixed demo supplies fictional upper/lower identities, segment notes and right/left anchorage context. These statements are authored examples, not calculated clinical recommendations.' : 'Without verified arch, stage and clinical evidence, sequencing and anchorage advice remain unavailable. Parsed structure alone is insufficient.'}</p>
      <button type="button" className="button button-primary mt-5" disabled={loading} onClick={() => void run()} aria-describedby="sequencing-privacy">{loading ? <><span className="button-spinner" aria-hidden="true" />Preparing sequencing review…</> : <>Run Sequencing Review<ArrowRight size={16} aria-hidden="true" /></>}</button>
      <p id="sequencing-privacy" className="mt-3 text-xs leading-6 text-muted">Explicit run only. Existing source and clinical gates are rechecked. This module uses deterministic wording and makes no LLM call.</p>
      {loading && <p role="status" className="motion-status mt-3 text-sm text-muted">Checking source and stage evidence and preparing the DRAFT…</p>}
      {error && <p role="alert" className="motion-status mt-4 text-sm text-notice-ink">{error}</p>}
      {!report && !loading && !error && <p className="mt-6 rounded-lg bg-canvas p-5 text-sm text-muted">Your sequencing review will appear here after you run the review.</p>}
      {report && <article aria-label="Sequencing review draft" className="motion-enter mt-8 overflow-hidden rounded-2xl border border-line bg-white shadow-panel">
        <ReportHeader
          eyebrow="Nano · Sequencing review"
          title="Sequencing review draft"
          headingRef={heading}
          draftStatus={report.draft_status}
          badges={[
            { label: report.evidence_domain === 'TEST_ONLY' ? 'Synthetic · TEST_ONLY' : 'Unverified input', tone: 'brand' },
            { label: 'Not approved', tone: 'notice' },
          ]}
          summary={<>
            {report.synthetic_notice && <p className="rounded-lg border border-notice-line bg-notice p-3 text-sm font-semibold text-notice-ink">{report.synthetic_notice}</p>}
            <p className={`text-sm leading-7 text-muted ${report.synthetic_notice ? 'mt-2' : ''}`}>{report.evidence_domain === 'TEST_ONLY' ? 'Fictional sequencing notes are separated from structural stage observations.' : 'Unverified input — sequence order and anchorage recommendations remain unavailable.'}</p>
            <SummaryGrid label="Sequencing review summary">
              <SummaryMetric label="Supplied statements" value={supplied} detail="Fictional demo notes" />
              <SummaryMetric label="Structural checks" value={structural} detail="TEST_ONLY metadata only" />
              <SummaryMetric label="Unknown / withheld" value={withheld} detail="Unavailable, not negative" tone="notice" />
              <SummaryMetric label="Stage records" value={report.stage_inspection.records.length} detail="No movement binding" />
            </SummaryGrid>
          </>}
        />
        <div className="p-5 sm:p-7">
          <ReportSection
            label="Stage data availability"
            title={report.stage_inspection.status === 'SUPPLIED_SYNTHETIC_METADATA' ? 'Fictional stage metadata checked · movement data unavailable' : report.stage_inspection.status === 'INVALID' ? 'Stage metadata inconsistent · dependent statements withheld' : 'Actual stage data unavailable'}
            tone="notice"
            description={report.stage_inspection.explanation}
            className="mb-5"
          >
            <EvidenceDisclosure summary="Stage metadata & structural checks">
              <p>NO_STAGE_MOVEMENT_BINDING · {report.stage_inspection.status}</p>
              {report.stage_inspection.issues.length > 0 && <p>Issues: {report.stage_inspection.issues.join(', ')}</p>}
              <ul className="mt-2 space-y-2">{report.stage_inspection.records.map((s, i) => <li key={`${s.stage_id}-${i}`} className="raw-text">{s.stage_id} · supplied index {s.index} · {s.arch} · {s.kind} · {s.evidence_ref}</li>)}</ul>
              <p className="raw-text">Source: {report.stage_inspection.evidence_ref ?? 'No accepted stage dataset'}</p>
            </EvidenceDisclosure>
          </ReportSection>

          <div className="grid gap-4 lg:grid-cols-2">{SEQUENCE_SECTIONS.map(section => {
            const entries = report.entries.filter(e => e.section === section)
            return <ReportSection key={section} title={TITLES[section]} label={TITLES[section]} tone={section === 'UNAVAILABLE' ? 'notice' : 'default'} className={section === 'SEGMENTS' || section === 'UNAVAILABLE' ? 'lg:col-span-2' : ''} actions={<span className="report-badge">{entries.length} {entries.length === 1 ? 'entry' : 'entries'}</span>}>
              <ul className={`grid gap-3 ${section === 'SEGMENTS' || section === 'UNAVAILABLE' ? 'xl:grid-cols-2' : ''}`}>{entries.map(e => <Note key={e.entry_id} note={e} report={report} />)}</ul>
            </ReportSection>
          })}</div>

          <ReportSection title="Independent clinician review required" label="Independent clinician review" tone="notice" className="my-5" description="No clinical approval is recorded. Unknown anchorage does not mean anchorage is unnecessary. R13 and T01–T08 remain disabled; no force, auxiliary, stage allocation, timing or collision-free result is calculated.">
            <p className="text-xs leading-6 text-notice-ink">Supplied fictional statements remain separate from structural stage observations. No stage optimization, movement scheduling or force decision is implied.</p>
          </ReportSection>

          <ExportBar label="Sequencing export" title="Export" description="Copy or download the complete DRAFT with statement origins and limitations." notice={status || undefined}>
            <button type="button" className="button button-example" onClick={() => void copy()}><Copy size={15} aria-hidden="true" />Copy sequencing DRAFT</button>
            <button type="button" className="button button-secondary" onClick={download}><Download size={15} aria-hidden="true" />Download sequencing DRAFT (TXT)</button>
          </ExportBar>

          <details className="technical-details"><summary>Sequencing scope & limitations</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{report.limitations.map(l => <li key={l}>{l}</li>)}</ul></details>
          <details className="technical-details"><summary>Source, engine findings & rule ledger ({report.engine_review.evaluations.length} rules)</summary><ul className="mt-3 space-y-2 text-xs leading-6">{report.engine_review.evaluations.map(e => <li key={e.rule_id}>{e.rule_id} · {e.status} · {e.execution ?? 'Legacy'} · {e.approval_status ?? 'UNKNOWN'}</li>)}</ul><pre tabIndex={0} aria-label="Sequencing provenance JSON" className="raw-text mt-4 max-h-96 overflow-auto text-xs">{JSON.stringify(report, null, 2)}</pre></details>
          <details className="technical-details"><summary>Complete sequencing DRAFT TXT preview</summary><pre tabIndex={0} aria-label="Sequencing export preview" className="raw-text mt-3 max-h-96 overflow-auto text-xs leading-6">{report.export_text}</pre></details>
        </div>
      </article>}
    </div>
  </section>
}
