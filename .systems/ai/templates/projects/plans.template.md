# <Project> Plans Router

## Purpose

`plans.md` is the router/index for canonical project planning artifacts under `planning/`.

It is not a loose planning notes file. Operational project plans belong in `planning/`.

## Planning Index

| Plan | Status | Route | Notes |
| --- | --- | --- | --- |
| `<plan name>` | `<draft|active|passed|superseded|blocked>` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/planning/<plan-file>.md` | `<notes>` |

## Delivery Constraints

Implementation-capable plans use `.systems/ai/core/delivery-constraints.md` and record a deadline/timebox or bounded owner opt-out, must-have outcome, cutline, deferred scope, quality floor, and overrun route.

## Rules

- Keep this file short. It points to planning artifacts.
- Do not store task specifications here; use `specs/`.
- Do not store QA evidence here; use `quality/`.
- Do not store task cards here; use `tasks/`.
