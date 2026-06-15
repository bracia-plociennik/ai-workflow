# User Skills

## Purpose

User-defined skills live here.

When a user skill and a system skill both match a task, the user skill has higher priority for local guidance. Skills cannot override `AGENTS.md`, `.systems/ai/core/`, phase gates, risk model, permissions, Definition of Done, approved scope, or required evidence.

Preferred skill path:

```text
AI_WORKFLOW_WORKSPACE_HOME/skills/<skill-name>/
  context/
  skill-intake-plan.md
  SKILL.md
  README.md
```

`SKILL.md` is the canonical agent contract. `README.md` is a short human-facing summary.

Use `context/` for raw source materials while creating or updating a skill. `context/` is not active guidance. If `context/` exists beside active skill artifacts, create `skill-intake-plan.md` before writing the final skill contract and resources.
