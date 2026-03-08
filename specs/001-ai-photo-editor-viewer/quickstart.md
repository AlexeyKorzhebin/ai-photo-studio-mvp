# Quickstart: Local MVP Run and Verification

## Prerequisites
- Docker + Docker Compose available locally.
- Working directory: repository root.

## 1) Start the stack
```bash
cp .env.example .env
docker compose up --build
```

Expected:
- Frontend reachable at `http://localhost:8088`.
- Backend reachable behind frontend `/api` path.

## 2) Basic smoke checks
Open in browser:
- App UI: `http://localhost:8088`
- API docs: `http://localhost:8088/docs`

CLI checks:
```bash
curl -s http://localhost:8088/api/health
```
Expected response:
```json
{"status":"ok"}
```

## 3) MVP demo flow verification
1. Upload 2-3 files (`png`, `jpg`, `webp`) from UI.
2. Confirm gallery shows metadata (filename, format/type, dimensions, size, created time).
3. Search by filename/tag/note fragments; verify term-based filtering behavior.
4. Sort by Created, Updated, and Name; repeat same request and confirm deterministic ordering.
5. Open an asset in editor and apply:
   - rotate, flip, brightness/contrast/saturation changes
   - preset filter
   - crop apply/cancel
6. Verify undo/redo boundaries (first and last states do not crash).
7. Hold compare control and confirm original vs edited preview changes.
8. Export as PNG, JPG, and WEBP:
   - filename format `<original-base>-edited.<ext>`
   - quality control affects JPG/WEBP only
9. Generate an AI image using valid prompt and one allowed size.
10. Clear provider credentials in `.env` and repeat generation; confirm deterministic mock fallback path still returns a gallery asset.

## 4) Non-destructive verification
- Reopen original image from gallery after edits/exports.
- Confirm original source appearance is unchanged.

## 5) Stop the stack
```bash
docker compose down
```

Optional cleanup (remove volume data):
```bash
docker compose down -v
```
