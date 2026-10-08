# PTO-004 Distillation

## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-RUN-004-lifecycle-recovery
- Date: 2026-10-04
- Workflow phase: phase-6-distillation
- Quality artifact: quality/phase-5-pto-run-004-lifecycle-recovery-quality.md
- Result: completed
- memory-in-repo-memory: true

## What Was Done
Single-writer CAS transitions bind reservations, attempts, events and revisions.
Recovery inspects observations and actual files; finished attempts remain history.
Owned runtime inventory admits only closed manifests and referenced sanitized results.

## Problems Encountered
Review found hash-only checkpoint admission, damaged-result recovery denial,
missing result-directory fsync and completed-parent invalidation losing its slot.
All fixed with regressions and fresh parent plus independent current-diff review.
A pending capture record must not point to a future Quality report.

## Decisions
Require completed checkpoint metadata and exact run/coordinator/epoch/task binding.
Damaged results can be reported and explicitly invalidated, never trusted or adopted.
Unknown worker effects retain reservations. Retry needs current parent-budget proof.
Never delete stale locks, replay uncertain writes or infer authority from metadata.

## Rules For Future Tasks
Audit producer-consumer fields and actual transaction ordering, not only JSON keys.
Invalidating completed work revokes its gate and restores its active parent slot.
Directory fsync precedes publication of references; power-loss testing remains limited.

## Memory Candidate
Project memory at next cadence: accepted-unit history is not current task completion.

## System Insight Candidate
None; no durable write beyond owned project evidence.

## External Workflow Memory Candidate
One final AI System handoff will describe tested lifecycle and unresolved native limits.

## Evidence
reviews/pto-004-quality-review.md; 25 planner, 12 protocol and 23 lifecycle tests;
full source run 004 passed in 641 seconds with 743 unique smoke IDs.

## Distillation Gate
- Captures reusable knowledge: yes
- Avoids local noise: yes
- Ready for checkpoint processing: yes

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: approved conditional high-risk Phase 5
- Questions asked: none
- Auto-resolved reversible decisions: concise evidence-only summary
- Optional owner refinements: none
- Decision artifacts: decisions/pto-quality-range-approval.md
- Next route: PTO-005 readiness; checkpoint cadence 1/3

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: preserve recovery invariants without copying raw observations
- Owner decision required: no
- Owner decision: defer-to-checkpoint
- Privacy/scope check: pass
- Suggested entry title: Recovery does not replay authority
- Suggested entry summary: Keep immutable attempts and restore parent slots after invalidation.
