# Workflow Templates

Reusable templates for artifacts produced by `docs/ai-workflow/ai/workflow/` phases.

Use these templates as starting points only. The phase rules in `docs/ai-workflow/ai/workflow/` remain authoritative.

## Template Map

| Phase | Template | Typical Destination |
| --- | --- | --- |
| 0 repo intake | `phase-0-repo-intake.template.md` | `docs/ai-workflow/repo/repo-intake.md` or `docs/ai-workflow/projects/<project>/intake/phase-0-repo-intake.md` |
| 0 project workspace | `phase-0-project-workspace.template.md` | `docs/ai-workflow/projects/<project>/` and `docs/ai-workflow/humans/<project>/` |
| 0 idea validation | `phase-0-idea-validation.template.md` | `docs/ai-workflow/projects/<project>/intake/phase-0-idea-validation.md` |
| 1 architecture | `phase-1-architecture.template.md` | `docs/ai-workflow/projects/<project>/architecture/phase-1-architecture.md` |
| 1 architecture QA | `phase-1-architecture-qa.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-1-architecture-qa.md` |
| 1 architecture fix loop | `phase-1-architecture-fix-loop.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-1-architecture-fix-loop.md` |
| 2 project plan | `phase-2-project-plan.template.md` | `docs/ai-workflow/projects/<project>/planning/phase-2-project-plan.md` |
| 2 plan QA | `phase-2-plan-qa.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-2-plan-qa.md` |
| 2 plan fix loop | `phase-2-plan-fix-loop.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-2-plan-fix-loop.md` |
| 2 task packaging | `phase-2-task-packaging.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-2-task-packaging.md` |
| 2 packaging QA | `phase-2-packaging-qa.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-2-packaging-qa.md` |
| 2 package fix loop | `phase-2-package-fix-loop.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-2-package-fix-loop.md` |
| 3 specification | `phase-3-specification.template.md` | `docs/ai-workflow/projects/<project>/specs/phase-3-<task-id>-specification.md` |
| 3 spec QA | `phase-3-spec-qa.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-3-<task-id>-spec-qa.md` |
| 3 spec fix loop | `phase-3-spec-fix-loop.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-3-<task-id>-spec-fix-loop.md` |
| 4 implementation | `phase-4-implementation.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-4-<task-id>-implementation-result.md` |
| 5 quality | `phase-5-quality.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-5-<task-id>-quality.md` |
| 5 fix loop | `phase-5-fix-loop.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-5-<task-id>-fix-loop.md` |
| 6 distillation | `phase-6-distillation.template.md` | `docs/ai-workflow/projects/<project>/distillations/phase-6-<task-id>-distillation.md` |
| 7 checkpoint | `phase-7-checkpoint.template.md` | `docs/ai-workflow/projects/<project>/checkpoints/phase-7-checkpoint-<date>-<scope>.md` |
| 8 final check | `phase-8-final-check.template.md` | `docs/ai-workflow/projects/<project>/quality/phase-8-final-check.md` |

Autopilot runtime templates live in `../autopilot/`.
