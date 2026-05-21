# update-from-upstream.md

## Purpose

This file defines the official update flow for target repositories that use AI Workflow as a nested clone in `ai-workflow/`.

Do not update target repositories with a raw pull inside the nested clone. Use:

```bash
ai-workflow/.systems/scripts/update-from-upstream
```

## Safety Model

The update flow treats the nested clone as two layers:

| Layer | Paths | Update Behavior |
| --- | --- | --- |
| System-owned | `AGENTS.md`, `HUMANS.md`, `README.md`, `.systems/**`, `.github/**` | Must be clean before update. Updated by upstream only. |
| Workspace-owned | `workspace/**` | Protected and restored after upstream update. |

Legacy filenames under `workspace/repo/legacy/` must not be normalized, renamed, or rewritten during update. They are preserved source context.

User skills under `workspace/skills/` and External Memory under `workspace/external-memory/` are workspace-owned and must survive upstream updates.

Target repositories must not edit `.systems/**`. If a target-repository run reveals a workflow improvement, write it to `workspace/external-memory/` and promote it only through the official upstream `ai-workflow` repository.

## Procedure

From the target repository root:

```bash
ai-workflow/.systems/scripts/update-from-upstream
```

The script:

1. Resolves `AI_WORKFLOW_HOME`.
2. Blocks if system-owned files are dirty.
3. Backs up the protected `workspace/**` tree.
4. Cleans protected paths only inside the nested clone working tree.
5. Runs `git fetch`.
6. Runs `git merge --ff-only`.
7. Restores protected paths.
8. Runs `.systems/scripts/validate-workflow`.

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
- the target branch cannot be fetched;
- the merge is not fast-forwardable;
- protected paths cannot be restored;
- validation fails after restore.

Do not continue by manually pulling or overwriting protected paths.

## Expected Result

After a successful update:

- system-owned files reflect upstream;
- workspace runtime still describes the target repository;
- real micro-projects are preserved;
- real project and human workspaces are preserved;
- local external memory and user skills are preserved;
- legacy source filenames are unchanged;
- validators pass.
