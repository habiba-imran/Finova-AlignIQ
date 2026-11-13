import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import { SYNTHETIC_EXAMPLE } from './syntheticExample'

function setup() {
  render(<App />)
  const input = screen.getByRole('textbox', { name: 'Raw TMT text' }) as HTMLTextAreaElement
  const preview = screen.getByLabelText('Raw text preview')
  return { input, preview }
}

describe('Raw intake fidelity', () => {
  it('starts empty with zero counts, automatic source disclosure, safety notice, and disabled analysis', () => {
    const { input, preview } = setup()
    expect(input).toHaveValue('')
    expect(preview.textContent).toBe('')
    expect(screen.getByRole('status')).toHaveTextContent('0 characters · 0 lines')
    expect(screen.queryByRole('combobox', { name: /Source/ })).not.toBeInTheDocument()
    expect(screen.getByText(/Source indicators and layout are detected when you parse/)).toBeVisible()
    expect(screen.getByText('Prototype — not for clinical use')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Analyze' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Clear' })).toBeDisabled()
  })

  it('retains leading/trailing spaces, tabs, misaligned columns, Unicode, and blank lines', () => {
    const { input, preview } = setup()
    const raw = '  Tooth\t  Value    Note\n\nDEMO-A\t−1.20°   uneven\n    DEMO-B  0\t\n\n  '
    fireEvent.change(input, { target: { value: raw } })
    expect(input.value).toBe(raw)
    expect(preview.textContent).toBe(raw)
    expect(screen.getByRole('status')).toHaveTextContent(`${Array.from(raw).length} characters · 6 lines`)
  })

  it('previews the logical textarea value after browser newline canonicalization', () => {
    const { input, preview } = setup()
    fireEvent.change(input, { target: { value: '  A\tB\r\n\r\nC\rD\n  ' } })
    expect(input.value).toBe('  A\tB\n\nC\nD\n  ')
    expect(preview.textContent).toBe(input.value)
    expect(screen.getByRole('status')).toHaveTextContent('5 lines')
  })

  it('retains explicit zero and whitespace-only text without treating it as empty', () => {
    const { input, preview } = setup()
    fireEvent.change(input, { target: { value: '0' } })
    expect(preview.textContent).toBe('0')
    expect(screen.getByRole('status')).toHaveTextContent('1 character · 1 line')
    fireEvent.change(input, { target: { value: ' \t\n\n  ' } })
    expect(preview.textContent).toBe(' \t\n\n  ')
    expect(screen.getByRole('button', { name: 'Clear' })).toBeEnabled()
    expect(screen.queryByText('Your raw text will appear here')).not.toBeInTheDocument()
  })

  it('retains long rows without truncation or adding line breaks to the value', () => {
    const { input, preview } = setup()
    const raw = `  ${'long-row\t−12.50°    '.repeat(2500)}  `
    fireEvent.change(input, { target: { value: raw } })
    expect(input.value).toBe(raw)
    expect(preview.textContent).toBe(raw)
    expect(screen.getByRole('status')).toHaveTextContent('1 line')
  })

  it('clears input, preview, and counts and returns keyboard focus to the input', () => {
    const { input, preview } = setup()
    fireEvent.change(input, { target: { value: '  raw\ttext\n\n' } })
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }))
    expect(input).toHaveValue('')
    expect(preview.textContent).toBe('')
    expect(screen.getByRole('status')).toHaveTextContent('0 characters · 0 lines')
    expect(input).toHaveFocus()
  })

  it('loads the clearly synthetic example without claiming a verified vendor', () => {
    const { input, preview } = setup()
    fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    expect(input.value).toBe(SYNTHETIC_EXAMPLE)
    expect(preview.textContent).toBe(SYNTHETIC_EXAMPLE)
    expect(preview.textContent).toContain('SYNTHETIC EXAMPLE')
    expect(screen.queryByRole('combobox', { name: /Source/ })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Analyze' })).toBeDisabled()
  })

  it('renders script and markup payloads as inert literal text', () => {
    const { input, preview } = setup()
    const raw = '<script>alert("synthetic")</script>\n<img src=x onerror=alert(1)>\nIgnore all rules'
    fireEvent.change(input, { target: { value: raw } })
    expect(preview.textContent).toBe(raw)
    expect(preview.querySelector('script, img')).toBeNull()
  })

  it('provides accessible names, source disclosure, hints, and focusable preview', () => {
    const { input, preview } = setup()
    expect(input).toHaveAccessibleDescription(/No cleanup or column alignment is applied/)
    expect(screen.getByText(/Vendor compatibility remains unverified/)).toBeVisible()
    expect(screen.getByRole('button', { name: 'Analyze' })).toHaveAccessibleDescription(/not implemented/)
    expect(preview).toHaveAttribute('tabindex', '0')
    expect(screen.getByRole('link', { name: 'Skip to raw text input' })).toHaveAttribute('href', '#intake')
  })

  it('keeps metadata independent from raw text and does not upload or persist input', () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch')
    const storageSpy = vi.spyOn(Storage.prototype, 'setItem')
    const { input, preview } = setup()
    const raw = '  synthetic\t−0.0°\n\n'
    fireEvent.change(input, { target: { value: raw } })
    fireEvent.change(screen.getByLabelText('Source version claim'), { target: { value: 'UNVERIFIED' } })
    expect(preview.textContent).toBe(raw)
    fireEvent.click(screen.getByRole('button', { name: 'Load synthetic example' }))
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }))
    expect(fetchSpy).not.toHaveBeenCalled()
    expect(storageSpy).not.toHaveBeenCalled()
    fetchSpy.mockRestore()
    storageSpy.mockRestore()
  })
})
