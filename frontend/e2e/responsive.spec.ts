import { expect, test } from '@playwright/test'

const WIDTHS = [1440, 1024, 768, 672, 375] as const

test('context heading, compact module tabs and layout remain usable at every target width', async ({ page }, testInfo) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const nav = page.getByRole('navigation', { name: 'Review purpose' })

  await expect(page.getByRole('heading', { level: 1, name: 'Planning Assistant' })).toBeVisible()
  await expect(page.getByText('Review programmed movements and prepare structured draft comments.')).toBeVisible()
  await expect(nav.getByRole('button', { name: /MACRO/ })).toHaveAttribute('aria-pressed', 'true')

  await nav.getByRole('button', { name: /MICRO/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Attachment Review' })).toBeVisible()
  await expect(page.getByText('Inspect tooth-wise attachment information and supporting evidence.')).toBeVisible()
  await expect(nav.getByRole('button', { name: /MICRO/ })).toHaveAttribute('aria-pressed', 'true')

  await nav.getByRole('button', { name: /NANO/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Sequencing Review' })).toBeVisible()
  await expect(page.getByText('Review sequencing information, segment notes and anchorage context.')).toBeVisible()
  await expect(nav.getByRole('button', { name: /NANO/ })).toHaveAttribute('aria-pressed', 'true')

  await nav.getByRole('button', { name: /MACRO/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Planning Assistant' })).toBeVisible()

  for (const width of WIDTHS) {
    await page.setViewportSize({ width, height: 1000 })
    await expect(nav).toBeVisible()
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    for (const code of ['MACRO', 'MICRO', 'NANO']) {
      const tab = nav.getByRole('button', { name: new RegExp(code) })
      const box = await tab.boundingBox()
      expect(box).not.toBeNull()
      expect(box!.width).toBeGreaterThanOrEqual(88)
      expect(box!.height).toBeGreaterThanOrEqual(44)
    }
    const sizes = await nav.locator('button').evaluateAll(buttons => buttons.map(button => {
      const code = button.querySelector('.module-tab-code'), label = button.querySelector('.module-tab-label')
      return [parseFloat(getComputedStyle(code!).fontSize), parseFloat(getComputedStyle(label!).fontSize)]
    }))
    for (const [codeSize, labelSize] of sizes) {
      expect(codeSize).toBeGreaterThanOrEqual(11)
      expect(labelSize).toBeGreaterThanOrEqual(13)
    }
    await page.screenshot({ path: testInfo.outputPath(`refined-intake-${width}.png`), fullPage: true })
  }
})

test('workflow progress distinguishes input, completed inspection, active review and available export', async ({ page }, testInfo) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const progress = page.getByRole('list', { name: 'Planning workflow' })
  await expect(progress.locator('li[aria-current="step"]')).toContainText('Input')
  await expect(progress.locator('li[data-state="complete"]')).toHaveCount(0)

  await page.getByRole('button', { name: 'Load Finova planning demo' }).click()
  await expect(page.getByRole('button', { name: 'Run Planning Assistant' })).toBeVisible()
  await expect(progress.locator('li[data-state="complete"]')).toHaveCount(2)
  await expect(progress.locator('li[aria-current="step"]')).toContainText('Planning review')
  await expect(progress.locator('li[aria-current="step"]')).toContainText('Run review')
  await expect(progress.getByText('Available')).toHaveCount(0)

  await page.getByRole('button', { name: 'Run Planning Assistant' }).click()
  await expect(page.getByRole('article', { name: 'Planning Assistant draft' })).toBeVisible()
  await expect(progress.locator('li[data-state="complete"]')).toHaveCount(3)
  await expect(progress.locator('li[aria-current="step"]')).toContainText('Export')
  await expect(progress.locator('li[aria-current="step"]')).toContainText('Available')

  await page.screenshot({ path: testInfo.outputPath('refined-review-1440.png'), fullPage: true })
  await page.setViewportSize({ width: 375, height: 1000 })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath('refined-review-375.png'), fullPage: true })

  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})
