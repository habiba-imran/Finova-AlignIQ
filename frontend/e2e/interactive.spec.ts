import { test, expect } from '@playwright/test'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { resolve } from 'node:path'
import liveMacro from '../../evidence/unified-wording/approved-macro.json' with { type: 'json' }
import liveMicro from '../../evidence/unified-wording/approved-micro.json' with { type: 'json' }
import liveNano from '../../evidence/unified-wording/approved-nano.json' with { type: 'json' }
const liveReports = { macro: liveMacro, micro: liveMicro, nano: liveNano }
import samples from '../../examples/interactive-synthetic-tmts.json' with { type: 'json' }

const modules = [
  { id: 'macro', action: 'Run Planning Assistant' },
  { id: 'micro', action: 'Run Attachment Review' },
  { id: 'nano', action: 'Run Sequencing Review' },
] as const

for (const sample of samples) test(`${sample.id}: pasted synthetic input works in all three modules`, async ({ page, context }, testInfo) => {
  test.setTimeout(90_000)
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message))
  await page.goto('/')
  const raw = page.getByRole('textbox', { name: 'Raw TMT text' })
  await raw.fill(sample.raw_text)
  const parsing = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const parsed = await (await parsing).json()
  expect(parsed.measurements.length).toBe({ rows: 12, columns: 6, markdown: 4, large: 112 }[sample.id])
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  await expect(page.getByLabel('Full parsing JSON')).toHaveCount(0)
  await expect(page.getByLabel('Wording preference')).toHaveCount(0)
  for (const module of modules) {
    await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(module.id.toUpperCase()) }).click()
    const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
    await page.getByRole('button', { name: module.action, exact: true }).click()
    const response = await pending, report = await response.json()
    expect(response.status()).toBe(200)
    expect(response.headers()['cache-control']).toBe('no-store')
    expect(response.request().postDataJSON()).toMatchObject({ module: module.id, raw_text: sample.raw_text, synthetic_data_confirmed: true })
    expect(report.parsed.measurements).toEqual(parsed.measurements)
    expect(report.observations.flatMap((o: { measurements: unknown[] }) => o.measurements)).toHaveLength(parsed.measurements.length)
    expect(report.engine_review.evaluations).toHaveLength(96)
    expect(report.engine_review.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
    expect(report.clinical_analysis_enabled).toBe(false)
    expect(report.generation.used_mode).toBe('STANDARD_TEMPLATES')
    const article = page.getByRole('article', { name: 'Generated synthetic report' })
    await expect(article).toBeVisible()
    await expect(article.getByText('Standard wording', { exact: true })).toBeVisible()
    if (module.id === 'macro') {
      await expect(article.getByRole('heading', { name: 'Planning comments', exact: true })).toBeVisible()
      expect(report.observations[0].text).toContain('The programmed movement record lists')
    }
    expect(await article.innerText()).not.toMatch(/Groq|transmi|shared with|provider/i)
    const facts = article.getByRole('region', { name: 'Factual tooth-wise observations' })
    await expect(facts.getByRole('heading', { level: 6 })).toHaveCount(parsed.teeth.length)
    expect(await article.innerText()).not.toMatch(/GROQ_|SEMANTICS_|\b(?:R13|T01|A05|H08)\b|finding_id|rule ledger/)
    await expect(article.getByRole('region', { name: 'Illustrative demo content' })).toHaveCount(module.id === 'macro' ? 0 : 1)
    if (module.id !== 'macro') await expect(article.getByText(/Simulated examples · not calculated findings/)).toBeVisible()
    const requests: string[] = []; page.on('request', r => { if (r.url().includes('/api/')) requests.push(r.url()) })
    await article.getByRole('button', { name: 'Copy', exact: true }).click()
    expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll('\r\n', '\n')).toBe(report.export_text)
    const txtPending = page.waitForEvent('download')
    await article.getByRole('button', { name: 'Export TXT', exact: true }).click()
    const txt = await txtPending, txtStream = await txt.createReadStream(), txtChunks: Buffer[] = []
    for await (const chunk of txtStream!) txtChunks.push(Buffer.from(chunk))
    expect(Buffer.concat(txtChunks).toString('utf8')).toBe(report.export_text)
    if (sample.id === 'large') {
      await txt.saveAs(testInfo.outputPath(`${module.id}-112.txt`))
      const pdfPending = page.waitForEvent('download')
      await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
      const download = await pdfPending
      await download.saveAs(testInfo.outputPath(`${module.id}-112.pdf`))
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
      expect(pdf.getPageCount()).toBeGreaterThan(2)
      await page.screenshot({ path: testInfo.outputPath(`${module.id}-112-results.png`), fullPage: true })
    }
    expect(requests).toEqual([])
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    await expect(raw).toHaveValue(sample.raw_text)
  }
  expect(errors).toEqual([])
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
  await raw.fill('edited synthetic input')
  await expect(page.getByRole('article')).toHaveCount(0)
  await expect(page.getByRole('button', { name: 'Export PDF', exact: true })).toHaveCount(0)
})

test('unsupported input keeps a clear error and cannot generate a fabricated report', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill('This is not a movement table.')
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('button', { name: 'Run Planning Assistant' })).toBeDisabled()
  await expect(page.getByRole('alert')).toContainText('supported table')
  await expect(page.getByRole('article')).toHaveCount(0)
})

for (const module of modules) test(`${module.id}: approved AI comments are prominent in the UI and PDF`, async ({ page }, testInfo) => {
  const livePlanning = liveReports[module.id]
  expect(livePlanning.generation.used_mode).toBe('GROQ_AI')
  expect(livePlanning.generation.accepted_comments).toBe(16)
  expect(new Set(livePlanning.observations.map(o => o.text.split(' ').slice(0, 3).join(' '))).size).toBeGreaterThanOrEqual(3)
  await page.route('**/api/v1/interactive/review', route => route.fulfill({ json: livePlanning }))
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(livePlanning.parsed.raw_text)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(module.id.toUpperCase()) }).click()
  await page.getByRole('button', { name: module.action, exact: true }).click()
  const article = page.getByRole('article', { name: 'Generated synthetic report' })
  await expect(article.getByRole('heading', { name: module.id === 'macro' ? 'Planning comments' : module.id === 'micro' ? 'Attachment review comments' : 'Sequencing review comments', exact: true })).toBeVisible()
  await expect(article.getByText('AI-assisted wording', { exact: true })).toBeVisible()
  const comment = livePlanning.observations.find(o => o.original_tooth.trim() === '11')!
  await expect(article.getByText(comment.text, { exact: true })).toBeVisible()
  expect(await article.innerText()).not.toMatch(/Groq|provider|transmission|shared with/i)
  const pending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
  const download = await pending
  await download.saveAs(testInfo.outputPath(`${module.id}-comments-approved.pdf`))
  if (testInfo.project.name === 'desktop') await download.saveAs(resolve(process.cwd(), `../evidence/unified-wording/finova-${module.id}-ai-comments.pdf`))
  const stream = await download.createReadStream(), chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  const pdf = await PDFDocument.load(Buffer.concat(chunks))
  const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
  const files: Record<string, string> = {}
  for (let i = 0; i < names.size(); i += 2) {
    const name = names.lookup(i, PDFHexString).decodeText(), spec = names.lookup(i + 1, PDFDict)
    files[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
  }
  expect(JSON.parse(files['validated-report.json'])).toEqual(livePlanning)
  expect(files['report.txt']).toContain(comment.text)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath(`${module.id}-comments-approved.png`), fullPage: true })
})
