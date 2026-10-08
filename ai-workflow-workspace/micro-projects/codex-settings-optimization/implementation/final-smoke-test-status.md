# Final Smoke Test Status

- Date: `2026-06-17`
- Micro-project: `codex-settings-optimization`
- Profile: `balanced safety`
- Status: `owner-applied-and-smoke-tested`
- Real Codex settings changed by owner: `yes`
- Real Codex settings changed by agent: `no`
- Tracked repository changes: `none`

## Scope

Final read-only smoke test after owner applied:

- clean balanced-safety config;
- optimized commit instructions;
- optimized pull request instructions;
- global personalization/custom instructions;
- selected UI settings.

## Result

Smoke test result: `pass-with-owner-accepted-node-repl-exception`

No blockers found.

Owner decision:

- `node_repl` may remain enabled.

## Verified Config Values

Observed in real Codex config during smoke test:

- `model = "gpt-5.5"`
- `model_reasoning_effort = "high"`
- `personality = "pragmatic"`
- `approval_policy = "on-request"`
- `approvals_reviewer = "auto_review"`
- `sandbox_mode = "workspace-write"`
- `web_search = "cached"`
- `features.memories = false`
- `features.chronicle = false`
- `features.browser_use_full_cdp_access = false`
- `features.js_repl = false`
- `sandbox_workspace_write.network_access = false`
- `sandbox_workspace_write.writable_roots = []`
- `desktop.followUpQueueMode = "steer"`
- `desktop.reviewDelivery = "inline"`
- `desktop.show-context-window-usage = true`
- `desktop.git-always-force-push = false`
- `desktop.git-create-pull-request-as-draft = true`

## Verified MCP State

- `openaiDeveloperDocs`: `enabled`
- `figma`: `disabled`
- `node_repl`: `enabled`, owner-approved exception

## Verified Instructions

Commit instructions:

- present in real config;
- use global examples;
- include focused-commit and workspace-only artifact boundaries.

Pull request instructions:

- present in real config;
- include summary, context, scope, validation, risks, checklist;
- include `Do not claim PASS without evidence`.

Personalization/custom instructions:

- present in global Codex guidance file;
- include pragmatic senior engineer behavior;
- include supporting-context boundary;
- include AI Workflow-specific contract pointer for repositories that use it.

## Hook And Repo Safety

Hook files checked:

- user hook file: `missing`
- repo hook file: `missing`
- repo `.codex/config.toml`: `missing`

Repository checks:

- `git status --short --branch` -> `## main...origin/main`
- `git ls-files ai-workflow-workspace` -> no output
- `git diff --check` -> no output

## Known Limits

- Some UI-only settings can only be fully confirmed through normal app usage.
- `node_repl` is intentionally enabled despite the initial disabled-by-default recommendation.
- Current setup should be re-reviewed after several days of real work and recorded friction points.

## Knowledge Capture

- Capture decision: `required`
- Capture target: `system-insights`
- Reason: the work produced reusable, anonymized operating lessons for future agent-tool configuration.
- Detailed insight: `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/2026-06-17-agent-tooling-balanced-safety-setup.md`
