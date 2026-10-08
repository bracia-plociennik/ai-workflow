# Value Flow And Economics

Use this reference for token flow, caps, supply, claims, refunds, rounding, dust, slippage, vaults, and ERC20 edge cases.

## Economic Authority

- Enforce hard caps, supply caps, mint caps, sale caps, claim limits, refund/release state, and settlement rules on-chain.
- Cap overflow behavior must be explicit: revert, partial fill, split, or other behavior only when accepted specs say so.
- If a purchase, referral mint, voucher redemption, reward, or claim can affect supply or balances, test cap boundaries.
- Do not rely on backend accounting as the source of truth for token issuance, settlement, or user entitlement.

## Value Movement

- Use `SafeERC20` for ERC20 transfers and approvals.
- Check allowance, balance, token decimals, and recipient/treasury/vault authority explicitly.
- Define exact allowance model per schedule, distribution, epoch, sale, or vault interaction.
- Prefer pull-based claims to push payouts when many users may receive funds.
- Vaults should have a single clear controller or a narrowly defined authority surface.

## Rounding, Dust, And Quotes

- Define rounding direction for every quote and distribution.
- Purchases should include a user-protecting bound such as `maxPaymentAmount`, `minTokensOut`, deadline, or expected stage
  where the accepted spec requires slippage or state-change protection.
- Remainder/dust policy must be deterministic. For distributions, either allocate final dust to the last eligible claimer,
  carry it forward, or sweep it under accepted rules.
- Reward or distribution sweeps must not take principal or already allocated user funds.

## Claims, Refunds, And Settlement

- Refund and release states should be mutually exclusive in the state machine.
- Sale closure should define hard cap, optional soft cap, close/finalize behavior, and blocking of later purchases.
- Escrow settlement is often safer than direct treasury transfer when a sale can fail or refund.
- Claims should be one-shot or explicitly idempotent, with claimed amount tracking and excluded-account behavior when in
  scope.

## Token Edge Cases

- Non-standard ERC20, fee-on-transfer, rebasing, blacklistable, pausable, and non-18-decimal tokens require explicit
  accepted policy and tests before support.
- If unsupported, reject or avoid those assets at the contract boundary or adapter boundary.
- ETH/native value flow needs the same recipient, reentrancy, accounting, and failure-mode treatment as ERC20 flow.

## Invariants To Prefer

- Caps are never exceeded.
- Total issued/sold/claimed/accounted values reconcile with balances and state.
- No double claim, double refund, double redemption, or double mint.
- Unauthorized accounts cannot move funds or change economic state.
- State transitions cannot reopen closed value-flow windows without an accepted migration or new contract.
