# Helper Questions

Use these before applying any Codex settings change.

## Minimum Decisions

1. Which operating profile should be the default: `balanced safety`, `high autonomy`, or `privacy-first`?
2. Should Codex memories remain off, or should we run an owner-approved trial with explicit capture boundaries?
3. Should Chronicle remain off, or is the research-preview value worth testing?
4. Should Any App control stay enabled, or should desktop automation be limited to Chrome/in-app browser only?
5. Should remote control of this Mac stay enabled for the iOS device?
6. Should Node REPL MCP stay always enabled, or only enabled for tasks that need browser/app automation?
7. Should Figma MCP and OpenAI Docs MCP stay always enabled?
8. Should context-window usage be turned on for long AI Workflow projects?
9. Should any hooks be introduced, and if yes, which lifecycle event should they support?
10. Should local environment setup/cleanup be configured for `ai-workflow`, or kept manual?
11. Should Codex worktrees be adopted for parallel work, and under what write-set/status/memory rules?
12. Should trusted project paths in the config template be pruned?

## Privacy Questions

- Are global Codex memories acceptable if project/client data is excluded?
- Should tool-assisted chats be excluded from any memory capture?
- Which data must never enter app-level memory: client names, repo names, screenshots, credentials, production URLs, billing data, private strategy?
- Should remote-control discovery be off unless actively needed?
- Should Chrome history/download/upload access always ask, even in high-autonomy mode?

## Autonomy Questions

- Which tasks are safe for lower-friction approvals?
- Which tasks must always remain approval-gated: network, installs, browser downloads/uploads, GUI control, file writes outside workspace, push/PR, hooks, environment cleanup?
- Should `xhigh` reasoning be default for all workflow work, or only planning/review/architecture/security?
- Should draft PRs remain default, or should mature low-risk side tasks create ready PRs?

## Tooling Questions

- Which MCP servers are essential for daily work?
- Which plugins are stale or rarely used enough to disable?
- Is the local Figma MCP URL stable enough for default use?
- Does OpenAI Docs MCP need to be always enabled, or can it be task-triggered?
- Should browser site exceptions be limited to localhost dev servers created in the current task?

## Workflow Questions

- Should context-window usage become a recommended setting for implementation-range autopilot and long micro-projects?
- Should hooks enforce only advisory checks, or should any hook block actions?
- Which non-destructive hook would add the most value first: pre-commit readiness reminder, validation command suggestion, or workspace ignore check?
- Should local environment setup scripts be generated from repo intake rather than hand-written in Codex settings?
- Should worktrees create separate AI Workflow workspace state, or only be used when status/memory writes are disabled?

## Follow-Up Routing

- Settings application: owner-approved side task.
- Hook design: workflow-maintenance micro-project.
- Worktree policy: workflow-maintenance micro-project.
- Memory/Chronicle trial: owner-approved experiment with privacy criteria.
- Environment setup scripts: repo-specific micro-project with rollback and safety review.
