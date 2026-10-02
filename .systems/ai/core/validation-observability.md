# Validation Observability And Smoke Partition

Whole-process timing follows `.systems/ai/core/execution-efficiency.md`: observed monotonic intervals, union of overlaps, rerun reason and input fingerprints. Keep model/reading time unknown without telemetry and estimates separate; synthetic script savings cannot prove whole-agent speedup.

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

LV002 timing uses monotonic nanoseconds and a versioned TSV. Its first five
columns remain `command/check_id`, `group`, `duration_seconds`, `result`, and
`profile`; v2 appends `schema_version`, `run_id`, `record_kind`, and `parent_id`.
An older five-column reader must reject the v2 header explicitly if it cannot
ignore appended columns. The timing sink must be a new ignored-workspace or
temporary file; symlink, tracked, unrelated existing and escaping paths fail
before validation begins. Timing files contain no command output.
The run ID binds a SHA-256 digest of the tracked and non-ignored untracked
source tree at start; validation rechecks that digest at completion. A changed
source tree makes the timed run fail. Capture recomputes the digest before
freezing its manifest; later comparisons verify the manifest against the
frozen timing file without demanding that an intentionally older baseline
still equal the candidate checkout.

Use `.systems/scripts/report-validation-comparison capture` immediately after
each complete or failed timed run to freeze a private manifest containing the
timing digest, source digest, revision, runtime, scope/input fingerprint and
setup regime. Keep timing and manifest in the same ignored or temporary
directory; v2 stores only the timing file name, not an absolute host path.
Scope, input and setup fingerprints are safe opaque identifiers, never paths
or raw workspace contents; their equivalence still requires operator review.
Existing local v1 manifests can be read only when their timing file remains
beside the manifest. A failed/timeout/interrupted run is retained as incomplete and
cannot enter a performance comparison. `summarize` requires at least three
complete same-source/same-input/same-environment full runs. `compare` requires
matching coverage and input across baseline/candidate manifests; different
reviewed source revisions are expected. It reports wall-clock separately from
child durations, smoke wall and unattributed shared setup. Do not add parent
smoke wall to individual smoke-test durations. The conservative screening
rule requires every candidate wall duration below every baseline duration and
median gain above five percent; other results are inconclusive, not slower
or faster proof. Source/code changes after a capture invalidate comparisons
unless each run's frozen manifest still matches its timing and source evidence.

The default `--group all` preserves the complete smoke suite. Named groups now
execute only their owned cases, assertions and setup in independent disposable
source fixtures. The public dispatcher validates `smoke/manifest.json` and its
live coverage index before launching any group. Group files are internal:
invoke them through `check-validator-smoke-tests`, not as public entrypoints.

The accepted partition preserves 674 reference IDs, 110 audited outside-wrapper
points (including failure branches and a failure fixture), and 34 nested Python
assertions. Whole reference regions retain their exact bytes and transaction
boundaries; pure helpers live in `smoke/common.sh`. Additional regression cases
are explicitly supplemental, not replacements for old cases. The manifest binds
each test's group, command/outcome contract, setup, mutation and cleanup, each
assertion's actual source line, frozen region digests and current group/helper
digests. Missing, duplicate, moved or unmapped coverage fails closed.

Public lifecycle markers remain `AI_WORKFLOW_SMOKE_START` and exactly one
`AI_WORKFLOW_SMOKE_COMPLETE`; group markers use `AI_WORKFLOW_SMOKE_GROUP_START`
and `AI_WORKFLOW_SMOKE_GROUP_COMPLETE`. An all run has one `smoke-suite-wall`
timing parent, while all child records retain profile `smoke-all`. A named group
has a subset profile and is not full validation evidence. Full and CI still run
all five groups sequentially, including supplemental cases.

The supervisor requires Python 3 and local `ps` process metadata (PID, PPID,
start time and status) for identity-bound cleanup. It checks that capability
before launching children. A sandbox that denies it fails explicitly; request
only the needed platform permission rather than disabling cleanup. Interrupt,
timeout, child failure, incomplete execution or cleanup failure cannot yield a
successful completion. The supervisor retains observed owned descendants while
the group runs; it is not a sandbox for arbitrary malicious detached processes.

Maintain the manifest atomically with group/helper changes. New cases need
unique supplemental IDs and command/outcome contracts; a change to a preserved
reference region requires a fresh assertion/behavior audit, not only a new
file hash. Before accepting membership or helper changes, compare the frozen
reference and candidate, repeat standalone groups in a different order, compare
typed rejection diagnostics and protected mutations, and test lifecycle/tree
cleanup. Recover the pre-partition reference from the reviewed parent revision
when needed. If equivalence is incomplete, retain or restore the monolith via
the approved fix/rollback route; do not reduce coverage to meet a timebox.
Group isolation reduces the eligible iteration scope, not the full safety gate.
No full-suite speedup follows merely from this partition or one timing run.

Green workflow scripts remain supporting evidence. Semantic QA, product checks,
DoD, findings, blockers, and residual risk determine quality.
