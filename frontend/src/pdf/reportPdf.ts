import { PDFDocument, StandardFonts, rgb } from 'pdf-lib'
import type { Color, PDFFont, PDFPage } from 'pdf-lib'
import fontkit from '@pdf-lib/fontkit'
import regularBase64 from './assets/NotoSans-Regular.base64?raw'
import symbolsBase64 from './assets/NotoSansSymbols-Arrows.base64?raw'
import { isPlanningDraft } from '../api/planning'
import { isAttachmentDraft } from '../api/attachments'
import { isSequencingDraft } from '../api/sequencing'
import { isFinalDraftReport } from '../api/report'
import { buildPdfPresentation } from './presentation'

export type PdfKind = 'macro' | 'micro' | 'nano' | 'descriptive'
const TITLES: Record<PdfKind, string> = { macro: 'Planning review', micro: 'Attachment review', nano: 'Sequencing review', descriptive: 'Descriptive planning review' }
const TEAL = rgb(8 / 255, 124 / 255, 114 / 255), INK = rgb(0.10, 0.19, 0.23), MUTED = rgb(0.32, 0.40, 0.44)
const LINE = rgb(0.84, 0.89, 0.90), SOFT = rgb(0.94, 0.97, 0.97)
const WIDTH = 595.28, HEIGHT = 841.89, MARGIN = 42, BODY_WIDTH = WIDTH - MARGIN * 2, BOTTOM = 54
type LayoutFont = Pick<PDFFont, 'widthOfTextAtSize'>
const widthCaches = new WeakMap<LayoutFont, Map<string, number>>()

function validated(kind: PdfKind, data: unknown) {
  if (kind === 'macro' && isPlanningDraft(data)) return { data, report: data.report, text: data.export_text }
  if (kind === 'micro' && isAttachmentDraft(data)) return { data, report: data, text: data.export_text }
  if (kind === 'nano' && isSequencingDraft(data)) return { data, report: data, text: data.export_text }
  if (kind === 'descriptive' && isFinalDraftReport(data)) return { data, report: data, text: data.export_text }
  throw new Error('PDF_INVALID_REPORT')
}

/** Wrap without rounding, truncating tokens or changing source character order.
 * Layout whitespace may wrap; the embedded UTF-8 TXT preserves exact whitespace. */
export function wrapPdfText(text: string, font: LayoutFont, size: number, width: number): string[] {
  let cache = widthCaches.get(font)
  if (!cache) { cache = new Map(); widthCaches.set(font, cache) }
  const measure = (value: string) => {
    const key = `${size}:${value}`
    let result = cache.get(key)
    if (result === undefined) { result = font.widthOfTextAtSize(value, size); cache.set(key, result) }
    return result
  }
  const lines: string[] = []
  let line = ''
  for (const part of text.replaceAll('\t', '    ').split(/(\s+)/u)) {
    if (!part) continue
    if (measure(line + part) <= width) { line += part; continue }
    if (line) { lines.push(line); line = '' }
    // Long IDs, URLs and unbroken original tokens must wrap inside the cell.
    let remaining = [...part]
    while (remaining.length) {
      let low = 1, high = remaining.length, fit = 0
      while (low <= high) {
        const mid = Math.floor((low + high) / 2)
        if (measure(remaining.slice(0, mid).join('')) <= width) { fit = mid; low = mid + 1 }
        else high = mid - 1
      }
      if (!fit) throw new Error('PDF_CHARACTER_TOO_WIDE')
      const chunk = remaining.slice(0, fit).join(''); remaining = remaining.slice(fit)
      if (remaining.length) lines.push(chunk)
      else line = chunk
    }
  }
  if (line || !lines.length) lines.push(line)
  return lines
}

/** Entirely local. The same validators used by the UI gate PDF generation.
 * This is presentation only: no fetch, provider, numerical conversion or clinical rule. */
export async function createReportPdf(kind: PdfKind, input: unknown): Promise<Uint8Array> {
  const accepted = validated(kind, input)
  // Freeze the accepted snapshot before the first await; never export later edits.
  const json = JSON.stringify(accepted.data, null, 2)
  const { data, report, text } = validated(kind, JSON.parse(json))
  const presentation = buildPdfPresentation(kind, data)
  const exported = new Date(), exportDate = exported.toISOString().slice(0, 10) + ' UTC'
  const doc = await PDFDocument.create()
  doc.registerFontkit(fontkit)
  const font = await doc.embedFont(Uint8Array.from(atob(regularBase64.trim()), c => c.charCodeAt(0)), { subset: true })
  const bold = await doc.embedFont(StandardFonts.HelveticaBold)
  const symbols = await doc.embedFont(Uint8Array.from(atob(symbolsBase64.trim()), c => c.charCodeAt(0)), { subset: true })
  const visible = [...presentation.summary, ...presentation.blocks.flatMap(b => b.type === 'table' ? [...b.headers, ...b.rows.flat()] : [b.text]),
    ...presentation.limitations, ...presentation.missing.map(s => s.replaceAll('_', ' ')), ...presentation.referenceGuide].join('\n')
  const characters = new Set(font.getCharacterSet())
  const symbolCharacters = new Set(symbols.getCharacterSet())
  const unsupported = [...new Set([...visible].filter(c => !'\r\n\t'.includes(c) && !characters.has(c.codePointAt(0)!) && !symbolCharacters.has(c.codePointAt(0)!)))]
  if (unsupported.length) throw new Error(`PDF_UNSUPPORTED_GLYPH:${unsupported.map(c => `U+${c.codePointAt(0)!.toString(16).toUpperCase()}`).join(', ')}`)
  function runs(value: string) {
    const result: { text: string; font: PDFFont }[] = []
    for (const character of value) {
      const selected = characters.has(character.codePointAt(0)!) ? font : symbols
      const previous = result.at(-1)
      if (previous?.font === selected) previous.text += character
      else result.push({ text: character, font: selected })
    }
    return result
  }
  const layoutFont: LayoutFont = { widthOfTextAtSize: (value, size) => runs(value).reduce((sum, run) => sum + run.font.widthOfTextAtSize(run.text, size), 0) }
  function draw(value: string, x: number, baseline: number, size: number, color: Color) {
    for (const run of runs(value)) {
      page.drawText(run.text, { x, y: baseline, font: run.font, size, color })
      x += run.font.widthOfTextAtSize(run.text, size)
    }
  }
  doc.setTitle(`Finova AlignIQ - ${TITLES[kind]} - DRAFT`)
  doc.setAuthor('Finova AlignIQ'); doc.setSubject('Prototype report - NOT CLINICAL ADVICE')
  doc.setCreator('Finova AlignIQ local PDF export')
  doc.setCreationDate(exported); doc.setModificationDate(exported)
  let page: PDFPage, y = 0
  function newPage() {
    page = doc.addPage([WIDTH, HEIGHT]); y = HEIGHT - 91
    page.drawRectangle({ x: 0, y: HEIGHT - 8, width: WIDTH, height: 8, color: TEAL })
    page.drawText('Finova AlignIQ', { x: MARGIN, y: HEIGHT - 39, font: bold, size: 13, color: TEAL })
    page.drawText(`${TITLES[kind]} / DRAFT`, { x: MARGIN, y: HEIGHT - 57, font, size: 9, color: MUTED })
    page.drawText(`${report.report_id.slice(0, 12)} | ${exportDate}`, { x: WIDTH - MARGIN - 200, y: HEIGHT - 39, font, size: 8, color: MUTED })
    page.drawLine({ start: { x: MARGIN, y: HEIGHT - 68 }, end: { x: WIDTH - MARGIN, y: HEIGHT - 68 }, color: LINE, thickness: 0.6 })
  }
  function ensure(height: number) { if (y - height < BOTTOM) newPage() }
  function paragraph(value: string, size = 9.5, color = INK) {
    const lines = value.split(/\r\n|\n|\r/).flatMap(original => wrapPdfText(original, layoutFont, size, BODY_WIDTH))
    // Keep ordinary result/status paragraphs together; genuinely long text flows.
    if (lines.length * size * 1.48 <= 160) ensure(lines.length * size * 1.48)
    for (const line of lines) {
        ensure(size * 1.48)
        draw(line, MARGIN, y, size, color); y -= size * 1.48
    }
  }
  function heading(value: string) {
    ensure(100); y -= 8
    page.drawRectangle({ x: MARGIN, y: y - 7, width: BODY_WIDTH, height: 26, color: SOFT })
    page.drawText(value, { x: MARGIN + 9, y, font: bold, size: 10.5, color: TEAL }); y -= 28
  }
  function table(headers: string[], widths: number[], rows: string[][]) {
    const wrapCell = (cell: string, index: number) => cell.split(/\r\n|\n|\r/).flatMap(line => wrapPdfText(line, layoutFont, 8.6, widths[index] - 12))
    function row(cells: string[], header = false, offset = 0, count?: number) {
      const wrapped = cells.map(wrapCell)
      const max = count ?? Math.max(...wrapped.map(c => c.length))
      const height = max * 12 + 12
      let x = MARGIN
      cells.forEach((_, i) => {
        page.drawRectangle({ x, y: y - height, width: widths[i], height, color: header ? SOFT : rgb(1, 1, 1), borderColor: LINE, borderWidth: 0.5 })
        const content = offset > 0 && wrapped[i].length <= max ? wrapped[i] : wrapped[i].slice(offset, offset + max)
        content.forEach((line, n) => draw(line, x + 6, y - 15 - n * 12, 8.6, header ? TEAL : INK))
        x += widths[i]
      }); y -= height
    }
    function tablePage() { newPage(); paragraph('Results continued', 9, MUTED); y -= 8; row(headers, true) }
    ensure(Math.max(...headers.map((cell, i) => wrapCell(cell, i).length)) * 12 + 60)
    row(headers, true)
    for (const cells of rows) {
      const lineCount = Math.max(...cells.map((cell, i) => wrapCell(cell, i).length))
      if (lineCount * 12 + 12 < HEIGHT - 200) {
        if (y - (lineCount * 12 + 12) < BOTTOM) tablePage()
        row(cells)
      } else {
        // Split an oversized row explicitly; repeat column headers on every page.
        let offset = 0
        while (offset < lineCount) {
          if (y - 24 < BOTTOM) tablePage()
          const count = Math.min(lineCount - offset, Math.floor((y - BOTTOM - 12) / 12))
          row(cells, false, offset, count); offset += count
          if (offset < lineCount) tablePage()
        }
      }
    }
    y -= 10
  }
  newPage()
  paragraph(TITLES[kind], 22, TEAL); y -= 8
  paragraph(report.draft_status, 11)
  paragraph(report.engine_review.evidence_domain === 'TEST_ONLY'
    ? 'SYNTHETIC EXAMPLE - NOT CLINICAL ADVICE' : 'UNVERIFIED INPUT - NOT CLINICAL ADVICE', 10, TEAL)
  y -= 8
  paragraph(`Report ID: ${report.report_id}`, 8)
  paragraph(`Exported: ${exportDate} | Clinical analysis enabled: false`, 8)
  paragraph(`Input SHA-256: ${report.engine_review.raw_sha256}`, 8)
  heading('Executive summary')
  for (const item of presentation.summary) { paragraph(item); y -= 5 }
  paragraph('Concise review only. Full technical evidence and the complete original report are available in embedded report.txt / validated-report.json and existing TXT export. Reference keys below locate the exact source records.', 9, MUTED)
  for (const block of presentation.blocks) {
    if (block.type === 'heading') heading(block.text)
    else if (block.type === 'text') { paragraph(block.text); y -= 7 }
    else table(block.headers, block.widths, block.rows)
  }
  heading('Important warnings and clinical limitations')
  paragraph('Missing information is unknown, not normal or approved. No clinical sign-off is recorded.', 9.5, TEAL); y -= 5
  for (const limitation of presentation.limitations) { paragraph(limitation); y -= 4 }
  if (presentation.missing.length) {
    heading('Missing information')
    paragraph('All distinct missing requirements for the displayed results are listed once. Per-result associations remain in the referenced JSON records.', 9, MUTED); y -= 4
    paragraph(presentation.missing.map(s => s.replaceAll('_', ' ')).join('; ') + '.', 9)
  }
  heading('Source and evidence references')
  for (const guide of presentation.referenceGuide) { paragraph(guide, 9, MUTED); y -= 5 }
  paragraph('Embedded attachments retain the exact full TXT, validated JSON, source spans, missing requirements and complete 96-rule audit ledger. No technical record is deleted or altered by this concise presentation.', 9, MUTED)
  const pages = doc.getPages()
  pages.forEach((p, index) => {
    p.drawLine({ start: { x: MARGIN, y: 40 }, end: { x: WIDTH - MARGIN, y: 40 }, color: LINE, thickness: 0.6 })
    p.drawText(`DRAFT / NOT CLINICAL ADVICE | ${report.report_id.slice(0, 12)}`, { x: MARGIN, y: 26, font: bold, size: 7, color: TEAL })
    p.drawText(`Page ${index + 1} of ${pages.length}`, { x: WIDTH - MARGIN - 75, y: 26, font, size: 8, color: MUTED })
  })
  await doc.attach(new TextEncoder().encode(text), 'report.txt', { mimeType: 'text/plain', description: 'Exact unchanged UTF-8 report, including original whitespace.' })
  await doc.attach(new TextEncoder().encode(json), 'validated-report.json', { mimeType: 'application/json', description: 'Complete validated report snapshot; no extra clinical authority.' })
  return doc.save()
}
