# owner-request-batch-triage

## Summary

- Date: `2026-06-22`
- Work mode: `workflow-maintenance`
- Scope: add advisory pre-routing for owner-provided batches of work items.
- Risk: `low`
- Status: `implemented-pending-review`

## Idea Validation

### Co zostaje

- Owner lists often contain multiple unrelated scopes and should be classified before planning or implementation.
- Similar low-risk workflow improvements can be grouped into one repo-level micro-project.
- New product features, active-project tasks, and post-final corrections need separate routes.

### Co jest słabe / do poprawy lub usunięcia

- Treating a whole list as one task can hide risk, dependencies, and change request timing.
- Automatic task/project creation from a list would be unsafe because triage is not approval.

### Czego brakuje

- Validator evidence for required matrix fields, mixed-list splitting, unsafe automatic implementation wording, and high-risk routing.
- Final review after validation.

### Blokery / decyzje

- No open blocker for implementation.
- Commit remains owner-triggered after review.

### Rekomendowany routing

- Implement as a low-risk workflow-maintenance micro-project in the official `ai-workflow` repo.

## Implementation Notes

- Added `.systems/ai/core/request-batch-triage.md`.
- Routed multi-item owner requests before ordinary Task Idea Validation.
- Added human guidance and README/commands references.
- Added `.systems/scripts/check-request-batch-triage`.
- Added smoke tests to `.systems/scripts/check-validator-smoke-tests`.
- Fixed review finding P2: canonical triage matrix examples now preserve 9 columns, and the validator/smoke tests check matrix column count.

## Evidence

- `git diff --check` passed.
- `.systems/scripts/check-request-batch-triage` passed.
- `.systems/scripts/check-validator-smoke-tests` passed.
- `.systems/scripts/validate-workflow` passed.
- `.systems/scripts/check-naming` passed.
- `.systems/scripts/check-required-artifacts` passed.
- `.systems/scripts/check-status-consistency` passed.
- `.systems/scripts/check-qa-evidence` passed.
- `.systems/scripts/check-system-insights` passed.
- `.systems/scripts/check-system-skills` passed.
- `.systems/scripts/check-contract-compliance` passed.
- `.systems/scripts/check-knowledge-capture-gate` passed.
- `.systems/scripts/check-default-quality-phase-chaining` passed.
- `.systems/scripts/check-dreaming-mode` passed.
- `.systems/scripts/check-global-quality-review-stance` passed.
- `.systems/scripts/check-branch-policy` passed.
- `git ls-files ai-workflow-workspace` returned no tracked workspace files.

## Knowledge Capture

- Knowledge capture: `not-required`
- Reason: this micro-project itself documents the workflow improvement; no separate External Memory entry is needed unless review finds a reusable broader lesson.
