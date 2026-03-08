import { describe, expect, it } from 'vitest'
import { editorReducer, initialEditorState } from '../../src/features/editor/editorReducer'

describe('editorReducer', () => {
  it('supports push/undo/redo', () => {
    const pushed = editorReducer(initialEditorState, { type: 'push', operation: { kind: 'rotate', params: { degrees: 90 } } })
    expect(pushed.cursor).toBe(1)
    const undone = editorReducer(pushed, { type: 'undo' })
    expect(undone.cursor).toBe(0)
    const redone = editorReducer(undone, { type: 'redo' })
    expect(redone.cursor).toBe(1)
  })
})
