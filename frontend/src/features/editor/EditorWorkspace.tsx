import type { Asset, EditOperation } from '../../state/types'
import { assetBinaryUrl } from '../../api/assets'
import { buildPreviewStyle } from './previewRenderer'

export function EditorWorkspace({ asset, operations, compareMode }: { asset: Asset | null; operations: EditOperation[]; compareMode: boolean }) {
  if (!asset) {
    return <div className="panel"><p>Select an image to start editing.</p></div>
  }

  const activeOperations = compareMode ? [] : operations

  return (
    <div className="panel stack">
      <div className="editor-preview">
        <img src={assetBinaryUrl(asset.id)} alt={asset.original_filename} style={buildPreviewStyle(activeOperations)} />
      </div>
      <div className="metrics">
        <div className="metric"><strong>Mode</strong><div>{compareMode ? 'Original' : 'Edited'}</div></div>
        <div className="metric"><strong>Ops</strong><div>{operations.length}</div></div>
        <div className="metric"><strong>Asset</strong><div>{asset.width}×{asset.height}</div></div>
      </div>
    </div>
  )
}
