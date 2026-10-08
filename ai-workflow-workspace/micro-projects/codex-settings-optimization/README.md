# Codex Settings Optimization

Workspace-only micro-project for evaluating Codex app settings against AI Workflow operating needs.

## Scope

- Source data: screenshots and `config.template.toml` in `context/`.
- Output: inventory, idea validation, decision matrix, and owner questions.
- No real Codex settings are changed.
- No tracked source files are changed.

## Artifacts

- `micro-project.md` - execution record, evidence, and acceptance status.
- `dump/settings-inventory.md` - observed settings inventory by Codex settings section.
- `idea-validation.md` - workflow-style validation of the optimization idea.
- `decision-matrix.md` - setting-level options for `balanced safety`, `high autonomy`, and `privacy-first`.
- `helper-questions.md` - owner questions needed before applying any setting changes.
- `implementation/balanced-safety-checklist.md` - full candidate checklist for a later owner-approved settings change.
- `implementation/config.template.toml` - clean from-scratch balanced-safety candidate config template; artifact only, not applied.
- `implementation/legacy/config.template.legacy-snapshot.toml` - legacy full snapshot preserved for comparison only, not recommended as the active template.
- `implementation/optimized-instructions.md` - optimized commit, PR, and custom instruction candidates.
- `implementation/final-smoke-test-status.md` - final read-only smoke test result after owner-applied settings.

## Current Recommendation

Use `balanced safety` as the working default until owner decisions resolve autonomy, memory, privacy, browser, MCP, hooks, and worktree tradeoffs.

Any real configuration change should be handled as a separate owner-approved side task or micro-project.
