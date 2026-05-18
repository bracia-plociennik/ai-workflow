# Workflow Overview

## Purpose

This file is a short orientation page for the phase specs in this directory. It is not a second full workflow source.

Use `docs/ai-workflow/ai/workflow.md` as the canonical phase router.

## Canonical Rule

- Phase files in this directory define phase-specific gates.
- Policy rules live in `docs/ai-workflow/ai/*.md`.
- Templates live in `docs/ai-workflow/ai/templates/`.
- Runtime facts live in `docs/ai-workflow/repo/` and `docs/ai-workflow/projects/<project>/`.

## Phase Files

Phase files are named with the phase number, not execution order:

- `phase-0-idea-validation.md`
- `phase-0-repo-intake.md`
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

## Gate Standard

Every phase file must include `## Gate Conditions` with the required headings defined in `docs/ai-workflow/ai/workflow.md`.

`scripts/ai-workflow/validate-workflow` enforces that structure.
