# Repo Runtime Templates

Templates for target-repository runtime artifacts under `AI_WORKFLOW_WORKSPACE_HOME/repo/`.

Use these when installing or refreshing `ai-workflow` in another repository:

- `context.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`
- `context-readme.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/context/README.md`
- `context-entry.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/context/<entry>.md`
- `legacy.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md`
- `repo-intake.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`
- `status.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md`
- `memory.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md`
- `memory-readme.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/README.md`
- `date-memory-entry.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/YYYY-MM-DD-short-kebab-title.md`

Keep these templates generic. Do not store repository-specific facts in `.systems/ai/templates/repo/`.
