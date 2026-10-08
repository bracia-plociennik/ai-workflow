# Autopilot State

autopilot:
  run-id: autopilot-002
  mode: autonomous-execution
  range: implementation-range
  status: superseded
  active-project: parallel-task-orchestration-v1
  readiness-artifact: autopilot/runs/autopilot-002/readiness.md
  readiness-result: blocked
  owner-actions-status: completed
current:
  task-id: PTO-COMPAT-006-capability-evaluation
  phase: phase-3-specification
  next-transition: phase-3-specification
progress:
  completed-tasks: [PTO-CORE-001-contract-routing, PTO-ALLOC-002-adaptive-allocation, PTO-ISO-003-isolated-delegation, PTO-RUN-004-lifecycle-recovery, PTO-QA-005-integration-acceptance]
  completed-distillations-since-checkpoint: 2
  checkpoint-required-now: false
  final-checkpoint-required: true
  final-check-owner-only: true
budget:
  max-parallel-tasks: 1
  delivery-constraints: owner-opt-out
retry-counts:
  quality-for-current-task: 0
blockers: [native-backend-isolation-unverified]
