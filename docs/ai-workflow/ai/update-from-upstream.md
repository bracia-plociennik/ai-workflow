# update-from-upstream.md

## Purpose

This file defines the official update flow for target repositories that use AI Workflow as a nested clone in `ai-workflow/`.

Do not update target repositories with a raw pull inside the nested clone. Use:

```bash
ai-workflow/scripts/ai-workflow/update-from-upstream
```

## Safety Model

The update flow treats the nested clone as two layers:

| Layer | Paths | Update Behavior |
| --- | --- | --- |
| Template-owned | `AGENTS.md`, `HUMANS.md`, `README.md`, `docs/ai-workflow/ai/**`, `scripts/**`, `.github/**`, `docs/ai-workflow/projects/EXAMPLE/**`, `docs/ai-workflow/humans/EXAMPLE/**` | Must be clean before update. Updated by upstream. |
| Repo runtime | `docs/ai-workflow/repo/**` | Protected and restored after upstream update. |
| Real project workspaces | `docs/ai-workflow/projects/*` except `README.md` and `EXAMPLE` | Protected and restored after upstream update. |
| Real human workspaces | `docs/ai-workflow/humans/*` except `README.md` and `EXAMPLE` | Protected and restored after upstream update. |
| Local external memory | `docs/ai-workflow/ai/external-memory.md`, `docs/ai-workflow/ai/external-memory/**` | Protected and restored after upstream update. |

Legacy filenames under `docs/ai-workflow/repo/legacy/` must not be normalized, renamed, or rewritten during update. They are preserved source context.

## Procedure

From the target repository root:

```bash
ai-workflow/scripts/ai-workflow/update-from-upstream
```

The script:

1. Resolves `AI_WORKFLOW_HOME`.
2. Blocks if template-owned files are dirty.
3. Backs up protected runtime/workspace/external-memory paths.
4. Cleans protected paths only inside the nested clone working tree.
5. Runs `git fetch`.
6. Runs `git merge --ff-only`.
7. Restores protected paths.
8. Runs `scripts/ai-workflow/validate-workflow`.

## Options

```bash
ai-workflow/scripts/ai-workflow/update-from-upstream --dry-run
ai-workflow/scripts/ai-workflow/update-from-upstream --remote origin --branch main
ai-workflow/scripts/ai-workflow/update-from-upstream --skip-validation
```

`--skip-validation` is for emergency debugging only. A skipped validation result is not eligible for final `PASS`.

## Stop Conditions

The update must stop when:

- any template-owned file is dirty;
- the target branch cannot be fetched;
- the merge is not fast-forwardable;
- protected paths cannot be restored;
- validation fails after restore.

Do not continue by manually pulling or overwriting protected paths.

## Expected Result

After a successful update:

- template-owned files reflect upstream;
- repo runtime still describes the target repository;
- real project and human workspaces are preserved;
- local external memory is preserved;
- legacy source filenames are unchanged;
- validators pass.
