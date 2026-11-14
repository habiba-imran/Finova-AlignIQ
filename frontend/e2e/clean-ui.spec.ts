import { expect, test } from '@playwright/test'
import interactiveJSON from '../src/test/fixtures/interactive-macro.json' with { type: 'json' }

test('normal workspace has one source, concise results and visible exports in all three modules', async ({ page }, testInfo) => {
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(interactiveJSON.parsed.raw_text)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('region', { name: 'Structured TMT table' })).toBeVisible()
  for (const module of [
    { code: 'MACRO', demo: 'planning', run: 'Run Planning Assistant' },
    { code: 'MICRO', demo: 'attachment', run: 'Run Attachment Review' },
    { code: 'NANO', demo: 'sequencing', run: 'Run Sequencing Review' },
  ]) {
    await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: new RegExp(module.code) }).click()
    await expect(page.getByRole('button', { name: `Load Finova ${module.demo} demo` })).toHaveCount(0)
    const table = page.getByRole('region', { name: 'Structured TMT table' })
    await expect(table.getByRole('columnheader', { name: /Rotation/ })).toBeVisible()
    await expect(page.getByLabel('Raw text preview')).toHaveCount(0)
    await expect(page.getByLabel('Full parsing JSON')).toHaveCount(0)
    await expect(page.getByLabel('Wording preference')).toHaveCount(0)
    await page.getByRole('button', { name: module.run }).click()
    const article = page.getByRole('article')
    await expect(article).toBeVisible()
    expect(await article.innerText()).not.toMatch(/Groq|GROQ|rule ledger|provenance JSON|\b(?:R13|T01|A05|H08)\b/)
    for (const name of ['Copy', 'Export TXT', 'Export PDF']) await expect(article.getByRole('button', { name, exact: true })).toBeEnabled()
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    await page.screenshot({ path: testInfo.outputPath(`clean-${module.code.toLowerCase()}.png`), fullPage: true })
  }
})

test('unavailable demo is disabled with a short message and retains original input', async ({ page }) => {
  await page.route('**/api/v1/development/planning-demo/input', route => route.fulfill({ status: 404, json: { detail: 'PRIVATE_BACKEND_CONFIG' } }))
  await page.goto('/?diagnostics=1')
  const raw = page.getByRole('textbox', { name: 'Raw TMT text' })
  await raw.fill('original table retained')
  const demo = page.getByRole('button', { name: 'Load Finova planning demo' })
  await demo.click()
  await expect(demo).toBeDisabled()
  await expect(page.getByRole('alert')).toContainText('unavailable in this session')
  await expect(raw).toHaveValue('original table retained')
  await expect(page.getByText(/PRIVATE_BACKEND_CONFIG/)).toHaveCount(0)
})

test('automatic AI wording uses one review action and no main UI selection', async ({ page }) => {
  const enhanced = structuredClone(interactiveJSON)
  Object.assign(enhanced.generation, { used_mode: 'GROQ_AI', reason: 'GROQ_VALIDATED', attempts: 1, accepted_comments: 4, provider: 'GROQ', model: 'openai/gpt-oss-120b' })
  enhanced.wording_notice = 'AI-assisted wording generated with Groq; all measurements and examples assembled locally.'
  let requests = 0
  await page.route('**/api/v1/interactive/review', route => { requests++; return route.fulfill({ json: enhanced }) })
  await page.goto('/')
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(enhanced.parsed.raw_text)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await page.getByRole('button', { name: 'Run Planning Assistant' }).click()
  const article = page.getByRole('article', { name: 'Generated synthetic report' })
  await expect(article).toBeVisible()
  await expect(article.getByText('AI-assisted wording', { exact: true })).toBeVisible()
  expect(await article.innerText()).not.toMatch(/Groq|provider|transmission/i)
  await expect(page.getByLabel('Wording preference')).toHaveCount(0)
  await expect(page.getByRole('group', { name: 'Report wording views' })).toHaveCount(0)
  expect(requests).toBe(1)
})
