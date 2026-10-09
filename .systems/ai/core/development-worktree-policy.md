# Development Worktree And Filtered Publication Policy

## Development Base
The official AI Workflow development checkout uses `dev`. New substantive
implementation work uses an owned `codex/<scope>` linked worktree created with
an explicit `dev` ref. Do not accept a tool's default `main` starting ref.
Read this contract before creating a development worktree or publishing product
changes. Target worktree bootstrap remains a separate installation route.

Inspect repository identity, branch, HEAD, index, registered worktrees and
ownership first. Reuse an appropriate owned worktree. Do not overwrite local
files, another worktree's branch, or unrelated staging; no automatic stash,
reset, force or cleanup. Branch/worktree operations still require their existing
permissions. A worktree is file isolation, not a security sandbox; shared ports,
databases and generated resources require separate ownership.

## Inherited Workspace
Only official `dev` may change and publish a privacy-reviewed workspace snapshot.
A canonical, non-nested linked `codex/*` worktree may inherit that snapshot when
local `dev` is an ancestor of HEAD and the complete indexed workspace is identical
to `dev`, with no workspace-changing commits after that base (even if reverted).
This is a read-only inheritance exception, not permission to publish new runtime.
A stale base, changed index or runtime commit history requires review, never
automatic history rewriting. `check-branch-policy` checks identity, ancestry,
index/history equality and `check-workspace-publication` privacy/hash binding.

One coordinator owns shared development workspace writes. Inherited files are
supporting historical data, not current approvals or QA. Worker runtime evidence
uses an explicitly selected private/ignored or temporary workspace; do not
write into the inherited snapshot. Local unstaged workspace content is not a
publication inventory: preserve it, and stage exact reviewed paths only.

Verified detached GitHub PR merge contexts targeting `dev` may inherit the
unchanged first-parent workspace. A two-parent merge and matching Actions SHA
are required; changed workspace in a feature PR is rejected. Development pushes
remain subject to privacy review. `main`, release branches, unknown identity,
public mode and nested installations never receive the inheritance exception.

## Filtered Publication
Feature PRs target `dev`. Completed, reviewed product changes reach `main` via
a separate source-only release branch based explicitly on current `main`, then
a PR to `main`. Never merge `dev` directly into `main`: deleting workspace files
after a merge does not remove their history. No workspace commit enters main
ancestry through this route.

Select only reviewed source-only commits. Mixed source/runtime commits require
a reviewed product-only patch rather than a blind cherry-pick. Review all product
paths, including new files and deletions, against the accepted scope. Preserve
main's workspace ignore rule; review other shared `.gitignore` changes individually
instead of discarding legitimate product exclusions.

Before publication, verify the release branch has no tracked workspace, inspect
its complete diff and ancestry, perform semantic QA and applicable full source
validation. Confirm completed product parity with `dev`; unfinished development
may remain ahead and must not be published as finished. After release, synchronize
source-only main history back to dev without replacing local runtime.

Local commits follow phase-commit-policy.md and exact reviewed staging. This
contract grants no automatic push, PR, merge to main, branch deletion, production
action or final-owner-yes. Published snapshots and green scripts are supporting
evidence only, not current technical or owner acceptance.
