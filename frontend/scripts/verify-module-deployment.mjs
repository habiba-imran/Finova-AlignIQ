// Explicit, bounded synthetic production check. Exports make no provider calls.
import assert from 'node:assert/strict'
import { existsSync, readFileSync, mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { gzipSync } from 'node:zlib'
import { chromium } from '@playwright/test'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'

if (!process.argv.includes('--run-live')) throw new Error('Use --run-live to authorize bounded synthetic review requests.')
const root = resolve(import.meta.dirname, '../..')
const output = resolve(root, 'evidence/module-final/deployed')
mkdirSync(output, { recursive: true })
const raw = JSON.parse(readFileSync(resolve(root, 'evidence/planning-wording/user-synthetic-live-report.json'), 'utf8')).parsed.raw_text
const origin = 'https://frontend-lr7x.vercel.app'
const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' })
const moduleArgument = process.argv.indexOf('--module')
const modules = moduleArgument < 0 ? ['macro', 'micro', 'nano'] : [process.argv[moduleArgument + 1]]
assert.ok(modules.every(module => ['macro', 'micro', 'nano'].includes(module)), 'Use --module macro, micro or nano')
const summaryPath = resolve(output, 'summary.json')
const summaries = moduleArgument >= 0 && existsSync(summaryPath) ? JSON.parse(readFileSync(summaryPath, 'utf8')).reports : []
try {
  const capability = await page.request.get(origin + '/api/v1/interactive/capabilities', { timeout: 60_000 })
  assert.equal(capability.status(), 200, 'Updated backend has not deployed')
  assert.equal((await capability.json()).revision, 'tmt-reviews-2026-11-15-v2')
  for (const module of modules) {
    await page.setViewportSize({ width: 1440, height: 1000 })
    await page.goto(origin)
    await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(module.toUpperCase()) }).click()
    await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
    const parseResponse = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
    await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
    const parsed = await (await parseResponse).json()
    assert.equal(parsed.measurements.length, 112)
    assert.equal(await page.getByLabel('Supplied review details').count(), 0)
    const reviewResponse = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'), { timeout: 60_000 })
    const action = { macro: 'Run Planning Assistant', micro: 'Run Attachment Review', nano: 'Run Sequencing Review' }[module]
    await page.getByRole('button', { name: action, exact: true }).click()
    const response = await reviewResponse
    assert.equal(response.status(), 200)
    const report = await response.json()
    assert.equal(report.report_format, 'MODULE_SPECIFIC_V1')
    assert.deepEqual(report.parsed.measurements, parsed.measurements)
    assert.equal(report.engine_review.evaluations.length, 96)
    assert.equal(report.engine_review.evaluations.filter(e => e.execution === 'DISABLED').length, 27)
    assert.equal(report.clinical_analysis_enabled, false)
    assert.deepEqual(report.illustrations, [])
    assert.equal(report.sections.length, module === 'macro' ? 0 : 4)
    const article = page.getByRole('article', { name: 'Generated synthetic report' })
    await article.waitFor()
    for (const comment of module === 'macro' ? report.observations : report.sections) assert.ok((await article.innerText()).includes(comment.text))
    assert.doesNotMatch(await article.innerText(), /Groq|provider|Illustrative attachment|Illustrative sequencing/i)
    const apiRequests = []
    const recordRequest = r => { if (r.url().includes('/api/')) apiRequests.push(r.url()) }
    page.on('request', recordRequest)
    const downloadPromise = page.waitForEvent('download', { timeout: 30_000 })
    await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
    const download = await downloadPromise
    await download.saveAs(resolve(output, module + '.pdf'))
    const pdf = await PDFDocument.load(readFileSync(resolve(output, module + '.pdf')))
    const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
    const attachments = {}
    for (let i = 0; i < names.size(); i += 2) {
      const name = names.lookup(i, PDFHexString).decodeText(), spec = names.lookup(i + 1, PDFDict)
      attachments[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) ).decode())
    }
    assert.equal(attachments['report.txt'], report.export_text)
    assert.deepEqual(JSON.parse(attachments['validated-report.json']), report)
    assert.equal(apiRequests.length, 0)
    page.off('request', recordRequest)
    for (const width of [1440, 375]) {
      await page.setViewportSize({ width, height: 1000 })
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth))
      await article.screenshot({ path: resolve(output, `${module}-${width}.png`) })
    }
    writeFileSync(resolve(output, module + '.json.gz'), gzipSync(JSON.stringify(report)))
    const summary = { module, generation: report.generation, sections: report.sections.map(s => ({ id: s.section_id, status: s.status })), pdf_pages: pdf.getPageCount(), source_positions: parsed.measurements.length, rules: 96, exact_attachments: true, export_api_calls: 0, widths: [1440, 375] }
    const previous = summaries.findIndex(row => row.module === module)
    if (previous < 0) summaries.push(summary)
    else summaries[previous] = summary
    writeFileSync(resolve(output, 'summary.json'), JSON.stringify({ checked_at: new Date().toISOString(), origin, reports: summaries }, null, 2))
    console.log(JSON.stringify(summary))
  }
} finally {
  await browser.close()
}
