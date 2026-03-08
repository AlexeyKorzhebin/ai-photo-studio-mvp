import type { EditOperation } from '../../state/types'
import type { EditorSession } from './editorTypes'

export type EditorAction =
  | { type: 'select'; asset: EditorSession['asset'] }
  | { type: 'push'; operation: EditOperation }
  | { type: 'undo' }
  | { type: 'redo' }
  | { type: 'toggle-compare' }
  | { type: 'reset' }

export const initialEditorState: EditorSession = {
  asset: null,
  operations: [],
  cursor: 0,
  compareMode: false,
}

export function editorReducer(state: EditorSession, action: EditorAction): EditorSession {
  switch (action.type) {
    case 'select':
      return { asset: action.asset, operations: [], cursor: 0, compareMode: false }
    case 'push': {
      const nextOps = [...state.operations.slice(0, state.cursor), action.operation]
      return { ...state, operations: nextOps, cursor: nextOps.length }
    }
    case 'undo':
      return { ...state, cursor: Math.max(0, state.cursor - 1) }
    case 'redo':
      return { ...state, cursor: Math.min(state.operations.length, state.cursor + 1) }
    case 'toggle-compare':
      return { ...state, compareMode: !state.compareMode }
    case 'reset':
      return state.asset ? { ...state, operations: [], cursor: 0, compareMode: false } : state
    default:
      return state
  }
}
