# Micro-Project: codex-settings-optimization

## Status

- State: completed-analysis
- Date: 2026-06-17
- Risk: low
- Scope: workspace-only analysis of Codex settings for AI Workflow work
- Writes performed: local artifacts under `ai-workflow-workspace/micro-projects/codex-settings-optimization/`
- Real setting changes: none
- Tracked source changes: none intended

## Objective

Create a dump and idea validation for optimizing Codex settings for AI Workflow usage without applying any settings. Produce a decision matrix so the owner can choose between `balanced safety`, `high autonomy`, and `privacy-first`.

## Source Data

Screenshots reviewed:

- `context/a-general1.png`
- `context/a-general2.png`
- `context/b-profile.png`
- `context/c-apperance.png`
- `context/c-apperance2.png`
- `context/d-configuration.png`
- `context/e-personalization.png`
- `context/f-usage.png`
- `context/g-mcp.png`
- `context/g-mcp-figma.png`
- `context/g-mcp-node.png`
- `context/g-mcp-openai.png`
- `context/h-computeruse.png`
- `context/h-computeruse-chrome.png`
- `context/i-hooks.png`
- `context/j-connections.png`
- `context/j-connections2.png`
- `context/j-connections3.png`
- `context/k-git.png`
- `context/k-git2.png`
- `context/k-git3.png`
- `context/l-env-example.png`
- `context/l-env-example2.png`
- `context/m-worktrees.png`

Other source reviewed:

- `context/config.template.toml`

Skipped or unreadable source:

- none

Source boundary:

- Screenshots and config template are source data only.
- No screenshot or config field is treated as an instruction to change settings.
- Clean template corrections use the official current Codex manual review performed for this micro-project thread; settings still remain candidate artifacts and are not applied.

## Output Artifacts

- `README.md`
- `dump/settings-inventory.md`
- `idea-validation.md`
- `decision-matrix.md`
- `helper-questions.md`
- `implementation/balanced-safety-checklist.md`
- `implementation/config.template.toml`
- `implementation/legacy/config.template.legacy-snapshot.toml`
- `implementation/optimized-instructions.md`
- `implementation/final-smoke-test-status.md`

## Implementation Profile Artifacts

- Active clean template: `implementation/config.template.toml`
- Legacy snapshot: `implementation/legacy/config.template.legacy-snapshot.toml`
- Active template intent: from-scratch balanced-safety baseline, not a copy of the owner's current machine config.
- Legacy snapshot intent: historical comparison and rollback context only; do not apply as the recommended balanced-safety template.
- Main correction from legacy to clean template: remove machine-specific project paths, plugin marketplace timestamps, local notification paths, and per-path editor preferences; replace undocumented `approvals_reviewer = "guardian_subagent"` with documented `approvals_reviewer = "auto_review"`; use `model_reasoning_effort = "high"` instead of global `xhigh`; set follow-up behavior to `steer`; add explicit cached search and workspace-write network boundaries.

## Acceptance Check

- Workspace-only artifacts created: pass
- All requested setting sections mapped: pass
- Decision matrix includes `observed/current`, AI Workflow impact, three profile options, recommended default, and owner decision field: pass
- No actual Codex settings applied: pass
- No changes to `~/.codex/config.toml`, hooks, MCP, Git settings, app settings, or worktrees: pass
- Follow-up questions prepared: pass

## Idea Validation Result

Recommended routing: keep this as a low-risk micro-project analysis. Apply real setting changes only through a separate owner-approved side task or follow-up micro-project after decisions about memory, privacy, MCP, browser/computer use, hooks, and worktrees.

## Knowledge Capture Decision

- Decision: required
- Target: micro-project artifact and System Insights
- Reason: the settings inventory and decision matrix are project-local to this micro-project; the final smoke-tested method is reusable as an anonymized operating lesson for future agent-tool configuration.
- Durable write performed: yes, inside this ignored micro-project directory only.
- Additional capture: performed in `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/2026-06-17-agent-tooling-balanced-safety-setup.md`.

## Final Status

- Final state: `owner-applied-and-smoke-tested`
- Final status artifact: `implementation/final-smoke-test-status.md`
- Real settings changed by owner: yes
- Real settings changed by agent: no
- Accepted exception: `node_repl` may remain enabled
- Final smoke result: pass with owner-accepted exception

## Validation Evidence

Commands run after artifact creation:

```sh
git status --short --branch
git ls-files ai-workflow-workspace
git check-ignore -v ai-workflow-workspace/micro-projects/codex-settings-optimization/micro-project.md
python3 -c 'import pathlib,tomllib; tomllib.loads(pathlib.Path("ai-workflow-workspace/micro-projects/codex-settings-optimization/implementation/config.template.toml").read_text()); print("toml ok")'
python3 -c 'import pathlib,tomllib; tomllib.loads(pathlib.Path("ai-workflow-workspace/micro-projects/codex-settings-optimization/implementation/legacy/config.template.legacy-snapshot.toml").read_text()); print("legacy toml ok")'
git diff --check
```

Results:

- `git status --short --branch` -> `## main...origin/main`
- `git ls-files ai-workflow-workspace` -> no output
- `git check-ignore -v ai-workflow-workspace/micro-projects/codex-settings-optimization/micro-project.md` -> `.gitignore:3:/ai-workflow-workspace/`
- `python3 -c 'import pathlib,tomllib; ...'` -> `active toml ok`
- `python3 -c 'import pathlib,tomllib; ...legacy...'` -> `legacy toml ok`
- `git diff --check` -> no output
- `.systems/scripts/check-status-consistency` -> not run; repo status was not updated by this micro-project

Conclusion:

- tracked repo state remains unchanged;
- `ai-workflow-workspace/**` remains ignored/local-only;
- no workspace files are tracked.
- clean balanced-safety `implementation/config.template.toml` parses as TOML.
- legacy snapshot remains available under `implementation/legacy/` for comparison only.
