import { expect, it } from 'vitest'
import type { InteractiveReport } from './api/interactive'
import micro from './test/fixtures/interactive-micro.json'
import nano from './test/fixtures/interactive-nano.json'
import { commentParagraphs, moduleReviewPresentation } from './reviewPresentation'
import { buildPdfPresentation } from './pdf/presentation'

const normalize = (value: string) => value.replace(/\s+/g, ' ').trim()

it.each([micro, nano])('formats $module observations while retaining a clear scope note', fixture => {
  const report = fixture as InteractiveReport
  const result = moduleReviewPresentation(report)
  expect(result.sections).toHaveLength(3)
  expect(result.scope).toContain('not assessed')
  expect(result.sections.some(section => section.section_id.endsWith('_LIMITS'))).toBe(false)
  // Genuine unavailable source fields are still visible.
  expect(result.sections).toEqual(report.sections!.filter(section => !section.section_id.endsWith('_LIMITS')))
  const pdf = buildPdfPresentation('interactive', report)
  for (const section of result.sections) {
    const paragraphs = commentParagraphs(section.text)
    expect(normalize(paragraphs.join(' '))).toBe(normalize(section.text))
    for (const paragraph of paragraphs) expect(pdf.blocks).toContainEqual({ type: 'text', text: paragraph })
  }
  expect(pdf.blocks).toContainEqual({ type: 'text', text: result.scope })
  expect(report.sections).toHaveLength(4)
})

it('keeps exact decimals, explicit zeros and unknown statements when separating sentences', () => {
  const text = 'Tooth 11 records 1.2300 mm. Tooth 12 records 0.00 mm (explicitly recorded zero). Missing values remain unknown, not zero.'
  const paragraphs = commentParagraphs(text)
  expect(paragraphs).toHaveLength(3)
  expect(paragraphs.join(' ')).toBe(text)
})
