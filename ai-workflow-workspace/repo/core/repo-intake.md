# Repo Intake

## Purpose

This is the repo-level intake artifact for this `ai-workflow` template repository.

## Metadata

| Field | Value |
| --- | --- |
| `repo-name` | `ai-workflow` |
| `repo-path` | `/Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow` |
| `date` | `2026-10-04` |
| `result` | `PASS` |
| `active-project` | `parallel-task-orchestration-v1` |
| `workflow-ready` | `yes` |
| `autopilot-ready` | `autopilot-003-completed-at-phase-7` |
| `owner-action-required` | `final-owner-yes remains separate after technical Phase8` |

## Current Completion Baseline: 2026-10-04

Official checkout: /Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow,
branch codex/parallel-task-orchestration-v1,HEAD8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1,
approved001..007local source dirty,index empty,workspace ignored/untracked.
Origin remains https://github.com/bracia-plociennik/ai-workflow.git; no network
refresh, remote parity or CI result claimed. All seven protocol task Quality and
Phase6 accepted; final checkpoint fresh artifact closure passed. Source full007
passed665seconds/43checks/745IDs. Native support remains deferred/unverified.
Owner-requested technical Phase8 follows; no final-owner-yes,commit,push or
counterpart source change. Safe command environment is Bash/Python local fixtures,
not the older Markdown-only historical description.

## Historical Planning Baseline: 2026-10-03

Official upstream checkout on clean main at 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1; origin is https://github.com/bracia-plociennik/ai-workflow.git. No remote freshness or CI claim.
Current scope is ignored-artifact planning only. See projects/parallel-task-orchestration-v1/intake/phase-0-repo-intake.md for safe commands, source boundaries and current decisions.
Earlier branch names and execution approvals below are historical, not this run's authority.

## Historical Planning Baseline: 2026-09-29

Current factual refresh: branch `codex/ai-workflow-lean-validation-v1` at `62090f482d47351a162c6558c2bfd8c1a1f9e1f0`, clean tracked worktree. LV001 quality and distillation are complete, and both branch reconciliation and LV001 source are committed locally. The owner approved high-risk LV001-LV006 implementation, synthetic-only eval and one AI System handoff. LV002 spec/source refresh is in progress. Historic snapshots below are retained as history, not current gate evidence; remote freshness was not checked for this refresh.

Implementation readiness observed later on 2026-09-29: planning artifacts still match their reviewed SHA-256s, but the source branch HEAD f362ce3 and cached origin/main 1b45483 diverge at e8b99e8. Autopilot-002 is awaiting-owner; remote freshness and branch reconciliation are required before high-risk source writes. The following planning-range observations remain historical evidence for that completed range.

- Official upstream checkout: `/Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow`.
- HEAD: `f362ce3c0ebb16c36e54bc48bb11b9a71db1548d`; branch `codex/prompt-and-skill-efficiency-core-001`, clean tracked worktree, ahead 2 of locally recorded tracking ref.
- Origin: `https://github.com/bracia-plociennik/ai-workflow.git`. No network refresh, remote parity or CI status claimed.
- Stack includes Bash and Python validation tooling plus Markdown contracts. Earlier Markdown-only descriptions below are historical.
- Active request is ignored-artifact-only planning-range LV001-LV006; no source implementation, benchmarks, model calls or Git changes.
- Evidence: live git status, rev-parse, remote get-url, script inspection and project intake. Historical snapshots below are retained, not current branch or approval evidence.

## Sources Reviewed

- `git status --short --branch`;
- `git branch --all`;
- `git ls-files ai-workflow-workspace`;
- `git check-ignore -v ai-workflow-workspace/repo/core/status.md`;
- `.systems/scripts/check-branch-policy`;
- `.systems/scripts/validate-workflow`;
- repository root listing via `rg --files`;
- `AGENTS.md`;
- `.systems/ai/templates/root-agents.template.md`;
- `HUMANS.md`;
- `README.md`;
- `.systems/ai/core/installation.md`;
- `.systems/ai/core/workflow.md`;
- `.systems/ai/workflow/`;
- `.systems/ai/core/autopilot.md`;
- `ai-workflow-workspace/repo/core/context.md`;
- `ai-workflow-workspace/repo/context/`;
- `ai-workflow-workspace/repo/core/status.md`;
- `ai-workflow-workspace/repo/core/memory.md`;
- `.systems/ai/templates/`;
- `ai-workflow-workspace/projects/README.md`;
- `ai-workflow-workspace/humans/README.md`;
- search for dependency manifests and nested `AGENTS.md`.

## Installation Collision Status

This repository is the upstream AI Workflow template, so root `AGENTS.md`, `HUMANS.md`, `README.md`, `.systems/**`, and `.github/workflows/ai-workflow-validate.yml` are system-owned here.

Current branch state observed on 2026-09-24:

- active branch: `main`;
- current HEAD: `7a904f736eaf029bea750c3a735cd53fa61ef4c0`;
- origin/main: `7a904f736eaf029bea750c3a735cd53fa61ef4c0`;
- remote branches: `origin/main`, `origin/codex/system-insights-memory`, and `origin/codex/update-workspace-script`;
- local `ai-workflow-workspace/` exists as ignored private runtime;
- `git ls-files ai-workflow-workspace` returns no tracked files;
- `.systems/scripts/check-branch-policy` blocks tracked `workspace/**` and `ai-workflow-workspace/**`.

In a target repository, AI Workflow must be installed as a nested clone at `ai-workflow/`. The only target-root file copied or merged by default is `AGENTS.md` from `ai-workflow/.systems/ai/templates/root-agents.template.md`. Target-root `docs/`, `.systems/`, `.github/`, `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, product code, app config, CI, and deployment files remain target-owned.

| Path | Owner | Status | Resolution |
| --- | --- | --- | --- |
| `README.md` | AI Workflow upstream | `current` | Template README for this repo; target repos must not overwrite their README. |
| `AGENTS.md` | AI Workflow upstream | `current` | Internal execution contract for this repo and nested clones; target repos use the shim template, not a direct copy of this file. |
| `.systems/ai/templates/root-agents.template.md` | AI Workflow upstream | `current` | Target-repository root `AGENTS.md` shim source. |
| `HUMANS.md` | AI Workflow upstream | `current` | Human runbook stays at `ai-workflow/HUMANS.md` in target repos; no root `HUMANS.md` copy by default. |
| `.systems/` | AI Workflow upstream | `current` | System workflow docs, templates, examples, skills, and validators. Target-root `.systems/` remains target-owned. |
| `.github/` | AI Workflow upstream | `current` | Template CI in this repo; target-root `.github/` remains target-owned unless owner explicitly installs optional integration. |
| target `ai-workflow/` | AI Workflow nested clone | `not-applicable-upstream` | Target repositories create this by cloning this repo. |

## Command Map

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `not configured` | `missing` | Markdown-only template repo. |
| dev server | `not configured` | `not-applicable` | No app runtime. |
| test | `.systems/scripts/validate-workflow` | `usable` | No-arg is standard; use explicit `--profile full` for high-impact contract changes. |
| lint/style check | `.systems/scripts/check-naming` | `usable` | Enforces Markdown filename policy, with context-only exemptions for preserved legacy input, detailed repo context entries, and project context source materials. |
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
| system ownership | target-repo facts written into root docs or `.systems/ai/` | any repo-specific fact outside `ai-workflow-workspace/repo/`, examples, or project artifacts | keep system docs generic |
| examples | EXAMPLE artifacts mistaken for active workflow state | using EXAMPLE as real PASS evidence | keep EXAMPLE marked documentation-only |
| workflow refs | stale paths after rename | references to legacy human/template/memory paths | run reference searches |
| git/release | destructive history operation | force-push, tag deletion, release publishing | branch + commit after validation |

## Restricted Zones

- secret-bearing files such as `.env*`;
- generated/runtime/cache/build artifacts;
- dependency directories;
- `.systems/**` in target repositories; workflow improvements discovered there must be recorded in `ai-workflow-workspace/external-memory/` instead;
- example artifacts unless the task is explicitly template/example maintenance.

## Artifact Reconciliation

| Artifact | Classification | Action |
| --- | --- | --- |
| `.systems/ai/core/status.md` | current | system-owned pointer to `ai-workflow-workspace/repo/core/status.md` |
| `.systems/ai/core/repo-intake.md` | current | system-owned intake guidance |
| `.systems/ai/core/installation.md` | current | system-owned installation and collision policy |
| `.systems/ai/core/memory.md` and `.systems/ai/memory/` | current | template-local memory router and entries |
| `ai-workflow-workspace/repo/` | current | repo-local runtime docs |
| `ai-workflow-workspace/projects/ai-system/` | removed | Owner-approved local cleanup on 2026-06-10 after the `ai-system` work moved to a separate repository. |
| `ai-workflow-workspace/humans/` | current | canonical human-facing docs path |
| `.systems/ai/templates/projects/` | current | canonical project template path |
| `.systems/ai/templates/humans/` | current | canonical human template path |

## Readiness Checklist

| Check | Result | Notes |
| --- | --- | --- |
| `AGENTS.md` exists and remains system-owned | `PASS` | repo-specific layer moved to `ai-workflow-workspace/repo/` |
| `.systems/ai/templates/root-agents.template.md` exists | `PASS` | target root shim delegates to `ai-workflow/AGENTS.md` |
| `HUMANS.md` exists and remains system-owned | `PASS` | human runbook updated |
| `.systems/ai/` workflow/template docs exist | `PASS` | phase files and templates present |
| `ai-workflow-workspace/repo/core/context.md` exists as router and `ai-workflow-workspace/repo/context/` describes the repository | `PASS` | filled for this template repo |
| `ai-workflow-workspace/repo/core/status.md` exists and is coherent | `PASS` | no active blocker; updated for main-only local workspace model |
| `ai-workflow-workspace/repo/core/memory.md` and `ai-workflow-workspace/repo/memory/README.md` exist | `PASS` | empty repo memory router and entry directory |
| detailed workflow phase files exist | `PASS` | includes `phase-0-repo-intake.md`, `phase-0-project-workspace.md`, and `phase-0-idea-validation.md` |
| templates exist | `PASS` | includes `.systems/ai/templates/repo/` |
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
- files read: `AGENTS.md`, `HUMANS.md`, `README.md`, `.systems/ai/core/workflow.md`, `.systems/ai/workflow/*`, `.systems/ai/core/autopilot.md`, `.systems/ai/templates/*`, `ai-workflow-workspace/projects/README.md`, `ai-workflow-workspace/humans/README.md`;
- missing files confirmed: app manifests such as `package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, and nested `AGENTS.md` were not detected;
- git status observed: working tree contains the nested-clone installation model update during this quality pass;
- validation passed: `git diff --check`;
- validation passed: `.systems/scripts/validate-workflow`;
- validation passed: `.systems/scripts/check-naming`;
- validation passed: `.systems/scripts/check-required-artifacts`;
- validation passed: `.systems/scripts/check-status-consistency`;
- validation passed: `.systems/scripts/check-qa-evidence`;
- validation passed: no stale legacy path or runtime-blocker references found in the configured reference search;
- validation passed: optional external review wording appears only in the human runbook;
- validation passed: workflow route includes repo intake, project workspace, idea validation, project context, and project/context intake before architecture.
- validation baseline refreshed on 2026-08-10: `.systems/scripts/check-branch-policy` and `.systems/scripts/validate-workflow --profile fast --explain`;
- status observed on 2026-08-10: `## main...origin/main`;
- branch state observed on 2026-08-10: active `main`, synchronized with `origin/main`;
- local workspace tracking check on 2026-08-10: `git ls-files ai-workflow-workspace` returned no files.
- repo baseline refreshed on 2026-09-24: `main` and `origin/main` both resolve to `7a904f736eaf029bea750c3a735cd53fa61ef4c0`; `git status --short --branch` returned `## main...origin/main` with no tracked changes.
- local workspace tracking check on 2026-09-24: `git ls-files ai-workflow-workspace` returned no files; `git check-ignore -v ai-workflow-workspace/repo/core/status.md` confirmed `.gitignore:3:/ai-workflow-workspace/`.
