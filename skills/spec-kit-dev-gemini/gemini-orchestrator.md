# Gemini Orchestrator Playbook

## Purpose
Provide canonical command patterns for running Spec-Kit stages through Gemini CLI.

Use this file as the operational layer for `spec-kit-dev-gemini`.

---

## Global Prompt Construction Rules

Build every prompt in this order:

1. Stage command (`/speckit.*`) or explicit stage statement
2. Scope (`read only`, `modify only`, `implement only`)
3. Context (feature id, target T-ID, relevant constraints)
4. Output contract (`return exactly`, `report OK/Requires adjustment`, concise summary)
5. Continuation rule (`do not continue`, or allow broader audit)

---

## Global Pre-Checks

Before every execution:

1. Confirm the current pipeline stage.
2. Confirm required previous stage is complete.
3. Check working tree status.
4. Check whether Gemini CLI is authenticated and responsive.
5. Decide mode explicitly: strict or audit.

Abort if any precondition fails.

---

## Mode Selection

### Strict Mode
Use when deterministic behavior is required.

Characteristics:
- one-shot
- narrow scope
- exact output contract
- no exploratory continuation

### Audit Mode
Use when broader review is acceptable.

Characteristics:
- wider scope
- exploratory reading allowed
- richer commentary acceptable

For workflow gates, default to strict mode.

---

## Stage: Constitution

### Strict Command
```bash
gemini --prompt "Read .specify/memory/constitution.md only. Return exactly one word: OK or Requires adjustment. Do not read any other files. Do not continue reasoning."
```

### Audit Command
```bash
gemini --prompt "/speckit.constitution

Context:
- feature: <FEATURE_ID>
- review constitution alignment with current project rules

Tasks:
1. Review constitution.
2. If needed, propose or apply focused adjustment.
3. Report concise verdict.
"
```

---

## Stage: Clarify

### Strict Command
```bash
gemini --prompt "/speckit.clarify

Context:
- feature: <FEATURE_ID>
- list only unresolved ambiguities
- do not implement code
- keep output concise
"
```

### Audit Command
```bash
gemini --prompt "/speckit.clarify

Context:
- feature: <FEATURE_ID>
- review ambiguity across spec and plan artifacts
- identify missing decisions and assumptions
"
```

---

## Stage: Plan

### Strict Command
```bash
gemini --prompt "/speckit.plan

Context:
- feature: <FEATURE_ID>
- produce a short executable plan only
- do not implement code
"
```

### Audit Command
```bash
gemini --prompt "/speckit.plan

Context:
- feature: <FEATURE_ID>
- review existing scope and generate a plan aligned with MVP-first execution
- include verification expectations
"
```

---

## Stage: Tasks

### Strict Command
```bash
gemini --prompt "/speckit.tasks

Context:
- feature: <FEATURE_ID>
- preserve completed tasks when demonstrably completed
- use canonical T-numbering
- modify only tasks.md
- do not implement code
- summarize task count
"
```

### Audit Command
```bash
gemini --prompt "/speckit.tasks

Context:
- feature: <FEATURE_ID>
- review current decomposition quality
- re-slice tasks for smaller waves if needed
- preserve completed work where justified
"
```

---

## Stage: Implement

### Strict Command
```bash
gemini --prompt "/speckit.implement <T-ID>

Context:
- feature: <FEATURE_ID>
- implement only <T-ID>
- include tests for the implemented requirement
- do not widen scope
- summarize changed files and verification
"
```

### Audit Command
```bash
gemini --prompt "/speckit.implement <T-ID>

Context:
- feature: <FEATURE_ID>
- implement the task while reviewing for drift against plan and constitution
- keep scope bounded to the task
"
```

---

## Stage: Checklist

### Strict Command
```bash
gemini --prompt "/speckit.checklist

Context:
- feature: <FEATURE_ID>
- validate current implementation against checklist
- report concise pass/fail only
- do not implement code
"
```

### Audit Command
```bash
gemini --prompt "/speckit.checklist

Context:
- feature: <FEATURE_ID>
- perform a broader compliance review against checklist and recent implementation
"
```

---

## Commit Message Patterns

Use these patterns after successful execution:

- `spec: refresh constitution governance`
- `spec: clarify feature assumptions`
- `spec: create implementation plan for <FEATURE_ID>`
- `spec: regenerate tasks for <FEATURE_ID>`
- `feat(<T-ID>): implement <short-scope>`
- `chore: refresh checklist after <T-ID>`

---

## Post-Execution Review

After every Gemini run:

1. Inspect diff.
2. Confirm only expected files changed.
3. Confirm selected mode behaved as intended.
4. Commit automatically if valid.
5. Ask before push.

If invalid, stop and return to the appropriate earlier stage.
