# Workspace Skills

This directory stores target-owned user skills.

## Precedence

When both a workspace skill and a system skill match the same task, use this order:

1. `ai-workflow-workspace/skills/<skill-name>/`
2. `.systems/ai/skills/<skill-name>/`

Workspace skills may make task-specific guidance stricter or more local, but they cannot override `AGENTS.md`, `.systems/ai/core/`, workflow gates, risk model, permissions, Definition of Done, required evidence, approved scope, or final owner approval.

## Naming

Use lowercase kebab-case skill directories:

```text
ai-workflow-workspace/skills/frontend-dev/
ai-workflow-workspace/skills/laravel-testing/
```

Each skill should include a `README.md` or `SKILL.md` explaining when to use it and what guidance it adds.
