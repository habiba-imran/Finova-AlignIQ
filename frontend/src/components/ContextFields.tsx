import { ChevronDown, Info, SlidersHorizontal } from 'lucide-react'
import type { ContextClaims } from '../api/parse'
import ModernSelect from './ModernSelect'

const options = {
  notation: ['UNKNOWN', 'FDI', 'UNIVERSAL', 'PALMER'],
  dentition: ['UNKNOWN', 'PERMANENT', 'PRIMARY', 'MIXED'],
  arch: ['UNKNOWN', 'UPPER', 'LOWER', 'BOTH'],
  plan_mode: ['UNKNOWN', 'ALIGN_FINAL', 'DOCTOR_FINAL', 'COMPARISON'],
  reference_basis: ['UNKNOWN', 'CROWN_CENTER', 'VIRTUAL_ROOT_APEX', 'CUSP_TIP'],
  scope: ['UNKNOWN', 'TOTAL', 'CUMULATIVE', 'INCREMENTAL'],
  decimal_separator: ['DOT', 'COMMA'],
} as const

const labels = { notation: 'Tooth notation claim', dentition: 'Dentition claim', arch: 'Arch claim', plan_mode: 'Plan mode claim', reference_basis: 'Measurement basis claim', scope: 'Movement scope claim', decimal_separator: 'Decimal convention' }

const optionLabels: Record<string, string> = {
  UNKNOWN: 'Unknown',
  FDI: 'FDI',
  UNIVERSAL: 'Universal',
  PALMER: 'Palmer',
  PERMANENT: 'Permanent',
  PRIMARY: 'Primary',
  MIXED: 'Mixed',
  UPPER: 'Upper',
  LOWER: 'Lower',
  BOTH: 'Both',
  ALIGN_FINAL: 'Align final',
  DOCTOR_FINAL: 'Doctor final',
  COMPARISON: 'Comparison',
  CROWN_CENTER: 'Crown center',
  VIRTUAL_ROOT_APEX: 'Virtual root apex',
  CUSP_TIP: 'Cusp tip',
  TOTAL: 'Total',
  CUMULATIVE: 'Cumulative',
  INCREMENTAL: 'Incremental',
  DOT: 'Dot (1.25)',
  COMMA: 'Comma (1,25)',
}

const toOptions = (values: readonly string[]) => values.map(value => ({ value, label: optionLabels[value] ?? value.replaceAll('_', ' ') }))

export default function ContextFields({ value, onChange }: { value: ContextClaims; onChange: (context: ContextClaims) => void }) {
  return <details className="group mt-5 overflow-hidden rounded-xl border border-line bg-white">
    <summary aria-label="Advanced Table Settings (Optional)" aria-describedby="advanced-table-settings-hint" className="flex cursor-pointer list-none items-center justify-between gap-3 px-4 py-3.5 transition-colors hover:bg-canvas/60 [&::-webkit-details-marker]:hidden">
      <span className="flex min-w-0 items-center gap-3">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-brand/20 bg-brand-soft text-brand" aria-hidden="true">
          <SlidersHorizontal size={16} strokeWidth={2} />
        </span>
        <span className="min-w-0">
          <span className="block text-[13px] font-semibold sm:text-sm">Advanced Table Settings <span className="font-normal text-muted">(Optional)</span></span>
          <span id="advanced-table-settings-hint" className="mt-0.5 block text-[11px] leading-5 text-muted sm:text-xs">Add only the context you know. Leave uncertain fields as Unknown.</span>
        </span>
      </span>
      <ChevronDown size={16} strokeWidth={2} className="modern-select-chevron shrink-0 text-muted group-open:rotate-180" aria-hidden="true" />
    </summary>
    <div className="border-t border-line bg-canvas/30 p-4 sm:p-5">
      <div className="grid gap-x-4 gap-y-4 sm:grid-cols-2">
        {Object.entries(options).map(([key, values]) => <div key={key} className="min-w-0">
          <label htmlFor={`context-${key}`} className="mb-1.5 block text-xs font-medium">{labels[key as keyof typeof options]}</label>
          <ModernSelect id={`context-${key}`} value={value[key as keyof typeof options]} options={toOptions(values)} ariaLabel={labels[key as keyof typeof options]} onChange={next => onChange({ ...value, [key]: next })} />
        </div>)}
      </div>
      <div className="mt-5 grid gap-4 border-t border-line pt-5 sm:grid-cols-2">
        <div className="min-w-0"><label htmlFor="source-version" className="mb-1.5 block text-xs font-medium">Source version claim</label><input id="source-version" value={value.source_version ?? ''} maxLength={64} placeholder="e.g. ClinCheck 6.0" onChange={event => onChange({ ...value, source_version: event.target.value || null })} className="context-control" autoComplete="off" /></div>
        <div className="min-w-0"><label htmlFor="stage-index" className="mb-1.5 block text-xs font-medium">Stage index claim</label><input id="stage-index" type="number" min="0" max="2147483647" step="1" placeholder="e.g. 12" value={value.stage_index ?? ''} onChange={event => onChange({ ...value, stage_index: event.target.value === '' ? null : Number(event.target.value) })} className="context-control" /></div>
        <div className="min-w-0 sm:col-span-2"><label htmlFor="coordinate-frame" className="mb-1.5 block text-xs font-medium">Coordinate frame claim</label><input id="coordinate-frame" value={value.coordinate_frame ?? ''} maxLength={128} placeholder="e.g. occlusal plane, +X buccal" onChange={event => onChange({ ...value, coordinate_frame: event.target.value || null })} className="context-control" autoComplete="off" /></div>
      </div>
      <p className="mt-4 flex items-start gap-2 text-[11px] leading-5 text-muted">
        <Info size={13} className="mt-0.5 shrink-0" aria-hidden="true" />
        <span>These are unverified claims. They cannot verify a source or enable canonical tooth, axis, or direction conversion.</span>
      </p>
    </div>
  </details>
}
