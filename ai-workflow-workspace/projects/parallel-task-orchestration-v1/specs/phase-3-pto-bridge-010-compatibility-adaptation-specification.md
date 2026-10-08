# Specification: PTO-BRIDGE-010-compatibility-adaptation

## Metadata
- Project: parallel-task-orchestration-v1
- Date: 2026-10-04
- Risk: high
- Source CR: PTO-CR-003-compatibility-adaptation
- Implementation writes: yes, after artifact QA and boundary decision
- Work mode: full-project
- Current decision: PTO-D10 approves read-only compatibility adaptation, not a native executor

## Accepted Intent And Sources
Compare the real AI System contract-1 producer with the current AI Workflow protocol,
then implement bounded adaptation in official AI Workflow only. The owner's handoff
is advisory; actual inspected sources are the isolated AI System development worktree's
parallel-run template, parallel_orchestration.py and project-orchestration-preflight.
This inspection does not transfer its approvals, test verdicts or source authority.

## Architecture Delta
Add one versioned read-only compatibility inspector beside the existing reducer.
It accepts explicit Workflow, target repository and AI System run paths, plus an
explicit closed mapping/budget envelope. It never invokes counterpart scripts,
interprets commands, launches agents or publishes state. Keep the installed protocol
capability separate from operational backend support, local phase gates and approvals.

The existing native-unverified release stays unchanged. Git-bearing worker trees
remain unsupported by the bounded inventory helper. Inspector output records the
need for a separately verified worktree/backend adapter, not a hidden .git exclusion.
Read-only adaptation is implementable without pretending native isolation exists.

## Definition Of Done
- PTO-010-AC1: Explicit version negotiation distinguishes supported contract-1 envelope from unknown/incompatible sources; execution_authorized and operational_support remain false.
- PTO-010-AC2: Validate exact run/coordinator/unit/attempt IDs, source manifest and actual current target HEAD/hash. Keep counterpart source digest algorithm separate from Workflow inventory, output and capability digests. Duplicate fields, paths, IDs, malformed/unsafe input and drift fail closed.
- PTO-010-AC3: One run-wide capacity observation explicitly counts live workers and reviewers from both systems, including external occupancy, without double-counting local attempts. Unknown/over-budget/missing identities block a parallel proposal. Cancellation or submitted/accepted labels never release occupancy without observed termination.
- PTO-010-AC4: State correspondence reports pending/planned, submitted/unaccepted, accepted/needs-local-receipt, failed/rejected and cancel-requested/reserved without applying transitions. Historical approvals or acceptance flags never satisfy local QA. Retired IDs and stale results reject reuse.
- PTO-010-AC5: Git worktree, native backend verification, logical rebase and cross-task delivery differences have explicit fail-closed dispositions. Unsupported operations never silently reset a run, loosen inventory or bypass parent Quality/capture/checkpoint gates.
- PTO-010-AC6: CLI is inspection-only with bounded duplicate-safe JSON reads and sanitized errors/output; no commands, writes, worker launches, counterpart imports, secrets, or native-support promotion.
- PTO-010-AC7: Positive and adversarial offline synthetic fixtures cover all six review gaps plus malformed/missing sources, unsafe paths, modes, source drift, reviewer occupancy, late results and no side effects. Existing protocol regressions and full source validation remain intact.
- PTO-010-AC8: Current semantic review covers intent/spec/DoD, complete added diff, producer-consumer mapping and failure paths. Current project route blocks final-owner-yes until owning formal Quality and required capture/final re-review; no restamping historical QA.

## Proposed Exact Source Write Set
- .systems/ai/core/parallel-compatibility.md (new)
- .systems/ai/templates/orchestration/compatibility.template.json (new)
- .systems/scripts/lib/parallel-compatibility.py (new)
- .systems/scripts/inspect-parallel-compatibility (new)
- .systems/scripts/tests/parallel-compatibility.py (new)
- .systems/ai/core/parallel-task-orchestration.md (route only)
- .systems/ai/core/commands.md (inspection guidance only)
- .systems/scripts/check-parallel-task-orchestration (require compatibility contract/files/tests)
- .systems/scripts/check-required-artifacts (add required inspector files)
- .systems/scripts/smoke/core.sh and .systems/scripts/smoke/manifest.json (supplemental compatibility tests; no removed IDs)
- .systems/scripts/check-validator-smoke-tests (integration references only if required by manifest contract)
- .systems/ai/core/changelog.md (scope/limits)

Owned workspace artifacts may record this CR, decision, architecture/plan delta,
specification, artifact review, slices, capture state and quality closure. Existing
historical reports are preserved. Source write set outside this list requires a
Spec Fix Loop; no changes to existing native metadata pins are planned.

## Interface And Failure Matrix
The closed mapping schema1 contains peer_contract/workflow_protocol (both1),
run_id, coordinator_id, project, unit_mapping (unit_id, task_id, slice_id,
read_paths), and capacity (known, complete, total, actors). Actors contain
agent_id, role (worker/reviewer), system, unit_id or null, and
termination_confirmed. All producer unit fields are required by the supported
closed contract-1 subset. Unknown extensions reject rather than infer support.
Manifest hashes attest only explicitly declared source files, not whole-repo
isolation. Actor observations are supplied supporting evidence, not native proof.
Read-only inspection success means structurally compatible, never dispatch-ready.
Unknown/incomplete capacity, missing live actors or over-budget occupancy reject.
Peer runtime_capacity must equal the observed run-wide total; no second pool.
Logical rebase requires a new verified input/run, not an adapter action.

| Producer / input | Consumer / check | Expected output | Forbidden outcome | Verification |
| --- | --- | --- | --- | --- |
| contract-1 run plus explicit mapping | compatibility inspector | mapped inspection, never runnable ledger | accepted status imported as local PASS | identity/state tests and manual trace |
| declared source manifest / actual repo HEAD | bounded physical file verifier | independently verified peer source digest | comparing unlike digest populations as equal | content/mode/path/HEAD drift cases |
| global worker/reviewer occupancy | budget checker | conservative free-slot observation | releasing cancelled-but-live agent or duplicate occupancy | lifecycle/budget negatives |
| Git-bearing implementation root | transport boundary | adapter-required | ignoring .git or claiming sandbox proof | synthetic Git worktree inspection |
| new baseline or cross-task result | recovery/parent gate boundary | local-reassessment-required | logical rebase mutates Workflow ledger | unsupported-operation and stale-result negatives |
| malformed, linked or missing source | strict input reader | sanitized nonzero failure | source content leaked or partial success | CLI failure/no-write tests |

## Implementation Slice Plan
- Source: owner request, CR003, current contracts and inspected counterpart interface
- DoD source: PTO-010-AC1 through AC8 above
- Scope: exact source write set, official AI Workflow only
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-010-S1 | Define wire mapping, authority and unsupported boundaries | contract/template, commands/router | complete six-gap matrix | artifact QA and producer-consumer table | planned |
| PTO-010-S2 | Implement conservative read-only inspector | helper/CLI | actual baseline plus closed schema and budget | positive/failure path fixtures | planned |
| PTO-010-S3 | Integrate behavioral regressions and review | tests/checks/smoke/changelog | all AC, preserved IDs and full source gate | semantic current-diff review before scripts | planned |
- Stop rule: missing boundary decision, native proof, unknown schema/ownership, broadened writes or unsafe input stops affected work. No automatic fallback that grants operational support.

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Timezone: Europe/Warsaw
- Time budget: none
- Must-have outcome: all protocol compatibility gaps explicitly checked or rejected
- Should-have scope: none
- Stretch scope: none
- Explicitly deferred scope: native backend/worktree executor, counterpart rollout and performance claim
- Quality floor: numbered AC and fresh semantic/adversarial review, required formal gates
- Cutline rule: never cut safety; unsupported capability stays blocked
- Overrun checkpoint: report actual progress and unresolved owner decisions
- Owner override: inherited no deadline / no timebox for this open PTO project

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: this specification and CR003
- Testable DoD / acceptance conditions: PTO-010-AC1 through AC8, mapped to matrix/test cases
- Artifact QA route: phase-1-architecture-qa, phase-2-plan-qa, phase-3-spec-qa
- Artifact QA trigger: after architecture/plan delta and complete specification, before source writes
- Implementation Quality Closure route: phase-5-quality
- Required verification: semantic current-diff review, adversarial/producer-consumer matrix, offline tests, preserved smoke coverage and fresh full source validation
- Quality-ready criteria: AC evidenced, no unresolved P0/P1/material P2, actual high-risk Quality approval before formal PASS
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none; PTO-D10 resolves protocol-only adaptation and technical Phase8 route
- Next route: artifact QA, pre-write readiness, then three source slices

## Publication And Capture
Cross-system impact yes is inherited from the explicitly coordinated PTO project.
One updated privacy-safe handoff will describe actual implemented adapter and limits
after Quality. No AI System or target writes, commits, push, updates or final-owner-yes
are authorized by this specification. Existing PTO no-commit boundary remains in force.
