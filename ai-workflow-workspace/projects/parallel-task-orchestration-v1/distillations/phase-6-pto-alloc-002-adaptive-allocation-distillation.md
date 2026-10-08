# PTO-002 Distillation

## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-ALLOC-002-adaptive-allocation
- Date: 2026-10-04
- Workflow phase: phase-6-distillation
- Quality artifact: quality/phase-5-pto-alloc-002-adaptive-allocation-quality.md
- Result: completed
- memory-in-repo-memory: true

## What Was Done
Strict read-only allocation proposals validate dependency DAG, resource/path
conflicts, the entire observed worker pool and accumulated parent checkpoint slots.
No proposal dispatches a worker or grants execution permission.

## Problems Encountered
Case folding before Unicode normalization can reorder combining marks. Normalize
before and after folding. Prefix inventories need bounded metadata scans;
hardlinks and special/linked subtrees are rejected rather than guessed safe.

## Decisions
Unknown capacity/isolation means conservative serial fallback; unknown checkpoint
state blocks new work. Cross-task unit acceptance never replaces formal task gates.
Strict schemas reject booleans as integers, duplicate JSON keys and nonfinite values.

## Rules For Future Tasks
Reobserve real backend and files before dispatch. Preserve active reservations
under uncertain liveness. Tests include directory aliases and Unicode permutations,
not only simple filename traversal. Invalid CLI input emits no valid proposal.

## Memory Candidate
Project memory: allocator is a bounded proposal engine, not an OS sandbox.

## System Insight Candidate
None; no separate durable insight write.

## External Workflow Memory Candidate
Include path normalization and conservative fallback in the one final AI System handoff.

## Distillation Gate
- Captures reusable knowledge: yes
- Avoids local noise: yes
- Ready for checkpoint processing: yes

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-002-007 Quality approved conditionally on complete evidence
- Questions asked: none
- Auto-resolved reversible decisions: concise knowledge summary
- Optional owner refinements: none
- Decision artifacts: decisions/pto-quality-range-approval.md
- Next route: PTO-003 readiness; checkpoint due after third completed task

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: preserve allocator safety constraints
- Owner decision required: no
- Owner decision: capture-now
- Privacy/scope check: pass
- Suggested entry title: Allocation is not dispatch
- Suggested entry summary: Verified capacity, canonical paths and parent task slots bound proposals
