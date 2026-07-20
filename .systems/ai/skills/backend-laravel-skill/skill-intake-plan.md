# Backend Laravel Skill Intake Plan

## Metadata

| Field | Value |
| --- | --- |
| `skill-name` | `backend-laravel-skill` |
| `target` | `.systems/ai/skills/backend-laravel-skill/` |
| `created-at` | `2026-06-17` |
| `result` | `accepted-for-active-skill-implementation` |

## Source Materials

- `context/prompt.md` - source prompt for Laravel, Backpack, PHP backend generation behavior.
- `context/backend-laravel-skill-source-practices.md` - reviewed current backend strengths, unsafe patterns, and recommended seed rules.
- `context/BACKEND-AGENTS.md` - auxiliary backend operational guidance preserved as source data only.

## Co zostaje

- Keep the repo-local Laravel/Backpack workflow: API work through FormRequest, service, DTO/resource, and tests; admin work through Backpack CRUD and FormRequest.
- Keep the useful safety findings from the backend source review: no runtime schema mutation, no direct `env()` outside config, no raw `curl_*`, no raw public Eloquent responses, and no sensitive data leakage.
- Keep backend-update/CHT boundaries: smart contracts are source of truth, backend is no-custody/no-signing/no-broadcast unless later owner-approved critical-risk scope changes that.

## Co poprawic lub usunac

- Do not copy the old master prompt as active instructions; convert it into concise skill guidance.
- Do not promote legacy `BACKEND-AGENTS.md` as an authority file; preserve its useful ideas only through the active skill and reference.
- Do not create README, changelog, scripts, or assets unless a later skill update proves they are needed.

## Czego brakuje

- Active `SKILL.md` for invocation and execution guidance.
- UI metadata in `agents/openai.yaml`.
- A detailed reference file for Laravel/Backpack practices that can be loaded only when needed.
- Validation evidence from skill validation and AI Workflow checks.

## Artifact Map

- `SKILL.md` - active skill contract and trigger metadata.
- `agents/openai.yaml` - UI metadata for skill listing and default invocation.
- `references/laravel-backpack-practices.md` - detailed practices loaded only when needed.
- `context/` - preserved source material only; not active normal-use guidance.

## Design Decisions

- Keep `context/**` as raw source data only. It is not active instruction for normal skill use.
- Keep `SKILL.md` concise and procedural; move examples, checklists, and detailed Laravel/Backpack guidance to `references/`.
- Do not add scripts or assets because this skill is advisory/procedural, not a deterministic tool wrapper.
- Do not use `init_skill.py` because the skill directory already exists with source context that must be preserved.
- Make the skill advisory. It cannot override root `AGENTS.md`, `ai-workflow/AGENTS.md`, AI Workflow phase gates, accepted specs, risk model, permissions, evidence requirements, or owner approvals.

## Residual Risk

- If future backend conventions change, the reference file may need refresh from current source review before use on new implementation tasks.
- The skill does not install Laravel tooling or add deterministic scripts; validation remains through repo commands and workflow evidence.
- `quick_validate.py` depends on `PyYAML`; if unavailable in the local Python runtime, use the validation result as blocked by missing dependency and perform a manual frontmatter/YAML parse check.

## Validation Plan

- Run `/Users/jakubplociennik/.codex/skills/.system/skill-creator/scripts/quick_validate.py ai-workflow-workspace/skills/backend-laravel-skill`.
- Run AI Workflow checks from `ai-workflow/`: `check-naming`, `check-required-artifacts`, and `validate-workflow`.
- Confirm no product code, backend implementation artifacts, frontend code, contracts, or smartcontracts artifacts were changed.
