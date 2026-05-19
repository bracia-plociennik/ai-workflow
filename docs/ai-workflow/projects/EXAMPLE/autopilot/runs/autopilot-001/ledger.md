# ledger.md - EXAMPLE

Purpose: example append-only ledger for one autopilot run. Not an active autopilot run.

```yaml
- at: 2026-05-16
  event-type: phase-started
  task-id: EX-01
  task-name: Example Task
  phase: 4. FAZA IMPLEMENTACJI
  result: n/a
  artifact: docs/ai-workflow/projects/EXAMPLE/specs/phase-3-ex-01-example-task-specification.md
  evidence:
    commands: []
    manual-checks:
      - EXAMPLE artifact exists
    artifacts:
      - docs/ai-workflow/projects/EXAMPLE/status.md
  decisions: []
  drift: []
  next-transition: 5. FAZA JAKOŚCI
  notes: Example ledger entry only.
```
