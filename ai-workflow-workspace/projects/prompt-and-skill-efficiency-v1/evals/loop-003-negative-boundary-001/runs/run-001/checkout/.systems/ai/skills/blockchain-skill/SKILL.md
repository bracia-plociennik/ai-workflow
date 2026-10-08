---
name: blockchain-skill
description: Use for EVM/Solidity smart-contract architecture, planning, implementation, QA, security review, Foundry workflows, static analysis, deployment/readback planning, blockchain evidence review, token economics, compliance gates, roles, owner-approved upgrade/proxy decisions, manifests, and on-chain/off-chain boundary decisions.
---

# Blockchain Skill

## Purpose

Use this skill to make EVM/Solidity work stricter, safer, and easier to validate inside AI Workflow.

This skill is advisory execution guidance only. It cannot override `AGENTS.md`, AI Workflow core policy, workflow phase
files, accepted architecture/specs, risk model, permissions, Definition of Done, evidence requirements, stop conditions,
or owner approvals. If this skill conflicts with a higher-priority source, follow the higher-priority source and report
the conflict.

## When To Use

Use for:

- Solidity/EVM architecture, specs, implementation, QA, and review.
- Token, sale, rewards, referral, voucher, escrow, distribution, compliance, DEX, deployment, and owner-approved
  upgrade/proxy work.
- Foundry build/test planning, fuzz/invariant testing, Slither/static-analysis planning, and blockchain evidence review.
- Deciding whether behavior belongs on-chain, in scripts, in backend, or in frontend.

Do not use for:

- General backend/frontend work with no blockchain or smart-contract boundary.
- Legal, tax, investment, or regulatory advice beyond identifying implementation gates and evidence needs.
- Real deploy, verify, provider, testnet, mainnet, secrets, or `.env*` actions without explicit owner approval and workflow gates.

## Required Read Order

1. Read the current task, accepted architecture/plan/spec, project status, repo intake, and relevant QA evidence first.
2. Read only the reference files needed for the current task from the routing table below.
3. Do not load every reference by default.
4. If a reference suggests scope that is not accepted by the current project artifacts, record it as out-of-scope or a
   future blocker instead of silently expanding the task.

## Reference Routing

Load:

- `references/evm-standards.md` for Solidity structure, OpenZeppelin use, roles, errors, events, readbacks, loops, and
  on-chain/off-chain boundaries.
- `references/value-flow-and-economics.md` for token flow, caps, supply, claims, refunds, rounding, slippage, vaults, and
  ERC20 edge cases.
- `references/compliance-and-governance.md` for KYC/allowlist enforcement, transfer restrictions, role separation,
  pausing, treasury governance, and production admin posture.
- `references/upgrades-deployments-and-manifests.md` for optional owner-approved upgradeability/proxies, storage layout,
  manifests, readbacks, local mocks, and external-effect gates.
- `references/testing-and-analysis.md` for Foundry checks, fuzz/invariants, static analysis, gas/coverage expectations,
  and skipped-check reporting.
- `references/rwa-demo-cautions.md` only for RWA, demo, tokenization trust, dashboard/read-model, treasury multisig,
  vesting, asset registry, document hash, valuation, refund, buyback, or audit-readiness questions.
- `references/foundry-commands.md` only when command syntax is needed.

## Universal Rules

- Smart contracts are the source of truth for on-chain economics, compliance, settlement, token flow, caps, claims,
  refunds, permissions, and value movement.
- Backend and frontend may read, project, prepare, and orchestrate. They must not compensate for missing on-chain
  enforcement.
- Prefer OpenZeppelin, explicit role separation, custom errors, stable events/readbacks, `SafeERC20`, bounded loops,
  Checks-Effects-Interactions, and manifest-backed runtime truth.
- Treat upgradeability and proxy patterns as optional, never default. They require accepted project scope and explicit
  owner approval, and some projects may ban them entirely.
- Never use `tx.origin` for authorization, `block.timestamp` as randomness, fake live manifests, hidden privileged
  economics, or backend-only enforcement for behavior that must be on-chain.
- Do not perform real deploy, broadcast, verify, provider, testnet, mainnet, secrets, or `.env*` actions without explicit
  owner approval and workflow permission.

## Stop Conditions

Stop and surface the blocker when:

- economic, compliance, security, permission, upgrade, deployment, provider, or external-effect decisions are unresolved;
- implementation conflicts with the accepted architecture, plan, task spec, or QA evidence;
- smart-contract correctness would depend on backend/frontend/script/operator discipline instead of on-chain enforcement;
- a loop may iterate over an unbounded user set;
- token/value movement has ambiguous authority, recipient, accounting, rounding, reentrancy, allowance, or decimals
  behavior;
- real provider calls, deployment, verification, testnet/mainnet, audit engagement, secrets, or `.env*` access would be
  needed without explicit owner approval.

## Evidence Expectations

For implementation or QA work, prefer `forge build`, `forge test`, `forge fmt --check` when safe and in scope, fuzz or
invariant tests for economic/security behavior, Slither/static analysis when available and safe, and deployment/readback
manifest checks for deployment tooling. Do not mark PASS without concrete command output or documented manual/static
evidence. Record skipped checks with reason and impact.

## Output Expectations

When using this skill, report:

- which project artifacts and skill references were read;
- key on-chain/off-chain boundary decisions;
- security/economic/compliance assumptions;
- tests/checks run and skipped checks with impact;
- residual blockers, especially external evidence, provider access, audit, deploy, verification, and owner approvals.
