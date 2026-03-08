# Feature Specification: AI Photo Studio MVP

## 1) Feature Metadata
- Feature Title: AI Photo Studio MVP
- Branch: `001-ai-photo-editor-viewer`
- Status: Clarified for planning
- Input Summary:
  - Source truth: existing MVP spec content in this feature folder.
  - Product intent: single-user local photo workflow for upload, organize, edit, export, and AI image generation.
  - Required constraints: local-first MVP, no auth, SQLite + local filesystem volume, React/Vite/TypeScript frontend, FastAPI backend, Docker Compose served on port `8088`, deterministic mock AI fallback.

## 2) User Scenarios & Testing

### Story 1 (P1): Upload and browse local images
As a user, I want to upload and browse images so I can manage my local collection.

Acceptance scenarios:
1. Given the app is running, when I upload valid `png`, `jpg/jpeg`, or `webp` files, then each file is persisted to the local image volume and appears in the gallery with metadata.
2. Given images exist, when I view the gallery, then I can see items in a visual list/grid with filename, format, dimensions, size, and created time.

### Story 2 (P1): Search and sort gallery assets
As a user, I want to search and sort assets so I can quickly find what I need.

Acceptance scenarios:
1. Given multiple assets with different names/tags/notes, when I search by a matching term, then only matching items are returned.
2. Given multiple assets, when I sort by `created`, `updated`, or `name`, then ordering is deterministic and consistent across repeated requests.

### Story 3 (P1): Non-destructive editing workflow
As a user, I want to edit an image without changing the original file so I can experiment safely.

Acceptance scenarios:
1. Given an opened image in editor view, when I apply crop/rotate/flip/adjustments/filters, then preview updates immediately.
2. Given edits have been applied, when I use undo/redo, then the visual state steps backward/forward through edit history.
3. Given edits exist, when I inspect the original source image, then the original file is unchanged.

### Story 4 (P1): Compare before and after
As a user, I want a before/after comparison so I can evaluate changes.

Acceptance scenarios:
1. Given an edited image, when I toggle or hold compare, then I can clearly view original versus current edited preview.

### Story 5 (P1): Export edited output
As a user, I want to export my current edit so I can use it elsewhere.

Acceptance scenarios:
1. Given an edited image, when I export as `png`, `jpg`, or `webp`, then a downloadable file is produced for the current edit state.
2. Given export format is `jpg` or `webp`, when I set quality, then output reflects the selected quality parameter.

### Story 6 (P1): AI image generation with provider abstraction and fallback
As a user, I want to generate images with a provider-backed API and a deterministic fallback for offline/dev reliability.

Acceptance scenarios:
1. Given valid generation input (`prompt`, `size`, optional `style`, optional provider override), when generation succeeds, then a generated image and metadata are returned and shown in gallery.
2. Given provider credentials/config are missing, when generation is requested, then the system returns deterministic mock output and stable metadata.
3. Given provider selection is configured by environment, when backend starts, then active provider resolution follows configuration.

### Story 7 (P2): Local run and service observability
As a user, I want simple local startup and basic API visibility.

Acceptance scenarios:
1. Given Docker is available, when I run `docker compose up --build`, then app is reachable at `http://localhost:8088`.
2. Given backend is running, when I call `GET /api/health`, then it returns an OK status.
3. Given backend is running, when I open API docs endpoint, then OpenAPI docs are reachable.

## 3) Edge Cases
- Upload rejects unsupported file types with a clear validation error.
- Upload handles duplicate filenames without overwriting existing source files.
- Search with empty query returns unfiltered results.
- Sort behavior for ties is deterministic (stable secondary key).
- Undo/redo boundaries are handled safely (no crash at first/last history state).
- Export without edits still succeeds from original state.
- AI generation input validation handles missing prompt or invalid size.
- Deterministic mock output remains stable for identical inputs across runs.

## 4) Functional Requirements
- FR-001: The system must run as a local-first web app with frontend and backend available through Docker Compose on port `8088`.
- FR-002: The system must support a single-user workflow without authentication or authorization.
- FR-003: The frontend must use React + Vite + TypeScript.
- FR-004: The backend must use FastAPI with SQLite for metadata persistence.
- FR-005: The system must persist source and generated image files on a local filesystem volume.
- FR-006: The system must accept image uploads for `png`, `jpg/jpeg`, and `webp`.
- FR-007: The system must create a persisted asset record for each uploaded/generated image.
- FR-008: The gallery must display uploaded and generated assets with core metadata (filename, format, dimensions, size, created/updated timestamps, provider when generated).
- FR-009: The gallery must support search across filename, tags, and notes.
- FR-010: The gallery must support sorting by created date, updated date, and name.
- FR-011: The editor must support zoom and pan for the currently opened image.
- FR-012: The editor must support crop with explicit apply/cancel behavior.
- FR-013: The editor must support rotate in 90-degree steps and horizontal/vertical flip.
- FR-014: The editor must support brightness, contrast, and saturation adjustments.
- FR-015: The editor must support preset filters including none/warm/cool/mono/vivid.
- FR-016: Edit operations must be non-destructive; original source files must not be mutated.
- FR-017: The editor must maintain ordered operation history with undo/redo.
- FR-018: The editor must provide before/after comparison between original and current edited state.
- FR-019: The system must export current edit state to `png`, `jpg`, or `webp`.
- FR-020: Export for `jpg` and `webp` must support quality configuration.
- FR-021: The AI generation API must accept `prompt`, `size`, optional `style`, and optional provider override.
- FR-022: AI provider integration must be abstracted to support `nano-banana` and `gpt-image` implementations.
- FR-023: Active AI provider must be selectable by environment configuration.
- FR-024: If AI provider credentials/config are unavailable, generation must use deterministic mock output.
- FR-025: The backend must expose `GET /api/health` and an OpenAPI docs endpoint.
- FR-026: Tags are stored as simple comma-separated strings (no taxonomy system in MVP).
- FR-027: Exported derivatives are generated on demand and are not persisted unless explicitly downloaded by the user.
- FR-028: The MVP must not write back EXIF metadata to source images.

## 5) Key Entities
- ImageAsset:
  - Represents an uploaded or AI-generated source image.
  - Core fields: `id`, `filename`, `storage_path`, `source_type` (`upload`|`generated`), `format`, `width`, `height`, `size_bytes`, `created_at`, `updated_at`, `provider?`, `tags`, `notes`.
- EditSession:
  - Represents current editable state for a selected ImageAsset.
  - Core fields: `image_asset_id`, `operation_history[]`, `history_index`, `current_preview_state`.
- EditOperation:
  - Represents one non-destructive edit step.
  - Core fields: `type` (crop/rotate/flip/adjust/filter), `params`, `created_at`, `sequence`.
- ExportRequest:
  - Represents a requested render from current edit state.
  - Core fields: `image_asset_id`, `target_format`, `quality?`, `requested_at`.
- AIGenerationRequest:
  - Represents a generation input request.
  - Core fields: `prompt`, `size`, `style?`, `provider_override?`.
- AIGenerationResult:
  - Represents generation output persisted as an ImageAsset.
  - Core fields: `image_asset_id`, `provider_used`, `is_mock`, `seed_or_hash`, `created_at`.

## 6) Success Criteria
- SC-001: A user can complete upload -> gallery browse -> open editor -> edit -> export in one session without page reload.
- SC-002: Original uploaded/generated source files remain unchanged after any editing and undo/redo activity.
- SC-003: Search and sort produce repeatable, deterministic results for identical inputs.
- SC-004: AI generation succeeds in both provider-configured mode and missing-credentials mode (deterministic mock fallback).
- SC-005: Local startup via Docker Compose exposes the product at `http://localhost:8088` and backend health/docs endpoints are reachable.

## 7) Clarifications
### 2026-03-08 Clarify Decisions (MVP defaults)
- Asset storage and duplicate filenames:
  - Preserve the user-visible `filename` value in metadata.
  - Always write files to unique storage paths so uploads or generations with the same filename never overwrite prior assets.
  - Filename uniqueness in storage is implementation-defined; product requirement is no overwrite and stable retrieval by asset id.
- Search semantics:
  - Search is case-insensitive substring matching over `filename`, `tags`, and `notes`.
  - A single query string is split on whitespace; all non-empty terms must match somewhere across those fields (AND semantics across terms).
  - No fuzzy matching, stemming, regex, or quoted-phrase parsing in MVP.
- Tags/notes editing scope:
  - Tags and notes are editable only at the asset metadata level (gallery/detail context), not as part of edit operation history.
  - Tags remain plain comma-separated text; no suggestions, taxonomy, or bulk edit in MVP.
- Editor history persistence scope:
  - Undo/redo history is session-scoped (current browser tab session).
  - History is not persisted across page reloads, browser restarts, or reopening an asset later.
  - Persisting/restoring edit stacks is out of scope for MVP.
- AI generation sizes and styles:
  - Supported `size` values are exactly `1024x1024`, `1024x1536`, and `1536x1024`.
  - `style` is optional free text passed through when provider supports it; unsupported styles do not hard-fail provider calls.
  - UI should offer a small preset style list for demoability plus optional custom text input.
- Deterministic mock fallback behavior:
  - Mock mode deterministically derives output from normalized input tuple: (`prompt`, `size`, `style`, `provider_override`).
  - Identical normalized inputs must yield identical mock image bytes and metadata (`is_mock`, seed/hash, dimensions) across runs on the same code version.
  - Changing any input field must change the deterministic seed/hash.
- Export behavior and filenames:
  - Export always returns a downloadable file and does not create a new ImageAsset record.
  - Default export filename: `<original-base>-edited.<target-ext>`.
  - If the client environment detects a download name conflict, it may append a numeric suffix; conflict resolution UX is delegated to browser behavior in MVP.
- Gallery pagination:
  - No pagination in MVP.
  - Gallery returns and renders the full asset list for the single-user local experiment scope.
  - Virtualization/infinite scroll/server pagination are explicitly out of scope.
- Single-user assumptions:
  - Exactly one local user context is assumed.
  - No account model, no per-user data partitioning, no concurrent edit conflict handling.
- Failure and validation behavior:
  - Validation failures return user-correctable messages (unsupported type, missing prompt, invalid size, invalid quality range).
  - Failed upload/generation/export operations are all-or-nothing at the request level (no partial success payloads in MVP).
  - On backend/provider failure, return a clear error response and preserve existing assets/history state.

## 8) Non-Goals and Constraints
- Non-goals:
  - Multi-user collaboration.
  - Authentication/authorization.
  - Cloud object storage.
  - Real-time collaborative editing.
- Constraints:
  - Local-first MVP only.
  - Backend: FastAPI + SQLite.
  - Frontend: React + Vite + TypeScript.
  - Storage: local filesystem volume.
  - Runtime: Docker Compose on port `8088`.
