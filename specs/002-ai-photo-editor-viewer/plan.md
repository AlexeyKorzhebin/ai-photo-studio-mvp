# Implementation Plan: AI Photo Studio MVP (Local-First Single User)

**Branch**: `002-ai-photo-editor-viewer` | **Date**: 2026-03-08 | **Spec**: [spec.md](/home/openclaw/projects/ai-photo-studio-mvp/specs/002-ai-photo-editor-viewer/spec.md)
**Input**: Feature specification from `/specs/002-ai-photo-editor-viewer/spec.md`

## Summary

Deliver an MVP local-first AI photo workflow on `localhost:8088` with four slices: (1) upload + gallery search/sort/metadata, (2) non-destructive editor with compare + undo/redo, (3) export in `png/jpg/webp`, and (4) provider-abstracted generation with deterministic fallback when provider credentials are missing or invalid. Keep architecture simple: React + Vite + TypeScript frontend, FastAPI backend, SQLite metadata, local filesystem for binaries, Docker Compose as canonical runtime.

## Technical Context

**Language/Version**: TypeScript (frontend), Python 3.11 (backend)  
**Primary Dependencies**: React, Vite, FastAPI, Pydantic, SQLAlchemy, Pillow  
**Storage**: SQLite for metadata; local filesystem for original/generated binaries and temp export artifacts  
**Testing**: Vitest + React Testing Library (frontend), pytest + FastAPI TestClient (backend), docker-compose smoke checks  
**Target Platform**: Local Docker runtime on developer workstation (Linux/macOS/Windows via Docker Desktop)  
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: Upload-to-gallery visibility <= 2s for typical local files; generation (provider or fallback) visible/error <= 20s p95  
**Constraints**: Single user only, local-first only, non-destructive editing, deterministic fallback, runtime served on port `8088`  
**Scale/Scope**: MVP for ~200 image library, one active editor session at a time, no authentication or multi-tenant concerns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **MVP-First, Demoable Delivery**: PASS. Plan is scoped to mandatory FR-001..FR-017 only; no production-hardening extras.
- **Spec-Driven Execution**: PASS. This plan maps directly to approved spec and acceptance scenarios.
- **CLI-Agent-First Orchestration**: PASS. Artifacts are structured for `/speckit.tasks` task decomposition and incremental verification.
- **Simplicity Over Abstraction**: PASS with bounded abstractions only (generation provider interface required by FR-013).
- **Auditable Work and Decisions**: PASS. Decisions and checkpoints captured in `research.md`, `data-model.md`, and `quickstart.md`.

**Post-Design Re-check**: PASS. No constitution violations introduced by Phase 1 artifacts.

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-photo-editor-viewer/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md              # created later by /speckit.tasks
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── features/
│   │   ├── gallery/
│   │   ├── editor/
│   │   ├── generation/
│   │   └── export/
│   ├── state/
│   └── utils/
└── tests/
    ├── integration/
    └── unit/

infra/
└── docker/
    └── docker-compose.yml
```

**Structure Decision**: Use a web application split (`frontend/`, `backend/`, `infra/`) to align with required local runtime behavior and to keep API/storage responsibilities isolated from UI editing state.

## Phase Plan

### Phase 0 - Research and Decision Lock

1. Lock deterministic fallback algorithm and normalization tuple for FR-015/FR-016.
2. Choose non-destructive edit representation (ordered operation stack + cursor) and preview rendering strategy.
3. Confirm duplicate filename strategy and asset storage layout that prevents overwrite.
4. Confirm minimal metadata indexing approach for case-insensitive AND search.

**Output**: `research.md`

### Phase 1 - Design and Contracts

1. Define data entities and validation rules for assets, metadata, edit sessions, exports, generation.
2. Author API contract for uploads, gallery list/search/sort, metadata patch, export, generation, health.
3. Write local-first quickstart with docker compose run + smoke verification on `localhost:8088`.

**Outputs**: `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

### Phase 2 - Implementation Planning Input (/speckit.tasks)

1. Convert stories to executable tasks grouped by user story priority.
2. Attach verification command/check per task.
3. Sequence backend contract implementation before frontend integration tasks.
4. Reserve final end-to-end smoke lane for full flow: upload -> edit -> compare -> export -> generate.

**Output**: `tasks.md` (next command)

## Story-to-Phase Mapping

- **US1 (P1): Local library upload + gallery search/sort**
  - Backend asset ingest/list/search/sort APIs + SQLite metadata model
  - Frontend gallery ingestion and deterministic sorting UX
  - Verification: upload/list/search/sort contract + UI tests
- **US2 (P1): Non-destructive editing + compare + undo/redo**
  - Frontend session edit stack, preview pipeline, compare toggle
  - Backend remains source-of-truth for immutable originals only
  - Verification: editor state reducer/unit tests + integration flow
- **US3 (P2): Export outputs**
  - Backend export endpoint accepting visible-state payload and format/quality
  - Frontend export modal/download behavior
  - Verification: format matrix tests (`png/jpg/webp`) + error paths
- **US4 (P2): AI generation with provider abstraction + deterministic fallback**
  - Backend provider interface and fallback implementation
  - Frontend generation form and gallery/editor integration
  - Verification: deterministic byte output tests + provider unavailable behavior

## Verification Strategy

- **Contract**: Validate API surface against `contracts/openapi.yaml`.
- **Backend Unit/Integration**: upload validation, duplicate name collision handling, search semantics, deterministic fallback, export format/quality behavior.
- **Frontend Unit/Integration**: gallery filters/sorts, edit stack transitions, compare toggle, generation and export UX states.
- **Smoke**: docker compose up; verify health + primary flow reachable on `http://localhost:8088`.

## Risks and Mitigations

- **Risk**: Client-side edit previews become inconsistent across operations.
  - **Mitigation**: canonical operation ordering and deterministic reducer tests for every operation type.
- **Risk**: Deterministic fallback drifts over time.
  - **Mitigation**: lock normalization rules and golden tests on output hashes.
- **Risk**: Search/sort behavior appears non-deterministic with ties.
  - **Mitigation**: enforce secondary sort by stable asset id and test tie cases.
- **Risk**: Export payload format mismatch between frontend and backend.
  - **Mitigation**: strict schema validation and shared TypeScript types generated from OpenAPI where practical.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
