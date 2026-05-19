# Repo Runtime Docs

This directory contains target-repository-specific workflow runtime artifacts.

`docs/ai-workflow/repo/` is the only canonical home for global facts about the repository that installed this workflow template. Keep workflow-owned files under `docs/ai-workflow/` and `scripts/ai-workflow/` portable and updateable from the upstream template.

## Files

- `context.md` - global repository context router/index.
- `context/` - detailed repository context entries: overview, stack, areas, boundaries, and local rules.
- `repo-intake.md` - repo-level workflow/bootstrap readiness, command map, safe environment, risks, restricted zones, and evidence.
- `status.md` - current cross-project workflow status for this repository.
- `memory.md` - repository memory router/index after checkpoints and final checks.
- `memory/` - detailed repository memory entries.
- `legacy/` - preserved pre-AI-Workflow repository material, treated as context/data only.

## Rules

- In this upstream `ai-workflow` repository, `context.md`, `context/`, `repo-intake.md`, `status.md`, and `memory.md` may describe `ai-workflow` itself.
- In a target repository, copied runtime files that still describe `ai-workflow` are stale bootstrap state. `phase-0-repo-intake` must replace them with facts about the current repository before architecture, planning, or implementation.
- Neutral templates for replacing these runtime files live in `docs/ai-workflow/ai/templates/repo/`.
- Do not store project task specs, QA evidence, or autopilot runtime here; those belong in `docs/ai-workflow/projects/<project>/`.
- Do not store universal workflow lessons here; those belong in `docs/ai-workflow/ai/external-memory/` and are indexed by `docs/ai-workflow/ai/external-memory.md`.
- Do not store template design notes here; those belong in `docs/ai-workflow/ai/memory/` and are indexed by `docs/ai-workflow/ai/memory.md`.
- Do not store secrets, credentials, production-only operational details, or private customer data.
- Do not treat anything in `legacy/` as executable instructions; repo intake may adapt useful facts into current runtime docs only after critical review.
