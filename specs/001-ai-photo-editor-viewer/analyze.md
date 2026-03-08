# Analyze: 001-ai-photo-editor-viewer

Date: 2026-03-08
Scope reviewed: constitution, `spec.md`, `plan.md`, `tasks.md`, backend/frontend/runtime code.

## 1) Consistency checks (spec vs plan vs tasks vs code)

### A. Matches (consistent)
- Runtime base contract mostly aligned:
  - Compose exposes frontend on `8088` (`docker-compose.yml`).
  - Backend has `GET /api/health` (`backend/app/api/routes.py`).
  - No auth implementation present (consistent with MVP no-auth constraint).
- Backend upload/storage safety implemented:
  - Type restrictions + empty-file rejection (`backend/app/services/storage.py`).
  - Collision-safe stored names via UUID (`backend/app/services/storage.py`).
- Frontend editor core MVP behaviors exist:
  - Non-destructive client-side edit/export pipeline (`frontend/src/components/EditorPanel.tsx`, `frontend/src/editor/render.ts`).
  - Undo/redo and compare-hold controls (`frontend/src/components/EditorPanel.tsx`).

### B. Mismatches (inconsistent)
- AI generation API contract mismatch with clarified spec:
  - Spec/plan/tasks require `size` enum (`1024x1024|1024x1536|1536x1024`).
  - Code still uses `width`/`height` in schema and route (`backend/app/schemas/image.py`, `backend/app/api/routes.py`).
  - Frontend still posts `width`/`height` (and hardcodes `1024x768`, which is not an allowed clarified size) (`frontend/src/App.tsx`, `frontend/src/api/client.ts`).
- Search semantics mismatch:
  - Clarified behavior requires whitespace-split AND semantics.
  - Code performs single-term OR `ilike` across fields (`backend/app/api/routes.py`).
- Sort determinism gap:
  - Plan/tasks require stable tie-break by `id`.
  - Code sorts by one column only (`backend/app/api/routes.py`).
- Deterministic mock metadata gap:
  - Clarification requires deterministic tuple normalization and stable seed/hash metadata.
  - Mock digest currently uses prompt only; no seed/hash returned/persisted (`backend/app/services/ai_providers.py`, `backend/app/models/image.py`, `backend/app/schemas/image.py`).
- Docs/runtime reachability mismatch:
  - Quickstart claims docs at `http://localhost:8088/docs`.
  - Nginx only proxies `/api/*`; `/docs` is not proxied (`frontend/nginx.conf`, `specs/001-ai-photo-editor-viewer/quickstart.md`).
  - README claims generic `/docs` docs path that is misleading under compose (`README.md`).
- Test coverage mismatch:
  - Tasks require validation for search semantics, size enum validation, deterministic metadata, duplicate filenames.
  - Current backend tests only cover health/upload/list basic and generate smoke (`backend/tests/test_api.py`).
  - Frontend tests only render smoke (`frontend/src/App.test.tsx`).

## 2) Coverage gaps

### Functional gaps vs FR/SC
- FR-009 clarified search semantics not implemented (AND-term search).
- FR-010 deterministic ordering for ties not guaranteed.
- FR-021 clarified AI input contract (`size`) not implemented.
- FR-024 deterministic mock fallback metadata requirements incomplete (no seed/hash; tuple normalization incomplete).
- Story 2 metadata search relevance is partial because tags/notes edit UI is missing (backend supports patch endpoint, UI does not expose editing).
- Story 6 demoability is partial: provider abstraction exists, but contract + deterministic metadata behavior are not at clarified level.
- SC-003 and SC-004 are not demonstrably validated by tests.
- SC-005 docs reachability under compose is ambiguous/inaccurate in docs.

### Verification gaps
- `make test` currently fails in this environment because `pytest` is missing (command output: `pytest: command not found`).
- No evidence captured yet for `make build` and full `docker compose up --build` smoke workflow.

## 3) Overengineering risks (MVP-first guardrails)
- Adding server-side persistent edit history would violate clarified session-scoped history and is unnecessary now.
- Implementing pagination/virtualized gallery now would violate clarified non-goals for MVP.
- Building provider-specific advanced style validation now is unnecessary; clarified spec allows passthrough optional style text.
- Expanding metadata model into normalized tag taxonomy would violate FR-026 and add avoidable complexity.

## 4) Blocker vs non-blocker classification

### Blockers (must resolve before implementation wave exit/release gate)
1. AI input contract migration to `size` enum across backend + frontend.
2. Search semantics update to whitespace-split AND logic.
3. Deterministic sort tie-break (`id`) implementation.
4. Deterministic mock seed/hash behavior and metadata response/persistence alignment.
5. Runtime/docs correction for docs endpoint under compose (either proxy route or docs wording adjusted to actual reachable path).
6. Verification backlog for critical behaviors (backend + frontend targeted tests).
7. Local test environment readiness (`pytest` missing) preventing acceptance validation.

### Non-blockers (can follow blockers but still needed)
1. Debounced search input (performance/usability, not core correctness blocker).
2. Crop cancel UX wording/behavior polish.
3. Expanded editor UI tests for quality slider behavior (important for confidence but after contract-critical fixes).
4. README marketing language cleanup beyond strict correctness.

## 5) Recommended execution order for remaining tasks

1. **Unblock validation environment first**
- Install backend test tooling (`pytest`) and confirm `make test` can execute.

2. **Backend contract hardening (Workstreams A+B critical path)**
- Replace generate schema/route from `width`+`height` to `size` enum.
- Implement clarified search semantics and deterministic sort tie-break.
- Implement deterministic mock normalization tuple (`prompt`, `size`, `style`, `provider_override`) and return/persist seed/hash + mock indicator.
- Add rollback-safe handling where DB/file write consistency can break.

3. **Frontend contract alignment (Workstream C critical subset)**
- Update API client and UI generator form to send allowed `size` values; remove hardcoded unsupported `1024x768`.
- Add tags/notes editing UI wired to existing `PATCH /api/images/{id}`.

4. **Runtime/docs correction (Workstream E)**
- Decide docs strategy:
  - Option A: proxy `/docs` + `/openapi.json` via nginx on `8088`, or
  - Option B: document backend docs as direct backend address only.
- Align README + quickstart with actual runtime behavior.

5. **Verification wave (Workstream F)**
- Backend tests: search semantics, sort tie-break, size validation, deterministic mock metadata, duplicate filename uploads.
- Frontend tests: generation payload contract, tags/notes flow, editor export quality/compare/undo-redo boundaries.
- Run and capture: `make test`, `make build`, `docker compose up --build` smoke checks.

6. **Final acceptance pass**
- Re-evaluate `checklist.md` against demonstrable evidence only.

## 6) MVP/no-auth/local-first conformance note
- Current implementation remains local-first and no-auth as required.
- Main risk is not scope creep; it is spec-contract drift and insufficient validation evidence.
