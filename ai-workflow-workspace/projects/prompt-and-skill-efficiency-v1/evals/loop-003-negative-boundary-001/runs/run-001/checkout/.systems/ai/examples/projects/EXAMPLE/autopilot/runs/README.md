# runs

## Purpose

This directory stores autopilot runtime runs.

Each run has its own directory:

```text
autopilot-001/
  README.md
  state.md
  ledger.md
  events.md
```

## Rules

- Create a new run directory for each independent autopilot run.
- Use monotonic names: `autopilot-001`, `autopilot-002`, and so on.
- Do not mix state, ledger, or events from different runs.
- The active run is recorded in `../README.md` and project status.
