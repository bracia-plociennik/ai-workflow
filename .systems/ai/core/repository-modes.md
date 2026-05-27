# repository-modes.md

## Purpose

AI Workflow supports two repository modes. The mode changes path resolution only; it does not change gates, risk policy, permissions, Definition of Done, or evidence requirements.

## Official Repo Mode

Use `official-repo` mode when working inside the upstream `ai-workflow` repository itself.

- `AI_WORKFLOW_HOME` is the repository root.
- `TARGET_REPO_ROOT` is the repository root.
- `.systems/`, `.github/`, `AGENTS.md`, `HUMANS.md`, and `README.md` live directly in the repository root.
- There is no inner `ai-workflow/` directory. This is expected and valid.
- On public `main`, no active runtime workspace may be tracked.
- On `dev`, this repository may track its own runtime under `AI_WORKFLOW_HOME/ai-workflow-workspace/`.

Default official workspace:

```text
<AI_WORKFLOW_HOME>/ai-workflow-workspace/
```

## Target Repo Mode

Use `target-repo` mode when AI Workflow is cloned into another repository as a nested clone.

- `AI_WORKFLOW_HOME` is `<TARGET_REPO_ROOT>/ai-workflow`.
- `TARGET_REPO_ROOT` is the parent application repository.
- `AI_WORKFLOW_WORKSPACE_HOME` is normally `<TARGET_REPO_ROOT>/ai-workflow-workspace`.
- The target root may have a local-only `AGENTS.md` shim created by `.systems/scripts/init-workspace`.
- The target repository should not commit `ai-workflow/` or the root shim.
- The target repository may commit `ai-workflow-workspace/` when it contains repo/project runtime facts.

Default target workspace:

```text
<TARGET_REPO_ROOT>/ai-workflow-workspace/
```

## Resolver Contract

Use `.systems/scripts/resolve-workflow-env` for shell scripts that need path resolution.

- `AI_WORKFLOW_MODE=auto|official|target`, default `auto`.
- `AI_WORKFLOW_WORKSPACE_HOME` overrides the default workspace path.
- In `official` mode, default workspace is inside `AI_WORKFLOW_HOME`.
- In `target` mode, default workspace is beside `AI_WORKFLOW_HOME`.
- Validators must not require a workspace to exist on public `main`.
- If the official `dev` workspace exists, validators should read it automatically.

The resolver exports:

```text
AI_WORKFLOW_MODE_RESOLVED
AI_WORKFLOW_HOME
TARGET_REPO_ROOT
AI_WORKFLOW_WORKSPACE_HOME
```

## Branch Policy

`.systems/scripts/check-branch-policy` enforces runtime tracking rules:

- `public` mode blocks `workspace/**` and `ai-workflow-workspace/**`.
- `dev` mode allows `ai-workflow-workspace/**`.
- all modes block legacy `workspace/**`.

The absence of an inner `ai-workflow/` directory in the upstream repository is not a branch policy violation.
