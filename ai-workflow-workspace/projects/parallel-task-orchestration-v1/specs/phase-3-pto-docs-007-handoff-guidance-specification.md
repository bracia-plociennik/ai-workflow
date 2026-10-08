# Task Specification: PTO-DOCS-007-handoff-guidance
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-DOCS-007-handoff-guidance
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: conditional
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual prerequisites reviewed on2026-10-04: revised PTO006 formal Quality PASS, accepted Phase6/capture and checkpoint004..006 synchronization. Full006run004 passed694seconds/43checks/745IDs. Fresh runtime closure is required before writes. Protocol-only/native-unverified distinction confirmed; six source paths and five AC unchanged.

## Task Contract
- Goal: Publish concise user guidance and one evidence-backed counterpart adaptation handoff.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-007-AC1: Entrypoints remain concise and route to one canonical orchestration contract.
  - PTO-007-AC2: Document dynamic count, one owner, nonrecursive units, QA, serial fallback and capability versions.
  - PTO-007-AC3: One privacy-safe External Memory artifact covers this scope with tested baseline, schema, limitations, source paths and adaptation checklist.
  - PTO-007-AC4: Do not claim AI System implementation or copy private runtime; no automatic counterpart update.
  - PTO-007-AC5: Final source semantic review and full validation precede publication readiness; Phase 8 still owner-only.
- Dependencies: blocking PTO-COMPAT-006-capability-evaluation; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Counterpart trusts unsupported capability or imports status/approval.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- AGENTS.md
- HUMANS.md
- README.md
- .systems/ai/core/commands.md
- .systems/ai/core/changelog.md
- .systems/ai/templates/orchestration/README.md
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
External Memory path: ai-workflow-workspace/external-memory/memory/<completion-date>-parallel-task-orchestration-ai-system-handoff.md. Runtime handoff is not tracked source. Changelog path verified as .systems/ai/core/changelog.md.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-007-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-007-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-007-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-007-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. Add concise discovery/usage pointers to AGENTS/HUMANS/README/commands and current changelog without duplicating full policy.
2. Explain single execution owner, dynamic count, unit vs task, approval gates, local evidence vs integrated QA and recovery/fallback.
3. Create one final External Memory handoff at completion-date path under workspace external-memory/memory/, documenting actual source versions, implemented fields, tested cases and unresolved runtime limitations.
4. Answer five counterpart questions: existing policy extension, one parent vs two autopilots, unit task/slice references, local/common QA and version handshake.
5. Privacy-review handoff; no approvals imported, no customer runtime or prompts. Do not modify AI System or nested clones.
6. Final semantic current-diff review followed by applicable tests and fresh full. Phase 6/7 per task cadence; commit/push and Phase 8 only by separate owner authorization.

## Dependency Status
PTO-006 revised by PTO-D06 to protocol-only discovery and offline verification;
native support is explicitly deferred/unverified. Guidance/handoff must identify
that limitation, not advertise native operational support. Actual PTO006 Quality
and capture are available; execution still waits for fresh checkpoint closure,
Spec QA and readiness; original six
source paths and five AC unchanged.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-007-T1 | Guidance agrees with executable modes and schema defaults; examples use existing task references not duplicate tasks. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-007-T2 | Handoff answers all five AI System questions and includes actual verified outcomes/skips. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-007-T3 | Privacy review; no client data, secret prompts, unsupported native claims or inherited approvals. | asserted required behavior and unchanged forbidden state; failures reported |
- Guidance verification: manually trace each documented command and handoff claim to implemented contract, current tests and installed capability; run check-cross-system-upgrade-handoff and new contract validator. No fictional guidance test subcommand.
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
Existing high-risk implementation and conditional Quality approvals plus PTO-D06 apply. No live worker/backend test is planned or permitted without genuine isolation and separate applicable gates. No additional planning question is needed.

## Assumptions And Revalidation
Standard library and existing shell entrypoints suffice; verify before writes. Platform backend support is unknown until observed.
Safe serial fallback is mandatory. A future unsupported backend does not justify false native-support or performance claims.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: task AC above, accepted context and project plan
- Testable DoD / acceptance conditions: all PTO-007-AC items and specified failure/compatibility tests
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after this specification is complete; repeat if predecessor changes its assumptions
- Implementation Quality Closure route: phase-5-quality
- Required verification: automated task regressions, manual success/failure trace, intent/DoD/current-diff review, applicable full supporting source validation.
- Quality-ready criteria: exact scope and consumer contracts, tests available, no unresolved material findings, current evidence and required owner approval.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none; existing conditional high-risk approval and PTO-D06 recorded
- Next route: phase-3-spec-qa

## Implementation Gate
- DoD complete and testable: yes
- Dependencies satisfied or explicitly gated: yes
- Required user decisions resolved: yes, accepted implementation and conditional Quality approvals plus PTO-D06
- Can enter implementation: yes
- Blocking reason: none; actual006gates/checkpoint and fresh SpecQA/readiness accepted, original six paths unchanged

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
