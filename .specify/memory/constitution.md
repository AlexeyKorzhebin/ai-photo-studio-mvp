# Spec-Kit Constitution — AI Photo Studio MVP

## 1) Core Principles
1. MVP-first and demoable: every iteration must produce a visible, runnable outcome over internal perfection.
2. Spec-driven discipline: non-trivial work requires `clarify -> plan -> tasks -> implement -> validate`; do not skip clarification.
3. CLI-agent-first delivery: implementation is delegated to coding agents via CLI; PM/orchestrator owns decomposition, sequencing, and acceptance.
4. Simplicity over abstraction: choose the smallest design that satisfies current MVP requirements; defer frameworks/patterns not needed now.
5. Auditable execution: major PM decisions and agent actions must be logged with timestamp, scope, and outcome.

## 2) Product Constraints
1. Scope: local-first AI Photo Studio MVP for experiment validation, not a production SaaS.
2. Auth: no authentication/authorization in MVP scope.
3. Data: SQLite for metadata/state and local filesystem volume for assets; no cloud DB/object storage dependencies.
4. Stack baseline: frontend React + Vite + TypeScript; backend FastAPI; Docker Compose as the canonical local runtime.
5. Runtime contract: app is demoable through Docker Compose on port `8088`.

## 3) Development Workflow & Quality Gates
1. Intake gate: confirm request, constraints, and acceptance criteria in writing before coding non-trivial changes.
2. Planning gate: produce a short executable plan with task-level ownership and expected verification per task.
3. Delivery gate: ship in testable increments with visible checkpoints (API endpoint, UI path, CLI output, or compose service behavior).
4. Validation gate: each increment must include minimally sufficient checks (targeted tests and/or manual verification steps) proving acceptance criteria.
5. Merge gate: reject overengineered solutions lacking immediate MVP value, and reject work that is not demonstrably runnable.

## 4) Governance
1. Authority: this constitution governs PM/orchestrator and coding-agent behavior for this repository.
2. Human acceptance gates: only the human orchestrator/stakeholder can approve stage completion and scope changes.
3. Change control: amendments require a written rationale and explicit update to this file before affected work proceeds.
4. Exception handling: urgent deviations must be logged with reason, risk, owner, and rollback/cleanup plan.
5. Recordkeeping: log constitution adoption/completion and all major phase transitions in `PM_ACTION_LOG.md`.
