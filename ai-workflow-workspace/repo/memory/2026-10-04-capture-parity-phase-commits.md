# Capture And QA Binding Commands

- Date: 2026-10-04
- Project: parallel-task-orchestration-v1
- Baseline: 8a0eeef, approved uncommitted PTO001..009 source.

Shared capture reader: .systems/scripts/lib/capture-record.py.
Bound commit verifier: .systems/scripts/verify-qa-commit-binding.
Binding regressions: .systems/scripts/tests/phase-commit-policy.py.
Current source gate receipt: /tmp/pto-009-full-source-002.json, authenticated locally.
Current owned artifact closure is required after every final runtime write;
source equivalence alone does not validate updated project status or capture.

Source full002 passed685seconds,44checks,757IDs,fivegroups. No source commit or
push has been made. Ignored memory is not forced into Git. V2 and historical
schema1 retain their existing limits; V3/schema3 is opt-in, current-only.
Native backend support remains unverified. Target installations are untouched.
