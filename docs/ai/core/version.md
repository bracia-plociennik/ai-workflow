# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.7.2` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-05-20` |
| Naming standard | lowercase kebab-case |
| Phase file standard | `phase-<number>-<name>.md` |

## Compatibility Notes

- `AGENTS.md` is a short router.
- `HUMANS.md` is the long human runbook.
- Default target-repository installation is a nested clone at `ai-workflow/` plus a root `AGENTS.md` shim from `docs/ai/templates/root-agents.template.md`.
- `docs/` is the workflow-owned documentation namespace inside `AI_WORKFLOW_HOME`.
- `docs/ai/` is template-owned policy and workflow source.
- `docs/ai/core/` stores canonical AI router and policy files.
- `docs/ai/core/update-from-upstream.md` defines the safe target-repository update flow for nested clones.
- `docs/ai/skills/` stores optional task-specific workflow skills.
- `docs/repo/` stores repo-specific runtime facts.
- `docs/repo/core/` stores canonical repo runtime routers.
- `docs/repo/core/context.md` is the repo context router; detailed repo context lives in `docs/repo/context/`.
- `docs/repo/core/legacy.md` is the legacy context router and summary; preserved source material lives in `docs/repo/legacy/`.
- Preserved legacy inputs under `docs/repo/legacy/`, detailed repo context entries under `docs/repo/context/`, and supporting project source materials under `docs/projects/<project>/context/` are exempt from strict Markdown filename checks. Canonical repo context remains `docs/repo/core/context.md`, and canonical accepted project context remains `docs/projects/<project>/context.md`.
- `docs/projects/<project>/` stores project-specific runtime facts.
- `docs/projects/<project>/plans.md` routes to `planning/`, and `tasks.md` routes to task cards in `tasks/`.
- `docs/projects/<project>/micro-tasks.md` routes to project-local low-risk micro-task artifacts in `micro-tasks/`.
- `docs/micro-projects/` stores repo-level low-risk micro-projects.
- Autopilot runtime is run-scoped under `docs/projects/<project>/autopilot/runs/`.
- `scripts/` is the workflow-owned validator namespace inside `AI_WORKFLOW_HOME`.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `scripts`, and `.github/` require merge or preservation, not overwrite.
