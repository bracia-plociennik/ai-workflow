# Pre-final Architecture Delta: Capture And Commit Boundaries

## Scope And Authority
Two independently accepted tasks extend PTO, not its native backend scope. Source writes are future high-risk work. Original protocol-only release and native-unverified limitation remain unchanged. PTO-D07 authorizes planning only.

## Architecture Decisions
A is a correctness repair; B depends on A and introduces an explicitly versioned freshness extension. A can ship independently without adopting B semantics. Existing canonical schema1/schema2 behavior is the compatibility floor, not exceptions added to three parsers.

### A: One Semantic Validator, Separate Population Selectors
Extract capture-record.py as a pure shared record/collection validator. It receives bounded evidence roots and safe path/Git/QA adapters from callers; it does not import validation-scope or discover a broader workspace. capture-state inventory and validation-scope select their existing populations, then call it. collection validation owns duplicate work IDs and reused distillation detection, not only per-record parsing. Existing path guards remain mandatory before callbacks. Preserve repo/core schema1 manifest population; do not replace it with whole-workspace inventory.
Schema1 missing derived output may be derived for display, never written. Historical completion does not imply current QA. Schema2 retains actual current HEAD, matching identity/kind/ownership/PASS/hash and unique accepted distillation. Registered history never qualifies as current PASS.
The distillation requirement applies to completed; ready may have no distillation and pending-quality may have no Quality. Direct lifecycle consumers (orchestration parent/checkpoint gates) must validate the bounded owning collection before selecting one record; a valid record cannot conceal an invalid/duplicate sibling.

### B: Commit Policy Is Not A Git Daemon
Canonical phase-commit-policy.md directs the execution owner at boundaries. Tooling reports/checks readiness and equivalence; it does not auto-stage/commit/checkout/merge/push. For future approved work under the installed policy, local commits default on when scope, publishability, risk and Quality are satisfied. Explicit no-commit wins. Existing PTO approval is not retroactively enlarged.
One coordinator owns the index and commits. Worker results are not commit authority. Larger projects, high risk and shared-contract work use a suitable dedicated branch before tracked writes; tiny reversible edits may use an existing allowed branch. Branch/index collisions stop; no auto-stash/reset.

### B: Post-commit Freshness Without Restamping
New assessments can opt into a versioned, complete pre-commit source snapshot. Existing reports without it keep existing strict behavior; do not rewrite them. Distinguish workflow-source and approved-target-source repository identities/HEADs. Never compare installed Workflow HEAD to target product HEAD as if they were the same repository.
Opt-in uses a distinct full-qa-verification-v3 marker and bound artifact-kind discriminator, paired with Capture schema: 3 when captured. Existing schema1/schema2/V2 remain unchanged. Do not embed V2 markers/runs in V3 outputs. Upgraded gate consumers must dispatch explicitly; frozen old consumers must reject current qualification, including legacy fallback paths. Missing installed capability blocks use, never silently drops proof fields.
Build immutable source snapshot before QA: exact product/source/dependency populations, additions/deletions, regular-file modes and hashes, allowed source roots and verification environment identity. Snapshot never contains its QA report hash or resulting commit SHA. Reviewer QA binds the snapshot; read-time binding ties snapshot hash, immutable QA hash, applicable approvals and actual commit. Unknown dependencies or incomplete coverage prohibit reuse.
The read-only verifier checks the actual commit tree AND live index/worktree against that snapshot. A commit merely preserving assessed bytes is not a new semantic implementation. New unexpected source files, hook changes, partial staging, deletes/mode drift, repo swaps or changed evidence invalidate the binding. Ancestry/HEAD text alone is insufficient.
Current QA eligibility still requires complete semantic PASS and current owning-project evidence. Binding is only an alternative proof of current source equivalence for explicitly opted-in records, not independent PASS. FAIL, wrong identity and historical/superseded QA always reject.
Pre-commit snapshots are immutable, content-addressed supporting evidence. Post-commit results go to /tmp or an already-approved ignored path; never add resulting commit SHA to files in that same commit. Recompute on read; stored current=true is not trusted. Missing proof means unknown/reverification, not a fabricated success.
Runtime evidence is a separate population: fresh naming/status/QA/capture validation follows artifact changes. Full/CI/updater remain independently fresh when required. Reuse a source receipt only under existing authenticated execution-efficiency rules.
If a dependency cycle arises between snapshot, QA, status and capture, fail planning/implementation: QA must bind stable source/decision/spec inputs, not its own mutable closure outputs. Do not solve a cycle by silently excluding an arbitrary path.

## Integration And Failure Traces
| Producer | Consumer | Required invariant | Failure route |
| --- | --- | --- | --- |
| selected capture population | shared collection validator | bounded owner and no duplicate identity/artifact | reject, no scans outside selected population |
| schema1 record | capture/status/Dream queue | historical/advisory is distinct from current eligibility | retain historical disposition, block current gate when needed |
| schema2 record | QA consumer | exact current proof, identity/PASS and protected references | reject stale/malformed/foreign evidence |
| accepted reviewed worktree | commit snapshot and staging audit | complete intended source state, no unrelated staged changes | stop before commit |
| local commit plus unchanged worktree | binding verifier | both source identities and all content/mode/dependency checks | re-QA affected scope, broaden if unknown |
| binding result | status/capture/checkpoint | no authority or verdict promotion | no automatic PASS/approval/publication |

## Alternatives Rejected
Three independent parsers perpetuate drift. Removing HEAD checks globally weakens stale-evidence rejection. Rewriting old QA or downgrading schema2 erases provenance. Empty commits/forced workspace tracking add no safety. Re-running all tests for every unchanged commit wastes time; evidence reuse must instead prove unchanged covered inputs.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: PTO-D07, CR-001/002 and task AC in the canonical plan/specs
- Testable DoD / acceptance conditions: consumer parity and strict negative cases; explicit commit authority; proven source equivalence without mutable/self-referential evidence
- Artifact QA route: phase-1-architecture-qa
- Artifact QA trigger: complete delta and compatibility review before Plan QA
- Implementation Quality Closure route: phase-5-quality
- Required verification: producer-consumer audit, adversarial matrix, target/upstream identity and commit failure traces; implementation tests remain future
- Quality-ready criteria: bounded write sets and proof scheme; missing proof fails closed
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: no planning blocker; implementation and added-scope handoff decisions remain boundary-gated
- Next route: phase-2-project-plan

## Delivery Constraints
No deadline/timebox by inherited owner choice. Must-have: safe parity and non-circular commit evidence. Deferred: target updates, native backend, CI cache redesign, global history migration. Stop for scope growth or unprovable equivalence.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D07
- Questions asked: none
- Auto-resolved reversible decisions: existing branch, serial work, two task IDs
- Optional owner refinements: none; added-scope cross-system impact decision is mandatory before local commit or handoff, pending and non-blocking for planning
- Decision artifacts: decisions/pto-pre-final-planning-authorization.md
- Next route: artifact QA only

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: preserve explicit freshness and authority design
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Historical validity and current QA are different
- Suggested entry summary: Consumer parity and commit equivalence must not grant approvals.
