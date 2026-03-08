# spec-kit-dev-gemini (Gemini-first)

## Purpose
Orchestrate Spec-Kit development strictly through Gemini CLI.

This skill mirrors spec-kit-dev (Codex-first) but uses Gemini as executor.

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
3. Generate canonical Gemini CLI command.
4. Execute via:
   gemini --prompt "..."
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

All changes must go through Gemini CLI.

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

- Auto-commit after Gemini execution
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

If Gemini CLI fails:
- Do NOT retry blindly
- Report infrastructure issue
- Suggest executor switch
- Pause execution

