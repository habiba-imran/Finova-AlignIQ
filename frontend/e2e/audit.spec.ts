import { expect, test } from '@playwright/test'

test('switching between all three loaded demos preserves text but cannot carry demo authority', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const nav = page.getByRole('navigation', { name: 'Review purpose' })
  const raw = page.getByRole('textbox', { name: 'Raw TMT text' })
  const pairs = [
    ['MACRO', 'planning', 'MICRO', 'attachments', 'Run Attachment Review'],
    ['MICRO', 'attachment', 'NANO', 'sequencing', 'Run Sequencing Review'],
    ['NANO', 'sequencing', 'MACRO', 'planning', 'Run Planning Assistant'],
  ] as const
  for (const [from, demo, to, module, action] of pairs) {
    await nav.getByRole('button', { name: new RegExp(from) }).click()
    await page.getByRole('button', { name: `Load Finova ${demo} demo` }).click()
    await expect(page.getByRole('button', { name: 'Parse Table', exact: true })).toBeEnabled()
    const original = await raw.inputValue()
    expect(original).toContain('1.2300 D')
    await nav.getByRole('button', { name: new RegExp(to) }).click()
    await expect(raw).toHaveValue(original)
    await expect(page.getByRole('article')).toHaveCount(0)
    await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
    const received = page.waitForResponse(r => r.url().endsWith(`/api/v1/${module}/draft`))
    await page.getByRole('button', { name: action, exact: true }).click()
    const response = await received, body = await response.json()
    expect(response.status()).toBe(200)
    expect(response.request().postDataJSON().raw_text).toBe(original)
    const review = module === 'planning' ? body.report.engine_review : body.engine_review
    expect(review.evidence_domain).toBe('UNVERIFIED')
    expect(review.coverage.eligible_positions).toBe(0)
    expect(review.evaluations.filter((e: { execution: string }) => e.execution === 'DISABLED')).toHaveLength(27)
    if (module === 'planning') expect(body.report.generation.attempts).toBe(0)
    else {
      expect(body.provider_attempts).toBe(0)
      expect(body.entries.every((e: { result_type: string }) => ['UNKNOWN', 'WITHHELD', 'DISABLED'].includes(e.result_type))).toBe(true)
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  }
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0])
})
