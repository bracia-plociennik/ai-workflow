# Transactional And Web3 Frontends

- Treat backend, contract, wallet, payment, and provider state as authoritative according to the project architecture.
- Show connected identity, network/environment, permissions, amounts, fees, limits, freshness, pending status, confirmation, rejection, and retry behavior.
- Never claim settlement, payment, ownership, balance, approval, or transaction success from a client-side optimistic state.
- Keep display precision, currency, token decimals, rounding, and error messages aligned with the source contract.
- Separate read models from write actions and make external effects explicit before confirmation.
- Route smart-contract correctness, privileged roles, value movement, and deployment questions to the blockchain skill and formal workflow gates.
