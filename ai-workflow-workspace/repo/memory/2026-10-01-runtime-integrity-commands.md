# Runtime Integrity Commands

- Date: 2026-10-01
- Type: command-note
- Scope: repo-wide
- Status: active
- Source: projects/workflow-parity-and-runtime-integrity-v1/quality and checkpoint evidence; current source paths.
- Privacy/scope check: pass

## Commands And Boundaries
- .systems/scripts/check-runtime-integrity runs 46 synthetic regressions plus policy scans.
- .systems/scripts/report-coordinator-status --project <slug> --format json|human is read-only; execution_authorized is always false.
- check-distillation-state no-arg inventory scans canonical owning namespaces. Project-scoped checks retain existing scoped populations.
- Before staging new source, smoke fixtures need exact AI_WORKFLOW_SMOKE_EXTRA_FILES paths; after the source is tracked, normal selected worktree inputs suffice.
- Use current worktree, not HEAD blobs, for fixtures. Never include ignored runtime or raw skill context.
- Full validation retained all 694 previous IDs and adds one supplemental test; no measured speedup or model behavior claim.
- Feature source is presently local/uncommitted. Verify availability and assessment freshness before using these commands in another checkout.

