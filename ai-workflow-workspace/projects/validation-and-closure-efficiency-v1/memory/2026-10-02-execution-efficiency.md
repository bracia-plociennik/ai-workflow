# Execution Efficiency - Project Memory

- Date: 2026-10-02
- Source: quality/phase-5-eff-all-quality.md; reviews/full-validation-evidence.json; distillations/phase-6-eff-all-distillation.md
- Scope: validation-and-closure-efficiency-v1; upstream branch codex/validation-and-closure-efficiency-v1
- Publication state: uncommitted, not pushed, not installed in AI System

## Stable Facts

The seven accepted capabilities are implemented under .systems/ai/core/execution-efficiency.md. Formal quality has seven independent DoD rows and current producer-consumer/adversarial evidence. The final full gate executed 703 smoke IDs (700 retained, three added), including 29 behavioral tests. It took 702 seconds, smoke 665 seconds.

Reuse is iteration-only, HMAC-authenticated and allowlisted to check-required-artifacts and check-full-qa-verification. Whole source/dependencies, input/argv/coverage, tools and environment are bound. Failed/incomplete/tampered or changed-source evidence is not reusable final QA.

Fresh Phase 6/7/8 runtime checks can use the unchanged full-source receipt in the same resolved execution context. They still execute naming, QA, status and capture-state consumers and require semantic/privacy review. Current receipt/key are temporary and local; loss or context/source drift requires a fresh gate.

Historical QA admission preserves bytes and checks explicit owning decision and report checksums. Current PASS consumers reject history. The V2 producer validates supplied reviewer sections before no-clobber publication. Technical Phase 8 is awaiting owner; separate final-owner-yes provenance is required to close.

## Measurement And Limits

Three equivalent samples per scenario exist in baseline.json and candidate-final.json. Cheap synthetic checks were slower with receipt overhead. Unchanged scenarios ran one actual check plus one reuse; changed source ran both fresh. No whole-agent/model/production latency speedup is claimed.

Shell/environment identity is deliberately conservative. In this macOS checkout, source-backed commands were verified with the same resolved Bash context used by validate-workflow. A standalone invocation from a different shell invalidates the environment binding safely.

## Operating Lessons

- Add public-interface tests in addition to internal helper tests.
- Keep synthetic CI probes isolated while separately testing production CI rejection.
- Open potential non-regular key inputs nonblocking before fstat.
- Semantic review precedes supporting scripts; source changes invalidate old closure.
- Consolidated package capture does not drop individual task acceptance criteria.
- No deadline/timebox, cross-system handoff, commit/push or final-owner-yes was authorized for this run.
