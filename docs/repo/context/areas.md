# Main Repository Areas

| Area | Purpose | Notes |
| --- | --- | --- |
| Root entrypoints | Internal execution contract, human runbook, and target shim template | In target repos, only `docs/ai/templates/root-agents.template.md` is copied or merged as root `AGENTS.md`; `HUMANS.md` stays available at `ai-workflow/HUMANS.md`. |
| `docs/ai/` | Workflow source and templates | Must stay generic and updateable from upstream. |
| `docs/repo/` | Repo-specific runtime docs | Contains this repo's context, intake, status, and memory. |
| `docs/ai/templates/root-agents.template.md` | Target-repository entrypoint shim | Delegates from target root `AGENTS.md` to `ai-workflow/AGENTS.md`. |
| `docs/projects/EXAMPLE/` | Example project workspace | Demonstrates artifact layout only. |
| `docs/humans/EXAMPLE/` | Example human-facing docs | Demonstrates summaries, decisions, runbooks, audits, approvals, and human plans. |
