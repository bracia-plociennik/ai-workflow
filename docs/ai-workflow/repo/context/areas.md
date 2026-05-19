# Main Repository Areas

| Area | Purpose | Notes |
| --- | --- | --- |
| Root entrypoints | Internal execution contract, human runbook, and target shim template | In target repos, only `root-agents.template.md` is copied or merged as root `AGENTS.md`; `HUMANS.md` stays available at `ai-workflow/HUMANS.md`. |
| `docs/ai-workflow/ai/` | Workflow source and templates | Must stay generic and updateable from upstream. |
| `docs/ai-workflow/repo/` | Repo-specific runtime docs | Contains this repo's context, intake, status, and memory. |
| `root-agents.template.md` | Target-repository entrypoint shim | Delegates from target root `AGENTS.md` to `ai-workflow/AGENTS.md`. |
| `docs/ai-workflow/projects/EXAMPLE/` | Example project workspace | Demonstrates artifact layout only. |
| `docs/ai-workflow/humans/EXAMPLE/` | Example human-facing docs | Demonstrates summaries, decisions, runbooks, audits, approvals, and human plans. |
