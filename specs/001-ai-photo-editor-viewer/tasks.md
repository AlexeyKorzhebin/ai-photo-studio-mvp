# Tasks: AI Photo Studio MVP (Re-sliced Execution Backlog)

Baseline note: repository already contains a partial implementation. This backlog is re-sliced from current `spec.md`/`plan.md`/`analyze.md`/`checklist.md` + prior `tasks.md` to unblock stalled execution by reducing task size. Existing genuinely completed tasks are preserved as completed.

## Workstream A: Backend Contract Hardening (API behavior vs clarified spec)
Dependency: foundation endpoints already exist; this stream should complete before frontend contract finalization in Workstream C.

- [x] Keep existing API surface available: `GET /api/health`, `GET/POST/PATCH /api/images*`, `POST /api/ai/generate` (`backend/app/api/routes.py`).
- [x] Enforce generation input contract from width/height to `size` enum (`1024x1024|1024x1536|1536x1024`) in schemas and route handling (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
- [x] Implement search semantics: split query by whitespace, AND across terms, case-insensitive substring across filename/tags/notes (`backend/app/api/routes.py`).
- [x] Implement deterministic sorting tie-breaker with secondary `id` for all supported sort keys (`backend/app/api/routes.py`).
- [x] Add generation response metadata required by plan/data model (`seed_hash`, mock flag) and persist fields if needed (`backend/app/models/image.py`, `backend/app/schemas/image.py`, `backend/app/api/routes.py`).

### A.1 Validation error contract (open)
- [ ] Verify missing prompt validation returns explicit user-correctable message (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
- [ ] Verify invalid `size` validation returns explicit user-correctable message with allowed values (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
- [ ] Decide whether `quality` validation is backend-enforced now or deferred; document decision in code comments/tests (`backend/app/api/routes.py`, `backend/tests/test_api.py`).
- [ ] If quality validation is in-scope server-side, implement explicit range error response (`backend/app/api/routes.py`, `backend/app/schemas/image.py`).

Parallelization:
- This workstream can run in parallel with Workstream D (editor UX polish) and Workstream E (docs/runtime corrections).

## Workstream B: Backend AI Determinism + Persistence Safety
Dependency: can start now; final API contract assertions should align with Workstream A.

- [x] Keep local storage collision-safe with unique stored filenames (`backend/app/services/storage.py`).
- [x] Keep upload type restrictions and empty-file rejection (`backend/app/services/storage.py`).
- [x] Normalize deterministic mock seed inputs to include (`prompt`, `size`, `style`, `provider_override`) and keep output stable for identical normalized input (`backend/app/services/ai_providers.py`).
- [x] Ensure deterministic metadata is returned and stored for generated assets (`backend/app/services/ai_providers.py`, `backend/app/models/image.py`, `backend/app/api/routes.py`).

### B.1 All-or-nothing request safety (open)
- [ ] Map upload flow failure points (file write vs DB commit) and document expected rollback behavior (`backend/app/api/routes.py`, `backend/app/services/storage.py`).
- [ ] Add/confirm cleanup when DB write fails after file write in upload path (`backend/app/api/routes.py`, `backend/app/services/storage.py`).
- [ ] Map generate flow failure points (provider/image bytes/storage/DB) and document expected rollback behavior (`backend/app/api/routes.py`, `backend/app/services/ai_providers.py`).
- [ ] Add/confirm cleanup when generate DB write fails after image storage write (`backend/app/api/routes.py`, `backend/app/services/storage.py`).

Parallelization:
- First three completed tasks can run in parallel with Workstream C frontend work; B.1 should be validated alongside Workstream F backend tests.

## Workstream C: Frontend Contract Alignment + Gallery Completion
Dependency: API contract from Workstream A must remain stable.

- [x] Keep gallery search/sort controls wired to API query params (`frontend/src/App.tsx`, `frontend/src/components/GalleryPanel.tsx`, `frontend/src/api/client.ts`).
- [x] Update generation client contract to send `size` (and optional style/provider) instead of width/height (`frontend/src/api/client.ts`, `frontend/src/types.ts`).
- [x] Update generator UI to select allowed size values and optional style preset/custom text (`frontend/src/components/TopBar.tsx`, `frontend/src/App.tsx`).

### C.1 Metadata editing UI (re-sliced from stalled task)
- [ ] Add local state for metadata draft values (`tags`, `notes`) in gallery/detail context (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Render tags input control for selected asset metadata (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Render notes input/textarea control for selected asset metadata (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Add per-asset edit mode toggle and cancel/reset behavior (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Implement save action wiring to `PATCH /api/images/{id}` client method (`frontend/src/components/GalleryPanel.tsx`, `frontend/src/api/client.ts`).
- [ ] Disable save button during in-flight patch request and prevent duplicate submits (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Surface patch failure state in UI with user-correctable message (`frontend/src/components/GalleryPanel.tsx`).
- [ ] Refresh or reconcile gallery state after successful patch without losing selected asset (`frontend/src/App.tsx`, `frontend/src/components/GalleryPanel.tsx`).

### C.2 Search/sort and selection stability (re-sliced)
- [ ] Add debounced dispatch wrapper for search input updates (`frontend/src/App.tsx`).
- [ ] Ensure debounce does not delay initial load or explicit refresh action (`frontend/src/App.tsx`).
- [ ] Preserve selected asset when list refresh returns same id (`frontend/src/App.tsx`).
- [ ] Gracefully clear or re-home selection when selected asset is no longer in filtered result (`frontend/src/App.tsx`).
- [ ] Ensure upload completion refresh keeps deterministic sort/search state (`frontend/src/App.tsx`).
- [ ] Ensure generate completion refresh keeps deterministic sort/search state (`frontend/src/App.tsx`).

Parallelization:
- C.1 metadata editor and C.2 selection stability can be delegated in parallel once API contract is stable.

## Workstream D: Frontend Editor MVP Completion
Dependency: independent of Workstream C except shared app state conventions.

- [x] Keep non-destructive client-side edit pipeline (original source untouched; export rendered client-side) (`frontend/src/components/EditorPanel.tsx`, `frontend/src/editor/render.ts`).
- [x] Keep undo/redo state history and compare-hold interaction in editor (`frontend/src/components/EditorPanel.tsx`).
- [x] Keep crop apply/clear controls and export naming pattern `<original-base>-edited.<ext>` (`frontend/src/components/EditorPanel.tsx`).

### D.1 Editor UX polish + verifiability (open)
- [ ] Verify crop cancel behavior exactly matches clarified apply/cancel intent (`frontend/src/components/EditorPanel.tsx`).
- [ ] If cancel behavior mismatches, adjust crop interaction copy and state transitions (`frontend/src/components/EditorPanel.tsx`).
- [ ] Make JPG/WEBP quality control visibility explicit by selected export format (`frontend/src/components/EditorPanel.tsx`).
- [ ] Ensure quality default and bounds are consistent for JPG/WEBP export options (`frontend/src/components/EditorPanel.tsx`).

Parallelization:
- This stream is parallel-safe with Workstreams A/B/C except for shared test updates in Workstream F.

## Workstream E: Runtime + Docs Contract Corrections
Dependency: can start immediately.

- [x] Keep Docker Compose exposing frontend at `http://localhost:8088` (`docker-compose.yml`).

### E.1 Docs reachability decision + docs accuracy (open)
- [ ] Choose docs strategy: proxy backend docs through frontend nginx vs document backend direct docs URL (`frontend/nginx.conf`, `README.md`, `specs/001-ai-photo-editor-viewer/quickstart.md`).
- [ ] Implement chosen docs strategy (proxy config change or docs-only correction) (`frontend/nginx.conf` and/or docs files).
- [ ] Verify `quickstart.md` docs instructions match actual reachable path under compose (`specs/001-ai-photo-editor-viewer/quickstart.md`).
- [ ] Verify README API/docs instructions match actual reachable path under compose (`README.md`).
- [ ] Reconcile README feature-status claims with implemented behavior only (`README.md`).

Parallelization:
- Fully parallel with implementation workstreams; re-check after final behavior changes.

## Workstream F: Verification and Release Gate (re-sliced by test surface)
Dependency: execute after corresponding implementation tasks land.

### F.1 Backend automated verification
- [x] Keep baseline API tests for health/upload/list/generate present (`backend/tests/test_api.py`).
- [x] Add tests for whitespace-split AND search semantics and deterministic tie-break sorting (`backend/tests/test_api.py`).
- [x] Add deterministic mock tests asserting stable bytes/metadata for identical normalized inputs and changed hash on input deltas (`backend/tests/test_api.py`, `backend/app/services/ai_providers.py`).
- [ ] Add test: missing prompt error contract (`backend/tests/test_api.py`).
- [ ] Add test: invalid `size` error contract includes allowed values (`backend/tests/test_api.py`).
- [ ] Add test: duplicate filename uploads create distinct records (`backend/tests/test_api.py`).
- [ ] Add test: duplicate filename uploads create distinct stored paths (`backend/tests/test_api.py`).
- [ ] Add test: upload rollback on DB failure (no orphaned stored file) (`backend/tests/test_api.py`).
- [ ] Add test: generate rollback on DB failure (no orphaned stored file) (`backend/tests/test_api.py`).

### F.2 Frontend automated verification
- [x] Keep baseline frontend smoke test present (`frontend/src/App.test.tsx`).
- [ ] Add test: generation request sends `size` field and optional style/provider values (`frontend/src/App.test.tsx` or dedicated test file).
- [ ] Add test: metadata editor renders existing tags/notes for selected asset (`frontend` tests).
- [ ] Add test: metadata save triggers PATCH request with expected payload (`frontend` tests).
- [ ] Add test: metadata save disabled while request in-flight (`frontend` tests).
- [ ] Add test: metadata save failure message is rendered (`frontend` tests).
- [ ] Add test: selected asset remains selected after successful metadata refresh (`frontend` tests).
- [ ] Add test: search debounce triggers fewer API calls while preserving query behavior (`frontend` tests).
- [ ] Add test: selection fallback behavior when selected asset disappears from filtered list (`frontend` tests).
- [ ] Add test: editor quality controls appear only for JPG/WEBP (`frontend` tests).
- [ ] Add test: undo/redo boundary controls are disabled at history edges (`frontend` tests).
- [ ] Add test: compare hold/toggle shows original preview state (`frontend` tests).

### F.3 Runtime and environment verification
- [ ] Ensure backend test dependencies are installed so `make test` can run (`backend` env/tooling).
- [ ] Run `make test`; record pass/fail and failing suites (`terminal evidence`).
- [ ] Run backend-only tests directly (if needed) to isolate backend failures (`terminal evidence`).
- [ ] Run frontend-only tests directly (if needed) to isolate frontend failures (`terminal evidence`).
- [ ] Run `make build`; record pass/fail (`terminal evidence`).
- [ ] Run `docker compose up --build` smoke flow (`terminal evidence`).
- [ ] Verify smoke checkpoint: app reachable at `http://localhost:8088`.
- [ ] Verify smoke checkpoint: `GET /api/health` reachable and OK.
- [ ] Verify smoke checkpoint: API docs reachable at chosen documented path.
- [ ] Verify smoke checkpoint: upload -> edit -> export succeeds.
- [ ] Verify smoke checkpoint: AI generate succeeds in provider mode or deterministic mock fallback mode.

### F.4 Release checklist closure
- [ ] Reconcile `specs/001-ai-photo-editor-viewer/checklist.md` line-by-line with evidence from F.1/F.2/F.3.
- [ ] Mark checklist items done only when evidence is captured in this wave.

Parallelization:
- Backend and frontend automated tests can run in parallel. Runtime smoke and checklist reconciliation can run once core tests are green or explicitly triaged.
