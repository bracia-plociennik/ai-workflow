# Skills

This directory stores system-defined AI Workflow skills.

Skills are reusable task-specific guidance for how to perform a class of work inside the workflow. They can describe domain standards, implementation preferences, UX rules, review checklists, testing expectations, or other execution guidance.

Target repositories must not edit this directory. Local user-defined skills belong in `AI_WORKFLOW_WORKSPACE_HOME/skills/`.

## Active Skill Layout

Use one directory per active skill:

```text
.systems/ai/skills/<skill-name>/
  context/
  skill-intake-plan.md
  SKILL.md
  README.md
  agents/
  references/
  scripts/
  assets/
  eval-viewer/
```

Only `SKILL.md` and `README.md` are required. Optional directories should exist only when they directly support the skill.

`SKILL.md` is the canonical agent contract. It must include frontmatter with `name` and `description`, task guidance, authority boundaries, required checks, output expectations, and stop conditions.

`README.md` is a short human-facing overview. It must point to `SKILL.md` and must not duplicate the full operational contract.

`context/` is raw source input for creating or updating a skill. It is not active guidance. If `context/` exists beside active skill artifacts, `skill-intake-plan.md` must record reviewed sources, trigger/non-trigger cases, keep/fix/missing/blockers, artifact map, approval state, validation plan, and residual risk.

Skill names must use lowercase kebab-case.

## Legacy Source Material

External or superseded skill imports can be preserved under:

```text
.systems/ai/skills/legacy/<source-name>/
```

Legacy entries are context/data only. They are not active system skills, are not loaded by skill routing, and may contain source-system conventions that fail current AI Workflow validation.

## When Agents Must Check Skills

Before planning or implementing a task, the agent must check whether a relevant user skill exists under `AI_WORKFLOW_WORKSPACE_HOME/skills/`, then check this directory for a system skill.

Examples:

- frontend, UI, UX, layout, interaction, responsive design, accessibility -> check for a frontend skill.
- API, endpoint, request validation, serialization -> check for a backend/API skill.
- schema, migration, data model, rollback -> check for a database/migration skill.
- tests, QA, review, release, observability -> check for a matching quality or operations skill.
- skill creation, skill updates, skill evals, or skill safety review -> check `skill-creator`.

If both a user skill and a system skill match, the user skill takes precedence as local task guidance and the system skill remains fallback context.

If a relevant skill exists, read its `SKILL.md` before producing the plan, specification, implementation, or QA result.

If no relevant skill exists, continue with the normal workflow and do not invent one.

## Authority

Skills are supporting execution guidance.

They may:

- add implementation conventions;
- define expected UI/UX or engineering standards;
- require additional checks;
- provide examples and review criteria;
- make a task stricter than the base workflow.

They must not:

- override `AGENTS.md`;
- weaken `.systems/ai/core/operating-model.md`;
- bypass phase gates;
- weaken Definition of Done, risk model, permissions, dependency policy, rollback policy, or evidence requirements;
- redefine project scope, acceptance criteria, owner approvals, or final owner approval.

When a skill conflicts with a higher-priority source, follow the higher-priority source and record the conflict.
