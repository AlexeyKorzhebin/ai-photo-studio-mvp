# AI Photo Studio MVP Constitution

## Core Principles

### I. MVP-First, Demoable Delivery
All work MUST optimize for a runnable, demonstrable MVP over production-hardening. Features are accepted only if they make the current demo more complete, testable, or understandable.

### II. Spec-Driven Execution
Non-trivial changes MUST follow a clear flow: clarify scope and constraints, plan executable tasks, implement in increments, and validate outcomes. Ambiguity MUST be resolved before coding.

### III. CLI-Agent-First Orchestration
Delivery is orchestrated through CLI-agent workflows. The orchestrator owns decomposition, sequencing, verification, and acceptance framing; executors own implementation details and evidence.

### IV. Simplicity Over Abstraction
Prefer direct, minimal solutions over generalized frameworks. Reject speculative architecture and overengineering unless explicitly required by current scope.

### V. Auditable Work and Decisions
Implementation decisions, deviations, and phase transitions MUST be traceable. Outputs should be runnable, reviewable, and linked to explicit acceptance criteria.

## Product and Technical Constraints

- Project scope is a local-first experimental MVP, not a production SaaS deployment.
- Authentication and multi-tenant user management are out of MVP scope unless explicitly approved as a scope change.
- Data storage is limited to SQLite and local filesystem persistence.
- Frontend stack is React + Vite + TypeScript.
- Backend stack is FastAPI.
- Canonical runtime and integration path is Docker Compose, with the application exposed on port 8088.

## Workflow and Quality Gates

- Before non-trivial implementation, confirm request, constraints, and concrete acceptance criteria.
- Produce a short executable plan where each task includes a verification method.
- Deliver in visible, testable increments; avoid batching large unverified changes.
- Each increment MUST include minimally sufficient checks (for example targeted tests, smoke checks, or endpoint/UI validation).
- Reject non-runnable output and unnecessary complexity.

## Governance

- This constitution governs orchestrator and executor behavior for this repository and supersedes conflicting local practices.
- Only a human approver can authorize stage completion and scope changes.
- Amendments require written rationale and an explicit update to this file.
- Any deviation MUST be logged with reason, risk, owner, and rollback plan.
- Major phase transitions MUST be logged in `PM_ACTION_LOG.md`.

**Version**: 1.0.0 | **Ratified**: 2026-03-08 | **Last Amended**: 2026-03-08
