# validation-profiles-v1

## Summary

- Date: `2026-07-09`
- Scope: `Optimize workflow validation by introducing lighter scoped validation paths while preserving full validation where needed.`
- Risk: `medium`
- Result: `implemented`

## Source Idea

System validation, especially `validate-workflow`, takes a long time. It should be optimized or split so the workflow does not always require the full heavy validation path when it is unnecessary.

## Batch Triage

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation optimization | validation-performance | validation profiles | medium | repo-level-micro-project | `AI_WORKFLOW_HOME` | validator chain, CI, commit readiness | approve micro-project | Could speed up work, but must not weaken required full validation. |

## Task Idea Validation

### Co zostaje

- Real developer-experience improvement.
- Can reduce time spent waiting for full workflow smoke tests.
- Fits existing command contract if implemented as profiles rather than removing checks.

### Co jest słabe / do poprawy lub usunięcia

- Do not simply remove checks from `validate-workflow`.
- Avoid making CI weaker.
- Avoid ambiguous wording like "run validation if needed" without defining need.

### Czego brakuje

- Validation profile taxonomy, e.g. `fast`, `scoped`, `full`.
- Rules mapping changed files to required validators.
- CI behavior and commit/push readiness behavior.
- Evidence format for skipped full validation.

### Blokery / decyzje

- Owner decision: `full` is not default. No-arg `validate-workflow` uses `standard` for daily iteration and ordinary post-implementation quality.
- Owner decision: `full` is explicit for checkpoint validation, major distillation, major verification, CI, release/final confidence, and high-impact workflow-template changes.
- Owner decision: `fast` and `scoped` remain iteration aids unless owner explicitly accepts narrow validation with residual risk.

## Recommended Routing

- `repo-level-micro-project`
- Plan after implementation slicing and instruction-adherence, unless validation speed becomes the top blocker.

## Acceptance Criteria For Future Plan

- Defines validation profiles and when each is allowed.
- Keeps full validation explicit for checkpoint validation, major distillation, major verification, CI, release/final confidence, and high-impact workflow-template changes.
- CI remains explicit `--profile full`.
- `commands.md`, README, AGENTS, and validators document the new profiles.
- Smoke tests cover profile routing and prevent accidental removal of critical checks.

## Definition of Done

- DoD source: `owner-approved micro-project plan from chat`
- Done when:
  - `.systems/scripts/validate-workflow` supports `full`, `standard`, `scoped`, and `fast` profiles;
  - no-arg `.systems/scripts/validate-workflow` uses `standard`;
  - `standard` is documented as daily iteration and ordinary post-implementation quality validation;
  - `full` is explicit for checkpoint validation, major distillation, major verification, CI, release/final confidence, and high-impact workflow-template changes;
  - `scoped` and `fast` are documented as iteration aids, not default final evidence;
  - `scoped` requires explicit `--checks`;
  - CI remains on no-arg full validation;
  - `check-validation-profiles` and smoke tests prevent profile wording from weakening full validation, CI, commit readiness, PASS Integrity, or quality closure.

## Implementation Slice Plan

- Source: `owner-approved plan`
- Implementation scope: `validation profile contract, validate-workflow profile interface, validator, docs, smoke tests, workspace evidence`
- DoD source: `Definition of Done above`

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| `slice-1-contract` | Add validation profile contract | `.systems/ai/core/validation-profiles.md` | Profiles and safety boundaries are explicit | `check-validation-profiles` | `completed` |
| `slice-2-script` | Add validate-workflow profile interface | `.systems/scripts/validate-workflow` | `full`, `standard`, `scoped`, `fast`, `--checks`, `--explain` work as specified | targeted profile commands | `completed` |
| `slice-3-validator` | Add validator and smoke coverage | `.systems/scripts/check-validation-profiles`, smoke tests, required artifacts | Unsafe weakening fails; no-arg standard and explicit full are protected | smoke tests | `completed` |
| `slice-4-docs` | Update guidance | `AGENTS.md`, `HUMANS.md`, `README.md`, `commands.md`, `contract-compliance.md` | Docs explain profile limits and final validation gate | validator and review | `completed` |
| `slice-5-quality` | Run validation and review | validators and workspace checks | No blockers/findings in advisory review | validation evidence | `completed` |

## Slice Execution Evidence

| Slice ID | Status | Files/Areas Changed | Checks Run Or Skipped | Acceptance Result | Residual Risk | Next Slice Or Stop Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `slice-1-contract` | `completed` | `.systems/ai/core/validation-profiles.md` | `.systems/scripts/check-validation-profiles` | `No blockers found` | low | next slice complete |
| `slice-2-script` | `completed` | `.systems/scripts/validate-workflow`, `.github/workflows/ai-workflow-validate.yml`, `update-from-upstream` | `validate-workflow --profile fast --explain`; `validate-workflow --profile scoped --checks check-validation-profiles --explain`; `validate-workflow --profile standard --explain`; `validate-workflow --profile full --explain` | `No blockers found` | low | next slice complete |
| `slice-3-validator` | `completed` | `.systems/scripts/check-validation-profiles`, `check-validator-smoke-tests`, `check-required-artifacts` | `.systems/scripts/check-validator-smoke-tests` | `No blockers found` | low | next slice complete |
| `slice-4-docs` | `completed` | `AGENTS.md`, `HUMANS.md`, `README.md`, `.systems/ai/core/commands.md`, `.systems/ai/core/contract-compliance.md`, `.systems/ai/core/update-from-upstream.md` | `.systems/scripts/check-validation-profiles`; `validate-workflow --profile standard --explain` | `No blockers found` | low | next slice complete |
| `slice-5-quality` | `completed` | full diff | `git diff --check`; `.systems/scripts/validate-workflow`; `.systems/scripts/validate-workflow --profile full --explain`; workspace tracking checks | `No blockers found` | low | ready for owner review/commit decision |

## Quality Closure

- Closure type: `advisory`
- Findings/blockers: `none found`
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Result wording: `Ready for owner review`
- Residual risk: `low; future tuning may refine which workflow events require explicit full validation`

## Knowledge Capture

- Knowledge capture: `not-required`
- Capture target: `micro-project-artifact`
- Reason: `This file captures the routing and safety constraints for later planning.`
