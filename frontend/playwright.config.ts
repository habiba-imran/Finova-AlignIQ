import { defineConfig } from '@playwright/test'
import { resolve } from 'node:path'

const backend = resolve(process.cwd(), '../backend')
const python = resolve(backend, process.platform === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python')

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  timeout: 30_000,
  use: { baseURL: 'http://127.0.0.1:5173', browserName: 'chromium', reducedMotion: 'reduce' },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1440, height: 1000 } } },
    { name: 'laptop', use: { viewport: { width: 1024, height: 900 } } },
    { name: 'tablet', use: { viewport: { width: 768, height: 1000 } } },
    { name: 'mobile', use: { viewport: { width: 375, height: 1000 } } },
  ],
  webServer: [
    { command: `"${python}" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log`, cwd: backend,
      url: 'http://127.0.0.1:8000/api/health', reuseExistingServer: !process.env.CI },
    { command: 'npm run dev', url: 'http://127.0.0.1:5173', reuseExistingServer: !process.env.CI },
  ],
})
