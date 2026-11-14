import { expect, test } from '@playwright/test'
import { selectedExport } from '../src/api/planning'

test('fixed synthetic Planning Assistant completes the real pipeline and exports exact DRAFT comments', async ({ page, context }, testInfo) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  const errors: string[] = []
  page.on('pageerror', e => errors.push(e.message))
  await page.goto('/', { waitUntil: 'networkidle' })
  await page.screenshot({ path: testInfo.outputPath('planning-intake.png'), fullPage: true })
  const requests: string[] = []
  page.on('request', r => requests.push(r.url()))
  const loaded = page.waitForResponse(r => r.url().endsWith('/api/v1/development/planning-demo/input'))
  await page.getByRole('button', { name: 'Load Finova planning demo' }).click()
  const inputResponse = await loaded
  expect(inputResponse.status()).toBe(200)
  expect(inputResponse.headers()['cache-control']).toBe('no-store')
  const input = await inputResponse.json()
  await expect(page.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(input.parsed.raw_text)
  expect(await page.getByLabel('Raw text preview').textContent()).toBe(input.parsed.raw_text)
  await page.getByLabel('Wording preference').selectOption('TEMPLATES')
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/development/planning-demo/draft'))
  await page.getByRole('button', { name: 'Run Planning Assistant' }).click()
  const response = await pending
  expect(response.request().postDataJSON()).toEqual({ comment_mode: 'TEMPLATES' })
  const draft = await response.json(), report = draft.report
  expect(report.engine_review.evidence_domain).toBe('TEST_ONLY')
  expect(report.engine_review.coverage).toMatchObject({ declared_positions: 20, eligible_positions: 4, unavailable_positions: 16 })
  expect(report.engine_review.evaluations).toHaveLength(96)
  expect(report.engine_review.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
  expect(report.generation.attempts).toBe(0)
  const article = page.getByRole('article', { name: 'Planning Assistant draft' })
  await expect(article).toBeVisible()
  await expect(article.getByRole('heading', { name: 'Planning review draft' })).toBeFocused()
  for (const dimension of ['Sagittal', 'Transverse', 'Vertical']) await expect(article.getByRole('region', { name: `${dimension} review` })).toBeVisible()
  await expect(article.getByText('1.2300 D', { exact: true }).first()).toBeVisible()
  const sagittal = article.getByRole('region', { name: 'Sagittal review' })
  await sagittal.getByRole('checkbox').check()
  await article.getByRole('button', { name: 'Copy selected comments' }).click()
  const copied = await page.evaluate(() => navigator.clipboard.readText())
  expect(copied.replaceAll('\r\n', '\n')).toBe(selectedExport(report, new Set(draft.sections[0].comment_ids)))
  await article.getByRole('button', { name: 'Copy complete DRAFT report' }).click()
  expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll('\r\n', '\n')).toBe(draft.export_text)
  const downloadPending = page.waitForEvent('download')
  await article.getByRole('button', { name: 'Download DRAFT (TXT)' }).click()
  const download = await downloadPending
  expect(download.suggestedFilename()).toMatch(/^finova-planning-draft-[a-f0-9]{12}\.txt$/)
  const stream = await download.createReadStream(), chunks: Buffer[] = []
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk))
  expect(Buffer.concat(chunks).toString('utf8')).toBe(draft.export_text)
  expect(draft.export_text).toContain('FINOVA SYNTHETIC DEMONSTRATION — TEST_ONLY')
  expect(draft.export_text).toContain('RULE EVALUATION LEDGER')
  expect(draft.export_text).toContain(report.engine_review.raw_sha256)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
  expect(requests.filter(url => !url.startsWith('blob:'))).toEqual([
    'http://127.0.0.1:5173/api/v1/development/planning-demo/input',
    'http://127.0.0.1:5173/api/v1/development/planning-demo/draft',
  ])
  await article.screenshot({ path: testInfo.outputPath('planning-draft.png') })
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(input.parsed.raw_text + '\nChanged')
  await expect(article).toHaveCount(0)
  await expect(page.getByRole('button', { name: 'Copy selected comments' })).toHaveCount(0)
  await expect(page.getByRole('checkbox', { name: /I confirm/ })).not.toBeChecked()
  expect(errors).toEqual([])
})

test('ordinary unknown vendor input abstains, cannot select comments and performs no external transmission', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const requests: string[] = []
  page.on('request', r => requests.push(r.url()))
  const raw = '# SYNTHETIC UnknownVendor\nTooth\tRotation (deg)\n13\t−1.2300 M\n'
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/planning/draft'))
  await page.getByRole('button', { name: 'Run Planning Assistant' }).click()
  const draft = await (await pending).json()
  expect(draft.report.engine_review.evidence_domain).toBe('UNVERIFIED')
  expect(draft.report.generation.attempts).toBe(0)
  const article = page.getByRole('article', { name: 'Planning Assistant draft' })
  for (const dimension of ['Sagittal', 'Transverse', 'Vertical']) await expect(article.getByRole('region', { name: `${dimension} review` })).toContainText('No sufficiently authorized descriptions')
  await expect(article.getByRole('button', { name: 'Copy selected comments' })).toBeDisabled()
  await expect(article.getByRole('checkbox')).toHaveCount(0)
  expect(requests).toEqual(['http://127.0.0.1:5173/api/v1/tmt/parse', 'http://127.0.0.1:5173/api/v1/planning/draft'])
  expect(await page.getByLabel('Raw text preview').textContent()).toBe(raw)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})

test('review-purpose navigation works by keyboard; all modules have distinct intake', async ({ page }) => {
  await page.goto('/')
  const nav = page.getByRole('navigation', { name: 'Review purpose' })
  const micro = nav.getByRole('button', { name: /MICRO/ })
  await micro.focus(); await page.keyboard.press('Enter')
  await expect(micro).toHaveAttribute('aria-pressed', 'true')
  await expect(page.getByRole('button', { name: 'Load Finova attachment demo' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Parse Table', exact: true })).toBeDisabled()
  await nav.getByRole('button', { name: /NANO/ }).click()
  await expect(page.getByRole('button', { name: 'Load Finova sequencing demo' })).toBeVisible()
  await nav.getByRole('button', { name: /MACRO/ }).click()
  await expect(nav.getByRole('button', { name: /MACRO/ })).toHaveAttribute('aria-pressed', 'true')
  await expect(page.getByRole('textbox', { name: 'Raw TMT text' })).toBeVisible()
  await page.setViewportSize({ width: 812, height: 375 })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})

test('planning errors keep input and allow explicit retry; changing wording removes the prior draft', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Load Finova planning demo' }).click()
  const run = page.getByRole('button', { name: 'Run Planning Assistant' })
  await expect(run).toBeVisible()
  const original = await page.getByRole('textbox', { name: 'Raw TMT text' }).inputValue()
  let calls = 0
  await page.route('**/api/v1/development/planning-demo/draft', async route => {
    calls++
    if (calls === 1) await route.fulfill({ status: 503, json: { detail: 'Unavailable' } })
    else await route.continue()
  })
  await run.click()
  await expect(page.getByRole('alert')).toContainText('original text is preserved')
  expect(calls).toBe(1)
  await expect(page.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(original)
  await run.click()
  const article = page.getByRole('article', { name: 'Planning Assistant draft' })
  await expect(article).toBeVisible()
  await page.getByLabel('Wording preference').selectOption('TEMPLATES')
  await expect(article).toHaveCount(0)
  expect(calls).toBe(2)
})
