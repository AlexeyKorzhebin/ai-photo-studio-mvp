# Spec-Kit Checklist (Post Re-Tasking)

Use this as a self-control gate. Only check an item when evidence exists in code/tests/runtime output for this branch.

## 1) Artifact and Backlog Consistency
- [ ] `spec.md`, `plan.md`, `analyze.md`, and `tasks.md` are mutually consistent after re-slicing.
- [ ] All open items in `tasks.md` are mapped to one of: contract, UX, docs/runtime, or verification.
- [ ] `analyze.md` blocker list still matches the current highest-risk gaps.

## 2) Contract-Complete Gate (Before Broad QA)
- [ ] Missing prompt validation behavior is explicit and user-correctable.
- [ ] Invalid `size` validation behavior is explicit and user-correctable (with allowed values).
- [ ] Decision on backend `quality` validation is documented and reflected in tests.
- [ ] Upload and generate paths have all-or-nothing cleanup behavior for DB/storage failure cases.
- [ ] Tags/notes edit flow is complete in UI (edit, cancel, save, in-flight disable, error handling, state reconcile).
- [ ] Search debounce and selection stability behavior are complete and intentional.
- [ ] Editor crop cancel/apply and JPG/WEBP quality control behavior match clarified intent.
- [ ] Docs reachability strategy is chosen and implemented (proxy vs direct backend URL).
- [ ] README and quickstart docs paths are accurate for compose runtime.

## 3) Verification Gate (Evidence Required)
- [ ] Backend tests cover missing prompt and invalid `size` error contracts.
- [ ] Backend tests cover duplicate filenames (distinct records and stored paths).
- [ ] Backend tests cover upload/generate rollback cleanup on DB failure.
- [ ] Frontend tests cover generation payload contract (`size`, optional style/provider).
- [ ] Frontend tests cover metadata edit flow and error/in-flight states.
- [ ] Frontend tests cover search debounce, selection persistence, and selection fallback.
- [ ] Frontend tests cover editor quality-control visibility and undo/redo boundary behavior.
- [ ] `make test` passes locally.
- [ ] `make build` passes locally.
- [ ] `docker compose up --build` smoke checks pass (`8088`, health endpoint, docs endpoint, upload->edit->export, AI generate/fallback).

## 4) Release Readiness Gate
- [ ] All acceptance criteria in `spec.md` are validated with evidence.
- [ ] Release documentation is accurate (`README.md`, `quickstart.md`, `.env.example` if applicable).
- [ ] No secrets are committed.
- [ ] Branch is pushed to origin.
