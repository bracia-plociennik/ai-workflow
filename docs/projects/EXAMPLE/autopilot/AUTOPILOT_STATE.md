# AUTOPILOT_STATE.md - EXAMPLE

Purpose: example runtime state. Not an active autopilot run.

```yaml
autopilot:
  mode: supervised
  status: not_running
  active_docs_workspace: EXAMPLE
  started_at: null
  updated_at: 2026-05-16

current:
  task_id: EX-01
  task_name: Example Task
  phase: 4. FAZA IMPLEMENTACJI
  phase_artifact: docs/projects/EXAMPLE/specs/3_EX-01_example-task_specification.md
  last_stable_pass: 3.5. SPEC QA
  next_transition: 4. FAZA IMPLEMENTACJI

retry_counts:
  spec_qa_for_current_task: 0
  quality_for_current_task: 0
  total_for_run: 0

budget:
  max_runtime_minutes: 300
  status: not_started

progress:
  completed_tasks: []
  completed_distillations_since_checkpoint: 0
  last_checkpoint: null
  final_checkpoint_required: true

blockers:
  - example workspace only
```
