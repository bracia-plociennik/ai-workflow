# Project Plan

Current extension: PTO-D10 adds PTO-BRIDGE-010-compatibility-adaptation, high risk,
three serial slices and eight AC from its specification. Architecture delta:
architecture/pre-final-compatibility-delta.md. Predecessor evidence is regression
reviewed, never imported as new permission. No deadline/timebox/native/commit/push.
Route: Architecture QA, Plan QA, Spec QA, implementation, actual high-risk Phase5,
Phase6/7 and requested technical Phase8; no final-owner-yes.
## Metadata
- Project: parallel-task-orchestration-v1
- Date: 2026-10-03
- Workflow phase: phase-2-project-plan
- Result: completed
- Risk: high
Current revision: pre-final CR001/002; nine tasks complete through actual Phase5 and accepted Phase6. Final checkpoint008/009 is complete; requested technical Phase8 remains separate from final-owner-yes.
## Sources
context.md; decisions/owner-decisions.md; architecture/phase-1-architecture.md; quality/phase-1-architecture-qa.md; intake/phase-0-repo-intake.md.
## Planning Constraints
Original planning authority was planning-only. Subsequent scoped high-risk implementation approvals are recorded in decisions/implementation-approval.md and decisions/pto-quality-range-approval.md; PTO-D06 revises only006AC6. Current task index records actual execution, not permission inferred from this plan.
The feature is developed serially; no live workers, model calls or worktrees in this planning-range.
Task packaging not requested. New behavior is not used to approve its own implementation.
## Tasks
Original planning-only approval is historical. PTO-D08 approves serial008/009 implementation and applicable quality/capture; PTO-D09 adds capability pin maintenance. No actual commit/push/final-owner-yes is authorized.

### PTO-CAP-008-capture-parity: Canonical capture consumer parity
- Goal: Canonical capture consumer parity, without changing original PTO release or native capability.
- Scope: exact source write set in specs/phase-3-pto-cap-008-capture-parity-specification.md; paths outside it require Spec Fix Loop and approval.
- Out of scope: target/nested changes, historical rewrites, native tests, commits/push during current planning.
- Definition of Done:
  - PTO-008-AC1: Identical selected records have identical structural/quality classifications through no-arg, --project and --runtime-only; differences due to intentionally different populations are reported, not widened.
  - PTO-008-AC2: Valid schema1 historical/advisory records including legacy ID/gate and absent derived output remain unchanged; historical integrity never supplies current QA PASS.
  - PTO-008-AC3: Schema2 ready/completed requires current owning-project implementation-quality PASS, matching source HEAD/hash/identity and explicit derived state; completed additionally requires one unique accepted owned distillation. Ready may have no distillation yet.
  - PTO-008-AC4: Reject missing references required by the state, foreign evidence paths, unsafe paths/symlinks, unknown schema, duplicate fields/work IDs/distillation reuse, inconsistent derived output and unaccepted completed distillation. Wrong QA kind/identity/freshness rejects schema2 ready/completed; schema1 remains historical/advisory rather than being promoted to current QA.
  - PTO-008-AC5: Historical scoped manifest populations and foreign/nested repository exclusions are unchanged; all selected records, not just successful rows, participate in duplicate detection.
  - PTO-008-AC6: Consumer conformance tests exercise positive and negative completed/ready records, not only pending-quality; full supporting validation and current-diff review preserve PTO.
- Dependencies: none from009; preserved PTO source baseline.
- Risk type: high
- Main risk: false QA eligibility or unintended write/commit authority.
- Start condition: accepted current Spec QA, explicit new-scope high-risk approval and implementation readiness.
- End condition: all AC evidenced; formal Phase5, accepted Phase6 and required Phase7; current whole-project final check later.
- Readiness status: ready, consumed
- Requires user decision before implementation: no, PTO-D08/D09 recorded
- Current task status: completed through actual Phase5 and accepted Phase6; final checkpoint008/009 completed.
- Test plan: synthetic positive/negative consumer and Git-boundary matrices in the specification.

### PTO-GIT-009-phase-commits: Phase commit boundaries and QA freshness
- Goal: Phase commit boundaries and QA freshness, without changing original PTO release or native capability.
- Scope: exact source write set in specs/phase-3-pto-git-009-phase-commits-specification.md; paths outside it require Spec Fix Loop and approval.
- Out of scope: target/nested changes, historical rewrites, native tests, commits/push during current planning.
- Definition of Done:
  - PTO-009-AC1: Planning, Phase6, Phase7 and Phase8 boundaries follow the approved matrix; explicit no-commit, ignored-only/no-op, blockers and missing approval never create a commit.
  - PTO-009-AC2: Dedicated branch selection is deterministic for substantive/high-risk work; existing correct branch is retained; no auto-stash/reset/force-add/push/merge/PR; one orchestrator owns staging and commits.
  - PTO-009-AC3: New opt-in evidence binds complete source/dependency populations, regular-file modes/content, QA identity and explicitly typed workflow/product repository baselines; legacy strict behavior remains.
  - PTO-009-AC4: Post-commit equivalence compares committed tree, index and live worktree; same bytes with new HEAD may qualify, but partial staging, hook mutations, unexpected paths, mode/dependency/environment/evidence drift and missing proof reject.
  - PTO-009-AC5: Snapshot -> reviewer QA -> computed binding is acyclic; stored success cannot authorize PASS; FAIL/wrong-owner/history and schema downgrade never qualify; report bytes are not restamped.
  - PTO-009-AC6: Artifact-only closure stays fresh; full/CI/updater remain full-required where contracted; all current/status/capture consumers use the same equivalence assessment.
  - PTO-009-AC7: Offline synthetic commit/failure tests, policy-boundary compound negatives, consumer audit and post-fix current-diff review pass; pending cross-system impact blocks local commit and handoff until owner decides, never inferred.
- Dependencies: blocking PTO-CAP-008-capture-parity through Quality and Phase6.
- Risk type: high
- Main risk: false QA eligibility or unintended write/commit authority.
- Start condition: accepted current Spec QA, explicit new-scope high-risk approval and implementation readiness.
- End condition: all AC evidenced; formal Phase5, accepted Phase6 and required Phase7; current whole-project final check later.
- Readiness status: ready, consumed under PTO-D08/D09
- Requires user decision before implementation: no, scoped PTO-D08/D09 approval granted
- Current task status: implemented; actual formal Phase5 PASS and accepted Phase6, final checkpoint follows.
- Test plan: synthetic positive/negative consumer and Git-boundary matrices in the specification.

### PTO-CORE-001-contract-routing: Contract and routing
- Goal: Align installed execution contracts around one orchestrator and delegated units.
- Scope: .systems/ai/core/parallel-task-orchestration.md, .systems/ai/core/parallel-work-policy.md, .systems/ai/core/autopilot.md, .systems/ai/core/implementation-slicing.md, .systems/ai/core/command-routing.md, .systems/ai/core/operating-model.md, .systems/ai/core/workflow.md, .systems/ai/workflow/phase-2-project-plan.md, .systems/ai/templates/autopilot/readiness.template.md, .systems/ai/templates/autopilot/state.template.md, .systems/scripts/check-parallel-task-orchestration, .systems/scripts/lib/validation-checks.json, .systems/scripts/validate-workflow, .systems/scripts/check-required-artifacts, .systems/scripts/smoke/core.sh, .systems/scripts/smoke/manifest.json, .systems/scripts/check-validator-smoke-tests, .systems/scripts/check-review-completeness-gate.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-001-AC1: One coordinator-owned implementation run can delegate units without creating independent autopilots.
  - PTO-001-AC2: Dynamic parallelism is gated by dependencies, resources, backend capability and approval; missing capability stays serial.
  - PTO-001-AC3: Packaging remains optional; no per-unit checkpoint, full workflow or formal PASS.
  - PTO-001-AC4: Existing default-policy validators and smoke expectations stay aligned; safe prohibition plus unsafe exception fails.
- Dependencies: blocking none; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Authority weakening or contradictory installed policy.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: Keep feature capability inactive until PTO-006. Shared validation registry modifications are bounded to registering this contract check.

### PTO-ALLOC-002-adaptive-allocation: Dependency and capacity planning
- Goal: Compute conservative parallel-ready units and explain worker count.
- Scope: .systems/scripts/lib/parallel-orchestration.py, .systems/scripts/plan-parallel-work, .systems/ai/templates/orchestration/run.template.json, .systems/ai/templates/orchestration/unit.template.json, .systems/scripts/smoke/core.sh, .systems/scripts/smoke/manifest.json, .systems/scripts/check-validator-smoke-tests, .systems/scripts/lib/parallel-orchestration-tests.py.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-002-AC1: Reject duplicate IDs, cycles, missing dependencies, unsafe paths and unknown access modes.
  - PTO-002-AC2: Planner selects a deterministic conflict-free ready set under observed capacity minus all active workers and resource reservations.
  - PTO-002-AC3: Read/write, write/write and parent/child paths conflict; read/read may run concurrently; unknown resources default exclusive.
  - PTO-002-AC4: Zero ready units reports blocked/complete accurately; one unit uses serial; no hard-coded two/three limit.
  - PTO-002-AC5: Plan CLI is read-only and emits structured reasoned proposals, not authorization or dispatch.
- Dependencies: blocking PTO-CORE-001-contract-routing; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: False independence or over-allocation.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: Use Python standard library, schema-1 JSON with unknown keys/types rejected. CLI --manifest <file> --format json|human; no shell commands in manifest executed. Reuse existing smoke group rather than adding a public group name. Put new tests in lib/parallel-orchestration-tests.py invoked from supplemental core smoke IDs; preserve all five group names and frozen regions. Update only supplemental manifest entries and current file hashes.

### PTO-ISO-003-isolated-delegation: Worker preflight and result contract
- Goal: Make delegated context, isolation and evidence boundaries explicit and checkable.
- Scope: .systems/scripts/lib/parallel-orchestration.py, .systems/ai/core/parallel-task-orchestration.md, .systems/ai/templates/orchestration/unit.template.json, .systems/ai/templates/orchestration/result.template.json, .systems/ai/templates/orchestration/worker-prompt.template.md, .systems/scripts/smoke/core.sh, .systems/scripts/lib/parallel-orchestration-tests.py, .systems/scripts/smoke/manifest.json.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-003-AC1: Every unit binds task/slice, approved DoD, source snapshot, minimal read context, allowed writes/resources, stop conditions and output schema.
  - PTO-003-AC2: Preflight validates actual backend workspace identity and available write constraints; prompt text is not sandbox proof.
  - PTO-003-AC3: Worker output has attempt handle, actual diff/input hashes, check evidence, findings, skipped checks and risk.
  - PTO-003-AC4: Results cannot overwrite canonical routers, approval or capture; out-of-scope actual writes block acceptance.
  - PTO-003-AC5: Worktree creation/cleanup requires existing authorization; no automatic destructive cleanup or data copying.
- Dependencies: blocking PTO-ALLOC-002-adaptive-allocation; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Worktree mistaken for complete sandbox or worker receives excessive authority/context.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: Native tool calls stay in agent execution path; no model API service or transport added. Fake adapter exercises protocol offline. Live backend verification is a later gated smoke, not assumed support.

### PTO-RUN-004-lifecycle-recovery: Single-writer lifecycle and recovery
- Goal: Persist safe unit/attempt ownership and reconcile interrupted work.
- Scope: .systems/scripts/lib/parallel-orchestration.py, .systems/scripts/manage-parallel-run, .systems/scripts/lib/validation-scope.py, .systems/ai/templates/orchestration/run.template.json, .systems/ai/core/parallel-task-orchestration.md, .systems/scripts/smoke/core.sh, .systems/scripts/lib/parallel-orchestration-tests.py, .systems/scripts/smoke/manifest.json.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-004-AC1: State transitions reject duplicate/stale attempts, invalid owner, revision mismatch and impossible dependencies.
  - PTO-004-AC2: Manifest updates are atomic and single-writer; reservation acquired before dispatch; rejected mutations leave bytes unchanged.
  - PTO-004-AC3: Resume reconciles platform handles, actual files and evidence before restart; unknown liveness keeps reservation.
  - PTO-004-AC4: Failure blocks dependent units, preserves independent evidence and never silently retries unknown external effects.
  - PTO-004-AC5: Retry ceilings respect parent workflow; no auto-deletion of stale locks, force reset, auto commit or recursive spawn.
  - PTO-004-AC6: Canonical orchestration manifest and sanitized result metadata participate in owned runtime inventory/freshness; private raw logs, foreign repos and worktrees do not enter the owned namespace.
- Dependencies: blocking PTO-ISO-003-isolated-delegation; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Double execution or corruption on resume.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: CLI subcommands validate, transition, reconcile. Mutations require explicit run root, expected revision and coordinator ID. Reconcile defaults read-only; accepted mutation only via explicit transition. Lock protects local races, not malicious host/distributed ownership.

### PTO-QA-005-integration-acceptance: Integration and common QA
- Goal: Separate submitted/accepted/integrated results and preserve formal task gates.
- Scope: .systems/scripts/lib/parallel-orchestration.py, .systems/ai/core/parallel-task-orchestration.md, .systems/ai/core/quality-review.md, .systems/ai/core/full-qa-verification.md, .systems/ai/workflow/phase-5-quality.md, .systems/ai/templates/orchestration/integration-review.template.md, .systems/scripts/smoke/core.sh, .systems/scripts/lib/parallel-orchestration-tests.py, .systems/scripts/smoke/manifest.json.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-005-AC1: Acceptance checks actual worker diff, provenance, allowed changes, DoD and check evidence, not prose done.
  - PTO-005-AC2: Same-task dependents bind accepted immutable outputs; cross-task gates retain Quality/capture/checkpoint prerequisites.
  - PTO-005-AC3: Integration is serial with destination before/after fingerprints; conflicts stop without auto resolve.
  - PTO-005-AC4: Common QA reviews integrated behavior, consumers and failure paths; no combining worker PASS into task PASS.
  - PTO-005-AC5: Checkpoint counts tasks rather than units; dispatch respects every-three-task/final barriers; one capture writer.
- Dependencies: blocking PTO-RUN-004-lifecycle-recovery; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Local evidence mistakenly promoted to global PASS.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: Tool verifies structural evidence and source bindings only, never generates semantic acceptance or owner approval. Reviewer supplies decision; rejection leaves integrated baseline unchanged. Do not auto merge/cherry-pick inside generic manifest validator.

### PTO-COMPAT-006-capability-evaluation: Capability negotiation and evaluation
- Goal: Expose tested support conservatively and measure integrated behavior.
- Scope: .systems/ai/capabilities/parallel-task-orchestration-v1.json, .systems/scripts/lib/coordinator-status.py, .systems/scripts/report-coordinator-status, .systems/ai/core/runtime-integrity.md, .systems/scripts/check-parallel-task-orchestration, .systems/scripts/smoke/core.sh, .systems/scripts/smoke/manifest.json, .systems/scripts/lib/parallel-orchestration-tests.py.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
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
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: PTO-D06 explicitly scopes release to installed protocol and conservative discovery. Native verification is deferred, not passed. Bounded test permission remains conditional on actual isolation; failed preflight prohibits launch. No fixed model chosen.

### PTO-DOCS-007-handoff-guidance: Guidance and AI System handoff
- Goal: Publish concise user guidance and one evidence-backed counterpart adaptation handoff.
- Scope: AGENTS.md, HUMANS.md, README.md, .systems/ai/core/commands.md, .systems/ai/core/changelog.md, .systems/ai/templates/orchestration/README.md.
- Out of scope: unrelated refactors, production data, AI System product and unapproved external effects.
- Definition of Done:
  - PTO-007-AC1: Entrypoints remain concise and route to one canonical orchestration contract.
  - PTO-007-AC2: Document dynamic count, one owner, nonrecursive units, QA, serial fallback and capability versions.
  - PTO-007-AC3: One privacy-safe External Memory artifact covers this scope with tested baseline, schema, limitations, source paths and adaptation checklist.
  - PTO-007-AC4: Do not claim AI System implementation or copy private runtime; no automatic counterpart update.
  - PTO-007-AC5: Final source semantic review and full validation precede publication readiness; Phase 8 still owner-only.
- Dependencies: blocking PTO-COMPAT-006-capability-evaluation; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Counterpart trusts unsupported capability or imports status/approval.
- Start condition: owner high-risk implementation approval, current Spec QA, safe environment and blocking predecessors complete through required gates.
- End condition: all AC evidenced; formal Phase 5 and Phase 6; Phase 7 when due.
- Readiness status: conditional
- Requires user decision before implementation: yes
- Notes: External Memory path: ai-workflow-workspace/external-memory/memory/<completion-date>-parallel-task-orchestration-ai-system-handoff.md. Runtime handoff is not tracked source. Changelog path verified as .systems/ai/core/changelog.md.

## Final Execution Order
1. PTO-CORE-001-contract-routing - completed, formal Quality PASS and Phase 6 accepted
2. PTO-ALLOC-002-adaptive-allocation - completed, formal Quality PASS and Phase 6 accepted
3. PTO-ISO-003-isolated-delegation - completed, formal Quality PASS and Phase 6 accepted
4. PTO-RUN-004-lifecycle-recovery - completed, formal Quality PASS and Phase6 accepted
5. PTO-QA-005-integration-acceptance - completed, formal Quality PASS and Phase6 accepted
6. PTO-COMPAT-006-capability-evaluation - completed in approved protocol-only scope, native verification deferred/unverified
7. PTO-DOCS-007-handoff-guidance - completed, formal Quality PASS and Phase6 accepted; final checkpoint and owner-requested technical Phase8 follow
8. PTO-CAP-008-capture-parity - completed: actual Phase5 PASS and accepted Phase6; final checkpoint008/009 completed
9. PTO-GIT-009-phase-commits - completed: actual formal Phase5 PASS and accepted Phase6 under PTO-D08/D09
Task-level dependencies are blocking, not worker-unit dependencies. Before each next task re-evaluate spec freshness against predecessor changes.
Original checkpoints after3,6 and7 are recorded history. New tasks008/009 count as
two new parents; final checkpoint after009 is mandatory, not one checkpoint per slice.
No permission to execute this order from planning completion alone.
Initial task readiness fields in001..007 are frozen planning conditions, not
current execution routers. Actual execution state follows this final order and
tasks.md/status.md. No new scope or approvals arise from this synchronization.

## Architecture Coverage Map
| Area | Task |
| --- | --- |
| Authority and routing | PTO-001 |
| Graph and dynamic allocation | PTO-002 |
| Write/resource isolation and worker protocol | PTO-003 |
| State/recovery/ownership | PTO-004 |
| Acceptance/integration/common QA | PTO-005 |
| Version handshake/tests/measurement | PTO-006 |
| Human guidance and counterpart handoff | PTO-007 |
| Canonical historical/current capture consumer parity | PTO-CAP-008 |
| Local commit boundaries and verified post-commit source equivalence | PTO-GIT-009 |

## Conditional Tasks
Implementation approval for008/009 is PTO-D08/D09, conditional on current task gates. Native-backend verification in PTO-006 requires actual safe runtime availability and approval; fake evidence cannot replace it for an operational-support claim.
Fallback is ordinary safe serial work without worker dispatch. PTO-D06 explicitly
changes the release scope: installed protocol may complete with native operational
support unverified; native verification is deferred, never counted as completed.
No weakening of isolation, permissions or QA. See decisions/pto-006-007-protocol-only-scope.md.

## Shared Write Set And Integration
parallel-orchestration.py, orchestration schemas, policy contract and smoke fixture are deliberately single-writer sequential task outputs.
Every new script/helper has tests in its own task, not deferred until PTO-006.
Existing policy validators affected by wording must be inventoried in Spec QA; exact additional edits require spec fix-loop before writes, not permission by broad directory glob.

## Definition Of Done
All nine task AC and common integration QA; no unresolved P0/P1/material P2; unchanged authority/serial fallback; fresh full supporting validation. Original PTO-001..007 retain their privacy-safe AI System handoff requirement. Counterpart impact for new008/009 is pending an owner decision before their commit/handoff; neither yes nor no is inferred.
No guarantee of speedup. Synthetic results are not production/model performance.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: accepted owner context, architecture and task AC above
- Testable DoD / acceptance conditions: nine bounded task contracts; original seven retained plus008/009 AC, parity/equivalence matrices, conditional dependencies and separate QA/capture routes.
- Artifact QA route: phase-2-plan-qa
- Artifact QA trigger: after plan and canonical task index completed.
- Implementation Quality Closure route: phase-5-quality
- Required verification: task/index/dependency audit, adversarial scenarios, local regression tests per task, common integrated QA, final full scripts after semantic review.
- Quality-ready criteria: all task contracts testable, PTO-D08/D09 implementation authority explicit, current artifact gates, no hidden design blocker.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none before scoped implementation; counterpart impact pending only before commit/handoff.
- Next route: phase-2-plan-qa

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Source: owner explicitly requested no deadline or timebox for this project.
- Must-have outcome: safe dynamic delegation, single execution owner, integrated QA; historical/current capture parity and safe local commit boundaries with independently verified QA freshness.
- Cutline/deferred scope: scheduler, recursive delegation, production effects and AI System implementation.
- Quality floor: current artifact QA, scoped evidence, no unresolved material findings.
- Overrun checkpoint: stop for new scope or permissions, never invent a delivery deadline.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D01 through PTO-D09; D06 preserves native-unverified scope, D08 approves scoped implementation/Quality/capture, D09 permits capability pins.
- Questions asked: none; prior owner answers remain applicable.
- Auto-resolved reversible decisions: canonical artifact names and serial planning.
- Optional owner refinements: no planning blocker; added-scope cross-system impact decision is required before later commit/handoff.
- Decision artifacts: decisions/owner-decisions.md; decisions/pto-006-007-protocol-only-scope.md; decisions/pto-008-009-implementation-approval.md; decisions/pto-capability-scope-extension.md
- Next route: fresh artifact consistency, final checkpoint and requested technical Phase8; no final-owner-yes.

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: preserve ownership and safety decisions.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Dynamic orchestration without duplicate authority
- Suggested entry summary: Single execution owner and evidence-backed integration; final AI System handoff after actual QA.
