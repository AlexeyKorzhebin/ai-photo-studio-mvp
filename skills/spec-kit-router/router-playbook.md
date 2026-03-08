# Spec-Kit Router Playbook

## Purpose
Provide a deterministic intake and routing flow before any Spec-Kit executor runs.

---

## Step 1 — Identify target project

Determine:
- repository path
- whether the request is about a new project or current project

If the target project is ambiguous, stop and resolve the target first.

---

## Step 2 — Detect initialization

Check for:
- `.specify/`
- Spec-Kit stage artifacts
- constitution memory/artifacts

### Routing outcome
- If initialized: continue to stage detection
- If not initialized: route to bootstrap/init path

---

## Step 3 — Detect current stage

Use request intent plus repository evidence.

### Typical mappings
- “start the project” → constitution
- “clarify requirements” → clarify
- “make a plan” → plan
- “split into tasks” → tasks
- “implement T-XXX” → implement
- “validate completion” → checklist
- “continue” → infer from repo state

---

## Step 4 — Validate execution readiness

Check:
- working tree state
- whether previous stage was completed
- whether a commit exists for the previous wave
- whether requested stage is valid now

Abort and report if pipeline order is invalid.

---

## Step 5 — Select executor

### Default
- Codex-first (`spec-kit-dev`)

### Fallback
- Gemini (`spec-kit-dev-gemini`) when Codex is limited or unavailable

### Gemini mode selection
- strict → deterministic verdict/gate tasks
- audit → broader review

---

## Step 6 — Handoff

### If Codex selected
Read:
- `../spec-kit-dev/SKILL.md`
- `../spec-kit-dev/codex-orchestrator.md`

### If Gemini selected
Read:
- `../spec-kit-dev-gemini/SKILL.md`
- `../spec-kit-dev-gemini/gemini-orchestrator.md`

Then construct the stage-specific command.

---

## Router output format

Return a concise routing block:

- project: <new|existing|uninitialized-existing>
- initialized: <yes|no>
- stage: <constitution|clarify|plan|tasks|implement|checklist>
- executor: <codex|gemini>
- mode: <strict|audit|n/a>
- next-read: <path>
- next-action: <summary>

