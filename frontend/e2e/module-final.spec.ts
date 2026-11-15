import { expect, test } from '@playwright/test'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { mkdirSync } from 'node:fs'
import { resolve } from 'node:path'
import samples from '../../examples/interactive-synthetic-tmts.json' with { type: 'json' }
import { buildPdfPresentation } from '../src/pdf/presentation'
import { commentParagraphs, moduleReviewPresentation } from '../src/reviewPresentation'

const sample = samples.find(row => row.id === 'large')!
const cases = [
  { module: 'macro', supplied: false, action: 'Run Planning Assistant' },
  { module: 'micro', supplied: false, action: 'Run Attachment Review' },
  { module: 'nano', supplied: false, action: 'Run Sequencing Review' },
] as const

for (const item of cases) test(`${item.module} ${item.supplied ? 'supplied' : 'TMT only'}: distinct comments and exact PDF`, async ({ page }, testInfo) => {
  test.setTimeout(60_000)
  await page.goto('/')
  await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(item.module.toUpperCase()) }).click()
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(sample.raw_text)
  const pendingParse = page.waitForResponse(response => response.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const parsed = await (await pendingParse).json()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  await expect(page.getByLabel('Supplied review details')).toHaveCount(0)
  const pendingReport = page.waitForResponse(response => response.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: item.action, exact: true }).click()
  const response = await pendingReport, report = await response.json()
  expect(response.status()).toBe(200)
  expect(report.report_format).toBe('ANALYTICAL_V1')
  expect(report.parsed.measurements).toEqual(parsed.measurements)
  expect(report.engine_review.evaluations).toHaveLength(96)
  expect(report.illustrations).toEqual([])
  const article = page.getByRole('article', { name: 'Generated synthetic report' })
  await expect(article).toBeVisible()
  if (item.module !== 'macro') {
    expect(report.sections).toHaveLength(item.module === 'micro' ? 4 : 5)
    const comments = article.getByRole('region', { name: 'Module review comments' })
    for (const section of moduleReviewPresentation(report).sections) for (const paragraph of commentParagraphs(section.text)) await expect(comments.getByText(paragraph, { exact: true }).first()).toBeVisible()
    await expect(comments.getByRole('heading', { level: 6 })).toHaveCount(report.sections.length)
    await expect(article.getByLabel('Report scope')).toHaveCount(0)
    await expect(article).not.toContainText('Not prescribed')
    expect(report.sections.at(-1).status).toBe(item.module === 'micro' ? 'UNAVAILABLE' : 'SOURCE_REPORTED')
    expect(report.sections[0].status).toBe('SOURCE_REPORTED')
    await expect(comments).not.toContainText('because no')
    await expect(comments).not.toContainText('Information needed:')
    await expect(comments).toContainText(item.module === 'micro' ? '15.1250' : '1.2300')
  }
  expect(await article.innerText()).not.toMatch(/Groq|provider|fictional demonstration group/i)
  const presentation = buildPdfPresentation('interactive', report)
  for (const section of moduleReviewPresentation(report).sections) for (const paragraph of commentParagraphs(section.text)) expect(presentation.blocks.some(block => block.type === 'text' && block.text === paragraph)).toBe(true)
  let exportRequests = 0
  page.on('request', request => { if (request.url().includes('/api/')) exportRequests++ })
  const pendingDownload = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
  const download = await pendingDownload
  const filename = `${item.module}-${item.supplied ? 'supplied' : 'tmt-only'}.pdf`
  await download.saveAs(testInfo.outputPath(filename))
  if (testInfo.project.name === 'desktop') {
    const output = resolve(process.cwd(), '../evidence/analysis-pipeline/regression-pdfs')
    mkdirSync(output, { recursive: true }); await download.saveAs(resolve(output, filename))
  }
  const stream = await download.createReadStream(), chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  const pdf = await PDFDocument.load(Buffer.concat(chunks))
  const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
  const attachments: Record<string, string> = {}
  for (let index = 0; index < names.size(); index += 2) {
    const name = names.lookup(index, PDFHexString).decodeText(), spec = names.lookup(index + 1, PDFDict)
    attachments[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
  }
  expect(attachments['report.txt']).toBe(report.export_text)
  expect(JSON.parse(attachments['validated-report.json'])).toEqual(report)
  expect(exportRequests).toBe(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath(filename.replace('.pdf', '.png')), fullPage: true })
})
