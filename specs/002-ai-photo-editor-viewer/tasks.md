# Tasks: AI Photo Studio MVP (Local-First Single User)

**Input**: Design documents from `/specs/002-ai-photo-editor-viewer/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml, quickstart.md

**Tests**: Include backend and frontend tests because verification strategy and quickstart explicitly define automated test lanes.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`US1`, `US2`, `US3`, `US4`)
- Include exact file paths in descriptions

## Path Conventions

- Backend code: `backend/app/`
- Backend tests: `backend/tests/`
- Frontend code: `frontend/src/`
- Frontend tests: `frontend/tests/`
- Infra/runtime: `infra/docker/`, root config files

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize repository structure and local-first runtime scaffolding for MVP delivery.

- [ ] T001 Create backend dependency manifest and tool config in backend/pyproject.toml
- [ ] T002 [P] Create frontend package and scripts in frontend/package.json
- [ ] T003 [P] Create local environment template for runtime and provider selection in ./.env.example
- [ ] T004 Create single-port compose runtime for frontend+backend on localhost:8088 in infra/docker/docker-compose.yml
- [ ] T005 [P] Add developer workflow commands (dev/test/lint/build/up/down) in ./Makefile
- [ ] T006 [P] Create backend app entrypoint and API router skeleton in backend/app/main.py
- [ ] T007 [P] Create frontend app shell and route container in frontend/src/App.tsx

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story work.

**⚠️ CRITICAL**: No user story implementation starts before this phase is complete.

- [ ] T008 Configure backend settings, provider selection, and storage paths in backend/app/core/config.py
- [ ] T009 [P] Implement SQLite engine/session lifecycle in backend/app/db/session.py
- [ ] T010 [P] Implement SQLAlchemy base and metadata naming conventions in backend/app/db/base.py
- [ ] T011 Implement core persisted entities (ImageAsset, ImageMetadata, GeneratedArtifact) in backend/app/models/assets.py
- [ ] T012 Implement initial schema bootstrap/migration script for MVP tables in backend/app/db/init_db.py
- [ ] T013 [P] Implement shared backend API error model and exception handlers in backend/app/api/errors.py
- [ ] T014 [P] Implement storage service for immutable originals and derived artifacts in backend/app/services/storage_service.py
- [ ] T015 [P] Implement backend image utility helpers (probe, validate, encode/decode) in backend/app/services/image_ops.py
- [ ] T016 [P] Implement typed frontend API client and base error handling in frontend/src/api/client.ts
- [ ] T017 [P] Define shared frontend domain types for assets, metadata, edit ops, export, generation in frontend/src/state/types.ts
- [ ] T018 Add health endpoint (`GET /api/health`) wiring in backend/app/api/routes/health.py and backend/app/main.py

**Checkpoint**: Foundation ready; story phases can now execute.

---

## Phase 3: User Story 1 - Build a Local Photo Library (Priority: P1) 🎯 MVP

**Goal**: Upload valid images and browse/search/sort metadata in a deterministic local gallery.

**Independent Test**: Upload mixed valid/invalid files, update metadata, and verify deterministic search/sort results.

### Tests for User Story 1

- [ ] T019 [P] [US1] Add backend upload validation and duplicate filename collision tests in backend/tests/unit/test_upload_service.py
- [ ] T020 [P] [US1] Add backend gallery search/sort determinism integration tests in backend/tests/integration/test_gallery_list.py
- [ ] T021 [P] [US1] Add API contract tests for upload/list/metadata endpoints in backend/tests/contract/test_assets_api.py
- [ ] T022 [P] [US1] Add frontend gallery upload/search/sort interaction test in frontend/tests/integration/gallery_flow.test.tsx

### Implementation for User Story 1

- [ ] T023 [US1] Implement upload/list/get/metadata schemas in backend/app/schemas/assets.py
- [ ] T024 [US1] Implement asset repository queries with case-insensitive AND search and stable tie-breaks in backend/app/services/asset_repository.py
- [ ] T025 [US1] Implement upload and metadata services with immutable source guarantees in backend/app/services/asset_service.py
- [ ] T026 [US1] Implement asset API routes (`/assets/upload`, `/assets`, `/assets/{assetId}`, `/assets/{assetId}/metadata`, `/assets/{assetId}/binary`) in backend/app/api/routes/assets.py
- [ ] T027 [US1] Wire asset router into application API composition in backend/app/main.py
- [ ] T028 [US1] Implement gallery API functions for upload/list/metadata/binary in frontend/src/api/assets.ts
- [ ] T029 [US1] Implement gallery state store for query/sort/results/loading/error in frontend/src/features/gallery/galleryStore.ts
- [ ] T030 [US1] Implement gallery upload panel UI with client-side file type checks in frontend/src/features/gallery/GalleryUploadPanel.tsx
- [ ] T031 [US1] Implement gallery grid/search/sort UI with deterministic ordering display in frontend/src/features/gallery/GalleryView.tsx
- [ ] T032 [US1] Compose US1 gallery flow in frontend/src/App.tsx

**Checkpoint**: US1 is independently functional and demoable as MVP baseline.

---

## Phase 4: User Story 2 - Edit Without Losing Originals (Priority: P1)

**Goal**: Provide non-destructive editing with undo/redo and before/after compare for a selected asset.

**Independent Test**: Open an uploaded image, apply operation sequence, undo/redo correctly, and toggle compare mode.

### Tests for User Story 2

- [ ] T033 [P] [US2] Add frontend edit reducer tests for crop/rotate/flip/tonal/filter + cursor behavior in frontend/tests/unit/editorReducer.test.ts
- [ ] T034 [P] [US2] Add frontend integration test for editor undo/redo/compare workflow in frontend/tests/integration/editor_flow.test.tsx
- [ ] T035 [P] [US2] Add backend export-preview operation validation tests reused by editor payloads in backend/tests/unit/test_edit_operation_validation.py

### Implementation for User Story 2

- [ ] T036 [US2] Define edit operation and session types/validators in frontend/src/features/editor/editorTypes.ts
- [ ] T037 [US2] Implement deterministic edit session reducer (ops stack + cursor + compare flag) in frontend/src/features/editor/editorReducer.ts
- [ ] T038 [US2] Implement canvas preview pipeline applying ordered operations non-destructively in frontend/src/features/editor/previewRenderer.ts
- [ ] T039 [US2] Implement editor controls for crop/rotate/flip/tonal/filter and compare toggle in frontend/src/features/editor/EditorControls.tsx
- [ ] T040 [US2] Implement editor workspace and before/after viewport in frontend/src/features/editor/EditorWorkspace.tsx
- [ ] T041 [US2] Integrate selected gallery asset with editor session lifecycle in frontend/src/App.tsx
- [ ] T042 [US2] Add backend shared edit-operation validation schema for export/generation safety in backend/app/schemas/edit_ops.py

**Checkpoint**: US2 works independently with immutable originals and session-scoped undo/redo.

---

## Phase 5: User Story 3 - Export Finished Results (Priority: P2)

**Goal**: Export current visible state to `png`, `jpg`, and `webp` with quality controls where applicable.

**Independent Test**: Export edited and unedited images in all supported formats and verify stream output + validation errors.

### Tests for User Story 3

- [ ] T043 [P] [US3] Add backend export format and quality matrix integration tests in backend/tests/integration/test_export_api.py
- [ ] T044 [P] [US3] Add backend export unit tests for PNG quality-ignore and asset-not-found behavior in backend/tests/unit/test_export_service.py
- [ ] T045 [P] [US3] Add frontend integration test for export modal and download trigger states in frontend/tests/integration/export_flow.test.tsx

### Implementation for User Story 3

- [ ] T046 [US3] Define export request/response schemas in backend/app/schemas/export.py
- [ ] T047 [US3] Implement export rendering service from asset + operation stack to encoded output in backend/app/services/export_service.py
- [ ] T048 [US3] Implement `POST /exports` route with strict validation and streamed response in backend/app/api/routes/exports.py
- [ ] T049 [US3] Wire export router into application API composition in backend/app/main.py
- [ ] T050 [US3] Implement frontend export API call and binary download helper in frontend/src/api/exports.ts
- [ ] T051 [US3] Implement export dialog (format/quality) and action handling in frontend/src/features/export/ExportDialog.tsx
- [ ] T052 [US3] Connect editor visible state payload to export flow in frontend/src/App.tsx

**Checkpoint**: US3 exports are independently functional across all required formats.

---

## Phase 6: User Story 4 - Generate AI Images Reliably (Priority: P2)

**Goal**: Generate images through provider abstraction with deterministic local fallback when provider is unavailable.

**Independent Test**: Generate with provider configured and with missing/invalid credentials; verify deterministic fallback byte identity for repeated normalized inputs.

### Tests for User Story 4

- [ ] T053 [P] [US4] Add deterministic fallback golden-hash unit tests for normalized inputs in backend/tests/unit/test_generation_fallback.py
- [ ] T054 [P] [US4] Add generation API integration tests for provider selection and fallback behavior in backend/tests/integration/test_generation_api.py
- [ ] T055 [P] [US4] Add frontend integration test for generation form success/error/fallback states in frontend/tests/integration/generation_flow.test.tsx

### Implementation for User Story 4

- [ ] T056 [US4] Define generation request/response schemas and size constraints in backend/app/schemas/generation.py
- [ ] T057 [US4] Implement provider interface and resolver for `nano-banana`, `gpt-image`, and `auto` selection in backend/app/services/generation/providers.py
- [ ] T058 [US4] Implement deterministic fallback renderer using normalized tuple + SHA-256 seed in backend/app/services/generation/fallback_provider.py
- [ ] T059 [US4] Implement external provider adapters and graceful error mapping in backend/app/services/generation/external_providers.py
- [ ] T060 [US4] Implement generation orchestration service with ingest into ImageAsset records in backend/app/services/generation_service.py
- [ ] T061 [US4] Implement `POST /generation` route with allowed size validation in backend/app/api/routes/generation.py
- [ ] T062 [US4] Wire generation router into application API composition in backend/app/main.py
- [ ] T063 [US4] Implement frontend generation API client and payload validation in frontend/src/api/generation.ts
- [ ] T064 [US4] Implement generation prompt panel UI and result state handling in frontend/src/features/generation/GenerationPanel.tsx
- [ ] T065 [US4] Integrate generated asset insertion into gallery/editor selection flow in frontend/src/App.tsx

**Checkpoint**: US4 generation works with deterministic fallback and full gallery/editor handoff.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final MVP hardening, documentation, and runbook verification across stories.

- [ ] T066 [P] Add backend/ frontend lint and typecheck scripts integration in ./Makefile and frontend/package.json
- [ ] T067 [P] Add backend test runner configuration and common fixtures in backend/tests/conftest.py
- [ ] T068 [P] Add end-to-end smoke script for upload -> edit -> compare -> export -> generate in scripts/smoke_mvp.sh
- [ ] T069 Update README architecture, runbook, API examples, local-first constraints, and known limitations in ./README.md
- [ ] T070 Validate quickstart steps against implemented commands and runtime in specs/002-ai-photo-editor-viewer/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all user stories.
- **Phase 3 (US1)**: Depends on Phase 2; establishes MVP baseline.
- **Phase 4 (US2)**: Depends on Phase 3 selected asset flow.
- **Phase 5 (US3)**: Depends on Phase 4 edit payload path.
- **Phase 6 (US4)**: Depends on Phase 2 and integrates with US1/US2 gallery/editor flow.
- **Phase 7 (Polish)**: Depends on completion of desired story phases.

### User Story Dependencies

- **US1 (P1)**: First deliverable and strict MVP gate.
- **US2 (P1)**: Depends on US1 selection and binary retrieval.
- **US3 (P2)**: Depends on US2 visible-state operations.
- **US4 (P2)**: Can start after Foundational, but integration completion depends on US1 and editor handoff from US2.

### Within Each User Story

- Tests first (expected failing initially).
- Schemas/types before services.
- Services before routes/API clients.
- API integration before UI composition.

## Parallel Opportunities

- Setup: `T002`, `T003`, `T005`, `T006`, `T007` can run in parallel after `T001` starts.
- Foundational: `T009`, `T010`, `T013`, `T014`, `T015`, `T016`, `T017` can run in parallel; `T011`/`T012` gate persistence completion.
- US1: `T019`-`T022` parallel test authoring; `T028`-`T031` parallel frontend work after backend contract stabilizes.
- US2: `T033`-`T035` parallel tests; `T036`-`T040` can be split by reducer vs UI.
- US3: `T043`-`T045` parallel tests; `T050` and `T051` parallel after `T048` contract stabilization.
- US4: `T053`-`T055` parallel tests; `T057`, `T058`, `T059` parallel provider implementation tracks.

## Parallel Example: User Story 4

```bash
# Parallel backend provider tracks
Task: "T057 Implement provider interface and resolver in backend/app/services/generation/providers.py"
Task: "T058 Implement deterministic fallback renderer in backend/app/services/generation/fallback_provider.py"
Task: "T059 Implement external provider adapters in backend/app/services/generation/external_providers.py"

# Parallel frontend/backend validation tracks
Task: "T054 Add backend integration tests in backend/tests/integration/test_generation_api.py"
Task: "T055 Add frontend integration tests in frontend/tests/integration/generation_flow.test.tsx"
```

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate upload/gallery/search/sort on `localhost:8088`.
4. Demo MVP baseline.

### Incremental Delivery

1. Add US2 for non-destructive editing and compare.
2. Add US3 for export matrix.
3. Add US4 for generation provider abstraction and deterministic fallback.
4. Finish with Phase 7 polish and full smoke verification.

### Local-First Guardrails

1. Keep SQLite + local filesystem as only persistence targets.
2. Keep single-user scope; do not add auth or multi-tenant complexity.
3. Preserve deterministic behavior for sort ties and fallback generation outputs.
