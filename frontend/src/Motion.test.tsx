import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import fixture from './test/fixtures/synthetic-parse-result.json'

const ok = (value: unknown) => ({ ok: true, status: 200, json: async () => value })
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

describe('Part 3 interaction presentation', () => {
  it('moves the module indicator without carrying stale results between purposes', () => {
    render(<App />)
    const nav = screen.getByRole('navigation', { name: 'Review purpose' })
    const indicator = nav.querySelector('.module-tab-indicator') as HTMLElement
    expect(indicator).toHaveAttribute('aria-hidden', 'true')
    expect(nav.style.getPropertyValue('--module-index')).toBe('0')
    expect(within(nav).getByRole('button', { name: /MACRO/ })).toHaveAttribute('aria-pressed', 'true')

    fireEvent.click(within(nav).getByRole('button', { name: /MICRO/ }))
    expect(nav.style.getPropertyValue('--module-index')).toBe('1')
    expect(within(nav).getByRole('button', { name: /MICRO/ })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('heading', { level: 1, name: 'Attachment Review' })).toBeVisible()
    expect(screen.queryByLabelText('Parse summary')).not.toBeInTheDocument()

    fireEvent.click(within(nav).getByRole('button', { name: /NANO/ }))
    expect(nav.style.getPropertyValue('--module-index')).toBe('2')
    expect(screen.getByRole('heading', { level: 1, name: 'Sequencing Review' })).toBeVisible()
  })

  it('shows an indeterminate control spinner and busy state until a parse response settles', async () => {
    let resolveFetch!: (value: unknown) => void
    const pending = new Promise(resolve => { resolveFetch = resolve })
    vi.stubGlobal('fetch', vi.fn().mockReturnValue(pending))
    render(<App />)
    fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: fixture.raw_text } })
    fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))

    const parsing = screen.getByRole('button', { name: 'Parsing…' })
    expect(parsing).toBeDisabled()
    expect(parsing.querySelector('.button-spinner')).not.toBeNull()
    expect(screen.getByRole('region', { name: 'Parse controls' })).toHaveAttribute('aria-busy', 'true')

    await act(async () => {
      resolveFetch(ok(fixture))
      await pending
    })
    const summary = await screen.findByLabelText('Parse summary')
    expect(summary).toBeVisible()
    expect(screen.getByRole('region', { name: 'Parse controls' })).toHaveAttribute('aria-busy', 'false')
    expect(screen.getByRole('button', { name: 'Parse Table' })).toBeEnabled()
    const preview = screen.getByRole('region', { name: 'Structured table' })
    expect(preview).toBeVisible()
  }, 15_000)
})
