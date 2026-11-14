import { expect, test } from '@playwright/test'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import macro from '../../evidence/deployed-wording-diagnosis/local-fixed-macro.json' with { type: 'json' }
import micro from '../../evidence/deployed-wording-diagnosis/local-fixed-micro.json' with { type: 'json' }
import nano from '../../evidence/deployed-wording-diagnosis/local-fixed-nano.json' with { type: 'json' }

for (const [report, action] of [[macro, 'Run Planning Assistant'], [micro, 'Run Attachment Review'], [nano, 'Run Sequencing Review']] as const) {
  test(`${report.module}: actual corrected wording reaches UI and PDF`, async ({ page }, testInfo) => {
    test.setTimeout(60_000)
    expect(report.generation.used_mode).toBe('GROQ_AI')
    expect(report.generation.accepted_comments).toBe(16)
    if (report.module === 'micro') expect(report.generation.attempts).toBe(2)
    let calls = 0
    await page.route('**/api/v1/interactive/review', route => { calls++; return route.fulfill({ json: report }) })
    await page.goto('/')
    await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(report.module.toUpperCase()) }).click()
    await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(report.parsed.raw_text)
    await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
    await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
    await page.getByRole('button', { name: action, exact: true }).click()
    const article = page.getByRole('article', { name: 'Generated synthetic report' })
    await expect(article.getByText('AI-assisted wording', { exact: true })).toBeVisible()
    for (const observation of report.observations) await expect(article.getByText(observation.text, { exact: true })).toBeVisible()
    expect(await article.innerText()).not.toMatch(/Groq|provider|transmission/i)
    const downloadPending = page.waitForEvent('download')
    await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
    const download = await downloadPending
    await download.saveAs(testInfo.outputPath(`${report.module}-corrected.pdf`))
    const stream = await download.createReadStream(), chunks: Buffer[] = []
    for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
    const pdf = await PDFDocument.load(Buffer.concat(chunks))
    const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
    const files: Record<string, string> = {}
    for (let i = 0; i < names.size(); i += 2) {
      const name = names.lookup(i, PDFHexString).decodeText(), spec = names.lookup(i + 1, PDFDict)
      files[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
    }
    expect(JSON.parse(files['validated-report.json'])).toEqual(report)
    expect(files['report.txt']).toBe(report.export_text)
    expect(calls).toBe(1)
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  })
}
