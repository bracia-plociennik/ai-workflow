# update-from-upstream.md

## Purpose

This file defines the official update flow for target repositories that use AI Workflow as a nested clone in `ai-workflow/`.

It is not the development flow for the upstream `ai-workflow` repository. In official repo mode, use normal git branch, merge, cherry-pick, and release procedures. Repository modes are defined in `.systems/ai/core/repository-modes.md`.

Do not update target repositories with a raw pull inside the nested clone. Use:

```bash
ai-workflow/.systems/scripts/update-from-upstream
```

## Safety Model

The update flow treats the nested clone as two layers:

| Layer | Paths | Update Behavior |
| --- | --- | --- |
| System-owned | `AGENTS.md`, `HUMANS.md`, `README.md`, `.systems/**`, `.github/**` | Must be clean before update. Updated by upstream only. |
| Target-owned workspace | `AI_WORKFLOW_WORKSPACE_HOME/**`, normally `../ai-workflow-workspace/**` | Outside the nested clone. The update script must not modify it. |

Legacy filenames under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` must not be normalized, renamed, or rewritten during update. They are preserved source context outside the nested clone.

User skills under `AI_WORKFLOW_WORKSPACE_HOME/skills/`, External Memory under `AI_WORKFLOW_WORKSPACE_HOME/external-memory/`, and System Insights under `AI_WORKFLOW_WORKSPACE_HOME/system-insights/` are target-owned and must not be touched by upstream updates.

Target repositories must not edit `.systems/**`. If a target-repository run reveals a workflow improvement, write it to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/` and promote it only through the official upstream `ai-workflow` repository. If it reveals an anonymized operating lesson, write it to `AI_WORKFLOW_WORKSPACE_HOME/system-insights/` only through checkpoint/final-check routing or explicit owner-approved capture.

## Procedure

From the target repository root:

```bash
ai-workflow/.systems/scripts/update-from-upstream
```

The script:

1. Resolves `AI_WORKFLOW_HOME`.
2. Detects and warns about legacy `workspace/**` still inside the nested clone.
3. Blocks if system-owned files are dirty.
4. Runs `git fetch`.
5. Runs `git merge --ff-only`.
6. Runs `.systems/scripts/validate-workflow`.

## Options

```bash
ai-workflow/.systems/scripts/update-from-upstream --dry-run
ai-workflow/.systems/scripts/update-from-upstream --remote origin --branch main
ai-workflow/.systems/scripts/update-from-upstream --skip-validation
```

`--skip-validation` is for emergency debugging only. A skipped validation result is not eligible for final `PASS`.

## Stop Conditions

The update must stop when:

- any system-owned file is dirty;
- legacy `workspace/**` inside the nested clone contains untracked or modified runtime that has not been migrated;
- the target branch cannot be fetched;
- the merge is not fast-forwardable;
- validation fails after the upstream update.

Do not continue by manually pulling, overwriting system files, or moving workspace data without an explicit migration decision.

## Expected Result

After a successful update:

- system-owned files reflect upstream;
- `AI_WORKFLOW_WORKSPACE_HOME/**` was not touched by the update script;
- real micro-projects remain in the target-owned workspace;
- real project and human workspaces remain in the target-owned workspace;
- local external memory, system insights, and user skills remain in the target-owned workspace;
- legacy source filenames remain unchanged because the update does not edit workspace legacy files;
- validators pass.
