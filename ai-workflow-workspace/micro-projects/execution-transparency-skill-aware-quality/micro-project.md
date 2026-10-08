# execution-transparency-skill-aware-quality

## Summary

- Date: `2026-06-22`
- Work mode: `workflow-maintenance`
- Risk: `low`
- Status: `implemented-pending-review`

## Idea Validation

### Co zostaje

- Owner needs evidence that AI Workflow uses declared procedures, sources, skills, and quality checks.
- Existing response contract, global quality review, skill routing, and default phase quality chaining are good foundations.
- Phase-level skills should be domain/task skills, not dedicated phase skills.

### Co jest słabe / do poprawy lub usunięcia

- Existing responses can end with `Co dalej?` without showing enough source/evidence trace.
- Existing skill routing is not explicit enough that every phase/procedure should discover applicable domain/task skills.
- Existing default quality behavior is strongest for formal phases, but weaker for side-task, micro-task, micro-project, and advisory work.

### Czego brakuje

- `Execution Trace` contract and validator.
- Phase Skill Discovery contract and validator.
- Default Quality Closure contract and validator.
- Smoke tests for the new boundaries.

### Blokery / decyzje

- No blocker.
- Owner selected: substantive responses only, domain/task skill discovery, and quality closure for all substantive work with explicit opt-out.

### Rekomendowany routing

- Repo-level workflow-maintenance micro-project in official `ai-workflow`.

## Evidence

- Review finding P3 fixed: `check-response-evidence-trace` now explicitly requires `Execution Trace` in `AGENTS.md`, with smoke coverage for removing that instruction.
- `git diff --check` passed.
- `.systems/scripts/check-response-evidence-trace` passed.
- `.systems/scripts/check-phase-skill-discovery` passed.
- `.systems/scripts/check-default-quality-closure` passed.
- `.systems/scripts/check-validator-smoke-tests` passed.
- `.systems/scripts/validate-workflow` passed.
- `.systems/scripts/check-naming` passed.
- `.systems/scripts/check-required-artifacts` passed.
- `.systems/scripts/check-status-consistency` passed.
- `.systems/scripts/check-qa-evidence` passed.
- `.systems/scripts/check-system-insights` passed.
- `.systems/scripts/check-system-skills` passed.
- `.systems/scripts/check-contract-compliance` passed.
- `.systems/scripts/check-knowledge-capture-gate` passed.
- `.systems/scripts/check-default-quality-phase-chaining` passed.
- `.systems/scripts/check-dreaming-mode` passed.
- `.systems/scripts/check-global-quality-review-stance` passed.
- `.systems/scripts/check-request-batch-triage` passed.
- `.systems/scripts/check-branch-policy` passed.
- `git ls-files ai-workflow-workspace` returned no tracked workspace files.

## Knowledge Capture

- Knowledge capture: `not-required`
- Reason: changelog/version plus this micro-project artifact capture the workflow maintenance decision.
