# STATUS.md

## Purpose

This is the repository-level workflow status file.

In a new repository, update this file during repo-level intake so it records workflow/bootstrap readiness, then point it to the active project workspace and current workflow phase once a project exists.

## Current Status

| Field | Value |
| --- | --- |
| `workflow_requirement` | `optional` |
| `workflow_scope` | `template_not_initialized` |
| `active_docs_workspace` | `none` |
| `active_plan_status` | `none` |
| `current_task` | `template setup / no active task` |
| `current_phase` | `none` |
| `phase_result` | `not_started` |
| `next_phase` | `repo-level intake in docs/ai/REPO-INTAKE.md` |
| `last_completed_phase` | `none` |
| `blocking_reason` | `repo adaptation layer not filled` |
| `autopilot_mode` | `not_active` |
| `autopilot_state` | `not_created` |
| `updated_at` | `<update during repo intake>` |

## Notes

- This template status is intentionally not tied to any real project.
- First fill `docs/ai/REPO-INTAKE.md` to validate repo-level workflow readiness.
- Keep `docs/ai/EXTERNAL-MEMORY.md` for universal workflow lessons only.
- Before implementation work, create or select `docs/projects/<project>/` and update this file.
- Do not mark any phase as `PASS` without evidence in the relevant project `quality/` directory.
