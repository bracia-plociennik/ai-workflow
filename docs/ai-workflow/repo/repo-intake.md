# Repo Intake

## Purpose

This is the repo-level intake artifact for this `ai-workflow` template repository.

## Metadata

| Field | Value |
| --- | --- |
| `repo-name` | `ai-workflow` |
| `repo-path` | `/Users/jakubplociennik/Code/ai-workflow` |
| `date` | `2026-05-19` |
| `result` | `PASS` |
| `active-project` | `none` |
| `workflow-ready` | `yes` |
| `autopilot-ready` | `not-applicable` |
| `owner-action-required` | `none` |

## Sources Reviewed

- repository root listing via `rg --files`;
- `git status --short --branch`;
- `AGENTS.md`;
- `docs/ai-workflow/ai/templates/root-agents.template.md`;
- `HUMANS.md`;
- `README.md`;
- `docs/ai-workflow/ai/installation.md`;
- `docs/ai-workflow/ai/workflow.md`;
- `docs/ai-workflow/ai/workflow/`;
- `docs/ai-workflow/ai/autopilot.md`;
- `docs/ai-workflow/repo/context.md`;
- `docs/ai-workflow/repo/context/`;
- `docs/ai-workflow/repo/status.md`;
- `docs/ai-workflow/repo/memory.md`;
- `docs/ai-workflow/ai/templates/`;
- `docs/ai-workflow/projects/README.md`;
- `docs/ai-workflow/humans/README.md`;
- search for dependency manifests and nested `AGENTS.md`.

## Installation Collision Status

This repository is the upstream AI Workflow template, so root `AGENTS.md`, `HUMANS.md`, `docs/ai-workflow/`, `scripts/ai-workflow/`, and `.github/workflows/ai-workflow-validate.yml` are template-owned here.

In a target repository, AI Workflow must be installed as a nested clone at `ai-workflow/`. The only target-root file copied or merged by default is `AGENTS.md` from `ai-workflow/docs/ai-workflow/ai/templates/root-agents.template.md`. Target-root `docs/`, `scripts/`, `.github/`, `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, product code, app config, CI, and deployment files remain target-owned.

| Path | Owner | Status | Resolution |
| --- | --- | --- | --- |
| `README.md` | AI Workflow upstream | `current` | Template README for this repo; target repos must not overwrite their README. |
| `AGENTS.md` | AI Workflow upstream | `current` | Internal execution contract for this repo and nested clones; target repos use the shim template, not a direct copy of this file. |
| `docs/ai-workflow/ai/templates/root-agents.template.md` | AI Workflow upstream | `current` | Target-repository root `AGENTS.md` shim source. |
| `HUMANS.md` | AI Workflow upstream | `current` | Human runbook stays at `ai-workflow/HUMANS.md` in target repos; no root `HUMANS.md` copy by default. |
| `docs/` | AI Workflow upstream | `current` | Template docs in this repo; target-root `docs/` remains target-owned. |
| `scripts/` | AI Workflow upstream | `current` | Template validators in this repo; target-root `scripts/` remains target-owned. |
| `.github/` | AI Workflow upstream | `current` | Template CI in this repo; target-root `.github/` remains target-owned unless owner explicitly installs optional integration. |
| target `ai-workflow/` | AI Workflow nested clone | `not-applicable-upstream` | Target repositories create this by cloning this repo. |

## Command Map

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `not configured` | `missing` | Markdown-only template repo. |
| dev server | `not configured` | `not-applicable` | No app runtime. |
| test | `scripts/ai-workflow/validate-workflow` | `usable` | Full workflow-template validation. |
| lint/style check | `scripts/ai-workflow/check-naming` | `usable` | Enforces Markdown filename policy. |
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
| template ownership | target-repo facts written into root docs or `docs/ai-workflow/ai/` | any repo-specific fact outside `docs/ai-workflow/repo/`, examples, or project artifacts | keep template docs generic |
| examples | EXAMPLE artifacts mistaken for active workflow state | using EXAMPLE as real PASS evidence | keep EXAMPLE marked documentation-only |
| workflow refs | stale paths after rename | references to legacy human/template/memory paths | run reference searches |
| git/release | destructive history operation | force-push, tag deletion, release publishing | branch + commit after validation |

## Restricted Zones

- secret-bearing files such as `.env*`;
- generated/runtime/cache/build artifacts;
- dependency directories;
- `docs/ai-workflow/ai/external-memory.md` and `docs/ai-workflow/ai/external-memory/` unless promoting a universal workflow lesson;
- example artifacts unless the task is explicitly template/example maintenance.

## Artifact Reconciliation

| Artifact | Classification | Action |
| --- | --- | --- |
| `docs/ai-workflow/ai/status.md` | current | template-owned pointer to `docs/ai-workflow/repo/status.md` |
| `docs/ai-workflow/ai/repo-intake.md` | current | template-owned intake guidance |
| `docs/ai-workflow/ai/installation.md` | current | template-owned installation and collision policy |
| `docs/ai-workflow/ai/memory.md` and `docs/ai-workflow/ai/memory/` | current | template-local memory router and entries |
| `docs/ai-workflow/repo/` | current | repo-local runtime docs |
| `docs/ai-workflow/humans/` | current | canonical human-facing docs path |
| `docs/ai-workflow/ai/templates/projects/` | current | canonical project template path |
| `docs/ai-workflow/ai/templates/humans/` | current | canonical human template path |

## Readiness Checklist

| Check | Result | Notes |
| --- | --- | --- |
| `AGENTS.md` exists and remains template-owned | `PASS` | repo-specific layer moved to `docs/ai-workflow/repo/` |
| `docs/ai-workflow/ai/templates/root-agents.template.md` exists | `PASS` | target root shim delegates to `ai-workflow/AGENTS.md` |
| `HUMANS.md` exists and remains template-owned | `PASS` | human runbook updated |
| `docs/ai-workflow/ai/` workflow/template docs exist | `PASS` | phase files and templates present |
| `docs/ai-workflow/repo/context.md` exists as router and `docs/ai-workflow/repo/context/` describes the repository | `PASS` | filled for this template repo |
| `docs/ai-workflow/repo/status.md` exists and is coherent | `PASS` | no active blocker |
| `docs/ai-workflow/repo/memory.md` and `docs/ai-workflow/repo/memory/README.md` exist | `PASS` | empty repo memory router and entry directory |
| detailed workflow phase files exist | `PASS` | includes `phase-0-repo-intake.md`, `phase-0-project-workspace.md`, and `phase-0-idea-validation.md` |
| templates exist | `PASS` | includes `docs/ai-workflow/ai/templates/repo/` |
| repo command map is discovered or marked missing | `PASS` | no app commands configured |
| safe test environment is known or explicitly missing | `PASS` | not applicable for Markdown-only repo |
| high-risk areas are identified | `PASS` | template ownership and stale refs identified |
| restricted/generated/runtime zones are identified | `PASS` | see restricted zones |
| real external effects are disabled by default or require STOP | `PASS` | no external effects required |
| retry/checkpoint/git policy is explicit | `PASS` | covered by `AGENTS.md` and workflow docs |

## Owner Decisions Required

No owner decisions required.

## Gate Decision

```text
result: PASS
blocking-reason: none
next-valid-step: none
```

## Evidence

- commands run: `rg --files`, `git status --short --branch`, targeted `rg` searches, `sed` reads;
- files read: `AGENTS.md`, `HUMANS.md`, `README.md`, `docs/ai-workflow/ai/workflow.md`, `docs/ai-workflow/ai/workflow/*`, `docs/ai-workflow/ai/autopilot.md`, `docs/ai-workflow/ai/templates/*`, `docs/ai-workflow/projects/README.md`, `docs/ai-workflow/humans/README.md`;
- missing files confirmed: app manifests such as `package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, and nested `AGENTS.md` were not detected;
- git status observed: working tree contains the nested-clone installation model update during this quality pass;
- validation passed: `git diff --check`;
- validation passed: `scripts/ai-workflow/validate-workflow`;
- validation passed: `scripts/ai-workflow/check-naming`;
- validation passed: `scripts/ai-workflow/check-required-artifacts`;
- validation passed: `scripts/ai-workflow/check-status-consistency`;
- validation passed: `scripts/ai-workflow/check-qa-evidence`;
- validation passed: no stale legacy path or runtime-blocker references found in the configured reference search;
- validation passed: optional external review wording appears only in the human runbook;
- validation passed: workflow route includes repo intake, project workspace, idea validation, project context, and project/context intake before architecture.
