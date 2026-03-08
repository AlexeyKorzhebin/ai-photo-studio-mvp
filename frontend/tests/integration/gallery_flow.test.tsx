import { render, screen } from '@testing-library/react'
import App from '../../src/App'
import { vi } from 'vitest'

vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(JSON.stringify({ items: [] }), { headers: { 'Content-Type': 'application/json' } }))))

test('renders app shell', async () => {
  render(<App />)
  expect(await screen.findByText(/AI Photo Studio MVP/i)).toBeTruthy()
})
