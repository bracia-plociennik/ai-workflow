# end-of-task-knowledge-capture

## Summary

- Mode: `repo-level-micro-project`
- Scope: workflow-maintenance contract, docs, template, validator, smoke tests
- Risk: `low`
- Commit: `not-requested`

## Task Idea Validation

Co zostaje:
- Chat-end capture helps preserve useful lessons after iterative work.
- Existing memory, distillation, checkpoint, System Insights, External Memory, and contract compliance boundaries can be reused.

Co jest słabe / do poprawy lub usunięcia:
- The new route must not steal explicit distillation, checkpoint, final review, final check, final-owner-yes, change request, or commit-readiness commands.
- The route must not automatically write memory just because the owner says the task is done.

Czego brakuje:
- Core contract, conflict-free command routing, output template, validator, smoke tests, and owner guidance.

Blokery / decyzje:
- Brak blockerów; owner approved implementation without commit.

Rekomendowany routing:
- Repo-level workflow-maintenance micro-project on `main`.

## Implementation Evidence

- Validation commands:
  - `git diff --check`: PASS
  - `.systems/scripts/check-end-of-task-capture`: PASS
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
  - `.systems/scripts/check-default-idea-validation-opt-out`: PASS
  - `.systems/scripts/check-branch-policy`: PASS
  - `git ls-files ai-workflow-workspace`: PASS, no tracked files listed
- Review: PASS advisory review, no findings/blockers found.
- Review notes:
  - Explicit formal phase commands keep precedence over End-of-Task Capture.
  - `final review` remains global quality review and does not route to final check.
  - `final-owner-yes` and change requests keep higher precedence.
  - Durable capture requires explicit owner intent plus clear target, scope, privacy, evidence, and write permission.
  - Validator and smoke tests cover missing artifacts, missing fields, routing conflicts, unsafe auto-PASS, auto-final-check, auto-close, raw-client System Insights, and External Memory domain-lesson misuse.

## Knowledge Capture

- Capture recommended: `no`
- Target: `none`
- Reason: The workflow source change itself is the durable system update; no separate memory entry is required unless review finds a reusable meta-lesson.
