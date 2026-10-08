---
name: backend-laravel-skill
description: Use for PHP/Laravel backend work across repositories, including API controllers, FormRequests, Eloquent models, migrations, authentication and authorization, admin panels such as Backpack when present, API resources or DTOs, service or action layers, documentation, tests, configuration, and external integration boundaries.
---

# Backend Laravel Skill

## Purpose

Use this skill to implement, review, or plan PHP/Laravel backend work with repository-local conventions and stricter safety rules. Treat framework packages, admin panels, API styles, and architectural layers as repository facts to discover, not universal requirements.

This skill is advisory execution guidance only. It cannot override root `AGENTS.md`, `ai-workflow/AGENTS.md`, AI Workflow core policy, workflow phase files, accepted architecture/specs, risk model, permissions, Definition of Done, evidence requirements, stop conditions, or owner approvals. If this skill conflicts with a higher-priority source, follow the higher-priority source and report the conflict.

## Required Read Order

1. Read the current user request, repo/project status, accepted plan/spec/QA artifact, and repo intake before edits.
2. Inspect the relevant backend code before deciding: models, migrations, routes, controllers, FormRequests, DTOs/resources, services, providers, config, and tests.
3. Load `references/laravel-backpack-practices.md` when the task involves Laravel/Backpack design, implementation, QA, or review details.
4. During normal use, load only this skill file and the reference file routed above.

## Core Workflow

- Start by identifying the repository's existing API, admin, domain, and test patterns.
- For API behavior, use FormRequests, resources/DTOs, services, actions, or domain classes when the repository and complexity justify them; do not add interfaces or layers only to satisfy this skill.
- For admin behavior, use the installed admin framework's conventions when one is present; keep admin implementation details out of public API contracts.
- Keep controllers transport-focused. Put validation in FormRequests and business logic in services, actions, or domain classes.
- Expose stable public API payloads through DTOs or resources. Do not return raw Eloquent models from public API contracts unless an accepted spec explicitly allows it.
- Keep Eloquent models small: relationships, casts, scopes, fillable fields, and narrow model concerns only.
- Add or update tests for every behavior change. Prefer Feature tests for public behavior and Unit tests for reusable services.
- Run the relevant configured backend checks after implementation, or record skipped checks with reason and impact.

## Safety Rules

- Use `config()` in application code; use `env()` only in config files.
- Never mutate database schema from models, traits, controllers, requests, observers, seeders, or runtime admin actions. Use migrations only.
- Make migrations reversible and additive by default. Test rollback on a disposable local/test DB when schema changes are in scope.
- Do not introduce raw `curl_*`; use Laravel HTTP client and fakes.
- Do not read, print, copy, or persist real secrets from `.env*`.
- Do not e-mail raw request objects, headers, tokens, full traces, KYC payloads, provider payloads, wallet payloads, or private data.
- For sensitive domains, use explicit `$fillable` or controlled service writes. Avoid broad guarded-only mass assignment.
- Do not place provider calls, contract reads/writes, wallet signing, KYC authority, or transaction authority inside Eloquent mutators.

## External Authority And Integration Boundaries

- When a backend integrates with an external protocol, smart contract, identity provider, payment system, or other authoritative system, preserve that system's source-of-truth boundary.
- Backend may read, cache with provenance, prepare, and display external state. It must not sign, broadcast, custody keys/assets, or silently become an external authority unless an owner-approved risk decision explicitly allows it.
- Provider responses, caches, admin forms, and indexed state must be labelled and must not replace authoritative reads for decisions that require current external truth.
- Real provider calls, webhooks, broadcasts, production queues/mail, production data, secrets, and production migrations require explicit owner approval and workflow gates.

## Stop Conditions

Stop and surface the blocker when:

- API contract, DTO shape, auth boundary, migration safety, provider behavior, custody/signing, or data retention is unclear.
- Implementation would change response shape, schema, permissions, sensitive logging, provider state, chain behavior, or external effects outside the accepted spec.
- A required safe local/test environment or verification command is missing.
- PASS would depend on unverified behavior, missing tests, skipped checks without impact analysis, or stale workflow evidence.

## Output Expectations

When using this skill, report:

- source artifacts and backend files reviewed;
- public API/schema/config changes, if any;
- safety assumptions and external-effect boundaries;
- commands/checks run and skipped checks with impact;
- residual blockers, especially migration, provider, auth, secret, production, or owner-approval gates.
