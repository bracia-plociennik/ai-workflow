# Blockchain Skill

Active AI Workflow system skill for EVM/Solidity smart-contract work.

The canonical agent contract is [`SKILL.md`](SKILL.md). This README is only a short human-facing overview.

## Use

Use this skill for smart-contract architecture, planning, implementation, QA, review, Foundry workflows, static analysis,
deployment/readback planning, and blockchain evidence review.

The skill is advisory only. It cannot override `AGENTS.md`, AI Workflow core policy, workflow phase files, accepted
project specs, risk policy, permissions, evidence requirements, stop conditions, or owner approvals.

## Resources

- `references/evm-standards.md` - Solidity/EVM coding standards and on-chain/off-chain boundaries.
- `references/value-flow-and-economics.md` - caps, token flow, claims, refunds, rounding, and ERC20 edge cases.
- `references/compliance-and-governance.md` - KYC/allowlist enforcement, roles, pause, and admin posture.
- `references/upgrades-deployments-and-manifests.md` - optional owner-approved proxies/upgrades, manifests, and external gates.
- `references/testing-and-analysis.md` - Foundry checks, fuzz/invariants, Slither, gas, and skipped-check evidence.
- `references/rwa-demo-cautions.md` - generic RWA/demo trust cautions loaded only when relevant.
- `references/foundry-commands.md` - concise Foundry command reference.

Raw `context/` dumps were intentionally removed and distilled into curated references. No scripts are bundled in v2.
