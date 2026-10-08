# Validation Baseline Evidence

## Scope

- Baseline date: `2026-08-10`
- Repository: `/Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow`
- Profile: `check-validator-smoke-tests --group all`
- Purpose: measure current cost before any smoke-suite split.
- Output contains command/check IDs, groups, durations, results, and profile only.

## Runs

- Successful runs: `3/3`
- Smoke-test records per run: `532`
- Smoke-test IDs per run: unique, each ID occurs exactly once within its run.
- Coverage change: none; the existing monolith remains the execution path.
- Equivalence audit: `not completed`; named groups remain compatibility labels.

## Median Cost Classes

Cost thresholds: `fast <2s`, `medium 2-15s`, `slow >15s`.

| Group | Records across 3 runs | Median per check | Cost class | Interpretation |
| --- | ---: | ---: | --- | --- |
| core | 276 | 0s | fast | Individual core checks are usually cheap; some outliers exist. |
| policy | 651 | 0s | fast | Individual policy checks are usually cheap. |
| quality | 477 | 1s | fast | Individual quality checks are usually cheap. |
| skills | 147 | 1s | fast | Individual skill checks are usually cheap. |
| workspace | 45 | 0s | fast | Individual workspace checks are usually cheap. |
| full smoke runner | 3 full observations | 389s observed final run | slow | The monolithic setup and shared assertions dominate total cost. |

## Decision

Do not split the smoke suite in this scope. The public `--group` interface is
available for measurement and compatibility, but each group still runs the
complete monolith until a separate equivalence audit proves safe partitioning.

## Evidence Paths

- Final full-profile timing: `/tmp/ai-workflow-health-final.tsv`
- Three-run baseline timing: `/tmp/ai-workflow-health-baseline.tsv`
- Validation command: `.systems/scripts/validate-workflow --profile full --timing-output <path> --explain`

## Limits

The timing resolution is whole seconds, so fast checks report `0s` or `1s`.
The baseline is advisory performance evidence and does not change workflow
gates, PASS Integrity, or required full validation.
