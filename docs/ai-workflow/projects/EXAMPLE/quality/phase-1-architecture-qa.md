# phase-1-architecture-qa.md - EXAMPLE

## Metadata

- Project: EXAMPLE
- Date: 2026-05-16
- Artifact under review: `docs/ai-workflow/projects/EXAMPLE/architecture/phase-1-architecture.md`
- Workflow phase: `phase-1-architecture-qa`
- Result: `PASS`

## Evidence

```yaml
commands:
  - command: "manual architecture artifact review"
    result: "PASS"
    notes: "Example architecture contains required sections and project-local paths."
manual-checks:
  - check: "architecture completeness"
    result: "PASS"
    notes: "Required example sections are present."
  - check: "internal consistency"
    result: "PASS"
    notes: "Referenced paths stay inside docs/ai-workflow/projects/EXAMPLE."
artifacts-reviewed:
  - "docs/ai-workflow/projects/EXAMPLE/architecture/phase-1-architecture.md"
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
required-next-phase: "phase-2-project-plan"
```
