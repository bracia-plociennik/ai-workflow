# Micro-projects

This directory stores repo-level low-risk micro-projects.

Micro-projects are small, self-contained work items that do not need a full `docs/ai-workflow/projects/<project>/` workspace, architecture, project plan, spec QA, quality phase, distillation, checkpoint, or autopilot run.

## Rules

- Use micro-projects only for low-risk work.
- Record scope, risk, acceptance, changed files, checks/evidence, result, and follow-up/promote decision.
- Do not use micro-projects for auth, billing, permissions, migrations, secrets, production data, security-sensitive work, external effects, or architectural decisions.
- If risk becomes medium, high, or critical, promote the work to the normal workflow.
- Real target-repository micro-projects are target-owned runtime and are protected by `scripts/ai-workflow/update-from-upstream`.

## Layout

```text
docs/ai-workflow/micro-projects/
  README.md
  EXAMPLE/
    README.md
    micro-project.md
  <micro-project-slug>/
    README.md
    micro-project.md
```
