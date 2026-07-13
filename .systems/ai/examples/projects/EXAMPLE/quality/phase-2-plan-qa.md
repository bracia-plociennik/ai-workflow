# phase-2-plan-qa.md - EXAMPLE

## Metadata

- Project: EXAMPLE
- Date: 2026-05-16
- Artifact under review: `.systems/ai/examples/projects/EXAMPLE/planning/phase-2-project-plan.md`
- Planning router under review: `.systems/ai/examples/projects/EXAMPLE/plans.md`
- Task index under review: `.systems/ai/examples/projects/EXAMPLE/tasks.md`
- Workflow phase: `phase-2-plan-qa`
- Result: `PASS`
- QA verification contract: `full-qa-verification-v1`

## QA Verification Scope

- Full QA contract: `.systems/ai/core/full-qa-verification.md`
- QA subject: plan, router, and task index only; no implementation code exists.

## Artifact QA Completeness Gate

- Owner intent and governing sources reviewed: `.systems/ai/examples/projects/EXAMPLE/architecture/phase-1-architecture.md`, `.systems/ai/examples/projects/EXAMPLE/planning/phase-2-project-plan.md`
- DoD / phase acceptance criteria reviewed: `yes`
- Scope and out-of-scope consistency: `aligned`
- Artifact / relevant diff review: `completed`
- Findings-first review: `completed`
- Failure / rework / dependency scenarios: `completed`
- Repository and source compatibility: `aligned`
- Post-fix full artifact re-review: `not-required`
- Evidence reviewed: `plan, plans.md, tasks.md`
- Skipped or unreadable sources: `none`
- Residual risk: `example-only artifact`
- Closure freshness: `current`

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
    notes: "Task ID, risk, status, task card path, spec path, and quality path are present."
  - check: "planning router consistency"
    result: "PASS"
    notes: "plans.md points to the example project plan."
artifacts-reviewed:
  - ".systems/ai/examples/projects/EXAMPLE/plans.md"
  - ".systems/ai/examples/projects/EXAMPLE/planning/phase-2-project-plan.md"
  - ".systems/ai/examples/projects/EXAMPLE/tasks.md"
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
