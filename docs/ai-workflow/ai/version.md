# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.7.0` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-05-19` |
| Naming standard | lowercase kebab-case |
| Phase file standard | `phase-<number>-<name>.md` |

## Compatibility Notes

- `AGENTS.md` is a short router.
- `HUMANS.md` is the long human runbook.
- Default target-repository installation is a nested clone at `ai-workflow/` plus a root `AGENTS.md` shim from `docs/ai-workflow/ai/templates/root-agents.template.md`.
- `docs/ai-workflow/` is the workflow-owned documentation namespace inside `AI_WORKFLOW_HOME`.
- `docs/ai-workflow/ai/` is template-owned policy and workflow source.
- `docs/ai-workflow/ai/skills/` stores optional task-specific workflow skills.
- `docs/ai-workflow/repo/` stores repo-specific runtime facts.
- `docs/ai-workflow/repo/context.md` is the repo context router; detailed repo context lives in `docs/ai-workflow/repo/context/`.
- `docs/ai-workflow/projects/<project>/` stores project-specific runtime facts.
- `docs/ai-workflow/projects/<project>/plans.md` routes to `planning/`, and `tasks.md` routes to task cards in `tasks/`.
- Autopilot runtime is run-scoped under `docs/ai-workflow/projects/<project>/autopilot/runs/`.
- `scripts/ai-workflow/` is the workflow-owned validator namespace inside `AI_WORKFLOW_HOME`.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `scripts`, and `.github/` require merge or preservation, not overwrite.
