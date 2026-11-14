import { test, expect } from '@playwright/test'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'

const modules = [
  { kind: 'macro', nav: /MACRO/, load: 'Load Finova planning demo', run: 'Run Planning Assistant', path: 'planning-demo/draft', article: 'Planning Assistant draft' },
  { kind: 'micro', nav: /MICRO/, load: 'Load Finova attachment demo', run: 'Run Attachment Review', path: 'attachment-demo/draft', article: 'Attachment review draft' },
  { kind: 'nano', nav: /NANO/, load: 'Load Finova sequencing demo', run: 'Run Sequencing Review', path: 'sequencer-demo/draft', article: 'Sequencing review draft' },
]

for (const module of modules) test(`${module.kind} PDF contains exact complete report and validated evidence, with no export requests`, async ({ page }, testInfo) => {
  await page.goto('/?diagnostics=1', { waitUntil: 'networkidle' })
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message))
  await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: module.nav }).click()
  await page.getByRole('button', { name: module.load }).click()
  if (module.kind === 'macro') await page.getByLabel('Wording preference').selectOption('TEMPLATES')
  const response = page.waitForResponse(r => r.url().endsWith(`/api/v1/development/${module.path}`))
  await page.getByRole('button', { name: module.run, exact: true }).click()
  const data = await (await response).json()
  const article = page.getByRole('article', { name: module.article })
  const requests: string[] = []; page.on('request', r => requests.push(r.url()))
  const pending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
  const download = await pending
  expect(download.suggestedFilename()).toMatch(new RegExp(`^finova-${module.kind}-draft-[a-f0-9]{12}\\.pdf$`))
  const file = testInfo.outputPath(`${module.kind}.pdf`); await download.saveAs(file)
  const stream = await download.createReadStream(), chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  const pdf = await PDFDocument.load(Buffer.concat(chunks))
  const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
  const files: Record<string, string> = {}
  for (let i = 0; i < names.size(); i += 2) {
    const name = names.lookup(i, PDFHexString).decodeText()
    const spec = names.lookup(i + 1, PDFDict)
    files[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
  }
  expect(files['report.txt']).toBe(data.export_text)
  expect(JSON.parse(files['validated-report.json'])).toEqual(data)
  const engine = module.kind === 'macro' ? data.report.engine_review : data.engine_review
  expect(engine.evaluations).toHaveLength(96)
  expect(engine.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
  expect(pdf.getPageCount()).toBeGreaterThanOrEqual(2)
  expect(pdf.getPageCount()).toBeLessThanOrEqual(5)
  await expect(article.getByText('Complete DRAFT PDF download requested.', { exact: true })).toBeVisible()
  await expect(article.getByRole('button', { name: 'Export PDF', exact: true })).toBeEnabled()
  expect(requests.filter(u => !u.startsWith('blob:'))).toEqual([])
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await article.getByRole('button', { name: 'Export PDF', exact: true }).scrollIntoViewIfNeeded()
  await page.screenshot({ path: testInfo.outputPath(`${module.kind}-pdf-export.png`) })
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill('Changed synthetic input')
  await expect(page.getByRole('button', { name: 'Export PDF', exact: true })).toHaveCount(0)
  expect(errors).toEqual([])
})

test('generic labels parse with exact zero and missing values while normal review remains unauthorized', async ({ page }) => {
  await page.goto('/?diagnostics=1', { waitUntil: 'networkidle' })
  const raw = '# SYNTHETIC lexical labels only\nTooth\tExtrusion / Intrusion (mm)\tRelative Ext / Int (mm)\tTranslation B / L (mm)\tTranslation M / D (mm)\nA\t1.2300E\t0.000\t-\t−2.00D\n'
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
  const response = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const parsed = await (await response).json()
  expect(parsed.measurements.map((m: { recognized_label: string }) => m.recognized_label)).toEqual(['vertical', 'relative_vertical', 'buccolingual', 'mesiodistal'])
  expect(parsed.measurements.map((m: { raw_value: string }) => m.raw_value)).toEqual(['1.2300E', '0.000', '-', '−2.00D'])
  expect(parsed.measurements.every((m: { semantics_verified: boolean; canonical_axis: unknown }) => m.semantics_verified === false && m.canonical_axis === null)).toBe(true)
  await page.getByLabel('Wording preference').selectOption('TEMPLATES')
  const review = page.waitForResponse(r => r.url().endsWith('/api/v1/planning/draft'))
  await page.getByRole('button', { name: 'Run Planning Assistant' }).click()
  const draft = await (await review).json()
  expect(draft.report.engine_review.evidence_domain).toBe('UNVERIFIED')
  expect(draft.report.engine_review.coverage.eligible_positions).toBe(0)
  expect(draft.report.generation.attempts).toBe(0)
  expect(await page.getByRole('textbox', { name: 'Raw TMT text' }).inputValue()).toBe(raw)
})
