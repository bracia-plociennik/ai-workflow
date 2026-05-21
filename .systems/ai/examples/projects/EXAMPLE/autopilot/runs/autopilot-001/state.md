# state.md - EXAMPLE

Purpose: example runtime state for one autopilot run. Not an active autopilot run.

```yaml
autopilot:
  mode: supervised
  status: not-running
  active-project: EXAMPLE
  started-at: null
  updated-at: 2026-05-16

current:
  task-id: EX-01
  task-name: Example Task
  phase: 4. FAZA IMPLEMENTACJI
  phase-artifact: .systems/ai/examples/projects/EXAMPLE/specs/phase-3-ex-01-example-task-specification.md
  last-stable-pass: 3.5. SPEC QA
  next-transition: 4. FAZA IMPLEMENTACJI

retry-counts:
  spec-qa-for-current-task: 0
  quality-for-current-task: 0
  total-for-run: 0

budget:
  max-runtime-minutes: 300
  status: not-started

progress:
  completed-tasks: []
  completed-distillations-since-checkpoint: 0
  last-checkpoint: null
  final-checkpoint-required: true

blockers:
  - example workspace only
```
