# <Project> Tasks Router

## Purpose

`tasks.md` is the canonical task index and router for this project.

Detailed task cards live in `docs/ai-workflow/projects/<project>/tasks/`.

Task cards do not replace specifications in `specs/` or QA evidence in `quality/`.

## Task ID Format

`<PROJECT>-<AREA>-<NNN>-<slug>`

Examples:

- `CRM-AUTH-001-reset-password-flow`
- `BILLING-API-004-stripe-webhook-retry`

## Tasks

Task index state: `pending-phase-2-project-plan`

| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Rules

- Keep `tasks.md` as the task index/router.
- An empty task table is valid only before `phase-2-project-plan` is completed.
- After `phase-2-project-plan` is `PASS` or `completed`, add concrete task rows with valid task IDs.
- Store detailed task cards in `tasks/` when extra task-level context is useful.
- Do not store implementation specifications here; use `specs/`.
- Do not store QA evidence here; use `quality/`.
