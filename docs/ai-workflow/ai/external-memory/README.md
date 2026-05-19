# external-memory

## Purpose

`docs/ai-workflow/ai/external-memory/` is portable advisory memory for improving the AI Workflow system itself.

Use it for universal recommendations, lessons, rules, refinements, anti-patterns, and process observations that should influence future versions of `ai-workflow` across repositories.

The router/index is `docs/ai-workflow/ai/external-memory.md`.

This directory is intentionally not repo-specific.

It does not replace:

- `AGENTS.md` as the execution contract in a concrete repository;
- `HUMANS.md` as the human operating guide;
- `docs/ai-workflow/ai/workflow.md` and `docs/ai-workflow/ai/workflow/` as workflow rules;
- `docs/ai-workflow/ai/memory.md` and `docs/ai-workflow/ai/memory/` as template-local memory router and entries;
- `docs/ai-workflow/repo/memory.md` and `docs/ai-workflow/repo/memory/` as repo-specific memory router and entries;
- `docs/ai-workflow/projects/<project>/memory.md` and `docs/ai-workflow/projects/<project>/memory/` as project-specific memory router and entries;
- repository state as the source of truth for implementation.

## Relationship To Other Memory Files

| Artifact | Scope | Belongs Here | Does Not Belong Here |
| --- | --- | --- | --- |
| `docs/ai-workflow/ai/external-memory/` | universal workflow/process memory | cross-repo workflow improvements, reusable autopilot rules, process anti-patterns, template and skill improvements | repo facts, domain facts, task-specific implementation knowledge |
| `docs/ai-workflow/ai/memory.md` and `docs/ai-workflow/ai/memory/` | this workflow template | template-local maintenance facts and history | target-repo facts or universal workflow lessons |
| `docs/ai-workflow/repo/memory.md` and `docs/ai-workflow/repo/memory/` | one repository | durable facts about this repo, local constraints, local history | generic workflow improvements meant for other repos |
| `docs/ai-workflow/projects/<project>/memory.md` and `docs/ai-workflow/projects/<project>/memory/` | one project/workspace | durable project decisions, project architecture facts, project-specific lessons | generic workflow system design |
| `docs/ai-workflow/projects/<project>/distillations/` | one completed task/package | task-level implementation lessons after PASS | broad rules unless promoted by checkpoint |

## Source-Of-Truth Rule

External Memory is advisory memory.

It can inspire updates to:

- `AGENTS.md`;
- `HUMANS.md`;
- `docs/ai-workflow/ai/workflow.md`;
- `docs/ai-workflow/ai/workflow/`;
- `docs/ai-workflow/ai/autopilot.md`;
- `docs/ai-workflow/ai/templates/`;
- `docs/ai-workflow/ai/skills/`;
- future standalone `ai-workflow` template repositories.

It does not directly override active workflow rules. A recommendation becomes enforceable only after it is intentionally written into the relevant contract or workflow document.

## Entry Naming

Create one file per memory entry:

```text
YYYY-MM-DD-short-kebab-title.md
```

If one day produces multiple similar entries, append a short suffix:

```text
YYYY-MM-DD-short-kebab-title-2.md
```

Use `docs/ai-workflow/ai/templates/external-memory/date-external-memory.template.md` for new entries.

After adding or updating an entry, update `docs/ai-workflow/ai/external-memory.md` with only date, topic, type, status, and route.

## What Belongs Here

Add entries when a lesson is:

- reusable across multiple repositories;
- about workflow mechanics, not a product domain;
- about Codex/operator collaboration;
- about autopilot behavior, gates, evidence, recovery, retry, checkpoints, or STOP conditions;
- about docs layout or template structure;
- about skills that should improve the reusable workflow;
- about how to reduce hallucination, drift, duplicate artifacts, or unsafe execution;
- about better handoff between owner, operator, engineer, and agent.

## What Does Not Belong Here

Do not add:

- customer or client data;
- secrets, credentials, tokens, or private keys;
- repo-specific commands unless they are examples clearly marked as examples;
- product/domain facts from a concrete repository;
- task implementation details;
- temporary chat context;
- raw logs or long command outputs;
- unreviewed guesses.

## Privacy Check

Before writing or sharing an external memory entry, confirm:

- it contains no secrets or credentials;
- it contains no client/customer personal data;
- it contains no proprietary product facts from the target repository;
- it is generalized enough to help improve `ai-workflow` across repositories;
- any examples are anonymized or clearly generic.

## Promotion Rules

An entry may be promoted from memory into workflow rules when:

- it is clearly universal, not repo-specific;
- it has a concrete recommendation and impact;
- it does not conflict with core safety rules;
- the owner accepts it or the workflow maintainer intentionally applies it;
- the target contract file is updated directly.

Promotion examples:

- universal process rule -> `docs/ai-workflow/ai/workflow/README.md`;
- agent execution rule -> `AGENTS.md`;
- human operating guidance -> `HUMANS.md`;
- template change -> `docs/ai-workflow/ai/templates/`;
- skill improvement -> `docs/ai-workflow/ai/skills/`;
- autopilot rule -> `docs/ai-workflow/ai/autopilot.md`;
- repo bootstrap requirement -> `docs/ai-workflow/repo/repo-intake.md`.

## Export And Share

When this directory has accumulated useful entries, for example 10-30 files, a human may zip it and send it to `ai@onlinen.tech`.

This is optional. It helps improve the reusable AI Workflow template and related skills.

Do not include repo-specific, project-specific, client, personal, secret, or proprietary data in the archive.

## Review Cadence

Review this directory:

- before extracting `ai-workflow` into a standalone template repository;
- after major workflow/autopilot experiments;
- after an autopilot STOP caused by process weakness;
- after repeated QA/fix-loop patterns;
- before changing universal workflow contracts or reusable skills.
