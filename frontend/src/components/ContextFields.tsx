import { Check, Info, RotateCcw, SlidersHorizontal, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { EMPTY_CONTEXT } from '../api/parse'
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

const labels: Record<keyof typeof options, string> = {
  notation: 'Tooth notation claim',
  dentition: 'Dentition claim',
  arch: 'Arch claim',
  plan_mode: 'Plan mode claim',
  reference_basis: 'Measurement basis claim',
  scope: 'Movement scope claim',
  decimal_separator: 'Decimal convention',
}

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

const toOptions = (values: readonly string[]) =>
  values.map(value => ({ value, label: optionLabels[value] ?? value.replaceAll('_', ' ') }))

export default function ContextFields({
  value,
  onChange,
}: {
  value: ContextClaims
  onChange: (context: ContextClaims) => void
}) {
  const [isOpen, setIsOpen] = useState(false)
  const windowRef = useRef<HTMLDivElement>(null)

  // Close on Escape key press
  useEffect(() => {
    if (!isOpen) return
    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen])

  // Count configured custom fields
  const customCount = [
    value.notation !== 'UNKNOWN',
    value.dentition !== 'UNKNOWN',
    value.arch !== 'UNKNOWN',
    value.plan_mode !== 'UNKNOWN',
    value.reference_basis !== 'UNKNOWN',
    value.scope !== 'UNKNOWN',
    value.decimal_separator !== 'DOT',
    !!value.source_version,
    value.stage_index !== null,
    !!value.coordinate_frame,
  ].filter(Boolean).length

  const modalMarkup = (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="advanced-settings-title"
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 transition-all duration-200 ${isOpen ? 'visible opacity-100' : 'invisible pointer-events-none opacity-0'
        }`}
      onClick={e => {
        if (e.target === e.currentTarget) setIsOpen(false)
      }}
    >
      {/* Blurred backdrop covering the rest of the UI */}
      <div
        aria-hidden="true"
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-md transition-opacity"
        onClick={() => setIsOpen(false)}
      />

      {/* Settings Window */}
      <div
        ref={windowRef}
        className="relative z-10 flex w-full max-w-2xl flex-col max-h-[88vh] overflow-hidden rounded-2xl border border-line bg-white shadow-2xl transition-all duration-200"
      >
        {/* Window Header */}
        <div className="flex shrink-0 items-center justify-between border-b border-line bg-white px-5 py-4 sm:px-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-brand/20 bg-brand-soft text-brand">
              <SlidersHorizontal size={18} strokeWidth={2} />
            </span>
            <div>
              <h3 id="advanced-settings-title" className="text-base font-semibold text-ink sm:text-lg">
                Advanced Table Settings
              </h3>
              <p className="text-xs text-muted">Inputs are automatically saved as you enter them.</p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setIsOpen(false)}
            aria-label="Close window"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-line bg-canvas text-muted transition-colors hover:bg-line/40 hover:text-ink"
          >
            <X size={17} />
          </button>
        </div>

        {/* Scrollable Window Body */}
        <div className="flex-1 overflow-y-auto p-5 sm:p-6 space-y-5">
          <div className="rounded-xl border border-notice-line bg-notice/40 p-4 text-xs leading-5 text-notice-ink">
            <p className="font-semibold text-ink">Context claims (Optional)</p>
            <p className="mt-1">
              Add only the context you know with certainty. Leave any uncertain fields as <strong>Unknown</strong>.
              These claims cannot authorize unverified vendor semantics.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">Movement & Grid Conventions</h4>
            <div className="mt-3 grid gap-x-4 gap-y-4 sm:grid-cols-2">
              {Object.entries(options).map(([key, values]) => (
                <div key={key} className="min-w-0">
                  <label htmlFor={`context-${key}`} className="mb-1.5 block text-xs font-medium text-ink">
                    {labels[key as keyof typeof options]}
                  </label>
                  <ModernSelect
                    id={`context-${key}`}
                    value={value[key as keyof typeof options]}
                    options={toOptions(values)}
                    ariaLabel={labels[key as keyof typeof options]}
                    onChange={next => onChange({ ...value, [key]: next })}
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="border-t border-line pt-4">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">Source Claims & Identifiers</h4>
            <div className="mt-3 grid gap-4 sm:grid-cols-2">
              <div className="min-w-0">
                <label htmlFor="source-version" className="mb-1.5 block text-xs font-medium text-ink">
                  Source version claim
                </label>
                <input
                  id="source-version"
                  value={value.source_version ?? ''}
                  maxLength={64}
                  placeholder="e.g. ClinCheck 6.0"
                  onChange={event => onChange({ ...value, source_version: event.target.value || null })}
                  className="context-control"
                  autoComplete="off"
                />
              </div>

              <div className="min-w-0">
                <label htmlFor="stage-index" className="mb-1.5 block text-xs font-medium text-ink">
                  Stage index claim
                </label>
                <input
                  id="stage-index"
                  type="number"
                  min="0"
                  max="2147483647"
                  step="1"
                  placeholder="e.g. 12"
                  value={value.stage_index ?? ''}
                  onChange={event =>
                    onChange({
                      ...value,
                      stage_index: event.target.value === '' ? null : Number(event.target.value),
                    })
                  }
                  className="context-control"
                />
              </div>

              <div className="min-w-0 sm:col-span-2">
                <label htmlFor="coordinate-frame" className="mb-1.5 block text-xs font-medium text-ink">
                  Coordinate frame claim
                </label>
                <input
                  id="coordinate-frame"
                  value={value.coordinate_frame ?? ''}
                  maxLength={128}
                  placeholder="e.g. occlusal plane, +X buccal"
                  onChange={event => onChange({ ...value, coordinate_frame: event.target.value || null })}
                  className="context-control"
                  autoComplete="off"
                />
              </div>
            </div>
          </div>

          <p className="flex items-start gap-2 text-[11px] leading-5 text-muted">
            <Info size={14} className="mt-0.5 shrink-0 text-muted" aria-hidden="true" />
            <span>
              These entries are unverified metadata. They do not verify a manufacturer source or enable canonical
              tooth numbering, axis, or direction conversions.
            </span>
          </p>
        </div>

        {/* Window Footer */}
        <div className="flex shrink-0 flex-wrap items-center justify-between gap-3 border-t border-line bg-canvas/40 px-5 py-3.5 sm:px-6">
          <div className="flex items-center gap-2 text-xs text-brand font-medium">
            <Check size={15} strokeWidth={2.5} />
            <span>Inputs saved automatically</span>
          </div>
          <div className="flex items-center gap-2">
            {customCount > 0 && (
              <button
                type="button"
                onClick={() => onChange({ ...EMPTY_CONTEXT })}
                className="button button-clear text-xs h-9 px-3 text-muted hover:text-ink"
              >
                <RotateCcw size={13} />
                Reset defaults
              </button>
            )}
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="button button-primary text-xs h-9 px-5"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <div className="mt-5">
      {/* Trigger Button that opens the Window */}
      <button
        type="button"
        onClick={() => setIsOpen(true)}
        aria-haspopup="dialog"
        aria-expanded={isOpen}
        aria-label={customCount > 0 ? `Open Advanced Table Settings (${customCount} set)` : 'Open Advanced Table Settings'}
        className="flex w-full items-center justify-between rounded-xl border border-line bg-white p-3.5 shadow-panel transition-all hover:border-brand/40 hover:bg-canvas/40 sm:p-4 text-left"
      >
        <span className="flex min-w-0 items-center gap-3">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-brand/20 bg-brand-soft text-brand">
            <SlidersHorizontal size={16} strokeWidth={2} />
          </span>
          <span className="min-w-0">
            <span className="block text-[13px] font-semibold text-ink sm:text-sm">
              Advanced Table Settings <span className="font-normal text-muted">(Optional)</span>
            </span>
            <span className="mt-0.5 block text-[11px] leading-5 text-muted sm:text-xs">
              {customCount > 0
                ? `${customCount} custom claim${customCount === 1 ? '' : 's'} configured · click to view or edit`
                : 'Add context you know (notation, arch, basis, decimal convention)'}
            </span>
          </span>
        </span>
        {customCount > 0 && (
          <span className="shrink-0 rounded-md border border-brand/25 bg-brand-soft px-2.5 py-1 text-xs font-semibold text-brand">
            {customCount} set
          </span>
        )}
      </button>

      {/* Render the modal window in document.body via Portal */}
      {typeof document !== 'undefined' ? createPortal(modalMarkup, document.body) : modalMarkup}
    </div>
  )
}
