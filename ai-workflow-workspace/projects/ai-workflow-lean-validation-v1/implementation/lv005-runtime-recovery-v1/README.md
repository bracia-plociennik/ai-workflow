# LV005 Offline Runtime Recovery

## Authority And Scope

- Owner approval: prepare LV005 harness and run offline preflight only in `/tmp` and ignored workspace.
- Work mode: full-project preparation-only; risk: high, approved for this bounded action.
- Source baseline: `0c767da0385723560d1b0d4794a9091316c23140`, clean `codex/ai-workflow-lean-validation-v1`.
- LV005 remains deferred under LV-DEC-010. No current Spec QA implementation authority or behavioral readiness is inferred.
- No login, authentication-status query, credential reading/copying, model evaluation, tracked writes, commit, push or global configuration changes.
- CLI frozen at `0.156.1`; GPT-6 Sol High is only a future eval target, not a model called by this harness.
- Prior preparation attempts and all bound project/final-check inputs remain immutable.

## Task Idea Validation

- Co zostaje: synthetic fixtures, real execution evidence, explicit failure preservation, isolation before evaluation.
- Co poprawic: separate host HOME as well as CODEX_HOME; enforce filesystem/network restrictions outside CLI; compare preview with actual request.
- Czego brakuje: authenticated-provider equivalence and future paired behavioral evidence, deliberately out of scope.
- Blokery / decyzje: stop on unavailable sandbox, unrecognized context, unexpected tools, missing request or unsafe transport; no owner question needed for approved offline preparation.
- Rekomendowany routing: bounded offline preparation, advisory current-harness review; not formal LV005 implementation or Phase 5.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PREP-1 | Freeze authority, runtime and scope | This README, capture-state | Scope matches exact owner approval | Baseline and hashes | complete |
| PREP-2 | Implement fail-closed detectors and isolation | preflight.py, test-preflight.py | Adversarial review before runtime | Detector and producer-consumer cases | complete; runtime compatibility not proven |
| PREP-3 | Run bounded offline probes | /tmp fixtures, runs/ | Actual observations, timeout/cleanup, no model | Redacted summary only | blocked; isolation not ready |
| PREP-4 | Fresh whole-harness QA | review.md | DoD, failure paths, full current source review | Findings-first closure | completed with runtime blocker |

## Definition Of Done

- Runtime version and binary hash are frozen, config/env/policy are inspectable and hashed.
- Environment is constructed from an allowlist; no inherited tokens, proxies or auth state.
- Child runtime has an OS-enforced default-deny filesystem and network policy, with one loopback sink exception.
- Real preview and exec request are compared; missing/malformed/unexpected context and tools fail closed.
- Detector rejects auth-bearing requests, ambient guidance, preview/exec mismatch and zero exit without actual results.
- Actual synthetic read/write, denied sibling read, denied non-loopback network and timeout cleanup have observed evidence.
- Generated evidence contains summaries/hashes only; no raw CLI output, requests, authorization values or private material.
- Offline eligibility is separate from hosted authenticated context, model tool execution, behavioral evaluation and formal quality.
- Historical attempts, tracked tree and project Phase 8 inputs remain unchanged.

## Plan Quality Contract

- Plan classification: implementation-capable, ignored harness only.
- DoD source: owner-approved offline recovery plan and this Definition Of Done.
- Artifact QA route: global-quality-review-stance before runtime execution.
- Implementation Quality Closure route: global-quality-review-stance after final edit and probes.
- Required verification: detector unit/adversarial tests; actual process/file/network/cleanup observations; adaptive request/result matrix; manual source and failure-path review.
- Quality-ready criteria: no harness blocker; offline-preflight-ready only if every isolation check succeeds; partial results never imply readiness.
- Owner opt-out: none.
- Blocking decision: none for offline scope; hosted/authenticated evaluation is not approved.
- Next route: read-only decision review of results; no automatic model eval or LV005 restart.

## Delivery Constraints

- Mode: owner-opt-out under LV-DEC-001.
- Deadline: none; Time budget: none; Timezone: Europe/Warsaw.
- Must-have outcome: bounded harness and truthful offline result.
- Deferred scope: login, behavioral eval, tracked LV005 candidate, final-owner-yes.
- Quality floor: isolation and honest evidence, never relaxed for completion.
- Cutline rule: omit unsupported runtime capability and report blocker rather than weaken boundaries.

## Running

`python3 -B test-preflight.py` is synthetic detector/wrapper testing only.
`python3 -B preflight.py` uses the pinned local CLI, default-deny macOS sandbox and local rejecting sink. It writes an append-only run directory beside this file and removes its own `/tmp` runtime. The present macOS runtime aborts under this profile; it is not ready. Do not rerun a blocked attempt with a relaxed security profile.

The sink is not a model endpoint. It returns HTTP 400 for every POST. No model response or evaluation is produced.

## Current Outcome

- Offline preflight: blocked, not offline-preflight-ready.
- The default-deny profile aborts even `/bin/sh` with SIGABRT before sandboxed timeout/capability observations. The isolated CLI also aborted before version output in an earlier attempt.
- A broad `syscall*` addition was rejected by platform auto-review before execution and was removed. No bypass performed.
- Synthetic detector and independent process-wrapper tests are supporting-only, not evidence of OS isolation, authenticated context or model behavior.
- Preview/actual request comparison, sandboxed file/network denial and model tool execution remain untested in a functioning isolated runtime.
- LV005 and the project's existing Phase 8 disposition are unchanged. Further runtime recovery requires a separately approved safe method; no login or eval is implied.
