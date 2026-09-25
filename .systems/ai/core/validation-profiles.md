# validation-profiles.md

## Purpose

Validation Profiles define faster local validation paths without weakening the final safety gate.

Default `.systems/scripts/validate-workflow` with no arguments is the `standard` profile. It is a daily AI Workflow iteration validator, not a default product-implementation QA command.

Profiles may reduce iteration time, but they must not change Definition of Done, PASS Integrity, quality closure, risk policy, permissions, evidence requirements, phase gates, owner approvals, CI behavior, or commit readiness.

## Profiles

| Profile | Intended use | Final validation evidence |
| --- | --- | --- |
| `full` | Checkpoint validation, major distillation, major verification, CI, release/final confidence checks, and high-impact workflow-template changes | `yes`, unless smoke tests are explicitly skipped and residual risk is reported |
| `standard` | Daily AI Workflow iteration and normal workflow-maintenance checks when workflow validation is applicable | `yes` for applicable ordinary workflow work; `no` when a full-required gate applies |
| `scoped` | Local iteration for one or more explicitly selected validators | `no` unless the owner explicitly accepts narrow validation with residual risk |
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

CI must call `.systems/scripts/validate-workflow --profile full` explicitly.

If `AI_WORKFLOW_SKIP_SMOKE_TESTS=1` is used, the result is not eligible for full validation evidence unless the owner explicitly accepts the residual risk.

## Scoped Profile

`scoped` runs fast base checks and the explicit validators named in `--checks`.

Use it only when iterating on a known validator or small docs area. It must not be described as enough before commit, enough before push, or equivalent to `full`.

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
