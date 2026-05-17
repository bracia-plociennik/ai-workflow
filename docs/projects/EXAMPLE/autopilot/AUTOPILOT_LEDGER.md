# AUTOPILOT_LEDGER.md - EXAMPLE

Purpose: example append-only ledger. Not an active autopilot run.

```yaml
- at: 2026-05-16
  event_type: phase_started
  task_id: EX-01
  task_name: Example Task
  phase: 4. FAZA IMPLEMENTACJI
  result: n/a
  artifact: docs/projects/EXAMPLE/specs/3_EX-01_example-task_specification.md
  evidence:
    commands: []
    manual_checks:
      - EXAMPLE artifact exists
    artifacts:
      - docs/projects/EXAMPLE/STATUS.md
  decisions: []
  drift: []
  next_transition: 5. FAZA JAKOŚCI
  notes: Example ledger entry only.
```
