# state.md

Purpose: runtime state for one Codex Autopilot run.

This file records state. It does not replace `status.md`, `docs/ai/workflow/`, `docs/ai/core/workflow.md`, `AGENTS.md`, or repository state.

```yaml
autopilot:
  run-id: <autopilot-001>
  mode: none # supervised | semi-autonomous | autonomous-execution
  status: not-running # not-running | running | stopped | awaiting-owner | completed
  active-project: <project>
  started-at: null
  updated-at: null

current:
  task-id: null
  task-name: null
  phase: null
  phase-artifact: null
  last-stable-pass: null
  next-transition: null

retry-counts:
  spec-qa-for-current-task: 0
  quality-for-current-task: 0
  total-for-run: 0

budget:
  max-runtime-minutes: 300
  max-spec-retries-per-task: 2
  max-quality-retries-per-task: 2
  max-total-retries: 32
  max-parallel-tasks: 1
  started-at: null
  status: not-started # ok | warning | exceeded | not-started

progress:
  completed-tasks: []
  completed-distillations-since-checkpoint: 0
  last-checkpoint: null
  final-checkpoint-required: true

blockers: []

recovery:
  last-recovery-check-at: null
  last-recovery-result: null
```
