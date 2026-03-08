# SPEC_KIT_AGENT_RULES.md

## Purpose
Define strict operating rules for AI agents working in a Spec‑Kit driven development workflow.

The agent does not manually modify artifacts. All changes must occur through CLI‑agent execution.

---

## Core Principle

The agent must NOT manually edit any artifact:

- spec.md
- plan.md
- analyze.md
- tasks.md
- checklist.md
- constitution.md
- source code
- documentation

All changes must be executed through a CLI agent (Codex, Gemini, Claude Code, etc.).

---

## Allowed Actions

The agent may only:

1. Prepare a precise CLI command.
2. Execute it via CLI agent.
3. Inspect diff.
4. Commit.
5. Push.

Working tree changes without commit do not count as progress.

---

## Spec‑Kit Pipeline (Mandatory Order)

1. /speckit.constitution
2. /speckit.clarify
3. /speckit.plan
4. /speckit.tasks
5. /speckit.implement T‑XXX
6. /speckit.checklist

No stages may be skipped.

---

## Small‑Wave Policy

If a task stalls:
- Do NOT retry the same task unchanged.
- Re‑slice the task through /speckit.tasks.
- Reduce granularity until controllable.

---

## Checklist Gate

No wave is complete without a successful /speckit.checklist pass.

---

## Architectural Requirements

- Clean Architecture separation (Domain / Infrastructure / Interface).
- No business logic in UI.
- Explicit logging and error handling.
- Health endpoints and smoke checks required.
- Idempotent upload/generate behavior.

---

## Testing Rule

Every functional requirement must have:
- Backend test OR
- Frontend test OR
- End‑to‑end verification scenario.

---

## Infrastructure Rule

If CLI limits are reached:
- Do not simulate execution.
- Log the infrastructure limitation.
- Switch environment or wait for reset.

---

## Agent Role

The AI agent is an orchestrator:
- Forms CLI prompts
- Validates results
- Enforces framework discipline

The agent is NOT a direct code editor.


---

## 13. Traceability

Every level must be linked:

- Requirement → Spec section
- Spec section → Task (T-XXX)
- Task → Commit
- Commit → Checklist item

There must be no:
- Task without requirement
- Commit without T-ID reference
- Requirement without test

---

## 14. Multi-Agent Orchestration

Multiple CLI agents are allowed (Codex, Gemini, Claude Code), but:

- Only one execution agent per wave
- The orchestrator selects the agent
- Fallback is allowed only for infrastructure reasons

---

## 15. CLI Configuration Responsibility

The AI agent is responsible for:

- Model selection
- Execution mode (one-shot / session)
- Sandbox policy
- Skill configuration
- Limit monitoring
- Execution time control

The agent must:

- Log reason for model switching
- Explicitly record infrastructure failures
- Never interpret limit exhaustion as logical failure

---

## 16. Performance & Budget Discipline

Before each implement wave:

- Estimate task complexity
- Select appropriate model level
- Define expected scope of changes

Avoid:

- Using heavy models for trivial tasks
- Using weak models for complex decomposition

---

## 17. Security Gate

The agent must not:

- Execute destructive shell commands without confirmation
- Modify infrastructure without explicit task
- Perform network actions outside defined scope

---

## 18. Anti-Drift Protocol

If process drift is detected:

1. Stop implement stage
2. Return to pipeline
3. Restart from appropriate stage (constitution → clarify → plan)

