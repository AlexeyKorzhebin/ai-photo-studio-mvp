# SPEC_KIT_SYSTEM_MAP.md

## Purpose
Provide a high-level map of the Spec-Kit agent system built for AI Photo Studio MVP.

This document explains the system layers, responsibilities, executor roles, and extension path.

---

## 1. System Goal

Build a controlled agent-development framework where:

- project work follows Spec-Kit stages,
- implementation is delegated to CLI agents,
- orchestration remains separate from execution,
- progress is commit-driven,
- guardrails prevent process drift.

---

## 2. System Layers

### Layer 1 — Policy Layer

Defines the operating law of the system.

Primary file:
- `docs/SPEC_KIT_AGENT_RULES.md`

Contains:
- pipeline order
- direct-edit restrictions
- commit policy
- traceability rules
- executor policy
- anti-drift protocol
- group communication rule

---

### Layer 2 — Skill Layer

Defines skill-specific agent behavior.

Primary files:
- `skills/spec-kit-dev/SKILL.md`
- `skills/spec-kit-dev-gemini/SKILL.md`

Contains:
- activation conditions
- executor identity
- hard guardrails
- commit/push behavior
- playbook linkage

---

### Layer 3 — Execution Playbooks

Defines canonical command templates by pipeline stage.

Primary files:
- `skills/spec-kit-dev/codex-orchestrator.md`
- `skills/spec-kit-dev-gemini/gemini-orchestrator.md`

Contains:
- stage goals
- preconditions
- canonical commands
- expected outputs
- abort conditions
- commit message patterns

---

### Layer 4 — Executor Runtime

Actual CLI agent runtime used to perform work.

Current executors:
- Codex CLI (primary)
- Gemini CLI (fallback)

Future executors:
- Claude Code
- other CLI-capable coding agents

---

## 3. Role Model

### Orchestrator

The orchestrator:
- chooses the stage
- prepares the command
- enforces policy
- checks diff
- commits results
- asks before push

The orchestrator does NOT directly edit product artifacts.

### Executor

The executor:
- receives a stage-specific command
- performs the requested operation
- returns result/diff/verdict

The executor does not own process design.

---

## 4. Current Executor Policy

### Codex

Status:
- primary executor
- natural fit for slash-command style prompts
- strong for strict scope-controlled runs

Use for:
- normal Spec-Kit execution
- stage-gated workflows
- default implementation path

### Gemini

Status:
- fallback executor
- validated in real CLI runs

Modes:
- **Strict Mode** — deterministic one-shot workflow gates
- **Audit Mode** — broader exploratory review

Use for:
- fallback when Codex is limited
- controlled verdict checks
- broader compliance review when explicitly intended

---

## 5. Pipeline Model

Canonical order:

1. `/speckit.constitution`
2. `/speckit.clarify`
3. `/speckit.plan`
4. `/speckit.tasks`
5. `/speckit.implement <T-ID>`
6. `/speckit.checklist`

Rules:
- do not skip stages
- do not manually modify artifacts
- do not implement without task scope
- do not close a wave without checklist pass

---

## 6. Artifact Governance

### CLI-only artifacts

These must only be changed through executor CLI:
- `constitution.md`
- `spec.md`
- `plan.md`
- `analyze.md`
- `tasks.md`
- `checklist.md`
- product code

### Manually editable artifacts

These may be edited directly by the orchestrator under policy constraints:
- governance documents
- skill files
- repo-operating documentation
- explicit infrastructure docs/config when requested

---

## 7. Commit Model

### Progress Rule

Working tree changes are not considered progress.

Progress exists only when:
- expected diff exists
- commit exists
- commit matches intended stage/task

### Push Rule

- commit may be automatic
- push requires user confirmation

---

## 8. Drift Control

Drift indicators:
- repeated failed implement attempts
- expanding diff without bounded scope
- manual artifact edits
- skipped pipeline stages
- infrastructure problems misread as logic errors

Response:
- stop execution
- return to previous valid stage
- re-slice tasks if needed
- log incident and prevention

---

## 9. Infrastructure Awareness

The system treats executor limits as infrastructure constraints, not reasoning failures.

Examples:
- Codex usage limit
- executor auth failure
- CLI timeout
- runtime unavailability

Correct response:
- report clearly
- do not fake progress
- switch executor or wait

---

## 10. Extension Path

### Short-term
- add Claude Code executor skill
- add prompt templates as reusable references
- add dry-run validation commands

### Mid-term
- create a meta-skill that routes to executor-specific skills
- standardize executor capability matrix
- add automated preflight checks

### Long-term
- unify multi-executor orchestration under one routing layer
- add metrics for executor quality, latency, and drift risk

---

## 11. Current Repository Map

### Governance
- `docs/SPEC_KIT_AGENT_RULES.md`
- `docs/SPEC_KIT_SYSTEM_MAP.md`

### Codex Path
- `skills/spec-kit-dev/SKILL.md`
- `skills/spec-kit-dev/guardrails.md`
- `skills/spec-kit-dev/codex-orchestrator.md`

### Gemini Path
- `skills/spec-kit-dev-gemini/SKILL.md`
- `skills/spec-kit-dev-gemini/guardrails.md`
- `skills/spec-kit-dev-gemini/gemini-orchestrator.md`

---

## 12. Practical Usage Model

When a user asks for Spec-Kit execution:

1. Trigger the correct executor skill.
2. Read the skill instructions.
3. Read the corresponding orchestrator playbook.
4. Determine stage and mode.
5. Run pre-checks.
6. Execute canonical command.
7. Inspect diff.
8. Commit.
9. Ask before push.

This keeps orchestration reproducible and executor behavior bounded.

