# permissions.md

## Default Permission Model

Agents may read repository files and run safe local inspection commands.

Agents may write files only when `AGENTS.md` write conditions are satisfied and the active phase allows writes.

## Forbidden Without Explicit Approval

An agent must not:

- read, print, copy, or expose secrets unless explicitly requested for a security audit;
- modify production credentials;
- run destructive database operations;
- run destructive git operations;
- change auth, billing, permissions, security, compliance, or data retention without approval;
- install new production dependencies without approval;
- weaken tests to pass;
- ignore failing checks;
- modify CI to bypass quality gates;
- send real emails, notifications, tickets, invoices, payments, or external API writes;
- deploy to production;
- change production infrastructure;
- delete historical decisions or superseded specs without deprecation policy.

## Safe Defaults

- Use local/test environments.
- Use fake/log/test adapters for external effects.
- Prefer read-only inspection before mutation.
- Record skipped checks and approval gaps.
