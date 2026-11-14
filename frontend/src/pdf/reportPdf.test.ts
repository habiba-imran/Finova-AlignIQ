// @vitest-environment node
/// <reference types="node" />
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { afterEach, expect, test, vi } from 'vitest'
import { createReportPdf, wrapPdfText } from './reportPdf'
import type { PdfKind } from './reportPdf'
import macro from '../test/fixtures/planning-demo-draft.json'
import micro from '../test/fixtures/attachment-demo-draft.json'
import nano from '../test/fixtures/sequencer-demo-draft.json'
import ordinary from '../test/fixtures/attachment-unverified-draft.json'
import descriptive from '../test/fixtures/synthetic-final-report.json'
import interactiveMacro from '../test/fixtures/interactive-macro.json'
import interactiveMicro from '../test/fixtures/interactive-micro.json'
import interactiveNano from '../test/fixtures/interactive-nano.json'

const output = resolve('../evidence/polish/qa')
async function attachments(bytes: Uint8Array) {
  const pdf = await PDFDocument.load(bytes)
  const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
  const files: Record<string, string> = {}
  for (let i = 0; i < names.size(); i += 2) {
    const name = names.lookup(i, PDFHexString).decodeText()
    const spec = names.lookup(i + 1, PDFDict)
    const stream = pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream
    files[name] = new TextDecoder().decode(decodePDFRawStream(stream).decode())
  }
  return { pdf, files }
}
afterEach(() => vi.unstubAllGlobals())

test.each([interactiveMacro, interactiveMicro, interactiveNano])('interactive $module PDF preserves source facts and simulated status', async data => {
  const bytes = await createReportPdf('interactive', data)
  const { pdf, files } = await attachments(bytes)
  expect(files['report.txt']).toBe(data.export_text)
  expect(JSON.parse(files['validated-report.json'])).toEqual(data)
  expect(pdf.getPageCount()).toBeGreaterThan(1)
  const directory = resolve('../evidence/interactive-demo'); mkdirSync(directory, { recursive: true })
  writeFileSync(resolve(directory, `${data.module}.pdf`), bytes)
}, 30_000)

test.each<[PdfKind, unknown]>([['macro', macro], ['micro', micro], ['nano', nano], ['descriptive', descriptive]])(
  '%s creates a multipage PDF preserving exact TXT and all validated report data without network', async (kind, data) => {
    vi.stubGlobal('fetch', vi.fn(() => { throw new Error('Unexpected network') }))
    const before = JSON.stringify(data)
    const bytes = await createReportPdf(kind, data)
    expect(new TextDecoder().decode(bytes.slice(0, 8))).toBe('%PDF-1.7')
    const { pdf, files } = await attachments(bytes)
    expect(files['report.txt']).toBe((data as { export_text: string }).export_text)
    expect(JSON.parse(files['validated-report.json'])).toEqual(data)
    expect(JSON.stringify(data)).toBe(before)
    expect(pdf.getPageCount()).toBeGreaterThanOrEqual(2)
    expect(pdf.getPageCount()).toBeLessThanOrEqual(5)
    expect(pdf.getTitle()).toContain('DRAFT')
    expect(pdf.getSubject()).toContain('NOT CLINICAL ADVICE')
    expect(fetch).not.toHaveBeenCalled()
    if (kind !== 'descriptive') { mkdirSync(output, { recursive: true }); writeFileSync(resolve(output, `${kind}.pdf`), bytes) }
  }, 30_000)

test('ordinary unverified report stays unverified in the exported snapshot', async () => {
  const bytes = await createReportPdf('micro', ordinary)
  const { files } = await attachments(bytes)
  const saved = JSON.parse(files['validated-report.json'])
  expect(saved.evidence_domain).toBe('UNVERIFIED')
  expect(saved.clinical_analysis_enabled).toBe(false)
  expect(saved.entries.every((e: { result_type: string }) => ['UNKNOWN', 'WITHHELD'].includes(e.result_type))).toBe(true)
  writeFileSync(resolve(output, 'ordinary.pdf'), bytes)
}, 30_000)

test('long visible results paginate without a cap; technical-only content stays exact in attachments', async () => {
  const data = structuredClone(micro)
  const previous = data.entries[0].explanation
  data.entries[0].explanation += '\n' + ('Long fictional explanation with exact source identifiers. ' + '0123456789'.repeat(20) + '\n').repeat(100) + 'END_VISIBLE_RESULT_SENTINEL'
  data.export_text = data.export_text.replace(previous, data.entries[0].explanation)
  data.export_text += '\nLONG REPORT TEST\n' + ('LONG_SOURCE_' + '0123456789'.repeat(70) + '\n').repeat(100) + 'END_LONG_REPORT_SENTINEL'
  const bytes = await createReportPdf('micro', data)
  const { pdf, files } = await attachments(bytes)
  expect(pdf.getPageCount()).toBeGreaterThan(5)
  expect(files['report.txt']).toBe(data.export_text)
  const font = await pdf.embedFont('Helvetica')
  const original = 'exact  0.0000 / 1.2300 D ' + 'long_identifier'.repeat(80)
  const lines = wrapPdfText(original, font, 9, 200)
  expect(lines.join('')).toBe(original)
  expect(lines.every(s => font.widthOfTextAtSize(s, 9) <= 200)).toBe(true)
  writeFileSync(resolve(output, 'long.pdf'), bytes)
}, 30_000)

test('invalid report or wrong module is rejected before export', async () => {
  await expect(createReportPdf('macro', { ...macro, report: { ...macro.report, clinical_analysis_enabled: true } })).rejects.toThrow('PDF_INVALID_REPORT')
  await expect(createReportPdf('micro', nano)).rejects.toThrow('PDF_INVALID_REPORT')
})

test('unavailable glyphs refuse visibly instead of emitting lost original text', async () => {
  const data = structuredClone(micro), previous = data.entries[0].explanation
  data.entries[0].explanation += '\n\u{1F9B7}'
  data.export_text = data.export_text.replace(previous, data.entries[0].explanation)
  await expect(createReportPdf('micro', data)).rejects.toThrow('PDF_UNSUPPORTED_GLYPH:U+1F9B7')
})

test('non-displayed technical Unicode remains lossless in attachments without needing a display glyph', async () => {
  const data = structuredClone(micro); data.export_text += '\nTECHNICAL_ONLY_\u{1F9B7}'
  const { files } = await attachments(await createReportPdf('micro', data))
  expect(files['report.txt']).toBe(data.export_text)
  expect(JSON.parse(files['validated-report.json'])).toEqual(data)
}, 30_000)
