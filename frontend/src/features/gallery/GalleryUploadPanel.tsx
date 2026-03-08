import { useState } from 'react'

export function GalleryUploadPanel({ onUpload }: { onUpload: (file: File) => Promise<void> }) {
  const [busy, setBusy] = useState(false)

  return (
    <div className="panel stack">
      <div>
        <h2>Ingest</h2>
        <p>Drop a local image into the library. Duplicate names never overwrite originals.</p>
      </div>
      <input
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={async (event) => {
          const file = event.target.files?.[0]
          if (!file) return
          setBusy(true)
          try {
            await onUpload(file)
          } finally {
            setBusy(false)
            event.currentTarget.value = ''
          }
        }}
      />
      <button type="button" disabled={busy}>{busy ? 'Uploading…' : 'Upload Image'}</button>
    </div>
  )
}
