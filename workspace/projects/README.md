# Project Workspaces

This directory stores project-local workflow artifacts.

Repo-level workflow/bootstrap intake belongs in `workspace/repo/core/repo-intake.md`. Do not create a project workspace only to validate that the workflow template is installed correctly.

Each real project should have its own workspace:

```text
workspace/projects/<project>/
```

The project workspace is the canonical location for project-specific intake, architecture, plan, task specifications, QA evidence, decisions, escalations, distillations, checkpoints, autopilot runtime, and project-local status.

## Expected Layout

```text
workspace/projects/<project>/
├── status.md
├── memory.md
├── plans.md
├── tasks.md
├── code-review.md
├── README.md
├── context.md
├── context/
├── memory/
├── tasks/
├── intake/
├── architecture/
├── planning/
├── specs/
├── quality/
├── decisions/
├── escalations/
├── distillations/
├── checkpoints/
├── reviews/
└── autopilot/
    └── runs/
```

Project context belongs in `context.md`. Supporting source materials under `context/` are exempt from naming checks, but `context.md` is canonical and required before architecture and later phases. Project memory is indexed by `memory.md`, with detailed entries under `memory/`. `plans.md` routes to canonical artifacts in `planning/`. `tasks.md` is the task index/router, with optional task cards under `tasks/`. Review artifacts belong in `reviews/`, while QA evidence stays in `quality/`. Project intake may include `intake/phase-0-idea-validation.md` before context is accepted when the owner starts from a rough idea or brain dump.

## Template Example

- `EXAMPLE/` shows the recommended structure and sample artifact shapes.

`EXAMPLE/` is not active project state. Copy it, rename it, or use the templates in `.systems/ai/templates/projects/` when starting a real project.

## Rules

- Do not mix artifacts from multiple projects in one workspace.
- Do not treat historical workspaces as active unless `workspace/repo/core/status.md` points to them.
- Do not create duplicate phase artifacts when a current artifact already exists.
- Keep project decisions in `decisions/`.
- Keep QA and gate evidence in `quality/`.
- Keep review artifacts in `reviews/`.
- Keep autopilot runtime in run directories under `autopilot/runs/`.
