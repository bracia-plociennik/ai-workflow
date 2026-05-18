# phase-2-plan-qa.md - EXAMPLE

## Metadata

- Project: EXAMPLE
- Date: 2026-05-16
- Artifact under review: `docs/projects/EXAMPLE/planning/phase-2-project-plan.md`
- Task index under review: `docs/projects/EXAMPLE/tasks.md`
- Workflow phase: `phase-2-plan-qa`
- Result: `PASS`

## Evidence

```yaml
commands:
  - command: "manual plan and task index review"
    result: "PASS"
    notes: "Example plan and task index describe the same example task."
manual-checks:
  - check: "architecture coverage"
    result: "PASS"
    notes: "Example architecture is covered by EX-DOCS-001-example-task."
  - check: "task index consistency"
    result: "PASS"
    notes: "Task ID, risk, status, spec path, and quality path are present."
artifacts-reviewed:
  - "docs/projects/EXAMPLE/planning/phase-2-project-plan.md"
  - "docs/projects/EXAMPLE/tasks.md"
skipped-checks: []
```

## Findings

- Critical errors: none.
- Warnings: none.
- Residual risk: example-only artifact.

## Gate Decision

```yaml
result: PASS
can-proceed: true
required-next-phase: "phase-2-task-packaging"
```
