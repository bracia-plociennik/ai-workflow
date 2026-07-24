# worktree-bootstrap.md

## Purpose

Provide a safe preflight when a target worktree is expected to use AI Workflow but lacks the nested `ai-workflow/` clone or root `AGENTS.md` shim.

This contract does not apply to the official upstream AI Workflow repository and must never clone AI Workflow into itself.

## Strong Target Marker

Bootstrap is eligible only when at least one strong marker exists:

- `ai-workflow-workspace/`; or
- an owner-accepted repository marker that explicitly identifies an AI Workflow installation.

A repository name, chat claim, empty directory, or guessed convention is not a strong marker.

## Preflight

Before any clone:

1. Resolve the target Git worktree with `git rev-parse`, including linked worktrees where `.git` is a file, and confirm it is not official AI Workflow repo mode.
2. Confirm a strong marker.
3. Confirm platform approval for network and write effects.
4. Stop if root `AGENTS.md` already exists; merge requires a separate owner-approved task.
5. Stop if `ai-workflow/` exists with a wrong origin, dirty system files, or ambiguous contents.

When the nested clone is absent, run exactly:

```sh
git clone https://github.com/bracia-plociennik/ai-workflow.git ai-workflow
```

Then:

1. verify origin is `https://github.com/bracia-plociennik/ai-workflow.git` or its canonical Git equivalent;
2. verify required clone contents, including `AGENTS.md` and `.systems/scripts/init-workspace`;
3. run `ai-workflow/.systems/scripts/init-workspace`;
4. verify the root shim was created only because root `AGENTS.md` was absent;
5. verify the clone and root shim are locally excluded as defined by installation policy.

Resolve the exclude file with `git rev-parse --git-path info/exclude`; do not assume `.git` is a directory in a linked worktree.

## Portable Instruction Shim

Global or parent-system instructions may use this short route:

```text
Before workflow-governed work in a target worktree, verify a strong AI Workflow marker, ai-workflow/, and root AGENTS.md. If the marker is strong but the clone is missing, obtain platform approval and run the canonical clone command, then verify origin and run init-workspace. Stop on an existing AGENTS.md, wrong origin, dirty clone, ambiguous marker, or official-repo self-clone.
```

The portable shim is routing guidance only. It does not grant network or write permission.

## Testability

`.systems/scripts/bootstrap-target-worktree` defaults to the canonical GitHub remote. Its test-only remote override requires `AI_WORKFLOW_BOOTSTRAP_TEST_MODE=1`; production use cannot choose an arbitrary remote.

Smoke tests must use a local bare remote and must not contact GitHub.

## Authority Boundary

Bootstrap cannot overwrite target-owned files, change product code, bypass platform approval, infer an installation from a weak marker, normalize a dirty clone, or merge existing root instructions.
