import type { InteractiveReport } from './api/interactive'

/** Layout only: every word of the accepted observation wording is retained. */
export function commentParagraphs(text: string): string[] {
  return text.split(/\n+/).flatMap(line =>
    Array.from(new Intl.Segmenter('en', { granularity: 'sentence' }).segment(line), part => part.segment.trim())
  ).filter(Boolean)
}

export function moduleReviewPresentation(report: InteractiveReport) {
  const sections = report.sections ?? []
  if (report.report_format === 'ANALYTICAL_V1' || report.report_format === 'FUNCTIONAL_DEMO_V1') return { sections, scope: null }
  const automatic = report.module !== 'macro' && sections.some(section => section.status === 'SOURCE_REPORTED')
    && !!report.review_details && Object.values(report.review_details).every(rows => rows.length === 0)
  if (!automatic) return { sections, scope: null }
  return {
    sections: sections.filter(section => !section.section_id.endsWith('_LIMITS')),
    scope: report.module === 'micro'
      ? 'Movement observations only. Attachment selection, dimensions, placement and clinical suitability are not assessed.'
      : 'Movement observations only. Stage schedules, timing, anchorage and clinical suitability are not assessed.',
  }
}
