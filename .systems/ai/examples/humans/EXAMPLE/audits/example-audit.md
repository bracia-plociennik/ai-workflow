# Human Audit: EXAMPLE Autopilot Readiness

## Date

`2026-05-16`

## Scope

Review whether the EXAMPLE workspace is ready for supervised autopilot.

## Sources Reviewed

- `.systems/ai/core/autopilot.md`
- `.systems/ai/examples/projects/EXAMPLE/status.md`
- `.systems/ai/examples/projects/EXAMPLE/specs/phase-3-ex-01-example-task-specification.md`

## Findings

| Severity | Finding | Evidence | Recommendation |
| --- | --- | --- | --- |
| info | Runtime files are examples | `autopilot/` contains sample files | Recreate from templates for real run |
| warning | Project is example-only | README marks it non-active | Do not use for production execution |

## Decisions Needed

- None for the example workspace.

## Residual Risk

The example may drift from future workflow rules unless templates are updated.

## Final Summary

EXAMPLE demonstrates all human-facing artifact types and is not active execution evidence.
