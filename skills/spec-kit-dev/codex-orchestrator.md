# Codex Orchestrator Playbook

## Purpose
Provide canonical command patterns for running Spec-Kit stages through Codex CLI.

Use this file as the operational layer for `spec-kit-dev`.

---

## Global Prompt Construction Rules

Build every prompt in this order:

1. Stage command (`/speckit.*`)
2. Scope (`read only`, `implement only`, `do not modify other files`)
3. Context (feature id, target T-ID, relevant constraints)
4. Output contract (`return exactly`, `summarize counts`, `report OK/Requires adjustment`)
5. Write restrictions (`do not modify files`, `modify only tasks.md`, etc.)

---

## Global Pre-Checks

Before every execution:

1. Confirm the current pipeline stage.
2. Confirm required previous stage is complete.
3. Check working tree status.
4. Check whether the task/wave already has a commit.
5. Check whether Codex is available (no active usage-limit error).

Abort if any precondition fails.

---

## Stage: Constitution

### Goal
Validate or refine the project constitution.

### Preconditions
- Project is initialized with Spec-Kit artifacts.
- No implement-stage work is running.

### Canonical Strict Command
```bash
codex exec --full-auto '/speckit.constitution

Read .specify/memory/constitution.md only.
Return exactly one word: OK or Requires adjustment.
Do not modify files.
Do not read other files.
'
```

### Canonical Review Command
```bash
codex exec --full-auto '/speckit.constitution

Context:
- feature: <FEATURE_ID>
- objective: validate constitution against current project rules

Tasks:
1. Review constitution.
2. Check whether it aligns with project operating rules.
3. If adjustment is needed, modify only constitution.md.
4. Report concise verdict.
'
```

### Expected Output
- `OK` or `Requires adjustment` in strict mode
- concise verdict in review mode

### Abort Conditions
- Codex usage limit
- uncontrolled file modifications
- reading beyond requested scope in strict mode

---

## Stage: Clarify

### Goal
Resolve ambiguity before planning or implementation.

### Preconditions
- Constitution pass completed.
- Feature/spec exists.

### Canonical Command
```bash
codex exec --full-auto '/speckit.clarify

Context:
- feature: <FEATURE_ID>
- identify unresolved ambiguity only
- keep clarifications concise and decision-oriented

Output:
- clarified questions or resolved assumptions only
- do not implement code
'
```

### Expected Output
- clarified questions, assumptions, or resolved decisions

### Abort Conditions
- no existing feature context
- attempts to jump into implementation

---

## Stage: Plan

### Goal
Produce an executable implementation plan.

### Preconditions
- Clarification complete.
- Scope is bounded.

### Canonical Command
```bash
codex exec --full-auto '/speckit.plan

Context:
- feature: <FEATURE_ID>
- produce a short executable plan
- include task-level ownership and verification expectations

Restrictions:
- do not implement code
- do not modify unrelated files
'
```

### Expected Output
- short plan with execution steps and verification notes

### Abort Conditions
- ambiguous scope
- plan expands beyond MVP boundaries

---

## Stage: Tasks

### Goal
Generate or re-slice task decomposition.

### Preconditions
- Plan exists.
- No active implement wave in progress.

### Canonical Command
```bash
codex exec --full-auto '/speckit.tasks

Context:
- feature: <FEATURE_ID>
- preserve completed tasks when demonstrably completed
- use canonical T-numbering
- keep decomposition small and implementation-friendly

Restrictions:
- modify only tasks.md
- do not implement code
- print concise task count summary
'
```

### Expected Output
- updated tasks.md
- canonical T-IDs
- concise task count summary

### Abort Conditions
- tasks explode in size without reslicing
- non-task files modified

---

## Stage: Implement

### Goal
Implement one task or one tightly-scoped wave.

### Preconditions
- Target T-ID exists.
- Tasks stage committed.
- Scope is explicit.

### Canonical Command
```bash
codex exec --full-auto '/speckit.implement <T-ID>

Context:
- feature: <FEATURE_ID>
- implement only <T-ID>
- follow current constitution and plan
- include tests for the implemented requirement

Restrictions:
- do not edit tasks.md manually
- do not widen scope beyond <T-ID>
- report files changed and verification run
'
```

### Expected Output
- code and tests for one task/wave
- concise change summary
- verification summary

### Abort Conditions
- scope drift
- large uncontrolled diff
- repeated failure on same task without reslicing

---

## Stage: Checklist

### Goal
Validate completion gate for a wave or feature.

### Preconditions
- Implement stage completed.
- Relevant verification exists.

### Canonical Command
```bash
codex exec --full-auto '/speckit.checklist

Context:
- feature: <FEATURE_ID>
- validate current implementation against checklist

Restrictions:
- update checklist artifacts only if required by the stage
- do not implement new code
- report pass/fail succinctly
'
```

### Expected Output
- checklist verdict
- explicit pass/fail notes

### Abort Conditions
- missing tests
- missing implementation for referenced task

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

After every Codex run:

1. Inspect diff.
2. Confirm only expected files changed.
3. Confirm output contract was satisfied.
4. Commit automatically if valid.
5. Ask before push.

If invalid, stop and return to the appropriate earlier stage.
