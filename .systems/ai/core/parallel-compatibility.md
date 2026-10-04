# Parallel Compatibility Inspection

## Scope And Authority
Read-only schema1 adaptation of the explicitly supported AI System contract1
subset to Workflow protocol1. One coordinator and one run-wide budget include
workers and reviewers across both systems. Metadata and supplied observations
are supporting evidence, never native isolation proof, approval or a repository lock.
execution_authorized: false; operational_support: false always.
No dispatch, Git mutation, runtime publication, counterpart import or automatic
local acceptance. Existing phase gates, permissions and checkpoint cadence remain.

## Closed Producer And Consumer Contract
Use compatibility.template.json beside an explicit peer run, target root and
Workflow root. Every unit maps once by exact ID to an existing local task/slice
identity; mapping is a supplied label, not proof of local approval or task existence.
Unknown versions/extensions, duplicate fields/IDs, missing inputs and unsafe
paths reject. Source manifest uses sorted path=sha256 newline SHA256 records.
Mapped read paths must be exact declared source files, not an unbounded directory.
Access lists reject normalized case/Unicode aliases. Known credential/key/private
paths are rejected before contents are read; this is not a content privacy oracle.
Only declared files are verified; not whole-repo inventory or output digest.
HEAD and actual content/mode observations are checked before and after inspection.
Retained evidence in failed/cancelled records is allowed but rechecked for actual
identity, freshness and modes; it never becomes a local accepted result.
Git repository/worktree roots can be inspected for declared data only; this does
not make them supported worker transports in the bounded Workflow executor.

## Capacity And State Correspondence
Capacity requires known/complete observations and the same total as the peer
runtime_capacity. All started units have exactly matching actor observations;
external workers and reviewers count once by unique native ID. Missing identities,
contradictory termination, retired IDs and over-budget occupancy reject. Unknown
capacity blocks inspection. Submitted, accepted, failed and cancel-requested labels
do not release occupied capacity; only matching termination observations do.
Observations remain caller-supplied, not authenticated backend observations.

| Peer state | Inspection disposition | Required local action |
| --- | --- | --- |
| pending / ready | planned / ready-for-local-review | local scope, gates and actual dispatch readiness |
| running | running-observed | retain occupied reservation |
| submitted | submitted-unaccepted | local review and current evidence receipt |
| accepted | accepted-needs-local-receipt | never import peer QA or PASS |
| failed | rejected-needs-reconciliation | inspect effects before retry |
| blocked | blocked | resolve source decision |
| cancel-requested | cancellation-reserved | wait for observed termination |
| cancelled | cancelled-observed | reconcile effects before retry |

## Unsupported Differences
Capability negotiation is static inspection, not installed interoperability.
Native backend verification: deferred/unverified. Git worktree executor:
adapter-required. Logical rebase: new verified run/input, never an action here.
Cross-task delivery: local parent Quality/capture/checkpoint gates still required.
No native-support promotion and no recursive delegation.

## CLI And Verification
inspect-parallel-compatibility --workflow PATH --repo PATH --run FILE --mapping FILE
prints sanitized JSON. Exit0 means compatible-inspection only; malformed, stale,
unsupported or unsafe inputs exit1. There is no write/output/dispatch flag.
Version negotiation, identity, manifest, full capacity, result receipt, dependencies,
path/resource conflict and no-side-effect regressions run offline in
.systems/scripts/tests/parallel-compatibility.py. Common integrated QA is mandatory
before a parent gate. Finite tests cannot establish real native isolation.
