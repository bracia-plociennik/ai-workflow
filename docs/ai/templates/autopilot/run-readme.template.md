# <autopilot-run-id>

## Purpose

Runtime directory for one autopilot run.

## Runtime Files

- `state.md` - current run state.
- `ledger.md` - append-only operational ledger for this run.
- `events.md` - owner-facing event log for this run.

## Status

| Field | Value |
| --- | --- |
| Run ID | `<autopilot-001>` |
| Status | `<not-running|running|stopped|awaiting-owner|completed>` |
| Active | `<yes|no>` |
