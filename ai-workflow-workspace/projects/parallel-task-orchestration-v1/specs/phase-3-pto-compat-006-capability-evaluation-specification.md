# Task Specification: PTO-COMPAT-006-capability-evaluation
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-COMPAT-006-capability-evaluation
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: conditional
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual dependency outputs reviewed on 2026-10-04: PTO-005 formal Quality PASS,
accepted Phase 6/capture and full source gate003 (703 seconds, 744 IDs).
Readiness: reviews/pto-006-prewrite-readiness.md. Native authorization remains separate.

## Task Contract
- Goal: Expose tested support conservatively and measure integrated behavior.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-006-AC1: Schema-1 coordinator output remains compatible; schema-2 is explicit opt-in and always execution_authorized=false.
  - PTO-006-AC2: Capability distinguishes installed protocol/modes/schemas from backend isolation/capacity and owner permission.
  - PTO-006-AC3: Unknown/malformed/version mismatch causes conservative fallback; no nested update.
  - PTO-006-AC4: Offline common fixtures cover authority, conflicts, ordering, recovery and failure paths; original smoke IDs remain exactly once.
  - PTO-006-AC5: At least three paired serial/parallel synthetic samples use same work/assertions; report total, integration, rework, conflicts and quality; no invented speedup.
  - PTO-006-AC6: Ship installed protocol capability with native operational support unverified and not authorized; missing or unverified isolation must prohibit native dispatch. Native backend verification is explicitly deferred to a separate owner-approved follow-up; no model/native speedup or isolation claim is part of this release.
- Dependencies: blocking PTO-QA-005-integration-acceptance; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: False capability announcement or benchmark overclaim.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- .systems/ai/capabilities/parallel-task-orchestration-v1.json
- .systems/scripts/lib/coordinator-status.py
- .systems/scripts/report-coordinator-status
- .systems/ai/core/runtime-integrity.md
- .systems/scripts/check-parallel-task-orchestration
- .systems/scripts/smoke/core.sh
- .systems/scripts/smoke/manifest.json
- .systems/scripts/lib/parallel-orchestration-tests.py
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
No model-based eval or live worker test is approved by this planning-range. Later implementation readiness must establish safe native backend test authorization or record a blocker. No fixed model chosen.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-006-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-006-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-006-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-006-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. Extend coordinator CLI --schema-version choices to 1|2, default 1. Schema-1 output remains unchanged. Schema-2 adds installed parallel capability/protocol, unit/result schemas and supported modes, alongside existing current QA/status.
2. Keep execution_authorized false in both schemas, including verified QA PASS. Capability must not implicitly acknowledge owner approval.
3. Add capability file only after tasks 1-5 checks and integrated review. Malformed/missing/version-unknown capability yields unsupported/unknown serial recommendation; never infer from branch name/date alone.
4. Run offline protocol compatibility cases and integrated failure fixtures using real local temp file behavior; fake platform handles are labelled simulated.
5. At least three paired serial/parallel samples with identical synthetic work, resource assumptions, assertions and start/end boundaries. Record wall-time including setup/integration/rework, active workers, conflicts, quality and failures; disclose no-improvement and sample limits.
6. Native backend smoke is explicitly deferred by PTO-D06 after failed preflight.
   Release capability records unverified native support and zero tested backends;
   serial fallback never dispatches a native worker. Later verification needs a
   separately approved compatible isolated backend; no simulated/model speedup.
7. Compare smoke ID inventory with source baseline: each old ID exactly once, supplemental entries unique, all five public groups retained. Full profile/CI still exercise all groups.

## Dependency Status
PTO-005 accepted current integration/delivery interfaces and formal gates are
available. Eight source paths and AC1..AC6 remain unchanged after comparison with
actual predecessors. Bounded native authorization is approved on 2026-10-04,
but direct preflight cannot confirm exclusive worker isolation. See
reviews/pto-006-native-backend-preflight.md. PTO-D06 subsequently approves the
protocol-only release and explicitly replaces AC6; original eight paths unchanged.
Native verification remains unverified/deferred, not a release prerequisite now.
No worker launch or native completion is inferred from artifact Spec QA.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-006-T1 | Old consumer/new provider and new consumer/old provider; unknown protocol; capabilities cannot grant permissions. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-006-T2 | Offline failure injection across planner/lifecycle/integration plus original smoke inventory equivalence. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-006-T3 | Paired samples with failures and no-improvement retained; actual model-run overhead not inferred from fake adapter. | asserted required behavior and unchanged forbidden state; failures reported |
- Offline behavioral entrypoint to be implemented: python3 .systems/scripts/lib/parallel-orchestration-tests.py --case compatibility. PTO-001 uses its registered policy smoke cases before the helper is introduced by PTO-002; PTO-007 uses document/handoff review rather than claiming a guidance subcommand.
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
High-risk implementation and conditional Phase5 approval are recorded. The
bounded native decision is now approved, with maximum two synthetic invocations
and stop if exclusive /tmp isolation is unconfirmed. Direct preflight stopped:
observed isolation is unverified. Permission does not supply that observation.

## Assumptions And Revalidation
Standard library and existing shell entrypoints suffice; verify before writes. Platform backend support is unknown until observed.
Safe serial fallback is mandatory. A future unsupported backend does not justify false native-support or performance claims.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: task AC above, accepted context and project plan
- Testable DoD / acceptance conditions: all PTO-006-AC items and specified failure/compatibility tests
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after this specification is complete; repeat if predecessor changes its assumptions
- Implementation Quality Closure route: phase-5-quality
- Required verification: automated task regressions, manual success/failure trace, intent/DoD/current-diff review, applicable full supporting source validation.
- Quality-ready criteria: exact scope and consumer contracts, tests available, no unresolved material findings, current evidence and required owner approval.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none; PTO-D06 approved protocol-only release, artifact QA required before writes
- Next route: phase-3-spec-qa

## Implementation Gate
- DoD complete and testable: yes
- Dependencies satisfied or explicitly gated: yes
- Required user decisions resolved: yes, bounded native test plan now approved; required isolation observations remain unverified
- Can enter implementation: yes, current revised Plan QA/Spec QA and readiness recorded
- Blocking reason: none for protocol-only writes; native dispatch still forbidden

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
- Material decisions: none; native permission and prior PTO-D01 through PTO-D05 resolved
- Questions asked: none; prior owner answers remain applicable.
- Auto-resolved reversible decisions: canonical artifact names and serial planning.
- Optional owner refinements: none required for planning.
- Decision artifacts: decisions/owner-decisions.md; decisions/pto-006-native-backend-authorization.md; decisions/pto-006-007-protocol-only-scope.md
- Next route: fresh Plan QA and Spec QA, then protocol-only implementation; no native dispatch

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: preserve ownership and safety decisions.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Dynamic orchestration without duplicate authority
- Suggested entry summary: Single execution owner and evidence-backed integration; final AI System handoff after actual QA.
