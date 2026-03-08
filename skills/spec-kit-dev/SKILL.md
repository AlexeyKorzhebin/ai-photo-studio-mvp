# spec-kit-dev (Codex-first)

## Purpose
Orchestrate Spec-Kit development strictly through Codex CLI.

This skill enforces:
- CLI-only artifact modification
- Strict pipeline order
- Commit-driven progress
- Guardrails against process drift
- Controlled push policy

---

## Activation Conditions

Activate when request mentions:
- speckit
- constitution
- clarify
- plan
- tasks
- implement
- checklist
- retask
- pipeline
- wave
- T-XXX

---

## Core Behavior

1. Determine current pipeline stage.
2. Validate prerequisites.
3. Generate canonical Codex CLI command.
4. Execute via:
   codex exec --full-auto '...'
5. Inspect diff.
6. Auto-commit.
7. Ask for push confirmation.

---

## Hard Guardrails

### Forbidden Direct Edits

The skill must NOT use edit/write tools for:
- spec.md
- plan.md
- analyze.md
- tasks.md
- checklist.md
- constitution.md
- any product code

All changes must go through Codex.

---

### Conditional Edit Allowed

Edit tool is allowed ONLY if:
- Governance documentation
- Skill internal files
- Explicit infrastructure request
- Emergency CLI unavailability

In such cases:
- Separate commit required
- Commit message must contain: manual-change

---

## Pipeline Enforcement

Block execution if:
- Implement requested before tasks
- Checklist skipped
- Working tree dirty from previous wave
- Previous stage not committed

---

## Commit Policy

- Auto-commit after Codex execution
- Commit message must reference T-ID or stage
- Push only after user confirmation

---

## Drift Detection

If:
- Repeated failed implement attempts
- No commit after CLI execution
- Large uncontrolled diff

Then:
- Abort implement
- Return to /speckit.tasks

---

## Infrastructure Awareness

If Codex limit hit:
- Do NOT retry blindly
- Report infrastructure limit
- Suggest fallback
- Pause execution

