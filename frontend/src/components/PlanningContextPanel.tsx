import { useState } from 'react'
import type { DemoModule, ReviewDetails } from '../api/interactive'
import type { ParseResult } from '../api/parse'
import type { PlanningOptions } from '../api/planningOptions'
import { CONCEPT_LABELS } from '../api/functional'
import type { AttachmentOption, Concept } from '../api/functional'

const field = 'mt-1 block w-full min-w-0 rounded-lg border border-field bg-white px-3 py-2 text-sm'
const decimal = (value: string) => /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value) && value.length <= 24

export default function PlanningContextPanel({ module, parsed, options, details, onChange }: {
  module: DemoModule; parsed: ParseResult; options: PlanningOptions; details: ReviewDetails
  onChange: (options: PlanningOptions, details: ReviewDetails) => void
}) {
  const cells = parsed.measurements.filter(m => m.recognized_label && ['mm', 'deg'].includes(m.unit ?? ''))
  const teeth = new Map(parsed.teeth.map(t => [t.id, t.raw_identifier.trim()]))
  const describe = (id: string) => { const m = cells.find(m => m.id === id)!; return `Tooth ${teeth.get(m.tooth_ref)} · ${m.recognized_label?.replaceAll('_', ' ')} · ${m.signed_decimal ?? 'unknown'} ${m.unit}${m.raw_direction ? ` (${m.raw_direction})` : ''}` }
  const change = (patch: Partial<PlanningOptions>) => onChange({ ...options, ...patch }, details)
  const [concept, setConcept] = useState<Concept>('RECTANGULAR')
  const [dimensions, setDimensions] = useState(['', '', ''])
  const [orientation, setOrientation] = useState<AttachmentOption['orientation']>(null)
  const [surface, setSurface] = useState<AttachmentOption['surface']>(null)
  const [placement, setPlacement] = useState(false)
  const [coordinates, setCoordinates] = useState(['', '', ''])
  const [catalogError, setCatalogError] = useState('')
  const [supportPhase, setSupportPhase] = useState('')
  const [supportTeeth, setSupportTeeth] = useState<string[]>([])
  const [activeTeeth, setActiveTeeth] = useState<string[]>([])
  const [stationary, setStationary] = useState(false)

  function applyCatalog() {
    const hasDimensions = dimensions.some(Boolean)
    if (hasDimensions && !dimensions.every(v => decimal(v) && Number(v) > 0) || placement && !coordinates.every(decimal)) {
      setCatalogError('Supply all three positive dimensions and all selected local coordinates, or leave them unspecified.'); return
    }
    const item: AttachmentOption = { concept, geometry: hasDimensions ? { width_mm: dimensions[0], height_mm: dimensions[1], depth_mm: dimensions[2] } : null,
      orientation, surface, placement: placement ? { frame: 'FICTIONAL_TOOTH_LOCAL_MM', x_mm: coordinates[0], y_mm: coordinates[1], z_mm: coordinates[2] } : null }
    setCatalogError(''); change({ attachment_options: [...options.attachment_options.filter(o => o.concept !== concept), item] })
  }

  function renameStage(index: number, id: string) {
    const old = details.stages[index].stage_id
    onChange({ ...options, phases: options.phases.map(p => ({ ...p, stage_ids: p.stage_ids.map(s => s === old ? id : s) })) },
      { ...details, stages: details.stages.map((s, i) => i === index ? { ...s, stage_id: id } : s), allocations: details.allocations.map(a => a.stage_id === old ? { ...a, stage_id: id } : a) })
  }

  function assignPhase(stage: string, phase: string) {
    const phases = options.phases.map(p => ({ ...p, stage_ids: p.stage_ids.filter(s => s !== stage) })).filter(p => p.stage_ids.length)
    if (phase) {
      const existing = phases.find(p => p.phase_id === phase)
      if (existing) existing.stage_ids.push(stage)
      else phases.push({ phase_id: phase, label: phase, stage_ids: [stage] })
    }
    change({ phases })
  }

  function addStage() {
    let n = 1
    while (details.stages.some(s => s.stage_id === `S${n}`)) n++
    onChange(options, { ...details, stages: [...details.stages, { stage_id: `S${n}`, order: Math.max(0, ...details.stages.map(s => s.order)) + 1, duration_days: null }] })
  }

  return <details className="mt-4 rounded-lg border border-line p-3 text-sm leading-6" aria-label="Optional planning context">
    <summary className="cursor-pointer font-medium">Planning context <span className="font-normal text-muted">· optional</span></summary>
    <p className="mt-2 text-xs text-muted">The pasted table is enough for a review. Add only the objectives or records you want this module to use.</p>
    <label className="mt-3 block text-xs font-medium">Policy mode
      <select className={field} value={options.policy_mode} onChange={e => change({ policy_mode: e.target.value as PlanningOptions['policy_mode'] })}>
        <option value="SYNTHETIC_REVIEW">Illustrative review</option><option value="EVIDENCE_REVIEW">Evidence review only</option>
      </select>
    </label>
    {module === 'macro' && <div className="mt-4 space-y-3">
      <label className="block text-xs font-medium">Planning objective
        <select className={field} value={options.objectives[0] ?? ''} onChange={e => change({ objectives: e.target.value ? [e.target.value] : [] })}>
          <option value="">No modification objective supplied</option><option value="REDISTRIBUTE_TRANSLATIONS">Review translation distribution</option><option value="VERTICAL_REVIEW">Review vertical relationships</option><option value="ANGULAR_CONTROL">Review angular control</option>
        </select>
      </label>
      <label className="flex items-start gap-2 text-xs"><input type="checkbox" className="mt-1" checked={options.source_convention === 'SOURCE_LABELS_AS_RECORDED'} onChange={e => change({ source_convention: e.target.checked ? 'SOURCE_LABELS_AS_RECORDED' : 'UNSPECIFIED' })} />Use the source labels as recorded for a fictional modification example.</label>
      <label className="block text-xs font-medium">Source measurement
        <select className={field} value={options.illustration_measurement_ref ?? ''} onChange={e => change({ illustration_measurement_ref: e.target.value || null, targets: [] })}>
          <option value="">Choose a source field only if proposing an example</option>{cells.filter(m => ['PARSED', 'EXPLICIT_ZERO'].includes(m.numeric_status) && m.field_status !== 'AMBIGUOUS').map(m => <option key={m.id} value={m.id}>{describe(m.id)}</option>)}
        </select>
      </label>
      <label className="block text-xs font-medium">Modification example
        <select className={field} value={options.illustration} onChange={e => change({ illustration: e.target.value as PlanningOptions['illustration'], targets: [] })}>
          <option value="NONE">Use an explicitly supplied replacement, or none</option><option value="HALF_MAGNITUDE">Fictional arithmetic: half the selected source value</option>
        </select>
      </label>
      {options.illustration === 'HALF_MAGNITUDE' ? <p className="text-xs text-muted">Method: source scalar ÷ 2, retaining its label. This is a transparent simulation, not a clinically justified target.</p> : <label className="block text-xs font-medium">Supplied replacement value <span className="font-normal">· optional</span>
        <input className={field} inputMode="decimal" value={options.targets[0]?.amount ?? ''} disabled={!options.illustration_measurement_ref} placeholder="Leave blank for review requests only" onChange={e => {
          const m = cells.find(m => m.id === options.illustration_measurement_ref)
          if (m) change({ targets: e.target.value ? [{ measurement_ref: m.id, amount: e.target.value, unit: m.unit as 'mm' | 'deg', source_direction: m.raw_direction }] : [] })
        }} />
      </label>}
    </div>}
    {module === 'micro' && <details className="mt-4 border-t border-line pt-3">
      <summary className="cursor-pointer font-medium">Supplied catalog specifications</summary>
      <p className="mt-2 text-xs text-muted">Category-only examples need no dimensions. Supply geometry and placement only when you have specifications.</p>
      <label className="mt-3 block text-xs font-medium">Catalog category<select className={field} value={concept} onChange={e => { setConcept(e.target.value as Concept); setDimensions(['', '', '']); setOrientation(null); setSurface(null); setPlacement(false); setCoordinates(['', '', '']) }}>
        {Object.entries(CONCEPT_LABELS).filter(([c]) => c !== 'NO_ATTACHMENT').map(([c, label]) => <option key={c} value={c}>{label}</option>)}
      </select></label>
      <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-3">{['Width', 'Height', 'Depth'].map((label, i) => <label key={label} className="text-xs font-medium">{label} (mm)<input className={field} inputMode="decimal" value={dimensions[i]} placeholder="Unspecified" onChange={e => setDimensions(previous => previous.map((v, n) => n === i ? e.target.value : v))} /></label>)}</div>
      <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <label className="text-xs font-medium">Supplied orientation<select className={field} value={orientation ?? ''} onChange={e => setOrientation(e.target.value as AttachmentOption['orientation'] || null)}><option value="">Unspecified</option>{(concept === 'VERTICAL_RECTANGULAR' ? ['VERTICAL'] : concept === 'HORIZONTAL_RECTANGULAR' ? ['HORIZONTAL'] : ['VERTICAL', 'HORIZONTAL', 'UNSPECIFIED']).map(o => <option key={o} value={o}>{o.toLowerCase()}</option>)}</select></label>
        <label className="text-xs font-medium">Supplied surface<select className={field} value={surface ?? ''} onChange={e => setSurface(e.target.value as AttachmentOption['surface'] || null)}><option value="">Unspecified</option><option value="BUCCAL">Buccal</option><option value="LINGUAL">Lingual</option></select></label>
      </div>
      <label className="mt-3 flex items-start gap-2 text-xs"><input type="checkbox" className="mt-1" checked={placement} onChange={e => setPlacement(e.target.checked)} />Supply fictional tooth-local coordinates in mm.</label>
      {placement && <div className="mt-2 grid grid-cols-1 gap-3 sm:grid-cols-3">{['X', 'Y', 'Z'].map((label, i) => <label key={label} className="text-xs font-medium">Local {label} (mm)<input className={field} inputMode="decimal" value={coordinates[i]} onChange={e => setCoordinates(previous => previous.map((v, n) => n === i ? e.target.value : v))} /></label>)}</div>}
      {catalogError && <p role="alert" className="mt-2 text-xs text-danger">{catalogError}</p>}
      <button type="button" className="button button-secondary mt-3" onClick={applyCatalog}>Apply catalog specification</button>
      {options.attachment_options.map(o => <p key={o.concept} className="mt-2 flex flex-wrap items-center gap-2 text-xs">{CONCEPT_LABELS[o.concept]} · {o.geometry ? `${o.geometry.width_mm} × ${o.geometry.height_mm} × ${o.geometry.depth_mm} mm` : 'Geometry unspecified'}<button type="button" className="underline" onClick={() => change({ attachment_options: options.attachment_options.filter(item => item.concept !== o.concept) })}>Remove {CONCEPT_LABELS[o.concept]} specification</button></p>)}
      <label className="mt-3 flex items-start gap-2 text-xs"><input type="checkbox" className="mt-1" checked={options.catalog_policy === 'SUPPLIED_OPTIONS_ONLY'} onChange={e => change({ catalog_policy: e.target.checked ? 'SUPPLIED_OPTIONS_ONLY' : 'CONCEPTS_WITH_SUPPLIED_SPECS' })} />Limit categories to the supplied catalog entries.</label>
    </details>}
    {module === 'nano' && <div className="mt-4 space-y-3">
      <label className="block text-xs font-medium">Stage amount convention<select className={field} value={options.stage_value_basis} onChange={e => change({ stage_value_basis: e.target.value as PlanningOptions['stage_value_basis'] })}>
        <option value="UNSPECIFIED">Unspecified · totals cannot be compared</option><option value="INCREMENTS_MATCH_SOURCE_LABELS">Supplied increments match the source totals and labels</option>
      </select></label>
      <p className="text-xs text-muted">Enter actual supplied stage records. Amounts remain blank until entered; source totals are never divided or filled into stages.</p>
      {details.stages.map((s, i) => <fieldset key={i} className="min-w-0 rounded-lg border border-line p-3"><legend className="px-1 text-xs font-medium">Supplied stage {i + 1}</legend>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <label className="text-xs">Stage {i + 1} ID<input className={field} value={s.stage_id} onChange={e => renameStage(i, e.target.value)} /></label>
          <label className="text-xs">Stage {i + 1} order<input className={field} type="number" min="1" step="1" value={s.order} onChange={e => onChange(options, { ...details, stages: details.stages.map((v, n) => n === i ? { ...v, order: Number(e.target.value) } : v) })} /></label>
          <label className="text-xs">Stage {i + 1} phase<input className={field} placeholder="Unspecified" value={options.phases.find(p => p.stage_ids.includes(s.stage_id))?.phase_id ?? ''} onChange={e => assignPhase(s.stage_id, e.target.value)} /></label>
          <label className="text-xs">Stage {i + 1} duration (days)<input className={field} type="number" min="1" step="1" placeholder="Unspecified" value={s.duration_days ?? ''} onChange={e => onChange(options, { ...details, stages: details.stages.map((v, n) => n === i ? { ...v, duration_days: e.target.value ? Number(e.target.value) : null } : v) })} /></label>
        </div>
        <button type="button" className="mt-2 text-xs underline" onClick={() => onChange({ ...options, phases: options.phases.map(p => ({ ...p, stage_ids: p.stage_ids.filter(id => id !== s.stage_id) })).filter(p => p.stage_ids.length) }, { ...details, stages: details.stages.filter((_, n) => n !== i), allocations: details.allocations.filter(a => a.stage_id !== s.stage_id) })}>Remove stage {i + 1}</button>
      </fieldset>)}
      <button type="button" className="button button-secondary" disabled={details.stages.length >= 64} onClick={addStage}>Add supplied stage</button>
      {details.allocations.map((a, i) => <fieldset key={i} className="min-w-0 rounded-lg border border-line p-3"><legend className="px-1 text-xs font-medium">Movement record {i + 1}</legend>
        <label className="block text-xs">Movement {i + 1} stage<select className={field} value={a.stage_id} onChange={e => onChange(options, { ...details, allocations: details.allocations.map((v, n) => n === i ? { ...v, stage_id: e.target.value } : v) })}>{details.stages.map((s, n) => <option key={n} value={s.stage_id}>{s.stage_id || 'Unnamed stage'}</option>)}</select></label>
        <label className="mt-2 block text-xs">Movement {i + 1} source<select className={field} value={a.measurement_ref} onChange={e => { const m = cells.find(m => m.id === e.target.value); onChange(options, { ...details, allocations: details.allocations.map((v, n) => n === i ? { ...v, measurement_ref: m?.id ?? '', tooth_ref: m?.tooth_ref ?? '', unit: (m?.unit ?? null) as 'mm' | 'deg' | null } : v) }) }}><option value="">Choose a recorded source field</option>{cells.map(m => <option key={m.id} value={m.id}>{describe(m.id)}</option>)}</select></label>
        <label className="mt-2 block text-xs">Movement {i + 1} supplied amount {a.unit ? `(${a.unit})` : ''}<input className={field} inputMode="decimal" value={a.amount ?? ''} placeholder="Unknown until supplied" onChange={e => onChange(options, { ...details, allocations: details.allocations.map((v, n) => n === i ? { ...v, amount: e.target.value || null } : v) })} /></label>
        <button type="button" className="mt-2 text-xs underline" onClick={() => onChange(options, { ...details, allocations: details.allocations.filter((_, n) => n !== i) })}>Remove movement {i + 1}</button>
      </fieldset>)}
      <button type="button" className="button button-secondary" disabled={!details.stages.length || details.allocations.length >= 128} onClick={() => onChange(options, { ...details, allocations: [...details.allocations, { stage_id: details.stages[0].stage_id, tooth_ref: '', measurement_ref: '', amount: null, unit: null }] })}>Add supplied movement</button>
      <details className="border-t border-line pt-3"><summary className="cursor-pointer font-medium">Supplied support constraints</summary>
        <label className="mt-2 block text-xs">Support phase<select className={field} value={supportPhase} onChange={e => setSupportPhase(e.target.value)}><option value="">Choose a supplied phase</option>{options.phases.map(p => <option key={p.phase_id} value={p.phase_id}>{p.label}</option>)}</select></label>
        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">{[{ label: 'Support tooth tokens', value: supportTeeth, update: setSupportTeeth }, { label: 'Active tooth tokens', value: activeTeeth, update: setActiveTeeth }].map(group => <label key={group.label} className="text-xs">{group.label}<select multiple className={field} value={group.value} onChange={e => group.update(Array.from(e.target.selectedOptions, o => o.value))}>{parsed.teeth.map(t => <option key={t.id} value={t.id}>{t.raw_identifier.trim()}</option>)}</select></label>)}</div>
        <label className="mt-3 flex items-start gap-2 text-xs"><input type="checkbox" className="mt-1" checked={stationary} onChange={e => setStationary(e.target.checked)} />Explicitly assume the support group is stationary in this fictional phase.</label>
        <button type="button" className="button button-secondary mt-3" disabled={!supportPhase || !supportTeeth.length || !activeTeeth.length || !stationary || options.support_constraints.length >= 16} onClick={() => change({ support_constraints: [...options.support_constraints, { phase_id: supportPhase, support_tooth_refs: supportTeeth, active_tooth_refs: activeTeeth, assumption: 'STATIONARY_IN_FICTIONAL_SCENARIO' }] })}>Apply support constraint</button>
        {options.support_constraints.map((c, i) => <p key={i} className="mt-2 text-xs">{c.phase_id}: support {c.support_tooth_refs.map(t => teeth.get(t)).join(', ')}; active {c.active_tooth_refs.map(t => teeth.get(t)).join(', ')}. <button type="button" className="underline" onClick={() => change({ support_constraints: options.support_constraints.filter((_, n) => n !== i) })}>Remove constraint {i + 1}</button></p>)}
      </details>
    </div>}
  </details>
}
