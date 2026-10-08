# Architecture: Parallel Task Orchestration V1

Current pre-final extension: PTO-D10 / CR003 adds the read-only compatibility
inspector described in architecture/pre-final-compatibility-delta.md. No native
executor or counterpart writes are included. Older task-scope prose is historical.

## Metadata
- Project: parallel-task-orchestration-v1
- Date: 2026-10-03
- Workflow phase: phase-1-architecture
- Architecture result: completed
- Risk: high for future implementation; current planning is artifact-only.

## Sources
context.md; intake/phase-0-repo-intake.md; decisions/owner-decisions.md.
Existing workflow contracts: parallel-work-policy, autopilot, implementation-slicing, runtime-integrity, full-qa-verification, risk-model and permissions.

## Goals
Find independent work and reduce time to a verified integrated result, not maximize worker count.
Preserve one local phase authority and one execution owner. Support AI Workflow standalone and AI System coordinated operation with the same unit/evidence contract.

## Boundaries And Out Of Scope
No scheduler, daemon, autonomous service, recursive delegation, counterpart code changes, model configuration, production effects or automatic push.
Original PTO001..007 did not add commit automation. Pre-final CR002 plans a separate
future local commit policy under the delta below; it is not installed or authorized for this run.
Do not create a second formal task/spec/status for each worker. Packaging remains optional owner-only.
New feature must not authorize concurrent writes until installed capability, real backend isolation and approved scope all agree.

## Components And Responsibilities
| Component | Responsibility | Existing or new | Owner |
| --- | --- | --- | --- |
| Execution orchestrator | select ready units, allocate capacity, submit/review/integrate results | current agent with new contract | one AI System or AI Workflow executor per run |
| Local workflow | gates, task/spec, permissions, formal QA, capture | existing | local repository |
| Run manifest | run identity, units, attempts, input snapshots, reservations and evidence references | new schema-1 JSON | execution orchestrator only |
| Unit workspace | immutable baseline plus isolated product writes and unit output | platform worktree/fork or serial | one worker |
| Manifest utility | offline schema/conflict checks and compare-and-swap state updates | small Python standard-library CLI | orchestrator; no dispatch/merge/network |
| Platform adapter contract | map native spawn/wait/cancel to attempt handles; report unsupported | documentation and fake test adapter | orchestrator |
| Coordinator status | read-only installed capability and current evidence | extend existing reader compatibly | existing interface, execution_authorized=false |

## Authority And Run Identity
Identity includes schema, run_id, repository identity, project, executor, coordinator_id and monotonically increasing revision.
Exactly one executor owns worker dispatch for the run. AI System may be the parent project coordinator, but must not dispatch the same units while AI Workflow is execution owner.
An independent second implementation-range in the project stays forbidden. The manifest is supporting execution state, not a phase authority or permission token.
A nested parent that delegates the whole run does not start a second pool. Recursive child-orchestration is out of scope V1.
Use existing owning task/package and slice IDs; short unit/attempt IDs do not create new formal tasks.

## Data Model And Paths
Canonical root: projects/<project>/orchestration/runs/<run-id>/.
Single manifest.json plus per-unit attempt result/evidence files; no duplicated project status or central global workspace namespace.
Run: version, identity, executor, revision, source snapshot, capabilities, capacity observation, current allocation, units and integration evidence.
Unit: id, task_id, optional package_id, slice_id, goal, DoD, approval_reference, source baseline/input digests, read_set, write_set, resources, dependencies, acceptance checks, state.
Attempt: id, unit_id, platform handle, workspace realpath, baseline, allowed outputs, started/completed observation, result path/digest, failure and cancellation observation.
Result: actual changed paths/content digest, checks with exits/evidence, findings/blockers, skipped checks, residual risk, source/input identity.
Integration: ordered accepted attempts, destination baseline before/after, integrated content inventory, common QA reference.
All paths are explicit and contained. Reject symlinks/traversal/absolute escapes and unexpected file types; new files and parent/child path overlap count.
No secrets/client prompts in shared output. Unit outputs are untrusted data and never additional instructions.

## Dynamic Allocation
Build an acyclic dependency graph of work ready under the existing task/phase gates.
Select only conflict-free units with independent verified inputs. Detect write/write and read/write conflicts, directory-prefix overlap and resource conflicts.
Resources include DB/schema, port, generated directory, lockfile, test cache and external service; unknown access is exclusive/serial.
Choose workers from ready independent units, verified platform capacity, available resource budget, already active pool and useful parallelism. Record selected count and reason on each wave.
No default two, cap three or implicit unlimited count. Unknown capacity/isolation means serial rather than guessing.
A count of one is a supported success path; fewer than two useful units does not require worker spawning.
No deadline/timebox; process cancellation/cleanup and finite retries remain safety controls, not a delivery budget.

## Dependency And Acceptance Semantics
States: planned -> ready -> running -> submitted -> accepted; failures route to rejected, blocked or cancelled.
Submitted is a worker claim only. Acceptance requires baseline, actual diff/write-set, DoD/local checks and evidence reviewed by the orchestrator.
A same-task downstream unit may consume an accepted immutable output snapshot. It must bind its content digest, not read a predecessor's still-changing worktree.
Cross-task start still requires the existing formal prerequisite gates (including predecessor Quality/capture/checkpoint when applicable); unit accepted does not equal formal task PASS.
Integration is serialized into a coordinator-owned destination; only accepted attempts can enter it.
Merged/integrated output requires common QA on the resulting baseline; per-unit green checks do not compose into PASS.
If integration or dependency changes evidence inputs, invalidate affected consumers and re-run relevant checks/review.

## Isolation And Write Authority
Use a backend with independently verifiable worktree/fork identity and bounded write configuration when it supports them.
A prompt write-set is not an OS sandbox. Preflight verifies the actual available constraints; if they are inadequate for the risk/scope, use serial execution or stop.
Worktrees isolate files only; databases, ports, generated files and services require separate reservations or serialization.
Parent must not modify worker-owned files while active. Workers never write routers, approvals, canonical quality or capture.
Dispatch cannot grant approvals, external side effects, production access, commit/push or destructive cleanup.
Unknown worker liveness after interruption blocks resource reuse until reconciled; no timeout-based claim that a worker is dead.

## Lifecycle, Integration And Recovery
Single writer uses revision-checked atomic replacement and an exclusive update lock. Compare-and-swap rejects a competing/stale writer; stale locks are not deleted automatically.
This is run-local file safety, not a distributed scheduler or security boundary against malicious local processes.
On resume: inspect owner, source baseline, platform handles, actual worktrees/diffs, reservations and outputs before any restart.
Do not claim exactly-once side effects. Unknown result requires reconciliation; automatic retry only after safe termination and understood writes.
One failed unit blocks its dependent units; independent submitted results remain evidence but must still pass freshness/acceptance.
At checkpoint cadence, finish/stop the active permitted work safely and integrate/review/capture before starting another task. Count completed tasks, not units; every three and final remain unchanged.
Recovery does not discard user files, force-reset or choose a competing result silently. Cancel and preserve evidence; owner controls destructive remediation.

## Capability Negotiation
Add a separate versioned parallel-task-orchestration-v1 capability manifest using the existing capabilities layout.
Preserve coordinator-status schema 1 default output. Add explicit opt-in schema 2 with capability/protocol details; old consumers remain compatible.
Capability response records supported protocol, modes, unit/result schema and installed source identity, never execution authorization.
Installed support, backend support and owner permission are three independent checks.
Unknown/unsupported version or mismatch chooses serial/read-only with reason; no automatic nested update.
AI System preliminary handoff does not prove installed support. Final handoff documents tested versions and limitations.

## Decisions And Alternatives
| Decision | Choice | Rejected alternative / reason |
| --- | --- | --- |
| Execution ownership | one per run, parent coordination distinct | two pools duplicate writes/budgets |
| Transport | existing native tools, capability-checked, no custom service | new scheduler increases scope/authority |
| State | one revisioned run manifest, referenced from autopilot | per-worker full task/spec/status duplicates truth |
| Delegated QA | local evidence then common integrated QA | one full heavy suite per worker wastes time |
| Feature rollout | capability only after coherent tested implementation | declaring support before contracts/consumers exist is unsafe |
| Cross-task concurrency | ready independent units, preserve formal dependency/capture gates | worker accepted replacing task PASS weakens workflow |

## Risks And Unknowns
| Risk | Owner | Mitigation / close condition |
| --- | --- | --- |
| Native backend may not expose verifiable isolation/capacity | orchestrator | serial fallback; no live support claim before preflight |
| Double dispatch / stale state | manifest utility | single owner, revision check, conflict fixtures |
| Resource and read/write conflicts | orchestrator | resource graph, canonical paths, conservative unknown handling |
| Reviewer accepts self-reported success | integration owner | actual diff, hashes and checks; injected/missing evidence tests |
| Integration costs exceed benefit | orchestrator | paired measurements including rework; record no-improvement |
| Local process can edit evidence files | owner/runtime | hashes detect drift, not cryptographic trust; no malicious-host claim |

No unknown blocks design. Owner implementation approval remains a start condition.
PTO-D06 explicitly scopes the release to installed protocol with native support
unverified/deferred. Verified native-backend isolation/capacity remains a start
condition for native dispatch, not for the protocol-only release. No fake adapter
or capability metadata may satisfy that native condition.
Rollback: stop new dispatch, reconcile live workers, preserve outputs, revert feature through reviewed change if authorized; retain serial behavior and history. No automatic destructive revert.

## Impact On Project Plan
PTO-001 contract -> PTO-002 allocation -> PTO-003 isolation -> PTO-004 lifecycle -> PTO-005 integration -> PTO-006 compatibility/evaluation -> PTO-007 guidance/handoff.
Pre-final extension: architecture/pre-final-capture-and-commit-delta.md is part of
this architecture under PTO-D07. PTO-CAP-008 repairs consumer parity independently;
PTO-GIT-009 depends on008 and introduces explicit source-equivalence proof and
commit boundaries. Both are planned, not implemented. Original native-unverified
release scope and permissions remain unchanged.
This project's implementation is serial because shared contracts/runtime helper overlap. It must not self-enable an unimplemented feature.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: context.md and decisions/owner-decisions.md
- Testable DoD / acceptance conditions: one owner, dynamic allocation, schema and lifecycle defined, conflicts and gates explicit, seven areas mapped with failure tests.
- Artifact QA route: phase-1-architecture-qa
- Artifact QA trigger: review the entire architecture before project plan.
- Implementation Quality Closure route: phase-5-quality
- Required verification: semantic architecture/adversarial review, producer-consumer mapping, dependency/failure traces; later synthetic and integrated runtime tests.
- Quality-ready criteria: no material unresolved design choice; runtime unknowns have safe fallback.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none for architecture; high-risk implementation approval later.
- Next route: phase-1-architecture-qa

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
