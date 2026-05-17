# REPO-INTAKE.md

## Purpose

`docs/ai/REPO-INTAKE.md` is the repo-level intake artifact for the AI workflow system.

Use it when a repository is new, when `ai-workflow` has just been copied into a repository, or when there is not yet any active project workspace under `docs/projects/<project>/`.

This file answers one question:

```text
Is this repository ready to use AGENTS.md, HUMANS.md, workflow docs, project docs and autopilot safely?
```

It does not replace:

- `AGENTS.md` as the execution contract;
- `HUMANS.md` as the human runbook;
- `docs/ai/WORKFLOW.md` as the phase router;
- `docs/ai/workflow/` as detailed process rules;
- `docs/projects/<project>/intake/0_initial_audit.md` as a project/context-specific audit.

## Relationship To Project Intake

Use this split:

| Artifact | Scope | Use When | Output |
| --- | --- | --- | --- |
| `docs/ai/REPO-INTAKE.md` | repo-level workflow readiness | no active project exists, workflow was just installed, or repo-wide workflow drift is suspected | confirms that the repo can safely run the workflow/autopilot system |
| `docs/projects/<project>/intake/0_initial_audit.md` | project/context-specific intake | a concrete project, feature, product area, context, or plan exists | prepares architecture and planning for that project |

`REPO-INTAKE.md` may exist before any `docs/projects/<project>/` directory exists.

`0_initial_audit.md` should not be forced until a real project workspace or project context exists.

## Template Status

This template file is intentionally repository-neutral.

After copying `ai-workflow` into a real repository, run repo intake and replace this section with the repository's actual repo-level intake snapshot.

Minimum snapshot fields:

| Field | Value |
| --- | --- |
| `repo_name` | `<fill during repo intake>` |
| `repo_path` | `<fill during repo intake>` |
| `date` | `<YYYY-MM-DD>` |
| `result` | `<PASS|BLOCKED>` |
| `active_project_workspace` | `<none|docs/projects/<project>>` |
| `workflow_ready` | `<yes|no>` |
| `autopilot_ready` | `<yes|no|not_applicable>` |
| `owner_action_required` | `<none|specific action>` |

## Update Rules

Update this file when:

- adding `ai-workflow` to a new repository;
- creating the first project workspace;
- changing canonical docs layout;
- changing workflow/autopilot rules;
- changing repo-level status, memory, templates or required artifacts;
- changing repo-level safe command policy;
- changing STOP conditions, side-effect policy, secret policy, migration policy or git policy;
- repo-level docs drift is detected.

Do not store task implementation details here. Those belong in project specs, quality evidence, distillations or checkpoints.

## Repo-Level Intake Contract

Every concrete repo intake should fill these sections.

### Metadata

| Field | Value |
| --- | --- |
| `repo_name` | `<fill during repo intake>` |
| `repo_path` | `<fill during repo intake>` |
| `date` | `<YYYY-MM-DD>` |
| `result` | `<PASS|BLOCKED>` |
| `active_project_workspace` | `<none|docs/projects/<project>>` |
| `workflow_ready` | `<yes|no>` |
| `autopilot_ready` | `<yes|no|not_applicable>` |
| `owner_action_required` | `<none|specific action>` |

### Sources Reviewed

Minimum source list:

- repository root listing;
- `AGENTS.md`;
- `HUMANS.md`;
- `README.md`, if present;
- `docs/ai/WORKFLOW.md`;
- `docs/ai/workflow/`;
- `docs/ai/AUTOPILOT.md`;
- `docs/ai/STATUS.md`;
- `docs/ai/REPO-INTAKE.md`;
- `docs/ai/EXTERNAL-MEMORY.md`;
- `docs/ai/REPO-MEMORY.md`;
- `docs/ai/templates/`;
- `docs/projects/README.md`, if present;
- `docs/human/README.md`, if present;
- dependency manifests such as `composer.json`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, etc.;
- test/build/lint config files;
- local/nested `AGENTS.md` files;
- git status and current branch.

### Required AI Workflow Files

| File or Directory | Required | Status | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | yes | `<present|missing|incomplete>` | execution contract |
| `HUMANS.md` | yes | `<present|missing|incomplete>` | human operating guide |
| `docs/ai/README.md` | yes | `<present|missing|incomplete>` | repo-level AI docs index |
| `docs/ai/REPO-INTAKE.md` | yes | `<present|missing|incomplete>` | repo-level workflow bootstrap intake |
| `docs/ai/WORKFLOW.md` | yes | `<present|missing|incomplete>` | phase router |
| `docs/ai/workflow/` | yes | `<present|missing|incomplete>` | detailed phase rules |
| `docs/ai/AUTOPILOT.md` | yes | `<present|missing|incomplete>` | autopilot launch contract |
| `docs/ai/STATUS.md` | yes | `<present|missing|incomplete>` | repo-level status |
| `docs/ai/EXTERNAL-MEMORY.md` | yes | `<present|missing|incomplete>` | universal workflow/process memory |
| `docs/ai/REPO-MEMORY.md` | yes | `<present|missing|incomplete>` | aggregate repo memory only |
| `docs/ai/templates/` | yes | `<present|missing|incomplete>` | reusable templates |
| `docs/projects/README.md` | recommended | `<present|missing|incomplete>` | project workspace index |
| `docs/human/README.md` | recommended | `<present|missing|incomplete>` | human docs index |

### Required Workflow Phase Files

Verify that `docs/ai/workflow/` contains detailed rules for:

- `00_overview.md`;
- `0_repo_intake_initial_audit.md`;
- `1_architecture.md`;
- `1_5_architecture_qa.md`;
- `1_7_architecture_fix_loop.md`;
- `2_project_plan.md`;
- `2_5_plan_qa.md`;
- `2_6_plan_fix_loop.md`;
- `2_7_task_packaging.md`;
- `2_9_packaging_qa.md`;
- `2_9_1_package_fix_loop.md`;
- `3_specification.md`;
- `3_5_spec_qa.md`;
- `3_7_spec_fix_loop.md`;
- `4_implementation.md`;
- `5_quality.md`;
- `5_5_fix_loop.md`;
- `6_distillation.md`;
- `7_checkpoint.md`;
- `8_final_check.md`.

### Canonical Layout Check

Expected repo-level layout:

```text
AGENTS.md
HUMANS.md
docs/
  ai/
    README.md
    REPO-INTAKE.md
    WORKFLOW.md
    AUTOPILOT.md
    STATUS.md
    EXTERNAL-MEMORY.md
    REPO-MEMORY.md
    workflow/
    templates/
  projects/
    README.md
    <project>/
  human/
    README.md
```

Expected project layout after a project exists:

```text
docs/projects/<project>/
  README.md
  STATUS.md
  PROJECT-MEMORY.md
  PLANS.md
  CODE-REVIEW.md
  intake/
  architecture/
  planning/
  specs/
  quality/
  decisions/
  escalations/
  distillations/
  checkpoints/
  autopilot/
```

### Repo Adaptation Layer

Record the discovered commands or mark them as missing:

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `<command or missing>` | `<usable|missing|unsafe>` | |
| dev server | `<command or missing>` | `<usable|missing|unsafe>` | |
| test | `<command or missing>` | `<usable|missing|unsafe>` | |
| lint/style check | `<command or missing>` | `<usable|missing|unsafe>` | |
| typecheck | `<command or missing>` | `<usable|missing|unsafe>` | |
| build | `<command or missing>` | `<usable|missing|unsafe>` | |
| scheduler/queue | `<command or missing>` | `<usable|missing|unsafe>` | |
| safe inspection | `<command or missing>` | `<usable|missing|unsafe>` | |

Do not invent commands. If a command cannot be discovered from repo state, write `missing`.

### Safe Environment

Record:

- safe test environment;
- safe database strategy;
- fake/log/array/test service strategy;
- dependency install policy;
- dev server policy;
- migration policy;
- external connector QA policy;
- secret/credential policy.

### Repo Risk Register

Record repo-level high-risk areas:

| Area | Risk | STOP Condition | Safe Default |
| --- | --- | --- | --- |
| secrets | plaintext, credentials, production env | production/private secret access | fake/test references only |
| database | destructive migration or real data change | destructive or production DB operation | additive test migration only |
| external effects | emails, alerts, tickets, API writes | real customer/user side effect | fake/log/array/test adapters |
| legal/ToS | scraping, paid vendor, privacy | legal/ToS-sensitive action | STOP for owner approval |
| git/release | force-push, tag deletion, release | destructive git/release operation | branch + commit after PASS |

Add repo-specific risks during intake.

### Artifact Reconciliation

Classify existing workflow/docs artifacts:

| Artifact | Classification | Action |
| --- | --- | --- |
| `<path>` | `<current|incomplete|outdated|conflicting|duplicate|historical>` | `<reuse|update|stop|defer>` |

Do not delete duplicates during repo intake unless the owner explicitly asks.

### Readiness Checklist

| Check | Result | Notes |
| --- | --- | --- |
| `AGENTS.md` exists and is adapted to the repo | `<PASS|FAIL>` | |
| `HUMANS.md` exists | `<PASS|FAIL>` | |
| `docs/ai/REPO-INTAKE.md` exists | `<PASS|FAIL>` | |
| `docs/ai/STATUS.md` exists and is coherent | `<PASS|FAIL>` | |
| `docs/ai/WORKFLOW.md` routes phases correctly | `<PASS|FAIL>` | |
| detailed workflow phase files exist | `<PASS|FAIL>` | |
| `docs/ai/AUTOPILOT.md` exists | `<PASS|FAIL>` | |
| `docs/ai/EXTERNAL-MEMORY.md` exists | `<PASS|FAIL>` | |
| templates exist | `<PASS|FAIL>` | |
| canonical docs layout is clear | `<PASS|FAIL>` | |
| repo adaptation layer is discovered or marked missing | `<PASS|FAIL>` | |
| safe test environment is known or explicitly missing | `<PASS|FAIL>` | |
| high-risk areas are identified | `<PASS|FAIL>` | |
| restricted/generated/runtime zones are identified | `<PASS|FAIL>` | |
| real external effects are disabled by default or require STOP | `<PASS|FAIL>` | |
| secret policy is explicit | `<PASS|FAIL>` | |
| migration policy is explicit | `<PASS|FAIL>` | |
| retry/checkpoint/git policy is explicit | `<PASS|FAIL>` | |
| no project workspace is required for repo-level readiness | `<PASS|FAIL>` | |

### Owner Decisions Required

Record only decisions that block safe workflow setup or autopilot setup:

| Decision | Class | Recommendation | Alternative | Blocks |
| --- | --- | --- | --- | --- |
| `<decision>` | `<auto-resolvable|high-impact|critical-risk|blocked-by-missing-facts>` | `<recommendation + impact>` | `<alternative + impact>` | `<yes|no>` |

### Gate Decision

Repo-level intake can pass when:

- required workflow docs exist or missing items are explicitly marked and non-blocking;
- `AGENTS.md` and `HUMANS.md` exist or their absence is the explicit blocker;
- canonical docs layout is clear;
- safe command/test policy is known or marked missing;
- STOP conditions are explicit;
- no unresolved blocker prevents project creation or workflow use.

Gate result:

```text
result: <PASS|BLOCKED>
blocking_reason: <none|reason>
next_valid_step: <create project workspace|project intake|fix repo workflow docs|owner decision>
```

### Evidence

Record the concrete checks used for the result:

- commands run;
- files read;
- searches performed;
- missing files confirmed;
- git status observed;
- validation commands that passed or failed.

Do not mark `PASS` without evidence.

