# Research: AI Photo Studio MVP (Local-First Single User)

## Scope and Inputs

- Spec source: [spec.md](/home/openclaw/projects/ai-photo-studio-mvp/specs/002-ai-photo-editor-viewer/spec.md)
- Constraint source: [constitution.md](/home/openclaw/projects/ai-photo-studio-mvp/.specify/memory/constitution.md)
- Background context used: [reference-plan.md](/home/openclaw/projects/ai-photo-studio-mvp/.tmp/reference-plan.md)

## Decision 1: Runtime Topology

- **Decision**: Keep a two-service local topology (React frontend + FastAPI backend) orchestrated with Docker Compose, exposed on host port `8088`.
- **Why**: Satisfies FR-001 and constitution runtime constraint with minimal operational overhead.
- **Alternatives considered**:
  - Monolithic backend-served templates: rejected to preserve fast frontend iteration and clear API contracts.
  - Bare local scripts only: rejected because spec asks for stable local runtime behavior.

## Decision 2: Asset Persistence and Filename Collisions

- **Decision**: Persist binaries under local filesystem with UUID-based stored filenames while preserving original filename in metadata.
- **Why**: Guarantees FR-003 (no overwrite on duplicate names) and keeps filesystem behavior deterministic.
- **Alternatives considered**:
  - Append incrementing suffix to original names: workable but harder to keep race-safe and deterministic.
  - Store binary blobs in SQLite: rejected for MVP simplicity and filesystem interoperability.

## Decision 3: Metadata and Search/Sort

- **Decision**: Use SQLite table for asset metadata with normalized search text column; search uses case-insensitive AND semantics over whitespace terms. Sort by chosen key + stable tie-break (`asset_id`).
- **Why**: Meets FR-005/FR-006 with deterministic output and simple implementation.
- **Alternatives considered**:
  - Full-text extension only: unnecessary complexity for MVP scale (~200 assets).

## Decision 4: Non-Destructive Editing Model

- **Decision**: Keep edit history session-scoped in frontend state as ordered operations + cursor (`undo/redo`), never mutating source binary.
- **Why**: Directly satisfies FR-007/FR-009 and assumption that edit session need not persist reloads.
- **Alternatives considered**:
  - Persist edit graph server-side: rejected as out of MVP scope and adds sync complexity.

## Decision 5: Preview and Compare

- **Decision**: Render preview from original + operation stack in deterministic order; compare mode toggles between original and current rendered state.
- **Why**: Meets FR-010 with minimal complexity and no original mutation risk.
- **Alternatives considered**:
  - Snapshot-per-operation caching: deferred unless performance shows need.

## Decision 6: Export Pipeline

- **Decision**: Frontend sends current visible state payload (or reference + ops) with requested format/quality to backend export endpoint; backend produces downloadable file stream.
- **Why**: Ensures consistent encoding and satisfies FR-011/FR-012.
- **Alternatives considered**:
  - Pure client-side export: less consistent across browsers; backend path is more testable.

## Decision 7: Generation Provider Abstraction + Deterministic Fallback

- **Decision**: Define backend `GenerationProvider` interface and route requests through provider resolver. If provider config invalid/missing, use local deterministic fallback renderer.
- **Why**: Required by FR-013/FR-015/FR-016 and keeps external integration optional.
- **Fallback determinism spec**:
  - Normalize tuple: `(prompt_normalized, size, style_normalized_or_empty)`
  - Compute seed from SHA-256 of tuple
  - Generate deterministic image bytes from seeded procedural renderer
  - Persist generated output as normal asset
- **Alternatives considered**:
  - Random placeholder image: rejected (fails FR-016).

## Decision 8: Testing Minimums

- **Decision**: Keep tests focused on acceptance-critical behavior.
- **Backend**:
  - upload validation and collision handling
  - list/search/sort determinism
  - deterministic fallback hash stability
  - export format/quality matrix
- **Frontend**:
  - gallery search/sort interactions
  - edit stack undo/redo + compare toggle
  - generation/export UI states
- **Smoke**:
  - local health endpoint and UI reachability on `localhost:8088`

## Open Questions Resolved for MVP

- **Edit history persistence across reload**: Not required (spec assumption).
- **Export output auto-ingest to library**: Not required (spec assumption).
- **Auth and multi-user behavior**: Explicitly out of scope per constitution and spec assumptions.
