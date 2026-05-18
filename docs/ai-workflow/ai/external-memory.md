# EXTERNAL-memory.md

## Purpose

`docs/ai-workflow/ai/external-memory.md` is portable memory for improving the AI workflow system itself.

Use it for universal recommendations, lessons, rules, refinements and process observations that should influence future versions of `ai-workflow` across repositories.

This file is intentionally not repo-specific.

It does not replace:

- `AGENTS.md` as the execution contract in a concrete repository;
- `HUMANS.md` as the human operating guide;
- `docs/ai-workflow/ai/workflow.md` and `docs/ai-workflow/ai/workflow/` as workflow rules;
- `docs/ai-workflow/ai/memory.md` as template-local aggregate memory;
- `docs/ai-workflow/repo/memory.md` as repo-specific aggregate memory;
- `docs/ai-workflow/projects/<project>/project-memory.md` as project-specific aggregate memory;
- repository state as the source of truth for implementation.

## Relationship To Other Memory Files

| Artifact | Scope | Belongs Here | Does Not Belong Here |
| --- | --- | --- | --- |
| `docs/ai-workflow/ai/external-memory.md` | universal workflow/process memory | cross-repo workflow improvements, reusable autopilot rules, process anti-patterns, template improvements | repo facts, domain facts, task-specific implementation knowledge |
| `docs/ai-workflow/ai/memory.md` | this workflow template | template-local maintenance facts and history | target-repo facts or universal workflow lessons |
| `docs/ai-workflow/repo/memory.md` | one repository | durable facts about this repo, local constraints, local history | generic workflow improvements meant for other repos |
| `docs/ai-workflow/projects/<project>/project-memory.md` | one project/workspace | durable project decisions, project architecture facts, project-specific lessons | generic workflow system design |
| `docs/ai-workflow/projects/<project>/distillations/` | one completed task/package | task-level implementation lessons after PASS | broad rules unless promoted by checkpoint |

## Source-Of-Truth Rule

This file is advisory memory.

It can inspire updates to:

- `AGENTS.md`;
- `HUMANS.md`;
- `docs/ai-workflow/ai/workflow.md`;
- `docs/ai-workflow/ai/workflow/`;
- `docs/ai-workflow/ai/autopilot.md`;
- templates under `docs/ai-workflow/ai/templates/`;
- future standalone `ai-workflow` template repositories.

It does not directly override active workflow rules. A recommendation becomes enforceable only after it is intentionally written into the relevant contract or workflow document.

## What Belongs Here

Add entries when a lesson is:

- reusable across multiple repositories;
- about workflow mechanics, not a product domain;
- about Codex/operator collaboration;
- about autopilot behavior, gates, evidence, recovery, retry, checkpoints or STOP conditions;
- about docs layout or template structure;
- about how to reduce hallucination, drift, duplicate artifacts or unsafe execution;
- about better handoff between owner, operator, engineer and agent.

Examples:

- "A repo-level intake artifact is needed before any project workspace exists."
- "Autopilot should distinguish repo-ready, project-ready and task-ready states."
- "Evidence-backed PASS must link to concrete commands or artifact checks."
- "Project specs that were created before dependencies completed must be refreshed before implementation."

## What Does Not Belong Here

Do not add:

- customer or client data;
- secrets, credentials, tokens or private keys;
- repo-specific commands unless they are examples clearly marked as examples;
- product/domain facts from a concrete repository;
- task implementation details;
- temporary chat context;
- raw logs or long command outputs;
- unreviewed guesses.

## Entry Format

Use this format for every entry:

```markdown
## YYYY-MM-DD - Short Title

- Type: recommendation | rule | anti-pattern | template-change | open-question
- Scope: universal | workflow | autopilot | docs-layout | quality | recovery | git | human-ops
- Status: proposed | accepted | implemented | superseded
- Source: where the lesson came from
- Recommendation: what should change or be remembered
- Impact: why it matters
- Applies to:
  - AGENTS.md
  - HUMANS.md
  - docs/ai-workflow/ai/workflow.md
  - docs/ai-workflow/ai/workflow/
  - docs/ai-workflow/ai/templates/
- Promotion path: where this should be made enforceable, if accepted
- Notes: short supporting context
```

Keep entries concise. Link to repo/project artifacts when useful, but do not copy large artifacts into this file.

## Promotion Rules

An entry may be promoted from memory into workflow rules when:

- it is clearly universal, not repo-specific;
- it has a concrete recommendation and impact;
- it does not conflict with core safety rules;
- the owner accepts it or the workflow maintainer intentionally applies it;
- the target contract file is updated directly.

Promotion examples:

- universal process rule -> `docs/ai-workflow/ai/workflow/overview.md`;
- agent execution rule -> `AGENTS.md`;
- human operating guidance -> `HUMANS.md`;
- template change -> `docs/ai-workflow/ai/templates/`;
- autopilot rule -> `docs/ai-workflow/ai/autopilot.md`;
- repo bootstrap requirement -> `docs/ai-workflow/repo/repo-intake.md`.

## Review Cadence

Review this file:

- before extracting `ai-workflow` into a standalone template repository;
- after major workflow/autopilot experiments;
- after an autopilot STOP caused by process weakness;
- after repeated QA/fix-loop patterns;
- before changing universal workflow contracts.

## Current Entries

## 2026-05-17 - Repo-Level Intake Before Project Workspace

- Type: rule
- Scope: docs-layout
- Status: implemented
- Source: workflow template refinement.
- Recommendation: keep `docs/ai-workflow/repo/repo-intake.md` as a repo-level bootstrap/readiness artifact that can exist before any project workspace.
- Impact: a new repository can validate `AGENTS.md`, `HUMANS.md`, `docs/ai-workflow/ai`, templates, status, safe command policy and STOP conditions before a concrete project exists.
- Applies to:
  - `docs/ai-workflow/repo/repo-intake.md`
  - `docs/ai-workflow/ai/workflow.md`
  - `docs/ai-workflow/ai/workflow/phase-0-repo-intake.md`
  - `HUMANS.md`
  - `AGENTS.md`
- Promotion path: already promoted into this workflow template.
- Notes: project-specific `phase-0-repo-intake.md` remains the correct artifact once a project/context exists.

## 2026-05-17 - Universal Workflow Memory Separate From Repo Memory

- Type: rule
- Scope: workflow
- Status: implemented
- Source: need to develop `ai-workflow` generally without polluting repo-specific memory.
- Recommendation: keep `docs/ai-workflow/ai/external-memory.md` for universal recommendations, rules and observations about the workflow system itself.
- Impact: reusable workflow improvements can be collected and later promoted into the standalone `ai-workflow` template without mixing them with one repository's product/domain history.
- Applies to:
  - `docs/ai-workflow/ai/external-memory.md`
  - `docs/ai-workflow/ai/README.md`
  - `docs/ai-workflow/repo/repo-intake.md`
  - `docs/ai-workflow/ai/autopilot.md`
- Promotion path: promote accepted entries into `AGENTS.md`, `HUMANS.md`, workflow docs, autopilot docs or templates.
- Notes: entries in external memory are advisory until promoted into an enforceable workflow contract.
