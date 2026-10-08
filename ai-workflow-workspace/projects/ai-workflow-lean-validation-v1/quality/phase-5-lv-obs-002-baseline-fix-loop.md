# Phase 5 Fix Loop: LV-OBS-002-baseline

- Date: 2026-09-30
- Input quality result: FAIL found during the owner-approved formal Phase 5 review.
- Finding: P2; safe_output accepted TMPDIR and tempfile.gettempdir as unrestricted temporary roots before checking Git tracking. With TMPDIR set to the official source root, read-only reproduction accepted a tracked validator path.
- Original evidence: validation-timing.py SHA-256 391dd7995377d6cc95b4e49fa12faedf2f76418b182f623fb5a6a7cff8dad6ab; source digest 4d3dfad031fcd5f0e9724f7852a19b66717af73e51a1be607bd9f0ec0b9bfbf6. The reproduction performed no output write.
- Owner approval: explicit "Zatwierdzam fix-loop"; implementation range and exact eight-file LV002 ceiling were previously approved.
- Retry count: 1
- Maximum quality retries: 2
- Limit reached: no

## Implementation Slice Plan

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| LV002-F1 | Preserve output boundary despite environment or temporary checkout | validation-timing.py | tracked/deleted tracked and unignored repo outputs rejected independent of caller CWD; standalone platform tmp remains allowed | ten local synthetic probes | implemented; targeted validation passed |
| LV002-F2 | Lock regression into full smoke coverage | check-validator-smoke-tests | exact exit 2 and diagnostics for three new adverse cases | frozen full runs | implemented; validation pending |
| LV002-F3 | Refresh source-bound baseline and formal QA | ignored project evidence | three complete full runs on the corrected source; fresh current-diff review | new manifests and Phase 5 artifact | pending |

- DoD source: accepted LV002 V2-08 sink safety, V2-07 explicit schema compatibility and the unchanged task contract.
- Fix: check tracking before any temporary-root acceptance; platform temporary roots are independent of TMPDIR; inspect the target repository from its nearest existing parent, independent of caller CWD. Repository outputs must satisfy the current ignored workspace boundary.
- Additional same-boundary variant: foreign temporary repositories, including deleted tracked targets, cannot be admitted by invoking from official source CWD. Three new smoke IDs cover these cases; ten direct probes passed.
- Fixture isolation: native Python/Git avoid macOS developer-tool cache writes under hostile TMPDIR. Own generated xcrun_db was removed; no unrelated file was changed. Earlier intermediate/interrupted runs are retained but excluded from the final baseline.
- Scope: two existing approved LV002 files; no new product behavior, coverage removal or optimization.
- Prior baselines: retained as historical source-specific measurements; they cannot stand in for the corrected source.
- Quality closure route: fresh formal phase-5-quality before distillation or commit.
- Residual risk: earlier late creation of capture-state is disclosed and remains a process warning; no retrospective compliance is asserted.

## Post-Fix Verification

- LV002-F1 and LV002-F2 completed: ten direct boundary probes and six new full-suite negative contracts reject with exact exit 2 and cause-specific diagnostics.
- LV002-F3 completed: three final-reviewed full runs passed on source digest 18d226a162ade008c96c791f115e862d16f16051aed434fde5579b63e9f64ec9; 40 checks and 660 tests per run, no lost prior IDs.
- Lifecycle probes: original failure 7, timeout 124, source drift 1, SIGTERM interrupt 143 and success 0 all preserve a single completion marker and truthful wall result.
- Final current-diff producer-consumer/adversarial review completed after the final edit. Original P2 and the foreign-target variant are resolved; historical source-specific runs remain untouched.
- Formal verdict is recorded separately in phase-5-lv-obs-002-baseline-quality.md; this fix-loop record does not replace that gate.
