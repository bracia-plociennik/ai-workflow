# Workspace Freshness Ledger

## Purpose

The Workspace Freshness Ledger is an advisory report for distinguishing current
repository facts from stale ignored workspace notes. It is evidence, not a
workflow gate, and it never overrides repository state or `AGENTS.md`.

Generate it with:

```sh
.systems/scripts/report-workspace-freshness --output <workspace-or-tmp-path>
```

The output must record observed-at, repository path, branch, HEAD, upstream
HEAD, worktree state, the recorded status/intake baseline, observed baseline,
drift classification (`current|stale|unknown`), recommended action, and
residual uncertainty.

Stale, moved, detached, dirty, or no-upstream states produce advisory findings
only. Existing source-of-truth stop conditions remain unchanged.

Reports must not copy secrets, client data, product data, or full repository
content. They contain command metadata and small factual identifiers only.
