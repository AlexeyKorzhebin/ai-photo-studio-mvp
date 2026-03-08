# Implementation Plan: AI Photo Studio MVP

## Plan Scope
This plan covers MVP delivery for `001-ai-photo-editor-viewer` using the clarified spec and constitution constraints:
- Local-first only, no auth, single user.
- Frontend: React + Vite + TypeScript.
- Backend: FastAPI + SQLite.
- Storage: SQLite metadata + local filesystem volume for image bytes.
- Runtime contract: Docker Compose app reachable on `http://localhost:8088`.

## Current Baseline (Repository)
- Backend already has foundational routes and storage service:
  - `GET /api/health`
  - asset list/upload/get/file/update
  - `POST /api/ai/generate`
- Frontend already has gallery/editor/generate shell and client-side edit/export pipeline.
- Compose already maps frontend to port `8088` and mounts backend data volume.

Plan focus is to close MVP spec gaps, harden determinism/validation behavior, and ensure phase-based, testable delivery.

## Technical Decisions (MVP)
- Keep edit history session-scoped in frontend state only.
- Keep edit operations client-side and non-destructive; backend stores source/generated assets only.
- Keep tags as plain comma-separated text on `ImageAsset` (no normalization table).
- Use deterministic mock generation based on normalized input tuple (`prompt`, `size`, `style`, `provider_override`) with stored seed/hash metadata.
- Enforce allowed AI size values at API boundary: `1024x1024`, `1024x1536`, `1536x1024`.
- Enforce deterministic sorting with stable secondary key (`id`) for tie handling.

## Implementation Phases

### Phase 1: Backend Contract Hardening
Goal: Align API behavior exactly with clarified MVP rules.

Implementation intent:
- `backend/app/schemas/image.py`
  - Replace free width/height with `size` enum input for generation.
  - Validate optional quality range for export-related schema if server export endpoint is added later.
- `backend/app/api/routes.py`
  - Implement search term splitting (AND across terms, case-insensitive substring across filename/tags/notes).
  - Add deterministic tie-break ordering (`primary sort`, then `id`).
  - Return user-correctable validation errors for unsupported size/empty prompt/invalid params.
- `backend/app/services/ai_providers.py`
  - Normalize prompt/style/provider override inputs.
  - Generate deterministic seed/hash and attach to result metadata.
  - Keep fallback to mock if provider config missing.
- `backend/app/models/image.py`
  - Add minimal metadata fields needed for generated outputs (`is_mock`, `seed_hash`, optional generation params) if absent.

Validation checkpoint:
- API tests for search semantics, stable sort, deterministic fallback bytes/metadata, and validation errors.

### Phase 2: Backend Metadata + Storage Safety
Goal: Guarantee non-overwrite storage and predictable metadata lifecycle.

Implementation intent:
- `backend/app/services/storage.py`
  - Keep UUID storage names for collision avoidance.
  - Ensure MIME/type validation and image readability checks are explicit.
- `backend/app/api/routes.py`
  - Confirm upload/generate operations are all-or-nothing at request level.
  - Preserve user-visible filename while decoupling stored path.

Validation checkpoint:
- Tests for duplicate original filenames producing unique stored files and separate records.
- Tests for unsupported type rejection and empty-file rejection.

### Phase 3: Frontend Gallery + Metadata Editing Completion
Goal: Meet gallery/search/sort/tag-note behavior expected by MVP.

Implementation intent:
- `frontend/src/api/client.ts`
  - Align generation payload with new backend `size` contract.
- `frontend/src/components/GalleryPanel.tsx`
  - Keep full-list rendering (no pagination), deterministic control mapping.
  - Provide editable tags/notes controls with save flow to `PATCH /api/images/{id}`.
- `frontend/src/App.tsx`
  - Apply debounced search input dispatch.
  - Ensure refresh/selection behavior remains stable when list updates.

Validation checkpoint:
- Frontend tests for search/sort requests, metadata edit save path, and asset selection persistence after refresh.

### Phase 4: Frontend Editor UX Completion
Goal: Ensure clarified edit workflow behavior is explicit and demoable.

Implementation intent:
- `frontend/src/components/EditorPanel.tsx`
  - Keep non-destructive operations stack and undo/redo boundaries.
  - Preserve explicit crop apply/cancel behavior.
  - Ensure compare mode clearly toggles original vs current state.
  - Keep export naming `<original-base>-edited.<ext>` and quality control for jpg/webp.
- `frontend/src/editor/render.ts`
  - Keep deterministic operation application order for repeatable rendering.

Validation checkpoint:
- Frontend tests for undo/redo boundaries, compare mode, and export filename/format handling.
- Manual smoke: original file unchanged after edits.

### Phase 5: Runtime, Observability, and Final Verification
Goal: Guarantee MVP is runnable and demonstrable through Compose.

Implementation intent:
- `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`
  - Keep compose runtime with frontend exposed on `8088`.
- `README.md` and `specs/.../quickstart.md`
  - Ensure runbook and smoke checks are accurate.

Validation checkpoint:
- `docker compose up --build` brings up services.
- Browser checks: `http://localhost:8088`, `GET /api/health`, `/docs`.

## Delivery Checkpoints
1. Checkpoint A: Backend contract and deterministic AI fallback behavior locked with tests.
2. Checkpoint B: Gallery metadata editing/search/sort semantics validated end-to-end.
3. Checkpoint C: Editor compare/undo-redo/export behaviors validated.
4. Checkpoint D: Compose runtime demo on `8088` plus smoke verification documented.

## Validation Strategy
- Backend:
  - `pytest` for API behavior and service determinism.
  - Focus tests on acceptance criteria + clarified edge cases.
- Frontend:
  - Vitest + Testing Library for gallery/editor interaction logic.
  - Keep tests targeted (state transitions, request payloads, key UI toggles).
- Manual smoke (required for release gate):
  - Upload sample images.
  - Search/sort/metadata edits.
  - Edit + undo/redo + compare + export.
  - AI generate in configured mode and fallback mode.
  - Verify health/docs/compose runtime.

## Minimal File-Level Implementation Map
- Backend API/contracts:
  - `backend/app/schemas/image.py`
  - `backend/app/api/routes.py`
  - `backend/app/models/image.py`
  - `backend/app/services/ai_providers.py`
  - `backend/app/services/storage.py`
  - `backend/tests/test_api.py`
- Frontend UI/contracts:
  - `frontend/src/types.ts`
  - `frontend/src/api/client.ts`
  - `frontend/src/App.tsx`
  - `frontend/src/components/GalleryPanel.tsx`
  - `frontend/src/components/EditorPanel.tsx`
  - `frontend/src/editor/render.ts`
  - `frontend/src/App.test.tsx`
- Runtime/docs:
  - `docker-compose.yml`
  - `README.md`
  - `specs/001-ai-photo-editor-viewer/quickstart.md`

## Out of Scope (Enforced)
- Auth/user accounts.
- Cloud storage or cloud database.
- Pagination/virtualized gallery.
- Persisted edit stacks across reload.
- EXIF write-back to source files.
