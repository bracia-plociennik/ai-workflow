# Global Quality Review Stance

## Summary

- Date: `2026-06-19`
- Scope: `read-only/advisory global quality review stance, routing, validator, smoke tests, and docs`
- Risk: `low`
- Result: `implemented-pending-review`

## Idea Validation

### Co zostaje

- `phase-5-quality` remains the formal PASS/FAIL quality gate for implemented tasks/packages.
- A global review stance is useful for side-tasks, micro-tasks, micro-projects, workflow-maintenance, and read-only reviews.
- Review-style commands should produce findings-first output with blockers, evidence reviewed, skipped areas, and residual risk.

### Co jest slabe / do poprawy lub usuniecia

- Generic `review` should not be treated as formal `phase-5-quality`.
- `final review` must not imply `phase-8-final-check`.
- Advisory review must not write artifacts, status, memory, source files, commits, or PRs.

### Czego brakuje

- Core contract for the global review stance.
- Routing for review/findings/blockers/final review.
- Validator and smoke tests.
- Human guidance that distinguishes review stance from formal quality gates.

### Blokery / decyzje

- No implementation blocker for V1.
- V1 does not create a new formal workflow phase.

### Rekomendowany routing

- Workflow-maintenance micro-project in the official AI Workflow repo.

## Evidence

- Commands:
  - `git diff --check` - pass.
  - `.systems/scripts/check-global-quality-review-stance` - pass.
  - `.systems/scripts/check-validator-smoke-tests` - pass.
  - `.systems/scripts/validate-workflow` - pass.
  - `.systems/scripts/check-required-artifacts` - pass.
  - `.systems/scripts/check-naming` - pass.
  - `.systems/scripts/check-status-consistency` - pass.
  - `.systems/scripts/check-qa-evidence` - pass.
  - `.systems/scripts/check-system-insights` - pass.
  - `.systems/scripts/check-system-skills` - pass.
  - `.systems/scripts/check-contract-compliance` - pass.
  - `.systems/scripts/check-knowledge-capture-gate` - pass.
  - `.systems/scripts/check-default-quality-phase-chaining` - pass.
  - `.systems/scripts/check-dreaming-mode` - pass.
  - `.systems/scripts/check-branch-policy` - pass.
  - `git ls-files ai-workflow-workspace` - empty output.
- Manual checks:
  - Tracked changes are intended to remain limited to workflow docs, validators, scripts, and policy files.
  - Review P2 resolved: unsafe wording detection now catches broader advisory review `PASS/FAIL` grants and final review -> `phase-8-final-check` trigger wording.
  - Added smoke coverage for `advisory review may produce PASS` and `final review starts phase-8-final-check`.
  - No commit created before review.

## Contract Compliance

- Work mode compliance: `pass`
- Work mode: `repo-level-micro-project`
- Scope/acceptance clear: `yes`
- Risk allowed for mode: `yes`
- Write-set conflicts: `none`

## Changed Files

- `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/global-quality-review-stance/micro-project.md`
- Tracked implementation scope:
  - `.systems/ai/core/quality-review.md`
  - `.systems/scripts/check-global-quality-review-stance`
  - routing/docs/validator wiring.

## Knowledge Capture

- Knowledge capture: `required`
- Capture target: `micro-project-artifact`
- Reason: New reusable workflow behavior and routing semantics should remain available for review and future maintenance.

## Follow-up / Promote Decision

- Promote to full workflow: `no`
- Reason: Low-risk workflow-maintenance micro-project; no product-code changes.
