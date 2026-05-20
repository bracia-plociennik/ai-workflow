# memory

## Purpose

`docs/projects/<project>/memory/` stores detailed project memory entries.

The router/index is `docs/projects/<project>/memory.md`.

## Entry Naming

Create one file per memory entry:

```text
YYYY-MM-DD-short-kebab-title.md
```

Use `docs/ai/templates/projects/date-memory-entry.template.md` for new entries.

## What Belongs Here

- durable project decisions;
- project-specific constraints;
- implementation knowledge needed by future tasks in the same project;
- project-level risks found through distillation/checkpoint/final check;
- project-specific drift/watch items.

## What Does Not Belong Here

- repo-wide facts;
- template maintenance memory;
- universal workflow/process lessons;
- secrets, credentials, client data, or production-only operational details.

## Router Rule

After adding or updating an entry, update `docs/projects/<project>/memory.md` with only date, topic, type, status, and route.
