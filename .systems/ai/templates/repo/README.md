# Repo Runtime Templates

Templates for target-repository runtime artifacts under `workspace/repo/`.

Use these when installing or refreshing `ai-workflow` in another repository:

- `context.template.md` -> `workspace/repo/core/context.md`
- `context-readme.template.md` -> `workspace/repo/context/README.md`
- `context-entry.template.md` -> `workspace/repo/context/<entry>.md`
- `legacy.template.md` -> `workspace/repo/core/legacy.md`
- `repo-intake.template.md` -> `workspace/repo/core/repo-intake.md`
- `status.template.md` -> `workspace/repo/core/status.md`
- `memory.template.md` -> `workspace/repo/core/memory.md`
- `memory-readme.template.md` -> `workspace/repo/memory/README.md`
- `date-memory-entry.template.md` -> `workspace/repo/memory/YYYY-MM-DD-short-kebab-title.md`

Keep these templates generic. Do not store repository-specific facts in `.systems/ai/templates/repo/`.
