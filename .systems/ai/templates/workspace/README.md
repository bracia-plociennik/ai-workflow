# Workspace Templates

## Purpose

These templates create the target-owned `AI_WORKFLOW_WORKSPACE_HOME` directory, normally `ai-workflow-workspace/` beside the nested `ai-workflow/` clone.

The public `ai-workflow` template does not track active runtime workspace files on `main`. Use `.systems/scripts/init-workspace` to create a fresh workspace in a target repository.

## Template Families

- `workspace-readme.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/README.md`
- `repo/` -> workspace-level repo runtime entrypoints and README files.
- `projects/` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/README.md`
- `humans/` -> `AI_WORKFLOW_WORKSPACE_HOME/humans/README.md`
- `micro-projects/` -> `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/README.md`
- `external-memory/` -> `AI_WORKFLOW_WORKSPACE_HOME/external-memory/`
- `skills/` -> `AI_WORKFLOW_WORKSPACE_HOME/skills/README.md`

Do not edit these templates from a target repository. Target-specific facts belong in `AI_WORKFLOW_WORKSPACE_HOME`.
