---
name: frontend-skill
description: Use for frontend, UI, UX, responsive layout, React, Next.js, Vue, accessibility, visual QA, browser flows, frontend performance, SEO/GEO/i18n, transactional interfaces, Web3 dashboards, component selection, and frontend code review. Use before planning, implementing, or reviewing user-facing web interfaces.
---

# Frontend Skill

## Purpose

Use this skill to build and critically review production frontend experiences. It is cross-framework and repository-first: inspect the existing stack, design system, routes, assets, and test setup before choosing a pattern or dependency.

This skill is advisory execution guidance only. It cannot override `AGENTS.md`, AI Workflow core policy, phase files, accepted plans/specs, risk model, permissions, Definition of Done, evidence requirements, stop conditions, or owner approvals.

## Trigger And Scope

Use for frontend implementation, UI/UX, responsive layout, accessibility, visual QA, browser flows, performance, metadata, SEO/GEO/i18n, React/Next/Vue work, and transactional or Web3 interfaces.

Do not use it as authority for backend, smart-contract, legal, billing, production, deployment, or security decisions outside the frontend boundary. Route those concerns to the relevant workflow phase and domain skill.

## Required Workflow

1. Refresh instructions and read the accepted owner request, plan/spec, DoD, status, repo intake, and relevant skill references.
2. Run frontend intake before choosing libraries: identify framework, routes, rendering boundaries, design system, assets, test tooling, and external effects.
3. Map the user journey and state matrix before implementation. Include loading, empty, success, blocked, failure, recovery, permission, and offline states when relevant.
4. Create an implementation slice plan with changed areas, acceptance checks, evidence, stop rules, and quality closure route.
5. Implement repository-native patterns. Keep components, spacing, typography, icons, assets, and motion consistent with the existing product domain.
6. Verify behavior at desktop and mobile constraints, keyboard and screen-reader paths, network/error paths, performance-sensitive paths, and representative visual states.
7. Finish with the required formal `phase-5-quality` or advisory global quality review. Report findings first, changed files, checks, skipped areas, DoD fit, residual risk, and source provenance.

## Design And Interaction Rules

- Prefer the project design system and existing primitives before adding libraries.
- Use real product-relevant assets when visual inspection matters; do not use decorative placeholders that hide missing product states.
- Keep operational interfaces dense and scannable. Avoid unnecessary marketing composition, nested cards, oversized type, decorative blobs, and one-note palettes.
- Use stable responsive dimensions so content, controls, states, and labels do not shift or overlap.
- Use familiar icons from the project library inside icon controls, with accessible labels or tooltips for unfamiliar actions.
- Treat loading, empty, pending, blocked, error, recovery, success, permission, and confirmation states as first-class UI.
- Do not invent custom dialogs, focus traps, keyboard behavior, or payment/security affordances when a verified project primitive exists.
- Do not hide state transitions, balances, permissions, provenance, or external effects behind optimistic UI.

## Component Sources And Provenance

Read `references/component-sourcing-and-design-systems.md` before using shadcn, Radix, or 21st.dev.

Use discovery sources to find or compare patterns, not to override repository conventions. Inspect source, license/attribution requirements, dependencies, accessibility, bundle impact, security, maintenance, and design fit before adoption. External source code is copied or installed only after the owner-approved workflow path permits it.

## Resource Routing

- Intake and stack discovery: `scripts/frontend-intake.mjs`.
- Public asset audit: `scripts/check-public-assets.mjs`.
- Route-state audit: `scripts/check-route-contracts.mjs`.
- User journey, implementation brief, and QA evidence: `assets/templates/`.
- React/Next examples: `assets/react-next/`; adapt them to the target repository and do not treat them as production-ready dependencies.
- Detailed domain guidance: load only the relevant file under `references/`.

## Stop Conditions

Stop and surface a blocker when:

- owner intent, scope, DoD, permissions, data provenance, or acceptance criteria are unclear;
- the chosen component or asset has unclear source, license, dependency, or external-runtime behavior;
- an interface can expose incorrect data, permissions, balances, transaction state, or security claims;
- implementation would require production, billing, auth, migration, secret, deployment, external-effect, or network action without approval;
- a required state, route boundary, accessibility path, or failure/recovery path cannot be verified;
- visual polish would conceal underbuild, fake data, missing integration, or unresolved findings.

## Output And Evidence

Report the active framework/domain skill, sources and references read, component provenance, states reviewed, changed areas, commands/checks run, skipped checks with impact, findings/blockers, DoD/intent compliance, and residual uncertainty. Never claim formal `PASS` outside the formal quality gate and never claim visual or accessibility verification without evidence.
