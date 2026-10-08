# Phase 2 Project Plan

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Date: 2026-09-29.
- Work mode: workflow-maintenance, formal project; risk high.
- Sources: context.md; architecture/phase-1-architecture.md; quality/phase-1-architecture-qa.md; decisions/lv-decisions.md.
- Plan approval scope: planning artifacts only. Implementation authorization remains separate.

## Task Contracts

### LV-CORE-001-verdict-integrity (LV001)

- Goal: Reject false smoke success and select only a coherent current QA assessment.
- Scope: Smoke outcome API; current-run QA parsing, templates and status consumers; compatibility and recovery diagnostics.
- Out of scope: No historical rewrites, automatic legacy registration, broad smoke partition or timing optimization.
- Definition of Done: Reserved infrastructure exits cannot pass policy tests; expected failures match status and diagnostic; current QA has one matching run/baseline/evidence/gate; ambiguous or stale assessment fails; valid V1 and permitted legacy remain supported.
- Dependencies: none beyond planning QA and source approval.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-core-001-verdict-integrity-specification.md.
- Spec QA: quality/phase-3-lv-core-001-verdict-integrity-spec-qa.md.
- Implementation quality: quality/phase-5-lv-core-001-verdict-integrity-quality.md (future).

### LV-OBS-002-baseline (LV002)

- Goal: Measure complete valid executions before optimizing coverage selection or partition.
- Scope: Monotonic timing, compatibility-safe metadata, local comparison tool and three post-correctness baseline runs.
- Out of scope: No speed claims from counts, benchmarks before LV001 quality, network, telemetry payloads or source optimization.
- Definition of Done: Three complete comparable baseline runs frozen; timing success/failure preserved; wall-clock separate from children/setup; median, range and noise rule documented; raw records remain private and durable.
- Dependencies: LV001.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-obs-002-baseline-specification.md.
- Spec QA: quality/phase-3-lv-obs-002-baseline-spec-qa.md.
- Implementation quality: quality/phase-5-lv-obs-002-baseline-quality.md (future).

### LV-VAL-003-scoped-selection (LV003)

- Goal: Remove duplicate checks without presenting a narrow execution as complete coverage.
- Scope: Explicit scope manifest, dependency closure/deduplication, canonical runtime discovery and profile/routing integration.
- Out of scope: No cache, inferred check selection, all-project scans for a selected runtime project, or lowering CI/updater requirements.
- Definition of Done: Selected checks and mandatory deps run once per normalized scope; no unconditional fast prelude; requested success distinct from coverage completeness; unknown/unreadable/deleted/shared cases handled safely; current public profiles preserved.
- Dependencies: LV001, LV002.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-val-003-scoped-selection-specification.md.
- Spec QA: quality/phase-3-lv-val-003-scoped-selection-spec-qa.md.
- Implementation quality: quality/phase-5-lv-val-003-scoped-selection-quality.md (future).

### LV-TEST-004-smoke-partition (LV004)

- Goal: Run relevant groups independently while all remains behaviorally equivalent to the monolith.
- Scope: Explicit test/assertion/setup/cleanup ownership; core/policy/quality/skills/workspace groups; isolation, equivalence and fallback.
- Out of scope: No dropping slow tests, ID-only equivalence or changed full CI coverage.
- Definition of Done: Every old ID and external assertion mapped exactly once; intended cases reject the same mutations; groups repeat/order independently; all propagates failures and cleanup; fallback preserves monolith if equivalence is inconclusive.
- Dependencies: LV002, LV003.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-test-004-smoke-partition-specification.md.
- Spec QA: quality/phase-3-lv-test-004-smoke-partition-spec-qa.md.
- Implementation quality: quality/phase-5-lv-test-004-smoke-partition-quality.md (future).

### LV-UX-005-instruction-efficiency (LV005)

- Goal: Reduce repeated instructions/artifact overhead without losing routing or safety behavior.
- Scope: Synthetic baseline/candidate protocol first, then bounded AGENTS/router/response/micro templates and skill-creator check guidance if non-regression proven.
- Out of scope: No domain skill rewrite, global Codex settings, phase-gate removal, customer fixtures or model runs without separate approval.
- Definition of Done: Frozen scenario rubric and same-configuration paired runs exist before promotion; no forbidden action or safety regression; ambiguous results defer promotion; changed-skill validation targets correct skill; mandatory trace/decisions/capture still discoverable.
- Dependencies: LV003, LV004.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-ux-005-instruction-efficiency-specification.md.
- Spec QA: quality/phase-3-lv-ux-005-instruction-efficiency-spec-qa.md.
- Implementation quality: quality/phase-5-lv-ux-005-instruction-efficiency-quality.md (future).

### LV-QA-006-integration (LV006)

- Goal: Establish coherent final behavior and honest performance evidence before later capture/closure.
- Scope: Same-input comparisons, cross-contract current-diff review, full CI/updater preservation, consolidated docs/evidence and conditional handoff.
- Out of scope: No hiding deferred tasks, new features, unauthorized commit/push or phase 8.
- Definition of Done: Each included task is quality accepted; all equivalence and behavioral gates resolved; no known P0/P1/material P2; full completes after semantic QA; performance/inconclusive outcomes documented; later phase6/7 and handoff routes explicit.
- Dependencies: LV001, LV002, LV003, LV004, LV005.
- Risk type: high; shared workflow contracts, verdicts or behavior.
- Main risk: false confidence or silently reduced safety/coverage.
- Start condition: accepted current spec and Spec QA; LV-DEC-002; dependency quality outputs; LV005 also LV-DEC-003 and frozen behavioral baseline before promotion.
- End condition: task DoD, fresh full-current-diff Phase 5 and applicable full validation; later distillation/checkpoint are separate workflow steps.
- Readiness status: conditional; planning complete is not executable authority.
- Requires user decision before implementation: yes.
- Task card: none; this complete task contract is canonical.
- Specification: specs/phase-3-lv-qa-006-integration-specification.md.
- Spec QA: quality/phase-3-lv-qa-006-integration-spec-qa.md.
- Implementation quality: quality/phase-5-lv-qa-006-integration-quality.md (future).

## Final Execution Order And Dependency Map

LV001 -> LV002 -> LV003 -> LV004 -> LV005 -> LV006. Sequential execution prevents overlapping validator/router writes.
All six specs may be prepared now with explicit dependency gates. Before implementing any later task, inspect predecessor outputs, refresh spec and repeat Spec QA if assumptions changed.
Task Packaging: not requested, solo-by-default. No automatic packaging or parallel implementation.
Each task includes matching docs, schema consumers and tests. LV006 performs final consistency review, not postponed integration of intentionally incompatible contracts.

## Fallback And Scope Decisions

- LV004: unproven equivalence keeps the monolith; measurement work remains useful. Record fallback and do not call the split implemented.
- LV005: missing eval permission or inconclusive/regressive evidence means deferred promotion. It does not count as a completed six-task project; owner must approve scope change or continue evidence work.
- LV006: may summarize partial outcomes but cannot claim project DoD until required tasks or owner-approved dispositions are reconciled in plan/index/spec QA.
- No performance threshold can justify weakening or reverting LV001 correctness.

## Architecture Coverage Map

LV001 owns verdict identity and process outcomes; LV002 owns measurement; LV003 owns scope provenance/dependencies; LV004 owns assertion equivalence; LV005 owns behavior/ergonomics; LV006 owns cross-contract final evidence.
Five adversarial findings map respectively to LV004, LV001, LV003, LV005 and LV002/LV006.

## Planning Acceptance

All tasks must have explicit source paths, stable input/output contracts, tests and edge cases, implementation gates and independent quality closure. Benchmark and eval outcomes are future evidence, not assumptions. No source policy takes effect from this plan.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: context.md and reviewed architecture.
- Testable DoD / acceptance conditions: six task contracts, indexed paths, acyclic dependencies, coverage of five review findings and preserved owner gates.
- Artifact QA route: phase-2-plan-qa.
- Artifact QA trigger: after plan and task index are synchronized.
- Implementation Quality Closure route: phase-5-quality for every task.
- Required verification: full artifact review, task/index/path checks, adversarial dependency/fallback reasoning, planned data/integration matrices and eventual full source validation.
- Quality-ready criteria: no planning blocker; conditional execution gates explicit.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: none for specification planning; implementation needs LV-DEC-002/003 and later handoff LV-DEC-004.
- Next route: phase-2-plan-qa then phase-3-specification for all six tasks.

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
