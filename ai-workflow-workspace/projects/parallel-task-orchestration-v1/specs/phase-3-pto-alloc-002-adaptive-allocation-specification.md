# Task Specification: PTO-ALLOC-002-adaptive-allocation
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-ALLOC-002-adaptive-allocation
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: ready after current Spec QA; see reviews/pto-002-prewrite-readiness.md
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual dependency outputs do not exist yet; before implementation refresh this spec against predecessor output rather than claiming those dependencies are satisfied.

## Task Contract
- Goal: Compute conservative parallel-ready units and explain worker count.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-002-AC1: Reject duplicate IDs, cycles, missing dependencies, unsafe paths and unknown access modes.
  - PTO-002-AC2: Planner selects a deterministic conflict-free ready set under observed capacity minus all active workers and resource reservations.
  - PTO-002-AC3: Read/write, write/write and parent/child paths conflict; read/read may run concurrently; unknown resources default exclusive.
  - PTO-002-AC4: Zero ready units reports blocked/complete accurately; one unit uses serial; no hard-coded two/three limit.
  - PTO-002-AC5: Plan CLI is read-only and emits structured reasoned proposals, not authorization or dispatch.
- Dependencies: blocking PTO-CORE-001-contract-routing; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: False independence or over-allocation.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- .systems/scripts/lib/parallel-orchestration.py
- .systems/scripts/plan-parallel-work
- .systems/ai/templates/orchestration/run.template.json
- .systems/ai/templates/orchestration/unit.template.json
- .systems/scripts/smoke/core.sh
- .systems/scripts/smoke/manifest.json
- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/lib/parallel-orchestration-tests.py
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
Use Python standard library, schema-1 JSON with unknown keys/types rejected. CLI --manifest <file> --format json|human; no shell commands in manifest executed. Reuse existing smoke group rather than adding a public group name. Put new tests in lib/parallel-orchestration-tests.py invoked from supplemental core smoke IDs; preserve all five group names and frozen regions. Update only supplemental manifest entries and current file hashes.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-002-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-002-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-002-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-002-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. Implement strict JSON schema parsing in lib/parallel-orchestration.py, rejecting duplicate keys, booleans-as-integers, unknown fields, invalid paths and missing identities.
2. Plan CLI: plan-parallel-work --manifest <path> --format json|human. Exit 0 for valid serial/parallel proposal, 2 for invalid input. Return state blocked with reasons for no eligible work; never execution_authorized=true.
3. Stable ready-order is dependency topological order, then declared priority and unit ID. Cycles/missing nodes are invalid. All formal task prerequisites must be externally reviewed and source-bound; a manifest flag is not proof of approval.
4. Compare canonical read/write paths including directory prefixes and realpath containment; nonexisting outputs resolve closest existing parent. Reserved shared resources use explicit shared-read/exclusive modes; unknown is exclusive.
5. selected_workers = at most verified free capacity and conflict-free ready units; no verified capacity means serial proposal. Observe active workers from whole execution run; never subtract only current task's workers.
6. Output includes proposed units, selected count, serial/parallel mode, observed limits, rejected candidates and reasons. No manifest write/spawn from planner.
7. Reserve parent task slots before dispatch: remaining checkpoint slots = 3 minus completed-since-checkpoint minus distinct active tasks in the current epoch. Multiple units of one task consume one task slot. Never dispatch a fourth distinct task before the checkpoint, even when the first three are still running. An unknown checkpoint state blocks task dispatch, not read-only review.

### Deterministic Examples
Four independent units within one approved task, verified free capacity four and disjoint resources -> select four.
Same input with two active worker slots from the shared pool -> select at most two.
Chain A -> B -> C with no accepted outputs -> select A only.
Unaccepted A result -> B remains blocked. Accepted immutable A -> B may become ready if its other gates hold.
Two tasks completed since checkpoint and one distinct active task -> no new task; another safe unit of the active task may run within available capacity.
Unknown capacity/isolation -> serial proposal with reason, never assume zero risk or unlimited workers.

## Dependency Status
PTO-001 has accepted formal Quality PASS and Phase 6 with unchanged source snapshot.
Fresh prerequisite review: reviews/pto-002-prewrite-readiness.md. Planner proposals
remain non-authorizing; cross-task dependencies retain separate formal gates.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-002-T1 | Chain, diamond and independent DAGs; capacity zero/one/four/unknown; active parent pool already consuming capacity. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-002-T2 | Path traversal, symlink, absolute path, directory-prefix overlap, lockfile/cache/port/DB clashes. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-002-T3 | Missing required capability or unknown write isolation chooses serial; deterministic same-input output. | asserted required behavior and unchanged forbidden state; failures reported |
- Offline behavioral entrypoint to be implemented: python3 .systems/scripts/lib/parallel-orchestration-tests.py --case planner. PTO-001 uses its registered policy smoke cases before the helper is introduced by PTO-002; PTO-007 uses document/handoff review rather than claiming a guidance subcommand.
- Relevant smoke category: core supplemental tests, preserving existing manifest and all old IDs.
- Targeted contract check: .systems/scripts/check-parallel-task-orchestration (new in PTO-001).
- Final source gate after semantic QA: .systems/scripts/validate-workflow --profile full --project parallel-task-orchestration-v1 --explain.
- These are future implementation checks, not checks executed during specification.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Valid approved unit and compatible inputs | scoped owned execution/evidence | task-specific output satisfying AC | authority expansion or extra writes | reject unsafe extension | task tests above | follow producer through consumer for successful unit |
| Missing/stale input, competing owner or failed evidence | blocked/unknown | reason and preserved evidence | accepted/PASS despite missing proof | stop dependent work, preserve independent results | task negative cases | follow one failure to rejection without side effects |
Planning defines these flows; runtime traces will be evidence from implementation, not invented here.

## Potential Errors And Edge Cases
Missing backend -> safe serial/blocked. Duplicate attempt -> reject. Malformed JSON/path -> reject without writes.
Unrelated file drift -> classify scope; affected baseline -> invalidate evidence. Submitted result -> no automatic acceptance.
Tests pass but DoD mismatch -> fix-loop, not PASS. Operator opt-out cannot supply a required gate.

## User Decisions
PTO-D01 dynamic count; PTO-D02 isolation/integration QA; PTO-D03 handoff; PTO-D04 no delivery deadline/timebox; PTO-D05 planning only.
Future high-risk implementation approval is required; live synthetic worker/backend check requires applicable runtime permissions. No additional planning question is needed.

## Assumptions And Revalidation
Standard library and existing shell entrypoints suffice; verify before writes. Platform backend support is unknown until observed.
Safe serial fallback is mandatory. A future unsupported backend does not justify false native-support or performance claims.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: task AC above, accepted context and project plan
- Testable DoD / acceptance conditions: all PTO-002-AC items and specified failure/compatibility tests
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after this specification is complete; repeat if predecessor changes its assumptions
- Implementation Quality Closure route: phase-5-quality
- Required verification: automated task regressions, manual success/failure trace, intent/DoD/current-diff review, applicable full supporting source validation.
- Quality-ready criteria: exact scope and consumer contracts, tests available, no unresolved material findings, current evidence and required owner approval.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: high-risk implementation approval; not required to finish this artifact QA
- Next route: phase-3-spec-qa

## Implementation Gate
- DoD complete and testable: yes
- Dependencies satisfied or explicitly gated: yes
- Required user decisions resolved: yes, accepted implementation-range approval and current continuation
- Can enter implementation: yes after refreshed Spec QA and runtime preflight
- Blocking reason: none for this task after preflight; future native dispatch is not authorized by planner output

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Source: owner explicitly requested no deadline or timebox for this project.
- Must-have outcome: safe dynamic delegation, single execution owner, integrated QA.
- Cutline/deferred scope: scheduler, recursive delegation, production effects and AI System implementation.
- Quality floor: current artifact QA, scoped evidence, no unresolved material findings.
- Overrun checkpoint: stop for new scope or permissions, never invent a delivery deadline.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D01 through PTO-D05
- Questions asked: none; prior owner answers remain applicable.
- Auto-resolved reversible decisions: canonical artifact names and serial planning.
- Optional owner refinements: none required for planning.
- Decision artifacts: decisions/owner-decisions.md
- Next route: artifact-specific gate; implementation approval remains separate.

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: preserve ownership and safety decisions.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Dynamic orchestration without duplicate authority
- Suggested entry summary: Single execution owner and evidence-backed integration; final AI System handoff after actual QA.
