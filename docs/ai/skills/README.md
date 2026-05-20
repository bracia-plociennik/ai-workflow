# Skills

This directory is reserved for AI Workflow skills.

Skills are reusable task-specific guidance for how to perform a class of work inside the workflow. They can describe domain standards, implementation preferences, UX rules, review checklists, testing expectations, or other execution guidance.

No concrete skills are included by default.

## Intended Layout

Use one directory per skill:

```text
docs/ai/skills/<skill-name>/README.md
```

Example future skill paths:

```text
docs/ai/skills/frontend-dev/README.md
docs/ai/skills/backend-api/README.md
docs/ai/skills/database-migrations/README.md
```

Skill names must use lowercase kebab-case.

## When Agents Must Check Skills

Before planning or implementing a task, the agent must check whether a relevant skill exists under this directory.

Examples:

- frontend, UI, UX, layout, interaction, responsive design, accessibility -> check for a frontend skill.
- API, endpoint, request validation, serialization -> check for a backend/API skill.
- schema, migration, data model, rollback -> check for a database/migration skill.
- tests, QA, review, release, observability -> check for a matching quality or operations skill.

If a relevant skill exists, read it before producing the plan, specification, implementation, or QA result.

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
- weaken `docs/ai/core/operating-model.md`;
- bypass phase gates;
- weaken Definition of Done, risk model, permissions, dependency policy, rollback policy, or evidence requirements;
- redefine project scope, acceptance criteria, owner approvals, or final owner approval.

When a skill conflicts with a higher-priority source, follow the higher-priority source and record the conflict.

## Skill README Minimum Content

Each future skill README should define:

- purpose;
- when to use it;
- when not to use it;
- required checks;
- output expectations;
- stop conditions;
- examples of acceptable and unacceptable work.
