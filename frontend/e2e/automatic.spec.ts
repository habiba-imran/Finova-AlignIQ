import { expect, test } from '@playwright/test'
import automatic from '../src/test/fixtures/synthetic-automatic-unsupported.json' with { type: 'json' }
import recovered from '../src/test/fixtures/synthetic-phase4-recovery.json' with { type: 'json' }
import generated from '../src/phase4Example.json' with { type: 'json' }

test('source indicators are automatic, unverified and do not alter tooth metadata', async ({ page }, testInfo) => {
  await page.goto('/')
  await expect(page.getByRole('combobox', { name: /Source/ })).toHaveCount(0)
  const raw = '# SYNTHETIC ClinCheck-style, not a vendor export\nTooth\tRotation (deg)\n13\t−2.7500\n'
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(raw)
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const body = await (await pending).json()
  expect(body.pipeline.detection.detected_source).toBe('ClinCheck')
  expect(body.pipeline.detection.verified_source).toBe(null)
  expect(body.source.context.notation).toBe('UNKNOWN')
  expect(body.pipeline.assistance.attempts).toBe(0)
  await expect(page.getByText('Detected source: ClinCheck · DETECTED UNVERIFIED')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Try AI-assisted parsing' })).toHaveCount(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await testInfo.attach('automatic-source-indicator', { body: await page.getByLabel('Automatic detection and clarification').screenshot(), contentType: 'image/png' })
  await page.evaluate(() => { (document.activeElement as HTMLElement)?.blur(); scrollTo(0, 0) })
  await page.screenshot({ path: testInfo.outputPath('automatic-intake.png'), fullPage: true })
})

test('Markdown parses deterministically with cloud disabled and raw text survives', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Load synthetic Markdown example' }).click()
  await expect(page.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(automatic.raw_text)
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Parsed measurements' })).toBeVisible()
  await expect(page.getByText('Partially parsed', { exact: true })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Try AI-assisted parsing' })).toHaveCount(0)
  expect(await page.getByLabel('Raw text preview').textContent()).toBe(automatic.raw_text)
  await expect(page.getByRole('button', { name: 'Analyze', exact: true })).toBeDisabled()
})

test('mocked development recovery runs through one explicit parse without another checkbox', async ({ page }) => {
  // Mock ONLY this synthetic development transport; no browser test contacts Groq.
  let assistedCalls = 0
  await page.route('**/api/v1/tmt/parse', r => {
    assistedCalls++
    expect(r.request().postDataJSON()).toMatchObject({ raw_text: generated.raw_text, synthetic_fixture: generated.identity, synthetic_data_confirmed: true })
    expect(r.request().postDataJSON()).not.toHaveProperty('cloud_synthetic_consent')
    return r.fulfill({ json: recovered })
  })
  await page.goto('/')
  await page.getByRole('button', { name: 'Load generated recovery example' }).click()
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  expect(assistedCalls).toBe(0)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Parsed measurements' })).toBeVisible()
  await expect(page.getByText(/AI-assisted structure recovery/)).toBeVisible()
  await expect(page.getByRole('button', { name: 'Try AI-assisted parsing' })).toHaveCount(0)
  expect(assistedCalls).toBe(1)
  expect(await page.getByLabel('Raw text preview').textContent()).toBe(generated.raw_text)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
})

test('generated input with cloud disabled is retained and arbitrary edits remove authorization', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Load generated recovery example' }).click()
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const data = await (await pending).json()
  expect(data.pipeline.assistance.attempts).toBe(0)
  expect(data.pipeline.quality.classification).toBe('RECOVERABLE_STRUCTURE')
  await expect(page.getByRole('textbox', { name: 'Raw TMT text' })).toHaveValue(generated.raw_text)
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(generated.raw_text + ' edited')
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  const next = page.waitForRequest(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  expect((await next).postDataJSON()).not.toHaveProperty('synthetic_fixture')
})

test('ordinary non-TMT input is rejected without cloud traffic', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill('Product | Price\nBook | 13\n')
  await page.getByRole('checkbox', { name: /I confirm/ }).check()
  const pending = page.waitForResponse(r => r.url().endsWith('/api/v1/tmt/parse'))
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  const data = await (await pending).json()
  expect(data.pipeline.quality.classification).toBe('NOT_TMT')
  expect(data.pipeline.assistance.attempts).toBe(0)
  await expect(page.getByText('Unsupported input · not a TMT', { exact: true })).toBeVisible()
})
