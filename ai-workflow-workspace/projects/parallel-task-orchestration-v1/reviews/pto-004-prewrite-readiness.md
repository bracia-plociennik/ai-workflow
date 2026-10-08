# PTO-004 Pre-Write Readiness

- Date: 2026-10-04
- Baseline: 8a0eeef with approved PTO-001..003 source, full 645 seconds/742 IDs.
- Predecessor: current PTO-003 formal Quality, Phase 6 and first checkpoint accepted.
- Sources: accepted architecture, plan, eight-path spec, current contracts/status.
- Approvals: implementation-approval and pto-quality-range-approval; no commit/push.
- Work mode: formal project/workflow-maintenance; risk high.
- Delivery: owner-opt-out; no deadline/timebox.
- Skills used: none.
- DoD: PTO-004 AC1..AC6, including CAS/lock/crash/recovery and sanitized inventory.
- Slice plan: strict lifecycle schema; bounded atomic utility/tests; fresh semantic
  current-diff and regression review, formal Phase 5 plus full supporting checks.
- Design: optional lifecycle metadata preserves old allocator manifests; one atomic
  manifest transaction contains revision, reservations and events. No automatic
  worker execution, cleanup, external effects or stale-lock deletion.
- Unknown parent retry budget blocks retry. Unknown worker liveness retains slots.
- Canonical inventory includes only closed sanitized manifest/result records;
  raw observations/prompts/logs/worktrees remain outside the active namespace.
- Artifact QA: fresh Spec QA after actual predecessor review.
- Post-implementation Quality: phase-5-quality with all AC, producer-consumer and
  adversarial review plus offline lifecycle tests and full source validation.
- Native backend/authenticity and malicious host remain unverified; this is not
  a sandbox, scheduler or transport.
- Stop: extra paths, missing permission/gate, unclear reconciliation or unsafe action.
