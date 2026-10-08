# Decision Matrix

Working default: `balanced safety`.

No setting in this matrix has been applied. Each row is a decision candidate for a future owner-approved side task or micro-project.

| Setting | Observed/current | AI Workflow impact | Balanced safety option | High autonomy option | Privacy-first option | Recommended default | Owner decision needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Work mode | For coding | Correct default for repository work | Keep | Keep | Keep | Keep | no |
| Approval policy | `on-request` | Controls escalation and write/network boundaries | Keep | Consider lower friction only for approved low-risk repos | Tighten to more prompts if needed | Keep `on-request` | yes, if changing |
| Sandbox mode | `workspace-write` | Allows repo/workspace edits without global writes | Keep | Keep unless explicit trusted full-access task | Read-only for review-only sessions | Keep `workspace-write` | yes, if changing |
| Network access | off | Prevents accidental external effects | Keep off; escalate per task | Allow in selected trusted workflows | Keep off | Keep off | yes |
| Full access | off | Prevents broad filesystem/control scope | Keep off | Enable only for explicit one-off maintenance | Keep off | Keep off | yes |
| Default permissions | on | Reduces routine prompts, but does not override workflow gates | Keep with AGENTS safety shim | Keep | Consider stricter prompts | Keep | no |
| Auto-review | on | Improves quality discipline | Keep | Keep | Keep | Keep | no |
| Speed | Standard | Balances responsiveness and reliability | Keep Standard | Use faster mode for trivial tasks | Keep Standard or slower | Keep Standard | yes, optional |
| Reasoning effort | Template uses `xhigh`; usage shows Extra High common | Helps planning/review, can waste budget on small tasks | Use high/xhigh for planning, review, architecture; lower for simple side tasks | Keep xhigh broadly | Use high selectively | Selective high/xhigh | yes |
| Model | Template uses `gpt-5.5`; UI plan references GPT-5.5 Pro | Model availability/cost may change | Verify before applying | Use best available for complex work | Use lower-cost/private-safe model where needed | Verify, do not blindly apply | yes |
| Projectless chat | off | Keeps work grounded in repo context | Keep off | Keep off | Keep off | Keep off | no |
| Follow-up behavior | Queue | Protects long-running thread continuity | Keep | Keep | Keep | Keep | no |
| Context window usage | off | Reduces visibility into long-context risk | Turn on if available and not noisy | Turn on | Turn on or monitor manually | Consider turning on | yes |
| Completion/permission/question notifications | enabled/targeted | Good for long work and gated decisions | Keep | Keep | Keep | Keep | no |
| Custom instructions | Short safety shim | Reinforces AGENTS without duplicating full policy | Keep short | Keep short | Keep minimal | Keep short | no |
| Codex memories | off | Could improve continuity but affects privacy/control | Owner-approved experiment only | Enable with capture rules | Keep off | Owner decision | yes |
| Chronicle | off | Research-preview memory/history implications | Keep off unless explicit trial | Consider trial if value is clear | Keep off | Keep off | yes |
| Figma MCP | enabled local URL | High value for design/frontend tasks | Keep enabled | Keep enabled | Enable only when needed | Keep enabled | yes, if privacy-sensitive |
| Node REPL MCP | enabled local command | Powerful local execution and browser control support | Keep enabled with sandbox discipline | Keep enabled | Disable unless needed | Keep enabled but monitored | yes |
| OpenAI Docs MCP | enabled official URL | Useful for current OpenAI/Codex docs | Keep enabled | Keep enabled | Enable when needed only | Keep enabled | yes, if strict privacy/network |
| Plugins/connectors | many enabled | Useful domain coverage, increases surface area | Keep high-value plugins; review stale ones | Keep broad set | Enable only task-needed plugins | Review periodically | yes |
| Browser/Chrome control | on/connected | Needed for GitHub, UI, web testing | Keep with approvals always ask | Keep, maybe add trusted localhost sites | Use in-app browser first; Chrome only when needed | Keep with approvals | yes |
| Full CDP access | off | Powerful browser control | Keep off | Enable only for explicit browser debugging task | Keep off | Keep off | yes |
| Any App control | on | Enables desktop automation, broad surface | Keep but use only with explicit need | Keep | Disable unless actively needed | Owner review | yes |
| Always-allowed apps | none | Prevents silent desktop control | Keep none | Add only specific safe apps | Keep none | Keep none | yes, if changing |
| Remote control this Mac | enabled for one iOS device | Convenience vs privacy/security | Keep only if owner actively uses it | Keep | Disable discovery/control | Owner decision | yes |
| Control other devices / SSH | not set up | No current workflow dependency | Keep unset | Add for remote dev if planned | Keep unset | Keep unset | yes, if changing |
| Hooks | none | Safe; no automatic enforcement | Keep none until concrete safe use case | Add non-destructive readiness hooks | Keep none | Candidate only | yes |
| Git branch prefix | `codex/` | Matches repo/app convention | Keep | Keep | Keep | Keep | no |
| PR merge method | Merge | Preserves commit history | Keep unless repo changes strategy | Could squash for cleaner history | Keep owner-controlled | Keep | yes, if changing |
| Always force push | off | Safety-critical | Keep off | Keep off except explicit repair | Keep off | Keep off | no |
| Draft PRs | on | Safer review posture | Keep on | Off only for mature automated PR flow | Keep on | Keep on | yes, if changing |
| Auto-delete worktrees | on, limit 15 | Useful cleanup, possible evidence loss concern | Keep with limit 15 | Lower limit if many tasks | Disable if forensic retention matters | Keep, review evidence retention | yes |
| Commit instructions | strict | Aligns with commit readiness gate | Keep | Keep | Keep | Keep | no |
| PR instructions | strict | Aligns with PR quality contract | Keep | Keep | Keep | Keep | no |
| Local environments | not configured | Could speed setup but scripts can have side effects | Do not configure yet | Configure after repo-specific safe plan | Keep off | Follow-up micro-project | yes |
| Setup script template | generic install commands | Could run dependency installs | Treat as example only | Build repo-specific script | Avoid automation | Do not apply | yes |
| Cleanup script template | includes Docker shutdown and `rm -rf .cache/tmp` | Potential destructive effects | Do not apply without review | Add after explicit safe cleanup spec | Avoid | Do not apply | yes |
| Worktrees | none active | Could support parallel work if write sets isolated | Plan before enabling | Use for parallel tasks with coordination | Avoid unless necessary | Follow-up plan | yes |
| Trusted project paths | broad template list | Convenience vs trust surface | Prune stale entries | Keep broad trusted workspace | Minimal trusted paths | Review and prune | yes |
| Usage/billing auto-reload | not enabled in screenshot | Billing risk | Owner-only | Owner-only | Owner-only | No change | yes |

## Profile Summaries

### Balanced Safety

- Keep current core security defaults.
- Keep high-value MCP and browser tools available.
- Do not enable memories, Chronicle, hooks, worktrees, environment scripts, network, or full access without separate owner approval.
- Improve observability by considering context-window usage.

### High Autonomy

- Still keep force push and full access off by default.
- Consider selective trusted localhost browser permissions, repo-specific environment setup, and non-destructive hooks.
- Consider worktrees only with explicit write-set/status/memory coordination.
- Consider memories only with a clear capture policy.

### Privacy-First

- Disable or narrowly enable Any App control, remote control, browser/Chrome control, broad plugins, Node REPL, and memories.
- Keep network off and use explicit per-task approvals.
- Keep only essential MCP servers for the active task.
- Prefer in-repo/workspace memory over global app memory.
