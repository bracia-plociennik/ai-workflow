# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.8.6` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-06-10` |
| Naming standard | lowercase kebab-case |
| Phase file standard | `phase-<number>-<name>.md` |

## Compatibility Notes

- `AGENTS.md` is a short router.
- `HUMANS.md` is the long human runbook.
- Default target-repository installation is a nested clone at `ai-workflow/`, a local-only root `AGENTS.md` shim, and a target-owned tracked workspace at `ai-workflow-workspace/`.
- `phase-0-init` is the first bootstrap phase after cloning AI Workflow into a target repository. It creates or verifies `AI_WORKFLOW_WORKSPACE_HOME`, preserves legacy context, and routes to repo intake.
- Official repo mode uses the upstream repository root as `AI_WORKFLOW_HOME`; there is no inner `ai-workflow/` directory.
- `.systems/ai/core/repository-modes.md` defines official repo mode, target repo mode, and shared path resolution.
- `.systems/` is the system-owned namespace inside `AI_WORKFLOW_HOME`.
- `AI_WORKFLOW_WORKSPACE_HOME/` is the target-owned runtime/advisory namespace, normally `ai-workflow-workspace/` beside `AI_WORKFLOW_HOME`.
- The official workflow repository must not track active `workspace/**` or `ai-workflow-workspace/**` on any branch.
- `.systems/scripts/check-branch-policy` blocks tracked `workspace/**` and `ai-workflow-workspace/**` inside the official repository. Local official `ai-workflow-workspace/` may exist only as ignored, untracked private runtime.
- `.systems/ai/` is system-owned policy and workflow source.
- `.systems/ai/core/` stores canonical AI router and policy files.
- `.systems/ai/core/response-contract.md` defines the required user-facing `Co dalej?` footer with one recommendation, one safe alternative, impacts, and copy-paste prompts.
- `.systems/ai/core/task-intake.md` defines the required Task Idea Validation lens before planning or executing any new task, approach request, side-task, micro-task, change request, or autopilot request.
- `.systems/ai/core/update-from-upstream.md` defines the safe target-repository update flow for nested clones. It does not touch `AI_WORKFLOW_WORKSPACE_HOME/**`.
- Autopilot requires a run-scoped readiness audit at `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/<run-id>/readiness.md` before the run can enter `running`.
- Autopilot must declare `planning-range` for phase 1 through phase 3 Spec QA or `implementation-range` for phase 4 through phase 7 checkpoint. `phase-8-final-check` is owner-triggered only and is not run automatically by autopilot.
- `.systems/ai/skills/` stores optional system-defined task-specific workflow skills.
- `AI_WORKFLOW_WORKSPACE_HOME/skills/` stores optional user-defined task-specific workflow skills and takes precedence as supporting guidance.
- `AI_WORKFLOW_WORKSPACE_HOME/external-memory/` stores target-owned External Memory improvement proposals.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/` stores repo-specific runtime facts.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/` stores canonical repo runtime routers.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/init.md` records target-repository bootstrap status.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md` is the repo context router; detailed repo context lives in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` is the legacy context router and summary; preserved source material lives in `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` and is indexed by `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/legacy-index.md`.
- Preserved legacy inputs under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`, detailed repo context entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`, and supporting project source materials under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/` are exempt from strict Markdown filename checks. Canonical repo context remains `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`, and canonical accepted project context remains `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/` stores project-specific runtime facts.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md` routes to `planning/`, and `tasks.md` routes to task cards in `tasks/`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/micro-tasks.md` routes to project-local low-risk micro-task artifacts in `micro-tasks/`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/change-requests.md` routes owner change requests before and after `final-owner-yes` to durable entries in `change-requests/`.
- `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` stores repo-level low-risk micro-projects.
- Autopilot runtime is run-scoped under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/`.
- `.systems/scripts/` is the system-owned validator namespace inside `AI_WORKFLOW_HOME`.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `.systems/`, `scripts`, and `.github/` require merge or preservation, not overwrite.
