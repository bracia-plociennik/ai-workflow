# state.md

## Phase Commit Boundary
- Commit disposition: <permitted|forbidden|not-required|blocked>
- Approved tracked scope: <paths|none>
- Current QA source binding: <strict-current|verified-v3|refresh-required>
- Fresh artifact closure: <evidence|pending>
- Push authority: <explicit-reference|none>
- Owner approval / no-commit override: <reference>
- Cross-system impact decision: <yes|no|pending>
- Branch ownership / index isolation: <evidence>
- Result commit: <actual-SHA|none>

Use phase-commit-policy.md. This template grants no Git authority; pending proof,
explicit no-commit, ignored-only/no-op and missing final-owner-yes preserve their
required boundary. Actual result SHA is recorded only after successful commit.

Purpose: runtime state for one Codex Autopilot run.

Delegated units use `.systems/ai/core/parallel-task-orchestration.md` and one scoped
ledger. Keep task-level state single-writer; the legacy serial budget remains valid.
Record observed allocation in the ledger, not a fabricated global capacity.

This file records state. It does not replace `status.md`, `.systems/ai/workflow/`, `.systems/ai/core/workflow.md`, `AGENTS.md`, or repository state.

```yaml
autopilot:
  run-id: <autopilot-001>
  mode: none # supervised | semi-autonomous | autonomous-execution
  range: none # planning-range | implementation-range | none
  status: not-running # not-running | running | stopped | awaiting-owner | completed
  active-project: <project>
  readiness-artifact: null
  readiness-result: draft # draft | blocked | awaiting-owner | ready | superseded
  owner-actions-status: not-started # not-started | pending | resolved | not-applicable
  start-phase: null
  stop-phase: null
  stop-condition: null
  started-at: null
  updated-at: null

current:
  task-id: null
  task-name: null
  phase: null
  phase-artifact: null
  last-stable-pass: null
  next-transition: null

execution:
  mode: auto # auto | human-coop; independent of autopilot.mode
  scope: task # task | project | session
  scope-id: <owner-approved-scope-id>
  source: <explicit-choice-or-new-work-default>
  approval-reference: <actual-owner-scope-reference>
  readiness-projection: <optional-execution-readiness-json-path-or-none>
  completed-units: []
  blocked-units: []
  pending-decisions: []

retry-counts:
  spec-qa-for-current-task: 0
  quality-for-current-task: 0
  total-for-run: 0

budget:
  max-runtime-minutes: null # no implicit timebox; preserve explicit/legacy limits on resume
  max-spec-retries-per-task: 2
  max-quality-retries-per-task: 2
  max-total-retries: 32
  max-parallel-tasks: 1
  started-at: null
  status: not-started # ok | warning | exceeded | not-started

progress:
  completed-tasks: []
  completed-distillations-since-checkpoint: 0
  checkpoint-required-now: false
  last-checkpoint: null
  final-checkpoint-required: true
  final-check-owner-only: true

blockers: []

recovery:
  projection-schema: 2
  attempts: [] # attempt_id, unit_id, stable cause_id, progress_evidence SHA-256 or null
  stalled-units: [] # excludes dependents/shared reservations; meaningful progress must be verified
  history-source: <current-persisted-attempts-and-retry-counts>
  last-recovery-check-at: null
  last-recovery-result: null
```
