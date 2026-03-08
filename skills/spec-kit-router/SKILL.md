---
name: spec-kit-router
description: Route Spec-Kit development requests to the correct workflow and executor. Use when a user wants to start or continue a Spec-Kit-driven software project and the agent must determine: (1) whether the project is new or existing, (2) whether Spec-Kit is initialized, (3) which pipeline stage is current or required, and (4) whether to use the Codex-first or Gemini-first executor skill.
---

# spec-kit-router

Route Spec-Kit work before any executor-specific skill is used.

## Core responsibility

Determine four things before execution:

1. Is this a new project or an existing one?
2. Is Spec-Kit initialized in the target project?
3. What is the correct current pipeline stage?
4. Which executor skill should be used?

Do not execute stage commands blindly.

---

## Routing policy

### 1. Classify project state

Determine whether the request targets:
- a new project,
- an existing project already using Spec-Kit,
- an existing project not yet initialized for Spec-Kit.

### 2. Detect initialization

Check for Spec-Kit initialization markers such as:
- `.specify/`
- Spec-Kit memory/artifact structure
- stage artifacts or constitution memory

If initialization is missing, route to initialization/bootstrap guidance before pipeline execution.

### 3. Determine pipeline stage

Map the user request to the correct stage:
- constitution
- clarify
- plan
- tasks
- implement
- checklist

If the user asks to continue, infer the stage from repository state instead of guessing.

### 4. Select executor

Use:
- `spec-kit-dev` for Codex-first execution
- `spec-kit-dev-gemini` for Gemini-first execution

Prefer Codex when available.
Use Gemini when Codex is limited or unavailable.

---

## Mandatory intake checks

Before routing, determine:

1. Target repository/path
2. New vs existing project
3. Spec-Kit initialized or not
4. Working tree status
5. Latest relevant commit
6. Current or required pipeline stage
7. Executor availability
8. Strict vs audit mode if Gemini is selected

---

## Hard constraints

Do not:
- directly edit Spec-Kit artifacts
- bypass pipeline order
- send execution commands before routing is complete
- choose implement stage without bounded task scope
- ignore dirty working tree when it affects stage validity

---

## Handoff rule

After routing is complete:

- if executor is Codex, read `../spec-kit-dev/codex-orchestrator.md`
- if executor is Gemini, read `../spec-kit-dev-gemini/gemini-orchestrator.md`

Then construct the canonical command for the selected stage.

Do not improvise if a canonical stage template exists.

---

## Expected output of the router

Produce a concise routing decision containing:

- project state: new / existing / uninitialized-existing
- initialization status
- selected stage
- selected executor
- selected mode (if Gemini)
- next file/playbook to read

