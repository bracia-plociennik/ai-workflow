# default-idea-validation-opt-out

## Summary

- Mode: `repo-level-micro-project`
- Scope: workflow-maintenance contract, validators, smoke tests, docs
- Risk: `low`
- Write policy: tracked workflow source only; workspace artifact stays local-only
- Commit: `not-requested`

## Task Idea Validation

Co zostaje:
- Default validation improves routing quality before planning or execution.
- Explicit opt-out preserves owner speed control.
- Batch input already has request-batch-triage, so the change can reuse that contract.

Co jest słabe / do poprawy lub usunięcia:
- Validation must not become a hidden hard blocker for simple factual/status answers.
- Opt-out must not be interpreted as permission to bypass risk, evidence, QA, approvals, or phase gates.

Czego brakuje:
- Validator coverage for default single work, project ideas, batch validation route, opt-out grammar, reporting phrase, and unsafe bypass wording.
- Documentation in owner-facing and agent-facing routing.

Blokery / decyzje:
- Brak blockerów; owner approved implementation without commit.

Rekomendowany routing:
- Repo-level workflow-maintenance micro-project on `main`, no commit until owner approval after review.

## Implementation Evidence

- Files reviewed: tracked workflow contracts, docs, validators, smoke tests.
- Validation commands:
  - `git diff --check`: PASS
  - `.systems/scripts/check-default-idea-validation-opt-out`: PASS
  - `.systems/scripts/check-validator-smoke-tests`: PASS
  - `.systems/scripts/validate-workflow`: PASS
  - `.systems/scripts/check-naming`: PASS
  - `.systems/scripts/check-required-artifacts`: PASS
  - `.systems/scripts/check-status-consistency`: PASS
  - `.systems/scripts/check-qa-evidence`: PASS
  - `.systems/scripts/check-system-insights`: PASS
  - `.systems/scripts/check-system-skills`: PASS
  - `.systems/scripts/check-contract-compliance`: PASS
  - `.systems/scripts/check-knowledge-capture-gate`: PASS
  - `.systems/scripts/check-default-quality-phase-chaining`: PASS
  - `.systems/scripts/check-dreaming-mode`: PASS
  - `.systems/scripts/check-global-quality-review-stance`: PASS
  - `.systems/scripts/check-request-batch-triage`: PASS
  - `.systems/scripts/check-response-evidence-trace`: PASS
  - `.systems/scripts/check-phase-skill-discovery`: PASS
  - `.systems/scripts/check-default-quality-closure`: PASS
  - `.systems/scripts/check-branch-policy`: PASS
  - `git ls-files ai-workflow-workspace`: PASS, no tracked files listed
- Quality review: PASS advisory review, no findings/blockers found.
- Review notes:
  - Default single-work, broad-project, and batch/list routes are explicitly covered.
  - Owner opt-out skips only the idea/task validation lens.
  - Batch triage remains required for lists and mixed batches even when validation is opted out.
  - Execution Trace must report skipped validation and residual risk.
  - New validator and smoke tests cover missing defaults, missing batch validation route, missing opt-out grammar, missing reporting phrase, and unsafe bypass wording.
  - `ai-workflow-workspace/micro-projects/default-idea-validation-opt-out/micro-project.md` is ignored by `.gitignore` and not tracked.

## Knowledge Capture

- Capture recommended: `no`
- Target: `none`
- Reason: This micro-project itself is the durable workflow-policy change; no separate memory entry is required unless review finds a reusable operating lesson.
