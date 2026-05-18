# version.md

| Field | Value |
| --- | --- |
| Workflow version | `0.5.0` |
| Compatible with | Codex CLI, Codex app, ChatGPT agent as optional reviewer |
| Last process migration | `2026-05-18` |
| Naming standard | lowercase kebab-case |
| Phase file standard | `phase-<number>-<name>.md` |

## Compatibility Notes

- `AGENTS.md` is a short router.
- `HUMANS.md` is the long human runbook.
- `docs/ai-workflow/` is the workflow-owned documentation namespace.
- `docs/ai-workflow/ai/` is template-owned policy and workflow source.
- `docs/ai-workflow/ai/skills/` stores optional task-specific workflow skills.
- `docs/ai-workflow/repo/` stores repo-specific runtime facts.
- `docs/ai-workflow/projects/<project>/` stores project-specific runtime facts.
- `scripts/ai-workflow/` is the workflow-owned validator namespace.
- Existing target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `scripts/`, and `.github/` require merge, not overwrite.
