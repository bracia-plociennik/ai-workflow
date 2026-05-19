# EXAMPLE Tasks Router

## Purpose

`tasks.md` is the canonical task index and router for this project.

Detailed task cards live in `docs/ai-workflow/projects/EXAMPLE/tasks/`.

Task cards do not replace specifications in `specs/` or QA evidence in `quality/`.

## Task ID Format

`<PROJECT>-<AREA>-<NNN>-<slug>`

## Tasks

| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `EX-DOCS-001-example-task` | Example Task | low | example-only | `docs/ai-workflow/projects/EXAMPLE/tasks/ex-docs-001-example-task.md` | `docs/ai-workflow/projects/EXAMPLE/specs/phase-3-ex-01-example-task-specification.md` | `docs/ai-workflow/projects/EXAMPLE/quality/phase-5-ex-01-quality.md` | Demonstrates task tracking only. |

## Rules

- Keep `tasks.md` as the task index/router.
- Store detailed task cards in `tasks/` when extra task-level context is useful.
- Do not store implementation specifications here; use `specs/`.
- Do not store QA evidence here; use `quality/`.
