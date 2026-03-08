# Research: Targeted MVP Implementation Decisions

## 1) AI generation API shape
- Decision: Use `size` enum input (`1024x1024`, `1024x1536`, `1536x1024`) instead of arbitrary width/height.
- Why: Matches clarified spec exactly and simplifies validation/testing.
- Rejected alternative: Keep free-form `width`/`height` range validation.
- Rejection reason: Allows unsupported sizes and increases UI/backend mismatch risk.

## 2) Deterministic fallback implementation
- Decision: Deterministic mock output derives from normalized tuple (`prompt`, `size`, `style`, `provider_override`), storing seed/hash metadata with generated asset record.
- Why: Required for stable offline/dev behavior and reproducible tests.
- Rejected alternative: Randomized placeholder image generation.
- Rejection reason: Breaks determinism requirement and weakens regression tests.

## 3) Edit state persistence boundary
- Decision: Keep edit operation history in frontend session state (tab lifetime), not persisted in database.
- Why: Clarified MVP scope explicitly says history is session-scoped and non-persistent.
- Rejected alternative: Persist `EditSession`/`EditOperation` tables.
- Rejection reason: Extra schema/API complexity without MVP value.

## 4) Export implementation path
- Decision: Keep export client-side from rendered canvas, downloaded directly, no backend persistence.
- Why: Aligns with FR-027 and keeps non-destructive pipeline simple.
- Rejected alternative: Backend export endpoint storing derivative files.
- Rejection reason: Adds storage lifecycle complexity and violates “not persisted unless explicitly downloaded” intent.

## 5) Tags model
- Decision: Keep tags as comma-separated text on `ImageAsset` with simple free-text edit.
- Why: Explicit clarified MVP decision.
- Rejected alternative: Tag table + relation/join queries.
- Rejection reason: Overengineering for local single-user MVP.

## 6) Search semantics
- Decision: Split query by whitespace; AND semantics across terms; each term matches substring in filename/tags/notes case-insensitively.
- Why: Explicit clarification; deterministic and easy to explain.
- Rejected alternative: OR terms, fuzzy match, stemming, or phrase parser.
- Rejection reason: Unnecessary complexity and less predictable MVP behavior.

## 7) Sorting determinism
- Decision: Sort by selected key (`created`, `updated`, `name`) plus stable secondary key (`id`).
- Why: Needed to satisfy deterministic repeated results.
- Rejected alternative: Single-column sort only.
- Rejection reason: Tie rows can reorder nondeterministically.

## 8) Runtime topology
- Decision: Keep two-service Compose topology (frontend nginx + backend FastAPI), frontend published on `8088`.
- Why: Already implemented and satisfies runtime contract with simple operational model.
- Rejected alternative: Merge frontend and backend into one process/container.
- Rejection reason: Adds coupling and build complexity with no MVP gain.
