import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'
import fixture from './test/fixtures/synthetic-parse-result.json'

afterEach(() => { vi.unstubAllGlobals() })

it('advances workflow progress only when input, parsing and review evidence exist', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ ...fixture }) }))
  render(<App />)
  const progress = screen.getByRole('list', { name: 'Planning workflow' })
  const active = () => progress.querySelector('li[aria-current="step"]') as HTMLElement
  const completed = () => progress.querySelectorAll('li[data-state="complete"]')

  expect(active()).toHaveTextContent('Input')
  expect(active()).toHaveTextContent('Add synthetic text')
  expect(completed()).toHaveLength(0)

  fireEvent.change(screen.getByRole('textbox', { name: 'Raw TMT text' }), { target: { value: fixture.raw_text } })
  expect(active()).toHaveTextContent('Input')
  expect(active()).toHaveTextContent('Confirm synthetic data')
  expect(completed()).toHaveLength(0)

  fireEvent.click(screen.getByRole('checkbox', { name: /I confirm this text is synthetic/ }))
  expect(active()).toHaveTextContent('Inspection')
  expect(active()).toHaveTextContent('Parse text')
  expect(completed()).toHaveLength(1)

  fireEvent.click(screen.getByRole('button', { name: 'Parse Table' }))
  await screen.findByRole('heading', { name: 'Structured lexical preview' })
  expect(active()).toHaveTextContent('Planning review')
  expect(active()).toHaveTextContent('Run review')
  expect(completed()).toHaveLength(2)

  fireEvent.click(within(screen.getByRole('navigation', { name: 'Review purpose' })).getByRole('button', { name: /MICRO/ }))
  expect(screen.queryByRole('heading', { name: 'Structured lexical preview' })).not.toBeInTheDocument()
  expect(active()).toHaveTextContent('Inspection')
  expect(active()).toHaveTextContent('Parse text')
  expect(completed()).toHaveLength(1)
})
