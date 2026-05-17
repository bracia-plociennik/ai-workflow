# AUTOPILOT_LEDGER.md

Purpose: append-only operational ledger for one autopilot run.

Each entry should be appended. Do not rewrite history except to correct an obvious typo, and record corrections as new entries when they affect meaning.

## Entries

```yaml
- at: null
  event_type: phase_started # phase_started | phase_completed | decision | qa_result | fix_loop | checkpoint | drift | escalation | recovery | final_approval
  task_id: null
  task_name: null
  phase: null
  result: null # PASS | FAIL | completed | blocked | STOP | n/a
  artifact: null
  evidence:
    commands: []
    manual_checks: []
    artifacts: []
  decisions: []
  drift: []
  next_transition: null
  notes: null
```
