import { Check, ChevronDown } from 'lucide-react'
import { useEffect, useId, useRef, useState } from 'react'
import type { CSSProperties, KeyboardEvent } from 'react'
import { createPortal } from 'react-dom'

export interface ModernSelectOption {
  value: string
  label: string
}

interface ModernSelectProps {
  id: string
  value: string
  options: readonly ModernSelectOption[]
  onChange: (value: string) => void
  ariaLabel: string
}

export default function ModernSelect({ id, value, options, onChange, ariaLabel }: ModernSelectProps) {
  const [open, setOpen] = useState(false)
  const [position, setPosition] = useState<CSSProperties>({})
  const selectedIndex = Math.max(0, options.findIndex(option => option.value === value))
  const [activeIndex, setActiveIndex] = useState(selectedIndex)
  const rootRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)
  const menuRef = useRef<HTMLDivElement>(null)
  const optionRefs = useRef<Array<HTMLDivElement | null>>([])
  const baseId = useId().replace(/[^a-zA-Z0-9_-]/g, '')
  const listId = `${baseId}-listbox`
  const optionId = (index: number) => `${baseId}-option-${index}`
  const selected = options[selectedIndex] ?? options[0]

  function placeMenu() {
    const trigger = triggerRef.current
    if (!trigger) return
    const rect = trigger.getBoundingClientRect()
    const gutter = 8
    const width = rect.width
    const estimatedHeight = Math.min(options.length * 44 + 12, 280)
    const spaceBelow = window.innerHeight - rect.bottom - gutter
    const spaceAbove = rect.top - gutter
    const openUp = spaceBelow < estimatedHeight && spaceAbove > spaceBelow
    const left = Math.min(Math.max(gutter, rect.left), Math.max(gutter, window.innerWidth - width - gutter))
    const top = openUp
      ? Math.max(gutter, rect.top - estimatedHeight - 8)
      : Math.max(gutter, Math.min(rect.bottom + 8, window.innerHeight - estimatedHeight - gutter))
    setPosition({ position: 'fixed', top, left, width, zIndex: 60 })
  }

  function openMenu(index = selectedIndex) {
    setActiveIndex(index)
    placeMenu()
    setOpen(true)
  }

  function closeMenu(refocus = false) {
    setOpen(false)
    if (refocus) triggerRef.current?.focus()
  }

  function choose(index: number) {
    const option = options[index]
    if (!option) return
    onChange(option.value)
    setActiveIndex(index)
    closeMenu(true)
  }

  useEffect(() => {
    if (!open) return
    const handlePointerDown = (event: PointerEvent) => {
      const target = event.target as Node
      if (!rootRef.current?.contains(target) && !menuRef.current?.contains(target)) setOpen(false)
    }
    const handleViewportChange = () => placeMenu()
    document.addEventListener('pointerdown', handlePointerDown)
    window.addEventListener('resize', handleViewportChange)
    window.addEventListener('scroll', handleViewportChange, true)
    return () => {
      document.removeEventListener('pointerdown', handlePointerDown)
      window.removeEventListener('resize', handleViewportChange)
      window.removeEventListener('scroll', handleViewportChange, true)
    }
  }, [open])

  useEffect(() => {
    if (open) optionRefs.current[activeIndex]?.scrollIntoView?.({ block: 'nearest' })
  }, [open, activeIndex])

  function handleKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      if (!open) openMenu()
      else setActiveIndex(index => Math.min(index + 1, options.length - 1))
    } else if (event.key === 'ArrowUp') {
      event.preventDefault()
      if (!open) openMenu()
      else setActiveIndex(index => Math.max(index - 1, 0))
    } else if (event.key === 'Home' && open) {
      event.preventDefault()
      setActiveIndex(0)
    } else if (event.key === 'End' && open) {
      event.preventDefault()
      setActiveIndex(options.length - 1)
    } else if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      if (open) choose(activeIndex)
      else openMenu()
    } else if (event.key === 'Escape' && open) {
      event.preventDefault()
      closeMenu(true)
    } else if (event.key === 'Tab') {
      setOpen(false)
    }
  }

  return (
    <div ref={rootRef} className="relative min-w-0">
      <button
        ref={triggerRef}
        id={id}
        type="button"
        role="combobox"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        aria-activedescendant={open ? optionId(activeIndex) : undefined}
        onClick={() => (open ? closeMenu() : openMenu())}
        onKeyDown={handleKeyDown}
        className="modern-select-trigger"
        data-open={open}
      >
        <span className="truncate">{selected.label}</span>
        <ChevronDown size={16} strokeWidth={2} className="modern-select-chevron" aria-hidden="true" />
      </button>
      {open && createPortal(
        <div ref={menuRef} id={listId} role="listbox" aria-label={`${ariaLabel} options`} className="modern-select-menu" style={position}>
          <div className="max-h-72 overflow-y-auto overscroll-contain p-1.5">
            {options.map((option, index) => {
              const isSelected = index === selectedIndex
              return (
                <div
                  key={option.value}
                  ref={element => { optionRefs.current[index] = element }}
                  id={optionId(index)}
                  role="option"
                  aria-selected={isSelected}
                  className="modern-select-option"
                  data-active={index === activeIndex}
                  data-selected={isSelected}
                  onMouseDown={event => event.preventDefault()}
                  onMouseEnter={() => setActiveIndex(index)}
                  onClick={() => choose(index)}
                >
                  <span className="truncate">{option.label}</span>
                  {isSelected && <Check size={15} strokeWidth={2.5} className="shrink-0 text-brand" aria-hidden="true" />}
                </div>
              )
            })}
          </div>
        </div>,
        document.body,
      )}
    </div>
  )
}
