import { test, expect } from '@playwright/test'
import type { Page } from '@playwright/test'
import { mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { PDFArray, PDFDict, PDFDocument, PDFHexString, PDFName, PDFRawStream, decodePDFRawStream } from 'pdf-lib'
import { isInteractiveReport } from '../src/api/interactive'
import type { InteractiveReport } from '../src/api/interactive'

const modules = [
  { id: 'macro', run: 'Run Planning Assistant' },
  { id: 'micro', run: 'Run Attachment Review' },
  { id: 'nano', run: 'Run Sequencing Review' },
] as const
const coverage = { A: [15, 105, 2], B: [16, 112, 3], C: [8, 56, 0], D: [3, 6, 3] }
const normalize = (text: string) => text.replace(/\s+/g, ' ').trim()
const inputs = JSON.parse(readFileSync(resolve(process.cwd(), '../evidence/generalized-planning/inputs.json'), 'utf8')) as Record<'A' | 'B' | 'C' | 'D', string>
const saveSnapshot = (folder: string, stem: string, report: unknown) => {
  const target = resolve(folder, stem + '.json'), temporary = target + `.${process.pid}.tmp`
  writeFileSync(temporary, JSON.stringify(report, null, 2))
  renameSync(temporary, target)
}

async function exportContextReport(page: Page, report: InteractiveReport, stem: string) {
  expect(isInteractiveReport(report)).toBe(true)
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'])
  const article = page.getByRole('article')
  await expect(article).toBeVisible()
  await article.getByRole('button', { name: 'Copy', exact: true }).click()
  expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll('\r\n', '\n')).toBe(report.export_text)
  let pending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export TXT', exact: true }).click()
  const txt = await pending, txtStream = await txt.createReadStream(), txtChunks: Buffer[] = []
  for await (const chunk of txtStream!) txtChunks.push(Buffer.from(chunk))
  expect(Buffer.concat(txtChunks).toString('utf8')).toBe(report.export_text)
  pending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
  const download = await pending
  const folder = resolve(process.cwd(), '../evidence/generalized-planning/pdfs')
  mkdirSync(folder, { recursive: true })
  await download.saveAs(resolve(folder, stem + '.pdf'))
  saveSnapshot(folder, stem, report)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
}

for (const caseId of ['A', 'B', 'C', 'D'] as const) for (const module of modules) {
  test(`${caseId}/${module.id}: ordinary pasted input, source-specific review and exact exports`, async ({ page, context }, testInfo) => {
    test.setTimeout(90000)
    await context.grantPermissions(['clipboard-read', 'clipboard-write'])
    await page.goto('/')
    const input = page.getByRole('textbox', { name: 'Raw TMT text' })
    await input.fill(inputs[caseId])
    await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
    await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
    await page.getByRole('button', { name: new RegExp(module.id.toUpperCase()) }).click()
    const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
    await page.getByRole('button', { name: module.run, exact: true }).click()
    const response = await pending, report = await response.json()
    expect(response.status()).toBe(200)
    expect(isInteractiveReport(report)).toBe(true)
    expect(report.planning_context.scenario_id).toBeNull()
    expect(report.planning_context.origin).toBe('INPUT_DRIVEN_POLICY_REVIEW')
    expect(response.request().postDataJSON().planning_context).toBeUndefined()
    expect(report.parsed.raw_text).toBe(inputs[caseId])
    expect([report.parsed.teeth.length, report.parsed.measurements.length, report.parsed.coverage.missing]).toEqual(coverage[caseId])
    expect(report.engine_review.evaluations).toHaveLength(96)
    expect(report.engine_review.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
    expect(report.functional_plan.clinical_authorized).toBe(false)
    expect(report.functional_plan.stages).toHaveLength(0)
    expect(report.generation.used_mode).toBe('STANDARD_TEMPLATES')
    expect(report.generation.attempts).toBe(0)
    const article = page.getByRole('article')
    await expect(article).toBeVisible()
    await expect(page.getByLabel('Loaded synthetic example')).toHaveCount(0)
    await expect(article).not.toContainText('Explicit fictional scenario')
    if (module.id === 'macro') await expect(article).toContainText('Technician review:')
    if (module.id === 'micro') {
      await expect(article.getByRole('table').getByRole('row')).toHaveCount(coverage[caseId][0] + 1)
      if (caseId === 'B') {
        expect(new Set(report.functional_plan.attachment_rows.map((r: { primary: string }) => r.primary)).size).toBe(7)
        await expect(article.getByRole('table')).toContainText('Insufficient information')
        await expect(article.getByRole('table')).toContainText('No supported candidate')
      }
      if (caseId === 'D') expect(report.functional_plan.attachment_rows.every((r: { primary: null }) => r.primary === null)).toBe(true)
    }
    if (module.id === 'nano') {
      await expect(article).toContainText('Inspection topics, not treatment stages')
      expect(report.functional_plan.review_outline.length).toBeGreaterThan(0)
    }
    await article.locator('details').evaluateAll(details => details.forEach(detail => { detail.open = true }))
    const visible = normalize(await article.innerText())
    for (const finding of report.analytical_findings) expect(visible).toContain(normalize(finding.text))
    let requests = 0
    page.on('request', request => { if (request.url().includes('/api/')) requests++ })
    await article.getByRole('button', { name: 'Copy', exact: true }).click()
    expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll('\r\n', '\n')).toBe(report.export_text)
    const txtPending = page.waitForEvent('download')
    await article.getByRole('button', { name: 'Export TXT', exact: true }).click()
    const txt = await txtPending, stream = await txt.createReadStream(), chunks: Buffer[] = []
    for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
    expect(Buffer.concat(chunks).toString('utf8')).toBe(report.export_text)
    const pdfPending = page.waitForEvent('download')
    await article.getByRole('button', { name: 'Export PDF', exact: true }).click()
    const download = await pdfPending
    const folder = resolve(process.cwd(), '../evidence/generalized-planning/pdfs')
    mkdirSync(folder, { recursive: true })
    const stem = `${caseId}-${module.id}-${testInfo.project.name}`
    await download.saveAs(resolve(folder, `${stem}.pdf`))
    saveSnapshot(folder, stem, report)
    const pdfStream = await download.createReadStream(), pdfChunks: Buffer[] = []
    for await (const chunk of pdfStream!) pdfChunks.push(Buffer.from(chunk))
    const pdf = await PDFDocument.load(Buffer.concat(pdfChunks))
    const names = pdf.catalog.lookup(PDFName.of('Names'), PDFDict).lookup(PDFName.of('EmbeddedFiles'), PDFDict).lookup(PDFName.of('Names'), PDFArray)
    const attachments: Record<string, string> = {}
    for (let i = 0; i < names.size(); i += 2) {
      const name = names.lookup(i, PDFHexString).decodeText(), spec = names.lookup(i + 1, PDFDict)
      attachments[name] = new TextDecoder().decode(decodePDFRawStream(pdf.context.lookup(spec.lookup(PDFName.of('EF'), PDFDict).get(PDFName.of('F'))) as PDFRawStream).decode())
    }
    expect(attachments['report.txt']).toBe(report.export_text)
    expect(JSON.parse(attachments['validated-report.json'])).toEqual(report)
    expect(requests).toBe(0)
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    await page.screenshot({ path: testInfo.outputPath(`${stem}.png`), fullPage: true })
  })
}

test('Macro context creates an explicit arithmetic example and removing context suppresses it', async ({ page }, testInfo) => {
  test.setTimeout(90000)
  await page.goto('/')
  const input = page.getByRole('textbox', { name: 'Raw TMT text' })
  await input.fill(inputs.C)
  const parsedPending = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const parsed = await (await parsedPending).json()
  const tooth = parsed.teeth.find((t: { token: string }) => t.token === '33')
  const movement = parsed.measurements.find((m: { tooth_ref: string; recognized_label: string }) => m.tooth_ref === tooth.id && m.recognized_label === 'rotation')
  await page.locator('summary').filter({ hasText: 'Planning context' }).click()
  await page.getByRole('combobox', { name: 'Planning objective', exact: true }).selectOption('ANGULAR_CONTROL')
  await page.getByLabel('Use the source labels as recorded').check()
  await page.getByRole('combobox', { name: 'Source measurement', exact: true }).selectOption(movement.id)
  await page.getByRole('combobox', { name: 'Modification example', exact: true }).selectOption('HALF_MAGNITUDE')
  let pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Planning Assistant', exact: true }).click()
  let report = await (await pending).json()
  expect(report.functional_plan.decisions.flatMap((d: { proposed_changes: unknown[] }) => d.proposed_changes)).toEqual([{ measurement_ref: movement.id, amount: '-2.0625', unit: 'deg', source_direction: 'M' }])
  await expect(page.getByRole('article')).toContainText('divide this source scalar by 2')
  await exportContextReport(page, report, `context-macro-${testInfo.project.name}`)
  await page.getByRole('combobox', { name: 'Planning objective', exact: true }).selectOption('')
  await expect(page.getByRole('article')).toHaveCount(0)
  pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Planning Assistant', exact: true }).click()
  report = await (await pending).json()
  expect(report.functional_plan.decisions.every((d: { proposed_changes: unknown[] }) => !d.proposed_changes.length)).toBe(true)
  await input.fill(inputs.B)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await page.locator('summary').filter({ hasText: 'Planning context' }).click()
  await expect(page.getByRole('combobox', { name: 'Planning objective', exact: true })).toHaveValue('')
  await expect(page.getByRole('combobox', { name: 'Modification example', exact: true })).toHaveValue('NONE')
})

test('Micro uses supplied geometry and removes it when its specification is removed', async ({ page }, testInfo) => {
  test.setTimeout(90000)
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(inputs.B)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  await page.getByRole('button', { name: /MICRO/ }).click()
  await page.locator('summary').filter({ hasText: 'Planning context' }).click()
  await page.getByText('Supplied catalog specifications', { exact: true }).click()
  await page.getByRole('combobox', { name: 'Catalog category', exact: true }).selectOption('OVAL')
  await page.getByLabel('Width (mm)', { exact: true }).fill('1.234')
  await page.getByLabel('Height (mm)', { exact: true }).fill('2.345')
  await page.getByLabel('Depth (mm)', { exact: true }).fill('0.456')
  await page.getByRole('button', { name: 'Apply catalog specification', exact: true }).click()
  let pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Attachment Review', exact: true }).click()
  let report = await (await pending).json()
  expect(report.sections[0].text).toContain('1.234 × 2.345 × 0.456 mm')
  await exportContextReport(page, report, `context-micro-${testInfo.project.name}`)
  await page.getByRole('button', { name: 'Remove Ellipsoid / oval specification', exact: true }).click()
  await expect(page.getByRole('article')).toHaveCount(0)
  pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Attachment Review', exact: true }).click()
  report = await (await pending).json()
  expect(report.planning_context.attachment_options.every((o: { geometry: null }) => o.geometry === null)).toBe(true)
})

test('Nano accepts supplied stages and support roles; removing a stage withholds dependent strategies', async ({ page }, testInfo) => {
  test.setTimeout(90000)
  const raw = 'Tooth\tRotation (deg)\tAngulation (deg)\tInclination (deg)\tVertical (mm)\tRelative Ext / Int (mm)\tTranslation B / L (mm)\tTranslation M / D (mm)\n11\t0.00\t0.00\t0.00\t0.00\t0.00\t0.60 L\t0.00\n21\t1.20 D\t0.00\t0.00\t0.00\t0.00\t0.00\t0.00'
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
  const parsedPending = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const parsed = await (await parsedPending).json()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  const teeth = Object.fromEntries(parsed.teeth.map((t: { token: string; id: string }) => [t.token, t.id]))
  const cell = (tooth: string, family: string) => parsed.measurements.find((m: { tooth_ref: string; recognized_label: string }) => m.tooth_ref === teeth[tooth] && m.recognized_label === family).id
  await page.getByRole('button', { name: /NANO/ }).click()
  await page.locator('summary').filter({ hasText: 'Planning context' }).click()
  await page.getByRole('combobox', { name: 'Stage amount convention', exact: true }).selectOption('INCREMENTS_MATCH_SOURCE_LABELS')
  await page.getByRole('button', { name: 'Add supplied stage', exact: true }).click()
  await page.getByRole('button', { name: 'Add supplied stage', exact: true }).click()
  await page.getByLabel('Stage 1 phase', { exact: true }).fill('P1')
  await page.getByLabel('Stage 2 phase', { exact: true }).fill('P2')
  const allocations = [['S1', '11', 'buccolingual', '0.60'], ['S2', '21', 'rotation', '1.20'], ['S1', '21', 'buccolingual', '0.00'], ['S2', '11', 'rotation', '0.00']]
  for (let i = 0; i < allocations.length; i++) {
    const [stage, tooth, family, amount] = allocations[i]
    await page.getByRole('button', { name: 'Add supplied movement', exact: true }).click()
    await expect(page.getByLabel(new RegExp(`Movement ${i + 1} supplied amount`))).toHaveValue('')
    await page.getByRole('combobox', { name: `Movement ${i + 1} stage`, exact: true }).selectOption(stage)
    await page.getByRole('combobox', { name: `Movement ${i + 1} source`, exact: true }).selectOption(cell(tooth, family))
    await page.getByLabel(new RegExp(`Movement ${i + 1} supplied amount`)).fill(amount)
  }
  await page.getByText('Supplied support constraints', { exact: true }).click()
  await page.getByLabel('Explicitly assume the support group').check()
  for (const [phase, support, active] of [['P1', '21', '11'], ['P2', '11', '21']]) {
    await page.getByRole('combobox', { name: 'Support phase', exact: true }).selectOption(phase)
    await page.getByRole('listbox', { name: 'Support tooth tokens', exact: true }).selectOption([teeth[support]])
    await page.getByRole('listbox', { name: 'Active tooth tokens', exact: true }).selectOption([teeth[active]])
    await page.getByRole('button', { name: 'Apply support constraint', exact: true }).click()
  }
  let pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Sequencing Review', exact: true }).click()
  let report = await (await pending).json()
  expect(isInteractiveReport(report)).toBe(true)
  expect(report.functional_plan.stages).toHaveLength(2)
  expect(report.functional_plan.review_outline).toHaveLength(0)
  expect(report.functional_plan.allocation_checks.every((c: { status: string }) => c.status === 'MATCH')).toBe(true)
  expect(report.functional_plan.decisions.filter((d: { dimension: string; status: string }) => d.dimension === 'ANCHORAGE' && d.status === 'ILLUSTRATIVE_PROPOSAL')).toHaveLength(2)
  await exportContextReport(page, report, `context-nano-${testInfo.project.name}`)
  await page.getByRole('button', { name: 'Remove stage 2', exact: true }).click()
  await expect(page.getByRole('article')).toHaveCount(0)
  pending = page.waitForResponse(r => r.url().endsWith('/api/v1/interactive/review'))
  await page.getByRole('button', { name: 'Run Sequencing Review', exact: true }).click()
  report = await (await pending).json()
  expect(report.functional_plan.decisions.filter((d: { dimension: string; status: string }) => d.dimension === 'ANCHORAGE' && d.status === 'ILLUSTRATIVE_PROPOSAL')).toHaveLength(0)
})
