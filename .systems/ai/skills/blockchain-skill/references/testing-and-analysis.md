# Testing And Analysis

Use this reference for Foundry checks, fuzz/invariants, static analysis, gas/coverage expectations, and skipped-check
reporting.

## Baseline Commands

- Run `forge build` for smart-contract implementation changes when safe and in scope.
- Run `forge test` for smart-contract implementation and QA changes when safe and in scope.
- Run `forge fmt --check` when formatting is in scope and the command is safe.
- Run deployment/readback script checks for deployment tooling changes, but avoid broadcast/external effects unless
  approved.

## Test Coverage Expectations

- Test initializer lock, reinitializer behavior, unauthorized upgrade, unauthorized privileged calls, and upgrade state
  preservation only when upgradeability is explicitly owner-approved and present.
- Test all economic boundaries: caps, sale close/finalize, claim/redeem/refund one-shot behavior, rounding, dust, and
  overflow/underflow assumptions.
- Test compliance and role behavior: approved/rejected/revoked/not-set states, transfer eligibility, purchase eligibility,
  voucher/reward eligibility, pause, and role rotation where in scope.
- Test composed system scenarios when multiple contracts share authority or value flow.

## Fuzz And Invariants

- Use fuzz or invariants for economic/security logic when behavior has many input combinations.
- Prefer invariants such as no oversell, caps never exceeded, total accounted equals balances/state, no double claim, no
  unauthorized economic authority, and no closed-state reopening.
- If a fuzz/invariant check is skipped, record why and whether PASS still has enough evidence.

## Static Analysis

- Use Slither when installed and safe for the environment.
- Slither reference: `https://github.com/crytic/slither`.
- Treat static-analysis findings as candidates until reviewed against the actual code path and accepted scope.
- If Slither is unavailable, record it as skipped with reason and impact.

## Gas, Coverage, And Workspace Hygiene

- Consider gas snapshots/budgets when loops, batch operations, or repeated claims are in scope.
- Consider coverage when QA needs evidence that critical economic/security branches are tested.
- Avoid committing generated outputs such as build artifacts or local tool homes unless the repo intentionally tracks them.

## PASS Rule

- Do not mark PASS without explicit evidence: command output, manual/static review notes, checked edge cases, and skipped
  checks with impact.
- A skipped check that is material to correctness blocks PASS unless another evidence source covers the risk.
