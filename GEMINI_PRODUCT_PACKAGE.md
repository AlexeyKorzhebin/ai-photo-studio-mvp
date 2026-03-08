# AI Photo Studio MVP: Complete Product & Engineering Package

This document serves as the single source of truth for the AI Photo Studio MVP, bridging product vision, design specifications, and engineering requirements.

---

## 1. PRD-Lite: Core Vision
**Objective:** A lightweight, local-first AI photo manipulation tool that allows users to upload images and apply styles using selectable AI providers.
- **Target Users:** Creative hobbyists and developers testing AI image workflows.
- **Success Metric:** Successful end-to-end transformation (Upload -> AI Process -> Download) in under 30 seconds.
- **Scope Constraints:** No user accounts, no cloud storage (local volume only), single-session focus.

---

## 2. UX Flows
### Flow A: The "Magic" Transformation (Happy Path)
1. **Landing:** User opens `localhost:8088`. Sees a clean "Drop Zone".
2. **Upload:** User drags a `.jpg` or `.png`. Backend saves to local volume and generates a unique `TaskID`.
3. **Configuration:** User selects a "Style Preset" (e.g., "Cinematic", "Sketch") and clicks "Generate".
4. **Processing:** A progress overlay appears. Frontend polls the backend for status.
5. **Result:** The processed image is displayed side-by-side with the original.
6. **Action:** User downloads the result or restarts.

---

## 3. Screen Map
- **[Main Dashboard]**
    - `Header`: Logo + AI Provider Status Indicator (Nano-Banana/GPT-Image).
    - `Upload Area`: Large drag-and-drop zone with file validation.
    - `Gallery Rail`: Thumbnails of the last 5 processed images (stored in current session memory).
- **[Studio Workspace]** (Triggered after upload)
    - `Left Pane`: Original Image Preview.
    - `Right Pane`: Configuration (Preset dropdown, Strength slider).
    - `Primary Action`: "Generate Image" button.
- **[Processing Modal]**
    - Spinner + Dynamic status messages ("Uploading...", "AI is thinking...", "Saving...").
- **[Result View]**
    - High-res comparison toggle.
    - Download (PNG) + "New Studio" button.

---

## 4. Design System (Tokens & Components)
**Theme:** Dark Mode (Pro-Studio Aesthetic)
- **Colors:**
    - Background: `#0F172A` (Slate-900)
    - Surface: `#1E293B` (Slate-800)
    - Primary: `#6366F1` (Indigo-500)
    - Accent: `#10B981` (Emerald-500) for success/completion.
- **Typography:**
    - Headings: `Inter`, Bold.
    - Body: `Inter`, Regular.
- **Components:**
    - `Button`: Rounded-lg, subtle hover transition (0.2s).
    - `Card`: Border `Slate-700`, subtle outer glow on hover.
    - `Indicator`: Pulsing dot for "AI Processing" state.

---

## 5. API Contract Proposal (FastAPI)

### Image Management
- `POST /api/upload`: Receives multipart/form-data. Returns `image_id` and `dimensions`.
- `GET /api/images/{image_id}`: Returns the raw image file from the local volume.

### AI Processing
- `POST /api/process`:
    - Body: `{ "image_id": "uuid", "provider": "nano-banana|gpt-image", "preset": "str" }`
    - Returns: `{ "task_id": "uuid" }`
- `GET /api/status/{task_id}`:
    - Returns: `{ "status": "pending|processing|completed|failed", "result_url": "str|null" }`

### System
- `GET /api/health`: Returns active provider and volume write-status.

---

## 6. QA Checklist
- [ ] **Upload Integrity:** Verify files > 10MB are rejected with a clear error.
- [ ] **Provider Switching:** Change `AI_PROVIDER` env var and verify the backend routes requests correctly.
- [ ] **Mock Fallback:** Ensure that if `MOCK_AI=true`, the system "processes" for 3 seconds and returns a grayscale version of the original.
- [ ] **Volume Persistence:** Restart Docker container and verify previously processed images are still accessible via `/api/images/{id}`.
- [ ] **UI Responsiveness:** Ensure the "Generate" button disables during active tasks to prevent duplicate submissions.

---

## 7. Release Checklist
1. **Environment:** Create `.env.example` with `AI_PROVIDER`, `API_KEY`, and `IMAGE_VOLUME_PATH`.
2. **Docker:** Verify `Dockerfile` multi-stage build (Vite build -> FastAPI static mount).
3. **Network:** Confirm port mapping `8088:8000` is explicit in `docker-compose.yml`.
4. **Volumes:** Ensure `/app/data/images` is mapped to a local host folder to prevent data loss on container stop.
5. **Final Smoke Test:** Run `docker-compose up`, upload one image, and confirm it appears in the host filesystem.

---

## 8. Top 10 Implementation Recommendations (Codex Stream)

1. **Adapter Pattern:** Create a `BaseAIProvider` class in FastAPI. Implement `NanoBananaProvider` and `GPTImageProvider` as subclasses for easy switching.
2. **React Query for Polling:** Use `useQuery` with a `refetchInterval` to handle the status polling of the `task_id`.
3. **Zustand for State:** Keep the "Current Session Gallery" in a lightweight Zustand store to avoid prop-drilling.
4. **Shadcn/UI + Tailwind:** Use these for the frontend to hit the "Pro" look with zero custom CSS overhead.
5. **Async Tasks:** Use Python `BackgroundTasks` in FastAPI for the AI call so the initial request returns the `task_id` immediately.
6. **Pydantic Schemas:** Strictly define the API request/response shapes to ensure frontend TS types are 1:1.
7. **Graceful Error UI:** If the AI provider returns a 500, show a "Provider Busy" toast instead of crashing the Studio view.
8. **Vite Proxy:** Configure `vite.config.ts` to proxy `/api` to `localhost:8000` during development to avoid CORS headaches.
9. **Image Optimization:** Use CSS `object-fit: contain` for previews to handle different aspect ratios (portrait/landscape) elegantly.
10. **Volume Initialization:** Add a startup script in FastAPI to ensure the image upload directory exists (`os.makedirs`) before the first upload attempt.
