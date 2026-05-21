# .systems/ai/workflow

This directory contains canonical phase-level workflow rules.

Use:

- `../core/workflow.md` as the phase router.
- `../core/operating-model.md` for the top-level operating model.
- `../core/risk-model.md` for approval and risk routing.
- `../core/definition-of-done.md` for done criteria.

## Canonical Rule

- Phase files in this directory define phase-specific gates.
- Policy rules live in `.systems/ai/core/*.md`.
- Templates live in `.systems/ai/templates/`.
- Runtime facts live in `workspace/repo/`, `workspace/projects/<project>/`, and `workspace/humans/<project>/`.

## Phase Files

- `phase-0-repo-intake.md`
- `phase-0-project-workspace.md`
- `phase-0-idea-validation.md`
- `phase-1-architecture.md`
- `phase-1-architecture-qa.md`
- `phase-1-architecture-fix-loop.md`
- `phase-2-project-plan.md`
- `phase-2-plan-qa.md`
- `phase-2-plan-fix-loop.md`
- `phase-2-task-packaging.md`
- `phase-2-packaging-qa.md`
- `phase-2-package-fix-loop.md`
- `phase-3-specification.md`
- `phase-3-spec-qa.md`
- `phase-3-spec-fix-loop.md`
- `phase-4-implementation.md`
- `phase-5-quality.md`
- `phase-5-fix-loop.md`
- `phase-6-distillation.md`
- `phase-7-checkpoint.md`
- `phase-8-final-check.md`

Phase files are named with the phase number, not execution order. Related QA and fix-loop files keep the phase number of their parent phase.

## Gate Standard

Every phase file must include `## Gate Conditions` with the required headings defined in `.systems/ai/core/workflow.md`.

`.systems/scripts/validate-workflow` enforces that structure.

## Maintenance Rule

Do not add a second workflow router here. Add or update the smallest relevant phase artifact and keep `../core/workflow.md` pointing to it.
