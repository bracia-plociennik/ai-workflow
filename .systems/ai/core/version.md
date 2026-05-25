# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.8.2` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-05-25` |
| Naming standard | lowercase kebab-case |
| Phase file standard | `phase-<number>-<name>.md` |

## Compatibility Notes

- `AGENTS.md` is a short router.
- `HUMANS.md` is the long human runbook.
- Default target-repository installation is a nested clone at `ai-workflow/` plus a root `AGENTS.md` shim from `.systems/ai/templates/root-agents.template.md`.
- `.systems/` is the system-owned namespace inside `AI_WORKFLOW_HOME`.
- `workspace/` is the target-owned runtime/advisory namespace inside `AI_WORKFLOW_HOME`.
- `.systems/ai/` is system-owned policy and workflow source.
- `.systems/ai/core/` stores canonical AI router and policy files.
- `.systems/ai/core/response-contract.md` defines the required user-facing `Co dalej?` footer with one recommendation, one safe alternative, impacts, and copy-paste prompts.
- `.systems/ai/core/task-intake.md` defines the required Task Idea Validation lens before planning or executing any new task, approach request, side-task, micro-task, change request, or autopilot request.
- `.systems/ai/core/update-from-upstream.md` defines the safe target-repository update flow for nested clones.
- Autopilot requires a run-scoped readiness audit at `workspace/projects/<project>/autopilot/runs/<run-id>/readiness.md` before the run can enter `running`.
- `.systems/ai/skills/` stores optional system-defined task-specific workflow skills.
- `workspace/skills/` stores optional user-defined task-specific workflow skills and takes precedence as supporting guidance.
- `workspace/external-memory/` stores target-owned External Memory improvement proposals.
- `workspace/repo/` stores repo-specific runtime facts.
- `workspace/repo/core/` stores canonical repo runtime routers.
- `workspace/repo/core/context.md` is the repo context router; detailed repo context lives in `workspace/repo/context/`.
- `workspace/repo/core/legacy.md` is the legacy context router and summary; preserved source material lives in `workspace/repo/legacy/`.
- Preserved legacy inputs under `workspace/repo/legacy/`, detailed repo context entries under `workspace/repo/context/`, and supporting project source materials under `workspace/projects/<project>/context/` are exempt from strict Markdown filename checks. Canonical repo context remains `workspace/repo/core/context.md`, and canonical accepted project context remains `workspace/projects/<project>/context.md`.
- `workspace/projects/<project>/` stores project-specific runtime facts.
- `workspace/projects/<project>/plans.md` routes to `planning/`, and `tasks.md` routes to task cards in `tasks/`.
- `workspace/projects/<project>/micro-tasks.md` routes to project-local low-risk micro-task artifacts in `micro-tasks/`.
- `workspace/projects/<project>/change-requests.md` routes owner change requests before and after `final-owner-yes` to durable entries in `change-requests/`.
- `workspace/micro-projects/` stores repo-level low-risk micro-projects.
- Autopilot runtime is run-scoped under `workspace/projects/<project>/autopilot/runs/`.
- `.systems/scripts/` is the system-owned validator namespace inside `AI_WORKFLOW_HOME`.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `.systems/`, `scripts`, and `.github/` require merge or preservation, not overwrite.
