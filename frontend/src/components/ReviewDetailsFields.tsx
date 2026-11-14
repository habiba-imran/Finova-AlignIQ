import type { ReactNode } from 'react'
import type { ParseResult } from '../api/parse'
import type { AnchorageNote, AttachmentDetail, DemoModule, ReviewDetails, SuppliedAllocation, SuppliedStage } from '../api/interactive'

const control = 'mt-1 block w-full min-w-0 rounded-lg border border-field bg-white px-3 py-2.5 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/15'
function Field({ label, value, onChange, numeric = false, maxLength = 80 }: { label: string; value: string | number | null; onChange: (value: string) => void; numeric?: boolean; maxLength?: number }) {
  return <label className="block text-xs font-medium text-muted">{label}<input aria-label={label} className={control} value={value ?? ''} onChange={e => onChange(e.target.value)} inputMode={numeric ? 'decimal' : 'text'} maxLength={maxLength} /></label>
}
function Select({ label, value, onChange, children }: { label: string; value: string; onChange: (value: string) => void; children: ReactNode }) {
  return <label className="block text-xs font-medium text-muted">{label}<select aria-label={label} className={control} value={value} onChange={e => onChange(e.target.value)}>{children}</select></label>
}

export default function ReviewDetailsFields({ module, parsed, value, onChange, disabled }: { module: DemoModule; parsed: ParseResult; value: ReviewDetails; onChange: (value: ReviewDetails) => void; disabled: boolean }) {
  if (module === 'macro') return null
  const teeth = <><option value="">Choose tooth row</option>{parsed.teeth.map(tooth => <option key={tooth.id} value={tooth.id}>{tooth.raw_identifier.trim()}</option>)}</>
  const attachment = (i: number, patch: Partial<AttachmentDetail>) => onChange({ ...value, attachments: value.attachments.map((row, j) => j === i ? { ...row, ...patch } : row) })
  const stage = (i: number, patch: Partial<SuppliedStage>) => onChange({ ...value, stages: value.stages.map((row, j) => j === i ? { ...row, ...patch } : row) })
  const allocation = (i: number, patch: Partial<SuppliedAllocation>) => onChange({ ...value, allocations: value.allocations.map((row, j) => j === i ? { ...row, ...patch } : row) })
  const anchorage = (i: number, patch: Partial<AnchorageNote>) => onChange({ ...value, anchorage_notes: value.anchorage_notes.map((row, j) => j === i ? { ...row, ...patch } : row) })
  return <details className="mt-4 rounded-xl border border-line bg-canvas p-4" aria-label="Supplied review details">
    <summary className="cursor-pointer text-sm font-semibold">{module === 'micro' ? 'Add supplied attachment details (optional)' : 'Add supplied sequencing details (optional)'}</summary>
    <p className="mt-2 text-xs leading-6 text-muted">Enter information already supplied for this synthetic plan. Blank information stays unknown. These entries are reported as supplied and unverified.</p>
    <fieldset disabled={disabled} className="mt-4 min-w-0 space-y-4">
      <legend className="sr-only">{module === 'micro' ? 'Attachment details' : 'Sequencing details'}</legend>
      {module === 'micro' ? <>
        {value.attachments.map((row, i) => <div key={i} className="rounded-lg border border-line bg-white p-4">
          <div className="mb-3 flex items-center justify-between gap-3"><h4 className="text-sm font-semibold">Attachment record {i + 1}</h4><button type="button" className="text-xs text-muted underline" onClick={() => onChange({ ...value, attachments: value.attachments.filter((_, j) => j !== i) })}>Remove attachment {i + 1}</button></div>
          <div className="grid min-w-0 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Select label={`Attachment ${i + 1} tooth`} value={row.tooth_ref} onChange={tooth_ref => attachment(i, { tooth_ref })}>{teeth}</Select>
            <Select label={`Attachment ${i + 1} choice`} value={row.choice} onChange={choice => attachment(i, { choice: choice as AttachmentDetail['choice'], ...(choice !== 'ATTACHMENT' ? { design: null, width_mm: null, height_mm: null, depth_mm: null, surface: null, orientation: null } : {}) })}><option value="UNKNOWN">Not supplied</option><option value="ATTACHMENT">Supplied attachment choice</option><option value="NO_ATTACHMENT">Supplied no-attachment choice</option></Select>
            {row.choice === 'ATTACHMENT' && <>
              <Field label={`Attachment ${i + 1} design`} value={row.design} onChange={design => attachment(i, { design: design || null })} />
              {(['width_mm', 'height_mm', 'depth_mm'] as const).map(key => <Field key={key} label={`Attachment ${i + 1} ${key.replace('_mm', '')} (mm)`} value={row[key]} numeric onChange={number => attachment(i, { [key]: number || null })} maxLength={24} />)}
              <Field label={`Attachment ${i + 1} surface`} value={row.surface} onChange={surface => attachment(i, { surface: surface || null })} />
              <Field label={`Attachment ${i + 1} orientation`} value={row.orientation} onChange={orientation => attachment(i, { orientation: orientation || null })} />
            </>}
          </div>
        </div>)}
        <button type="button" className="button button-secondary" disabled={value.attachments.length >= 32} onClick={() => onChange({ ...value, attachments: [...value.attachments, { tooth_ref: '', choice: 'UNKNOWN', design: null, width_mm: null, height_mm: null, depth_mm: null, surface: null, orientation: null }] })}>Add attachment record</button>
      </> : <>
        <h4 className="text-sm font-semibold">Stages</h4>
        {value.stages.map((row, i) => <div key={i} className="rounded-lg border border-line bg-white p-4">
          <div className="mb-3 flex items-center justify-between gap-3"><h5 className="text-sm font-medium">Stage record {i + 1}</h5><button type="button" className="text-xs text-muted underline" onClick={() => onChange({ ...value, stages: value.stages.filter((_, j) => j !== i) })}>Remove stage {i + 1}</button></div>
          <div className="grid gap-3 sm:grid-cols-3">
            <Field label={`Stage ${i + 1} ID`} value={row.stage_id} onChange={stage_id => stage(i, { stage_id })} maxLength={40} />
            <Field label={`Stage ${i + 1} order`} value={row.order || null} numeric onChange={order => stage(i, { order: Number(order) })} />
            <Field label={`Stage ${i + 1} duration (days)`} value={row.duration_days} numeric onChange={duration => stage(i, { duration_days: duration ? Number(duration) : null })} />
          </div>
        </div>)}
        <button type="button" className="button button-secondary" disabled={value.stages.length >= 64} onClick={() => onChange({ ...value, stages: [...value.stages, { stage_id: '', order: 0, duration_days: null }] })}>Add stage record</button>
        <h4 className="pt-2 text-sm font-semibold">Movement allocations</h4>
        <p className="text-xs leading-6 text-muted">A source movement reference does not automatically assign its value to a stage. Enter a stage amount only when supplied.</p>
        {value.allocations.map((row, i) => <div key={i} className="rounded-lg border border-line bg-white p-4">
          <div className="mb-3 flex items-center justify-between gap-3"><h5 className="text-sm font-medium">Allocation {i + 1}</h5><button type="button" className="text-xs text-muted underline" onClick={() => onChange({ ...value, allocations: value.allocations.filter((_, j) => j !== i) })}>Remove allocation {i + 1}</button></div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Select label={`Allocation ${i + 1} stage`} value={row.stage_id} onChange={stage_id => allocation(i, { stage_id })}><option value="">Choose stage</option>{value.stages.filter(s => s.stage_id).map(s => <option key={s.stage_id} value={s.stage_id}>{s.stage_id}</option>)}</Select>
            <Select label={`Allocation ${i + 1} tooth`} value={row.tooth_ref} onChange={tooth_ref => allocation(i, { tooth_ref, measurement_ref: '', unit: null })}>{teeth}</Select>
            <Select label={`Allocation ${i + 1} movement`} value={row.measurement_ref} onChange={measurement_ref => allocation(i, { measurement_ref, unit: parsed.measurements.find(m => m.id === measurement_ref)?.unit as SuppliedAllocation['unit'] ?? null })}><option value="">Choose source movement</option>{parsed.measurements.filter(m => m.tooth_ref === row.tooth_ref).map(m => <option key={m.id} value={m.id}>{m.raw_label.trim()}</option>)}</Select>
            <Field label={`Allocation ${i + 1} stage amount`} value={row.amount} numeric onChange={amount => allocation(i, { amount: amount || null })} maxLength={24} />
            <Select label={`Allocation ${i + 1} unit`} value={row.unit ?? ''} onChange={unit => allocation(i, { unit: unit as SuppliedAllocation['unit'] || null })}><option value="">Not supplied</option><option value="mm">mm</option><option value="deg">deg</option></Select>
          </div>
        </div>)}
        <button type="button" className="button button-secondary" disabled={value.allocations.length >= 128} onClick={() => onChange({ ...value, allocations: [...value.allocations, { stage_id: '', tooth_ref: '', measurement_ref: '', amount: null, unit: null }] })}>Add movement allocation</button>
        <h4 className="pt-2 text-sm font-semibold">Anchorage notes</h4>
        {value.anchorage_notes.map((row, i) => <div key={i} className="rounded-lg border border-line bg-white p-4">
          <div className="mb-3 flex justify-between gap-3"><h5 className="text-sm font-medium">Anchorage note {i + 1}</h5><button type="button" className="text-xs text-muted underline" onClick={() => onChange({ ...value, anchorage_notes: value.anchorage_notes.filter((_, j) => j !== i) })}>Remove anchorage note {i + 1}</button></div>
          <div className="grid gap-3 sm:grid-cols-2"><Select label={`Anchorage ${i + 1} scope`} value={row.tooth_ref ?? ''} onChange={tooth_ref => anchorage(i, { tooth_ref: tooth_ref || null })}><option value="">Overall plan</option>{parsed.teeth.map(tooth => <option key={tooth.id} value={tooth.id}>{tooth.raw_identifier.trim()}</option>)}</Select><Field label={`Anchorage ${i + 1} supplied note`} value={row.note} onChange={note => anchorage(i, { note })} maxLength={240} /></div>
        </div>)}
        <button type="button" className="button button-secondary" disabled={value.anchorage_notes.length >= 32} onClick={() => onChange({ ...value, anchorage_notes: [...value.anchorage_notes, { tooth_ref: null, note: '' }] })}>Add anchorage note</button>
      </>}
    </fieldset>
  </details>
}
