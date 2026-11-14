import type { ReactNode, Ref } from 'react'

type Tone = 'default' | 'notice' | 'danger' | 'brand'

const toneClasses: Record<Tone, string> = {
  default: '',
  notice: 'report-badge-notice',
  danger: 'report-badge-danger',
  brand: 'report-badge-brand',
}

export function ReportHeader({ eyebrow, title, headingRef, draftStatus, badges = [], summary, children }: {
  eyebrow: string
  title: string
  headingRef?: Ref<HTMLHeadingElement>
  draftStatus: string
  badges?: { label: string; tone?: Tone }[]
  summary?: ReactNode
  children?: ReactNode
}) {
  return <header className="report-header">
    <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
      <div className="min-w-0">
        <p className="report-eyebrow">{eyebrow}</p>
        <h3 ref={headingRef} tabIndex={-1} className="report-title">{title}</h3>
      </div>
      <div className="flex flex-wrap items-center gap-2 lg:justify-end">
        <span className="report-badge report-badge-draft">DRAFT · Prototype</span>
        {badges.map(badge => <span key={badge.label} className={`report-badge ${toneClasses[badge.tone ?? 'default']}`}>{badge.label}</span>)}
      </div>
    </div>
    <p className="report-status-line">{draftStatus}</p>
    {summary && <div className="mt-4">{summary}</div>}
    {children}
  </header>
}

export function SummaryGrid({ label, children }: { label: string; children: ReactNode }) {
  return <dl aria-label={label} className="summary-grid">{children}</dl>
}

export function SummaryMetric({ label, value, detail, tone = 'default' }: {
  label: string
  value: ReactNode
  detail?: ReactNode
  tone?: Tone
}) {
  return <div className={`summary-metric ${tone === 'notice' ? 'summary-metric-notice' : tone === 'danger' ? 'summary-metric-danger' : ''}`}>
    <dt className="summary-label">{label}</dt>
    <dd className="summary-value">{value}</dd>
    {detail && <dd className="summary-detail">{detail}</dd>}
  </div>
}

export function ReportSection({ title, label, description, tone = 'default', className = '', actions, children }: {
  title: string
  label?: string
  description?: ReactNode
  tone?: Tone
  className?: string
  actions?: ReactNode
  children: ReactNode
}) {
  return <section aria-label={label ?? title} className={`report-section ${tone === 'notice' ? 'report-section-notice' : tone === 'danger' ? 'report-section-danger' : ''} ${className}`}>
    <div className="report-section-heading">
      <div className="min-w-0">
        <h4 className="report-section-title">{title}</h4>
        {description && <p className="report-section-note">{description}</p>}
      </div>
      {actions && <div className="flex shrink-0 flex-wrap items-center gap-2">{actions}</div>}
    </div>
    <div className="mt-3 min-w-0">{children}</div>
  </section>
}

export function EvidenceDisclosure({ summary, children, className = '' }: {
  summary: string
  children: ReactNode
  className?: string
}) {
  return <details className={`evidence-disclosure ${className}`}>
    <summary>{summary}</summary>
    <div className="evidence-content">{children}</div>
  </details>
}

export function ExportBar({ label, title = 'Export', description, notice, children }: {
  label: string
  title?: string
  description?: ReactNode
  notice?: ReactNode
  children: ReactNode
}) {
  return <section aria-label={label} className="export-bar">
    <div className="export-bar-heading">
      <span className="section-number">04</span>
      <h4 className="export-bar-title">{title}</h4>
      {description && <p className="export-bar-note">{description}</p>}
    </div>
    <div className="export-bar-actions">{children}</div>
    {notice && <div role="status" className="motion-status mt-3 text-sm leading-6 text-brand">{notice}</div>}
  </section>
}
