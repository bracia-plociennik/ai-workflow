# Optional Upgrades, Deployments, And Manifests

Use this reference for optional owner-approved proxy patterns, initializers, storage layout, manifests, readbacks, local
mocks, and external-effect gates.

## Upgradeability Decision Gate

- Upgradeability and proxy patterns are optional, never default.
- Some projects ban upgradeability entirely. In that case, do not add proxy, UUPS, initializer, storage-gap, proxy-admin,
  or upgrade-authority patterns.
- Before designing or implementing upgradeability, require accepted project scope and explicit owner approval for the
  specific project/environment.
- Record whether the accepted posture is immutable/non-upgradeable, demo-only upgradeable, upgradeable with controls, or
  deferred/blocked.
- If the posture is unresolved, stop and request the decision instead of assuming a proxy architecture.

## Upgradeable Contracts, Only When Approved

- Approved upgradeable implementation contracts must disable initializers in the constructor.
- Approved proxy deploys must use `abi.encodeCall(...)` for initializer calldata.
- Approved UUPS upgrades must authorize through `_authorizeUpgrade(...)` and an accepted upgrader role.
- Constructors must not initialize upgradeable runtime state except for disabling initializers.
- Define storage gap or namespaced storage policy when approved upgradeability is in scope.

## Upgrade Evidence, Only When Approved

- Before real upgrade evidence, require owner approval, storage layout diff, state-preservation tests, authorization tests,
  and post-upgrade readback checks.
- Reinitializer behavior should be explicit and tested when present.
- Emergency revoke and signer rotation should be documented before production upgrade paths.

## Deployment Truth

- Proxy/runtime addresses are the addresses applications and evidence should use.
- Implementation addresses are operational metadata, not the app-facing runtime address, when an approved proxy design is
  in use.
- Deployment manifests are source of truth for runtime addresses, chain ID, proxy kind, implementation, roles, mode,
  verification status, and readback evidence. For non-upgradeable deployments, omit proxy-only fields or mark them
  `not-applicable`.
- Do not guess addresses. If a manifest is missing, placeholder-only, or inconsistent with readbacks, stop.

## Local Versus External

- Local mocks must be clearly labeled local/mock and never presented as live deployment evidence.
- Dry-runs, scripts, and manifests must state whether they are local, mock, testnet, mainnet, simulated, or broadcast.
- Do not perform real deploy, broadcast, verify, provider calls, testnet/mainnet actions, audit engagement, secrets, or
  `.env*` access without explicit owner approval and workflow permission.

## Readbacks

- Deployment/readback scripts should verify role assignments, important config, token addresses, caps, treasury/vault
  addresses, chain ID, and mode.
- Readback output should be stable enough to attach as evidence and compare against manifests.
- If backend/frontend will consume addresses, use manifest/readback output as input instead of hard-coded guesses.
