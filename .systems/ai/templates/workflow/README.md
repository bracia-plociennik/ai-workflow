# Workflow Templates

Reusable templates for artifacts produced by `.systems/ai/workflow/` phases.

Use these templates as starting points only. The phase rules in `.systems/ai/workflow/` remain authoritative.

## Template Map

| Phase | Template | Typical Destination |
| --- | --- | --- |
| 0 repo intake | `phase-0-repo-intake.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md` or `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/intake/phase-0-repo-intake.md` |
| 0 project workspace | `phase-0-project-workspace.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/` and `AI_WORKFLOW_WORKSPACE_HOME/humans/<project>/` |
| 0 idea validation | `phase-0-idea-validation.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/intake/phase-0-idea-validation.md` |
| 1 architecture | `phase-1-architecture.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/architecture/phase-1-architecture.md` |
| 1 architecture QA | `phase-1-architecture-qa.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-1-architecture-qa.md` |
| 1 architecture fix loop | `phase-1-architecture-fix-loop.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-1-architecture-fix-loop.md` |
| 2 project plan | `phase-2-project-plan.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/planning/phase-2-project-plan.md` |
| 2 plan QA | `phase-2-plan-qa.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-2-plan-qa.md` |
| 2 plan fix loop | `phase-2-plan-fix-loop.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-2-plan-fix-loop.md` |
| 2 task packaging | `phase-2-task-packaging.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-2-task-packaging.md` |
| 2 packaging QA | `phase-2-packaging-qa.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-2-packaging-qa.md` |
| 2 package fix loop | `phase-2-package-fix-loop.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-2-package-fix-loop.md` |
| 3 specification | `phase-3-specification.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/specs/phase-3-<task-id>-specification.md` |
| 3 spec QA | `phase-3-spec-qa.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-3-<task-id>-spec-qa.md` |
| 3 spec fix loop | `phase-3-spec-fix-loop.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-3-<task-id>-spec-fix-loop.md` |
| 4 implementation | `phase-4-implementation.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-4-<task-id>-implementation-result.md` |
| 5 quality | `phase-5-quality.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-5-<task-id>-quality.md` |
| 5 fix loop | `phase-5-fix-loop.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-5-<task-id>-fix-loop.md` |
| 6 distillation | `phase-6-distillation.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/distillations/phase-6-<task-id>-distillation.md` |
| 7 checkpoint | `phase-7-checkpoint.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/checkpoints/phase-7-checkpoint-<date>-<scope>.md` |
| 8 final check | `phase-8-final-check.template.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-8-final-check.md` |

Autopilot runtime templates live in `../autopilot/`.
