# repository-modes.md
For future approved scopes, use `.systems/ai/core/phase-commit-policy.md` at planning-range end and phases 6/7/8. Explicit no-commit is not overridden; current PTO approval is non-retroactive. Ignored-only/no-op creates no commit. Phase8 requires actual final-owner-yes, counterpart impact must be resolved, one coordinator owns the index, and push is never inferred. Bound V3/schema3 is opt-in and current-only; unsupported proof needs fresh QA. Fresh owned artifact closure remains separate from source equivalence. Validator: `check-phase-commit-policy`.


## Purpose

AI Workflow supports two repository modes. The mode changes path resolution only; it does not change gates, risk policy, permissions, Definition of Done, or evidence requirements.

## Official Repo Mode

Use `official-repo` mode when working inside the upstream `ai-workflow` repository itself.

- `AI_WORKFLOW_HOME` is the repository root.
- `TARGET_REPO_ROOT` is the repository root.
- `.systems/`, `.github/`, `AGENTS.md`, `HUMANS.md`, and `README.md` live directly in the repository root.
- There is no inner `ai-workflow/` directory. This is expected and valid.
- Only the official `dev` branch may track a privacy-reviewed `ai-workflow-workspace/` snapshot. `main`, other branches, unknown branch identity and nested installations must not track this directory.
- On `main` and other branches a local workspace remains ignored. On official `dev`, remove only its root ignore rule, retain generated/sensitive-file exclusions, and run `check-workspace-publication` before publishing changed blobs.
- Published runtime is supporting data, not installed target state or current QA PASS. Historical reports retain their original content and baseline; privacy-sensitive files remain local.

Default official workspace:

```text
<AI_WORKFLOW_HOME>/ai-workflow-workspace/
```

## Target Repo Mode

Use `target-repo` mode when AI Workflow is cloned into another repository as a nested clone.

- `AI_WORKFLOW_HOME` is `<TARGET_REPO_ROOT>/ai-workflow`.
- `TARGET_REPO_ROOT` is the parent application repository.
- `AI_WORKFLOW_WORKSPACE_HOME` is normally `<TARGET_REPO_ROOT>/ai-workflow-workspace`.
- The target root may have a local-only `AGENTS.md` shim created by `phase-0-init`.
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
- Validators must not require a workspace to exist in the official repository.
- Validators may read the selected local workspace when runtime checks are requested. Source CI uses a separate empty validation workspace and checks publication integrity separately; it does not certify the snapshot's current project QA.

The resolver exports:

```text
AI_WORKFLOW_MODE_RESOLVED
AI_WORKFLOW_HOME
TARGET_REPO_ROOT
AI_WORKFLOW_WORKSPACE_HOME
```

## Branch Policy

`.systems/scripts/check-branch-policy` enforces runtime tracking rules:

- all modes block legacy `workspace/**`;
- only official `dev` with a current publication review may track `ai-workflow-workspace/**`; all other branches and nested installations block it;
- target repositories may commit their sibling `ai-workflow-workspace/**` in the parent application repository, not inside the nested `ai-workflow/` clone.

The absence of an inner `ai-workflow/` directory in the upstream repository is not a branch policy violation.

Local Git branch identity and the canonical `origin` URL govern the exception. Verified detached GitHub Actions push/PR context may identify `dev`; a PR targeting `main` remains forbidden. `AI_WORKFLOW_BRANCH_POLICY=dev` cannot override branch or installation identity, while `public` always forbids tracked runtime. Move product changes from `dev` to `main` by selecting product commits; never merge the workspace snapshot or its dev-only ignore configuration into `main`.
