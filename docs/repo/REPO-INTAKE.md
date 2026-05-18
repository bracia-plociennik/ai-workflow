# Repo Intake

## Purpose

This is the repo-level intake artifact for this `ai-workflow` template repository.

## Metadata

| Field | Value |
| --- | --- |
| `repo_name` | `ai-workflow` |
| `repo_path` | `/Users/jakubplociennik/Code/ai-workflow` |
| `date` | `2026-05-18` |
| `result` | `PASS` |
| `active_project_workspace` | `none` |
| `workflow_ready` | `yes` |
| `autopilot_ready` | `not_applicable` |
| `owner_action_required` | `none` |

## Sources Reviewed

- repository root listing via `rg --files`;
- `git status --short --branch`;
- `AGENTS.md`;
- `HUMANS.md`;
- `README.md`;
- `docs/ai/WORKFLOW.md`;
- `docs/ai/workflow/`;
- `docs/ai/AUTOPILOT.md`;
- `docs/repo/CONTEXT.md`;
- `docs/repo/STATUS.md`;
- `docs/repo/MEMORY.md`;
- `docs/ai/templates/`;
- `docs/projects/README.md`;
- `docs/humans/README.md`;
- search for dependency manifests and nested `AGENTS.md`.

## Command Map

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `not configured` | `missing` | Markdown-only template repo. |
| dev server | `not configured` | `not_applicable` | No app runtime. |
| test | `git diff --check` | `usable` | Whitespace validation only. |
| lint/style check | `not configured` | `missing` | No markdown linter configured. |
| typecheck | `not configured` | `not_applicable` | No typed source detected. |
| build | `not configured` | `not_applicable` | No build system detected. |
| migration/schema check | `not configured` | `not_applicable` | No database layer. |
| scheduler/queue | `not configured` | `not_applicable` | No scheduler/queue runtime. |
| e2e/browser tests | `not configured` | `not_applicable` | No web app runtime. |
| safe inspection | `rg --files`, `rg`, `git status --short --branch` | `usable` | read-only |

## Safe Environment

- Test database strategy: not applicable.
- Fake/log/array/test service strategy: not applicable.
- Mail/notification strategy: not applicable.
- Queue/background job strategy: not applicable.
- External API strategy: no external API calls required for this repo.
- Commands that must never run against production: not applicable for this Markdown-only template repo.
- Dependency install policy: no dependency manifests detected.
- Dev server policy: no dev server configured.
- Migration policy: no migrations detected.
- Secret/credential policy: do not add secrets or target-repo credentials to this template.

## Repo Risk Register

| Area | Risk | STOP Condition | Safe Default |
| --- | --- | --- | --- |
| template ownership | target-repo facts written into root docs or `docs/ai/` | any repo-specific fact outside `docs/repo/`, examples, or project artifacts | keep template docs generic |
| examples | EXAMPLE artifacts mistaken for active workflow state | using EXAMPLE as real PASS evidence | keep EXAMPLE marked documentation-only |
| workflow refs | stale paths after rename | references to legacy human/template/memory paths | run reference searches |
| git/release | destructive history operation | force-push, tag deletion, release publishing | branch + commit after validation |

## Restricted Zones

- secret-bearing files such as `.env*`;
- generated/runtime/cache/build artifacts;
- dependency directories;
- `docs/ai/EXTERNAL-MEMORY.md` unless promoting a universal workflow lesson;
- example artifacts unless the task is explicitly template/example maintenance.

## Artifact Reconciliation

| Artifact | Classification | Action |
| --- | --- | --- |
| `docs/ai/STATUS.md` | current | template-owned pointer to `docs/repo/STATUS.md` |
| `docs/ai/REPO-INTAKE.md` | current | template-owned intake guidance |
| `docs/ai/MEMORY.md` | current | template-local memory |
| `docs/repo/` | current | repo-local runtime docs |
| `docs/humans/` | current | canonical human-facing docs path |
| `docs/ai/templates/projects/` | current | canonical project template path |
| `docs/ai/templates/humans/` | current | canonical human template path |

## Readiness Checklist

| Check | Result | Notes |
| --- | --- | --- |
| `AGENTS.md` exists and remains template-owned | `PASS` | repo-specific layer moved to `docs/repo/` |
| `HUMANS.md` exists and remains template-owned | `PASS` | human runbook updated |
| `docs/ai/` workflow/template docs exist | `PASS` | phase files and templates present |
| `docs/repo/CONTEXT.md` exists and describes the repository | `PASS` | filled for this template repo |
| `docs/repo/STATUS.md` exists and is coherent | `PASS` | no active blocker |
| `docs/repo/MEMORY.md` exists | `PASS` | empty aggregate memory |
| detailed workflow phase files exist | `PASS` | includes `000_idea_validation.md` |
| templates exist | `PASS` | includes `templates/ai/` |
| repo command map is discovered or marked missing | `PASS` | no app commands configured |
| safe test environment is known or explicitly missing | `PASS` | not applicable for Markdown-only repo |
| high-risk areas are identified | `PASS` | template ownership and stale refs identified |
| restricted/generated/runtime zones are identified | `PASS` | see restricted zones |
| real external effects are disabled by default or require STOP | `PASS` | no external effects required |
| retry/checkpoint/git policy is explicit | `PASS` | covered by `AGENTS.md` and workflow docs |

## Owner Decisions Required

| Decision | Class | Recommendation | Alternative | Blocks |
| --- | --- | --- | --- | --- |
| Uppercase filename separator migration | `high-impact` | Defer to a later dedicated rename task. | Rename now with broad reference migration. | no |

## Gate Decision

```text
result: PASS
blocking_reason: none
next_valid_step: quality
```

## Evidence

- commands run: `rg --files`, `git status --short --branch`, targeted `rg` searches, `sed` reads;
- files read: `AGENTS.md`, `HUMANS.md`, `README.md`, `docs/ai/WORKFLOW.md`, `docs/ai/workflow/*`, `docs/ai/AUTOPILOT.md`, `docs/ai/templates/*`, `docs/projects/README.md`, `docs/humans/README.md`;
- missing files confirmed: app manifests such as `package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, and nested `AGENTS.md` were not detected;
- git status observed: clean `main` before implementation;
- validation passed: `git diff --check`;
- validation passed: no stale legacy path or runtime-blocker references found in the configured reference search;
- validation passed: optional external review wording appears only in the human runbook;
- validation passed: workflow route includes `000 idea validation -> 0_context.md -> 0 repo intake / initial audit`.
