# changelog.md

## 0.5.0 - 2026-05-18

- Moved workflow-owned docs under `docs/ai-workflow/`.
- Moved workflow validators under `scripts/ai-workflow/`.
- Added installation collision policy for existing target repositories.
- Clarified that target-owned `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, `docs/`, `scripts/`, and `.github/` must not be overwritten.
- Added `docs/ai-workflow/ai/skills/` as the reserved space for reusable task-specific workflow skills.

## 0.4.0 - 2026-05-18

- Converted workflow filenames to lowercase kebab-case.
- Added policy docs for operating model, Definition of Done, permissions, risk, commands, prompt injection, rollback, dependencies, and deprecation.
- Converted `AGENTS.md` into a short execution router.
- Added automatic workflow validation scripts and GitHub Actions workflow.
- Added Codex configuration templates.
- Added canonical task ID model and project task index.

## 0.3.0 - 2026-05-18

- Moved repo-specific runtime facts to `docs/ai-workflow/repo/`.
- Added idea validation phase.
- Renamed legacy singular human docs path to `docs/ai-workflow/humans`.
- Made Codex the primary executor with ChatGPT as optional support.
