// Full existing suite against the built bundle and fresh, owned audit servers.
import { defineConfig } from '@playwright/test'
import { resolve } from 'node:path'
import base from './playwright.config'

const backend = resolve(process.cwd(), '../backend')
const python = resolve(backend, process.platform === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python')

export default defineConfig({
  ...base,
  use: { ...base.use, baseURL: 'http://127.0.0.1:5179', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: [
    { command: `"${python}" -m uvicorn app.main:app --host 127.0.0.1 --port 8019 --no-access-log`, cwd: backend,
      env: { FINOVA_ENVIRONMENT: 'development', FINOVA_PLANNING_DEMO_ENABLED: 'true', FINOVA_ATTACHMENT_DEMO_ENABLED: 'true', FINOVA_SEQUENCER_DEMO_ENABLED: 'true', FINOVA_GROQ_SYNTHETIC_ENABLED: 'false', FINOVA_PARSER_GROQ_ENABLED: 'false' },
      url: 'http://127.0.0.1:8019/api/health', reuseExistingServer: false },
    { command: 'npx vite preview --config vite.audit.config.ts --host 127.0.0.1 --port 5179 --strictPort',
      url: 'http://127.0.0.1:5179', reuseExistingServer: false },
  ],
})
