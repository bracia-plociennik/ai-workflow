# Phase 4 Implementation: LV002

## Source And Scope

- Source: accepted LV002 specification and current Spec QA dependency recheck at `62090f482d47351a162c6558c2bfd8c1a1f9e1f0`.
- Work mode: formal implementation-range; risk: high; approval: LV-DEC-002.
- DoD source: LV002 task contract and V2-01..09 in the accepted specification.
- Artifact QA route: completed phase-3-spec-qa; implementation quality route: phase-5-quality.
- Current write ceiling: eight tracked paths in the spec; this ignored implementation artifact is supporting evidence.
- Delivery constraint: owner opted out of deadline/timebox; no quality reduction.

## Implementation Slice Plan

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| LV002-A | Safe, precise, versioned timing records | new validation-timing.py | unsafe sink and schema cases reject without overwrite | targeted CLI tests and source review | completed |
| LV002-B | Instrument validation and smoke while preserving exit behavior | validate-workflow, check-validator-smoke-tests | full run and negative failure/timeout cases retain verdict | timing sample, targeted smoke, failure-path trace | completed |
| LV002-C | Compare complete equivalent manifests conservatively | new report-validation-comparison | complete/incomplete and mismatch fixtures classify correctly | synthetic fixtures, manual trace | completed |
| LV002-D | Contract, docs, and frozen baseline | check-validation-observability, validation-observability.md, commands.md, README.md | three complete full runs on one frozen revision/input | private manifests, timing files, semantic QA then scripts | completed |

Stop on write-set expansion, unsafe output, altered coverage/exit behavior, missing comparable runs or a material finding. No source optimization or LV003 work in this scope.

## Slice Execution Evidence

### LV002-A: Timing Sink

- Added monotonic nanosecond collection and a versioned TSV retaining the legacy first five columns. `now`, `init` and `record` separate measurement from report comparison.
- Path containment rejects symlinks, escaping or tracked targets and existing output. `O_EXCL` prevents an existing timing file from being truncated. The full smoke suite covers sub-second precision and negative sink cases.
- Failure path reviewed: invalid timing metadata or a failed record write exits nonzero instead of producing a successful timing record.

### LV002-B: Validation And Smoke Instrumentation

- Top-level validator checks, individual smoke IDs, smoke-suite wall and validation wall are separate records under one source-bound run ID. Existing completion-marker and child exit behavior is retained.
- Existing LV001 negative-status and diagnostic assertions still precede timing writes. The shared smoke runner changed, so a fresh LV001 regression assessment was appended to its formal quality artifact; original and first regression assessments remain historical. Project-scoped QA and status validators pass for that current report.
- An initial smoke run was invalid because the source was edited while it executed; it ended nonzero and is not used as evidence. After the final source edit, the frozen-source all-group smoke run passed in 492 seconds.

### LV002-C: Comparison And Adversarial Review

- Added capture, summarize and compare interfaces. A manifest binds timing-file SHA-256, source digest, HEAD, runtime, profile, declared scope/input/setup identifiers, full check IDs and smoke-test IDs. v2 stores only the timing file name beside its manifest; local v1 evidence remains readable under same-directory containment.
- The full-current-diff review found and repaired three false-completeness/privacy paths before the final baseline: a smoke wall without its top-level check, impossible smoke-wall nesting or nonfinite duration, and absolute/private path material in the manifest or fingerprint. Adversarial smoke cases now reject these inputs.
- Exact check/test ID arrays provide an inspectable inventory and are compared across runs. The source-bound successful full runner provides the expected full execution context; a declared input fingerprint alone is not proof of identical runtime inputs, so workspace/input stability also requires manual review.

### LV002-D: Frozen Post-Correction Baseline

- Final source digest: `4d3dfad031fcd5f0e9724f7852a19b66717af73e51a1be607bd9f0ec0b9bfbf6`; HEAD: `62090f482d47351a162c6558c2bfd8c1a1f9e1f0`. No tracked source was edited during the three final runs.
- All three `validate-workflow --profile full --progress quiet --timing-output ...` runs emitted `result=pass`, with `smoke-all/pass`, 40 check IDs and 654 smoke-test IDs each. The complete manifests are `lv002-final-baseline-001.json`, `002.json`, `003.json` beside their TSV files in this ignored implementation directory.
- Full wall durations: 609.855898, 609.863651 and 607.384199 seconds; median 609.855898, min 607.384199, max 609.863651. The spread is about 2.48 seconds. These are baseline costs, not evidence of an optimization gain.
- The earlier three full manifests with source digest `005bfde6e1e52cea67d222c9daea2e165fda965726bc76b851d5fb82797ebf7c` are preserved as pre-fix historical measurements and excluded from the final baseline.
- `git diff --check`, Bash/Python syntax, `check-validation-observability`, project-scoped QA/status checks, complete smoke suite and three explicit full validations passed. `git ls-files ai-workflow-workspace` is empty. Linux CI is unrun because no commit or push was requested.

## Pre-Phase-5 Quality Review

- Owner intent, accepted plan/spec and V2-01..09 reviewed against all eight proposed tracked paths; no out-of-scope source change found.
- Findings-first current-diff review and post-fix re-review covered path safety, source/input/coverage identity, malformed or partial timing, wall/child nesting, false speed claims, privacy, exit status and completion markers. The material findings found during implementation were fixed and retested before the final baseline; no unresolved material finding is known.
- The manual producer-consumer trace followed `validate-workflow` -> timing helper -> smoke runner -> TSV -> capture manifest -> summarize. A failed/incomplete or mismatched run cannot enter the three-run comparison. Scripts are supporting evidence; they do not grant the formal quality verdict.
- Pre-Phase-5 contract compliance found the LV002 per-work Distillation State record missing. It was created late as `pending-quality` in `capture-state/lv-obs-002-baseline.md`; the missed pre-write timing is disclosed and was not backdated. Formal quality must assess this process finding.
- Residual risk: declared scope/input/setup IDs rely on operator review for actual input equivalence; only source, timing digest and check/test identity are mechanically bound. The three final runs used the same source, profile and observed project inputs. Linux CI remains unrun.
- Formal high-risk `phase-5-quality` requires a separate owner gate; this implementation artifact does not assert `PASS` or authorize LV003.

## Owner-Approved Fix Loop And Final Baseline: 2026-09-30

- Authority: LV-DEC-006 records the owner-approved high-risk Phase 5 and fix loop, followed by Phase 6/local commit only at PASS. The eight-file source ceiling is unchanged.
- The original timing boundary allowed TMPDIR to widen temporary roots. The fix checks tracking before temporary acceptance and inspects the destination repository independently of caller CWD, including deleted tracked and unignored foreign temporary targets.
- Six cause-specific smoke cases were added; native Python/Git prevent macOS wrapper cache writes under hostile TMPDIR. Only the generated xcrun_db was removed. No unrelated state was changed.
- Final reviewed source digest: 18d226a162ade008c96c791f115e862d16f16051aed434fde5579b63e9f64ec9. All earlier measurements above are historical and excluded from this corrected baseline.
- New complete manifests: lv002-final-reviewed-001.json, lv002-final-reviewed-002.json and lv002-final-reviewed-003.json, each beside its TSV/log. All emitted a single full/pass completion marker and smoke-all/pass; 40 checks and 660 unique smoke IDs each. No old smoke ID was removed; six boundary IDs were added.
- Wall times: 860.714997, 711.405061 and 805.782230 seconds; median 805.782230, range 711.405061-860.714997. Source, runtime, profile, check/test arrays and declared input/setup IDs match. This is a noisy instrumented baseline, not a speed improvement or statistical certainty.
- Ten direct output-boundary probes, five lifecycle probes (including actual SIGTERM), and three comparison probes passed. Probe code is retained in this implementation directory. A synthetic separated range qualifies, repeated run IDs/fewer than three runs reject; no real optimization gain is claimed.
- Fresh full-current-diff review after the final source edit covered all eight paths, complete DoD, failure/interrupt/source-drift flows, TSV/manifest compatibility, source/input/coverage boundaries and privacy. The formal current Phase 5 report owns the verdict.
- Known limits: declared runtime input equivalence requires operator review; telemetry binds source/timing/IDs mechanically but is not proof of all runtime input contents. Linux CI is unrun. The late capture-state creation remains a disclosed process warning, not backdated compliance.
