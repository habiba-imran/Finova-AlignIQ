/** Presentation of existing validated results only. No clinical selection or inference. */
import { isPlanningDraft } from '../api/planning'
import { isAttachmentDraft } from '../api/attachments'
import { isSequencingDraft, SEQUENCE_SECTIONS } from '../api/sequencing'
import { isFinalDraftReport } from '../api/report'
import type { FinalDraftReport, ReportComment } from '../api/report'
import type { PdfKind } from './reportPdf'
import { isInteractiveReport } from '../api/interactive'

export type PdfBlock = { type: 'heading'; text: string } | { type: 'text'; text: string } | { type: 'table'; headers: string[]; widths: number[]; rows: string[][] }
export interface PdfPresentation {
  summary: string[]; blocks: PdfBlock[]; limitations: string[]; missing: string[]; referenceGuide: string[]
}
const unique = (values: string[]) => [...new Set(values)]
const readable = (value: string) => value.replaceAll('_', ' ')
// Only the existing repeated fact-renderer lines move to source tables/attachments.
// Unexpected prose, including extra warnings, stays visible rather than being truncated.
const commentProse = (value: string) => value.split(/\r?\n/).filter(line => !['Programmed magnitude:', 'Required information:', 'Assessment withheld:'].some(prefix => line.startsWith(prefix))).join('\n')
const heading = (text: string): PdfBlock => ({ type: 'heading', text })
const text = (value: string): PdfBlock => ({ type: 'text', text: value })

function compactIndices(indices: number[]): string {
  const ranges: string[] = []
  let i = 0
  while (i < indices.length) {
    const start = indices[i]; let end = start
    while (i + 1 < indices.length && indices[i + 1] === end + 1) end = indices[++i]
    ranges.push(start === end ? `C${start}` : `C${start}-C${end}`); i++
  }
  return ranges.join(', ')
}

function macroBlocks(report: FinalDraftReport, sections: { dimension: string; comment_ids: string[]; explanation: string }[], prefix: string): PdfPresentation {
  const blocks: PdfBlock[] = [], unavailable = report.comments.filter(c => c.section === 'UNAVAILABLE')
  const commentIndex = (c: ReportComment) => report.comments.indexOf(c) + 1
  for (const section of sections.filter(s => s.dimension !== 'UNAVAILABLE')) {
    blocks.push(heading(section.dimension === 'OTHER' ? 'Other observations' : readable(section.dimension)))
    blocks.push(text(section.explanation))
    for (const id of section.comment_ids) {
      const c = report.comments.find(c => c.comment_id === id)!, ref = `C${commentIndex(c)}`
      blocks.push(text(`${ref} | ${c.evidence_status} | DRAFT\n${commentProse(c.text)}`))
      if (c.measurements.length) blocks.push({ type: 'table', headers: ['Source token / label', 'Original value', 'Exact scalar', 'Source / evidence'], widths: [177, 106, 92, 136.28],
        rows: c.measurements.map(m => [`${m.raw_tooth_identifier} | ${m.raw_label}`, m.raw_value, m.signed_decimal,
          `${ref} / ${m.measurement_id}\n${m.verification}\n${m.source_spans.map(s => `L${s.line}:C${s.column_start}`).join('; ')}`]) })
    }
  }
  blocks.push(heading('Unavailable assessments'))
  // Identical outcome/status prose is displayed once; every original comment is referenced.
  const groups = new Map<string, { message: string; status: string; indices: number[] }>()
  for (const c of unavailable) {
    const message = commentProse(c.text), status = c.evaluation_statuses.join(', '), key = JSON.stringify([message, status, c.evidence_status])
    const group = groups.get(key) ?? { message, status, indices: [] }
    group.indices.push(commentIndex(c)); groups.set(key, group)
  }
  for (const group of groups.values()) blocks.push(text(`${group.message}\n${group.indices.length} unavailable results | ${group.status}\nReferences: ${compactIndices(group.indices)}.`))
  const reasons = unique(unavailable.flatMap(c => c.abstain_reasons))
  if (reasons.length) blocks.push(text(`Withheld reasons: ${reasons.map(readable).join('; ')}.`))
  if (!unavailable.length) blocks.push(text('No unavailable comment rows were supplied. This does not establish complete clinical assessment.'))
  const coverage = report.engine_review.coverage
  return {
    summary: [`Input verification: ${report.engine_review.evidence_domain}. Vendor semantics remain unverified; TEST_ONLY is fictional engineering evidence, not vendor verification.`,
      `${coverage.eligible_positions} of ${coverage.declared_positions} positions eligible for descriptions; ${coverage.unavailable_positions} unavailable. ${report.comments.length - unavailable.length} descriptive comment units; ${unavailable.length} unavailable assessments. Missing is not zero; unavailable is not normal.`,
      'Dimensions organize descriptions only. No complete clinical dimension, treatment decision or approval is established.'],
    blocks, limitations: unique(report.limitations), missing: unique(report.comments.flatMap(c => c.missing_required_fields)),
    referenceGuide: [`C<n> identifies ${prefix}comments[n-1] in validated-report.json, including full finding IDs, evidence_refs, measurements and exact source spans. Unavailable reference ranges include every original comment, without merging its evidence.`,
      `Input source: ${prefix}engine_review.source. Full rule outcomes and original text remain in the attachments and existing TXT export.`],
  }
}

export function buildPdfPresentation(kind: PdfKind, input: unknown): PdfPresentation {
  if (kind === 'interactive' && isInteractiveReport(input)) {
    const blocks: PdfBlock[] = [heading('Factual tooth-wise observations')]
    for (const o of input.observations) blocks.push(heading('Tooth observation'), text(`Tooth token ${o.original_tooth}\n${o.text}`))
    if (input.illustrations.length) {
      blocks.push(heading('Illustrative demo content'), text('SIMULATED DEMO - not calculated treatment findings or recommendations.'))
      for (const i of input.illustrations) blocks.push(text(`Tooth token ${i.original_tooth}\n${i.label}: ${i.text}`))
    }
    return { summary: [input.module.toUpperCase(), input.summary, input.wording_notice], blocks,
      limitations: input.limitations, missing: [], referenceGuide: ['Exact source cells, Decimal strings, direction labels and source spans: /parsed/measurements in validated-report.json. The original input and complete 96-rule ledger remain in the embedded TXT and JSON.'] }
  }
  if (kind === 'macro' && isPlanningDraft(input)) return macroBlocks(input.report, input.sections, '/report/')
  if (kind === 'descriptive' && isFinalDraftReport(input)) return macroBlocks(input,
    [{ dimension: 'Observations', comment_ids: input.comments.filter(c => c.section !== 'UNAVAILABLE').map(c => c.comment_id), explanation: 'Evidence-controlled descriptive observations only.' }], '/')
  if (kind === 'micro' && isAttachmentDraft(input)) {
    const labels = { CANDIDATE: 'Supplied candidate', ALTERNATIVE: 'Supplied alternative', NOT_INDICATED: 'Supplied no attachment', UNKNOWN: 'Unknown', WITHHELD: 'Withheld' }
    return {
      summary: [`Input verification: ${input.evidence_domain}. Vendor semantics and clinical attachment policies remain unapproved.`,
        `${input.entries.filter(e => e.result_type === 'CANDIDATE').length} supplied candidates; ${input.entries.filter(e => e.result_type === 'ALTERNATIVE').length} alternatives; ${input.entries.filter(e => e.result_type === 'NOT_INDICATED').length} supplied no-attachment rows; ${input.entries.filter(e => ['UNKNOWN', 'WITHHELD'].includes(e.result_type)).length} unknown/withheld.`,
        'Positive choices and geometry are supplied fictional inputs. Unknown/withheld is not no attachment; no omission is inferred from zero or missing movement.'],
      blocks: [heading('Tooth-wise attachment review'), { type: 'table', headers: ['Original token', 'Status / origin', 'Supplied option / geometry', 'Explanation / source'], widths: [53, 110, 154, 194.28], rows: input.entries.map((e, i) => {
        const d = e.design, alternative = e.alternative_for ? input.entries.findIndex(c => c.entry_id === e.alternative_for) + 1 : null
        return [e.original_tooth ?? 'UNKNOWN', `${labels[e.result_type]}\n${readable(e.decision_origin)}\n${e.evidence_status}\nNOT APPROVED / DRAFT`,
          d ? `${d.label}\nShape: ${d.shape ?? 'UNKNOWN'}\nOrientation: ${d.orientation ?? 'UNKNOWN'}\n${d.dimensions ? `${d.dimensions.x} x ${d.dimensions.y} x ${d.dimensions.z} ${d.dimensions.unit}` : 'Dimensions: UNKNOWN'}\n${e.placement ? `Surface: ${e.placement.surface_id}; frame: ${e.placement.frame_id}; stage: ${e.placement.stage_ref ?? 'UNKNOWN'}` : 'Placement: UNKNOWN'}` : e.result_type === 'NOT_INDICATED' ? 'No attachment - supplied fictional decision' : 'No authorized option',
          `${e.explanation}\n${alternative ? `Alternative for A${alternative}.\n` : ''}Source: A${i + 1}${e.observation_refs.length ? ` / ${e.observation_refs.join(', ')}` : ' / no authorized observation'}.`]
      }) }, heading('Exact observed source values'), { type: 'table', headers: ['Original token / label', 'Original value', 'Exact scalar', 'Source / evidence'], widths: [177, 106, 92, 136.28],
        rows: [...new Map(input.engine_review.findings.flatMap(f => f.observed_measurements).map(m => [m.measurement_id, m])).values()].map(m => [`${m.raw_tooth_identifier} | ${m.raw_label}`, m.raw_value, m.signed_decimal, `${m.measurement_id} / ${m.verification}\n${m.source_spans.map(s => `L${s.line}:C${s.column_start}`).join('; ')}`]) }], limitations: unique(input.limitations), missing: unique(input.entries.flatMap(e => e.missing_prerequisites)),
      referenceGuide: ['A<n> identifies /entries[n-1] in validated-report.json: complete evidence_refs, measurement_refs, observation_refs, finding_refs, missing prerequisites and supplied geometry. Original token is not a verified anatomical identity.',
        'Exact observed measurements and source spans: /engine_review/findings/*/observed_measurements. Full technical record remains in report.txt, validated-report.json and existing TXT export.'],
    }
  }
  if (kind === 'nano' && isSequencingDraft(input)) {
    const titles = { UPPER_ARCH: 'Upper-arch sequencing', LOWER_ARCH: 'Lower-arch sequencing', SEGMENTS: 'Segments & tooth groups', RIGHT_ANCHORAGE: 'Right-side anchorage', LEFT_ANCHORAGE: 'Left-side anchorage', UNAVAILABLE: 'Unavailable assessments' }
    const blocks: PdfBlock[] = [heading('Stage information'), text(`${input.stage_inspection.status} | ${input.stage_inspection.movement_binding}\n${input.stage_inspection.explanation}`)]
    if (input.stage_inspection.issues.length) blocks.push(text(`Stage issues: ${input.stage_inspection.issues.join('; ')}`))
    for (const section of SEQUENCE_SECTIONS) {
      blocks.push(heading(titles[section]))
      for (const e of input.entries.filter(e => e.section === section)) {
        const index = input.entries.indexOf(e) + 1
        blocks.push(text(`N${index} | ${readable(e.result_type)} | ${e.evidence_status} | ${readable(e.origin)} | DRAFT\n${e.text}\nOriginal tokens: ${e.original_tooth_tokens.join(', ') || 'UNKNOWN'}; side: ${e.side}; scope: ${e.movement_scope}.${e.stage_window ? ` Supplied stage IDs: ${e.stage_window.start_id} → ${e.stage_window.end_id}; no movement allocation.` : ' Stage window unavailable.'}`))
      }
    }
    blocks.push(heading('Original lexical values - not stage allocations'), { type: 'table', headers: ['Token / original label', 'Original value', 'Exact scalar', 'Lexical status / source'], widths: [177, 106, 92, 136.28],
      rows: input.parsed.measurements.map(m => [`${input.parsed.teeth.find(t => t.id === m.tooth_ref)!.raw_identifier} | ${m.raw_label}`, m.raw_value ?? '(omitted cell)', m.signed_decimal ?? '(unavailable)', `${m.numeric_status}\n${m.id}`]) })
    return { summary: [`Input verification: ${input.evidence_domain}. Vendor semantics remain unverified.`,
      `${input.entries.filter(e => e.result_type === 'SUPPLIED_SYNTHETIC').length} supplied fictional notes; ${input.entries.filter(e => ['UNKNOWN', 'WITHHELD', 'DISABLED'].includes(e.result_type)).length} unknown, withheld or disabled results.`,
      `${input.stage_inspection.records.length} supplied stage metadata records; NO_STAGE_MOVEMENT_BINDING. No clinical order, timing, force, auxiliary or anchorage need is calculated.`],
      blocks, limitations: unique(input.limitations), missing: unique(input.entries.flatMap(e => e.missing_prerequisites)),
      referenceGuide: ['N<n> identifies /entries[n-1] in validated-report.json, including evidence_refs, finding_refs, measurement_refs, exact statement origin and missing prerequisites. Stage information: /stage_inspection.',
        'Original values, Decimal strings, missing/zero states and source spans: /parsed/measurements. These are not stage allocations. Full technical evidence remains in the attachments and existing TXT export.'],
    }
  }
  throw new Error('PDF_INVALID_REPORT')
}
