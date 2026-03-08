# Tasks: AI Photo Studio MVP (Truthful Execution Backlog)

Baseline note: repository already contains a partial implementation. This backlog is normalized from `spec.md`/`plan.md` deltas versus current code, not from previously optimistic checkbox status.

## Workstream A: Backend Contract Hardening (API behavior vs clarified spec)
Dependency: foundation endpoints already exist; this stream should complete before frontend contract finalization in Workstream C.

- [x] Keep existing API surface available: `GET /api/health`, `GET/POST/PATCH /api/images*`, `POST /api/ai/generate` (`backend/app/api/routes.py`).
- [x] Enforce generation input contract from width/height to `size` enum (`1024x1024|1024x1536|1536x1024`) in schemas and route handling (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
- [x] Implement search semantics: split query by whitespace, AND across terms, case-insensitive substring across filename/tags/notes (`backend/app/api/routes.py`).
- [x] Implement deterministic sorting tie-breaker with secondary `id` for all supported sort keys (`backend/app/api/routes.py`).
- [ ] Return explicit user-correctable validation errors for missing prompt, invalid size, invalid quality params where applicable (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
- [x] Add generation response metadata required by plan/data model (`seed_hash`, mock flag) and persist fields if needed (`backend/app/models/image.py`, `backend/app/schemas/image.py`, `backend/app/api/routes.py`).

Parallelization:
- This workstream can run in parallel with Workstream D (editor UX polish) and Workstream E (docs/runtime corrections).

## Workstream B: Backend AI Determinism + Persistence Safety
Dependency: can start now; final API contract assertions should align with Workstream A.

- [x] Keep local storage collision-safe with unique stored filenames (`backend/app/services/storage.py`).
- [x] Keep upload type restrictions and empty-file rejection (`backend/app/services/storage.py`).
- [x] Normalize deterministic mock seed inputs to include (`prompt`, `size`, `style`, `provider_override`) and keep output stable for identical normalized input (`backend/app/services/ai_providers.py`).
- [x] Ensure deterministic metadata is returned and stored for generated assets (`backend/app/services/ai_providers.py`, `backend/app/models/image.py`, `backend/app/api/routes.py`).
- [ ] Verify upload/generate DB+file writes remain all-or-nothing at request level; add rollback handling if needed (`backend/app/api/routes.py`, `backend/app/services/storage.py`).

Parallelization:
- First three tasks can run in parallel with Workstream C frontend work; final all-or-nothing hardening should be validated alongside Workstream F backend tests.

## Workstream C: Frontend Contract Alignment + Gallery Completion
Dependency: finalize after Workstream A API contract decisions are merged.

- [x] Keep gallery search/sort controls wired to API query params (`frontend/src/App.tsx`, `frontend/src/components/GalleryPanel.tsx`, `frontend/src/api/client.ts`).
- [x] Update generation client contract to send `size` (and optional style/provider) instead of width/height (`frontend/src/api/client.ts`, `frontend/src/types.ts`).
- [x] Update generator UI to select allowed size values and optional style preset/custom text (`frontend/src/components/TopBar.tsx`, `frontend/src/App.tsx`).
- [ ] Add asset metadata editing UI for tags/notes and wire to `PATCH /api/images/{id}` (`frontend/src/components/GalleryPanel.tsx`, `frontend/src/api/client.ts`).
- [ ] Add debounced search dispatch to reduce API churn while preserving deterministic results (`frontend/src/App.tsx`).
- [ ] Ensure selection stability after refresh/search/sort and after generate/upload updates (`frontend/src/App.tsx`).

Parallelization:
- `tags/notes` editor and `generation contract/UI` can be delegated in parallel once Workstream A schema is settled.

## Workstream D: Frontend Editor MVP Completion
Dependency: independent of Workstream C except shared app state conventions.

- [x] Keep non-destructive client-side edit pipeline (original source untouched; export rendered client-side) (`frontend/src/components/EditorPanel.tsx`, `frontend/src/editor/render.ts`).
- [x] Keep undo/redo state history and compare-hold interaction in editor (`frontend/src/components/EditorPanel.tsx`).
- [x] Keep crop apply/clear controls and export naming pattern `<original-base>-edited.<ext>` (`frontend/src/components/EditorPanel.tsx`).
- [ ] Verify crop cancel behavior exactly matches clarified apply/cancel intent; adjust UX copy/behavior if needed (`frontend/src/components/EditorPanel.tsx`).
- [ ] Ensure JPG/WEBP quality behavior is explicit and validated in UI tests (`frontend/src/components/EditorPanel.tsx`, `frontend/src/App.test.tsx` or dedicated editor tests).

Parallelization:
- This stream is parallel-safe with Workstreams A/B/C except for shared test updates in Workstream F.

## Workstream E: Runtime + Docs Contract Corrections
Dependency: can start immediately.

- [x] Keep Docker Compose exposing frontend at `http://localhost:8088` (`docker-compose.yml`).
- [ ] Fix docs/runtime guidance for API docs reachability under compose (currently backend `/docs` is not exposed on `8088`) (`README.md`, `specs/001-ai-photo-editor-viewer/quickstart.md`, optionally `frontend/nginx.conf` if proxying `/docs` is chosen).
- [ ] Reconcile README feature claims with actual implemented behavior (avoid claiming completed deterministic metadata/search semantics until delivered) (`README.md`).

Parallelization:
- Fully parallel with implementation workstreams; should be re-checked after final behavior changes.

## Workstream F: Verification and Release Gate (separate from implementation)
Dependency: execute after corresponding implementation tasks land.

### Backend verification
- [x] Keep baseline API tests for health/upload/list/generate present (`backend/tests/test_api.py`).
- [x] Add tests for whitespace-split AND search semantics and deterministic tie-break sorting (`backend/tests/test_api.py`).
- [ ] Add tests for generation `size` enum validation and clear error responses (`backend/tests/test_api.py`).
- [x] Add deterministic mock tests asserting stable bytes/metadata for identical normalized inputs and changed hash on input deltas (`backend/tests/test_api.py`, `backend/app/services/ai_providers.py`).
- [ ] Add tests for duplicate filename uploads producing distinct stored files/records (`backend/tests/test_api.py`).

### Frontend verification
- [x] Keep baseline frontend smoke test present (`frontend/src/App.test.tsx`).
- [ ] Add tests for generation payload contract (`size` + optional style/provider) (`frontend/src/api/client.ts`, `frontend/src/App.test.tsx` or new tests).
- [ ] Add tests for tags/notes update flow and state refresh behavior (`frontend/src/components/GalleryPanel.tsx`, frontend tests).
- [ ] Add tests for editor export format/quality controls and compare/undo/redo boundaries (frontend tests).

### Runtime/manual verification
- [ ] Run `make test` and record pass/fail with notes.
- [ ] Run `make build` and record pass/fail with notes.
- [ ] Run `docker compose up --build` smoke flow from quickstart and capture outcomes for: UI `8088`, `GET /api/health`, API docs path, upload/edit/export/generate fallback.

Parallelization:
- Backend and frontend automated tests can run in parallel.
- Manual compose smoke can run in parallel with final docs cleanup.
