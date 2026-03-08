import { api } from './client'

export async function generateImage(prompt: string, size: string, style?: string) {
  return api<{ asset_id: string; provider: string }>('/api/generation', {
    method: 'POST',
    body: JSON.stringify({ prompt, size, style }),
  })
}
