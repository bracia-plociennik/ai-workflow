# AUTOPILOT_STATE.md

Purpose: runtime state for Codex Autopilot in one active docs workspace.

This file records state. It does not replace `STATUS.md`, `docs/ai/workflow/`, `WORKFLOW.md`, `AGENTS.md`, or repository state.

```yaml
autopilot:
  mode: none # supervised | semi_autonomous | autonomous_execution
  status: not_running # not_running | running | stopped | awaiting_owner | completed
  active_docs_workspace: <what_we_doing>
  started_at: null
  updated_at: null

current:
  task_id: null
  task_name: null
  phase: null
  phase_artifact: null
  last_stable_pass: null
  next_transition: null

retry_counts:
  spec_qa_for_current_task: 0
  quality_for_current_task: 0
  total_for_run: 0

budget:
  max_runtime_minutes: 300
  max_spec_retries_per_task: 2
  max_quality_retries_per_task: 2
  max_total_retries: 32
  max_parallel_tasks: 1
  started_at: null
  status: not_started # ok | warning | exceeded | not_started

progress:
  completed_tasks: []
  completed_distillations_since_checkpoint: 0
  last_checkpoint: null
  final_checkpoint_required: true

blockers: []

recovery:
  last_recovery_check_at: null
  last_recovery_result: null
```
