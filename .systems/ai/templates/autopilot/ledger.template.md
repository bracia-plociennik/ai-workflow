# ledger.md

Purpose: append-only operational ledger for one autopilot run.

Each entry should be appended. Do not rewrite history except to correct an obvious typo, and record corrections as new entries when they affect meaning.

## Entries

```yaml
- at: null
  event-type: phase-started # readiness-started | readiness-completed | phase-started | phase-completed | decision | qa-result | fix-loop | checkpoint | drift | escalation | recovery | final-approval
  task-id: null
  task-name: null
  phase: null
  result: null # PASS | FAIL | completed | blocked | STOP | n/a
  artifact: null
  readiness-result: null # draft | blocked | awaiting-owner | ready | superseded | n/a
  evidence:
    commands: []
    manual-checks: []
    artifacts: []
  decisions: []
  drift: []
  next-transition: null
  notes: null
```
