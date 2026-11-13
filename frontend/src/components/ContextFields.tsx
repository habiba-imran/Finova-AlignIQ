import type { ContextClaims } from '../api/parse'

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
const humanize = (value: string) => value.replaceAll('_', ' ')

export default function ContextFields({ value, onChange }: { value: ContextClaims; onChange: (context: ContextClaims) => void }) {
  return <details className="mt-5 rounded-lg border border-line p-4">
    <summary className="cursor-pointer text-sm font-medium">Context claims <span className="font-normal text-muted">(optional, unverified)</span></summary>
    <p className="my-3 text-xs leading-5 text-muted">Supply only what you know. These claims cannot verify a source or enable canonical tooth/axis/direction conversion.</p>
    <div className="grid gap-3 sm:grid-cols-2">
      {Object.entries(options).map(([key, values]) => <div key={key}>
        <label htmlFor={`context-${key}`} className="mb-1.5 block text-xs font-medium">{labels[key as keyof typeof options]}</label>
        <select id={`context-${key}`} value={value[key as keyof typeof options]} onChange={event => onChange({ ...value, [key]: event.target.value })} className="context-control">
          {values.map(option => <option key={option} value={option}>{humanize(option)}</option>)}
        </select>
      </div>)}
      <div><label htmlFor="source-version" className="mb-1.5 block text-xs font-medium">Source version claim</label><input id="source-version" value={value.source_version ?? ''} maxLength={64} onChange={event => onChange({ ...value, source_version: event.target.value || null })} className="context-control" autoComplete="off" /></div>
      <div><label htmlFor="stage-index" className="mb-1.5 block text-xs font-medium">Stage index claim</label><input id="stage-index" type="number" min="0" max="2147483647" step="1" value={value.stage_index ?? ''} onChange={event => onChange({ ...value, stage_index: event.target.value === '' ? null : Number(event.target.value) })} className="context-control" /></div>
      <div><label htmlFor="coordinate-frame" className="mb-1.5 block text-xs font-medium">Coordinate frame claim</label><input id="coordinate-frame" value={value.coordinate_frame ?? ''} maxLength={128} onChange={event => onChange({ ...value, coordinate_frame: event.target.value || null })} className="context-control" autoComplete="off" /></div>
    </div>
  </details>
}
