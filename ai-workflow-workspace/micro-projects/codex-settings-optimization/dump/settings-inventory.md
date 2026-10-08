# Settings Inventory

Source scope: screenshots and `context/config.template.toml` from 2026-06-17.

This inventory records observed settings only. It does not apply changes and does not assert that screenshot values are globally current outside this local Codex installation.

## General

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Work mode | For coding | Good fit for repo-governed work. |
| Default permissions | on | Useful, but must remain bounded by AGENTS and workflow gates. |
| Auto-review | on | Supports quality gates and review-first culture. |
| Full access | off | Correct default for AI Workflow. |
| File open destination | VS Code | Low-risk preference. |
| Language | Auto Detect | Good for mixed Polish/English workflow. |
| Show in menu bar | on | Preference only. |
| Bottom panel | on | Preference only. |
| Default terminal location | Bottom | Preference only. |
| Prevent sleep while running | on | Useful for longer validation/autopilot runs. |
| Speed | Standard | Safer default than aggressive speed for workflow-governed work. |
| Code review delivery | Inline | Aligns with actionable review findings. |
| Context window usage | off | Weakness: less visibility into long-run context pressure. |
| Follow-up behavior | Queue | Good for long-running work and interruption handling. |
| Require cmd+enter for long prompts | off | Convenience tradeoff; accidental sends remain possible. |
| Projectless chat default | off | Good: encourages project-scoped execution. |
| Dictation | mostly off | No material workflow impact. |
| Completion notifications | Only when unfocused | Good signal/noise balance. |
| Permission notifications | on | Useful for review of escalations. |
| Question notifications | on | Useful for blocked decisions. |

## Profile

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Account/profile | Pro | Enables higher usage, not a workflow contract. |
| Lifetime tokens | 5.4B | Usage signal only. |
| Peak tokens | 276.6M | Indicates heavy long-context use. |
| Longest task | 1h30m | Supports need for durable status, checkpoints, and context hygiene. |
| Reasoning usage | Extra High 49% | AI Workflow benefits from high reasoning on planning/review, but not every small task needs it. |
| Skills explored | 16 | Skill system is active enough to justify skill governance. |
| Most used plugins | Figma, Browser, browser-use, figma-implement-design | Confirms visual/product work is a major use case. |

## Appearance

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Theme | System | Preference only. |
| Light/Dark theme | Codex | Preference only. |
| Accent/background/foreground | default Codex colors | Preference only. |
| Translucent sidebar | on | Preference only. |
| Contrast | light 45, dark 60 | Potential readability tuning only. |
| Pointer cursors | on | Useful for UI clarity. |
| Reduce motion | System | Good accessibility default. |
| UI font size | 14 | Preference only. |
| Code font size | 12 | Could be raised if review accuracy suffers. |
| Diff markers | Color | Useful for review scanning. |
| Font smoothing | on | Preference only. |
| Dock icon / companion UI | default | No workflow impact. |

## Configuration

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Approval policy | `on-request` | Best baseline for low/medium workflow work with explicit escalation. |
| Sandbox mode | `workspace-write` | Best baseline for repo work without global write access. |
| Network access | off | Correct default; escalate only when task evidence requires network. |
| Workspace dependencies | version `26.614.11602` | Useful for document/spreadsheet/PDF work. |
| Codex dependencies | on | Good default for bundled tooling. |
| Diagnose/reinstall dependencies | available | Useful recovery option, not part of normal flow. |

## Personalization

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Personality | Pragmatic | Fits AI Workflow execution style. |
| Custom instructions | Safety shim that points to repo state, AGENTS, gates, evidence, write conditions | Good. Keep short; avoid duplicating full AGENTS. |
| Memories | off | Owner decision: continuity benefit vs privacy/control. |
| Chronicle | off | Owner decision: research preview and broader memory implications. |
| Skip tool-assisted chats | off | Only relevant if memories are enabled. |

## Usage

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Plan | Pro plan, 5x more usage than Plus, GPT-5.5 Pro label visible | Treat as local account state, not a workflow guarantee. |
| Credits | $0, auto-reload available | Billing setting; owner-only decision. |
| General 5 hour limit | 100% left | Operational signal only. |
| General weekly limit | 68% left | Long projects may need usage awareness. |
| GPT-5.3-Codex-Spark limits | 100% left | Model-specific usage signal only. |

## MCP

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Figma MCP | enabled, URL `http://127.0.0.1:3845/mcp`, no custom headers | Good for design work; local URL reduces exposure. |
| Node REPL MCP | enabled, local Codex app command, browser backends `chrome,iab`, working directory `~/code` | Powerful; keep enabled only with sandbox and command discipline. |
| OpenAI Developer Docs MCP | enabled, URL `https://developers.openai.com/mcp`, no custom headers | Useful for current OpenAI product/API docs. |
| Plugin app server | `codex_apps` visible | Supports connectors/plugins; evaluate per plugin. |

## Browser And Computer Use

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Any App control | on | Powerful; should remain approval-governed. |
| Google Chrome control | on and connected | Useful for GitHub/UI verification and web testing. |
| Locked use | off | Good; avoids blanket unattended control. |
| Always-allowed apps | none | Correct default. |
| Website approval | Always ask | Correct default. |
| History/downloads/uploads | Always ask | Correct default. |
| Site permission | `http://127.0.0.1:3109` allow browsing | Local exception only; should be periodically reviewed. |
| Full CDP access | off | Correct default. |
| Dedicated Browser screenshot | not present in context | Treat Browser section as not fully captured; do not infer beyond available Computer Use/Chrome screenshots. |

## Hooks

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Hooks | none configured | Good for safety now; candidates exist for future non-destructive readiness checks. |

## Connections

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Control this Mac | one iOS device can control this Mac; discovery/control enabled; keep-awake while plugged in enabled | Convenience vs privacy/security tradeoff. Owner decision if this should stay on. |
| Control other devices | not set up | No current effect. |
| SSH connections | none | Good default unless remote development becomes explicit scope. |

## Git

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Branch prefix | `codex/` | Matches app/repo convention. |
| PR merge method | Merge | Consistent with preserving commits; owner can choose squash separately. |
| Show PR icons in sidebar | off | Preference only. |
| Always force push | off | Correct safety default. |
| Create draft pull requests | on | Good safety default for reviewable changes. |
| Auto-delete old worktrees | on | Useful cleanup, but be aware of evidence retention. |
| Auto-delete limit | 15 | Reasonable default. |
| Commit instructions | strict, repo-relevant, no AI/tool mentions, coherent commits | Aligns with AI Workflow commit gate. |
| PR instructions | strict template with validation, risk, checklist, no hidden skipped tests | Aligns with AI Workflow PR contract. |

## Environments

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Project environment | `ai-workflow` project path visible | Current project recognized. |
| Local environment | screenshot says no local environment configured for project yet | No active environment automation. |
| Example setup script | `cd "$CODEX_WORKTREE_PATH"`, `pip install -r requirements.txt`, `npm install`, `./run/setup.sh` | Useful template only; unsafe to apply without repo-specific validation. |
| Example cleanup script | `docker compose down --remove-orphans`, `rm -rf .cache/tmp` | Potentially destructive; must be owner-approved and repo-specific. |
| Actions | none | Candidate for future safe local toolbar commands. |

## Worktrees

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| Worktrees | none yet | Potential support for parallel low-overlap work, but must follow AI Workflow parallel-work policy. |

## Config Template Highlights

| Setting | Observed/current | AI Workflow note |
| --- | --- | --- |
| `personality` | `pragmatic` | Good fit. |
| `model` | `gpt-5.5` | Treat as template/local desired state; verify availability before applying. |
| `model_reasoning_effort` | `xhigh` | Good for planning/review; may be excessive for small micro-tasks. |
| `sandbox_mode` | `workspace-write` | Good baseline. |
| `approval_policy` | `on-request` | Good baseline. |
| `approvals_reviewer` | `guardian_subagent` | Stronger safety if available; verify current app support before relying on it. |
| Plugins | documents, spreadsheets, presentations, figma, github, canva, codex-security, notion, pdf, browser | Useful, but should be enabled based on actual work domains. |
| Trusted project paths | many local project paths | Convenience vs broad trust surface; should be periodically pruned. |
