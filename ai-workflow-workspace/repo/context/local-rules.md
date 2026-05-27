# Local Operating Rules

- Do not put repo-specific facts in root entrypoints or `.systems/ai/`.
- Put global repo facts in `ai-workflow-workspace/repo/context/`, `ai-workflow-workspace/repo/core/repo-intake.md`, `ai-workflow-workspace/repo/core/status.md`, and detailed repo memory entries under `ai-workflow-workspace/repo/memory/`.
- Keep `ai-workflow-workspace/repo/core/context.md` as the router/index for repo context entries.
- Put project-specific execution artifacts in `ai-workflow-workspace/projects/<project>/`.
- Put human-facing coordination artifacts in `ai-workflow-workspace/humans/<project>/`.
