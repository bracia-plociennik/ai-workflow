# LV005 Offline Preparation: Final Advisory Review

## Findings First

- P2 / infrastructure blocker: a functioning default-deny runtime is not established. The sandboxed pinned CLI terminated with SIGABRT before version output; the sandboxed shell also terminated before actual timeout/read/write/network probes. Preview and actual exec context comparison therefore did not run. Cause beyond this observed startup failure is unproven.
- Platform approval blocker: adding broad `syscall*` primitives was rejected by auto-review before execution. The rejected additions were removed; no unsandboxed CLI fallback, indirect bypass or model request was run.
- Preparation limitations: preview wire-shape adapter and actual runtime tool inventory are deliberately unproven. Unrecognized shapes/text/tools fail closed; matching a familiar environment/permissions tag no longer exempts unknown content. This is not a usable behavioral-eval runtime.
- Corrected harness findings: actual child-start evidence added to timeout controls; missing sink startup is distinguished from failed sink cleanup; malformed/missing sources and output-zero false confidence rejected; image tools removed from allowed inventory; raw preview schema keys no longer persisted.

## Reviewed Baseline And Evidence

- Source HEAD: `0c767da0385723560d1b0d4794a9091316c23140`; branch `codex/ai-workflow-lean-validation-v1`; tracked tree clean.
- Current harness SHA-256: `c66ae4125fa7208e946fd5dd1026b5a32995b82cc85797edbe279f6be8adcbf3`.
- Current test source SHA-256: `ce9c5b27fa4a972ccb68c3bdeb097310468a101908b343ab761e83894ad3d78b`.
- Pinned CLI binary SHA-256: `0196e89fe5a7598f816ee54232c3d7c26d75e502ab5cfe2c9240e81d90f7255a`; release path 0.156.1. Version output under isolation was not obtained.
- Seven runtime-attempt summaries remain under `runs/`; failures are preserved, not graded as model/evaluation failures.
- Last actual runtime attempt: `runs/20261001T092201-21585/summary.json`, blocked at sandboxed timeout setup. It refers to its own recorded older source hash, not the final source below. No runtime-success evidence is borrowed across edits.
- Final synthetic tests: `runs/detectors-20261001T092719903047/summary.json`; 14 tests, zero failures/errors, 1.318 seconds, source hashes match current files.
- Independent wrapper test observed child-start stdout, controlled timeout exit 124 and absence of its delayed write. It did not invoke CLI, sandbox-exec, auth or network.
- Runtime summaries confirm temporary-root removal and stopped sinks after successful sink setup. The initial setup failure had an overly broad cleanup label; it remains preserved and the current producer distinguishes not-started from failed-cleanup.
- Final exact `/private/tmp/lv005-offline-*`, `lv005-wrapper-*`, `lv005-policy-diag-*` inventory is empty.
- `git diff --check`: clean; `git ls-files ai-workflow-workspace`: empty; `git check-ignore -v` confirms harness is ignored.

## DoD And Intent Compliance

| Condition | Assessment |
| --- | --- |
| Approved writes confined to ignored workspace and owned temporary fixtures | satisfied by commands/write paths and tracked baseline checks |
| No login, auth-status query, credentials copying, model eval, global config edit, source candidate, commit or push | satisfied for this scope |
| Frozen inspectable binary/config/env/policy and fail-closed detector | implemented and synthetic-tested; real runtime compatibility unproven |
| Actual OS isolation and working CLI startup | blocked |
| Actual sandboxed read/write/canary/network evidence | not reached; not inferred from detector/wrapper tests |
| Preview equals actual loopback exec request | not reached |
| Timeout wrapper cleanup | independently observed; sandboxed runtime cleanup test not reached |
| Privacy-safe append-only evidence and preservation of history | satisfied |
| Main LV005 task, final checkpoint/Phase 8 inputs and deferral unchanged | satisfied; no writes outside this preparation folder in project |

Overall intent/plan/spec compliance: partial delivery due to runtime isolation blocker, no scope expansion. Offline preflight was attempted and recorded, but its readiness DoD is unmet. LV005 remains deferred, not accepted, not distilled, and not behaviorally evaluated.

## Adaptive Verification And Producer-Consumer Audit

| Source | Expected canonical result | Forbidden outcome | Failure behavior / evidence |
| --- | --- | --- | --- |
| Synthetic payload | Explicit classified summary and hashes | Missing input interpreted as clean; foreign tagged text accepted | Malformed/required-field/ambient/tag-spoof negative controls fail closed |
| Tool inventory/header names | Allowed immutable tool names, no auth header | Unknown/duplicate tool or credential-bearing transport accepted | Tools/auth negative controls fail closed; values not persisted |
| Preview and exec summary | Equal instructions/context/roles/tool schemas | Matching subset mistaken for equivalent context | Synthetic mismatch tests; actual comparison not reached |
| Process exit and file/output | Actual required observations | Zero exit alone accepted | Missing-result negative test and actual-output wrapper test |
| Child process and timeout | Child started, group killed, no delayed write | Dead-before-start child called successful cleanup | Real independent wrapper trace with start marker; isolated trace blocked |
| Runtime startup | Exact version, restrictive OS policy | Broad fallback or guessed permission result | SIGABRT preserved; rejected syscall addition removed; stopped |

Manual representative trace: clean synthetic request -> required schema/roles/tool checks -> redacted hashes -> equal comparison. Failure trace: sandboxed runtime -> SIGABRT before observation -> blocker -> own sink/temp cleanup -> append-only blocked summary; no preview/exec/model call occurs. Synthetic wrapper trace independently verifies timeout handling, never filling the missing isolation fields.

## Review Completeness Gate

- Cross-contract consistency: aligned with offline-only authority; preparation readiness remains blocked.
- Risk/work mode compatibility: aligned; high-risk full-project preparation with explicit owner approval.
- Source-of-truth, permissions, phase gates, artifact state and acceptance criteria reviewed: yes.
- Negative-space / adversarial review: completed for current source; unsupported runtime scenarios explicitly blocked.
- Policy-boundary adversarial matrix: completed; strict policy assertions and direct/combined unknown-context controls; broad syscall/Mach rules prohibited by regression tests.
- Producer-consumer field audit: completed; runtime and model-context fields cannot be supplied by detector/wrapper evidence.
- Required-field mapping: complete for preparation summaries; actual context production not proven.
- Automated evidence role: supporting-only.
- Instruction refresh: performed-full after compaction; current AGENTS/router/operating/risk/permissions/slicing/quality/full-QA/response/compliance/DoD/delivery and project deferral/baseline reviewed.
- Post-fix full re-review: completed against all current harness sources, tests, scope/capture evidence and preserved runtime summaries.
- Instruction baseline: current. Closure freshness: current for this blocked advisory assessment.
- Formal gate eligibility: not eligible; no formal PASS/FAIL or task promotion.

## Closure And Next Route

Advisory result: blocker found; not offline-preflight-ready or behavioral-eval-ready. Broad system validation is not applicable to unchanged tracked source and would not resolve runtime isolation. No authentication or model comparison was performed.

Knowledge capture: supporting preparation evidence recorded here; separate preparation Distillation State remains pending-quality, is_distilled false. Main LV005 capture remains unchanged. No Phase 6/7, memory promotion or cross-system implementation handoff inferred.

Next route: separately approve and design a safe runtime recovery method, preferably a dedicated isolated OS user/VM with no inherited auth/private configuration. Do not weaken this profile or resume behavioral eval merely because detector tests are green.
