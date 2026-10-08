# Frontend Skill Intake Plan

## Metadata

| Field | Value |
| --- | --- |
| `skill-name` | `frontend-skill` |
| `target` | `.systems/ai/skills/frontend-skill/` |
| `work-mode` | `workflow-maintenance` |
| `risk` | `medium` |
| `implementation-timebox` | `1 working day` |
| `result` | `accepted-for-active-skill-implementation` |

## Source Materials

- `.systems/ai/skills/legacy/frontend-skill-source/context/dump-blueprint.md` - frontend skill blueprint and proposed resource map.
- `.systems/ai/skills/legacy/frontend-skill-source/context/dump-idea-validation.md` - source review and frontend quality lessons; contains project-specific source data.
- `.systems/ai/skills/legacy/frontend-skill-source/context/dump-masterprompt.md` - raw prompt source preserved as legacy data only.
- Existing `blockchain-skill` and `backend-laravel-skill` - local active-skill layout and authority conventions.
- Official shadcn, Radix Themes, and 21st.dev documentation - external reference data only.

## Trigger And Non-Trigger Cases

Use for frontend, UI, UX, responsive layout, accessibility, visual QA, browser flows, frontend performance, metadata, SEO/GEO/i18n, React/Next/Vue and transactional frontend work.

Do not use as authority for backend-only, contract-only, legal, product approval, deployment, or security decisions outside the frontend surface.

## Co Zostaje

- Complete user journeys and explicit loading, empty, success, blocked, failure, and recovery states.
- Framework-neutral, repository-convention-first frontend guidance.
- Accessibility, responsive constraints, performance, metadata, provenance, and evidence-based QA.
- 21st.dev, shadcn, and Radix as optional discovery/reference sources with source and dependency review.

## Co Poprawic Lub Usunac

- Do not promote the old master prompt into active guidance.
- Do not copy client names, project paths, or client-specific conclusions into `SKILL.md`, references, scripts, or assets.
- Do not install or configure external tools from the skill automatically.
- Do not ship fake custom dialogs or unverified UI primitives as production-ready code.

## Czego Brakuje

- Active `SKILL.md`, short `README.md`, and `agents/openai.yaml`.
- Routed references for design, interaction, accessibility, performance, SEO, sourcing, transactions, and QA.
- Read-only intake and route-contract scanners.
- Framework-neutral templates and React/Next examples.
- Forward-evaluation cases for trigger, non-trigger, quality, and safety behavior.

## Blockers

- Stop before commit if raw context scan finds secrets or if copied third-party code lacks usable provenance/licensing evidence.
- Stop if a resource would require network access, MCP setup, package installation, or external writes without owner approval.

## Artifact Map

- `SKILL.md` - canonical active contract.
- `README.md` - short human description.
- `agents/openai.yaml` - UI metadata.
- `references/` - progressive-disclosure guidance.
- `scripts/` - read-only deterministic scanners.
- `assets/` - templates and examples, not active instructions.
- `evals/evals.json` - local forward-evaluation cases.
- `.systems/ai/skills/legacy/frontend-skill-source/` - tracked raw source only; not active guidance.

## Portability / Privacy Review

- Active artifacts contain no client names, project names, private domains, or machine-specific paths.
- Project-specific source material is preserved only under `.systems/ai/skills/legacy/`.
- Active guidance was checked for historical project identifiers and source-repository path leakage.

## Approval And Validation

- Owner approved implementation by accepting the `frontend-skill-v1` plan.
- Validate with `quick_validate.py`, `check-system-skills`, scanner fixtures, TypeScript checks where available, eval cases, and full workflow validation.
- Final quality route: findings-first advisory `global-quality-review-stance`; no commit before review.

## Validation Plan

- Run the skill creator quick validator when PyYAML is available; otherwise record the dependency block and run manual frontmatter, layout, and boundary checks.
- Run `check-system-skills`, `check-naming`, `git diff --check`, scanner fixtures, TypeScript checks, eval-plan validation, and full workflow validation.
- Review active artifacts for client data, external runtime resources, authority violations, unreviewed dependencies, and missing failure/recovery evidence.

## Residual Risk

The raw context intentionally preserves project/client metadata selected by the owner. It is non-authoritative and must not be loaded during normal skill use. Active artifacts must remain anonymized, dependency-aware, and free of external runtime resources.
