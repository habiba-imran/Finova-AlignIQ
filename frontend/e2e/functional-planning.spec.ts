import { test, expect } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { isInteractiveReport } from '../src/api/interactive'

const modules = [
  { module: 'macro', load: 'Load Macro planning scenario', run: 'Run Planning Assistant' },
  { module: 'micro', load: 'Load Micro attachment scenario', run: 'Run Attachment Review' },
  { module: 'nano', load: 'Load Nano sequencing scenario', run: 'Run Sequencing Review' },
] as const

for (const item of modules) test(`${item.module}: functional policy scenario, exact exports and context invalidation`, async ({ page, context }, testInfo) => {
  test.setTimeout(90000)
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  await page.goto('/')
  await page.getByText('Optional fictional planning scenarios', { exact: true }).click()
  await page.getByRole('button', { name: item.load, exact: true }).click()
  await expect(page.getByLabel('Selected fictional scenario')).toBeVisible()
  const original = await page.getByRole('textbox', { name: 'Raw TMT text' }).inputValue()
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: item.run, exact: true }).click()
  const response = await pending, report = await response.json()
  expect(response.status()).toBe(200)
  expect(isInteractiveReport(report)).toBe(true)
  expect(report.report_format).toBe('FUNCTIONAL_DEMO_V1')
  expect(report.functional_plan.clinical_authorized).toBe(false)
  expect(report.engine_review.evaluations).toHaveLength(96)
  expect(report.engine_review.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
  const article = page.getByRole('article')
  await expect(article).toBeVisible()
  await expect(article).toContainText('Explicit fictional scenario')
  if (item.module === 'macro') {
    await expect(article).toContainText('change mesiodistal from 2.00 mm (D-labelled) to 1.00 mm (D-labelled)')
    expect(report.functional_plan.decisions.filter((d: { status: string }) => d.status === 'ILLUSTRATIVE_PROPOSAL')).toHaveLength(4)
  } else if (item.module === 'micro') {
    const table = article.getByRole('table')
    await expect(table.getByRole('row')).toHaveCount(9)
    await expect(table).toContainText('Vertical rectangular')
    await expect(table).toContainText('No attachment in this fictional scenario')
    await article.getByText('Tooth 11 details', { exact: true }).click()
    await expect(article).toContainText('Fictional supplied dimensions: 2.000 × 3.000 × 1.000 mm')
    await expect(table.getByRole('cell').filter({ hasText: /^No supported candidate/ })).toHaveCount(2)
  } else {
    await expect(article).toContainText('Angular finishing · S3 · supplied order 3')
    for (const id of ['S1', 'S2', 'S3']) await article.getByText(`Stage ${id} movements and assumptions`, { exact: true }).click()
    await expect(article).toContainText('Tooth 11: 0.40 mm')
    await expect(article).toContainText('source label L')
    await article.getByText('Stage-to-total consistency', { exact: true }).click()
    expect(report.functional_plan.allocation_checks.every((c: { status: string }) => c.status === 'MATCH')).toBe(true)
  }
  let apiCalls = 0
  page.on('request', r => { if (r.url().includes('/api/')) apiCalls++ })
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
  const folder = resolve(process.cwd(), '../evidence/functional-planning/pdfs')
  mkdirSync(folder, { recursive: true })
  await download.saveAs(resolve(folder, `${item.module}-${testInfo.project.name}.pdf`))
  writeFileSync(resolve(folder, `${item.module}-${testInfo.project.name}.json`), JSON.stringify(report, null, 2))
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
  expect(apiCalls).toBe(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath(`${item.module}-functional.png`), fullPage: true })
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(original + '\n')
  await expect(page.getByLabel('Selected fictional scenario')).toHaveCount(0)
  await expect(page.getByRole('article')).toHaveCount(0)
})
