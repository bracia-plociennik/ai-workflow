# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.8.20` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-07-20` |
| Naming standard | lowercase kebab-case with canonical `SKILL.md` skill-contract exception |
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
- `.systems/ai/core/task-intake.md` defines the default Task Idea Validation lens before planning or executing any new task, approach request, side-task, micro-task, change request, or autopilot request. Owner opt-out requires explicit wording and cannot bypass risk, permissions, evidence, QA/Quality, phase gates, or approvals.
- `.systems/ai/core/parallel-work-policy.md` defines status-only coordination for multiple projects, tasks, micro-tasks, micro-projects, and Codex threads without adding lock files or scheduler state.
- `.systems/ai/core/contract-compliance.md` defines advisory work mode compliance and commit readiness knowledge capture decisions.
- Each workflow phase artifact includes `Optional Knowledge Capture` as a soft phase-level decision for memory, decision, status, External Memory, and System Insights candidates.
- `.systems/ai/core/prompt-composition.md` defines advisory prompt modules, role profiles, variable packs, project-local prompting lifecycle, and authority limits.
- `.systems/ai/core/system-insights.md` defines advisory anonymized System Insights, privacy rules, allowed categories, status lifecycle, write routing, and skill-candidate boundaries.
- `.systems/ai/core/dreaming-mode.md` defines advisory-only Dreaming Mode reports for AFK/nightly analysis. Dream Reports live under `AI_WORKFLOW_WORKSPACE_HOME/dreams/runs/`, default to `workflow-artifacts-only`, require explicit owner request for `full-repo`, and never perform durable writes, scheduler setup, memory promotion, status mutation, commits, or source changes.
- `.systems/ai/core/quality-review.md` defines read-only/advisory global quality review stance for review, code review, final review, findings, blockers, and generic quality-check prompts that are not formal workflow phase runs.
- `.systems/ai/core/request-batch-triage.md` defines advisory pre-routing for owner lists, checklists, brain dumps, mixed improvements, and `2+ owner items` before ordinary task intake or implementation routing.
- `.systems/ai/core/end-of-task-capture.md` defines chat-end knowledge capture for prompts such as `to koniec zadania`, while preserving formal distillation, checkpoint, final review, final check, final-owner-yes, change request, and commit-readiness routing.
- Substantive responses include `Execution Trace` before the final `Co dalej?` footer, Phase Skill Discovery checks existing domain/task skills before workflow-governed procedures, and Default Quality Closure reports formal or advisory review status unless the owner opts out.
- `.systems/ai/templates/prompting/` stores reusable prompt composition templates, while `.systems/ai/examples/prompting/` stores documentation-only examples.
- Project-local prompting artifacts belong under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/prompting/` when a project explicitly creates them.
- `.systems/scripts/check-prompt-composition` validates required prompt composition artifacts, router references, and deterministic unsafe-authority grant patterns.
- `.systems/ai/core/update-from-upstream.md` defines the safe target-repository update flow for nested clones. It does not touch `AI_WORKFLOW_WORKSPACE_HOME/**`.
- `.systems/scripts/update-workspace` backfills missing neutral `AI_WORKFLOW_WORKSPACE_HOME/**` schema files after upstream updates without overwriting existing runtime artifacts.
- Autopilot requires a run-scoped readiness audit at `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/<run-id>/readiness.md` before the run can enter `running`.
- Autopilot must declare `planning-range` for phase 1 through phase 3 Spec QA or `implementation-range` for phase 4 through phase 7 checkpoint. `phase-8-final-check` is owner-triggered only and is not run automatically by autopilot.
- `.systems/ai/skills/` stores optional system-defined task-specific workflow skills. Active skills use `SKILL.md` as the canonical agent contract and `README.md` as a short human-facing summary.
- Skill `context/` directories under `.systems/ai/skills/<skill>/context/` and `AI_WORKFLOW_WORKSPACE_HOME/skills/<skill>/context/` are raw source archives only. Context-driven skill builds require `skill-intake-plan.md` before final active artifacts are written.
- Active skill contracts should stay compact; `.systems/scripts/check-system-skills` and `skill-creator/scripts/quick_validate.py` enforce a 300-line `SKILL.md` limit and block `context/**` from becoming active guidance or authority.
- `.systems/ai/skills/legacy/**` stores preserved external skill source material as context/data only, not active skill guidance.
- Registered pre-V1 formal QA evidence may receive terminal compatibility admission only through an exact workspace-relative path and SHA-256 registry match; V1-marked artifacts always use current strict validation.
- `AI_WORKFLOW_WORKSPACE_HOME/skills/` stores optional user-defined task-specific workflow skills and takes precedence as supporting guidance.
- `AI_WORKFLOW_WORKSPACE_HOME/external-memory/` stores target-owned External Memory improvement proposals.
- `AI_WORKFLOW_WORKSPACE_HOME/system-insights/` stores target-owned anonymized cross-project operating lessons and skill candidates.
- `AI_WORKFLOW_WORKSPACE_HOME/dreams/` stores target-owned advisory Dream Reports and owner decision queues.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/` stores repo-specific runtime facts.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/` stores canonical repo runtime routers.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/init.md` records target-repository bootstrap status.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md` is the repo context router; detailed repo context lives in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` is the legacy context router and summary; preserved source material lives in `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` and is indexed by `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/legacy-index.md`.
- Preserved legacy inputs under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`, detailed repo context entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`, supporting project source materials under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/`, and skill source materials under `.systems/ai/skills/<skill>/context/` and `AI_WORKFLOW_WORKSPACE_HOME/skills/<skill>/context/` are exempt from strict Markdown filename checks. Canonical repo context remains `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`, and canonical accepted project context remains `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/` stores project-specific runtime facts.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md` routes to `planning/`, and `tasks.md` routes to task cards in `tasks/`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/micro-tasks.md` routes to project-local low-risk micro-task artifacts in `micro-tasks/`.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/change-requests.md` routes owner change requests before and after `final-owner-yes` to durable entries in `change-requests/`.
- `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` stores repo-level low-risk micro-projects.
- Autopilot runtime is run-scoped under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/`.
- `.systems/scripts/` is the system-owned validator namespace inside `AI_WORKFLOW_HOME`.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `.systems/`, `scripts`, and `.github/` require merge or preservation, not overwrite.
