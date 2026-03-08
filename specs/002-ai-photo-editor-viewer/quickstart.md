# Quickstart: AI Photo Studio MVP (Local-First)

## Goal

Run the full MVP locally and validate the core workflow on `http://localhost:8088`.

## Prerequisites

- Docker + Docker Compose
- Open local terminal in repository root: `/home/openclaw/projects/ai-photo-studio-mvp`

## Environment

Create `.env` values used by compose (exact file location depends on final compose setup):

```bash
APP_PORT=8088
DATABASE_URL=sqlite:///./data/app.db
ASSET_STORAGE_DIR=./data/assets
EXPORT_STORAGE_DIR=./data/exports
GENERATION_PROVIDER=auto
# Optional provider key(s) for non-fallback generation
# OPENAI_API_KEY=...
```

## Start

```bash
docker compose up --build
```

Expected:

- Frontend reachable at `http://localhost:8088`
- API health route reachable at `http://localhost:8088/api/health`

## Smoke Verification

1. Upload 2-3 valid files (`png/jpg/webp`) and one invalid file.
2. Confirm valid files appear in gallery and invalid file returns clear error.
3. Add metadata notes/tags to one image.
4. Search gallery with mixed-case terms and verify expected AND matches.
5. Change sort key/order and verify deterministic ordering for repeated refresh.
6. Open an image in editor and apply crop + rotate + tonal adjustment.
7. Use undo/redo and confirm state transitions are correct.
8. Toggle compare mode and verify original vs edited view.
9. Export current state as `png`, `jpg` (quality 80), and `webp` (quality 80).
10. Submit generation request with one allowed size; verify result appears in gallery/editor flow.
11. Disable external provider config and repeat same generation request twice; verify fallback output is byte-identical.

## Test Commands (target)

```bash
# backend
pytest backend/tests/unit backend/tests/integration

# frontend
npm --prefix frontend test

# optional contract checks
# npm --prefix frontend run test:contract
# pytest backend/tests/contract
```

## Stop and Cleanup

```bash
docker compose down
```

Optional cleanup of local generated data:

```bash
rm -rf data/assets data/exports data/app.db
```
