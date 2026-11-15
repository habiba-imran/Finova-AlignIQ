import { expect, test } from '@playwright/test'
import { readFileSync, mkdirSync } from 'node:fs'
import { resolve } from 'node:path'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { commentParagraphs } from '../src/reviewPresentation'

const raw = readFileSync(resolve(process.cwd(), '../backend/tests/fixtures/analysis_15_tooth.md'), 'utf8')
const modules = [
  { module: 'macro', action: 'Run Planning Assistant', first: 'Sagittal / Mesiodistal movement' },
  { module: 'micro', action: 'Run Attachment Review', first: 'Priority tooth profiles' },
  { module: 'nano', action: 'Run Sequencing Review', first: 'Arch and tooth-group distribution' },
] as const

for (const item of modules) test(`${item.module}: 15-tooth analytical UI, Copy, TXT, PDF and cache agree`, async ({ page, context }, testInfo) => {
  test.setTimeout(60000)
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  await page.goto('/')
  const nav = page.getByRole('navigation', { name: 'Review purpose' })
  await nav.getByRole('button', { name: new RegExp(item.module.toUpperCase()) }).click()
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: item.action, exact: true }).click()
  const report = await (await pending).json()
  expect(report.report_format).toBe('ANALYTICAL_V1')
  expect(report.parsed.teeth).toHaveLength(15)
  expect(report.parsed.measurements).toHaveLength(105)
  expect(report.parsed.measurements.filter((m: { numeric_status: string }) => ['PARSED', 'EXPLICIT_ZERO'].includes(m.numeric_status))).toHaveLength(103)
  const article = page.getByRole('article')
  await expect(article.getByRole('heading', { name: item.first, exact: true })).toBeVisible()
  await expect(article).toContainText('All available movement values were parsed successfully')
  for (const section of report.sections) {
    const card = article.locator('.comment-card').filter({ has: page.getByRole('heading', { name: section.title, exact: true }) })
    for (const paragraph of commentParagraphs(section.text)) await expect(card.getByText(paragraph, { exact: true }).first()).toBeVisible()
  }
  const requests: string[] = []
  page.on('request', request => { if (request.url().includes('/api/')) requests.push(request.url()) })
  await article.getByRole('button', { name: 'Copy', exact: true }).click()
  expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll('\r\n', '\n')).toBe(report.export_text)
  const txtPending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export TXT', exact: true }).click()
  const txt = await txtPending, txtStream = await txt.createReadStream(), txtChunks: Buffer[] = []
  for await (const chunk of txtStream!) txtChunks.push(Buffer.from(chunk))
  expect(Buffer.concat(txtChunks).toString('utf8')).toBe(report.export_text)
  const pdfPending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
  const download = await pdfPending
  const folder = resolve(process.cwd(), '../evidence/analysis-pipeline/pdfs')
  mkdirSync(folder, { recursive: true })
  await download.saveAs(resolve(folder, `${item.module}-${testInfo.project.name}.pdf`))
  const stream = await download.createReadStream(), chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  const pdf = await PDFDocument.load(Buffer.concat(chunks))
  const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
  const files: Record<string, string> = {}
  for (let i = 0; i < names.size(); i += 2) {
    const name = names.lookup(i, PDFHexString).decodeText(), spec = names.lookup(i + 1, PDFDict)
    files[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
  }
  expect(files['report.txt']).toBe(report.export_text)
  expect(JSON.parse(files['validated-report.json'])).toEqual(report)
  await nav.getByRole('button', { name: item.module === 'nano' ? /MACRO/ : /NANO/ }).click()
  await nav.getByRole('button', { name: new RegExp(item.module.toUpperCase()) }).click()
  await expect(page.getByRole('article')).toBeVisible()
  expect(requests).toEqual([])
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath(`${item.module}-15.png`), fullPage: true })
})
