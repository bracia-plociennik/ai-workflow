# validation-profiles.md

`.systems/ai/core/execution-efficiency.md` adds a distinct source-backed artifact-closure route: after one fresh full gate for unchanged sources, validate new owned Phase 6/7/8 artifacts with fresh runtime consumers. This is not arbitrary scoped final evidence and not a full-profile cache. Iteration `--execution-plan` evidence remains unverified/non-final. CI/updater/release full execution is unchanged.

## Purpose

Validation Profiles define faster local validation paths without weakening the final safety gate.

Default `.systems/scripts/validate-workflow` with no arguments is the `standard` profile. It is a daily AI Workflow iteration validator, not a default product-implementation QA command.

Profiles may reduce iteration time, but they must not change Definition of Done, PASS Integrity, quality closure, risk policy, permissions, evidence requirements, phase gates, owner approvals, CI behavior, or commit readiness.

## Profiles

| Profile | Intended use | Final validation evidence |
| --- | --- | --- |
| `full` | Checkpoint validation, major distillation, major verification, CI, release/final confidence checks, and high-impact workflow-template changes | `yes`, unless smoke tests are explicitly skipped and residual risk is reported |
| `standard` | Daily AI Workflow iteration and normal workflow-maintenance checks when workflow validation is applicable | `yes` for applicable ordinary workflow work; `no` when a full-required gate applies |
| `scoped` | Explicit checks and dependency closure, bounded to declared runtime roots | Conditional runtime-only checkpoint evidence; otherwise iteration or owner-accepted narrow evidence |
| `fast` | Quick sanity check during editing | `no` |

## Script Interface

`.systems/scripts/validate-workflow` supports:

- no arguments: same as `--profile standard`;
- `--profile full`;
- `--profile standard`;
- `--profile scoped --checks <check-a,check-b>`;
- `--profile fast`;
- `--project <slug>` with any profile to scope runtime status, QA evidence, and naming to one existing project while retaining global product and non-project workspace checks;
- `--explain` with any profile.
- `--scope-manifest <path>` only with `scoped`; optional, but necessary for verified coverage.

`--checks` is valid only with `--profile scoped`. Scoped checks must be explicit script basenames such as `check-validation-profiles`; automatic changed-file inference is intentionally out of scope for v1.

`--explain` must report:

- selected profile;
- whether smoke tests run;
- whether the result qualifies as final validation evidence;
- any explicit scoped checks.

## Standard Profile

`standard` runs the core validator and structural checks but does not run embedded `check-validator-smoke-tests`.

Use it for normal daily AI Workflow iteration and routine workflow maintenance after semantic review. Do not run it by default for ordinary product implementation, PDF/document/design work, or unrelated code QA. If work reveals validator changes, high-impact contract changes, checkpoint-level synchronization, major distillation, major verification, or release/final confidence needs, escalate to `full`.

Use `.systems/ai/core/validation-routing.md` to decide applicability. Workflow scripts remain supporting evidence and never replace semantic QA, product tests, findings-first review, or final verdict reasoning.

## Full Profile

`full` runs the complete validator chain and `check-validator-smoke-tests`.

Use it for checkpoint validation, major distillation, major verification, CI, release/final confidence checks, and high-impact workflow-template changes.

Checkpoint exceptions are the bounded runtime-only manifest policy below and
the explicit authenticated source-backed artifact-closure route in execution-efficiency.md.
It does not apply to source/system-impact checkpoints or broader memory namespaces.

CI must call `.systems/scripts/validate-workflow --profile full` explicitly.

If `AI_WORKFLOW_SKIP_SMOKE_TESTS=1` is used, the result is not eligible for full validation evidence unless the owner explicitly accepts the residual risk.

## Scoped Profile

`scoped` runs only explicit checks and their declared dependency closure from
`.systems/scripts/lib/validation-checks.json`. It has no unconditional fast
prelude. Identical check/root/project invocations run once; different runtime
roots receive separate invocations and privacy-safe timing IDs. Framework
policy checks run once, not once per project.

The strict JSON scope manifest is generated read-only by
`.systems/scripts/lib/validation-scope.py snapshot`. It binds canonical repository
and workspace identity, approved Git base, observed HEAD, implementation scope,
NUL-safe committed/staged/unstaged/untracked/rename/deletion inventory and hashes,
framework source digest, and a separate ignored-runtime inventory. It must be
fresh before and after execution. It is evidence, never permission or secret-read
approval. All Git changes must fit the declared scope; deleted required sources,
missing/unreadable roots, unknown dependencies, cycles and symlink escapes fail.

Supported runtime roots are `repo/core` and `projects/<slug>`. Canonical direct
Markdown and project-owned artifact directories are inspected; raw `context/`,
eval fixture, legacy and dump trees are supporting data, not active producers.
Foreign repositories or links in owned artifact directories are rejected. The
single project-relative dependency directory `quality/artifacts/node_modules`
is supporting tooling, not active evidence: inventory explicitly reports and
prunes this directory (including a symlink or dangling symlink) without following
it. No other `node_modules` path or symlink is exempt. Direct evidence references
into this excluded directory are rejected even when it is a real directory.
This fixed classification adds no arbitrary exclusions or permission to read
dependency targets; schema1 still inventories only active owned files. The
legacy QA registry is separately bound as supporting evidence when present.
Known tracked runtime edits inside those selected owned roots are bound by both
Git and runtime inventories; they do not become framework changes solely because
the target workspace is tracked. Missing/deleted artifacts, raw supporting trees
or edits outside the selected roots cannot qualify as complete scoped coverage.
Repo status with an active project requires that project's root too. Capture to
External Memory/System Insights or another unsupported namespace requires its
applicable checks and escalation; it cannot be called complete by this manifest.

Output distinguishes `execution_result` from `coverage_result`:
`complete|incomplete|unverified`, with requested, required, executed, skipped IDs,
reason and `final_evidence_eligible`. No manifest means unverified/ineligible.
A changed shared/framework source or unknown Git impact means
`full-required-source-impact`, even when every requested check passes.

A runtime-only checkpoint may use scoped evidence only when the manifest has
`intent: checkpoint`, all runtime-required dependencies are included, framework
source is unchanged, all selected artifacts are bounded and fresh, checks pass,
and semantic QA/privacy/capture applicability is separately established. This
does not replace formal QA, owner approvals or full-required gates for source
changes, CI, updater, release, major verification or high-impact maintenance.
`complete` for an iteration manifest is still ineligible for checkpoint closure.

Save the manifest and live timing/log output outside the assessed runtime roots
(for example in approved standalone `/tmp` artifacts). They must not mutate the
frozen input inventory during execution. Record the finished result in project
evidence afterward; a subsequent validation needs a new snapshot. Runtime scans
do not inspect raw supporting trees, and manifest generation is not permission
to read secret-bearing inputs.

Outside that bounded checkpoint case, use it for iteration on known validators
or small docs areas. It must not be described as enough before commit, enough
before push, or equivalent to `full`.

## Fast Profile

`fast` runs cheap sanity checks only:

- `git diff --check` when running inside a git repository;
- `check-required-artifacts`;
- `check-branch-policy`;
- `check-naming`;
- `check-status-consistency`;
- `check-qa-evidence`;
- `check-contract-compliance`.

Use it for quick feedback during edits. `fast` is not final validation evidence.

## Safety Boundaries

Validation profiles must not:

- make `fast` or `scoped` enough before commit for workflow-template maintenance without owner acceptance and residual risk;
- make `standard` enough for checkpoint validation, major distillation, major verification, CI, release/final confidence checks, or high-impact workflow-template changes;
- let skipped smoke tests count as `PASS`;
- bypass full validation for high-impact workflow files without explicit owner acceptance and residual risk;
- weaken CI;
- weaken PASS Integrity, Default Quality Closure, Implementation Slicing, contract compliance, knowledge capture, risk, permissions, evidence, phase gates, or owner approvals.

Skipped full validation must be reported with:

- profile used;
- checks run;
- checks skipped;
- reason;
- residual risk;
- owner approval, when narrow validation is accepted.
