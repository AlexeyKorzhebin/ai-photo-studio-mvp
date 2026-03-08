import type { Asset } from '../../state/types'
import { assetBinaryUrl } from '../../api/assets'

export function GalleryView({ assets, selectedId, onSelect }: { assets: Asset[]; selectedId?: string; onSelect: (asset: Asset) => void }) {
  return (
    <div className="gallery-grid">
      {assets.map((asset) => (
        <article key={asset.id} className="asset-card" style={{ outline: asset.id === selectedId ? '2px solid var(--accent)' : 'none' }}>
          <img src={assetBinaryUrl(asset.id)} alt={asset.original_filename} loading="lazy" />
          <div style={{ padding: '12px' }}>
            <strong>{asset.original_filename}</strong>
            <div style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>{asset.width}×{asset.height} • {Math.round(asset.byte_size / 1024)} KB</div>
          </div>
          <button type="button" onClick={() => onSelect(asset)}>Open</button>
        </article>
      ))}
    </div>
  )
}
