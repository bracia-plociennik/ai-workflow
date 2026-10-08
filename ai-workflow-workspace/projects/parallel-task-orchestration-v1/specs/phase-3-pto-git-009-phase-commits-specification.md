# Specification: PTO-GIT-009-phase-commits
## Metadata
- Task/package ID: PTO-GIT-009-phase-commits
- Project: parallel-task-orchestration-v1
- Date: 2026-10-04
- Risk: high
- Readiness: conditional, dependency-gated
- Source CR: PTO-CR-002-phase-commits

## Goal And Scope
Define local commit boundaries and independently proven post-commit freshness without rewriting QA or granting publication authority. Requires accepted008 behavior.
Sources: canonical plan/architecture, architecture/pre-final-capture-and-commit-delta.md, PTO-D07, execution-efficiency, actual QA producer/consumer.
Out of scope: repository auto-updater, auto-push/PR/merge, actual PTO commit now, native backend, target changes and global history backfill.

## Definition Of Done
- PTO-009-AC1: Planning, Phase6, Phase7 and Phase8 boundaries follow the approved matrix; explicit no-commit, ignored-only/no-op, blockers and missing approval never create a commit.
- PTO-009-AC2: Dedicated branch selection is deterministic for substantive/high-risk work; existing correct branch is retained; no auto-stash/reset/force-add/push/merge/PR; one orchestrator owns staging and commits.
- PTO-009-AC3: New opt-in evidence binds complete source/dependency populations, regular-file modes/content, QA identity and explicitly typed workflow/product repository baselines; legacy strict behavior remains.
- PTO-009-AC4: Post-commit equivalence compares committed tree, index and live worktree; same bytes with new HEAD may qualify, but partial staging, hook mutations, unexpected paths, mode/dependency/environment/evidence drift and missing proof reject.
- PTO-009-AC5: Snapshot -> reviewer QA -> computed binding is acyclic; stored success cannot authorize PASS; FAIL/wrong-owner/history and schema downgrade never qualify; report bytes are not restamped.
- PTO-009-AC6: Artifact-only closure stays fresh; full/CI/updater remain full-required where contracted; all current/status/capture consumers use the same equivalence assessment.
- PTO-009-AC7: Offline synthetic commit/failure tests, policy-boundary compound negatives, consumer audit and post-fix current-diff review pass; pending cross-system impact blocks local commit and handoff until owner decides, never inferred.

## Planned Write Set
- .systems/ai/capabilities/parallel-task-orchestration-v1.json
- .systems/ai/capabilities/phase-commit-policy-v1.json
- .systems/ai/core/phase-commit-policy.md
- .systems/ai/core/autopilot.md
- .systems/ai/core/permissions.md
- .systems/ai/core/contract-compliance.md
- .systems/ai/core/execution-efficiency.md
- .systems/ai/core/distillation-state.md
- .systems/ai/core/command-routing.md
- .systems/ai/core/commands.md
- .systems/ai/core/workflow.md
- .systems/ai/core/parallel-task-orchestration.md
- .systems/ai/core/repository-modes.md
- .systems/ai/core/changelog.md
- .systems/ai/workflow/phase-6-distillation.md
- .systems/ai/workflow/phase-7-checkpoint.md
- .systems/ai/workflow/phase-8-final-check.md
- .systems/ai/templates/workflow/phase-6-distillation.template.md
- .systems/ai/templates/workflow/phase-7-checkpoint.template.md
- .systems/ai/templates/workflow/phase-8-final-check.template.md
- .systems/ai/templates/autopilot/readiness.template.md
- .systems/ai/templates/autopilot/state.template.md
- .systems/scripts/lib/qa-commit-binding.py
- .systems/scripts/verify-qa-commit-binding
- .systems/scripts/lib/qa-evidence.py
- .systems/scripts/check-qa-evidence
- .systems/scripts/lib/quality-record.py
- .systems/scripts/prepare-quality-record
- .systems/scripts/lib/capture-record.py
- .systems/scripts/lib/capture-state.py
- .systems/scripts/lib/validation-scope.py
- .systems/scripts/lib/parallel-orchestration.py
- .systems/scripts/lib/parallel-orchestration-tests.py
- .systems/scripts/lib/coordinator-status.py
- .systems/scripts/check-phase-commit-policy
- .systems/scripts/check-required-artifacts
- .systems/scripts/check-review-completeness-gate
- .systems/scripts/lib/validation-checks.json
- .systems/scripts/validate-workflow
- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/smoke/core.sh
- .systems/scripts/smoke/policy.sh
- .systems/scripts/smoke/manifest.json
- .systems/scripts/tests/phase-commit-policy.py
- AGENTS.md
- HUMANS.md
- README.md
Only changed consumer references and exact contract integration inside listed files. New helper/validator/test paths are new files; no source edits during planning.
PTO-D09 approves refresh of the existing parallel capability source pins after final source changes. Protocol/native-unverified/isolation/fallback/authority fields stay unchanged; this maintenance does not prove native support.

## Commit Boundary Contract
| Boundary | Necessary conditions | Result |
| --- | --- | --- |
| planning-range end | artifact QA, publishable tracked changes, installed default and no explicit prohibition | local scoped planning commit, then stop for implementation readiness |
| Phase6 | accepted task Quality and distillation, current source/evidence, approved stage scope | coherent implementation/capture commit |
| Phase7 | current checkpoint and new tracked synchronization changes | local commit; otherwise not-required |
| Phase8 | technical final check and actual explicit scoped final-owner-yes, fresh closure | local final-closure commit; otherwise no closure commit |
| ignored-only/no changes | runtime remains ignored, no force-add | no commit, explain |
| worker output | integrated accepted work with common QA, orchestrator owns index | worker cannot infer commit permission |

A future owner-approved implementation under the installed policy includes local boundary commits unless explicitly excluded; this is not retroactive. no-commit overrides defaults, not QA. Existing dedicated branch reused; large/high-risk/shared-contract/new multi-task work gets a dedicated branch before writes. Git collisions/detached or unknown ownership stop; no destructive remediation. Push/merge/PR never inferred.

## Versioned Freshness Protocol
- Versioned source snapshot v1 fields: schema, project/task identity, approved root-kind/repository identities, original HEAD per repository, complete population selectors with coverage reason, sorted path/type/mode/content entries (including explicit deletions), dependency inventory, verification environment/check references. Reject duplicate/unknown fields, unsafe paths and unsupported versions. The assessment opts in by a checksum-bound snapshot reference and explicit capability version; no inferred opt-in.
- Read-time binding output fields: schema, QA path/hash/run/identity, snapshot path/hash, actual repository identities/HEADs/tree IDs, compared population digest, artifact-evidence freshness, status eligible/ineligible/unknown, reasons and checked-at. All fields are recomputed; loading a saved eligible JSON cannot skip verification. Stable inputs do not include this output.
- Optional means opting into a distinct fail-closed wire version, not adding ignored fields to V2. NEW bound reports use full-qa-verification-v3 and a distinct bound artifact-kind discriminator mapped to the ordinary expected QA kind only by upgraded readers. No V2 compatibility marker or embedded old V2 run is copied into a new V3 report. Source baselines remain typed actual SHA values. Existing V2 reports retain their exact old eligibility behavior.
- Capture records consuming bound V3 QA use Capture schema: 3; versions1/2 are unchanged. Old capture readers reject schema3, and old qa-evidence readers reject the V3 marker/kind. New consumers explicitly recognize the pair and capability version. Do not automatically migrate an existing record. Unknown versions and mixed-version encodings reject. Historical integrity remains separate from current qualification.
- Audit every gate path, including check-qa-evidence dispatch, capture inventory, scoped/runtime validation, coordinator and orchestration parent/checkpoint gates. Test frozen old consumers against new records: none may issue verified-current/current PASS, even through legacy fallback. A consumer that ignores or accepts the new representation is a release blocker requiring Spec Fix Loop, not permission to advertise compatibility.
- Build immutable source snapshot BEFORE QA. Snapshot never contains its QA report hash or resulting commit SHA. Reviewer QA binds snapshot, original baseline identities and semantic sections. Read-time binding ties snapshot hash, immutable QA hash and actual current commit. This direction is acyclic.
- Snapshot inventory enumerates all relevant sources/dependencies including additions, deletions and regular-file modes. Unknown, omitted or newly discovered source input blocks equivalence. Explicit owned runtime roots are a separate typed population with fresh checks, not an arbitrary ignore glob.
- Producer must distinguish workflow repository HEAD from approved target repository HEAD and require explicit approved target root when supplied; no root guessed from a report path.
- verify-qa-commit-binding is read-only; no commit/stage/checkout/network. It recomputes commit-tree, index/worktree and evidence equivalence and reports eligible/ineligible/unknown plus reason. Missing/invalid proof exits nonzero. Output JSON is supporting evidence, not PASS.
- Actual commit must be the expected scoped commit extending the recorded baseline; unexpected rebase, merge or unrelated history does not qualify in V1. Later consecutive artifact-only commits require explicit complete chain verification, not ancestry-only trust.
- Verify current required environment/check bindings through existing authenticated receipts where reused. No new implicit key, no scripts-only promotion. Full/CI/updater continue fresh.
- Snapshot and QA remain immutable; computation result goes to /tmp or existing approved ignored storage. Readers verify live state each time; cache/result flags are not authority. If proof is lost, recompute from bound immutable inputs or require fresh QA.
- Changed semantic scope, DoD, required approval, QA evidence or dependency means re-QA; changed runtime artifacts mean fresh owned artifact closure. Unknown impact means broader verification. Never update hashes alone to repair an old PASS.
- Shared eligibility routine serves capture, QA and coordinator status; proof of content equivalence cannot rescue registered history, FAIL, wrong identity or missing approval.
- Migration and unsupported-version fallback: no automatic rewrite; old installed Workflow keeps old behavior and cannot consume new bound evidence as current PASS. Explicit capability required before using extension. No change to schema1 historical meaning or schema2 strict current-HEAD behavior.

## Normative Population And Receipt Coverage

The V1 population is independently derived by the verifier, not accepted from a
submitted selector. Workflow sources are the fixed smoke-fixture product roots:
`.systems/`, `.github/`, `AGENTS.md`, `HUMANS.md`, `README.md`, `.gitignore`.
Enumerate the union of baseline tree, current tree, index and non-ignored
untracked paths under these roots; retain deletion tombstones and compare the
complete sorted path set. Preserved skill context/legacy imports are typed data,
not active source; explicit dependencies may not point into excluded data.
Tracked files are never excluded merely because an ignore rule now matches.
Unknown ignored inputs under production roots stop equivalence, except known
generated Python bytecode; they are not read or silently admitted. Symlinks,
gitlinks, unsafe/private paths and ambiguous roots reject before content reads.

For an explicitly approved target repository, enumerate all Git-selected product
paths and require explicit typed owning-workspace and installed-workflow roots
for exclusion. Reject other nested repositories or unknown ignored dependencies.
The snapshot binds each root's canonical path, Git common-directory identity,
actual baseline HEAD, tree and separate path/type/mode/hash inventory. Runtime
evidence uses exact bound references to spec/DoD, owner approval, implementation
and review; those required roles may not be omitted or marked not-applicable.
Snapshot coverage does not include mutable status, capture or its own QA output.
These are separate typed closure artifacts, validated fresh after their changes.

Existing full-source receipts prove only workflow byte inventory, registered
check coverage and tools/environment, with their existing HMAC and explicit
key. They do not prove modes or target-product checks. The binding independently
compares source modes/complete paths at every read, and uses the receipt only for
the coverage it actually authenticates. Unsupported target/check coverage may
not be reused: require fresh bound evidence or report unknown/nonzero. No change
to execution-efficiency.py or report-validation-comparison is implied; those
paths are outside the approved write set. Never fabricate broader coverage from
a successful receipt or a saved binding result.

## Adaptive Data / Integration Verification Matrix
| Source shape | Expected state | Derived output | Forbidden state | Failure behavior | Automated check | Manual trace |
| --- | --- | --- | --- | --- | --- | --- |
| accepted snapshot -> semantic QA -> exact commit | current equivalent inputs | eligible supporting binding | invented new QA verdict | still require current QA/approval | synthetic commit test | prewrite -> review -> staged tree -> commit -> verifier |
| missing proof, stale inputs or wrong source repo | unknown/ineligible | no current qualification | HEAD-only or equal hash in foreign repo accepted | nonzero, refresh/readiness | negative bindings | reject before phase gate |
| partial staging, hook-mutated file, extra source, mode/delete change | ineligible | changed paths/reason | subset comparison gives success | stop/re-QA | mutation matrix | commit tree AND live worktree |
| runtime-only status/capture changes | fresh artifact checks needed | no global QA shortcut | old artifact closure reused blindly | rerun owned consumers | independent runtime fixture | full source receipt + current artifact closure |
| FAIL/history/no owner approval | ineligible for required gate | no promotion | equivalence grants permission | stop | policy and runtime negatives | binding -> semantic/owner gates |
| ignored-only or explicit no-commit | not-required/forbidden | no Git mutation | force-add/empty commit/push | preserve index/worktree | offline boundary scenarios | phase output -> stage readiness |

## Verification
Use Python stdlib and local synthetic Git repositories only; tests may commit only inside temporary fixtures after future implementation approval. Cover failed commit, hooks, unrelated staged changes, no changes, quoted compound unsafe policy, missing proof, forged result, repository identity mismatch, changed approval/DoD, unknown schema and report self-reference. No real branch/commit in current planning.
Targeted tests: tests/phase-commit-policy.py, check-phase-commit-policy, QA/capture/coordinator conformance, existing execution-efficiency regressions. Shared helper must be included in policy-boundary audit where applicable. Run affected smoke groups then fresh full after semantic integrated review. CI/updater exemptions are forbidden.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: accepted owner request, PTO-D07, architecture delta and PTO-009 AC
- Testable DoD / acceptance conditions: every numbered AC maps to a regression and semantic review below
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after full specification and prerequisite Plan QA
- Implementation Quality Closure route: phase-5-quality
- Required verification: adversarial and producer-consumer matrix, unit/integration tests, targeted scripts, smoke suite, fresh full source gate after semantic review
- Quality-ready criteria: all AC evidenced with no unresolved P0/P1/material P2; no borrowed historical/current verdict
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: separate high-risk implementation/Phase5 approval before relevant gate
- Next route: stop before implementation-range readiness

## Implementation Slice Plan
- Source: this spec, canonical plan and PTO-D07
- DoD source: numbered AC in this specification
- Scope: exact paths above; extra path or behavior requires Spec Fix Loop before writes
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-009-S1 | Introduce bounded shared contract/helper | listed helper and contract files | design invariants and negative cases | tests and source diff | planned |
| PTO-009-S2 | Integrate actual producers and consumers | listed consumers/templates | same inputs give agreed outcome | conformance matrix and failure traces | planned |
| PTO-009-S3 | Regress policy/runtime and document | listed tests/smoke/docs | all AC and preserved coverage | current-diff review and full source result | planned |
- Stop rule: scope growth, missing facts/approval, unprovable equivalence or unsafe effects stop dependent writes.
- Compact mode: not-applicable for high-risk work.

## Gates, Rollback And Delivery
Dependency: PTO-CAP-008-capture-parity through formal Quality and Phase6; refresh009 Spec QA after008 source changes. Each task has separate Spec QA, formal Phase5 and Phase6. Final Phase7 after009; existing checkpoint cadence is not counted per slice.
No deadline/timebox, inherited owner opt-out. No cut of the quality floor to save time.
Rollback: stop using newly advertised capability; preserve evidence; reviewed source rollback only after explicit approval. Never rewrite history or downgrade schema to pass.
Implementation unstarted. Existing PTO001..007 approvals do not authorize these writes. Commit/push/final-owner-yes remain outside current planning.
Before final closure, rereview affected prior PTO evidence and original native-unverified limitation; do not rebind old hashes without a real assessment.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D07 planning scope
- Questions asked: none
- Auto-resolved reversible decisions: serial execution design and exact names
- Optional owner refinements: added-scope cross-system impact remains pending; resolve before local commit or handoff, not optional and not push-only
- Decision artifacts: decisions/pto-pre-final-planning-authorization.md
- Next route: Spec QA then stop

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: retain design and safety boundaries
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: PTO-009 design boundaries
- Suggested entry summary: Scope, proof obligations and skipped implementation are explicit.
