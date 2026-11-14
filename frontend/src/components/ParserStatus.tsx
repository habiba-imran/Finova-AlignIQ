import type { AutomaticParseResult } from '../api/parse'

const issueLabels: Record<string, string> = {
  EMPTY_INPUT: 'Add a table with headings and at least one tooth row.',
  UNSUPPORTED_LAYOUT: 'Table headings or row boundaries could not be recognized.',
  AMBIGUOUS_LAYOUT: 'More than one table layout is possible. Separate the tables and retry.',
  ROW_ALIGNMENT_UNRESOLVED: 'Some rows do not align with the headings.',
  NO_DATA_ROWS: 'No tooth rows could be read beneath the headings.',
  INVALID_NUMBER: 'Some values are not valid plain numbers.',
  AMBIGUOUS_VALUE_SUFFIX: 'Some values have an unclear unit or direction.',
  DECIMAL_CONVENTION_REQUIRED: 'Check the decimal convention in Advanced Table Settings.',
  UNIT_CONFLICT: 'Some cell units conflict with their column headings.',
  CONFLICTING_FIELD: 'Repeated movement cells contain conflicting values.',
  DUPLICATE_FIELD: 'Repeated movement cells need clarification.',
  LINE_LIMIT: 'The table contains too many lines. Split it into smaller tables.',
  GRID_LIMIT: 'The table contains too many columns or cells. Split it into smaller tables.',
  CELL_LIMIT: 'Some cells are too long. Check the original text.',
  UNSUPPORTED_LABEL: 'Some movement headings are unrecognized.',
  UNSUPPORTED_HEADER_UNIT: 'Some column units are unrecognized.',
  UNIT_REQUIRED: 'Some movement units are missing.',
  SHORT_DELIMITED_ROW: 'Some rows have missing trailing cells.',
  UNRECOGNIZED_PREAMBLE: 'Some text outside the table was not read.',
}

export default function ParserStatus({ result, demonstration = false }: { result: AutomaticParseResult; demonstration?: boolean }) {
  const classification = result.pipeline.quality?.classification
  const status = classification === 'NOT_TMT' ? 'Unsupported input · not a TMT'
    : classification === 'AMBIGUOUS_STRUCTURE' ? 'Needs clarification'
      : result.status === 'INVALID' ? 'Table needs correction'
        : result.status === 'UNSUPPORTED' ? 'Unsupported input'
      : !result.measurements.length ? 'Unsupported input'
        : result.status === 'PARTIAL' ? 'Partially parsed' : 'Table ready'
  const errors = result.issues.filter(i => i.severity === 'ERROR')
  const groups = [...new Set(result.issues.filter(i => i.severity !== 'INFO').map(i => i.code))]
    .filter(code => issueLabels[code] || errors.some(i => i.code === code))
  const errorCodes = new Set(errors.map(i => i.code))
  const visibleGroups = [...groups.filter(code => errorCodes.has(code)), ...groups.filter(code => !errorCodes.has(code)).slice(0, 2)]
  return <section aria-label="Automatic detection and clarification" className="panel motion-enter">
    <div className="panel-heading">
      <h3 className="panel-title">{status}</h3>
      <span className="report-badge report-badge-notice">{demonstration ? 'Verified synthetic demonstration only' : 'Unverified input'}</span>
    </div>
    <div className="p-5 sm:p-6">
      <p className="text-sm leading-6 text-muted">{demonstration ? 'Only the fixed fictional example has checked demonstration evidence. This does not verify patient data or vendor compatibility.' : 'Reading the table does not verify tooth identity, source conventions or clinical eligibility.'}</p>
      <dl aria-label="Parse summary" className="summary-grid mt-4" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))' }}>
        {[['Tooth rows', result.teeth.length], ['Movement positions', result.measurements.length], ['Missing values', result.coverage.missing], ['Explicit zeros', result.coverage.explicit_zero]].map(([label, count]) => <div key={label} className="summary-metric"><dt className="summary-label">{label}</dt><dd className="summary-value">{count}</dd></div>)}
      </dl>
      {!!groups.length && <section aria-label={errors.length ? 'Blocking parse issues' : 'Table clarification'} className="mt-4 rounded-lg border border-notice-line bg-notice p-4 text-sm leading-6 text-notice-ink">
        <p className="font-semibold">{errors.length ? 'Some table content could not be read reliably.' : 'Check the marked cells before review.'}</p>
        <ul className="mt-2 list-disc space-y-1 pl-5">{visibleGroups.map(code => <li key={code}>{issueLabels[code] ?? 'Some table content needs clarification. Check the original text and marked cells.'}</li>)}</ul>
        {groups.length > visibleGroups.length && <p className="mt-2 text-xs">Additional warnings affect this table. Full details remain in complete review exports.</p>}
      </section>}
    </div>
  </section>
}
