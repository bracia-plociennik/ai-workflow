# upgrade-with-master-prompt Tasks Router

## Purpose

`tasks.md` is the canonical task index and router for this project.

Detailed task cards live in `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/tasks/`.

Task cards do not replace specifications in `specs/` or QA evidence in `quality/`.

## Task ID Format

`<PROJECT>-<AREA>-<NNN>-<slug>`

Examples:

- `UMP-CORE-001-master-prompt-intake`
- `UMP-DOCS-002-upgrade-contract`

## Tasks

Task index state: `completed`

| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `UMP-CORE-001-prompt-composition-contract` | Define prompt composition core contract | `high` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-core-001-prompt-composition-contract-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-core-001-prompt-composition-contract-quality.md` | Quality PASS and phase 6 distillation complete. |
| `UMP-TPL-002-role-variable-templates` | Add role and variable templates | `high` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-tpl-002-role-variable-templates-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-tpl-002-role-variable-templates-quality.md` | Quality PASS and phase 6 distillation complete. |
| `UMP-WF-003-workflow-phase-routing` | Integrate workflow phase routing | `high` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-wf-003-workflow-phase-routing-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-wf-003-workflow-phase-routing-quality.md` | Quality PASS and phase 6 distillation complete. |
| `UMP-PROJ-004-project-local-generation` | Define project-local generation lifecycle | `high` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-proj-004-project-local-generation-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-proj-004-project-local-generation-quality.md` | Quality PASS and phase 6 distillation complete. |
| `UMP-VAL-005-safety-validators` | Add safety validator coverage | `high` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-val-005-safety-validators-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-val-005-safety-validators-quality.md` | Quality PASS and phase 6 distillation complete. |
| `UMP-DOCS-006-human-guidance-examples` | Add human guidance and examples | `medium` | `done` | `none` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/specs/phase-3-ump-docs-006-human-guidance-examples-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-docs-006-human-guidance-examples-quality.md` | Quality PASS and phase 6 distillation complete. |

## Rules

- Keep `tasks.md` as the task index/router.
- An empty task table is valid only before `phase-2-project-plan` is completed.
- After `phase-2-project-plan` is `PASS` or `completed`, add concrete task rows with valid task IDs.
- Store detailed task cards in `tasks/` when extra task-level context is useful.
- Do not store implementation specifications here; use `specs/`.
- Do not store QA evidence here; use `quality/`.
