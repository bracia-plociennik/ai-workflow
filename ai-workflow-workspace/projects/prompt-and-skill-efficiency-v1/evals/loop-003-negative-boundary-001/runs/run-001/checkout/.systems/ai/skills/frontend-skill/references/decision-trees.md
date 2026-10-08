# Frontend Decision Trees

## Before Coding

1. Identify the product surface: marketing, operational, authenticated, transactional, admin, or data-heavy.
2. Identify the user goal and failure cost.
3. Inspect existing routes, tokens, components, icons, data contracts, and test commands.
4. Choose the smallest repository-native pattern that satisfies the accepted DoD.

## Escalation

- Known repository primitive: reuse it.
- Existing dependency with compatible behavior: extend it after evidence review.
- New dependency or third-party component: record provenance, license, bundle, accessibility, and maintenance impact.
- Unknown external effect or permission boundary: stop and ask the owner.

## Review Decision

Classify each concern as `implemented`, `missing`, `not-applicable`, or `blocked`. Do not convert an unknown into a positive result.
