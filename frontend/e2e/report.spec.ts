import { expect, test } from '@playwright/test'

test('final report uses templates for unverified data and copies/downloads a complete local DRAFT', async ({ page, context }, testInfo) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto('/', { waitUntil: 'networkidle' })
  const requests: string[] = []
  page.on('request', request => requests.push(request.url()))
  const raw = '# SYNTHETIC\n\nTooth\tRotation (deg)\tExtrusion (mm)\n 13 \t−1.2300 M\t0.00 E  \n14\t\t—\n'
  const input = page.getByRole('textbox', { name: 'Raw TMT text' })
  await input.fill(raw)
  await page.getByRole('checkbox').check()
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  await page.getByText('Advanced: separate engineering review & legacy report actions').click()
  await page.getByRole('button', { name: 'Create draft review', exact: true }).click()
  await expect(page.getByLabel('Draft review results')).toBeVisible()
  await expect(page.getByLabel('Comment generation mode')).toHaveValue('AUTO')
  expect(requests).toHaveLength(2)
  const pending = page.waitForResponse(response => response.url().endsWith('/api/v1/reports/draft'))
  await page.getByRole('button', { name: 'Create final report', exact: true }).click()
  const response = await pending
  expect(response.status()).toBe(200)
  expect(response.headers()['cache-control']).toBe('no-store')
  expect(response.request().postDataJSON().raw_text).toBe(raw)
  const report = await response.json()
  expect(report.generation.reason).toBe('NO_ELIGIBLE_FINDINGS')
  expect(report.generation.attempts).toBe(0)
  expect(report.clinical_analysis_enabled).toBe(false)
  const article = page.getByRole('article', { name: 'Final draft report results' })
  await expect(article).toBeVisible()
  await expect(article.getByText('DRAFT — Requires Orthodontist Review', { exact: true })).toBeVisible()
  await expect(article.getByText(/No eligible findings: Groq was not called/)).toBeVisible()
  await page.getByRole('button', { name: 'Copy Report', exact: true }).click()
  // Windows clipboard serialization can use CRLF; the application passes export_text unchanged.
  const clipboard = await page.evaluate(() => navigator.clipboard.readText())
  expect(clipboard.replaceAll('\r\n', '\n')).toBe(report.export_text)
  const downloadPending = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Download Report (TXT)', exact: true }).click()
  const download = await downloadPending
  expect(download.suggestedFilename()).toBe(`finova-aligniq-draft-${report.report_id.slice(0, 12)}.txt`)
  const stream = await download.createReadStream()
  const chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  expect(Buffer.concat(chunks).toString('utf8')).toBe(report.export_text)
  expect(report.export_text).toContain(report.engine_review.raw_sha256)
  expect(report.export_text).toContain('RULE EVALUATION LEDGER')
  expect(report.export_text).toContain('CLINICAL LIMITATIONS / SCOPE')
  await expect(input).toHaveValue(raw)
  expect(await page.getByLabel('Raw text preview').textContent()).toBe(raw)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
  expect(requests.filter(url => !url.startsWith('blob:'))).toEqual([
    'http://127.0.0.1:5173/api/v1/tmt/parse', 'http://127.0.0.1:5173/api/v1/tmt/observations', 'http://127.0.0.1:5173/api/v1/reports/draft',
  ])
  await article.screenshot({ path: testInfo.outputPath('phase3-report.png') })
  await input.fill(raw + '\n')
  await expect(article).toHaveCount(0)
  await expect(page.getByRole('button', { name: 'Copy Report', exact: true })).toHaveCount(0)
  expect(errors).toEqual([])
})
