# implementation-slicing-v1

## Summary

- Date: `2026-07-09`
- Scope: `Require implementation work to start with an implementation slice plan and then execute slices sequentially with evidence.`
- Risk: `medium`
- Result: `implemented`

## Source Idea

Every implementation should be split into smaller slices. Formal `phase-4-implementation` should derive slices from the accepted spec. Micro-tasks or side tasks without a dedicated spec should derive slices from the accepted chat/context implementation plan before writing.

## Batch Triage

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| implementation slicing | implementation-discipline | phase-4 execution model | medium | repo-level-micro-project | `AI_WORKFLOW_HOME` | phase-4, micro-task/side-task contracts, quality evidence | approve micro-project | Changes the default execution model and should be planned separately. |

## Task Idea Validation

### Co zostaje

- Reduces large unstructured implementation passes.
- Makes progress easier to review and recover.
- Fits existing source-of-truth and intent/plan/spec compliance rules.

### Co jest słabe / do poprawy lub usunięcia

- Avoid turning every tiny edit into heavy ceremony.
- Slicing must not authorize scope changes or bypass spec/QA gates.
- Need clear rules for what counts as a slice.

### Czego brakuje

- Slice plan format.
- Minimum evidence per slice.
- Rules for micro-task and side-task slice plans when no formal spec exists.
- Validator/smoke tests for missing slice plan in phase-4 implementation contract.

### Blokery / decyzje

- Decide whether slice plans are mandatory for all writes or only implementation-class writes.
- Decide whether tiny one-file fixes can use a compact inline slice plan.

## Recommended Routing

- `repo-level-micro-project`
- Suggested next prompt: `Zaplanuj micro-project implementation-slicing-v1: phase-4 i micro-task implementations mają zaczynać od implementation slice planu, potem realizować slice’y po kolei z evidence i QA closure.`

## Acceptance Criteria For Future Plan

- Formal `phase-4-implementation` requires an implementation slice plan before writes.
- Micro-task and side-task implementation paths require at least a compact slice plan from accepted context.
- Slice execution records evidence, changed files, skipped checks, and residual risk.
- QA/review can compare completed slices with the slice plan and accepted spec/context.
- Opt-out or fast path cannot bypass risk, permissions, scope, evidence, or QA gates.

## Implementation Slice Plan

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| `slice-1-contract` | Add implementation slicing core contract | `.systems/ai/core/implementation-slicing.md` | Contract defines slice plan, evidence, compact mode, and authority boundary | New contract file reviewed by validator | `completed` |
| `slice-2-phase-template` | Add phase-4 and template integration | `phase-4-implementation.md`, `phase-4-implementation.template.md` | Phase-4 requires slice plan and slice execution evidence | Validator and diff review | `completed` |
| `slice-3-micro-routing` | Add side-task/micro-task/micro-project routing | `operating-model.md`, `command-routing.md`, docs | Micro work requires compact/full slice plan for implementation-class writes | Validator and docs review | `completed` |
| `slice-4-validator` | Add validator and smoke tests | `.systems/scripts/check-implementation-slicing`, smoke tests, validator wiring | Missing plan/evidence and unsafe bypass wording fail | Smoke tests and validate-workflow | `completed` |
| `slice-5-docs-qa` | Update public docs and run QA | `AGENTS.md`, `HUMANS.md`, `README.md`, commands | Docs mention slicing and validation passes | Full validation and review | `completed` |
| `slice-6-dod-quality-pass-integrity` | Add DoD source, mandatory quality closure, and PASS integrity | slicing contract, phase-4, templates, quality review, validators, docs | DoD exists before writes, implementation ends with quality closure, and formal PASS requires findings-first review | Targeted validators, smoke tests, validate-workflow, global review | `completed` |

## Slice Execution Evidence

| Slice ID | Status | Files/Areas Changed | Checks Run Or Skipped | Acceptance Result | Residual Risk | Next Slice Or Stop Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `slice-1-contract` | `completed` | core contract | `.systems/scripts/check-implementation-slicing`: `PASS` | `PASS` | low | next slice complete |
| `slice-2-phase-template` | `completed` | phase-4 docs/template | `.systems/scripts/check-implementation-slicing`: `PASS` | `PASS` | low | next slice complete |
| `slice-3-micro-routing` | `completed` | operating model/routing/docs | `.systems/scripts/check-implementation-slicing`: `PASS` | `PASS` | low | next slice complete |
| `slice-4-validator` | `completed` | validator, smoke tests, wiring | `.systems/scripts/check-validator-smoke-tests`: `PASS`; `.systems/scripts/validate-workflow`: `PASS` | `PASS` | low | full validation pending |
| `slice-5-docs-qa` | `completed` | public docs and validation | `git diff --check`: `PASS`; `.systems/scripts/check-implementation-slicing`: `PASS`; `.systems/scripts/check-validator-smoke-tests`: `PASS`; `.systems/scripts/validate-workflow`: `PASS`; standard validators: `PASS`; `git ls-files ai-workflow-workspace`: `empty` | `PASS` | low | ready for owner review/commit decision |
| `slice-6-dod-quality-pass-integrity` | `completed` | core contracts, templates, validators, docs | `git diff --check`; `.systems/scripts/check-implementation-slicing`; `.systems/scripts/check-default-quality-closure`; `.systems/scripts/check-global-quality-review-stance`; `.systems/scripts/check-intent-plan-spec-compliance-review`; `.systems/scripts/check-validator-smoke-tests`; `.systems/scripts/validate-workflow`; standard validators; workspace tracking checks | `No blockers found` | low | ready for owner review/commit decision |

## Addendum: DoD, Mandatory Quality Closure, PASS Integrity

### Definition of Done

- DoD source: `owner-approved addendum from chat plus existing implementation-slicing-v1 artifact`
- Done when:
  - every implementation-class write path requires DoD source before writes;
  - formal phase-4 stops when DoD is missing or untestable;
  - micro-task and micro-project templates include `Definition of Done`;
  - implementation work ends with formal or advisory quality closure unless owner explicitly opts out;
  - formal `PASS` is allowed only after findings-first review with no unresolved `P0`, `P1`, or material `P2`;
  - advisory micro-work does not claim formal `PASS`.

### Quality Closure

- Closure type: `advisory`
- Findings/blockers: `none found in final read-only global review`
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Result wording: `Ready for owner review`
- Residual risk: `low; future review may still find new findings, but the PASS-before-review false negative is covered by validators and smoke tests`

## Knowledge Capture

- Knowledge capture: `not-required`
- Capture target: `micro-project-artifact`
- Reason: `This file is the durable workspace artifact and implementation evidence; no separate memory entry is needed before final QA.`
