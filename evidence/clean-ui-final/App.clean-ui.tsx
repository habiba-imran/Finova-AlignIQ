import { useEffect, useRef, useState } from 'react'
import type { CSSProperties } from 'react'
import { ArrowRight, Check, FileText, FlaskConical, Info, LockKeyhole, Trash2 } from 'lucide-react'
import { SYNTHETIC_EXAMPLE } from './syntheticExample'
import { EMPTY_CONTEXT, MAX_TEXT_CHARACTERS, requestParse } from './api/parse'
import type { AutomaticParseResult, ContextClaims, SourceClaim, SyntheticFixture } from './api/parse'
import ContextFields from './components/ContextFields'
import ParseResults from './components/ParseResults'
import StructuredPreview from './components/StructuredPreview'
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

type Purpose = 'macro' | 'micro' | 'nano'

const MODULES: Record<Purpose, {
  code: string
  name: string
  kicker: string
  heading: string
  support: string
  reviewTitle: string
  demoLabel: string
  demoNote: string
}> = {
  macro: {
    code: 'MACRO',
    name: 'Planning',
    kicker: 'Macro · Planning',
    heading: 'Planning Assistant',
    support: 'Review programmed movements and prepare structured draft comments.',
    reviewTitle: 'Planning review',
    demoLabel: 'Load Finova planning demo',
    demoNote: 'Fixed TEST_ONLY data · no vendor or clinical validation implied.',
  },
  micro: {
    code: 'MICRO',
    name: 'Attachments',
    kicker: 'Micro · Attachments',
    heading: 'Attachment Review',
    support: 'Inspect tooth-wise attachment information and supporting evidence.',
    reviewTitle: 'Attachment review',
    demoLabel: 'Load Finova attachment demo',
    demoNote: 'Supplied fictional decisions · no clinical policy implied.',
  },
  nano: {
    code: 'NANO',
    name: 'Sequencing',
    kicker: 'Nano · Sequencing',
    heading: 'Sequencing Review',
    support: 'Review sequencing information, segment notes and anchorage context.',
    reviewTitle: 'Sequencing review',
    demoLabel: 'Load Finova sequencing demo',
    demoNote: 'Fictional sequencing and anchorage notes · no clinical strategy calculated.',
  },
}

const MODULE_ORDER: Purpose[] = ['macro', 'micro', 'nano']

export default function App({ diagnostics = new URLSearchParams(window.location.search).get('diagnostics') === '1' }: { diagnostics?: boolean }) {
  const [rawText, setRawText] = useState('')
  const source: SourceClaim = 'Unknown'
  const [context, setContext] = useState<ContextClaims>({ ...EMPTY_CONTEXT })
  const [result, setResult] = useState<AutomaticParseResult | null>(null)
  const [syntheticFixture, setSyntheticFixture] = useState<SyntheticFixture | undefined>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [purpose, setPurpose] = useState<Purpose>('macro')
  const [demo, setDemo] = useState<DemoInput | null>(null)
  const [attachmentDemo, setAttachmentDemo] = useState<AttachmentDemoInput | null>(null)
  const [sequencingDemo, setSequencingDemo] = useState<SequencingDemoInput | null>(null)
  const [complete, setComplete] = useState(false)
  const [unavailableDemos, setUnavailableDemos] = useState<Partial<Record<Purpose, boolean>>>({})
  const requestRef = useRef<AbortController | null>(null)
  const revisionRef = useRef(0)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  // Display counts only. Neither calculation changes the input or extracts TMT fields.
  const characterCount = Array.from(rawText).length
  const lineCount = rawText.length === 0 ? 0 : 1 + (rawText.match(/\r\n|\r|\n/g)?.length ?? 0)
  const copy = MODULES[purpose]

  useEffect(() => () => { revisionRef.current += 1; requestRef.current?.abort() }, [])
  useEffect(() => { document.title = `Finova AlignIQ · ${copy.heading}` }, [copy.heading])

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
    setSyntheticFixture(undefined)
    setRawText(value)
  }

  function editContext(value: ContextClaims) {
    invalidateParse()
    setContext(value)
  }

  async function parseInput() {
    if (rawText.length === 0 || characterCount > MAX_TEXT_CHARACTERS || requestRef.current) return
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
      setError(controller.signal.aborted ? 'Reading the table timed out. Your original text is preserved; please retry.'
        : code === 'SIZE_LIMIT' ? 'The table is too large to read. Your original text is preserved.'
          : code === 'REQUEST_INVALID' ? 'Check the table text and optional settings, then retry. Your original text is preserved.'
            : 'The table could not be read. Please retry. Your original text is preserved.')
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
        setRawText(value.parsed.raw_text); setContext(value.context)
        setSyntheticFixture(undefined); setDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) {
        if (e instanceof Error && ['DEMO_DISABLED', 'DEMO_UNAVAILABLE'].includes(e.message)) setUnavailableDemos(v => ({ ...v, macro: true }))
        setError('The planning demo is unavailable in this session. Your existing text is preserved.')
      }
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
        setRawText(value.parsed.raw_text); setContext(value.context)
        setSyntheticFixture(undefined); setAttachmentDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) {
        if (e instanceof Error && ['DEMO_DISABLED', 'DEMO_UNAVAILABLE'].includes(e.message)) setUnavailableDemos(v => ({ ...v, micro: true }))
        setError('The attachment demo is unavailable in this session. Your existing text is preserved.')
      }
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
        setRawText(value.parsed.raw_text); setContext(value.context)
        setSyntheticFixture(undefined); setSequencingDemo(value); setResult(value.parsed)
      }
    } catch (e) {
      if (revision === revisionRef.current) {
        if (e instanceof Error && ['DEMO_DISABLED', 'DEMO_UNAVAILABLE'].includes(e.message)) setUnavailableDemos(v => ({ ...v, nano: true }))
        setError('The sequencing demo is unavailable in this session. Your existing text is preserved.')
      }
    } finally {
      window.clearTimeout(timeout)
      if (revision === revisionRef.current) { requestRef.current = null; setLoading(false) }
    }
  }

  const inputReady = rawText.length > 0
  const currentStep = !inputReady ? 0 : !result ? 1 : !complete ? 2 : 3
  const stepStatus = (index: number) => {
    if (index < currentStep) return index === 0 ? 'Ready' : 'Complete'
    if (index > currentStep) return index === 3 ? 'After review' : 'Waiting'
    if (index === 0) return 'Add text'
    if (index === 1) return error ? 'Retry parse' : loading ? 'Parsing…' : 'Parse text'
    if (index === 2) return 'Run review'
    return 'Available'
  }
  const steps = ['Input', 'Inspection', copy.reviewTitle, 'Export'].map((title, index) => ({
    title,
    status: stepStatus(index),
    state: index < currentStep ? 'complete' : index === currentStep ? 'active' : 'pending',
  }))

  return (
    <div className="min-h-screen">
      <a href="#intake" className="skip-link">Skip to raw text input</a>
      <header className="border-b border-line bg-white">
        <div className="app-shell flex h-16 items-center justify-between gap-4">
          <div className="flex min-w-0 items-center gap-2.5">
            <img src="/favicon.svg" alt="" width="34" height="34" />
            <div className="whitespace-nowrap text-[19px] tracking-tight"><span className="font-bold">Finova</span> <span className="font-medium text-brand">AlignIQ</span></div>
          </div>
        </div>
      </header>

      <main className="app-shell pb-10 pt-7 sm:pt-9">
        <div className="max-w-3xl" key={purpose}>
          <p className="motion-swap text-[11px] font-semibold uppercase tracking-[0.16em] text-brand">{copy.kicker}</p>
          <h1 className="motion-swap mt-1.5 text-[28px] font-semibold leading-tight tracking-[-0.03em] sm:text-[32px]">{copy.heading}</h1>
          <p className="motion-swap mt-2 max-w-2xl text-[15px] leading-6 text-muted">{copy.support}</p>
        </div>

        <div className="mt-5">
          <nav aria-label="Review purpose" className="module-tabs" style={{ '--module-index': MODULE_ORDER.indexOf(purpose) } as CSSProperties}>
            <span aria-hidden="true" className="module-tab-indicator" />
            {MODULE_ORDER.map(id => {
              const module = MODULES[id]
              return <button
                type="button"
                key={id}
                aria-pressed={purpose === id}
                onClick={() => { if (purpose !== id) { invalidateParse(); setPurpose(id) } }}
                className={`module-tab ${purpose === id ? 'module-tab-active' : ''}`}
              >
                <span className="module-tab-code">{module.code}</span>
                <span className="module-tab-label">{module.name}</span>
                <span className="sr-only">. {module.heading}</span>
              </button>
            })}
          </nav>
          <p className="mt-2 text-xs leading-5 text-muted">Prototype — not for clinical use. All reports require independent orthodontist review.</p>
        </div>

        <ol aria-label="Planning workflow" className="workflow-steps mt-4">
          {steps.map((step, index) => <li key={step.title} data-state={step.state} aria-current={index === currentStep ? 'step' : undefined} className="workflow-step">
            <span className="workflow-index" aria-hidden="true">{step.state === 'complete' ? <Check size={14} /> : String(index + 1).padStart(2, '0')}</span>
            <span className="min-w-0">
              <span className="workflow-title">{step.title}</span>
              <span className="workflow-state">{step.status}{step.state === 'complete' && <span className="sr-only"> — completed</span>}</span>
            </span>
          </li>)}
        </ol>

        <section aria-labelledby="input-area-heading" className="mt-6">
          <div className="section-heading flex-col items-start justify-between gap-3 lg:flex-row lg:items-start">
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
              <span className="section-number">01</span>
              <h2 id="input-area-heading" className="section-title">Input</h2>
              <p className="section-note">Paste TMT text, then parse to populate the structured table.</p>
            </div>
            <div className="flex w-full flex-col items-start gap-1 lg:w-auto lg:items-end">
              <button type="button" className="button button-accent" aria-describedby="demo-availability" onClick={() => void (purpose === 'nano' ? loadSequencingDemo() : purpose === 'micro' ? loadAttachmentDemo() : loadPlanningDemo())} disabled={loading || unavailableDemos[purpose]}><FlaskConical size={15} aria-hidden="true" />{copy.demoLabel}</button>
              <p id="demo-availability" className="text-xs leading-5 text-muted">{unavailableDemos[purpose] ? 'Demo unavailable in this session.' : 'Fixed fictional example'}</p>
            </div>
          </div>

          <div className="workspace-grid grid min-w-0 gap-4 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
            <section aria-labelledby="input-heading" className="panel min-w-0">
              <div className="panel-heading">
                <div className="flex items-center gap-2.5"><FileText size={17} className="text-brand" aria-hidden="true" /><h3 id="input-heading" className="panel-title">Paste TMT text</h3></div>
                <span className="section-kicker">Raw input</span>
              </div>
              <div className="p-5 sm:p-6">
                <p className="mb-4 text-xs leading-5 text-muted">Source indicators and layout are detected when you parse.</p>
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
                  className="raw-text block min-h-60 w-full resize-y rounded-lg border border-field bg-canvas p-4 text-[13px] leading-6 placeholder:text-placeholder"
                />
                <div className="mt-3 flex flex-wrap justify-between gap-2 text-xs leading-5 text-muted">
                  <p id="input-hint">No cleanup or column alignment is applied.</p>
                  <p id="input-counts" role="status" aria-live="polite" aria-atomic="true" className="tabular-nums">{characterCount.toLocaleString()} {characterCount === 1 ? 'character' : 'characters'} <span aria-hidden="true">·</span> {lineCount.toLocaleString()} {lineCount === 1 ? 'line' : 'lines'}</p>
                </div>
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  <button type="button" onClick={loadExample} className="button button-secondary"><FlaskConical size={15} aria-hidden="true" />Load synthetic example</button>
                  {diagnostics && <><button type="button" onClick={() => { editRawText(syntheticCatalog.fixtures.find(f => f.id === 'synthetic-markdown-rows')!.raw_text); setContext({ ...EMPTY_CONTEXT }); inputRef.current?.focus() }} className="button button-secondary">Load synthetic Markdown example</button>
                  <button type="button" onClick={() => { editRawText(generatedExample.raw_text); setSyntheticFixture(generatedExample.identity); setContext({ ...EMPTY_CONTEXT }); inputRef.current?.focus() }} className="button button-secondary">Load generated recovery example</button></>}
                  <button type="button" onClick={clearText} disabled={rawText.length === 0} className="button button-danger"><Trash2 size={14} aria-hidden="true" />Clear</button>
                </div>
                <ContextFields value={context} onChange={editContext} />
              </div>
            </section>

            <StructuredPreview result={result} rawText={rawText} loading={loading} showRawEvidence={diagnostics} />
          </div>

          <section aria-label="Parse controls" aria-busy={loading} className="mt-4 rounded-xl border border-line bg-white p-5 shadow-panel sm:p-6">
            <div className="flex items-start gap-3">
              <Info size={17} className="mt-0.5 shrink-0 text-muted" aria-hidden="true" />
              <div>
                <h3 className="text-[15px] font-semibold">View your formatted table</h3>
                <p id="parse-hint" className="mt-1 text-xs leading-5 text-muted">Read the table before running a review. Your original text stays editable.</p>
              </div>
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-3">
              <button type="button" onClick={() => void parseInput()} disabled={loading || rawText.length === 0 || characterCount > MAX_TEXT_CHARACTERS} aria-describedby="parse-hint" className="button button-primary px-5">{loading ? <><span className="button-spinner" aria-hidden="true" />Parsing…</> : <>Parse Table<ArrowRight size={16} aria-hidden="true" /></>}</button>
              {diagnostics && <button type="button" disabled className="button button-secondary">Analyze</button>}
            </div>
            {characterCount > MAX_TEXT_CHARACTERS && <p role="alert" className="mt-3 text-sm text-notice-ink">Parsing is limited to 100,000 characters. Your full raw input is still retained.</p>}
            {loading && <p role="status" className="motion-status mt-3 text-sm text-muted">Parsing the submitted text structure…</p>}
            {error && <p role="alert" className="motion-status mt-3 text-sm text-notice-ink">{error}</p>}
            {result && <p role="status" className="motion-status mt-3 text-sm text-muted">Table read. Check marked values before running a review.</p>}
          </section>

        </section>

        {result && <section aria-labelledby="inspection-heading" className="mt-6">
          <div className="section-heading">
            <span className="section-number">02</span>
            <h2 id="inspection-heading" className="section-title">Movement inspection</h2>
            <p className="section-note">Missing and unknown values remain marked.</p>
          </div>
          <ParserStatus result={result} demonstration={!!(demo || attachmentDemo || sequencingDemo)} />
          {diagnostics && <ParseResults key={revisionRef.current} result={result} />}
        </section>}

        {result && <section aria-labelledby="review-area-heading" className="mt-6">
          <div className="section-heading">
            <span className="section-number">03</span>
            <h2 id="review-area-heading" className="section-title">Review results</h2>
            <p className="section-note">{complete ? 'Review the DRAFT below, then use the export area when ready.' : 'Run the review below to prepare a DRAFT.'}</p>
          </div>
          {purpose === 'macro' && <PlanningWorkspace key={`planning-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!demo} onComplete={setComplete} />}
          {purpose === 'micro' && <AttachmentWorkspace key={`attachment-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!attachmentDemo} onComplete={setComplete} />}
          {purpose === 'nano' && <SequencingWorkspace key={`sequencing-${revisionRef.current}`} rawText={rawText} context={context} parsed={result} demo={!!sequencingDemo} onComplete={setComplete} />}
          {diagnostics && purpose === 'macro' && !demo && <details className="technical-details"><summary>Advanced: separate engineering review & legacy report actions</summary><DraftReviewPanel key={`review-${revisionRef.current}`} rawText={rawText} source={source} context={context} rawHash={result.raw_sha256} recoveryReceipt={result.pipeline.recovery_receipt ?? undefined} /></details>}
        </section>}

        <footer className="mt-8 flex flex-wrap justify-between gap-3 border-t border-line pt-5 text-xs leading-5 text-muted">
          <p className="flex items-center gap-2"><LockKeyhole size={14} aria-hidden="true" />Input stays in memory. Exports are saved locally.</p>
          <p>Finova AlignIQ{diagnostics ? ' / Internal diagnostics' : ''}</p>
        </footer>
      </main>
    </div>
  )
}
