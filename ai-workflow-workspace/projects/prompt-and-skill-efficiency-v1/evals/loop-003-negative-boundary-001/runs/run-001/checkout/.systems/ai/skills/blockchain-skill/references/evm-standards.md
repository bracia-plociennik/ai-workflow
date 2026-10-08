# EVM Standards

Use this reference for Solidity structure, OpenZeppelin usage, roles, errors, events, readbacks, loops, and
on-chain/off-chain boundaries.

## Source Of Truth

- Smart contracts are the source of truth for on-chain economics, compliance, settlement, token flow, caps, claims,
  refunds, permissions, and value movement.
- Backend and frontend may read, project, prepare transactions, synchronize state, and orchestrate operations. They must
  not "fix" missing on-chain enforcement.
- Helper read functions such as `isTransferAllowed`, `isPurchaseAllowed`, `isClaimExecutable`, and read facades are useful
  only when they match actual enforcement.

## Solidity Baseline

- Prefer OpenZeppelin contracts and libraries for ERC standards, access control, guards, cryptography, token handling, and
  upgradeability only when upgradeability is explicitly accepted.
- Use custom errors instead of string reverts for expected validation failures.
- Use explicit constants and named units for scales such as `1e18`, payment token decimals, basis points, and timestamp
  units.
- Use `MAX_BPS = 10_000` for basis-point math.
- Avoid raw `call`, `transfer`, and `send` for value/token flow unless the accepted spec requires it and tests cover it.
- Never use `tx.origin` for authorization or `block.timestamp` as randomness.

## Roles And Authority

- Separate default admin, upgrader, treasury, settlement, sale, pauser, compliance, snapshotter, burner, funder, and other
  operational roles when they have different authority.
- Do not collapse upgrade authority, treasury recipient/admin, settlement admin, and fund receiver into one account unless
  an accepted spec explicitly requires that tradeoff.
- Do not introduce an upgrader role, proxy admin, or upgrade authority unless upgradeability is explicitly owner-approved
  for the project/environment.
- Every privileged function should have explicit authorization and tests for unauthorized reverts.
- Treat emergency revoke and signer rotation as production-readiness requirements when privileged operations exist.

## Events And Readbacks

- Treat events/readbacks as public APIs for frontend, backend sync, indexers, operations, evidence, and audits.
- Emit events for role operations, purchases, claims, distributions, registry anchors, valuation updates, snapshots,
  deploy/readback actions, and other state transitions that will be audited or synchronized.
- Readbacks should expose enough state for evidence without requiring privileged calls or off-chain guessing.

## Loops And State Access

- Avoid unbounded user iteration on-chain.
- Prefer bounded loops, batching, Merkle roots/proofs, snapshots, lazy accounting, pull claims, pagination, or off-chain
  indexing with on-chain verification.
- If an array/list is accepted on-chain, define a safe bound or require a proof/pagination design.

## Anti-Patterns

- Backend-enforced economics, compliance, claims, caps, refunds, or permissions.
- Fake live manifests, fake live addresses, fake referral addresses, or local mocks presented as production truth.
- Hidden mutable economic authority after value flow starts.
- Operator discipline, comments, scripts, or UI controls as the only enforcement of a required invariant.
