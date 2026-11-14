import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import ModernSelect from './components/ModernSelect'

const options = [
  { value: 'UNKNOWN', label: 'Unknown' },
  { value: 'FDI', label: 'FDI' },
  { value: 'UNIVERSAL', label: 'Universal' },
]

function setup(value = 'UNKNOWN') {
  const onChange = vi.fn()
  render(<>
    <label htmlFor="notation">Tooth notation</label>
    <ModernSelect id="notation" value={value} options={options} onChange={onChange} ariaLabel="Tooth notation" />
  </>)
  return { onChange, trigger: screen.getByRole('combobox', { name: 'Tooth notation' }) }
}

describe('ModernSelect', () => {
  it('opens, marks the selected option and chooses with a pointer', () => {
    const { onChange, trigger } = setup()
    fireEvent.click(trigger)
    expect(screen.getByRole('listbox', { name: 'Tooth notation options' })).toBeVisible()
    expect(screen.getByRole('option', { name: 'Unknown' })).toHaveAttribute('aria-selected', 'true')
    fireEvent.click(screen.getByRole('option', { name: 'FDI' }))
    expect(onChange).toHaveBeenCalledWith('FDI')
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
    expect(trigger).toHaveFocus()
  })

  it('supports arrow keys and Enter', () => {
    const { onChange, trigger } = setup()
    fireEvent.keyDown(trigger, { key: 'ArrowDown' })
    expect(screen.getByRole('listbox')).toBeVisible()
    fireEvent.keyDown(trigger, { key: 'ArrowDown' })
    fireEvent.keyDown(trigger, { key: 'Enter' })
    expect(onChange).toHaveBeenCalledWith('FDI')
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })

  it('closes with Escape and returns focus to the trigger', () => {
    const { trigger } = setup()
    fireEvent.click(trigger)
    fireEvent.keyDown(trigger, { key: 'Escape' })
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
    expect(trigger).toHaveFocus()
  })

  it('closes when the pointer goes outside', () => {
    const { trigger } = setup()
    fireEvent.click(trigger)
    fireEvent.pointerDown(document.body)
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })
})
