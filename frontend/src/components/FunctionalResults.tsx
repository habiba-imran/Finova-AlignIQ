import type { InteractiveReport } from '../api/interactive'
import { CONCEPT_LABELS } from '../api/functional'
import { commentParagraphs } from '../reviewPresentation'

export default function FunctionalResults({ report }: { report: InteractiveReport }) {
  const plan = report.functional_plan, context = report.planning_context
  if (!plan || !context) return null
  const teeth = new Map(report.parsed.teeth.map(t => [t.id, t.raw_identifier.trim()]))
  const cells = new Map(report.parsed.measurements.map(m => [m.id, m]))
  const decisions = new Map(plan.decisions.map(d => [d.decision_id, d]))
  const facts = new Map(report.analytical_findings?.map(f => [f.finding_id, f.text]))
  const movement = (ref: string) => { const m = cells.get(ref)!; return `${m.recognized_label?.replaceAll('_', ' ') ?? m.raw_label}: ${m.signed_decimal ?? 'unknown'} ${m.unit ?? '(unit unknown)'}${m.raw_direction ? ` (${m.raw_direction}-labelled)` : ''}` }
  return <div className="mt-5 space-y-5">
    <aside className="rounded-lg border border-notice-line bg-notice/40 p-4 text-sm leading-6" aria-label="Fictional planning context">
      <strong>Explicit fictional scenario · no clinical authorization.</strong>
      <p>Scenario objectives, catalog geometry and stage records are supplied separately from the pasted TMT. Editing the source clears this context.</p>
      {!!context.objectives.length && <p>Fictional objectives: {context.objectives.map(o => o.toLowerCase().replaceAll('_', ' ')).join('; ')}.</p>}
    </aside>
    {report.module === 'micro' && <section aria-label="Illustrative attachment candidates">
      <h5 className="font-semibold">Tooth-wise attachment options</h5>
      <div className="movement-scroll mt-3" tabIndex={0} role="region" aria-label="Attachment candidate table">
        <table className="movement-table"><thead><tr><th>Tooth</th><th>Relevant movement</th><th>Illustrative attachment candidate</th><th>Alternative</th><th>Rationale</th></tr></thead><tbody>
          {plan.attachment_rows.map(row => { const d = decisions.get(row.decision_id)!; return <tr key={row.tooth_ref}>
            <th scope="row">{teeth.get(row.tooth_ref)}</th>
            <td><ul>{row.movement_refs.filter(ref => cells.get(ref)?.signed_decimal !== '0.00' || row.outcome === 'NO_ATTACHMENT').map(ref => <li key={ref}>{movement(ref)}</li>)}</ul></td>
            <td>{row.primary ? CONCEPT_LABELS[row.primary] : 'No supported candidate'}<p className="mt-1 text-xs text-muted">Illustration only</p></td>
            <td>{row.alternative ? CONCEPT_LABELS[row.alternative] : 'None supplied by the policy'}</td>
            <td><p>{d.rationale}</p><details className="mt-2 text-xs leading-6"><summary className="cursor-pointer font-medium">Tooth {teeth.get(row.tooth_ref)} details</summary>
              <div className="mt-2 space-y-2">{commentParagraphs(facts.get(d.finding_id)!).map((text, i) => <p key={i}>{text}</p>)}</div>
              <p>Illustrative policy {d.policy_id}, version {d.policy_version}. Source references: {d.measurement_refs.join(', ')}.</p>
            </details></td>
          </tr> })}
        </tbody></table>
      </div>
    </section>}
    {report.module === 'nano' && <section aria-label="Supplied sequencing plan">
      <h5 className="font-semibold">Ordered phases and movements</h5>
      {plan.stages.length ? <ol className="mt-3 space-y-3">{plan.stages.map(stage => <li key={stage.stage_id} className="comment-card">
        <h6 className="font-semibold">{context.phases.find(p => p.phase_id === stage.phase_id)?.label ?? 'Phase unknown'} · {stage.stage_id} · supplied order {stage.order}</h6>
        <p className="mt-1 text-sm">Teeth: {[...new Set(stage.movements.map(m => teeth.get(m.tooth_ref)))].join(', ') || 'No assignments supplied'}.</p>
        <details className="mt-2 text-sm leading-7"><summary className="cursor-pointer font-medium">Stage {stage.stage_id} movements and assumptions</summary><div className="mt-2 space-y-2">
          {stage.decision_ids.flatMap(id => commentParagraphs(facts.get(decisions.get(id)!.finding_id)!)).map((text, i) => <p key={i}>{text}</p>)}
          {!stage.movements.length && <p>Explicit stage-bound movement records are needed.</p>}
        </div></details>
      </li>)}</ol> : <p className="mt-2 text-sm">No supported stage plan. Explicit consistent stage data is required.</p>}
      {!!plan.allocation_checks.length && <details className="mt-4 text-sm"><summary className="cursor-pointer font-medium">Stage-to-total consistency</summary>
        <div className="movement-scroll mt-2"><table className="movement-table"><thead><tr><th>Tooth / field</th><th>Source total</th><th>Supplied stage sum</th><th>Check</th></tr></thead><tbody>{plan.allocation_checks.map(check => <tr key={check.measurement_ref}>
          <td>{teeth.get(cells.get(check.measurement_ref)!.tooth_ref)} · {cells.get(check.measurement_ref)!.recognized_label}</td><td>{check.source_total ?? 'Unknown'} {check.unit}</td><td>{check.allocated_total ?? 'Unknown'} {check.unit}</td><td>{check.status.toLowerCase().replaceAll('_', ' ')}</td>
        </tr>)}</tbody></table></div>
      </details>}
    </section>}
  </div>
}
