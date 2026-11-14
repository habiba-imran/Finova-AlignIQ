import { expect, test } from 'vitest'
import { buildPdfPresentation } from './presentation'
import macro from '../test/fixtures/planning-demo-draft.json'
import micro from '../test/fixtures/attachment-demo-draft.json'
import nano from '../test/fixtures/sequencer-demo-draft.json'
import ordinary from '../test/fixtures/attachment-unverified-draft.json'

test('Macro retains every descriptive comment, exact scalar, source span and unavailable reference', () => {
  const model = buildPdfPresentation('macro', macro), visible = JSON.stringify(model.blocks)
  for (const name of ['SAGITTAL', 'TRANSVERSE', 'VERTICAL', 'Other observations']) expect(visible).toContain(name)
  macro.report.comments.filter(c => c.section !== 'UNAVAILABLE').forEach(c => {
    expect(visible).toContain(c.text.split('\n')[0])
    c.measurements.forEach(m => { expect(visible).toContain(m.raw_value); expect(visible).toContain(m.signed_decimal); expect(visible).toContain(m.measurement_id) })
  })
  const included = new Set<number>()
  for (const block of model.blocks) if (block.type === 'text' && block.text.includes('References:')) {
    for (const match of block.text.split('References:')[1].matchAll(/C(\d+)(?:-C(\d+))?/g)) {
      for (let n = Number(match[1]); n <= Number(match[2] ?? match[1]); n++) included.add(n)
    }
  }
  expect([...included].sort((a, b) => a - b)).toEqual(macro.report.comments.flatMap((c, i) => c.section === 'UNAVAILABLE' ? [i + 1] : []))
  expect(new Set(model.missing)).toEqual(new Set(macro.report.comments.flatMap(c => c.missing_required_fields)))
  expect(model.limitations).toEqual([...new Set(macro.report.limitations)])
  expect(model.referenceGuide.join(' ')).toContain('/report/comments[n-1]')
  expect(visible).not.toContain('RULE EVALUATION LEDGER')
})

test('Micro preserves every supplied/unknown/withheld row, geometry, alternative and exact observations', () => {
  const model = buildPdfPresentation('micro', micro), tables = model.blocks.filter(b => b.type === 'table')
  expect(tables[0].rows).toHaveLength(micro.entries.length)
  micro.entries.forEach((e, i) => {
    const row = tables[0].rows[i].join(' ')
    expect(row).toContain(e.explanation)
    expect(row).toContain(e.evidence_status)
    expect(row).toContain(`A${i + 1}`)
    if (e.design?.dimensions) for (const value of [e.design.dimensions.x, e.design.dimensions.y, e.design.dimensions.z]) expect(row).toContain(value)
  })
  expect(tables[0].rows[1].join(' ')).toContain('Alternative for A1')
  expect(tables[0].rows[3].join(' ')).toContain('supplied fictional decision')
  expect(tables[0].rows[4].join(' ')).toContain('Unknown')
  expect(tables[0].rows[5].join(' ')).toContain('Withheld')
  expect(new Set(model.missing)).toEqual(new Set(micro.entries.flatMap(e => e.missing_prerequisites)))
  expect(model.limitations).toEqual([...new Set(micro.limitations)])
})

test('Nano includes all exact statements, side/scope/window context, missing states and original lexical values', () => {
  const model = buildPdfPresentation('nano', nano), visible = JSON.stringify(model.blocks)
  nano.entries.forEach(e => { expect(visible).toContain(e.text.replaceAll('\n', '\\n')); expect(visible).toContain(e.result_type.replaceAll('_', ' ')) })
  expect(visible).toContain('NO_STAGE_MOVEMENT_BINDING')
  expect(visible).toContain('Right-side anchorage'); expect(visible).toContain('Left-side anchorage')
  const rows = model.blocks.filter(b => b.type === 'table')[0].rows
  expect(rows.map(r => r[1])).toEqual(nano.parsed.measurements.map(m => m.raw_value ?? '(omitted cell)'))
  expect(rows.map(r => r[2])).toEqual(nano.parsed.measurements.map(m => m.signed_decimal ?? '(unavailable)'))
  expect(model.limitations).toEqual([...new Set(nano.limitations)])
  expect(new Set(model.missing)).toEqual(new Set(nano.entries.flatMap(e => e.missing_prerequisites)))
})

test('ordinary report remains explicitly unverified and preserves all unknown/withheld explanations', () => {
  const model = buildPdfPresentation('micro', ordinary)
  expect(model.summary.join(' ')).toContain('UNVERIFIED')
  const visible = JSON.stringify(model.blocks)
  ordinary.entries.forEach(e => expect(visible).toContain(e.explanation.replaceAll('\n', '\\n')))
  expect(model.limitations).toEqual([...new Set(ordinary.limitations)])
})

test('additional warning prose is retained even when repeated technical facts are moved to attachments', () => {
  const data = structuredClone(macro), old = data.report.comments[0].text
  data.report.comments[0].text += '\nAdditional supplied warning: no clinical approval.'
  data.report.export_text = data.report.export_text.replace(old, data.report.comments[0].text)
  data.export_text = data.export_text.replace(old, data.report.comments[0].text)
  expect(JSON.stringify(buildPdfPresentation('macro', data).blocks)).toContain('Additional supplied warning: no clinical approval.')
})
