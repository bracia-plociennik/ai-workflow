# Canonical Update And Validation Completion Handoff

## Scope

Privacy-safe conceptual handoff for adapting the canonical nested-clone and
validation lifecycle boundaries in `ai-system`. This entry contains no client
data, secrets, repository runtime facts, or copied target-repository code.

## Contract

- The official AI Workflow repository is the source of truth for nested
  `ai-workflow/` system files.
- A target nested clone may be equal to or behind fetched upstream and may be
  changed only by canonical fast-forward synchronization.
- `ahead` and `diverged` local commits are stop conditions. The updater must
  not reset, rebase, delete, or silently merge them.
- Target-owned runtime belongs in `AI_WORKFLOW_WORKSPACE_HOME/**`; ordinary
  target work must not edit or commit nested `ai-workflow/**` system files.

## Validation Lifecycle

Full validation must expose a machine-readable lifecycle:

```text
AI_WORKFLOW_VALIDATE_START profile=<profile>
AI_WORKFLOW_VALIDATE_PROGRESS stage=<stage> check=<check>
AI_WORKFLOW_VALIDATE_COMPLETE profile=<profile> result=<pass|fail|timeout|interrupted>
```

The completion marker is emitted exactly once for a valid run. A timeout or
interruption is not PASS. Long smoke runs report the active test ID and use a
process-group timeout without shell interpolation.

## Adaptation Checklist

- Preserve full-profile smoke coverage and existing smoke IDs.
- Add canonical upstream relation detection before merge.
- Keep `update-workspace` separate and target-owned.
- Add start, progress, completion, timeout, and skipped-validation evidence.
- Treat green scripts as supporting evidence; semantic QA and PASS Integrity
  remain authoritative.
- Add adversarial tests for equal, behind, ahead, diverged, failure, timeout,
  interruption, skip, and workspace non-mutation.

## Evidence Boundary

This handoff is advisory External Memory. It does not grant write permission,
change phase gates, or authorize changes in `ai-system`.
