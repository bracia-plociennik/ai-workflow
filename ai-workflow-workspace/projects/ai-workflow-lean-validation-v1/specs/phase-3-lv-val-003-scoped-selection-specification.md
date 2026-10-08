# Phase 3 Specification: LV003

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Task/package ID: LV-VAL-003-scoped-selection.
- Task/package name: Explicit scope and dependency-aware checks.
- Date: 2026-09-30.
- Readiness: dependencies resolved; fresh Spec QA and task-scoped readiness required before writes.
- Baseline: 00708146b6859bf3f2452baf1a5ef918c178c48f; clean tracked branch codex/ai-workflow-lean-validation-v1, no push.

## Sources

- Project plan: planning/phase-2-project-plan.md; Plan QA: quality/phase-2-plan-qa.md.
- Architecture: architecture/phase-1-architecture.md and its Architecture QA.
- Intake: intake/phase-0-repo-intake.md; decisions: decisions/lv-decisions.md; context.md.
- Existing dependency outputs: LV001 and LV002 formal current Quality PASS, accepted Phase 6, local source commits and corrected LV002 baseline.

## Task Contract

- Goal: Remove duplicate checks without presenting a narrow execution as complete coverage.
- Scope: Explicit scope manifest, dependency closure/deduplication, canonical runtime discovery and profile/routing integration.
- Out of scope: No cache, inferred check selection, all-project scans for a selected runtime project, or lowering CI/updater requirements.
- Definition of Done: Selected checks and mandatory deps run once per normalized scope; no unconditional fast prelude; requested success distinct from coverage completeness; unknown/unreadable/deleted/shared cases handled safely; current public profiles preserved.
- Dependencies: LV001, LV002.
- Risk type: high; formal workflow-maintenance.
- Main risk: false confidence, coverage loss or unintended authority change.
- Start condition: LV-DEC-002, current source baseline, accepted Spec QA and predecessor quality evidence.
- End condition: testable task DoD, semantic findings-first Phase 5, applicable explicit full validation and no unresolved material findings; later capture follows phase rules.
- Requires user decision before implementation: no new decision; LV-DEC-002 approves this exact source range, subject to fresh Spec QA/readiness.

## Proposed Write Set

- .systems/scripts/validate-workflow
- .systems/scripts/lib/validation-scope.py (new)
- .systems/scripts/lib/validation-checks.json (new)
- .systems/scripts/check-status-consistency
- .systems/scripts/check-qa-evidence
- .systems/scripts/check-distillation-state
- .systems/scripts/check-naming
- .systems/scripts/check-validation-profiles
- .systems/scripts/check-validation-routing
- .systems/scripts/check-validator-smoke-tests
- .systems/ai/core/validation-profiles.md
- .systems/ai/core/validation-routing.md
- .systems/ai/core/contract-compliance.md
- .systems/ai/core/commands.md
- .systems/ai/workflow/phase-7-checkpoint.md
- .systems/ai/templates/workflow/phase-7-checkpoint.template.md
- AGENTS.md
- HUMANS.md
- README.md

These paths are the proposed task ceiling, not current write permission. Brace expressions enumerate only named sibling files. New helpers are explicitly marked new. Any additional source consumer discovered at pre-write must be reconciled in this spec and Spec QA before editing.

## Dependency Status

- LV001: current formal Quality PASS and Phase 6 inspected; preserve exact negative-test outcomes and the typed current QA/status reader.
- LV002: current formal Quality PASS, Phase 6 and commit 0070814 inspected. Corrected frozen full baseline has three complete runs, 40 checks and 660 smoke IDs; source/timing/coverage identity verified. Median 805.782230 seconds and broad range are baseline only, not performance improvement.
- Source approval/base: LV-DEC-002 approved for LV001-LV006 on the dedicated branch. LV-DEC-004 shared-impact handoff and LV-DEC-006 LV002 capture/commit boundary are resolved.
- Current source is the post-LV002 commit. Earlier planning dependency notes are superseded by this refresh; no LV003 implementation or performance result is assumed.

## Interface And Implementation Slices

1. Define a strict JSON scope manifest schema plus explicit check dependency registry. New optional CLI --scope-manifest PATH; --checks remains mandatory for scoped. Without manifest, selected checks can execute but report coverage-result=unverified and cannot qualify as final scoped evidence.
2. Manifest describes canonical repo identity, approved base commit, observed HEAD, staged/unstaged/untracked/deleted/renamed paths with status, intended task scope, and separate canonical runtime roots. Build/verify Git facts with read-only NUL-delimited Git APIs; no shell interpolation or automatic check choice.
3. Compute dependency closure for explicit checks; detect cycles/unknown names and deduplicate by check ID plus normalized project/root/options. Preserve stable order. No unconditional run_fast_checks call.
4. Constrain runtime consumers (naming, QA, status, distillation) to canonical owned roots and actual selected project/artifact boundaries. Separate globally applicable framework checks from runtime scans.
5. Atomically update profiles/routing/checkpoint guidance and their validators. Existing no-arg standard, full CI and updater remain unchanged. Narrow checkpoint eligibility is an explicit new policy with this task, never activated by this plan.

## Post-LV002 Interface Constraints

- Preserve the nine-column timing producer-consumer schema and source-bound run identity. Distinct normalized project/root/options invocations need distinct privacy-safe timing check identities; identical invocations deduplicate. Implement this in the already-approved validate-workflow integration, without expanding the source ceiling into the LV002 helper or comparison tool.
- report-validation-comparison currently admits complete full/smoke-all baselines only. A scoped execution cannot be advertised as a complete full baseline or compared against it as equivalent performance. Scoped performance promotion requires separately comparable input/coverage evidence in the later integration task; LV003 correctness has no numeric speed promise.
- Keep capture sinks bounded, old baseline source/records immutable and failure/timeout/interrupt markers truthful. Any required producer/consumer outside the nineteen approved files stops writes for explicit spec/scope reconciliation.
- Before source writes, create LV003's scoped Distillation State and record the implementation slices/current instruction baseline. The predecessor late-record warning must not recur silently.

## Coverage And Eligibility Rules

Output includes execution-result, coverage-result (complete/incomplete/unverified), requested/required/executed/skipped IDs, reasons and final-evidence eligibility.
Dependencies are declared, not inferred from filenames heuristically. Map each in-scope changed path or runtime artifact kind to known consumers; renames cover old and new names, deletions use the base tree. A deleted required helper is an error, not merely an expensive-check trigger.
Paths outside the approved scope, malformed manifests, escaping symlinks, missing base refs, unknown registry entries and unreadable sources fail closed. Unrecognized impact escalates to full, but full cannot repair missing evidence or make unbounded input complete.
Runtime-only scoped checkpoint requires complete capture/privacy/distillation/status/QA dependency coverage, unchanged canonical framework scope and explicit applicability evidence. No-profile/fast or --checks alone cannot satisfy it.
Shared validators, policy authority, templates, AGENTS, CI, helpers and runner changes remain full-required. Declared no-op cannot hide staged, unstaged or untracked work. Evidence snapshot is invalidated by changes in assessed inputs.
Ignored runtime inputs require a separate explicit inventory and digest; git status alone cannot enumerate them. Exclusions for frozen eval inputs need an identified owner boundary, not a blanket ignored-directory exemption. Inspect path metadata before content; manifests cannot authorize secret reads.
No cache, external lookup, automatic check selection or automatic Git mutation.

## Planned Tests

| ID | Input | Expected state/output |
| --- | --- | --- |
| V3-01 | duplicate checks, shared transitive dependency | one execution per normalized scope |
| V3-02 | same checker for two different projects | two distinct required invocations |
| V3-03 | missing --checks, empty/unknown ID, dependency cycle | actionable nonzero, no success eligibility |
| V3-04 | deleted/renamed shared helper; staged + unstaged changes | complete inventory; full-required or missing-source failure |
| V3-05 | untracked in-scope file, spaces/newlines in path | no silently dropped path |
| V3-06 | no manifest or stale manifest | unverified/incomplete; not final evidence |
| V3-07 | selected project with nested clone/eval fixtures | owned runtime only; foreign inputs excluded |
| V3-08 | missing root, unreadable source, symlink escape | fail closed |
| V3-09 | complete runtime-only checkpoint manifest | scoped checks cover all required consumers, semantic gate still required |
| V3-10 | shared source change or CI/upstream update | full remains mandatory; skip-smoke never full evidence |

## Adaptive Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| explicit checks and strict manifest | dependency graph and owned scope | complete or ineligible execution record | bare checks called complete | fail or full escalation with reason | V3-01..06 | dedup then deleted helper |
| project/runtime roots | bounded canonical sources | pertinent validation only | foreign fixture scanned or real source skipped | stop on unresolved scope | V3-07..10 | selected project and escaping link |

## Specific DoD And Stop Conditions

Update every impacted consumer in the task write set; evidence and status must agree on the same scope. A new unknown consumer blocks coverage claims.
Rollback optimization to existing broad execution if needed, preserving LV001 failure integrity and truthful coverage labels.

## Potential Errors

Green subset represented as full; ignored runtime omitted; duplicate dependency invocations.

## Edge Cases

Rename/deletion, staged and unstaged divergence, newline paths, two different project scopes.

## Assumptions

Explicit registry and manifests replace no current gates until same-scope contract update.

## Blocking Uncertainties

None after the dependency refresh and fresh Spec QA: scope, DoD, safety and existing high-risk source approval are resolved. Execution still requires a current pre-write readiness check; changed dependencies or a discovered out-of-ceiling consumer stop writes.

## Non-Blocking Uncertainties

Actual runtime cost and future compatibility details are measured during implementation; no performance gain is assumed. Discovery outside the proposed write set stops for spec reconciliation.

## User Decisions

LV-DEC-001 resolved the delivery opt-out. LV-DEC-002 approved the high-risk LV001-LV006 source range and branch. LV-DEC-003 governs later synthetic-only LV005 model runs. LV-DEC-004 approves the single AI System handoff. LV-DEC-006 requests LV003 readiness after completed LV002 capture/commit; no LV003 source writes occur in this readiness step.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes; LV001/LV002 current Quality PASS and Phase 6 reviewed.
- Required user decisions resolved: yes within the approved nineteen-path LV003 source scope.
- Can enter implementation: after fresh Spec QA PASS and current task-scoped pre-write readiness; the current request stops at readiness.
- Blocking reason: fresh Spec QA/readiness pending; no new owner decision.
- Gate invalidation: changed predecessor interfaces, approved scope, source or evidence requires spec refresh and fresh Spec QA.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted project context, architecture and LV003 task contract.
- Testable DoD / acceptance conditions: task DoD plus the concrete test/matrix cases in this specification.
- Artifact QA route: phase-3-spec-qa.
- Artifact QA trigger: after complete spec review, before any execution approval/readiness.
- Implementation Quality Closure route: phase-5-quality.
- Required verification: targeted regression tests, manual representative success/failure trace, adversarial policy matrix, producer-consumer audit, fresh full-current-diff review, then explicit full profile for source changes.
- Quality-ready criteria: complete coherent spec; runtime correctness is not claimed until implemented and checked.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: none; existing LV-DEC-002/LV-DEC-004 apply, changed scope requires a new decision.
- Next route: phase-3-spec-qa then LV003 readiness; stop before implementation in this request.

## Delivery Constraints

- Mode: owner-opt-out.
- Deadline: none.
- Time budget: none.
- Timezone: Europe/Warsaw.
- Owner override: LV-DEC-001; explicit no-deadline/no-timebox for this project.
- Must-have outcome: preserve safety and coverage while reducing unnecessary validation cost.
- Should-have scope: measured workflow ergonomics improvements.
- Stretch scope: none.
- Explicitly deferred scope: automatic changed-file inference, cache, production changes.
- Quality floor: semantic QA, DoD, evidence, approvals and complete required coverage.
- Cutline rule: retain monolith if equivalence is inconclusive; defer LV005 promotion if behavioral evidence is inconclusive.
- Overrun checkpoint: no calendar limit; stop on material scope/permission conflict, infrastructure blocker or retry limit.

## Model Recommendation

- Recommended: GPT-5.6 Sol High.
- Reason: contract-preservation, parser and failure-path reasoning; advisory inherited guidance, not an assertion about current model availability.
- Criticality: high for future implementation.
- Current model known: no.
- Blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued.
- Decision state: clear.
- Material decisions: none blocking this planning phase; implementation gates remain explicit.
- Questions asked: none during running.
- Auto-resolved reversible decisions: kebab-case artifact names and sequential artifact writes.
- Optional owner refinements: none.
- Decision artifacts: decisions/lv-decisions.md.
- Next route: next declared planning phase only; stop before implementation.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: decision-artifact.
- Reason: preserve approved scope, safety boundaries and dependency gates.
- Owner decision required: no additional approval for requested planning artifacts.
- Owner decision: capture-now.
- Privacy/scope check: pass.
- Suggested entry title: Lean validation planning decisions.
- Suggested entry summary: current artifact and decisions/lv-decisions.md contain the planning evidence; no ad hoc global memory write.
