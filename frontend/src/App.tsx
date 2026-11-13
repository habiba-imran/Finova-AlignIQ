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

export default function App() {
  const [rawText, setRawText] = useState('')
  const source: SourceClaim = 'Unknown'
  const [context, setContext] = useState<ContextClaims>({ ...EMPTY_CONTEXT })
  const [confirmedSynthetic, setConfirmedSynthetic] = useState(false)
  const [result, setResult] = useState<AutomaticParseResult | null>(null)
  const [syntheticFixture, setSyntheticFixture] = useState<SyntheticFixture | undefined>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
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
            <span className="hidden sm:inline">TMT review workspace</span>
            <span className="rounded-md border border-line bg-canvas px-2.5 py-1.5 tracking-wide">PHASE 5</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[1320px] px-5 pb-10 pt-8 sm:px-9 sm:pt-11">
        <div className="mb-5 flex items-center gap-2 text-xs font-semibold tracking-[0.13em] text-brand">
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-brand-soft text-[11px] tracking-normal">01</span>
          RAW TEXT INTAKE
        </div>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-[-0.035em] sm:text-[40px] sm:leading-tight">Start with the source.</h1>
            <p className="mt-3 max-w-2xl text-[15px] leading-7 text-muted">A workspace for pasted Tooth Movement Table (TMT) text.<br className="hidden sm:block" /> Parse recognizable structure while keeping source semantics explicitly unverified.</p>
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
        {result && <DraftReviewPanel key={`review-${revisionRef.current}`} rawText={rawText} source={source} context={context} rawHash={result.raw_sha256} recoveryReceipt={result.pipeline.recovery_receipt ?? undefined} />}

        <footer className="mt-7 flex flex-wrap justify-between gap-3 border-t border-line pt-5 text-xs leading-5 text-muted">
          <p className="flex items-center gap-2"><LockKeyhole size={14} aria-hidden="true" />Input stays in memory. Only server-authorized generated fixtures can use automatic development cloud recovery. Copy/download creates a local export.</p>
          <p>Finova AlignIQ <span aria-hidden="true">/</span> Internal prototype</p>
        </footer>
      </main>
    </div>
  )
}
