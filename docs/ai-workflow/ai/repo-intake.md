# repo-intake.md

## Purpose

This file is template-owned guidance for repo-level intake.

Runtime repo intake for a target repository belongs in:

```text
docs/ai-workflow/repo/repo-intake.md
```

The copyable templates for repo runtime artifacts live at:

```text
docs/ai-workflow/ai/templates/repo/
```

Installation and collision handling is defined in:

```text
docs/ai-workflow/ai/installation.md
```

Do not fill this `docs/ai-workflow/ai/repo-intake.md` with target-repository facts. Keeping `docs/ai-workflow/ai` generic makes the workflow template updateable from upstream without conflicts.

If `docs/ai-workflow/repo/context.md`, `docs/ai-workflow/repo/repo-intake.md`, `docs/ai-workflow/repo/status.md`, or `docs/ai-workflow/repo/memory.md` still describe the upstream `ai-workflow` repository after this workflow is copied into another repository, repo intake must treat them as `STALE_RUNTIME_COPY`.

In that case, phase 0 must replace the runtime files with facts about the current repository before architecture, planning, specification, implementation, or autopilot can continue. Use `docs/ai-workflow/ai/templates/repo/` as the neutral source templates.

## Repo-Level Intake Contract

Repo-level intake answers:

```text
Is this repository ready to use AGENTS.md, HUMANS.md, workflow docs, project docs, and autopilot safely?
```

It must record, in `docs/ai-workflow/repo/repo-intake.md`:

- metadata and gate result;
- installation collision status;
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
| `docs/ai-workflow/repo/context.md` | whole repository | global repo description before project work |
| `docs/ai-workflow/repo/repo-intake.md` | whole repository | workflow/bootstrap readiness after installing `ai-workflow` |
| `docs/ai-workflow/projects/<project>/intake/phase-0-idea-validation.md` | one project idea | brain dump validation before context creation |
| `docs/ai-workflow/projects/<project>/intake/context.md` | one project | accepted project context |
| `docs/ai-workflow/projects/<project>/intake/phase-0-repo-intake.md` | one project | project/context-specific audit before architecture |

## Gate Rule

Repo-level intake can pass only when:

- `docs/ai-workflow/repo/context.md`, `docs/ai-workflow/repo/repo-intake.md`, `docs/ai-workflow/repo/status.md`, and `docs/ai-workflow/repo/memory.md` exist;
- those files describe the current repository, not stale upstream `ai-workflow` runtime state;
- AI Workflow entrypoints and `docs/ai-workflow/ai/` remain free of target-repo facts;
- target-owned `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, `docs/`, `scripts/`, and `.github/` were not overwritten;
- repo command policy is discovered or explicitly marked missing;
- safe environment policy and STOP conditions are explicit;
- no unresolved blocker prevents project workspace creation or workflow use.

If the gate is not satisfied, update `docs/ai-workflow/repo/status.md` with the blocker and stop.
