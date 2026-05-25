# AI Docs

This directory contains system-owned AI operational knowledge and workflow infrastructure.

Do not store target-repository-specific facts in `.systems/ai/`. Runtime repo context, intake, status, and aggregate memory belong in `workspace/repo/`.

## Contents

- `core/` - canonical routers, policy docs, update policy, version, changelog, and memory indexes.
- `core/operating-model.md` - primary operating contract behind the short `AGENTS.md` router.
- `core/workflow.md` - phase router and canonical phase index.
- `core/installation.md` - safe installation and collision policy for existing repositories.
- `core/update-from-upstream.md` - safe upstream update policy for target repositories using the nested clone.
- `core/autopilot.md` - autopilot launch and runtime rules.
- `core/command-routing.md` - user-facing workflow command aliases and interpretation rules.
- `core/task-intake.md` - required lightweight validation lens before planning or executing new tasks.
- `core/guide.md` - orientation rules for lost, starting, next-step, and recovery prompts.
- `core/response-contract.md` - required user-facing response footer with one recommendation, one safe alternative, impacts, and copy-paste prompts.
- `core/change-requests.md` - owner change request policy before and after final owner approval.
- `core/definition-of-done.md` - evidence-backed done criteria.
- `core/risk-model.md` - risk classes and approval routing.
- `core/commands.md` - verification command contract.
- `core/permissions.md` - forbidden actions and safe defaults.
- `core/prompt-injection.md` - defense rules for untrusted repository content.
- `core/rollback.md` - rollback requirements for high-risk work.
- `core/dependencies.md` - dependency approval and review policy.
- `core/deprecation.md` - archive and supersession policy.
- `core/version.md` and `core/changelog.md` - workflow version and migration history.
- `core/memory.md` and `memory/` - system-owned template-local memory router and detailed maintenance entries.
- `workflow/` - detailed phase-level workflow rules.
- `templates/` - reusable templates for repo runtime, workflow, autopilot, project, human, and Codex artifacts.
- `skills/` - system-defined task-specific execution guidance, empty by default.

## Runtime Boundaries

In target repositories, this directory normally lives under `AI_WORKFLOW_HOME`, usually `ai-workflow/.systems/ai/`. Product files, app commands, tests, builds, migrations, and target-owned root docs remain in `TARGET_REPO_ROOT`.

- Repo-specific facts belong in `workspace/repo/`; detailed repo context belongs in `workspace/repo/context/` and is indexed by `workspace/repo/core/context.md`.
- Project-specific facts belong in `workspace/projects/<project>/`, with accepted project context under `workspace/projects/<project>/context.md`.
- Repo-level low-risk micro-projects belong in `workspace/micro-projects/`.
- Human-facing coordination docs belong in `workspace/humans/<project>/`.
- Template/process docs belong in `.systems/ai/` and are read-only in target repositories.
- Template maintenance memory belongs in `.systems/ai/memory/` and is indexed by `.systems/ai/core/memory.md`.
- Universal AI Workflow improvement lessons belong in `workspace/external-memory/memory/` and are indexed by `workspace/external-memory/external-memory.md`.
- System-defined AI Workflow skills belong in `.systems/ai/skills/`.
- User-defined local skills belong in `workspace/skills/` and take precedence over system skills as supporting guidance only.

## Manual Iterations

For a new repository or a repository where `ai-workflow/` was just cloned, start from `workspace/repo/core/context.md`, `workspace/repo/context/`, and `workspace/repo/core/repo-intake.md`, using `templates/repo/` if the runtime files are missing or still describe the upstream `ai-workflow` repository.

Before installing into an existing repository, follow `core/installation.md`. Do not overwrite target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `.systems/`, or `.github/`. The default install keeps workflow internals inside `ai-workflow/` and uses only the root `AGENTS.md` shim from `.systems/ai/templates/root-agents.template.md`.

For project-level workflow work, start from `core/workflow.md`, verify `workspace/repo/core/status.md`, then open the relevant phase file under `workflow/`.

Before planning, specifying, implementing, or reviewing a task, apply `core/task-intake.md`, then check `workspace/skills/` first and `skills/` second for a relevant task-specific skill. If no matching skill exists, continue with the normal workflow.

## Autopilot Iterations

Global autopilot rules and templates live here. Runtime autopilot artifacts belong in the active project workspace, under run directories such as `workspace/projects/<project>/autopilot/runs/autopilot-001/`.

Do not store project task specs, project plans, project QA evidence, project decisions, External Memory, user skills, or target-repo runtime facts directly in `.systems/ai/`.
