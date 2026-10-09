# risk-model.md

Bounded-defect handling under `.systems/ai/core/execution-efficiency.md` is a compact record within existing formal-project/workflow-maintenance modes, not risk reclassification. Medium risk still requires accepted plan and QA; high/critical or unknown impact excludes this route.

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
- an accepted concrete plan may cover its named local implementation and formal Phase 5 assessment under execution-modes.md; retain the approval reference and recheck actual coverage instead of repeating permission requests;
- rollback or safety notes when applicable.

Critical:

- decision artifact;
- human approval before plan;
- human approval before implementation;
- human-led execution unless explicitly delegated with controls.
