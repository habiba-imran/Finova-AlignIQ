import { expect, test } from '@playwright/test'

const presentationTable = '# SYNTHETIC\nTooth\tRotation (deg)\tExtrusion (mm)\tUnknown label\n11\t-1.2300 M\t0.50 E\t3\n12\t0\t—\t4\n13\t2.3 D\t0\t5\n'

test('parse presentation promotes movement inspection and keeps raw source and diagnostics available', async ({ page }, testInfo) => {
  await page.goto('/?diagnostics=1', { waitUntil: 'networkidle' })
  await expect(page.getByText('Parse your TMT to see the structured table.')).toBeVisible()
  await page.getByRole('textbox', { name: 'Raw TMT text' }).fill(presentationTable)
  await page.getByRole('button', { name: 'Parse Table', exact: true }).click()

  await expect(page.getByText('Parse your TMT to see the structured table.')).toHaveCount(0)
  const structured = page.getByRole('region', { name: 'Structured TMT table' })
  await expect(structured).toBeVisible()
  await expect(structured.getByRole('columnheader', { name: /Rotation/ })).toBeVisible()
  await expect(structured.getByRole('columnheader', { name: /Extrusion/ })).toBeVisible()
  await expect(structured.getByRole('columnheader', { name: /Unknown label/ })).toContainText('Unrecognized')
  await expect(structured.getByRole('rowheader', { name: /13/ })).toBeVisible()
  expect(await structured.evaluate(element => element.scrollWidth <= element.clientWidth)).toBe(true)

  await expect(page.getByRole('heading', { name: 'Structured lexical preview' })).toBeVisible()
  const summary = page.getByLabel('Parse summary')
  await expect(summary).toBeVisible()
  for (const metric of ['Tooth rows', 'Movement positions', 'Missing values', 'Explicit zeros']) await expect(summary).toContainText(metric)
  await expect(page.getByText('Source verification: UNVERIFIED')).toBeVisible()

  const measurements = page.getByRole('region', { name: 'Parsed measurements' })
  await expect(measurements).toBeVisible()
  await measurements.getByText('Row details', { exact: true }).first().click()
  await expect(measurements.getByText('Semantic verification: NOT VERIFIED.', { exact: true }).first()).toBeVisible()

  const preview = page.getByLabel('Raw text preview')
  expect(await preview.evaluate(element => !element.closest('details')?.hasAttribute('open'))).toBe(true)
  await page.locator('summary', { hasText: 'Raw preview · original TMT text' }).click()
  await expect(preview).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Parsing warnings and errors' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Fields requiring clarification or verification' })).toBeVisible()

  await page.setViewportSize({ width: 375, height: 1000 })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  const firstStructuredCell = structured.locator('tbody td').first()
  await expect(firstStructuredCell).toHaveCSS('display', 'grid')
  expect(await firstStructuredCell.getAttribute('data-label')).toContain('Rotation')
  expect(await structured.evaluate(element => element.scrollWidth <= element.clientWidth)).toBe(true)
  const overflow = await measurements.evaluate(element => ({ scroll: element.scrollWidth, client: element.clientWidth }))
  expect(overflow.scroll).toBeGreaterThan(overflow.client)
  await page.screenshot({ path: testInfo.outputPath('parser-presentation-375.png'), fullPage: true })
})

test('result reports remain the workflow destination and Micro stacks into readable cards at 375', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 375, height: 1000 })
  await page.goto('/?diagnostics=1', { waitUntil: 'networkidle' })
  await page.getByRole('navigation', { name: 'Review purpose' }).getByRole('button', { name: /MICRO/ }).click()
  await page.getByRole('button', { name: 'Load Finova attachment demo' }).click()
  await page.getByRole('button', { name: 'Run Attachment Review' }).click()

  const article = page.getByRole('article', { name: 'Attachment review draft' })
  await expect(article).toBeVisible()
  await expect(article.getByText('DRAFT', { exact: true })).toBeVisible()
  await expect(article.getByText('DRAFT — Requires Orthodontist Review', { exact: true })).toBeVisible()
  await expect(article.getByLabel('Attachment review summary')).toBeVisible()
  await expect(article.getByRole('table')).toContainText('Supplied candidate')
  expect(await article.locator('tbody tr').first().evaluate(element => getComputedStyle(element).display)).toBe('block')
  await article.getByText('Details & provenance · row 1').click()
  await expect(article.getByText('Supplied dimensions: 2.000 × 1.250 × 0.500 mm', { exact: true })).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: testInfo.outputPath('micro-cards-375.png'), fullPage: true })
})
