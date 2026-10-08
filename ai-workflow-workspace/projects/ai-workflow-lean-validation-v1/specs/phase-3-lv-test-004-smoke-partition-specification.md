# Phase 3 Specification: LV004

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Task/package ID: LV-TEST-004-smoke-partition.
- Task/package name: Assertion-preserving independent smoke groups.
- Date: 2026-09-30; refreshed after completed LV001-LV003 checkpoint.
- Readiness: current implementation-range authority LV-DEC-008; fresh Spec QA required before tracked writes.
- Baseline: 03fb788; clean dedicated branch. Frozen reference inventory: implementation/lv004-reference/inventory.json.

## Sources

- Project plan: planning/phase-2-project-plan.md; Plan QA: quality/phase-2-plan-qa.md.
- Architecture: architecture/phase-1-architecture.md and its Architecture QA.
- Intake: intake/phase-0-repo-intake.md; decisions: decisions/lv-decisions.md; context.md.
- Existing dependency outputs: current LV001/LV002 regression and LV003 Quality PASS, their accepted Phase 6 records and checkpoints/phase-7-checkpoint-2026-09-30-lv001-lv003.md.

## Task Contract

- Goal: Run relevant groups independently while all remains behaviorally equivalent to the monolith.
- Scope: Explicit test/assertion/setup/cleanup ownership; core/policy/quality/skills/workspace groups; isolation, equivalence and fallback.
- Out of scope: No dropping slow tests, ID-only equivalence or changed full CI coverage.
- Definition of Done: Every old ID and external assertion mapped exactly once; intended cases reject the same mutations; groups repeat/order independently; all propagates failures and cleanup; fallback preserves monolith if equivalence is inconclusive.
- Dependencies: LV002, LV003.
- Risk type: high; formal workflow-maintenance.
- Main risk: false confidence, coverage loss or unintended authority change.
- Start condition: LV-DEC-002, current source baseline, accepted Spec QA and predecessor quality evidence.
- End condition: testable task DoD, semantic findings-first Phase 5, applicable explicit full validation and no unresolved material findings; later capture follows phase rules.
- Requires user decision before implementation: yes.

## Proposed Write Set

- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/smoke/manifest.json (new)
- .systems/scripts/smoke/common.sh (new)
- .systems/scripts/smoke/{core,policy,quality,skills,workspace}.sh (new)
- .systems/scripts/check-validation-observability
- .systems/scripts/check-validation-completion
- .systems/ai/core/validation-observability.md
- .systems/ai/core/commands.md
- README.md

These paths are the proposed task ceiling, not current write permission. Brace expressions enumerate only named sibling files. New helpers are explicitly marked new. Any additional source consumer discovered at pre-write must be reconciled in this spec and Spec QA before editing.

## Dependency Status

- LV002: current regression assessment and immutable three-run source-specific baseline reviewed. Timing producer/consumer nine-column schema is unchanged.
- LV003: current quality, actual full 637s and fresh checkpoint full 647s reviewed. Explicit check dependency planning, source-impact gate and coverage/eligibility separation remain intact.
- Source approval/base: LV-DEC-008 authorizes this existing ceiling on current 03fb788; no push.
- Frozen reference: 674 actual test IDs, 110 lexical external assertion candidates requiring semantic classification, and 32 source-consumer references. Counts alone do not establish equivalence.

## Current Producer-Consumer Design

- The public runner preserves CLI, lifecycle markers and one suite timing wall. Owned group executions have distinct group markers; child timings in an all run retain smoke-all profile and one smoke-suite-wall parent.
- Each group has a disposable source fixture and its own setup/cleanup. common.sh imports pure shared functions only; setup executes in the owning runner/group, never by importing common.
- Existing validators use literal integration references in the public runner. A declared coverage index may preserve these references only if it is checked against the live manifest and group contents before dispatch. Comments disconnected from executed cases are not evidence and are forbidden as a compatibility workaround.
- Manifest binds every executed reference ID, exact group, test outcome helper contract, external assertion ownership, original region hash, current group/common hashes and setup/cleanup/mutation provenance. All wrapper and post-call assertions remain executable, not merely listed.
- Source-copy prototypes and exploratory group runs are ignored/tmp supporting evidence only. They do not constitute implementation PASS or split promotion. Any unidentified executable assertion, ambiguous ownership or new required consumer outside the ceiling stops promotion.

## Interface And Implementation Slices

1. Freeze the LV002-instrumented monolith source and enumerate all named tests AND assertions outside wrappers. Assign stable assertion IDs, parent test/group, fixture prerequisites, mutation, cleanup and failure propagation contract.
2. Create manifest.json and isolated group files; common.sh contains only pure/shared utilities, not assertions executed accidentally on import. Every standalone shell test/grep/python assertion is mapped or explicitly classified setup/cleanup with a rationale.
3. Preserve public --group all default and exact group enum. Named groups run only owned tests/assertions plus declared setup. Test-specific output is created inside its group's disposable fixture; no reliance on another group's execution.
4. Compare old reference and split under identical safe inputs, including mutation outcomes, unexpected failures, all orderings of dependent groups considered, repeated execution and interrupted cleanup.
5. Publish split only after equivalence audit; otherwise leave functional monolith/all behavior and report split unproven.

## Manifest And Equivalence

Each entry: test ID, assertion IDs, owning group, command/expected outcome contract, setup ID, cleanup ID and mutation ID. Old IDs cannot disappear or multiply. Internal supplemental regression tests may be new but are distinguished from the frozen old inventory.
Setup may be shared conceptually but executes in isolated group state. Manifest proves union and ownership, not behavior by itself.
Explicitly account for existing marker-count checks after wrappers, process-group cleanup, updater canonical-state assertions and preservation of workspace markers. Tests are not reduced to exit code checking.
Full invokes all groups; skip flags or a subset cannot claim full evidence. Exactly one top-level completion marker; child/group markers are namespaced and do not masquerade as top-level completion.
Failure/timeout stops or reports according to the original public failure contract, preserves cleanup, and never turns a skipped group into a successful one.

## Planned Tests

| ID | Input | Expected state/output |
| --- | --- | --- |
| V4-01 | missing/duplicate old test ID or assertion ownership | equivalence rejected |
| V4-02 | all IDs preserved but marker-count assertion removed | equivalence rejected by assertion inventory/mutation |
| V4-03 | each group standalone in clean fixture | same owned assertions and outcomes |
| V4-04 | groups permuted/repeated | no hidden cross-group state or fixture bleed |
| V4-05 | timeout/signal/failing child, including cleanup failure | failure propagated, child cleanup checked |
| V4-06 | source mutation breaking a protected invariant | both reference and candidate reject for same reason |
| V4-07 | all union vs frozen monolith | no lost assertion or silent skip |
| V4-08 | unknown group or incomplete manifest | nonzero, no all/full success |
| V4-09 | equivalence inconclusive | monolith retained; fallback accurately reported |

## Adaptive Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| old monolith and manifest | complete ownership graph | isolated groups and all union | ID-only equivalence | reject promotion | V4-01..04 | marker-count assertion ownership |
| mutated fixture and process failure | same rejection plus cleanup | no false success | timeout swallowed, orphan child | failed run with active ID | V4-05..09 | canonical updater assertion then interruption |

## Specific DoD And Stop Conditions

Do not invent an old test count from historical runs; inventory the actual frozen baseline. Test-level comparison includes the after-call assertions identified during LV001.
If a shared fixture cannot be isolated without changing semantics, keep the monolith; any scope reduction needs owner disposition and plan QA.

## Potential Errors

After-call assertions lost despite preserved test IDs; setup leaks across groups.

## Edge Cases

Repeated/permuted groups, partial runs, timeout cleanup and fresh-fixture execution.

## Assumptions

Frozen monolith is an executable reference; fallback is retained until equivalence is proven.

## Blocking Uncertainties

None for refreshed specification design; current Spec QA remains the pre-write gate. Prototype equivalence, mutation rejection and lifecycle behavior remain actual implementation acceptance evidence, not assumed.

## Non-Blocking Uncertainties

Actual runtime cost and future compatibility details are measured during implementation; no performance gain is assumed. Discovery outside the proposed write set stops for spec reconciliation.

## User Decisions

LV-DEC-001 resolved the delivery opt-out. LV-DEC-002 requires source execution/base approval. LV-DEC-003 governs LV005 model runs. LV-DEC-004 governs later commit/handoff. Planning approval resolves none of these future gates.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes, explicitly gated above.
- Required user decisions resolved: yes, LV-DEC-008 within the existing ceiling.
- Can enter implementation: only after fresh current Spec QA.
- Blocking reason: fresh Spec QA required before tracked source writes.
- Gate invalidation: changed predecessor interfaces, approved scope, source or evidence requires spec refresh and fresh Spec QA.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted project context, architecture and LV004 task contract.
- Testable DoD / acceptance conditions: task DoD plus the concrete test/matrix cases in this specification.
- Artifact QA route: phase-3-spec-qa.
- Artifact QA trigger: after complete spec review, before any execution approval/readiness.
- Implementation Quality Closure route: phase-5-quality.
- Required verification: targeted regression tests, manual representative success/failure trace, adversarial policy matrix, producer-consumer audit, fresh full-current-diff review, then explicit full profile for source changes.
- Quality-ready criteria: complete coherent spec; runtime correctness is not claimed until implemented and checked.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: none within current ceiling; new material scope/consumer requires reconciliation.
- Next route: fresh phase-3-spec-qa, then phase-4-implementation under LV-DEC-008.

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
