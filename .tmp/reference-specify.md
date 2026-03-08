# Reference context for fresh Spec-Kit generation

Use this file as background context only.
Generate fresh artifacts through Spec-Kit commands.
Do not mechanically copy old artifacts.
Prefer concise, stakeholder-readable wording in spec artifacts.

## Product intent
Build a local-first AI Photo Studio MVP for experiment validation.
Single-user workflow: upload, browse, search, sort, edit non-destructively, compare before/after, export, and generate images through provider abstraction with deterministic fallback.

## Hard constraints
- local-first MVP only
- no auth / no multi-user model
- SQLite for metadata/state
- local filesystem volume for image assets
- frontend: React + Vite + TypeScript
- backend: FastAPI
- canonical runtime: Docker Compose on port 8088
- deterministic mock AI fallback must exist when provider config/credentials are missing

## Prior reference spec summary
- Upload valid png/jpg/jpeg/webp files
- Gallery shows metadata: filename, format, dimensions, size, created/updated time
- Search over filename/tags/notes
- Sort by created, updated, or name with deterministic behavior
- Non-destructive editing with crop/rotate/flip/adjustments/filters
- Undo/redo history
- Before/after compare mode
- Export current edit as png/jpg/webp with quality for jpg/webp
- AI generation accepts prompt, size, optional style, optional provider override
- Health endpoint and docs should be reachable

## Prior clarified defaults worth considering
- duplicate filenames must never overwrite stored files
- search = case-insensitive substring, split by whitespace, AND semantics across terms
- tags are simple comma-separated text
- edit history is session-scoped, not persisted across reloads
- allowed AI sizes: 1024x1024, 1024x1536, 1536x1024
- mock fallback should be deterministic for identical normalized inputs
- exported derivatives are downloadable outputs, not persisted as new assets by default
- no gallery pagination in MVP
- no EXIF write-back to source files

## Old artifact sources
- old constitution: /home/openclaw/projects/ai-photo-studio-mvp-codex/.specify/memory/constitution.md
- old spec: /home/openclaw/projects/ai-photo-studio-mvp-codex/specs/001-ai-photo-editor-viewer/spec.md
- old plan: /home/openclaw/projects/ai-photo-studio-mvp-codex/specs/001-ai-photo-editor-viewer/plan.md
- old tasks: /home/openclaw/projects/ai-photo-studio-mvp-codex/specs/001-ai-photo-editor-viewer/tasks.md
- old system map: /home/openclaw/projects/ai-photo-studio-mvp-codex/docs/SPEC_KIT_SYSTEM_MAP.md
