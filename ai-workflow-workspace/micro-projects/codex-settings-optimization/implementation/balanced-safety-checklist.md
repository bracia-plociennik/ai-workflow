# Balanced Safety Implementation Checklist

Status: candidate checklist only.

Do not apply these settings automatically. Use this checklist as the owner-approved execution guide for a later side task.

## Safety Boundary

- [ ] Confirm this is the intended profile: `balanced safety`.
- [ ] Confirm no Codex Memories experiment is planned.
- [ ] Confirm no Chronicle experiment is planned.
- [ ] Confirm no hooks are being introduced.
- [ ] Confirm existing hooks are not silently active before calling hooks "off": review `/hooks`, `~/.codex/hooks.json`, project `.codex/hooks.json`, inline `[hooks]` tables, and plugin-bundled hooks if available.
- [ ] Confirm local environments remain manual.
- [ ] Confirm trusted project paths are not pruned in this pass.
- [ ] Confirm real `~/.codex/config.toml` has been reviewed before any edit.
- [ ] Confirm a backup or copy of real `~/.codex/config.toml` exists before any edit.

## General UI

- [ ] Work mode: `For coding`.
- [ ] Default permissions: `on`.
- [ ] Auto-review: `on`.
- [ ] Full access: `off`.
- [ ] File open destination: keep current value.
- [ ] Language: `Auto Detect`.
- [ ] Bottom panel: keep current value.
- [ ] Default terminal location: keep current value.
- [ ] Prevent sleep while running: `on`.
- [ ] Speed: `Standard`.
- [ ] Code review delivery: `Inline`.
- [ ] Follow-up behavior: `Steer`.
- [ ] Default to projectless chat: `off`.
- [ ] Completion notifications: keep `Only when unfocused`.
- [ ] Permission notifications: `on`.
- [ ] Question notifications: `on`.
- [ ] Show context window usage: `on`, if the setting is available.

## Configuration UI

- [ ] Approval policy: `On request`.
- [ ] Sandbox settings: `Workspace write`.
- [ ] Allow network access: `off`.
- [ ] Workspace dependencies: installed/available.
- [ ] Codex dependencies: `on`.

## Personalization UI

- [ ] Personality: `Pragmatic`.
- [ ] Custom instructions: keep a short safety shim that delegates to repo state and `AGENTS.md`.
- [ ] Custom instructions: do not paste the full AI Workflow contract here.
- [ ] Memories: `off`.
- [ ] Chronicle: `off`.
- [ ] Skip tool-assisted chats: no change while Memories remain off.

## MCP UI

- [ ] `openaiDeveloperDocs`: enabled.
- [ ] `figma`: disabled by default; enable only for Figma tasks.
- [ ] `node_repl`: disabled by default; enable only when browser/app automation or a specific tool flow requires it.
- [ ] Before disabling `node_repl`, note that current Node REPL env advertises both in-app browser and Chrome automation support; `@Browser`/`@Chrome` flows may require re-enabling it.
- [ ] Do not delete MCP server definitions; disable them so they can be re-enabled intentionally.
- [ ] Do not add bearer tokens or static headers in this pass.

## Browser And Computer Use UI

- [ ] Google Chrome control: keep enabled.
- [ ] Any App control: disable.
- [ ] Locked use: `off`.
- [ ] Always-allowed apps: keep empty.
- [ ] Chrome website approvals: `Always ask`.
- [ ] Chrome history approvals: `Always ask`.
- [ ] Chrome downloads approvals: `Always ask`.
- [ ] Chrome uploads approvals: `Always ask`.
- [ ] Full CDP access: `off`.
- [ ] Keep only necessary localhost site permissions; do not add broad public-site allow rules.

## Connections UI

- [ ] Remote control for current iOS device: keep enabled.
- [ ] Control other devices: keep unset.
- [ ] SSH connections: keep unset.

## Git UI

- [ ] Branch prefix: `codex/`.
- [ ] Pull request merge method: keep `Merge`.
- [ ] Show PR icons in sidebar: no required change.
- [ ] Always force push: `off`.
- [ ] Create draft pull requests: `on`.
- [ ] Automatically delete old worktrees: `on`.
- [ ] Auto-delete limit: `15`.
- [ ] Commit instructions: keep strict current rules.
- [ ] Pull request instructions: keep strict current rules.

## Environments UI

- [ ] Local environment for `ai-workflow`: keep not configured.
- [ ] Setup script: do not add.
- [ ] Cleanup script: do not add.
- [ ] Actions: do not add.

## Worktrees UI

- [ ] Keep worktrees available as a per-task execution mode.
- [ ] Do not make every task a worktree by default.
- [ ] Use worktrees for parallel work only when write sets, status updates, memory writes, and branch ownership are isolated.
- [ ] Prefer Codex-managed worktrees for background tasks.
- [ ] Use handoff to Local when inspection, local IDE validation, or a single foreground dev server is required.

## config.toml Patch Scope

Safe candidate config changes:

- [ ] Use `implementation/config.template.toml` as the clean from-scratch balanced-safety baseline.
- [ ] Treat `implementation/legacy/config.template.legacy-snapshot.toml` as historical context only.
- [ ] Set `model = "gpt-5.5"` and `model_reasoning_effort = "high"` unless the owner chooses a different model/cost profile.
- [ ] Set `approval_policy = "on-request"`.
- [ ] Set `approvals_reviewer = "auto_review"`.
- [ ] Set `sandbox_mode = "workspace-write"`.
- [ ] Set `web_search = "cached"`.
- [ ] Add `[sandbox_workspace_write].network_access = false`.
- [ ] Add `[sandbox_workspace_write].writable_roots = []`.
- [ ] Add `[features].memories = false`.
- [ ] Add `[features].browser_use_full_cdp_access = false`.
- [ ] Add `[mcp_servers.figma].enabled = false`.
- [ ] Add `[mcp_servers.node_repl].enabled = false`.
- [ ] Keep `[mcp_servers.openaiDeveloperDocs]` enabled.

Do not include in config patch for this pass:

- [ ] Do not set `[features].computer_use = false`, because the owner wants Chrome control available.
- [ ] Do not set `[features].hooks = false`, because the decision is to add no hooks, not necessarily to block all hook sources.
- [ ] Do not interpret missing new hook definitions as proof that hooks cannot run; verify active hook sources separately.
- [ ] Do not add local environment setup/cleanup scripts.
- [ ] Do not edit project trust paths.
- [ ] Do not copy `projects.*`, `marketplaces.*`, plugin timestamps, per-path editor preferences, or machine-specific notification paths from the legacy snapshot unless intentionally preserving the current real config.

## Post-Change Verification For Later Side Task

When a future side task applies changes, verify:

- [ ] Codex settings UI reflects the requested values.
- [ ] `~/.codex/config.toml` parses as TOML.
- [ ] A new Codex thread shows expected MCP availability: OpenAI docs available, Figma disabled until enabled, Node REPL disabled until enabled.
- [ ] If `@Browser`, `@Chrome`, or app/browser automation fails after disabling `node_repl`, re-enable `node_repl` for that task and record the dependency.
- [ ] `/hooks` or the app hook review surface shows no unexpected active user/project/plugin hooks for this profile.
- [ ] Computer Use still permits Chrome control but not broad Any App control.
- [ ] AI Workflow repo still opens with `approval_policy = on-request` and `sandbox_mode = workspace-write`.
- [ ] No tracked repo files changed.
- [ ] No workspace project artifacts were accidentally promoted to tracked source.

## Rollback Notes

- Re-enable `figma` MCP if a Figma task starts.
- Re-enable `node_repl` MCP if browser/app automation needs it.
- Re-enable Any App control only for a scoped GUI task that cannot use Chrome, Browser, a connector, or an MCP server.
- Remove `[features].memories = false` only if owner starts a Memories trial.
- Keep Chronicle off unless owner starts a separate privacy-reviewed trial.
