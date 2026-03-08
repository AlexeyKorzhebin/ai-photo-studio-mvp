import type { Asset } from '../../state/types'

export type GalleryState = {
  items: Asset[]
  query: string
  sortBy: string
  order: string
  loading: boolean
  error: string | null
}

export const initialGalleryState: GalleryState = {
  items: [],
  query: '',
  sortBy: 'updated_at',
  order: 'desc',
  loading: false,
  error: null,
}
