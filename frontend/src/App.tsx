import { useEffect, useMemo, useReducer, useState } from 'react'
import { listAssets, updateMetadata, uploadAsset } from './api/assets'
import { GalleryUploadPanel } from './features/gallery/GalleryUploadPanel'
import { GalleryView } from './features/gallery/GalleryView'
import { initialGalleryState } from './features/gallery/galleryStore'
import { EditorControls } from './features/editor/EditorControls'
import { EditorWorkspace } from './features/editor/EditorWorkspace'
import { editorReducer, initialEditorState } from './features/editor/editorReducer'
import { ExportDialog } from './features/export/ExportDialog'
import { GenerationPanel } from './features/generation/GenerationPanel'
import type { Asset } from './state/types'

export default function App() {
  const [gallery, setGallery] = useState(initialGalleryState)
  const [editor, dispatch] = useReducer(editorReducer, initialEditorState)
  const [selected, setSelected] = useState<Asset | null>(null)
  const [notes, setNotes] = useState('')
  const [tags, setTags] = useState('')

  async function refresh(query = gallery.query, sortBy = gallery.sortBy, order = gallery.order) {
    setGallery((prev) => ({ ...prev, loading: true, error: null, query, sortBy, order }))
    try {
      const items = await listAssets(query, sortBy, order)
      setGallery((prev) => ({ ...prev, items, loading: false, query, sortBy, order }))
      if (selected) {
        const updated = items.find((asset) => asset.id === selected.id)
        if (updated) {
          setSelected(updated)
          dispatch({ type: 'select', asset: updated })
          setNotes(updated.metadata.notes)
          setTags(updated.metadata.tags.join(', '))
        }
      }
    } catch (error) {
      setGallery((prev) => ({ ...prev, loading: false, error: error instanceof Error ? error.message : 'Failed to load assets' }))
    }
  }

  useEffect(() => { void refresh() }, [])

  const activeOperations = useMemo(() => editor.operations.slice(0, editor.cursor), [editor.operations, editor.cursor])

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p>Local-first image lab for uploads, non-destructive edits, exports, and deterministic AI fallback generation.</p>
          <h1>AI Photo Studio MVP</h1>
        </div>
        <div className="panel">
          <strong>Runtime</strong>
          <div>Single-user, local-first, port 8088</div>
        </div>
      </section>
      <section className="layout">
        <div className="stack">
          <GalleryUploadPanel onUpload={async (file) => { await uploadAsset(file); await refresh() }} />
          <div className="panel stack">
            <div className="field">
              <label>Search</label>
              <input value={gallery.query} onChange={(event) => setGallery((prev) => ({ ...prev, query: event.target.value }))} placeholder="filename, tag, note" />
            </div>
            <div className="toolbar">
              <select value={gallery.sortBy} onChange={(event) => void refresh(gallery.query, event.target.value, gallery.order)}>
                <option value="updated_at">Updated</option>
                <option value="created_at">Created</option>
                <option value="name">Name</option>
              </select>
              <select value={gallery.order} onChange={(event) => void refresh(gallery.query, gallery.sortBy, event.target.value)}>
                <option value="desc">Desc</option>
                <option value="asc">Asc</option>
              </select>
            </div>
            <button type="button" onClick={() => void refresh(gallery.query, gallery.sortBy, gallery.order)}>Refresh Query</button>
            {gallery.error && <div style={{ color: 'crimson' }}>{gallery.error}</div>}
          </div>
          {selected && (
            <div className="panel stack">
              <h2>Metadata</h2>
              <div className="field">
                <label>Tags</label>
                <input value={tags} onChange={(event) => setTags(event.target.value)} placeholder="portrait, test, red" />
              </div>
              <div className="field">
                <label>Notes</label>
                <textarea rows={4} value={notes} onChange={(event) => setNotes(event.target.value)} />
              </div>
              <button type="button" onClick={async () => {
                await updateMetadata(selected.id, tags.split(',').map((item) => item.trim()).filter(Boolean), notes)
                await refresh()
              }}>Save Metadata</button>
            </div>
          )}
          <GenerationPanel onCreated={async () => { await refresh() }} />
          <ExportDialog assetId={selected?.id} operations={activeOperations} />
        </div>
        <div className="stack">
          <EditorControls dispatch={dispatch} disabled={!selected} canUndo={editor.cursor > 0} canRedo={editor.cursor < editor.operations.length} />
          <EditorWorkspace asset={selected} operations={activeOperations} compareMode={editor.compareMode} />
          <div className="panel stack">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2>Library</h2>
              <span>{gallery.loading ? 'Refreshing…' : `${gallery.items.length} assets`}</span>
            </div>
            <GalleryView assets={gallery.items} selectedId={selected?.id} onSelect={(asset) => {
              setSelected(asset)
              dispatch({ type: 'select', asset })
              setNotes(asset.metadata.notes)
              setTags(asset.metadata.tags.join(', '))
            }} />
          </div>
        </div>
      </section>
    </main>
  )
}
