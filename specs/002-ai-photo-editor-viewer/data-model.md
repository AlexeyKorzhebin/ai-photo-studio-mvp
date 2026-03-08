# Data Model: AI Photo Studio MVP

## Entity: ImageAsset

- **Purpose**: Canonical stored item for uploaded/generated images shown in gallery.
- **Fields**:
  - `id` (UUID, primary key)
  - `origin_type` (`upload` | `generated`)
  - `original_filename` (string, required)
  - `stored_filename` (string, required, unique)
  - `mime_type` (`image/png` | `image/jpeg` | `image/webp`)
  - `width` (int, >0)
  - `height` (int, >0)
  - `byte_size` (int, >0)
  - `created_at` (datetime)
  - `updated_at` (datetime)
- **Constraints**:
  - `stored_filename` is unique and never user-controlled.
  - Source binary is immutable once saved.

## Entity: ImageMetadata

- **Purpose**: User-maintained searchable text for an asset.
- **Fields**:
  - `asset_id` (UUID, PK/FK -> ImageAsset.id)
  - `tags` (string array serialized for MVP)
  - `notes` (text)
  - `search_text_normalized` (text, derived lowercase field)
  - `updated_at` (datetime)
- **Constraints**:
  - One metadata record per asset.
  - `search_text_normalized` updates whenever tags/notes/filename source terms change.

## Entity: EditSession (Frontend-only)

- **Purpose**: Session-scoped non-destructive working state for one selected asset.
- **Fields**:
  - `session_id` (UUID)
  - `asset_id` (UUID)
  - `operations` (ordered array of edit operations)
  - `cursor` (int; points to active prefix of operations)
  - `compare_mode` (bool)
  - `last_preview_hash` (string, optional)
- **Constraints**:
  - `0 <= cursor <= operations.length`
  - Undo decrements cursor; redo increments cursor.
  - Session is discarded on app reload.

## Value Object: EditOperation

- **Purpose**: Single non-destructive transform command.
- **Variants**:
  - `crop`: `{ x, y, width, height }`
  - `rotate`: `{ degrees }` (MVP supports 90-degree increments)
  - `flip`: `{ axis: "horizontal" | "vertical" }`
  - `tonal`: `{ brightness, contrast, saturation }`
  - `filter`: `{ preset }`
- **Rules**:
  - Applied in array order from index `0` to `cursor-1`.
  - Validation rejects invalid bounds/values.

## Entity: ExportRequest

- **Purpose**: Request to render current visible state as downloadable output.
- **Fields**:
  - `asset_id` (UUID)
  - `operations` (EditOperation[])
  - `format` (`png` | `jpg` | `webp`)
  - `quality` (int 1-100, optional; required for `jpg`/`webp`)
- **Constraints**:
  - Reject when selected asset does not exist.
  - Ignore `quality` for `png`.

## Entity: GenerationRequest

- **Purpose**: User prompt payload for AI generation.
- **Fields**:
  - `prompt` (string, required, trimmed)
  - `size` (`1024x1024` | `1024x1536` | `1536x1024`)
  - `style` (string, optional)
  - `provider` (string, optional)
- **Constraints**:
  - `size` must be one of FR-014 values.
  - Empty prompt rejected with validation error.

## Entity: GeneratedArtifact

- **Purpose**: Result of generation job linked into normal gallery workflow.
- **Fields**:
  - `asset_id` (UUID, FK -> ImageAsset.id)
  - `provider_used` (string; e.g., `openai`, `fallback`)
  - `deterministic_key` (string; set for fallback path)
  - `created_at` (datetime)
- **Constraints**:
  - When provider fallback is used, `deterministic_key` is required.

## Relationships

- `ImageAsset 1:1 ImageMetadata`
- `ImageAsset 1:0..1 GeneratedArtifact`
- `ImageAsset 1:N EditSession` (session-scoped, not persisted)

## State Transitions

- **Asset lifecycle**: `ingested -> listed -> selected -> (edited in session)* -> exported?`
- **Generation lifecycle**: `requested -> provider_selected -> generated_or_error -> ingested_asset`
- **Edit session lifecycle**: `created -> operations_mutate_cursor -> compare_toggle -> discarded`
