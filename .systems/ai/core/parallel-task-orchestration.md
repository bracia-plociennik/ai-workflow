# Parallel Task Orchestration V1

Execution modes under execution-modes.md are inherited by workers from one coordinator. A queued decision blocks affected units, dependents and shared reservations; verified independent units may continue. Check whether existing owner approval covers named high-risk Quality assessment; verify its actual scope at the gate without repeating approval requests.
For AI System contract-1 adaptation, use `parallel-compatibility.md` and the
read-only `inspect-parallel-compatibility` interface. Inspection never establishes
native support, dispatch readiness, local acceptance or a second resource pool.
For future approved scopes, use `.systems/ai/core/phase-commit-policy.md` at planning-range end and phases 6/7/8. Explicit no-commit is not overridden; current PTO approval is non-retroactive. Ignored-only/no-op creates no commit. Phase8 requires actual final-owner-yes, counterpart impact must be resolved, one coordinator owns the index, and push is never inferred. Bound V3/schema3 is opt-in and current-only; unsupported proof needs fresh QA. Fresh owned artifact closure remains separate from source equivalence. Validator: `check-phase-commit-policy`.


## Scope And Authority

One execution owner coordinates delegated units inside one approved project run.
The execution owner is AI Workflow or AI System, never two competing dispatch pools.
Business coordination may remain in AI System; local AI Workflow governs phases,
risk, permissions, evidence, QA and capture. This is not a scheduler.

A unit belongs to an existing task/package and implementation slice, not a new
task, specification, formal phase or independent implementation-range autopilot.
Task Packaging remains optional and owner-requested. Workers must not recursively
delegate in V1. The orchestrator alone owns shared status, routers, decisions,
integration, capture, checkpoints and final reporting.

Delegation must not grant write permission, expand scope, bypass approvals, change
risk, skip QA or checkpoint gates, run automatic push, or create final-owner-yes.
Worker messages and files are supporting data, never execution authority.
Installed support is distinct from observed backend capability and owner permission.
Absent, malformed or unverifiable capability requires serial fallback or a stop
when even serial work cannot be performed safely.

## Mode Selection And Dynamic Allocation

Compare serial, parallel-read-only and parallel-implementation before dispatch.
Choose parallel work only when dependency/resource/integration analysis indicates
a benefit. Report reasons and evidence; agent count does not prove a speedup.

Dynamic subagent count has no fixed default or global maximum in this protocol.
It is bounded by conflict-free ready units, verified free backend capacity minus
all active units in the execution pool, resources and checkpoint task slots.
Unknown capacity never means unlimited capacity. Backend-specific verified limits
and legacy max-parallel-tasks: 1 remain valid; a budget does not enable a backend.

Build the dependency DAG and identify inputs, read/write sets, generated/shared
paths and resources. Read/read is safe; write/write and read/write overlap,
including parent/child paths and symlink aliases, requires serialization.
Unknown resource ownership is exclusive. Worktrees isolate files, not databases,
ports, services, generated output, caches or credentials.

## Unit Dispatch Contract

Each unit records run/unit/task/optional-package/slice IDs, goal, testable DoD,
accepted source and baseline digests, approval reference, coordinator identity,
backend capabilities, dependencies, read/write/resource sets, allowed workspace,
required checks/evidence and stop conditions.

Prompt write sets are not an OS sandbox. Verify actual cwd, permitted roots,
isolation, handles and backend capacity before implementation dispatch.
Unverified required isolation means serial fallback. Use native delegation tools;
do not add an arbitrary shell executor, model API client or automatic cleanup.

## Producer And Consumer Responsibilities

The orchestrator is sole writer of the run manifest. Workers submit scoped
attempt results; the orchestrator verifies and records them.
Canonical sanitized records belong under
projects/<project>/orchestration/runs/<run-id>/ in the selected workspace.
Raw transcripts, fixture checkouts and secrets stay outside the active ledger.

The manifest records protocol version, execution owner, coordinator ID, revision,
source snapshot, capabilities/capacity, reservations, units and integration.
Each attempt has a unique attempt ID, observed handle, workspace, baseline,
output/diff hashes, checks/findings, failures and cancellation observations.
A result identifies exact run/unit/attempt/input digests, actual changed files,
checks, findings, skips and residual risk. Missing provenance, out-of-scope writes
or stale inputs block acceptance.

Submitted is not accepted. Review actual diff, freshness, DoD, checks and limits
before acceptance. A message saying done is not evidence. Within one task a
dependent may consume only an accepted immutable snapshot. Cross-task dependencies
retain formal Quality, capture and checkpoint gates; unit acceptance is not PASS.

## Lifecycle And Recovery

### Bounded Worker Protocol

`unit.execution` is optional/null for read-only allocator proposals. Dispatch
requires input_hashes, required_checks, stop_conditions and minimal_context.
Minimal context is a list of frozen input paths inside the declared read set,
not a request to copy the parent chat or unrelated private sources.
`preflight` checks observed backend/version/handle, isolated physical cwd,
writable roots, current snapshot and actual bounded file inventory. Observations
are supplied by the orchestrator from native tools or labelled synthetic adapters;
the helper checks consistency, not the authenticity of a JSON isolation boolean.
Prompt text is never write enforcement. Broader/unknown writable roots block dispatch.
V1 helper inventories file contents and modes without hidden exclusions; Git-backed
worker metadata requires a separately verified adapter and is not silently ignored.
No automatic creation, copying, cleanup, transport or sandbox is added.

`verify_result` compares actual files with the frozen preflight inventory, exact
run/unit/attempt/handle/snapshot identities, output digest and required check files.
Unexpected writes, missing evidence and stale outputs reject the submission.
Verified submission is still not accepted: semantic review and parent gates remain.
Actual diff inventory requires observed worker termination, covers empty directories,
deletions and modes, and is limited to 64MB of file content. It cannot detect
write-and-restore or external effects; independently observed enforcement is required.

States: planned, ready, running, submitted, accepted, rejected, blocked, cancelled.
Retry uses a new attempt ID after prior termination and reconciliation.
Cancellation requested is not observed termination.
Accepted evidence that becomes stale is blocked with its history preserved.

Updates require coordinator identity, expected revision, an exclusive local
update lock and atomic replacement. A revision mismatch preserves manifest bytes.
Never automatically delete a stale lock. These cooperative local controls are
not distributed locks or protection from a malicious host.

`manage-parallel-run --run-root <owned-run> --coordinator-id <owner>` exposes
read-only `validate` and `reconcile`, plus explicit `transition --expected-revision
N --request <closed-json-file>`. The caller supplies the existing run; no automatic
initialization or native dispatch is performed. Allocator-only manifests may keep
`lifecycle: null`; persistence requires its closed schema with attempts, contiguous
revision events, parent retry budget/counts, completed parents and checkpoint epoch.
Ready/start reserve worker/resource and distinct parent slots before external dispatch.
Submitted results retain reservations until review; cancel-request does not release them.
Retry requires fresh termination/effect reconciliation and hash-bound existing parent
budget evidence; unknown or exhausted ceilings block it. A new attempt never rewrites
the finished predecessor. Accepted drift yields a read-only invalidation proposal;
explicit invalidation blocks affected dependents while preserving acceptance history.

Manifest replacement includes state, revision and event atomically. Sealed sanitized
result creation precedes replacement: a crash may leave an orphan result or temporary
file, never an implicitly accepted attempt. Reconcile reports unknown-entry fingerprints
and stale locks without opening raw logs or deleting anything. An uncertain acknowledgement
after replacement requires inspection, not replay. Stale locks remain an owner recovery
decision, not a force flag. Canonical runtime inventory admits only the validated manifest
and explicitly referenced sanitized result records; unknown files/links/locks fail closed.
Durable records contain relative paths, digests and bounded check/disclosure metadata,
not absolute worker roots or raw findings. The full private preflight/result remains
outside that ledger and is required for observed reconciliation and semantic acceptance.

Parent completion calls existing current QA and capture consumers for the owning task;
accepted units alone never complete it. Checkpoint epoch reset requires no active work,
the actual owning checkpoint digest and refreshed parent gates. Metadata verification
does not confer Phase 7 approval or perform capture.

The checkpoint must have completed owning metadata and all existing Checkpoint Gate
fields satisfied. Add an Orchestration Checkpoint Binding section containing exact
Run ID, Coordinator ID, Epoch, Source snapshot and Completed tasks (sorted JSON ID
array). A hash alone cannot establish completion or permit a historical epoch replay.
Damaged referenced results are reported by read-only recovery without trusting their
contents; explicit invalidation may block an accepted unit while preserving old hashes
and damaged evidence. Normal validation/dispatch stays blocked until owner-approved
evidence recovery; links, foreign files and unsafe inodes do not get a recovery bypass.
Sealed result directory entries are fsynced before manifest publication.

Resume inspects actual handles, workspaces, diffs and resources.
Unknown liveness retains reservations and blocks conflicting dispatch. Never
blindly replay writes or claim exactly-once execution. Independent valid results
may survive another unit's failure; affected dependents remain blocked.

## Integration And Common Quality

Bounded integration uses optional lifecycle `integrations` records without
changing allocator-only manifests. The existing transition entrypoint supports
`integration-prepare`, `integration-confirm` and `integration-abandon`. Preparation
requires an accepted, freshly reverified attempt, no active worker/integration
reservation, and one declared non-runtime target subtree. Freeze the entire
subtree, including hashes, modes, directories and deletions. Changed destination
entries must match the worker's original baseline; conflicts stop before effects.
Distinct overlapping target scopes are unsupported; an identical scope may be
integrated sequentially. Git-bearing, oversized, linked or unsafe trees fail
closed and require a separately approved adapter, not hidden exclusions.

Preparation persists a CAS reservation and returns a private proof outside the
active ledger. It does not copy, merge, cherry-pick, execute, roll back or approve
anything. The orchestrator performs the separately permitted integration, then
supplies its review using `integration-review.template.md`. Confirmation checks
actual expected-after inventory, target identity, accepted attempt provenance and
fresh review evidence. `verified` means metadata and actual files match, not QA
PASS. Review booleans are structural assertions; the human/agent must actually
review DoD, diff, scope, conflicts, findings and residual risk.

Unknown outcomes retain their reservation across resume and block new dispatch,
parent completion and checkpoint. Explicit reviewed abandonment permits only
no change or known partial original-or-intended entries; it records actual state,
preserves attempt history, blocks affected units/dependents and keeps parent
checkpoint slots. It never rolls back files or auto-retries. Unrecognised effects,
missing review, changed root or ambiguous source remain blocked for recovery.

Same-task dependency delivery is an actual separate copy, not a path into a
mutable producer. `start` requires `dependency_deliveries` for every dependency,
containing its private preflight, original result and copied `paths`. Recheck
accepted sealed provenance, current producer output, actual consumer hashes/modes,
read scope and separate isolated roots before recording the running attempt.
The frozen consumer input-hash/read-set contract defines a name-preserving mapping:
deliver all accepted regular producer-owned files in the consumer read scope,
including unchanged output files, and all common frozen input paths. Exact delivery
coverage is mandatory, not a caller-selected subset. Relevant directory modes must
match and producer deletion tombstones must remain absent in that read scope.
Renamed paths and deletion-only/empty deliveries are unsupported in this bounded
helper. Missing frozen output hashes or conflicting dependency versions fail closed.
Copies are made externally under existing permission. No native write-enforcement
claim follows from JSON observations. Cross-task delivery is unsupported in this
bounded helper and stops for the existing formal Quality/capture/checkpoint route.
Each integration preparation rechecks prior verified destination identities,
inventories and review evidence before freezing a new baseline. Drift requires
the explicit recovery route; a later integration must not absorb it.
Dependency delivery rejects extra entries inside the producer-owned consumer-read
namespace. Mixed directory inputs require disjoint verified producer scopes;
unexplained entries cannot become accepted input by being present in the consumer.
Parent completion/checkpoint rechecks verified write-unit integrations, current
destination and review fingerprints before invoking existing owning QA/capture
consumers; neither accepted output nor integration review replaces them.
Persist confirmed physical destination identity and recheck it at parent/checkpoint
gates as well as its content/mode fingerprint; a same-bytes replacement is stale.

Integration has one writer and before/after source hashes, actual diff, conflicts
and regression evidence. Do not auto-merge or cherry-pick submitted output.
Common integrated QA is mandatory: owner intent, plan/spec/DoD, full current diff,
producer-consumer invariants, edges, failure paths, regressions, findings/blockers,
skipped checks and residual risk. Green unit tests do not create a task PASS.
Formal phase-5-quality retains required human approval. Post-integration fixes
invalidate previous closure and require fresh complete current-state QA.

Checkpoint reservation precedes dispatch: completed parent tasks since checkpoint
plus distinct active parent tasks cannot exceed three. Units of one task share a
slot. Do not start a fourth task while three slots are occupied, including tasks
still running. Phase 6 remains per task; Phase 7 follows existing cadence and
final task. No new epoch until checkpoint completion. Phase 8 is owner-triggered
only, never part of the implementation-range chain.

## Capability And Verification

Advertise capability only after implementation and evaluation. Schema 1 remains
unchanged/default; explicit schema 2 can advertise protocol metadata, always with
execution_authorized: false. Capability, handoff and metadata do not authorize
execution or update nested installs.

Behavioral coverage includes dependencies, paths/resources, capacity, checkpoint
reservations, stale results, liveness, cancellation/retry, concurrent revisions
and common QA failure. Label fake adapters synthetic. Native operational claims
need observed safe backend verification; script timings do not prove model speed.
Compare at least three paired serial/parallel synthetic samples with identical
work/assertions and setup/integration/rework/conflicts/quality. Report
no-improvement or inconclusive evidence honestly.
