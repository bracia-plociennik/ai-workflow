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
| Range | `<planning-range|implementation-range>` |
| Status | `<not-running|running|stopped|awaiting-owner|completed>` |
| Readiness | `<draft|blocked|awaiting-owner|ready|superseded>` |
| Start phase | `<phase-1-architecture|phase-4-implementation|current-stable-phase>` |
| Stop phase | `<phase-3-spec-qa|phase-7-checkpoint>` |
| Stop condition | `<all-planned-specs-pass|final-checkpoint-complete|owner-stop|blocked>` |
| Phase 8 | `owner-triggered-only` |
| Active | `<yes|no>` |
