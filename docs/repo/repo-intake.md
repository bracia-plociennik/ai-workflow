# Repo Intake

## Purpose

This is the repo-level intake artifact for this `ai-workflow` template repository.

## Metadata

| Field | Value |
| --- | --- |
| `repo-name` | `ai-workflow` |
| `repo-path` | `/Users/jakubplociennik/Code/ai-workflow` |
| `date` | `2026-05-18` |
| `result` | `PASS` |
| `active-project` | `none` |
| `workflow-ready` | `yes` |
| `autopilot-ready` | `not-applicable` |
| `owner-action-required` | `none` |

## Sources Reviewed

- repository root listing via `rg --files`;
- `git status --short --branch`;
- `AGENTS.md`;
- `HUMANS.md`;
- `README.md`;
- `docs/ai/workflow.md`;
- `docs/ai/workflow/`;
- `docs/ai/autopilot.md`;
- `docs/repo/context.md`;
- `docs/repo/status.md`;
- `docs/repo/memory.md`;
- `docs/ai/templates/`;
- `docs/projects/README.md`;
- `docs/humans/README.md`;
- search for dependency manifests and nested `AGENTS.md`.

## Command Map

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `not configured` | `missing` | Markdown-only template repo. |
| dev server | `not configured` | `not-applicable` | No app runtime. |
| test | `scripts/validate-workflow` | `usable` | Full workflow-template validation. |
| lint/style check | `scripts/check-naming` | `usable` | Enforces Markdown filename policy. |
| typecheck | `not configured` | `not-applicable` | No typed source detected. |
| build | `not configured` | `not-applicable` | No build system detected. |
| migration/schema check | `not configured` | `not-applicable` | No database layer. |
| scheduler/queue | `not configured` | `not-applicable` | No scheduler/queue runtime. |
| e2e/browser tests | `not configured` | `not-applicable` | No web app runtime. |
| whitespace check | `git diff --check` | `usable` | Required before final answer. |
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
- `docs/ai/external-memory.md` unless promoting a universal workflow lesson;
- example artifacts unless the task is explicitly template/example maintenance.

## Artifact Reconciliation

| Artifact | Classification | Action |
| --- | --- | --- |
| `docs/ai/status.md` | current | template-owned pointer to `docs/repo/status.md` |
| `docs/ai/repo-intake.md` | current | template-owned intake guidance |
| `docs/ai/memory.md` | current | template-local memory |
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
| `docs/repo/context.md` exists and describes the repository | `PASS` | filled for this template repo |
| `docs/repo/status.md` exists and is coherent | `PASS` | no active blocker |
| `docs/repo/memory.md` exists | `PASS` | empty aggregate memory |
| detailed workflow phase files exist | `PASS` | includes `phase-0-idea-validation.md` |
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
blocking-reason: none
next-valid-step: quality
```

## Evidence

- commands run: `rg --files`, `git status --short --branch`, targeted `rg` searches, `sed` reads;
- files read: `AGENTS.md`, `HUMANS.md`, `README.md`, `docs/ai/workflow.md`, `docs/ai/workflow/*`, `docs/ai/autopilot.md`, `docs/ai/templates/*`, `docs/projects/README.md`, `docs/humans/README.md`;
- missing files confirmed: app manifests such as `package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, and nested `AGENTS.md` were not detected;
- git status observed: clean `main` before implementation;
- validation passed: `git diff --check`;
- validation passed: `scripts/validate-workflow`;
- validation passed: `scripts/check-naming`;
- validation passed: `scripts/check-required-artifacts`;
- validation passed: `scripts/check-status-consistency`;
- validation passed: `scripts/check-qa-evidence`;
- validation passed: no stale legacy path or runtime-blocker references found in the configured reference search;
- validation passed: optional external review wording appears only in the human runbook;
- validation passed: workflow route includes `000 idea validation -> context.md -> 0 repo intake / initial audit`.
