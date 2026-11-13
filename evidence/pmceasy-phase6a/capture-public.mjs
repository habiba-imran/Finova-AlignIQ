// Research-only capture. No product code/config changes, authentication or traffic recording.
// Run with the project's existing Playwright; a fresh temporary browser profile is closed on exit.
import { chromium } from '../../frontend/node_modules/playwright-core/index.mjs'
import { mkdir, writeFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('./', import.meta.url))
await mkdir(`${root}images`, { recursive: true })
await mkdir(`${root}pages`, { recursive: true })
const images = [
  ['S01-tmt', '3e6ccf_5f290142e1414e518171635642f3a08b~mv2.jpeg'],
  ['S02-planning-input', '3e6ccf_54fade0cfea04ce394fb18748155aae6~mv2.jpg'],
  ['S03-planning-comments', '3e6ccf_38c1c632f3f64d198199c70bc94ab24a~mv2.png'],
  ['S04-functional', '3e6ccf_8cfe0f31111c4943b6f6aca7e323d53c~mv2.png'],
  ['S05-attachment-input', '3e6ccf_66e4c6964d59404c84a20a3cbc3e6808~mv2.png'],
  ['S06-attachment-output', '3e6ccf_c8d85f7deea64cb9a6450c92c3a4de64~mv2.png'],
  ['S07-sequencer-input', '3e6ccf_29beda4ea67f4943975f6117063df82c~mv2.png'],
  ['S08-sequencer-output', '3e6ccf_040682902f9c4662b8bd6b610942923c~mv2.png'],
]
const manifest = { kind: 'PUBLIC_MARKETING_OBSERVATIONS_NOT_PRODUCT_EXECUTION', date: '2026-11-14', source_page: 'https://www.pmceasy.com/', images: [], pages: [], limitations: [] }
const assetBrowser = await chromium.launch({ headless: true })
const assetContext = await assetBrowser.newContext({ serviceWorkers: 'block' })
await assetContext.route('**/*', route => new URL(route.request().url()).hostname === 'static.wixstatic.com' ? route.continue() : route.abort())
const assetPage = await assetContext.newPage()
for (const [id, asset] of images) {
  const url = `https://static.wixstatic.com/media/${asset}`
  try {
    const response = await assetPage.goto(url, { waitUntil: 'load', timeout: 25000 })
    if (!response?.ok() || !response.headers()['content-type']?.startsWith('image/')) throw new Error(`HTTP_${response?.status()}`)
    const bytes = await response.body()
    if (bytes.length > 20 * 1024 * 1024) throw new Error('ASSET_SIZE_LIMIT')
    const path = `images/${id}.${asset.split('.').pop()}`
    await writeFile(root + path, bytes)
    manifest.images.push({ id, url, path, bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex'), content_type: response.headers()['content-type'] })
  } catch (error) { manifest.images.push({ id, url, status: String(error.message).slice(0, 80) }) }
}
await assetContext.close()
await assetBrowser.close()
const browser = await chromium.launch({ headless: true })
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: 'en-US', serviceWorkers: 'block' })
  const allowed = new Set(['www.pmceasy.com', 'pmceasy.com', 'static.wixstatic.com', 'static.parastorage.com', 'siteassets.parastorage.com', 'video.wixstatic.com', 'fonts.googleapis.com', 'fonts.gstatic.com'])
  await context.route('**/*', route => {
    const u = new URL(route.request().url())
    if (u.protocol === 'https:' && allowed.has(u.hostname)) return route.continue()
    return route.abort()
  })
  for (const [id, url] of [['P01-home', 'https://www.pmceasy.com/'], ['P02-how-to', 'https://www.pmceasy.com/how-to'], ['P03-start-planning', 'https://www.pmceasy.com/start-planning']]) {
    const page = await context.newPage()
    try {
      const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 35000 })
      await page.waitForTimeout(2500)
      const structure = await page.evaluate(() => ({
        title: document.title,
        headings: [...document.querySelectorAll('h1,h2,h3,h4')].map(x => ({ level: x.tagName, text: x.textContent?.trim() })),
        controls: [...document.querySelectorAll('button,a,input,textarea,select')].map(x => ({
          tag: x.tagName, role: x.getAttribute('role'), label: x.getAttribute('aria-label') || x.textContent?.trim()?.slice(0, 160) || x.getAttribute('placeholder'),
          href: x.tagName === 'A' ? x.getAttribute('href') : undefined, type: x.getAttribute('type')
        })),
        images: [...document.querySelectorAll('img')].map(x => ({ alt: x.alt, src: x.currentSrc || x.src })),
        // URLs only, never downloaded script bodies, headers, cookies, storage or request payloads.
        script_urls: [...document.scripts].filter(x => x.src).map(x => { const u = new URL(x.src); return u.origin + u.pathname }),
      }))
      await page.screenshot({ path: `${root}pages/${id}.png`, fullPage: true })
      await writeFile(`${root}pages/${id}.json`, JSON.stringify(structure, null, 2) + '\n')
      manifest.pages.push({ id, requested_url: url, final_url: page.url().split('?')[0], http_status: response?.status(), screenshot: `pages/${id}.png`, structure: `pages/${id}.json`, behavior: 'NAVIGATION_ONLY_NO_FORMS_OR_AUTHENTICATION' })
    } catch (error) { manifest.pages.push({ id, requested_url: url, status: String(error.message).split('\n')[0].slice(0, 120) }) }
    await page.close()
  }
  await context.close()
} finally { await browser.close() }
manifest.limitations.push('Fresh isolated temporary browser profile; no existing user session. No login, purchase, form submission, HAR, cookies, storage, credentials or application script source retained. Third-party requests outside the explicit relevant asset allowlist were blocked; this can alter page behavior. No paid module was run.')
await writeFile(`${root}public-capture-manifest.json`, JSON.stringify(manifest, null, 2) + '\n')
console.log(JSON.stringify({ images: manifest.images.map(x => ({ id: x.id, bytes: x.bytes, status: x.status || 'SAVED' })), pages: manifest.pages }))
