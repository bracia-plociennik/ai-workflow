# Compliance And Governance

Use this reference for KYC/allowlist enforcement, transfer restrictions, role separation, pause behavior, treasury
governance, and production admin posture.

## Compliance Enforcement

- If KYC, allowlist, sanctions, send block, receive block, jurisdiction, or profile status affects purchase, mint,
  transfer, claim, or redemption, enforce it on-chain.
- Off-chain KYC providers may decide status, but the on-chain registry/allowlist must be the enforcement surface when
  eligibility affects token/value movement.
- Do not store PII on-chain. Store only status, role, hash, reference, or other accepted minimal data.
- If threshold-based eligibility is accepted, specify the threshold, transition behavior, and what happens before and
  after KYC approval.
- If transfer restrictions are required, decide whether both sender and receiver must be approved or only one side.

## Role Separation

- Separate treasury, settlement, compliance, sale operations, pausing, signer management, reward funding, emergency
  operations, and any owner-approved upgrade authority when they have different risk.
- Do not present singlesig governance as treasury multisig.
- Do not present an upgrader role as a treasury control role.
- Tests should cover unauthorized reverts for every privileged function.

## Pause And Emergency Controls

- Pause should be scoped to the emergency it mitigates.
- Avoid pause semantics that can permanently block user refunds, claims, exits, or already owed payouts unless explicitly
  accepted and disclosed.
- Emergency controls should have clear unpause, revoke, rotation, or migration paths.
- If compliance or market-start behavior freezes after first real transfer, define that boundary and test it.

## Production Posture

- Production admin, treasury, and any owner-approved upgrader paths should prefer multisig, timelock, two-step ownership,
  hardware-backed signing, or explicit role rotation when the accepted scope includes production readiness.
- Plain EOA admin is a local/demo shortcut unless accepted by the owner for the specific environment.
- Provider names and dashboards are integration/config/evidence choices, not immutable smart-contract requirements unless
  an accepted spec says otherwise.

## Stop And Escalate

- Missing compliance policy for mint, transfer, purchase, redemption, claim, or refund.
- Ambiguous privileged role ownership.
- Any design where backend-only checks are the final authority for on-chain value movement.
- Any attempt to weaken compliance or governance assumptions without owner approval and accepted artifact updates.
