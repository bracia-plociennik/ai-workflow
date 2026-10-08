# Plan Quality Contract V1

## Summary

- Date: `2026-07-16`
- Scope: require every implementation-capable plan, including Codex `/plan`, to declare DoD and a quality route before writes.
- Risk: `medium`
- Work mode: `workflow-maintenance`
- Result: `ready-for-owner-review`

## Acceptance

- Every plan-producing contract and template contains a complete `Plan Quality Contract`.
- Plans distinguish artifact QA from post-implementation quality closure.
- A plan without a testable DoD or a required quality route cannot authorize implementation-class writes.
- Read-only plans use justified `not-applicable`; owner QA opt-out remains explicit and cannot create formal PASS.
- The global Custom Instructions artifact contains a short planning-quality shim without duplicating AI Workflow.

## Definition of Done

- DoD source: `owner-approved micro-project plan and current AI Workflow contracts`
- Done when:
  - core contract, templates, routing, validator, smoke tests, and validation wiring agree;
  - full validation passes with no unresolved findings/blockers in the final advisory review;
  - workspace evidence remains ignored and no global Codex settings are changed.

## Implementation Slice Plan

- Source: `accepted owner prompt/context`
- Implementation scope: `Plan Quality Contract V1 only`
- DoD source: `Definition of Done above`
- Stop rule: stop and route to an owner decision if a route would weaken formal QA, owner opt-out boundaries, source-of-truth order, permissions, or PASS integrity.

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| `S1` | Define canonical contract and routes | core contracts, AGENTS, workflow routing | Every plan type has one explicit quality route | contract review | `completed` |
| `S2` | Add plan/template fields | phase, task, micro-work templates | Required fields appear before implementation readiness | template review | `completed` |
| `S3` | Add static enforcement | validator and validation wiring | Missing routes/DoD and unsafe opt-out wording fail | targeted validator | `completed` |
| `S4` | Add regression coverage | smoke suite | positive and adversarial plan cases run | smoke evidence | `completed` |
| `S5` | Close quality | full validation and advisory review | complete current-diff review has no unresolved blockers | validation and review evidence | `completed` |

## Quality Closure

- Closure type: `advisory`
- Findings/blockers: `none unresolved; P2 concrete artifact values and implementation-capable artifact QA route were added during final review`
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Result wording: `Ready for owner review`
- Residual risk: `Global Custom Instructions require a later owner-applied UI step; static repository validation cannot mechanically inspect future Codex `/plan` output.`

## Slice Execution Evidence

- `S1-S3`: added the core contract, canonical plan fields, routing, validator, validator-chain wiring, and policy-boundary audit coverage.
- `S4`: `.systems/scripts/check-validator-smoke-tests` passed after artifact-level negative and adversarial cases.
- `S5`: `.systems/scripts/validate-workflow --profile full --explain` passed after the final P2 fix.

## Final Review Evidence

- Review mode: `global-quality-review-stance` (read-only/advisory).
- Intent / Plan / Spec Compliance: `aligned` with the owner-approved `plan-quality-contract-v1` scope.
- Producer-consumer field audit: `completed` for formal plan templates, micro-work templates, QA checks, and `check-plan-quality-contract` artifact parsing.
- Policy-boundary adversarial matrix: `completed` through smoke coverage for direct unsafe, safe prohibition, and compound safe-plus-unsafe wording.
- Reviewed baseline: `main worktree after final P2 fix`.
- Closure freshness: `current`.
