# Guardrails for spec-kit-dev

## Mandatory Pre-Execution Checks

Before any Codex execution:

1. Verify working tree status (must be clean unless expected).
2. Verify previous pipeline stage completed.
3. Ensure commit exists for previous wave.
4. Validate T-ID exists before implement.

---

## Abort Conditions

Abort execution if:
- Pipeline order violated
- Attempted manual artifact modification
- Infrastructure limit detected
- CLI execution returns non-zero without diff

---

## Emergency Mode

If CLI is unavailable:
- Manual edit allowed only for governance or infrastructure
- Commit must include: manual-change
- Explicit log entry required

