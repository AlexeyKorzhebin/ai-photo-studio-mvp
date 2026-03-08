# Data Model: AI Photo Studio MVP

## Overview
MVP persists only asset/generation metadata in SQLite. Edit history is transient in frontend session state.

## Persisted Entities (SQLite)

### 1) ImageAsset (`images`)
Represents one source image (uploaded or AI-generated).

Fields:
- `id` (int, PK)
- `filename` (string, required)
- `stored_name` (string, required, unique)
- `mime_type` (string, required)
- `size_bytes` (int, required)
- `width` (int, required)
- `height` (int, required)
- `source_type` (enum-like string: `upload` | `generated`, required)
- `provider` (string, nullable; generation provider used)
- `prompt` (text, nullable; generation prompt when `generated`)
- `tags` (text, nullable; comma-separated user text)
- `notes` (text, nullable)
- `created_at` (datetime, required)
- `updated_at` (datetime, required)

Planned MVP extension fields for generation determinism:
- `is_mock` (bool, default false)
- `seed_hash` (string, nullable)
- `generation_size` (string, nullable; e.g., `1024x1024`)
- `generation_style` (string, nullable)

Constraints/behavior:
- `stored_name` is UUID-based to prevent overwrite collisions.
- Duplicate `filename` values are allowed.
- Original file bytes are immutable after creation.

## Non-Persisted Runtime Entities

### 2) EditState (frontend session)
Current visual state for selected image.

Fields:
- `rotate` (number; 90-degree step ops)
- `flipX` (boolean)
- `flipY` (boolean)
- `brightness` (number)
- `contrast` (number)
- `saturation` (number)
- `filter` (`none` | `warm` | `cool` | `mono` | `vivid`)
- `crop` ({ `x`, `y`, `width`, `height` } | `null`, percentage space)

### 3) EditHistory (frontend session)
Undo/redo timeline of `EditState` snapshots.

Fields:
- `history` (`EditState[]`)
- `index` (current pointer)

Rules:
- Session-scoped only; resets on reload/reopen.
- No backend table/API for history in MVP.

### 4) AIGenerationRequest (API payload)
- `prompt` (required)
- `size` (required enum: `1024x1024`, `1024x1536`, `1536x1024`)
- `style` (optional free text)
- `provider` (optional override)

### 5) AIGenerationResult (API response + persisted asset)
- `image` (`ImageAsset` response view)
- `provider_used` (string)
- `fallback_used` (boolean)
- `seed_hash` (string for deterministic fallback tracing)

## Relationships
- `ImageAsset` is the only persisted root entity.
- A generated image is represented as another `ImageAsset` row (`source_type=generated`).
- `EditState` and `EditHistory` reference a selected `ImageAsset` in frontend memory only.

## Lifecycle Summary
1. Upload/generate creates one `ImageAsset` row + one file in local volume.
2. Gallery/search/sort reads `ImageAsset` rows.
3. Tags/notes update mutates existing `ImageAsset` row.
4. Editing mutates only in-memory `EditState`/`EditHistory`.
5. Export emits downloadable bytes only; no new `ImageAsset` row.
