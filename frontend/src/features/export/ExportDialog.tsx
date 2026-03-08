import { useState } from 'react'
import type { EditOperation } from '../../state/types'
import { exportAsset } from '../../api/exports'

export function ExportDialog({ assetId, operations }: { assetId?: string; operations: EditOperation[] }) {
  const [format, setFormat] = useState('png')
  const [quality, setQuality] = useState(80)
  const [busy, setBusy] = useState(false)

  const disabled = !assetId || busy

  async function handleExport() {
    if (!assetId) return
    setBusy(true)
    try {
      const blob = await exportAsset(assetId, operations, format, format === 'png' ? undefined : quality)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `export.${format}`
      link.click()
      URL.revokeObjectURL(url)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel stack">
      <h2>Export</h2>
      <div className="field">
        <label>Format</label>
        <select value={format} onChange={(event) => setFormat(event.target.value)}>
          <option value="png">PNG</option>
          <option value="jpg">JPG</option>
          <option value="webp">WebP</option>
        </select>
      </div>
      {format !== 'png' && (
        <div className="field">
          <label>Quality</label>
          <input type="range" min="1" max="100" value={quality} onChange={(event) => setQuality(Number(event.target.value))} />
        </div>
      )}
      <button type="button" disabled={disabled} onClick={handleExport}>{busy ? 'Exporting…' : 'Export Current View'}</button>
    </div>
  )
}
