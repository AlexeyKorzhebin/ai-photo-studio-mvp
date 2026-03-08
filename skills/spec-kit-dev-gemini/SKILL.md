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


---

## Gemini Operating Modes

Support two modes explicitly.

### Strict Mode

Use strict mode when deterministic behavior is required.

Pattern:
- one-shot prompt
- narrow file scope
- exact output contract
- no exploratory continuation

Use for:
- constitution verdicts
- checklist verdicts
- gate-style validations
- tight acceptance checks

### Audit Mode

Use audit mode when broader review is useful.

Pattern:
- wider prompt scope
- exploratory reading allowed
- richer commentary acceptable

Use for:
- broader compliance review
- drift detection
- exploratory analysis

Prefer strict mode for workflow gates. Use audit mode only when the wider scope is intentional.

---

## Playbook Usage

When this skill is activated for an actual pipeline stage, read `gemini-orchestrator.md` before constructing the command.

Use it to select:
- the current stage template
- strict vs audit mode
- required pre-checks
- expected output contract
- abort conditions

Do not improvise stage commands when a canonical playbook entry exists.
