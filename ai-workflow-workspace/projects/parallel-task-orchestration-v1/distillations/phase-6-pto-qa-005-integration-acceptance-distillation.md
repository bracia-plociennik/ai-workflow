# PTO-005 Distillation

## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-QA-005-integration-acceptance
- Date: 2026-10-04
- Workflow phase: phase-6-distillation
- Quality artifact: quality/phase-5-pto-qa-005-integration-acceptance-quality.md
- Result: completed
- memory-in-repo-memory: true

## What Was Done
Accepted results are bound to actual immutable copied inputs and serial destination
before/after proof. CAS reservations persist until verified integration or explicit
known-effects abandonment. Existing formal parent QA/capture remain required.

## Problems Encountered
Consumer-selected subsets, extra directory entries and resurrected deletions can
hide invalid inputs. Repeated integration can launder prior destination drift.
Physical root replacement can preserve bytes while invalidating provenance.
All material findings were fixed with real filesystem negatives and fresh review.

## Decisions
Cover the entire relevant producer-owned consumer-read namespace, with hashes,
modes, unchanged files and tombstones. Reject unexplained entries. Recheck previous
verified destinations and review evidence before the next preparation as well as
parent completion/checkpoint. A later baseline cannot make unreviewed drift safe.

## Rules For Future Tasks
Audit actual consumers, directory enumeration and sequential state transitions.
Record semantic acceptance separately from integration metadata. Unknown effects
retain reservations; no automatic rollback, retry, copy, Git operation or PASS.
Cross-task delivery remains an external formal gate, not a helper shortcut.

## Memory Candidate
Project memory updated with lifecycle/integration facts and native-support limits.
Repo memory remains deferred to the next required checkpoint (current cadence 2/3).

## System Insight Candidate
None; reusable lessons remain inside the approved project capture.

## External Workflow Memory Candidate
One final AI System handoff remains PTO-007 work after PTO-006 actual capability
and evaluation evidence. No native capability or counterpart deployment inferred.

## Evidence
Current formal Quality, reviews/pto-005-quality-review.md, parent filesystem tests
planner25/protocol12/lifecycle23/integration17 and independent post-fix review.
Full source gate003 passed: exit0, 703 seconds, five groups and 744 smoke IDs.
Source receipt /tmp/pto-005-full-source-003.json; two interrupted runs are history.

## Distillation Gate
- Captures reusable knowledge: yes
- Avoids local noise: yes
- Ready for checkpoint processing: yes

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: approved conditional high-risk Quality and continuation
- Questions asked: none
- Auto-resolved reversible decisions: compact evidence-only capture
- Optional owner refinements: none
- Decision artifacts: decisions/pto-quality-range-approval.md
- Next route: PTO-006 readiness; checkpoint cadence 2/3

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: preserve input and integration integrity without raw observations
- Owner decision required: no
- Owner decision: defer-to-checkpoint
- Privacy/scope check: pass
- Suggested entry title: New baselines cannot launder drift
- Suggested entry summary: Verify exact copied inputs and prior integrated state before proceeding.
