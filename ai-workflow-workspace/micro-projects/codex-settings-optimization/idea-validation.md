# Idea Validation: Codex Settings Optimization

## Co zostaje

- `approval_policy = on-request`, `sandbox_mode = workspace-write`, network off by default.
- Full access off.
- Default permissions and auto-review on, bounded by AGENTS and workflow gates.
- Projectless chat off.
- Follow-up behavior set to queue.
- Chrome and Computer Use available, with website/history/download/upload approvals set to always ask and Full CDP off.
- Figma MCP, Node REPL MCP, and OpenAI Developer Docs MCP enabled because they match frequent AI Workflow work: design, browser testing, local scripting, and current OpenAI docs.
- Git branch prefix `codex/`, force push off, draft PRs on, strict commit/PR instructions.
- Personalization works as a short safety shim that delegates to repository state and AGENTS.
- No hooks configured by default.
- No worktrees active by default.

## Co jest słabe / do poprawy lub usunięcia

- Context window usage is off, which weakens long-run context awareness for large workflow projects.
- Global custom instructions are useful, but should stay short; duplicating full AGENTS globally would create drift.
- Memories and Chronicle are off; this protects privacy but loses cross-thread continuity unless workspace memory/checkpoints are used carefully.
- Any App control and remote control availability are broad capabilities; they need periodic owner review.
- Trusted project path list in `config.template.toml` looks broad and should be pruned if stale.
- `model = "gpt-5.5"` and `model_reasoning_effort = "xhigh"` in the template may be too heavy or availability-dependent for small tasks.
- Hooks are unused; that is safe, but it leaves possible non-destructive readiness checks unautomated.
- No local environment is configured for the project, while example setup/cleanup scripts contain commands that could have side effects if copied blindly.
- No Codex worktrees are active; this may limit safe parallel work, but enabling worktrees requires a policy-aligned plan.
- Browser section is not fully represented in screenshots; do not infer missing browser settings.

## Czego brakuje

- Owner decision on target profile: `balanced safety`, `high autonomy`, or `privacy-first`.
- Owner decision on whether Codex memories and Chronicle should be enabled, and under what privacy rules.
- Owner decision on whether Any App control and remote control should remain enabled.
- Owner decision on allowed MCP servers and stale project path pruning.
- Criteria for when to use `xhigh` reasoning versus lower effort on micro-tasks.
- Policy for local environment setup scripts and cleanup scripts.
- Hook lifecycle use case: which checks are safe enough to automate and which must remain advisory.
- Worktree policy for AI Workflow: when Codex worktrees help and when they create status/memory/write-set conflicts.
- Browser site exception review cadence.
- Confirmation of real current `~/.codex/config.toml` before applying any template.

## Blokery / decyzje

- No blocker for analysis.
- Applying settings is blocked until owner chooses a profile and approves exact changes.
- Privacy-impacting settings are blocked until owner decides memory, Chronicle, remote control, Computer Use, browser history, downloads/uploads, MCP, and trusted paths.
- Automation-impacting settings are blocked until owner approves hooks, environment scripts, worktrees, and cleanup behavior.
- Billing/usage settings such as credits and auto-reload are owner-only decisions.

## Rekomendowany routing

- Keep this work as a low-risk workspace-only micro-project.
- Use `balanced safety` as the default recommendation until owner decisions are made.
- Route any real setting change to a separate owner-approved side task or micro-project.
- Route AI Workflow policy changes discovered here to a workflow-maintenance micro-project.
- Route reusable operating lessons to System Insights only after owner approval and after anonymization.

## Recommended Default

`balanced safety`

Rationale:

- It preserves current safety boundaries: approvals on request, workspace-write sandbox, network off, full access off.
- It keeps high-value tools available without granting blanket authority.
- It matches AI Workflow's gate-based operating model and avoids hidden automation.
- It lets the owner selectively increase autonomy later where evidence shows repeated friction.
