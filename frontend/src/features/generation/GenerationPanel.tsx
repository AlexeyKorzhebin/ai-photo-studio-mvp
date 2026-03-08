import { useState } from 'react'
import { generateImage } from '../../api/generation'

export function GenerationPanel({ onCreated }: { onCreated: () => Promise<void> }) {
  const [prompt, setPrompt] = useState('')
  const [size, setSize] = useState('1024x1024')
  const [style, setStyle] = useState('')
  const [busy, setBusy] = useState(false)
  const [provider, setProvider] = useState<string | null>(null)

  async function handleGenerate() {
    if (!prompt.trim()) return
    setBusy(true)
    try {
      const result = await generateImage(prompt, size, style || undefined)
      setProvider(result.provider)
      await onCreated()
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel stack">
      <h2>Generate</h2>
      <div className="field">
        <label>Prompt</label>
        <textarea rows={4} value={prompt} onChange={(event) => setPrompt(event.target.value)} />
      </div>
      <div className="field">
        <label>Size</label>
        <select value={size} onChange={(event) => setSize(event.target.value)}>
          <option value="1024x1024">1024×1024</option>
          <option value="1024x1536">1024×1536</option>
          <option value="1536x1024">1536×1024</option>
        </select>
      </div>
      <div className="field">
        <label>Style</label>
        <input value={style} onChange={(event) => setStyle(event.target.value)} placeholder="cinematic / comic / clean product" />
      </div>
      <button type="button" disabled={busy} onClick={handleGenerate}>{busy ? 'Generating…' : 'Generate Image'}</button>
      {provider && <div style={{ color: 'var(--muted)' }}>Last provider: {provider}</div>}
    </div>
  )
}
