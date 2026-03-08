# Reference context for fresh plan generation

Use this file as background context only.
Create fresh planning artifacts through Spec-Kit.
Do not mechanically copy prior plan/tasks.

## Product frame
- Feature: AI Photo Studio MVP (local-first single-user)
- Key flows: upload, gallery browse/search/sort, metadata, non-destructive edit, compare, export, AI generation with deterministic fallback
- Runtime target: Docker Compose on port 8088

## Prior technical direction worth considering
- frontend: React + Vite + TypeScript
- backend: FastAPI
- metadata persistence: SQLite
- binary asset persistence: local filesystem volume
- edit history remains session-scoped in frontend state
- generated/exported files should not mutate original assets
- deterministic mock generation should derive outputs from normalized input tuple
- sorting should have deterministic tie-breaks
- duplicate filenames must never overwrite stored files

## Prior engineering themes
- keep edit pipeline client-side and non-destructive where possible
- backend owns asset persistence, metadata, provider abstraction, validation, and health/docs endpoints
- frontend owns gallery/editor/generation UX and state transitions
- plan should produce research.md, data-model.md, contracts/, quickstart.md where relevant
- favor small testable phases and explicit verification checkpoints

## Older reference artifacts
- old plan: /home/openclaw/projects/ai-photo-studio-mvp-codex/specs/001-ai-photo-editor-viewer/plan.md
- old tasks: /home/openclaw/projects/ai-photo-studio-mvp-codex/specs/001-ai-photo-editor-viewer/tasks.md
- old system map: /home/openclaw/projects/ai-photo-studio-mvp-codex/docs/SPEC_KIT_SYSTEM_MAP.md
