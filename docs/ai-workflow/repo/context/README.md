# context

## Purpose

This directory stores detailed global context for the current repository.

The router/index is `docs/ai-workflow/repo/context.md`.

Files in this directory are supporting repo context entries and are exempt from `scripts/ai-workflow/check-naming`. The canonical router is still `docs/ai-workflow/repo/context.md` and should remain lowercase kebab-case.

## Entry Types

- `overview.md` - what this repository is and who it serves.
- `stack.md` - languages, frameworks, package managers, runtime services, datastores, queues, schedulers, and integrations.
- `areas.md` - main repository areas and ownership boundaries.
- `boundaries.md` - in-scope, out-of-scope, and shared ownership boundaries.
- `local-rules.md` - repo-local operating rules that affect future work.

## Rules

- Treat this directory as repo-specific runtime context.
- Do not store target-repository facts in `docs/ai-workflow/ai/`.
- Do not store project-specific context here; use `docs/ai-workflow/projects/<project>/context/`.
- Do not store secrets, credentials, private customer data, or production-only operational details.
- Update `docs/ai-workflow/repo/context.md` when adding, renaming, or superseding an entry.
