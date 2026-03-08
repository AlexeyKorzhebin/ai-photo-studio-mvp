import type { Dispatch } from 'react'
import type { EditorAction } from './editorReducer'

export function EditorControls({ dispatch, disabled, canUndo, canRedo }: { dispatch: Dispatch<EditorAction>; disabled: boolean; canUndo: boolean; canRedo: boolean }) {
  const addTonal = () => dispatch({ type: 'push', operation: { kind: 'tonal', params: { brightness: 1.08, contrast: 1.08, saturation: 1.1 } } })
  return (
    <div className="panel stack">
      <div>
        <h2>Edit Stack</h2>
        <p>Session-scoped, non-destructive operations. Originals stay immutable.</p>
      </div>
      <div className="toolbar">
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'push', operation: { kind: 'rotate', params: { degrees: 90 } } })}>Rotate 90°</button>
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'push', operation: { kind: 'flip', params: { axis: 'horizontal' } } })}>Flip H</button>
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'push', operation: { kind: 'flip', params: { axis: 'vertical' } } })}>Flip V</button>
        <button type="button" disabled={disabled} onClick={addTonal}>Boost Tone</button>
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'push', operation: { kind: 'filter', params: { preset: 'grayscale' } } })}>Grayscale</button>
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'push', operation: { kind: 'filter', params: { preset: 'sepia' } } })}>Sepia</button>
        <button type="button" disabled={!canUndo} onClick={() => dispatch({ type: 'undo' })}>Undo</button>
        <button type="button" disabled={!canRedo} onClick={() => dispatch({ type: 'redo' })}>Redo</button>
      </div>
      <div className="toolbar">
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'toggle-compare' })}>Before / After</button>
        <button type="button" disabled={disabled} onClick={() => dispatch({ type: 'reset' })}>Reset Session</button>
      </div>
    </div>
  )
}
