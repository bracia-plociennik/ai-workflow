# Phase 3 Specification: LV006

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Task/package ID: LV-QA-006-integration.
- Task/package name: Integrated non-regression and measured closure.
- Date: 2026-09-29.
- Readiness: conditional; specification reviewable, implementation not authorized.
- Baseline: f362ce3; source truth must be refreshed after predecessors.

## Sources

- Project plan: planning/phase-2-project-plan.md; Plan QA: quality/phase-2-plan-qa.md.
- Architecture: architecture/phase-1-architecture.md and its Architecture QA.
- Intake: intake/phase-0-repo-intake.md; decisions: decisions/lv-decisions.md; context.md.
- Existing dependency outputs: planning contracts only; implemented results are explicitly gated.

## Task Contract

- Goal: Establish coherent final behavior and honest performance evidence before later capture/closure.
- Scope: Same-input comparisons, cross-contract current-diff review, full CI/updater preservation, consolidated docs/evidence and conditional handoff.
- Out of scope: No hiding deferred tasks, new features, unauthorized commit/push or phase 8.
- Definition of Done: Each included task is quality accepted; all equivalence and behavioral gates resolved; no known P0/P1/material P2; full completes after semantic QA; performance/inconclusive outcomes documented; later phase6/7 and handoff routes explicit.
- Dependencies: LV001, LV002, LV003, LV004, LV005.
- Risk type: high; formal workflow-maintenance.
- Main risk: false confidence, coverage loss or unintended authority change.
- Start condition: LV-DEC-002, current source baseline, accepted Spec QA and predecessor quality evidence.
- End condition: testable task DoD, semantic findings-first Phase 5, applicable explicit full validation and no unresolved material findings; later capture follows phase rules.
- Requires user decision before implementation: yes.

## Proposed Write Set

- .systems/ai/core/commands.md
- AGENTS.md
- HUMANS.md
- README.md
- .systems/ai/core/changelog.md
- Ignored project evidence and one External Memory handoff only after shared-impact yes; any source correction beyond these paths routes back to owning task/spec fix loop.

These paths are the proposed task ceiling, not current write permission. Brace expressions enumerate only named sibling files. New helpers are explicitly marked new. Any additional source consumer discovered at pre-write must be reconciled in this spec and Spec QA before editing.

## Dependency Status

- LV001: implementation evidence unavailable during planning; inspect actual output, refresh this spec and rerun Spec QA before dependent writes.
- LV002: implementation evidence unavailable during planning; inspect actual output, refresh this spec and rerun Spec QA before dependent writes.
- LV003: implementation evidence unavailable during planning; inspect actual output, refresh this spec and rerun Spec QA before dependent writes.
- LV004: implementation evidence unavailable during planning; inspect actual output, refresh this spec and rerun Spec QA before dependent writes.
- LV005: implementation evidence unavailable during planning; inspect actual output, refresh this spec and rerun Spec QA before dependent writes.
- Source approval/base: LV-DEC-002 pending; does not block producing this conditional spec.
- No source or timing/eval outcome is assumed.

## Interface And Implementation Slices

1. Collect each task's current spec/quality, actual implementation source identity, coverage manifests, baseline and all owner dispositions. Reject stale or missing inputs.
2. Perform semantic full-current-diff review before scripts: owner intent/DoD/scope, code/contract drift, data/entrypoint/failure paths, producer-consumer mapping and adversarial policy cases.
3. Repeat equivalent timing paths with LV002 protocol; distinguish real full coverage equivalence from reduced but complete explicit scope. Keep correctness changes even if slower.
4. Verify public CLI behavior, standard no-arg, complete full/CI/updater chain, timeout/progress/completion, legacy compatibility, owned runtime scan and instruction behavioral evidence.
5. Run explicit full validation after semantic review. Record actual outcome; any fix invalidates closure and routes to owning task/spec refresh, fresh review and relevant tests.
6. Prepare consolidated changelog/guidance only within listed paths. After implementation Phase 5, phase 6/7 and conditional External Memory capture use their own phase permissions. Commit, push and Phase 8 remain separately owner-triggered.

## Final Evidence Rules

Manifest links immutable reviewed input digests, current QA outcomes, all test/assertion IDs, timing raw files, fallback/deferred decisions and scope-limited conclusions.
No historical FAIL removal. No closure based on counts, shorter docs, green scripts alone, a partial run or an inherited grade.
All six tasks must meet DoD or have an explicit owner-approved scope disposition propagated through plan/index/Spec QA. LV004 fallback and LV005 deferral are visible outcomes, not automatic task completion.

## Planned Tests

| ID | Check | Acceptance |
| --- | --- | --- |
| V6-01 | CLI/profile/CI/updater integration | full all coverage and markers preserved; standard remains default |
| V6-02 | reference/candidate scenario and scope identities | only equivalent complete comparisons; uncertainty explicit |
| V6-03 | producer-consumer round trip across templates/QA/status | same run and scope interpreted everywhere |
| V6-04 | required policy safe/direct-unsafe/compound cases and absent sources | boundaries enforced, missing sources fail closed |
| V6-05 | current-diff review after last fix | no unresolved P0/P1/material P2; freshness recorded |
| V6-06 | project dispositions and capture/handoff authority | no false completion, no unauthorized write/commit/push |
| V6-07 | git ls-files ai-workflow-workspace and scoped diff | workspace untracked; unrelated local commits preserved |

## Adaptive Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| task results and current source | coherent accepted scope | implementation QA eligibility | stale or partial task called done | route to owning fix loop | V6-01..05 | complete scope and stale-evidence case |
| owner disposition and final evidence | authorized next phase only | capture/handoff readiness | automatic commit/push/Phase8 | stop at gate | V6-06..07 | scoped handoff with pending shared impact |

## Specific DoD And Stop Conditions

Source corrections outside this task's consolidation write set require the owning task fix loop, not opportunistic broad cleanup.
Shared impact pending blocks commit/handoff; yes requires one privacy-safe External Memory concept and path map. This planning-range does not resolve that owner choice.

## Potential Errors

Incomplete task dispositions hidden; final QA stale after fixes; incomparable performance claim.

## Edge Cases

Fallback monolith, deferred guidance, new source changes after assessment, pending handoff choice.

## Assumptions

Integration only follows accepted predecessor evidence or an explicit owner scope change.

## Blocking Uncertainties

None for this conditional specification: design and stop rules are explicit. Execution remains blocked by LV-DEC-002 and the Dependency Status section; predecessor source changes require fresh Spec QA.

## Non-Blocking Uncertainties

Actual runtime cost and future compatibility details are measured during implementation; no performance gain is assumed. Discovery outside the proposed write set stops for spec reconciliation.

## User Decisions

LV-DEC-001 resolved the delivery opt-out. LV-DEC-002 requires source execution/base approval. LV-DEC-003 governs LV005 model runs. LV-DEC-004 governs later commit/handoff. Planning approval resolves none of these future gates.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes, explicitly gated above.
- Required user decisions resolved: no for execution; yes for artifact-only planning scope.
- Can enter implementation: no.
- Blocking reason: high-risk source authorization/base and applicable dependency/eval evidence.
- Gate invalidation: changed predecessor interfaces, approved scope, source or evidence requires spec refresh and fresh Spec QA.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted project context, architecture and LV006 task contract.
- Testable DoD / acceptance conditions: task DoD plus the concrete test/matrix cases in this specification.
- Artifact QA route: phase-3-spec-qa.
- Artifact QA trigger: after complete spec review, before any execution approval/readiness.
- Implementation Quality Closure route: phase-5-quality.
- Required verification: targeted regression tests, manual representative success/failure trace, adversarial policy matrix, producer-consumer audit, fresh full-current-diff review, then explicit full profile for source changes.
- Quality-ready criteria: complete coherent spec; runtime correctness is not claimed until implemented and checked.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: LV-DEC-002 for source execution; LV-DEC-004 before commit/handoff.
- Next route: phase-3-spec-qa, then stop at planning-range boundary.

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
