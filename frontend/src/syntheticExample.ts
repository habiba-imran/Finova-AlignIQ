import example from '../../examples/functional-all-in-one.json'
import type { DemoModule } from './api/interactive'
import type { FunctionalScenario } from './api/functional'

// One explicitly loaded fictional case, shared across all three review modules.
// Authored targets, catalog and stage records remain separate from the source TMT.
export const SYNTHETIC_EXAMPLE = example.raw_text
export const SYNTHETIC_SCENARIOS = example.modules as Record<DemoModule, FunctionalScenario>
