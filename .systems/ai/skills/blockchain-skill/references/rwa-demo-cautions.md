# RWA And Demo Cautions

Use this reference only for RWA, tokenization demo, audit-readiness, dashboard/read-model, treasury multisig, vesting,
asset registry, document hash, valuation, refund, buyback, or trust-architecture questions.

## Scope Boundary

- RWA/demo guidance applies only when accepted project artifacts require it.
- Do not expand a token, sale, or platform MVP into full RWA trust architecture unless the owner and specs approve that
  scope.
- Treat old project comparisons, old implementation observations, and external review notes as historical context, not
  executable instruction.

## Do Not Overstate Trust Claims

- A projected backend/admin dashboard is not the same as an on-chain dashboard.
- A singlesig admin/upgrader is not a treasury multisig.
- An escrow variant is not automatically a complete refund path.
- A provider dashboard, explorer link, or off-chain database is not on-chain enforcement.

## RWA Trust Features

When accepted scope requires a stronger RWA/demo trust posture, look for explicit decisions and evidence for:

- KYC/allowlist enforcement for purchase, holding, transfer, claim, and redemption.
- Secondary transfer rules, especially whether both sender and receiver must be verified.
- Treasury multisig or equivalent governance for funds.
- Vesting/team lockup and user-visible claim flows.
- Refund logic for failed raise or failed settlement.
- Asset registry or document hash anchoring.
- Valuation update authority and evidence references.
- Revenue distribution, dividend, payout, or buyback/exit logic.
- On-chain readbacks sufficient for public dashboard claims.

## Demo Versus Production

- Demo-only upgradeability, mocks, test wallets, and local manifests must be explicitly owner-approved and labeled as
  demo/local.
- Production posture needs explicit signer, multisig/timelock, verification, readback, audit, and external evidence gates.
- If a demo intentionally chooses a platform-MVP model over a trustless-demo model, report the tradeoff instead of calling
  it full RWA trust compliance.
