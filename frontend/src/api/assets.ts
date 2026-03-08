import { api } from './client'
import type { Asset } from '../state/types'

export async function listAssets(query = '', sortBy = 'updated_at', order = 'desc'): Promise<Asset[]> {
  const params = new URLSearchParams({ q: query, sortBy, order })
  const response = await api<{ items: Asset[] }>(`/api/assets?${params.toString()}`)
  return response.items
}

export async function uploadAsset(file: File): Promise<Asset> {
  const body = new FormData()
  body.append('file', file)
  return api<Asset>('/api/assets/upload', { method: 'POST', body })
}

export async function updateMetadata(assetId: string, tags: string[], notes: string): Promise<Asset> {
  return api<Asset>(`/api/assets/${assetId}/metadata`, {
    method: 'PATCH',
    body: JSON.stringify({ tags, notes }),
  })
}

export function assetBinaryUrl(assetId: string): string {
  return `/api/assets/${assetId}/binary`
}
