import { test, expect } from '@playwright/test'

test('shared empty states, aligned summaries, evidence disclosure and export order remain cohesive', async ({ page }, testInfo) => {
  await page.goto('/', { waitUntil: 'networkidle' })
  const modules = [
    { code: 'macro', nav: /MACRO/, load: 'Load Finova planning demo', run: 'Run Planning Assistant', article: 'Planning Assistant draft', copy: 'Copy complete DRAFT report', txt: 'Download DRAFT (TXT)' },
    { code: 'micro', nav: /MICRO/, load: 'Load Finova attachment demo', run: 'Run Attachment Review', article: 'Attachment review draft', copy: 'Copy attachment DRAFT', txt: 'Download attachment DRAFT (TXT)' },
    { code: 'nano', nav: /NANO/, load: 'Load Finova sequencing demo', run: 'Run Sequencing Review', article: 'Sequencing review draft', copy: 'Copy sequencing DRAFT', txt: 'Download sequencing DRAFT (TXT)' },
  ]
  for (const module of modules) {
    await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: module.nav }).click()
    await page.getByRole('button', { name: module.load }).click()
    await expect(page.getByRole('note').filter({ hasText: 'Review not started' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Export PDF', exact: true })).toHaveCount(0)
    await page.screenshot({ path: testInfo.outputPath(`${module.code}-intake.png`), fullPage: true })
    if (module.code === 'macro') await page.getByLabel('Wording preference').selectOption('TEMPLATES')
    await page.getByRole('button', { name: module.run, exact: true }).click()
    const article = page.getByRole('article', { name: module.article })
    await expect(article).toBeVisible()
    await expect(page.getByRole('note').filter({ hasText: 'Review not started' })).toHaveCount(0)
    const positions = await article.locator('.summary-metric').evaluateAll(nodes => nodes.map(node => {
      const r = node.getBoundingClientRect(); return { top: r.top, height: r.height }
    }))
    const firstRow = positions.filter(p => Math.abs(p.top - positions[0].top) < 2)
    expect(Math.max(...firstRow.map(p => p.height)) - Math.min(...firstRow.map(p => p.height))).toBeLessThan(2)
    const details = article.locator('.evidence-disclosure').first()
    await details.locator('summary').focus(); await page.keyboard.press('Enter')
    await expect(details).toHaveAttribute('open', '')
    await details.locator('summary').press('Enter')
    const buttons = [article.getByRole('button', { name: module.copy, exact: true }), article.getByRole('button', { name: module.txt, exact: true }), article.getByRole('button', { name: 'Export PDF', exact: true })]
    for (const button of buttons) await expect(button).toBeEnabled()
    for (let i = 1; i < buttons.length; i++) {
      const previous = await buttons[i - 1].elementHandle()
      expect(await buttons[i].evaluate((button, prior) => !!(prior!.compareDocumentPosition(button) & Node.DOCUMENT_POSITION_FOLLOWING), previous)).toBe(true)
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    await article.screenshot({ path: testInfo.outputPath(`${module.code}-review.png`) })
    await article.locator('.export-bar').screenshot({ path: testInfo.outputPath(`${module.code}-exports.png`) })
  }
})
