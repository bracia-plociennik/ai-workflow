# Repo Runtime Docs

This directory contains target-repository-specific workflow runtime artifacts.

`docs/repo/` is the only canonical home for global facts about the repository that installed this workflow template. Keep `AGENTS.md`, `HUMANS.md`, root workflow docs, and `docs/ai/` portable and updateable from the upstream template.

## Files

- `context.md` - global repository context: what this repository is, domain, stack, modules, boundaries, and local constraints.
- `repo-intake.md` - repo-level workflow/bootstrap readiness, command map, safe environment, risks, restricted zones, and evidence.
- `status.md` - current cross-project workflow status for this repository.
- `memory.md` - aggregate repository memory after checkpoints and final checks.

## Rules

- Do not store project task specs, QA evidence, or autopilot runtime here; those belong in `docs/projects/<project>/`.
- Do not store universal workflow lessons here; those belong in `docs/ai/external-memory.md`.
- Do not store template design notes here; those belong in `docs/ai/memory.md`.
- Do not store secrets, credentials, production-only operational details, or private customer data.
