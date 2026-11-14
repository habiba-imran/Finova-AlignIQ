import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Braces, FileText, FlaskConical, Info, LockKeyhole, ShieldAlert, Trash2 } from 'lucide-react'
import { SYNTHETIC_EXAMPLE } from './syntheticExample'
import { EMPTY_CONTEXT, MAX_TEXT_CHARACTERS, requestParse } from './api/parse'
import type { AutomaticParseResult, ContextClaims, SourceClaim, SyntheticFixture } from './api/parse'
import ContextFields from './components/ContextFields'
import ParseResults from './components/ParseResults'
import DraftReviewPanel from './components/DraftReviewPanel'
import ParserStatus from './components/ParserStatus'
import syntheticCatalog from '../../examples/parser-finalization-synthetic.json'
import generatedExample from './phase4Example.json'
import PlanningWorkspace from './components/PlanningWorkspace'
import { requestDemoInput } from './api/planning'
import type { DemoInput } from './api/planning'
import AttachmentWorkspace from './components/AttachmentWorkspace'
import { requestAttachmentDemoInput } from './api/attachments'
import type { AttachmentDemoInput } from './api/attachments'
import SequencingWorkspace from './components/SequencingWorkspace'
import { requestSequencingDemoInput } from './api/sequencing'
import type { SequencingDemoInput } from './api/sequencing'

export default function App() {
  const [rawText, setRawText] = useState('')
  const source: SourceClaim = 'Unknown'
  const [context, setContext] = useState<ContextClaims>({ ...EMPTY_CONTEXT })
  const [confirmedSynthetic, setConfirmedSynthetic] = useState(false)
  const [result, setResult] = useState<AutomaticParseResult | null>(null)
  const [syntheticFixture, setSyntheticFixture] = useState<SyntheticFixture | undefined>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [purpose, setPurpose] = useState<'macro' | 'micro' | 'nano'>('macro')
  const [demo, setDemo] = useState<DemoInput | null>(null)
  const [attachmentDemo, setAttachmentDemo] = useState<AttachmentDemoInput | null>(null)
  const [sequencingDemo, setSequencingDemo] = useState<SequencingDemoInput | null>(null)
  const [complete, setComplete] = useState(false)
  const requestRef = useRef<AbortController | null>(null)
  const revisionRef = useRef(0)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  // Display counts only. Neither calculation changes the input or extracts TMT fields.
  const characterCount = Array.from(rawText).length
  const lineCount = rawText.length === 0 ? 0 : 1 + (rawText.match(/\r\n|\r|\n/g)?.length ?? 0)

  useEffect(() => () => { revisionRef.current += 1; requestRef.current?.abort() }, [])

  function invalidateParse() {
    revisionRef.current += 1
    requestRef.current?.abort()
    requestRef.current = null
    setResult(null)
    setError(null)
    setLoading(false)
    setDemo(null)
    setAttachmentDemo(null)
    setSequencingDemo(null)
    setComplete(false)
  }

  function editRawText(value: string) {
    invalidateParse()
    setConfirmedSynthetic(false)
    setSyntheticFixture(undefined)
    setRawText(value)
  }

  function editContext(value: ContextClaims) {
    invalidateParse()
    setContext(value)
  }

  async function parseInput() {
    if (!confirmedSynthetic || rawText.length === 0 || characterCount > MAX_TEXT_CHARACTERS || requestRef.current) return
    const controller = new AbortController()
    const revision = ++revisionRef.current
    requestRef.current = controller
    setLoading(true)
    setError(null)
    setResult(null)
    setDemo(null)
    setAttachmentDemo(null)
    setSequencingDemo(null)
    setComplete(false)
    const timeout = window.setTimeout(() => controller.abort(), syntheticFixture ? 35_000 : 20_000)
    try {
      const parsed = await requestParse(rawText, source, context, controller.signal, syntheticFixture)
      if (revision === revisionRef.current) setResult(parsed)
    } catch (failure) {
      if (revision !== revisionRef.current) return
      const code = failure instanceof Error ? failure.message : ''
      setError(controller.signal.aborted ? 'The parse request timed out. Your raw input is preserved; you can retry.'
        : code === 'SIZE_LIMIT' ? 'The request exceeded the parser size limit. Your raw input is preserved.'
          : code === 'REQUEST_INVALID' ? 'The parser rejected the request fields. Check metadata, text limits, and synthetic-data confirmation. Your raw input is preserved.'
            : 'The parser could not return a valid result. Check that the local backend is running and retry. Your raw input is preserved.')
    } finally {
      window.clearTimeout(timeout)
      if (revision === revisionRef.current) {
        requestRef.current = null
        setLoading(false)
      }
    }
  }

  function clearText() {
    editRawText('')
    inputRef.current?.focus()
  }

  function loadExample() {
    editRawText(SYNTHETIC_EXAMPLE)
    setContext({ ...EMPTY_CONTEXT })
    inputRef.current?.focus()
  }

  async function loadPlanningDemo() {
    invalidateParse()
    const controller = new AbortController(), revision = ++revisionRef.current
    requestRef.current = controller; setLoading(true)
    const timeout = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const value = await requestDemoInput(controller.signal)
      if (revision === revisionRef.current) {
        setRawText(value.parsed.raw_text); setContext(value.context); setConfirmedSynthetic(true)
        setSyntheticFixture(undefined); setDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) setError(e instanceof Error && e.message === 'DEMO_DISABLED'
        ? 'The synthetic planning demonstration is disabled on this backend. Use a development server configured for the fixed demonstration. Your existing text is preserved; ordinary pasted text cannot gain demonstration authority.'
        : 'The fixed demonstration could not be loaded. Your existing text is preserved. Check the backend and retry.')
    } finally {
      window.clearTimeout(timeout)
      if (revision === revisionRef.current) { requestRef.current = null; setLoading(false) }
    }
  }

  async function loadAttachmentDemo() {
    invalidateParse()
    const controller = new AbortController(), revision = ++revisionRef.current
    requestRef.current = controller; setLoading(true)
    const timeout = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const value = await requestAttachmentDemoInput(controller.signal)
      if (revision === revisionRef.current) {
        setRawText(value.parsed.raw_text); setContext(value.context); setConfirmedSynthetic(true)
        setSyntheticFixture(undefined); setAttachmentDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) setError(e instanceof Error && e.message === 'DEMO_DISABLED'
        ? 'The synthetic attachment demonstration is disabled on this backend. Use a development server configured for the fixed demonstration. Your existing text is preserved.'
        : 'The fixed attachment demonstration could not be loaded. Your existing text is preserved. Check the backend and retry.')
    } finally {
      window.clearTimeout(timeout)
      if (revision === revisionRef.current) { requestRef.current = null; setLoading(false) }
    }
  }

  async function loadSequencingDemo() {
    invalidateParse()
    const controller = new AbortController(), revision = ++revisionRef.current
    requestRef.current = controller; setLoading(true)
    const timeout = window.setTimeout(() => controller.abort(), 20_000)
    try {
      const value = await requestSequencingDemoInput(controller.signal)
      if (revision === revisionRef.current) {
        setRawText(value.parsed.raw_text); setContext(value.context); setConfirmedSynthetic(true)
        setSyntheticFixture(undefined); setSequencingDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) setError(e instanceof Error && e.message === 'DEMO_DISABLED'
        ? 'The synthetic sequencing demonstration is disabled on this backend. Use a development server configured for the fixed demonstration. Your existing text is preserved.'
        : 'The fixed sequencing demonstration could not be loaded. Your existing text is preserved. Check the backend and retry.')
    } finally {
      window.clearTimeout(timeout)
      if (revision === revisionRef.current) { requestRef.current = null; setLoading(false) }
    }
  }

  return (
    <div className="min-h-screen">
      <a href="#intake" className="skip-link">Skip to raw text input</a>
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-[1320px] flex-wrap items-center justify-between gap-4 px-5 py-5 sm:px-9">
          <div className="flex items-center gap-3">
            <img src="/favicon.svg" alt="" width="40" height="40" />
            <div className="text-[21px] tracking-tight"><span className="font-bold">Finova</span> <span className="font-medium text-brand">AlignIQ</span></div>
          </div>
          <div className="flex items-center gap-3 text-xs font-medium text-muted">
            <span className="hidden sm:inline">Planning workspace</span>
            <span className="rounded-md border border-line bg-canvas px-2.5 py-1.5 tracking-wide">SYNTHETIC PROTOTYPE</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[1320px] px-5 pb-10 pt-8 sm:px-9 sm:pt-11">
        <p className="mb-3 text-xs font-semibold tracking-[0.16em] text-brand">{purpose === 'nano' ? 'SEQUENCER' : purpose === 'micro' ? 'ATTACHMENT INTERFACE' : 'PLANNING ASSISTANT'}</p>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-[-0.035em] sm:text-[40px] sm:leading-tight">A clearer view of the plan.</h1>
            <p className="mt-3 max-w-2xl text-[15px] leading-7 text-muted">Inspect tooth movements, review traceable observations and prepare descriptive DRAFT comments for communication.</p>
          </div>
          <span className="mb-1 flex items-center gap-2 text-xs font-medium text-muted"><LockKeyhole size={14} aria-hidden="true" /> No input persistence</span>
        </div>

        <aside aria-label="Prototype safety notice" className="my-7 flex items-start gap-3 rounded-xl border border-notice-line bg-notice px-5 py-4">
          <ShieldAlert className="mt-0.5 shrink-0 text-notice-ink" size={19} aria-hidden="true" />
          <div className="text-sm leading-6 text-notice-ink">
            <p className="font-semibold">Prototype — not for clinical use</p>
            <p>Use synthetic text only. Do not paste real patient data. Parsing recognizes text structure; it does not verify vendor semantics or clinically assess your input.</p>
          </div>
        </aside>

        <section aria-labelledby="purpose-heading" className="mb-6">
          <h2 id="purpose-heading" className="mb-2 text-sm font-semibold">Choose a review purpose</h2>
          <p className="mb-4 text-xs leading-6 text-muted">Review passes are flexible planning purposes, not aligner stages or a prescribed number of modifications. Your choice does not authorize clinical assessments.</p>
          <nav aria-label="Review purpose" className="grid gap-3 md:grid-cols-3">{([
            ['macro', 'Macro', 'Planning Assistant', 'Major sagittal, transverse & vertical review'],
            ['micro', 'Micro', 'Attachment Interface', 'Tooth-indexed attachment evidence & review'],
            ['nano', 'Nano', 'Sequencer', 'Sequencing, segments & anchorage context'],
          ] as const).map(([id, title, subtitle, description]) => <button type="button" key={id} aria-pressed={purpose === id} onClick={() => { if (purpose !== id) { invalidateParse(); setPurpose(id) } }} className={`purpose-card ${purpose === id ? 'purpose-active' : ''}`}><span className="text-xs font-semibold tracking-widest text-brand">{title.toUpperCase()}</span><span className="mt-2 block text-sm font-semibold">{subtitle}</span><span className="mt-1 block text-xs leading-6 text-muted">{description}</span></button>)}</nav>
        </section>
        <ol aria-label="Planning workflow" className="workflow-steps mb-6">{['Paste TMT', 'Inspect movements', purpose === 'nano' ? 'Run sequencing review' : purpose === 'micro' ? 'Run attachment review' : 'Run assistant', 'Review & export'].map((label, i) => <li key={label} aria-current={(complete ? i === 3 : result ? i === 2 : i === 0) ? 'step' : undefined}><span aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>{label}</li>)}</ol>
        <aside className="mb-5 flex flex-wrap items-center justify-between gap-4 rounded-xl border border-brand/20 bg-brand-soft p-5"><div><h2 className="text-sm font-semibold text-brand">Try the complete synthetic workflow</h2><p className="mt-1 max-w-2xl text-xs leading-6 text-muted">{purpose === 'nano' ? 'The fixed Nano demo contains supplied fictional arch, segment and anchorage notes, checked stage metadata and explicit withholding. No clinical strategy is calculated.' : purpose === 'micro' ? 'The fixed attachment demo contains supplied candidates, an alternative, a supplied no-attachment decision, unknown and withheld rows. No clinical policy is implied.' : 'The fixed Finova demo includes authorized TEST_ONLY descriptions and a deliberately withheld value. No vendor or clinical validation is implied.'}</p></div><button type="button" className="button border border-brand/30 bg-white text-brand disabled:opacity-50" onClick={() => void (purpose === 'nano' ? loadSequencingDemo() : purpose === 'micro' ? loadAttachmentDemo() : loadPlanningDemo())} disabled={loading}><FlaskConical size={16} aria-hidden="true" />{purpose === 'nano' ? 'Load Finova sequencing demo' : purpose === 'micro' ? 'Load Finova attachment demo' : 'Load Finova planning demo'}</button></aside>
        {demo && <details className="technical-details mb-5"><summary>Finova Synthetic Demonstration · conventions & scope</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{demo.convention.map(c => <li key={c}>{c}</li>)}</ul></details>}
        {attachmentDemo && <details className="technical-details mb-5"><summary>Finova Synthetic Attachment Demonstration · conventions & scope</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{attachmentDemo.convention.map(c => <li key={c}>{c}</li>)}</ul></details>}
        {sequencingDemo && <details className="technical-details mb-5"><summary>Finova Synthetic Sequencer Demonstration · conventions & scope</summary><ul className="mt-3 list-disc space-y-2 pl-5 text-xs leading-6 text-muted">{sequencingDemo.convention.map(c => <li key={c}>{c}</li>)}</ul></details>}

        <div className="workspace-grid grid min-w-0 gap-5 lg:grid-cols-2">
          <section aria-labelledby="input-heading" className="panel min-w-0">
            <div className="panel-heading">
              <div className="flex items-center gap-2.5"><FileText size={18} className="text-brand" aria-hidden="true" /><h2 id="input-heading" className="font-semibold">Paste TMT text</h2></div>
              <span className="text-xs text-muted">Input</span>
            </div>
            <div className="p-5 sm:p-6">
              <p className="mb-5 text-xs leading-5 text-muted">Source indicators and layout are detected when you parse. Vendor compatibility remains unverified.</p>
              <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                <label htmlFor="intake" className="text-sm font-medium">Raw TMT text</label>
                <span className="text-xs text-muted">Plain text only</span>
              </div>
              <textarea
                ref={inputRef}
                id="intake"
                value={rawText}
                onChange={(event) => editRawText(event.target.value)}
                aria-describedby="input-hint input-counts"
                placeholder={'Paste synthetic TMT text here…\n\nTabs, uneven spacing, and blank lines are welcome.'}
                spellCheck={false}
                autoComplete="off"
                autoCorrect="off"
                autoCapitalize="off"
                className="raw-text block min-h-72 w-full resize-y rounded-lg border border-field bg-canvas p-4 text-[13px] leading-6 placeholder:text-placeholder"
              />
              <div className="mt-3 flex flex-wrap justify-between gap-2 text-xs leading-5 text-muted">
                <p id="input-hint">No cleanup or column alignment is applied.</p>
                <p id="input-counts" role="status" aria-live="polite" aria-atomic="true" className="tabular-nums">{characterCount.toLocaleString()} {characterCount === 1 ? 'character' : 'characters'} <span aria-hidden="true">·</span> {lineCount.toLocaleString()} {lineCount === 1 ? 'line' : 'lines'}</p>
              </div>
              <div className="mt-5 flex flex-wrap items-center gap-2.5">
                <button type="button" onClick={loadExample} className="button button-example"><FlaskConical size={16} aria-hidden="true" />Load synthetic example</button>
                <button type="button" onClick={() => { editRawText(syntheticCatalog.fixtures.find(f => f.id === 'synthetic-markdown-rows')!.raw_text); setContext({ ...EMPTY_CONTEXT }); inputRef.current?.focus() }} className="button button-example">Load synthetic Markdown example</button>
                <button type="button" onClick={() => { editRawText(generatedExample.raw_text); setSyntheticFixture(generatedExample.identity); setContext({ ...EMPTY_CONTEXT }); inputRef.current?.focus() }} className="button button-example">Load generated recovery example</button>
                <button type="button" onClick={clearText} disabled={rawText.length === 0} className="button button-clear"><Trash2 size={15} aria-hidden="true" />Clear</button>
              </div>
              <ContextFields value={context} onChange={editContext} />
            </div>
          </section>

          <section aria-labelledby="preview-heading" className="panel flex min-w-0 flex-col">
            <div className="panel-heading">
              <div className="flex items-center gap-2.5"><Braces size={18} className="text-brand" aria-hidden="true" /><h2 id="preview-heading" className="font-semibold">Raw preview</h2></div>
              <span className="rounded-md bg-canvas px-2 py-1 text-[11px] font-medium text-muted">TEXT ONLY</span>
            </div>
            <div className="relative m-5 flex min-h-80 flex-1 flex-col rounded-lg border border-line bg-canvas sm:m-6">
              <pre aria-label="Raw text preview" tabIndex={0} className="raw-text min-h-80 flex-1 p-4 text-[13px] leading-6">{rawText}</pre>
              {rawText.length === 0 && <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center px-7 text-center">
                <span className="mb-4 rounded-xl border border-line bg-white p-3 text-brand"><FileText size={24} strokeWidth={1.5} aria-hidden="true" /></span>
                <p className="text-sm font-medium">Your raw text will appear here</p>
                <p className="mt-2 max-w-64 text-xs leading-6 text-muted">Paste text or load the synthetic example to see a faithful, unparsed preview.</p>
              </div>}
            </div>
            <p className="px-5 pb-5 text-xs leading-5 text-muted sm:px-6 sm:pb-6">Spacing and line breaks are retained. Long rows wrap to fit.</p>
          </section>
        </div>

        <section aria-label="Parse controls" className="mt-5 rounded-xl border border-line bg-white px-5 py-5 sm:px-6">
          <div className="flex items-start gap-3"><Info size={17} className="mt-0.5 shrink-0 text-muted" aria-hidden="true" /><div><p className="text-sm font-medium">Parse structure, with evidence intact.</p><p id="parse-hint" className="mt-1 text-xs leading-5 text-muted">Parse Table sends unchanged text to this app’s backend. Arbitrary pasted input is processed by this app’s backend only. Server-authorized generated examples may use automatic Groq recovery when development testing is enabled. No input is saved.</p></div></div>
          <label className="my-4 flex cursor-pointer items-start gap-3 text-sm leading-6"><input type="checkbox" checked={confirmedSynthetic} onChange={event => { if (!event.target.checked) invalidateParse(); setConfirmedSynthetic(event.target.checked) }} className="mt-1 h-4 w-4 shrink-0 accent-brand" />I confirm this text is synthetic and contains no patient data.</label>
          <div className="flex flex-wrap items-center gap-3">
            <button type="button" onClick={() => void parseInput()} disabled={loading || !confirmedSynthetic || rawText.length === 0 || characterCount > MAX_TEXT_CHARACTERS} aria-describedby="parse-hint" className="button border border-brand bg-brand px-5 text-white enabled:hover:bg-[#06675f] disabled:border-line disabled:bg-canvas disabled:text-muted">{loading ? 'Parsing…' : 'Parse Table'}<ArrowRight size={16} aria-hidden="true" /></button>
            <button type="button" disabled aria-describedby="analysis-hint" className="button border border-line bg-canvas text-muted">Analyze</button>
            <p id="analysis-hint" className="text-xs text-muted">Clinical analysis is not implemented.</p>
          </div>
          {characterCount > MAX_TEXT_CHARACTERS && <p role="alert" className="mt-3 text-sm text-notice-ink">Parsing is limited to 100,000 characters. Your full raw input is still retained.</p>}
          {loading && <p role="status" className="mt-3 text-sm text-muted">Parsing the submitted text structure…</p>}
          {error && <p role="alert" className="mt-3 text-sm text-notice-ink">{error}</p>}
          {result && <p role="status" className="mt-3 text-sm text-muted">Parse response received. Source semantics remain unverified.</p>}
          {syntheticFixture && <p className="mt-3 text-xs leading-5 text-muted">Generated synthetic test input selected. The server must reproduce it exactly before any automatic external recovery.</p>}
        </section>

        {result && <ParserStatus result={result} />}
        {result && <ParseResults key={revisionRef.current} result={result} />}
        {result && purpose === 'macro' && <PlanningWorkspace key={`planning-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!demo} onComplete={setComplete} />}
        {result && purpose === 'micro' && <AttachmentWorkspace key={`attachment-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!attachmentDemo} onComplete={setComplete} />}
        {result && purpose === 'nano' && <SequencingWorkspace key={`sequencing-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!sequencingDemo} onComplete={setComplete} />}
        {result && purpose === 'macro' && !demo && <details className="technical-details"><summary>Advanced: separate engineering review & legacy report actions</summary><DraftReviewPanel key={`review-${revisionRef.current}`} rawText={rawText} source={source} context={context} rawHash={result.raw_sha256} recoveryReceipt={result.pipeline.recovery_receipt ?? undefined} /></details>}

        <footer className="mt-7 flex flex-wrap justify-between gap-3 border-t border-line pt-5 text-xs leading-5 text-muted">
          <p className="flex items-center gap-2"><LockKeyhole size={14} aria-hidden="true" />Input stays in memory. Only server-authorized generated fixtures can use automatic development cloud recovery. Copy/download creates a local export.</p>
          <p>Finova AlignIQ <span aria-hidden="true">/</span> Internal prototype</p>
        </footer>
      </main>
    </div>
  )
}
