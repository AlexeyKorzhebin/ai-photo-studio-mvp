# Reference constitution context

Generate a fresh project constitution for AI Photo Studio MVP.
Use this as background context only; produce a proper Spec-Kit constitution file.

## Governing principles
- MVP-first and demoable
- Spec-driven discipline: clarify -> plan -> tasks -> implement -> validate
- CLI-agent-first delivery; orchestrator owns decomposition and acceptance
- Simplicity over abstraction
- Auditable execution

## Product constraints
- local-first experiment MVP, not production SaaS
- no auth in MVP scope
- SQLite + local filesystem only
- frontend React + Vite + TypeScript
- backend FastAPI
- canonical runtime via Docker Compose on port 8088

## Workflow and quality gates
- confirm request/constraints/acceptance before coding non-trivial changes
- produce short executable plan with verification per task
- ship in testable, visible increments
- each increment needs minimally sufficient checks
- reject overengineering and non-runnable output

## Governance expectations
- constitution governs orchestrator and executor behavior
- only human can approve stage completion and scope changes
- amendments require written rationale and explicit file update
- deviations must be logged with reason/risk/owner/rollback plan
- major phase transitions must be logged in PM_ACTION_LOG.md
