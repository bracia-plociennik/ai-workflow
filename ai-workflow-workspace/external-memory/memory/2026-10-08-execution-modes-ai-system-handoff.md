# Cross-System Upgrade Handoff

## Metadata
- Date: 2026-10-08
- Source system: ai-workflow
- Counterpart: ai-system
- Status: accepted-for-handoff
- Implementation status: implemented on local branch codex/execution-modes-v1; not pushed or installed in the counterpart
- Privacy/scope check: pass
- Authority: advisory coordination context

## Concept And Intended Outcome
Default Auto reduces interaction during approved work, selecting covered reversible technical/preferences/local architecture choices and reporting assumptions and override costs. Explicit Human Coop consults material choices in 1-3 grouped questions. Mode is independent from technical autopilot.mode, phase and permissions.

## Owner Decisions
- Default Auto; Human Coop task-local unless explicitly project/session-wide.
- No deadline/timebox and no implicit 300-minute Auto run budget; retain explicit/legacy limits and retry/no-progress stops.
- Actual accepted concrete scope may cover named local high-risk implementation and formal Quality assessment, not its result.
- One handoff; no counterpart/nested edits, paid evals, push or merge.

## Cross-System Impact
- Owner decision: yes
- Counterpart: ai-system
- Handoff artifact: external-memory/memory/2026-10-08-execution-modes-ai-system-handoff.md

## Safety And Authority Boundaries
Mode never grants approval. New protected effects, production, costs, destructive actions, critical risk and platform approvals retain their boundaries. Git revert cannot undo exposure or external effects. One coordinator owns shared state, decisions, integrated QA and commits. Block affected units/dependents and unknown/shared resources; independent continuation requires actual verified evidence.

Legacy missing execution metadata does not gain autonomy. Resume preserves recorded mode and checks actual baseline, executors, gates and approvals. Planning-only ends with a reviewed plan. Phase8 requires a separately explicit scope and never implies final-owner-yes. Local scoped commits follow phase policy; no automatic push, main merge or branch deletion.

## Source-System References
- .systems/ai/core/execution-modes.md
- .systems/ai/core/owner-decision-checkpoints.md
- .systems/ai/core/autopilot.md
- .systems/ai/core/delivery-constraints.md
- .systems/ai/core/permissions.md
- .systems/ai/templates/autopilot/readiness.template.md
- .systems/ai/templates/autopilot/state.template.md
- .systems/ai/templates/autopilot/task-decisions.template.md
- .systems/ai/templates/autopilot/execution-readiness.template.json
- .systems/scripts/check-execution-modes
- .systems/scripts/lib/execution-modes.py
- .systems/scripts/tests/execution-modes.py

## Implemented Interface
check-execution-modes --state path.json is pure schema/readiness inspection, not dispatch or proof of authority. Schema1 records mode/scope/source/ref, unit actions and dependencies, resource claims and pending/agent-choice/owner-approved dispositions. It rejects malformed explicit modes, duplicate keys, linked input, cyclic/unknown dependencies, uncovered actions, empty implementation metadata and premature completion.
Summary decision IDs do not replace full decision request/alternatives/impact/artifact fields. Verify actual sources before acting.

### Compatibility Adaptation: EM-COMPAT-002
Portable capability: .systems/ai/capabilities/execution-modes-v1.json, contract 1; exact auto -> auto and human -> human-coop mapping, six closed behaviors and fourteen pinned relative sources. It is support metadata only.
New projections use schema 2. Unique chronological attempt IDs, stable unit/cause IDs and optional progress fingerprints enforce three unsuccessful attempts, while the existing 2 Spec / 2 Quality / 32 total limits remain stricter independent budgets. Completed results after the last permitted successful fix remain valid; exhausted budgets prohibit more retries. Legacy schema 1 remains readable as legacy-unverified, not recovery proof.
The current AI System adapter does not consume this portable capability directly. It uses its own reviewed contract 1 profile with fourteen source hashes/modes, tested_commit, mode_mapping, delivery_mapping and inspector path, plus committed HEAD/index/live equality. auto-unconstrained maps to auto-unbounded. Forward the original projection and mode/scope/source, not a reconstructed weakened state.
Compatibility evidence uses a frozen actual adapter/preflight/harness and a separately generated profile in an isolated synthetic committed candidate. All 23 counterpart scenarios and five extra recovery/tamper scenarios pass; 38 Workflow deterministic tests pass. No counterpart source or installed profile was changed. Current source commit is eb5f4d6973d2e0d3fadc15c3b8d3412741ad3249. Source-copy paths/bytes/modes are equal; fresh formal prerequisite QA and both implementation Qualities bind this HEAD. Phase6 capture and Phase7 synchronization are completed. Technical final acceptance remains awaiting-owner-final-yes; final evidence is owned by projects/execution-modes-v1/quality/phase-8-final-check.md, not this advisory handoff.

### Adoption Boundary
The AI System owner must separately approve its reviewed installed-source profile for the actual published Workflow version and validate that installation. This handoff and the synthetic profile do not authorize nested updates, native dispatch or real approval inference. Synthetic protocol compatibility is established; installed interoperability and model adherence remain unclaimed.

## Historical CORE Verification
29 offline tests and 16 supplemental smoke cases cover the implemented contract and inspector. Full validation at actual committed HEAD 9d00bba3a17a9208b42a59ea29b0796ae5f15a6e completed with result=pass, exit_code=0, duration_seconds=739; all smoke groups passed. Semantic current-diff, adversarial and producer-consumer reviews preceded scripts; scripts remain supporting-only.

Local source commits: d3536e5 and 9d00bba on codex/execution-modes-v1; neither is pushed by this work. Fresh formal prerequisite QA and implementation Quality were assessed at that committed HEAD. Phase 6 capture and Phase 7 checkpoint are recorded in the owning project. The separately requested technical Phase 8 route follows that checkpoint and retains awaiting-owner-final-yes; no owner acceptance or counterpart rollout is claimed.

## Current Compatibility Verification
- Assessed source commit: eb5f4d6973d2e0d3fadc15c3b8d3412741ad3249, local branch codex/execution-modes-v1, clean tracked worktree and empty index.
- Fresh full profile on this committed source and owning execution-modes-v1 runtime: result=pass, exit_code=0, duration_seconds=698; all five smoke groups pass, smoke duration_seconds=664.
- Fresh source tests: 38 deterministic regressions. Frozen actual counterpart integration: 23 scenarios plus five recovery/tamper extras, all pass; frozen source preservation verified.
- Architecture/Plan/both Spec QA and both implementation Qualities are current at this HEAD. Earlier assessments are preserved as history, not restamped.
- Phase6 and Phase7 are complete for both tasks. Technical final-check evidence remains distinct from final-owner-yes; neither this handoff nor installed capability metadata grants final acceptance.
- Semantic/adversarial full-current-diff and producer-consumer review precede scripts; scripts remain supporting-only. No paid/model/native trials, installation, counterpart source writes, push or merge.

## Counterpart Adaptation Checklist
- [ ] Compare installed contracts; do not import historical status/approvals.
- [ ] Persist interaction mode separately from technical mode.
- [ ] Resolve task/session/project scope and resume identity.
- [ ] Qualify existing global decision stops into verified affected-unit blocking.
- [ ] Keep actual approval verification and protected-effect gates.
- [ ] Preserve full queued decision records and coordinator ownership.
- [ ] Remove only implicit new Auto time budget, not real limits.
- [ ] Test malformed modes, dependency/resource conflicts, partial completion, plan-only and explicit final-check boundaries.
- [ ] Adapt own quality/capture/commit policy through separately approved counterpart work.

## Privacy Check
- Raw client data included: no
- Secrets or credentials copied: no
- Private runtime or production identifiers copied: no
- Content: reusable workflow integration only; references repository-relative.

## Residual Risk
No model behavior eval, native dispatcher trial, real approval attestation or counterpart rollout was performed. Synthetic tests establish contract/inspector behavior, not perfect model judgment. Interoperability and installed AI System support remain unclaimed.
