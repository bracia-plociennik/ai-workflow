# permissions.md

Use execution-modes.md to verify existing scope-bound approval at each gate. An accepted concrete plan can cover its named local high-risk implementation and Phase 5 assessment. Mode metadata creates no permission; new effects/risks and critical-risk actions keep required approvals.
For future approved scopes, use `.systems/ai/core/phase-commit-policy.md` at planning-range end and phases 6/7/8. Explicit no-commit is not overridden; current PTO approval is non-retroactive. Ignored-only/no-op creates no commit. Phase8 requires actual final-owner-yes, counterpart impact must be resolved, one coordinator owns the index, and push is never inferred. Bound V3/schema3 is opt-in and current-only; unsupported proof needs fresh QA. Fresh owned artifact closure remains separate from source equivalence. Validator: `check-phase-commit-policy`.


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
