import { test, expect } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { isInteractiveReport } from '../src/api/interactive'

const modules = [
  { module: 'macro', run: 'Run Planning Assistant' },
  { module: 'micro', run: 'Run Attachment Review' },
  { module: 'nano', run: 'Run Sequencing Review' },
] as const

for (const item of modules) test(`${item.module}: functional policy scenario, exact exports and context invalidation`, async ({ page, context }, testInfo) => {
  test.setTimeout(90000)
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  await page.goto('/')
  await page.getByRole('button', { name: new RegExp(item.module.toUpperCase()) }).click()
  await expect(page.getByText('Optional fictional planning scenarios', { exact: true })).toHaveCount(0)
  await page.getByRole('button', { name: 'Load synthetic example', exact: true }).click()
  await expect(page.getByLabel('Loaded synthetic example')).toBeVisible()
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
    await expect(article).toContainText('change mesiodistal from 3.10 mm (D-labelled) to 2.50 mm (D-labelled)')
    expect(report.functional_plan.decisions.filter((d: { status: string }) => d.status === 'ILLUSTRATIVE_PROPOSAL')).toHaveLength(4)
  } else if (item.module === 'micro') {
    const table = article.getByRole('table')
    await expect(table.getByRole('row')).toHaveCount(16)
    await expect(table).toContainText('Vertical rectangular')
    await article.getByText('Tooth 11 details', { exact: true }).click()
    await expect(article).toContainText('Fictional supplied dimensions: 2.000 × 3.000 × 1.000 mm')
    await expect(table.getByRole('cell').filter({ hasText: /^No supported candidate/ })).toHaveCount(1)
  } else {
    await expect(article).toContainText('Remaining supplied movements · S3 · supplied order 3')
    for (const id of ['S1', 'S2', 'S3']) await article.getByText(`Stage ${id} movements and assumptions`, { exact: true }).click()
    await expect(article).toContainText('Tooth 11: 1.00 mm')
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
  const folder = resolve(process.cwd(), '../evidence/unified-synthetic-example/pdfs')
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
  await expect(page.getByLabel('Loaded synthetic example')).toHaveCount(0)
  await expect(page.getByRole('article')).toHaveCount(0)
})

test('one load and one parse serve all three modules; source edits remove the extra context', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Load synthetic example', exact: true }).click()
  const input = page.getByRole('textbox', { name: 'Raw TMT text' })
  const original = await input.inputValue()
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  let hash = ''
  for (const item of modules) {
    await page.getByRole('button', { name: new RegExp(item.module.toUpperCase()) }).click()
    await expect(page.getByLabel('Loaded synthetic example')).toBeVisible()
    const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
    await page.getByRole('button', { name: item.run, exact: true }).click()
    const response = await pending, report = await response.json()
    expect(response.status()).toBe(200)
    expect(isInteractiveReport(report)).toBe(true)
    expect(report.planning_context.module).toBe(item.module)
    hash ||= report.parsed.raw_sha256
    expect(report.parsed.raw_sha256).toBe(hash)
    await expect(page.getByRole('article')).toBeVisible()
    await expect(input).toHaveValue(original)
  }
  await page.getByRole('button', { name: /MACRO/ }).click()
  await expect(page.getByRole('article')).toBeVisible()
  await input.fill(original + '\n')
  await expect(page.getByLabel('Loaded synthetic example')).toHaveCount(0)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Planning Assistant', exact: true }).click()
  const response = await pending, ordinary = await response.json()
  expect(response.request().postDataJSON().planning_context).toBeUndefined()
  expect(ordinary.report_format).toBe('FUNCTIONAL_DEMO_V1')
  expect(ordinary.planning_context.origin).toBe('INPUT_DRIVEN_POLICY_REVIEW')
  expect(ordinary.planning_context.scenario_id).toBeNull()
  expect(ordinary.planning_context.targets).toEqual([])
  expect(ordinary.functional_plan.stages).toEqual([])
})
