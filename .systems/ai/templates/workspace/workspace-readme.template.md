# AI Workflow Workspace

## Purpose

This directory is the target-owned workspace for AI Workflow runtime artifacts.

Default path:

```text
ai-workflow-workspace/
```

The nested `ai-workflow/` clone is system-owned and should stay local to the target repository. This workspace is target-owned and should be committed when it contains repo/project runtime facts.

## Layout

- `repo/` - repository-level init, context, status, intake, memory, and legacy context.
- `projects/` - full project workspaces.
- `humans/` - owner-facing project artifacts.
- `micro-projects/` - small low-risk repo-level work items.
- `external-memory/` - portable AI Workflow improvement suggestions.
- `system-insights/` - anonymized operating lessons and skill candidates.
- `dreams/` - advisory-only Dreaming Mode reports and recommendation queues.
- `repo/capture-state/` - scoped `Distillation State` records for repo-level work; these records never grant write authority.
- `skills/` - user-defined workflow skills that can override system skills.

## Rules

- Do not store system workflow docs here.
- Do not edit `ai-workflow/.systems/**` from a target repository.
- If the workflow itself needs an improvement, record it in `external-memory/`.
- If a project yields an anonymized reusable lesson about delivery quality, product, client work, domain practice, or skills, record it in `system-insights/` only through checkpoint/final-check routing or explicit owner-approved capture.
- Dream Reports in `dreams/` are advisory only; they do not promote memory, System Insights, External Memory, skills, status, or source changes without later owner-approved routing.
- Do not store secrets, credentials, production data dumps, build caches, dependencies, or generated artifacts here.
- `repo/core/init.md` records phase 0 init status.
- `repo/legacy/legacy-index.md` records preserved legacy context from target-owned files.
