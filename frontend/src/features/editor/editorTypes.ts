import type { Asset, EditOperation } from '../../state/types'

export type EditorSession = {
  asset: Asset | null
  operations: EditOperation[]
  cursor: number
  compareMode: boolean
}
