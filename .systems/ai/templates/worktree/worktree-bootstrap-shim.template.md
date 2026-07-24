# AI Workflow Worktree Bootstrap Shim

Before workflow-governed work:

1. Confirm `ai-workflow-workspace/` or another owner-accepted strong installation marker.
2. Confirm the worktree is not the official AI Workflow repository.
3. Confirm root `AGENTS.md` and nested `ai-workflow/`.
4. If the strong marker exists but `ai-workflow/` is missing, obtain platform approval and run:

```sh
git clone https://github.com/bracia-plociennik/ai-workflow.git ai-workflow
```

5. Verify origin and required clone files, then run:

```sh
ai-workflow/.systems/scripts/init-workspace
```

Stop on missing approval, a weak marker, existing root `AGENTS.md`, wrong origin, dirty clone, ambiguous contents, or official-repo self-clone. Do not overwrite or merge target-owned instructions automatically.
