import type { EditOperation } from '../state/types'

export async function exportAsset(assetId: string, operations: EditOperation[], format: string, quality?: number) {
  const response = await fetch('/api/exports', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ asset_id: assetId, operations, format, quality }),
  })
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Export failed' }))
    throw new Error(payload.detail ?? 'Export failed')
  }
  return response.blob()
}
