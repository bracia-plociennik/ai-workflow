# Project Workspaces

This directory stores project-local workflow artifacts.

Repo-level workflow/bootstrap intake belongs in `docs/repo/repo-intake.md`. Do not create a project workspace only to validate that the workflow template is installed correctly.

Each real project should have its own workspace:

```text
docs/projects/<project>/
```

The project workspace is the canonical location for project-specific intake, architecture, plan, task specifications, QA evidence, decisions, escalations, distillations, checkpoints, autopilot runtime, and project-local status.

## Expected Layout

```text
docs/projects/<project>/
├── status.md
├── project-memory.md
├── plans.md
├── code-review.md
├── README.md
├── intake/
├── architecture/
├── planning/
├── specs/
├── quality/
├── decisions/
├── escalations/
├── distillations/
├── checkpoints/
└── autopilot/
```

Project intake may include `intake/phase-0-idea-validation.md` before `intake/context.md` when the owner starts from a rough idea or brain dump.

## Template Example

- `EXAMPLE/` shows the recommended structure and sample artifact shapes.

`EXAMPLE/` is not active project state. Copy it, rename it, or use the templates in `docs/ai/templates/projects/` when starting a real project.

## Rules

- Do not mix artifacts from multiple projects in one workspace.
- Do not treat historical workspaces as active unless `docs/repo/status.md` points to them.
- Do not create duplicate phase artifacts when a current artifact already exists.
- Keep project decisions in `decisions/`.
- Keep QA and gate evidence in `quality/`.
- Keep autopilot runtime in `autopilot/`.
