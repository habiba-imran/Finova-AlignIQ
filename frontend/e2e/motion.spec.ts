import { expect, test } from '@playwright/test'

test.use({ reducedMotion: 'no-preference' })

async function prepareParse(page: import('@playwright/test').Page) {
  await page.getByRole('button', { name: 'Load synthetic example' }).click()
  await page.getByRole('checkbox', { name: /I confirm this text is synthetic/ }).check()
}

test('module indicator and result entrance are brief, purposeful and do not preserve stale content', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const nav = page.getByRole('navigation', { name: 'Review purpose' })
  const indicator = nav.locator('.module-tab-indicator')
  const resting = await indicator.evaluate(element => getComputedStyle(element).transform)

  await nav.getByRole('button', { name: /MICRO/ }).click()
  await expect(nav.getByRole('button', { name: /MICRO/ })).toHaveAttribute('aria-pressed', 'true')
  await expect(page.getByRole('heading', { level: 1, name: 'Attachment Review' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toHaveCount(0)
  await expect.poll(async () => indicator.evaluate(element => getComputedStyle(element).transform)).not.toBe(resting)

  await nav.getByRole('button', { name: /MACRO/ }).click()
  await prepareParse(page)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  const panel = page.locator('section[aria-labelledby="structured-heading"]')
  const motion = await panel.evaluate(element => {
    const style = getComputedStyle(element)
    return { name: style.animationName, duration: style.animationDuration }
  })
  expect(motion.name).toBe('result-enter')
  expect(parseFloat(motion.duration)).toBeLessThanOrEqual(0.26)
  await panel.evaluate(element => Promise.all(element.getAnimations().map(animation => animation.finished)))
  expect(await panel.evaluate(element => getComputedStyle(element).opacity)).toBe('1')
  await expect(page.getByLabel('Parse summary')).toBeVisible()
  await expect(page.getByText('Parse response received. Source semantics remain unverified.')).toBeVisible()
})

test('loading controls expose a spinner and busy state while the explicit request is pending', async ({ page }) => {
  let parseRequests = 0
  await page.route('**/api/v1/tmt/parse', async route => {
    parseRequests += 1
    await new Promise(resolve => setTimeout(resolve, 500))
    await route.continue()
  })
  await page.goto('/', { waitUntil: 'networkidle' })
  await prepareParse(page)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()

  const busy = page.getByRole('button', { name: 'Parsing…' })
  await expect(busy).toBeDisabled()
  await expect(busy.locator('.button-spinner')).toBeVisible()
  await expect(page.getByRole('region', { name: 'Parse controls' })).toHaveAttribute('aria-busy', 'true')
  expect(parseRequests).toBe(1)

  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Parse controls' })).toHaveAttribute('aria-busy', 'false')
  await expect(page.getByRole('button', { name: 'Parse Table', exact: true })).toBeEnabled()
  expect(parseRequests).toBe(1)
})

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' })

  test('keeps results immediately visible and collapses decorative durations', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' })
    const nav = page.getByRole('navigation', { name: 'Review purpose' })
    const transition = await nav.locator('.module-tab-indicator').evaluate(element => getComputedStyle(element).transitionDuration)
    expect(parseFloat(transition)).toBeLessThan(0.01)

    await prepareParse(page)
    await page.getByRole('button', { name: 'Parse Table', exact: true }).click()
    await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
    const panel = page.locator('section[aria-labelledby="structured-heading"]')
    const motion = await panel.evaluate(element => {
      const style = getComputedStyle(element)
      return { duration: style.animationDuration }
    })
    expect(parseFloat(motion.duration)).toBeLessThan(0.01)
    await panel.evaluate(element => Promise.all(element.getAnimations().map(animation => animation.finished)))
    expect(await panel.evaluate(element => getComputedStyle(element).opacity)).toBe('1')
    await expect(page.getByLabel('Parse summary')).toBeVisible()
    await expect(page.getByText('Source verification: UNVERIFIED')).toBeVisible()
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  })
})
