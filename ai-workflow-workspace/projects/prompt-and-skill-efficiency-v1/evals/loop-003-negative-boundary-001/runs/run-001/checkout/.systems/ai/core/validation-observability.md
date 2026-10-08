# Validation Observability And Smoke Partition

## Purpose

Validation observability measures cost before changing validation coverage. It
does not replace semantic QA, product checks, findings-first review, or PASS
Integrity.

Interfaces:

```sh
.systems/scripts/validate-workflow --profile <full|standard|scoped|fast> \
  --timing-output <workspace-or-tmp-path>
.systems/scripts/check-validator-smoke-tests --group <all|core|policy|quality|skills|workspace>
```

Validation lifecycle is observable even when a check is slow. Valid runs emit
`AI_WORKFLOW_VALIDATE_START`, `AI_WORKFLOW_VALIDATE_PROGRESS`, and exactly one
`AI_WORKFLOW_VALIDATE_COMPLETE` marker. The smoke runner emits the equivalent
`AI_WORKFLOW_SMOKE_*` markers and reports the active smoke-test ID. Use
`--progress quiet|summary|verbose`; `summary` is the default and `verbose`
prints every smoke-test result.

Each nested check is run through `.systems/scripts/run-with-timeout` without
shell interpolation. The default top-level check timeout is 1200 seconds and
the default individual smoke-test timeout is 180 seconds. A timeout returns
code `124`, terminates the child process group, and produces a `timeout`
completion result. Timeout values may be changed explicitly, but timeouts do
not reduce full-profile coverage.

Canonical nested-clone updates report `equal`, `behind`, `ahead`, or `diverged`
state before validation; `ahead` and `diverged` are stop conditions.

Timing records only command/check ID, group, duration, result, and profile. It
must not record repository contents, prompts, secrets, client data, or command
output. Cost classes use the median of three runs: `fast <2s`, `medium 2-15s`,
`slow >15s`.

The default `--group all` preserves the complete smoke suite. In v1, named
groups are compatibility labels for timing runs and still execute the complete
monolith because shared setup/assertions have not passed an equivalence audit.
A future split must preserve every existing smoke-test ID exactly once and pass
that audit before it changes execution. If equivalence is incomplete, retain
the monolith and ship observability only.

Green workflow scripts remain supporting evidence. Semantic QA, product checks,
DoD, findings, blockers, and residual risk determine quality.
