# risk-model.md

## Risk Classes

| Risk | Examples | Mode |
| --- | --- | --- |
| Low | docs, tests, local refactor without behavior change | autopilot allowed after normal gates |
| Medium | local feature, small endpoint, UI change | plan plus QA |
| High | auth, billing, permissions, migrations, security, external integrations | human approval before implementation |
| Critical | production data, secrets, infrastructure, destructive scripts, real external side effects | human-led only; approval before plan and implementation |

## Classification Rules

- Choose the highest applicable risk class.
- Complexity alone does not make a task critical.
- Critical risk requires material irreversibility, production impact, security exposure, legal/financial impact, or real external side effect.
- Medium-risk, high-risk, and critical-risk tasks are not eligible for micro-task or micro-project handling.

## Required Actions

Low:

- normal gates and evidence.

Medium:

- accepted plan;
- QA evidence;
- status update.

High:

- decision artifact;
- human approval before implementation;
- rollback or safety notes when applicable.

Critical:

- decision artifact;
- human approval before plan;
- human approval before implementation;
- human-led execution unless explicitly delegated with controls.
