# Main Repository Areas

| Area | Purpose | Notes |
| --- | --- | --- |
| Root entrypoints | Execution contract and human runbook | In target repos, existing `AGENTS.md`, `HUMANS.md`, and `README.md` are merged, not overwritten. |
| `docs/ai-workflow/ai/` | Workflow source and templates | Must stay generic and updateable from upstream. |
| `docs/ai-workflow/repo/` | Repo-specific runtime docs | Contains this repo's context, intake, status, and memory. |
| `docs/ai-workflow/projects/EXAMPLE/` | Example project workspace | Demonstrates artifact layout only. |
| `docs/ai-workflow/humans/EXAMPLE/` | Example human-facing docs | Demonstrates summaries, decisions, runbooks, audits, approvals, and human plans. |
