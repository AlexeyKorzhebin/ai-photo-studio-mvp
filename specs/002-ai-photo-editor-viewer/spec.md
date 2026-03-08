# Feature Specification: AI Photo Studio MVP (Local-First Single User)

**Feature Branch**: `002-ai-photo-editor-viewer`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "Build a fresh AI Photo Studio MVP specification for a local-first single-user photo workflow. Use branch short-name ai-photo-editor-viewer if a short-name must be derived. The spec should cover upload, gallery browse/search/sort, non-destructive editing, before/after compare, export, AI image generation with provider abstraction and deterministic fallback, and local runtime on port 8088."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build a Local Photo Library (Priority: P1)

As a single local user, I can upload images into a personal library and immediately browse them in a gallery so I can manage my photos in one place.

**Why this priority**: Without reliable ingest and gallery access, no downstream editing or generation workflow is useful.

**Independent Test**: Upload a mixed set of supported image files and verify they appear in the gallery with searchable metadata and stable sort behavior.

**Acceptance Scenarios**:

1. **Given** the app is running locally, **When** I upload valid image files, **Then** each file is stored without overwriting existing files and appears in the gallery.
2. **Given** a populated gallery, **When** I search by filename terms or metadata text, **Then** only matching images are shown.
3. **Given** a populated gallery, **When** I change sort order, **Then** images are ordered consistently and repeatably.

---

### User Story 2 - Edit Without Losing Originals (Priority: P1)

As a single local user, I can perform non-destructive edits and compare before/after views so I can iterate confidently without altering my source image.

**Why this priority**: Safe iterative editing is core product value and must protect original files.

**Independent Test**: Open an uploaded image, apply multiple edits, use undo/redo, and confirm compare mode reflects original versus current edited state.

**Acceptance Scenarios**:

1. **Given** an image is open in the editor, **When** I apply crop, rotate, flip, tonal adjustments, or filters, **Then** the preview updates while the original source remains unchanged.
2. **Given** a sequence of edits in the current session, **When** I use undo and redo controls, **Then** the image state changes in the correct order.
3. **Given** edited and original states exist, **When** I toggle compare mode, **Then** I can clearly view before/after outputs for the same image.

---

### User Story 3 - Export Finished Results (Priority: P2)

As a single local user, I can export the current edited result in common image formats so I can reuse it outside the app.

**Why this priority**: Editing is incomplete unless users can produce an output file.

**Independent Test**: Edit an image and export it to each supported format, then verify downloaded output matches selected format settings.

**Acceptance Scenarios**:

1. **Given** an edited image is open, **When** I choose an export format and export, **Then** I receive a downloadable image file matching that format.
2. **Given** I export as a quality-configurable format, **When** I set quality, **Then** the resulting output reflects the selected quality setting.
3. **Given** an image has never been edited, **When** I export it, **Then** export still succeeds using the current visible state.

---

### User Story 4 - Generate AI Images Reliably (Priority: P2)

As a single local user, I can generate images from prompts through a provider-agnostic interface, and still get deterministic output when external providers are unavailable.

**Why this priority**: AI generation is a key capability, and deterministic fallback keeps local workflows usable without credentials.

**Independent Test**: Generate with provider credentials present and absent, confirming normal provider execution when configured and deterministic fallback output when not configured.

**Acceptance Scenarios**:

1. **Given** a configured generation provider, **When** I submit a prompt and size, **Then** the system returns a generated image from that provider.
2. **Given** provider configuration is missing or invalid, **When** I submit the same normalized generation inputs multiple times, **Then** the fallback returns identical output each time.
3. **Given** I select an allowed output size, **When** generation completes, **Then** the generated image appears in the application workflow for viewing and further editing/export.

### Edge Cases

- Upload attempts include unsupported formats, zero-byte files, or corrupted image data.
- Multiple uploads share the same filename and must not overwrite prior assets.
- Search query contains mixed case, repeated spaces, or terms that produce no matches.
- Sort keys are identical for multiple images and require deterministic tie-breaking.
- User attempts to export while no image is loaded.
- Edit actions exceed undo history limits within a session.
- Compare mode is triggered when no edit delta exists.
- Generation request uses a disallowed size.
- Generation provider times out or returns an error mid-request.
- Runtime endpoint is unavailable on expected local port 8088.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST run as a local-first single-user application accessible at local runtime port `8088`.
- **FR-002**: System MUST allow upload of supported image files (`png`, `jpg`, `jpeg`, `webp`) and reject unsupported formats with clear user-facing feedback.
- **FR-003**: System MUST ensure duplicate filenames never overwrite an existing stored asset.
- **FR-004**: System MUST present a gallery view for all stored assets, including core metadata needed for browsing and selection.
- **FR-005**: System MUST support gallery search across filename and user-provided text metadata using case-insensitive matching.
- **FR-006**: System MUST support gallery sorting by at least name, created time, and updated time with deterministic ordering.
- **FR-007**: System MUST provide non-destructive editing so source image files are never modified by edit operations.
- **FR-008**: System MUST support at least crop, rotate, flip, tonal adjustments, and filter effects in the editor.
- **FR-009**: System MUST provide undo and redo for edit operations in the current editing session.
- **FR-010**: System MUST provide a before/after compare view between original and current edited state.
- **FR-011**: System MUST export the current visible image state to `png`, `jpg`, or `webp` as a downloadable output.
- **FR-012**: System MUST support configurable export quality for formats that use quality settings.
- **FR-013**: System MUST provide AI image generation through a provider abstraction that accepts prompt, size, and optional style inputs.
- **FR-014**: System MUST support generation sizes `1024x1024`, `1024x1536`, and `1536x1024`.
- **FR-015**: System MUST execute a deterministic fallback generator when no valid external provider is configured.
- **FR-016**: System MUST guarantee deterministic fallback behavior such that identical normalized inputs produce identical outputs.
- **FR-017**: System MUST make generated images available for the same view/edit/export workflow as uploaded images.

### Key Entities *(include if feature involves data)*

- **Image Asset**: A user-visible image entry containing stored file reference and browse metadata (name, format, dimensions, size, created/updated timestamps).
- **Image Metadata**: User-maintained descriptive text associated with an image asset, including tags and notes used for search.
- **Edit Session**: Non-persistent working state for one image containing ordered edit operations and undo/redo cursor.
- **Export Output**: User-downloaded derivative file produced from the current visible state, format selection, and optional quality setting.
- **Generation Request**: User-submitted prompt payload including normalized text prompt, output size, optional style, and optional provider override.
- **Generation Provider**: Abstract provider target that can be an external model service or deterministic local fallback.

## Assumptions

- This MVP is strictly single-user and local; authentication and multi-user access are out of scope.
- Search terms are split on whitespace and use AND semantics across terms.
- Edit history is session-scoped and not required to persist after app reload.
- Export outputs are downloadable artifacts and are not automatically added as new library assets.
- Deterministic fallback output consistency is required for identical normalized generation inputs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid uploads appear in the gallery within 2 seconds of upload completion on the reference local environment.
- **SC-002**: In acceptance testing, users can locate a known image using search and sort controls in under 10 seconds for a 200-image library.
- **SC-003**: In acceptance testing, users can complete a basic non-destructive edit flow (apply edit, undo, redo, compare) in under 60 seconds.
- **SC-004**: 100% of export attempts for supported formats produce a downloadable file or a clear actionable error message.
- **SC-005**: When provider credentials are absent, repeated generation requests with identical normalized inputs produce byte-identical fallback outputs in 100% of test runs.
- **SC-006**: 95% of AI generation requests (provider-backed or fallback) complete with a visible result or explicit error in under 20 seconds in the reference local environment.
- **SC-007**: Application startup and primary UI access on `localhost:8088` succeeds in 100% of smoke-test runs.
