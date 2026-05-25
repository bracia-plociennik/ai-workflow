# <autopilot-run-id>

## Purpose

Runtime directory for one autopilot run.

## Runtime Files

- `readiness.md` - required pre-start and pre-resume readiness audit.
- `state.md` - current run state.
- `ledger.md` - append-only operational ledger for this run.
- `events.md` - owner-facing event log for this run.

## Status

| Field | Value |
| --- | --- |
| Run ID | `<autopilot-001>` |
| Status | `<not-running|running|stopped|awaiting-owner|completed>` |
| Readiness | `<draft|blocked|awaiting-owner|ready|superseded>` |
| Active | `<yes|no>` |
