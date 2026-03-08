export type AssetMetadata = { tags: string[]; notes: string }

export type Asset = {
  id: string
  origin_type: string
  original_filename: string
  stored_filename: string
  mime_type: string
  width: number
  height: number
  byte_size: number
  metadata: AssetMetadata
}

export type EditOperation = {
  kind: 'crop' | 'rotate' | 'flip' | 'tonal' | 'filter'
  params: Record<string, string | number>
}
