# Templates

Reusable templates for repo runtime, workflow, project, micro-project, human, autopilot, memory, external memory, and system insights artifacts.

Use these as starting points when a target repository needs repo runtime files, project phase artifacts, QA evidence, escalation records, ledgers, decisions, or human-facing docs.

## Template Groups

- `root-agents.template.md` - target-repository root `AGENTS.md` shim that delegates to `ai-workflow/AGENTS.md`.
- `workspace/` - bootstrap templates used by `.systems/scripts/init-workspace` to create `AI_WORKFLOW_WORKSPACE_HOME`.
- `repo/` - templates for target-repo runtime files under `AI_WORKFLOW_WORKSPACE_HOME/repo/`.
- `workflow/` - templates for artifacts produced by `.systems/ai/workflow/*` phases.
- `autopilot/` - runtime autopilot, QA evidence, escalation, and decision templates.
- `projects/` - project workspace support-file, context, memory, planning router, task, micro-task, and review router templates.
- `micro-projects/` - repo-level low-risk micro-project templates.
- `reviews/` - project-local review artifact templates.
- `humans/` - owner/operator-facing document templates.
- `memory/` - template maintenance memory templates.
- `external-memory/` - AI Workflow improvement memory templates.
- `system-insights/` - anonymized cross-project operating insight templates.

Project-specific copies should be written under the relevant `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/...` or `AI_WORKFLOW_WORKSPACE_HOME/humans/<project>/...` directory, not edited in place here.

Repo-specific copies should be written under `AI_WORKFLOW_WORKSPACE_HOME/repo/`, not edited into `.systems/ai/`.
