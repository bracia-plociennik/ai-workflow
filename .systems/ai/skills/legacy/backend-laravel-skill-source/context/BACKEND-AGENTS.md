# TokBase Backend Agent Instructions (Laravel + Backpack)

## Status

- This file is auxiliary backend guidance.
- Root [`AGENTS.md`](/Users/jakubplociennik/Code/GFI/AGENTS.md) remains authoritative.
- Local [`backend/AGENTS.md`](/Users/jakubplociennik/Code/GFI/backend/AGENTS.md) is the active workspace extension layer.
- This file extends those two documents and must not replace them.

## Purpose

This file defines strict operational rules for coding agents (Codex / Copilot).

Goals:

- enforce contract-first API
- prevent frontend-backend drift
- ensure deterministic, predictable backend behavior
- enforce minimal, safe changes

This file is binding.

---

# 1. Repo Context

## Core Areas

- app/Models → data structure (source of truth)
- database/migrations → schema
- app/Http/Controllers → transport layer only
- app/Http/Requests → validation
- app/Services or app/Actions → business logic
- app/DTO → response mapping layer
- routes/api.php → API exposure
- app/Http/Controllers/Admin → Backpack (admin only)

## External Source of Truth

Priority:

1. API contracts (https://api.tokbase.io/api/*)
2. Database schema
3. Existing DTOs
4. Code

Never infer API shape from:

- Backpack
- random controllers
- frontend assumptions

---

# 2. Execution Modes

## 2.1 Bugfix Mode

- reproduce issue
- locate root cause
- fix with minimal diff
- do NOT refactor unrelated code

## 2.2 Feature Mode

- check if contract exists
- if missing → STOP and propose contract
- implement:
  Model → Service → DTO → Controller

## 2.3 Refactor Mode

Allowed:

- extract services
- introduce DTO
- remove duplication
- fix performance

Forbidden:

- contract changes
- schema changes without migration plan

## 2.4 Review Mode

- detect violations of AGENTS.md
- detect contract drift
- detect hidden logic

---

# 3. Mandatory Analysis (before ANY change)

You MUST analyze:

## Models

- fields
- relations
- casts
- scopes

## Migrations

- schema
- constraints
- indexes
- nullability

## API Layer

- controllers
- routes
- response structure

## Requests

- validation rules
- missing validation

## DTO Layer

- mapping completeness
- contract alignment

## Backpack

- only for admin
- must NOT affect API

---

# 4. Core Rules

## 4.1 Contract-first (non-negotiable)

If contract exists:

- follow EXACTLY
- do not add/remove fields

If missing:

- STOP
- propose contract

---

## 4.2 DTO Mapping (mandatory)

Flow:

Model → DTO → JSON

Forbidden:

- returning Eloquent models
- returning arrays from models

---

## 4.3 Controllers are transport only

Controllers must:

- receive request
- call service/action
- return DTO

Forbidden:

- business logic
- validation
- mapping

---

## 4.4 No Backpack leakage

Backpack must NOT:

- define API structure
- affect DTO
- influence response

---

## 4.5 Deterministic API

Same input → same output

Forbidden:

- random sorting
- conditional fields
- hidden defaults

---

## 4.6 Explicit output only

Response contains ONLY:

- contract-defined fields

No:

- hidden fields
- accidental attributes

---

# 5. Database Rules

## Migrations

- always reversible
- no destructive change without warning

## Relations

- explicit
- optimized

## Performance

- prevent N+1
- ensure indexes

---

# 6. Validation Rules

Required:

- FormRequest for every endpoint

Forbidden:

- validation in controller
- missing validation

---

# 7. CMS / ServicePage Rules

Must follow CMS structure (code)

Key constraints:

- sections defined by backend
- frontend consumes only payload
- no frontend fallback logic

Critical:

- section_key must be valid
- fallback logic must stay backend-side
- content_json must match schema to actual code

---

# 8. Scope Control

## Rules

- change only necessary files
- no “drive-by fixes”
- no refactors during bugfix

## When to STOP

Stop and ask if:

- API contract unclear
- multiple valid approaches
- change affects response shape
- schema inconsistency

---

# 9. Diff Rules

Allowed:

- minimal diff
- focused change

Forbidden:

- formatting-only changes
- renames without reason
- moving files without need

---

# 10. Safety Rules (High Risk Areas)

High risk:

- API contracts
- migrations
- multi-language fields
- CMS structure
- DTO layer

For these:

- plan first
- do not auto-apply risky changes

---

# 11. Commands (assumed Laravel standard)

If missing, verify before use.

- install: composer install
- migrate: php artisan migrate
- serve: php artisan serve
- test: php artisan test
- lint: vendor/bin/pint

---

# 12. Verification

## Quick Path (safe change)

- endpoint works
- no errors
- DTO correct

## Full Path (risky change)

- test endpoints manually
- verify DTO vs contract
- check N+1 queries
- validate all locales (?lang=...)

---

# 13. Output Protocol

When making changes:

1. Findings
2. Issues
3. Proposed fix
4. Apply (only if safe)
5. Final structure

---

# 14. Definition of Done

Task is complete ONLY if:

- API matches contract
- DTO exists and is used
- validation exists
- no N+1 queries
- deterministic response
- no debug code
- no unused imports

---

# 15. Review Checklist

Before finishing:

- contract respected
- no hidden logic
- no controller logic
- validation present
- DTO mapping complete
- edge cases considered

---

# 16. Failure Handling

If unsure:

- do NOT guess
- do NOT implement partial solution
- propose options

If cannot verify:

- state what is unverified

---

# 17. Priority Order

1. correctness
2. contract compliance
3. data consistency
4. performance
5. code style

---

END
