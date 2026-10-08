# Task Specification: PTO-CORE-001-contract-routing
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-CORE-001-contract-routing
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: conditional
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual dependency outputs do not exist yet; before implementation refresh this spec against predecessor output rather than claiming those dependencies are satisfied.

## Task Contract
- Goal: Align installed execution contracts around one orchestrator and delegated units.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-001-AC1: One coordinator-owned implementation run can delegate units without creating independent autopilots.
  - PTO-001-AC2: Dynamic parallelism is gated by dependencies, resources, backend capability and approval; missing capability stays serial.
  - PTO-001-AC3: Packaging remains optional; no per-unit checkpoint, full workflow or formal PASS.
  - PTO-001-AC4: Existing default-policy validators and smoke expectations stay aligned; safe prohibition plus unsafe exception fails.
- Dependencies: blocking none; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Authority weakening or contradictory installed policy.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- .systems/ai/core/parallel-task-orchestration.md
- .systems/ai/core/parallel-work-policy.md
- .systems/ai/core/autopilot.md
- .systems/ai/core/implementation-slicing.md
- .systems/ai/core/command-routing.md
- .systems/ai/core/operating-model.md
- .systems/ai/core/workflow.md
- .systems/ai/workflow/phase-2-project-plan.md
- .systems/ai/templates/autopilot/readiness.template.md
- .systems/ai/templates/autopilot/state.template.md
- .systems/scripts/check-parallel-task-orchestration
- .systems/scripts/lib/validation-checks.json
- .systems/scripts/validate-workflow
- .systems/scripts/check-required-artifacts
- .systems/scripts/smoke/core.sh
- .systems/scripts/smoke/manifest.json
- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/check-review-completeness-gate
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
Keep feature capability inactive until PTO-006. Shared validation registry modifications are bounded to registering this contract check.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-001-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-001-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-001-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-001-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. Inventory every routing consumer of parallel-work, serial autopilot and slicing. Preserve default serial behavior for absent capability.
2. Define one execution owner and unit-not-task model in parallel-task-orchestration.md. Explicitly retain separate implementation-range exclusion.
3. Update only listed policy/readiness/state references. Dynamic allocation field is observed run state, not a global default raising capacity; legacy max-parallel-tasks: 1 remains valid.
4. Add check-parallel-task-orchestration using policy-boundaries.sh for enabling-clause rejection, including negation plus unsafe exception on one line. Register with validation-checks.json, runner, required artifacts, completeness audit and smoke coverage index.
5. Keep capability advertisement absent until PTO-006. Add supplemental core policy smoke tests without modifying historical frozen regions.

## Dependency Status
No task predecessor. Implementation still waits for separate high-risk approval and runtime preflight.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-001-T1 | Reject dual implementation-range owners and subagent permission escalation; retain valid serial route. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-001-T2 | Reject gate-skipping, automatic push and unsafe compound policy wording. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-001-T3 | Review every serial/parallel instruction and validator consumer; no contradictory blanket serial rule for capable delegated runs. | asserted required behavior and unchanged forbidden state; failures reported |
- Policy tests: registered supplemental core smoke cases invoke check-parallel-task-orchestration against isolated mutated contract fixtures. Behavioral helper is introduced by PTO-002, not required from a future task.
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
- Testable DoD / acceptance conditions: all PTO-001-AC items and specified failure/compatibility tests
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
- Required user decisions resolved: no, implementation approval not requested in this planning range
- Can enter implementation: no
- Blocking reason: separate implementation readiness/approval and prerequisite refresh required

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
