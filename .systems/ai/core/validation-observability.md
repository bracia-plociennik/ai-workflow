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
