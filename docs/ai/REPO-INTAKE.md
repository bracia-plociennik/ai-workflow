# REPO-INTAKE.md

## Purpose

This file is template-owned guidance for repo-level intake.

Runtime repo intake for a target repository belongs in:

```text
docs/repo/REPO-INTAKE.md
```

The copyable template for that runtime artifact lives at:

```text
docs/ai/templates/ai/REPO-INTAKE.template.md
```

Do not fill this `docs/ai/REPO-INTAKE.md` with target-repository facts. Keeping `docs/ai` generic makes the workflow template updateable from upstream without conflicts.

## Repo-Level Intake Contract

Repo-level intake answers:

```text
Is this repository ready to use AGENTS.md, HUMANS.md, workflow docs, project docs, and autopilot safely?
```

It must record, in `docs/repo/REPO-INTAKE.md`:

- metadata and gate result;
- sources reviewed;
- command map;
- safe local/test environment;
- high-risk areas and STOP conditions;
- restricted/generated/runtime zones;
- secret, migration, external-effect, retry, checkpoint, and git policy;
- artifact reconciliation;
- owner decisions required;
- evidence for the gate result.

## Relationship To Project Intake

| Artifact | Scope | Use When |
| --- | --- | --- |
| `docs/repo/CONTEXT.md` | whole repository | global repo description before project work |
| `docs/repo/REPO-INTAKE.md` | whole repository | workflow/bootstrap readiness after installing `ai-workflow` |
| `docs/projects/<project>/intake/000_idea_validation.md` | one project idea | brain dump validation before context creation |
| `docs/projects/<project>/intake/0_context.md` | one project | accepted project context |
| `docs/projects/<project>/intake/0_initial_audit.md` | one project | project/context-specific audit before architecture |

## Gate Rule

Repo-level intake can pass only when:

- `docs/repo/CONTEXT.md`, `docs/repo/REPO-INTAKE.md`, `docs/repo/STATUS.md`, and `docs/repo/MEMORY.md` exist;
- `AGENTS.md`, `HUMANS.md`, root workflow docs, and `docs/ai/` remain template-owned and free of target-repo facts;
- repo command policy is discovered or explicitly marked missing;
- safe environment policy and STOP conditions are explicit;
- no unresolved blocker prevents project workspace creation or workflow use.

If the gate is not satisfied, update `docs/repo/STATUS.md` with the blocker and stop.
