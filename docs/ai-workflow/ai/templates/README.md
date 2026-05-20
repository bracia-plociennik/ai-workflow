# Templates

Reusable templates for repo runtime, workflow, project, micro-project, human, autopilot, memory, and external memory artifacts.

Use these as starting points when a target repository needs repo runtime files, project phase artifacts, QA evidence, escalation records, ledgers, decisions, or human-facing docs.

## Template Groups

- `root-agents.template.md` - target-repository root `AGENTS.md` shim that delegates to `ai-workflow/AGENTS.md`.
- `repo/` - templates for target-repo runtime files under `docs/ai-workflow/repo/`.
- `workflow/` - templates for artifacts produced by `docs/ai-workflow/ai/workflow/*` phases.
- `autopilot/` - runtime autopilot, QA evidence, escalation, and decision templates.
- `projects/` - project workspace support-file, context, memory, planning router, task, micro-task, and review router templates.
- `micro-projects/` - repo-level low-risk micro-project templates.
- `reviews/` - project-local review artifact templates.
- `humans/` - owner/operator-facing document templates.
- `memory/` - template maintenance memory templates.
- `external-memory/` - universal AI Workflow improvement memory templates.

Project-specific copies should be written under the relevant `docs/ai-workflow/projects/<project>/...` or `docs/ai-workflow/humans/<project>/...` directory, not edited in place here.

Repo-specific copies should be written under `docs/ai-workflow/repo/`, not edited into `docs/ai-workflow/ai/`.
