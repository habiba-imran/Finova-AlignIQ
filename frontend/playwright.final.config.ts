// Final acceptance extends the full production-bundle suite to all five requested widths.
import { defineConfig } from '@playwright/test'
import audit from './playwright.audit.config'

export default defineConfig({
  ...audit,
  projects: [
    ...audit.projects!,
    { name: 'compact', use: { viewport: { width: 672, height: 1000 } } },
  ],
})
