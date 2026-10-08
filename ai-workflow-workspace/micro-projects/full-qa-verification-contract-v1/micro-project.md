# Full QA Verification Contract V1

## Summary

- Date: `2026-07-13`
- Scope: Full, artifact-appropriate QA across formal phase QA and global review.
- Risk: `medium`
- Work mode: `repo-level-micro-project`
- Result: `completed`

## Acceptance

- Every formal QA records intent, DoD/phase criteria, scope, artifact/diff review, findings/blockers, evidence, skipped sources, residual risk, and fresh closure.
- Implementation/data/integration QA uses an adaptive matrix when the change affects executable data or state flows.
- Only phase 5 can mark formal implementation `PASS` or `FAIL`.

## Definition of Done

- DoD source: `owner prompt/context and full-qa-verification.md`
- Done when:
  - Contract, phases, templates, validator, and smoke tests encode the same QA boundary.
  - Full validation and a current-diff advisory review provide evidence.

## Implementation Slice Plan

- Source: `accepted owner prompt/context`
- Implementation scope: QA contract, phase/template integration, validator, smoke tests, and guidance.
- DoD source: `owner prompt/context and full-qa-verification.md`

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Define common QA contract | core policy and guidance | Contract defines artifact and implementation boundaries | validator references | `completed` |
| 2 | Add phase and template evidence | formal QA and global review templates | All required gates are recordable | template review | `completed` |
| 3 | Enforce contract | validator and smoke suite | Negative and positive cases are covered | full validation | `completed` |

## Evidence

- Reviewed anonymized lessons:
  - Profile selection must be traced through every executable entrypoint, not only isolated helpers.
  - Cross-day data/state changes need canonical-state, derived-output, forbidden-state, and failure-path coverage.
- Commands: `git diff --check`, `check-full-qa-verification`, `check-qa-evidence`, `check-validator-smoke-tests`, `validate-workflow --profile full --explain` all passed.
- Manual checks: reviewed phase-to-template-to-validator mapping, required matrix rows, V1 marker enforcement, and legacy fingerprint handling.

## Quality Closure

- Closure type: `advisory`
- Findings/blockers: `fixed: matrix header could satisfy complete-row regex; generic legacy marker could bypass V1; artifact PASS values could contradict completeness gate`
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Cross-contract consistency: `aligned`
- Risk/work mode compatibility: `aligned`
- Negative-space / adversarial review: `completed`
- Automated evidence role: `supporting-only`
- Post-fix full re-review: `completed`
- Reviewed baseline: `b679218 plus current full-qa-verification-contract-v1 diff`
- Instruction refresh: `performed-full`
- Instruction baseline: `current`
- Closure freshness: `current`
- Result wording: `No blockers found`
- Residual risk: `The contract cannot prove that future project-specific tests cover every undiscovered runtime condition.`

## Knowledge Capture

- Knowledge capture: `not-required`
- Capture target: `micro-project-artifact`
- Reason: `This artifact records implementation evidence; durable lessons require a later capture route.`
