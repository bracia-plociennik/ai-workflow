# PTO-003 Readiness And Spec Regression Review

- Date: 2026-10-04
- Current instruction refresh: full after resumed continuity; targeted before write.
- Baseline: official branch codex/parallel-task-orchestration-v1, HEAD 8a0eeef;
  only approved PTO-001/002 sources are changed; no staged files.
- Predecessor: PTO-002 current formal Quality PASS and Phase 6 exist. 25 tests,
  current 656-second full and source freeze reviewed, including exact unit/run keys.
- Accepted eight-file spec remains applicable; no transport, worker process service,
  model API, automatic worktree creation/cleanup or native operational support claim.
- Interface refinement: unit.execution may carry an explicit dispatch contract;
  null remains valid for allocator-only templates. Strict field validation remains.
- Source snapshot and allowed write/resource context are explicit. Native observation
  is caller-supplied evidence, checked against actual files; it is not authenticated
  by a JSON boolean. Synthetic observations are labelled, never native proof.
- Three slices: contract/result/prompt; protocol validation and adversarial tests;
  full-current-diff review, producer-consumer audit and applicable supporting checks.
- DoD: PTO-003 AC1..AC5; semantic QA route formal Phase 5 with existing conditional
  owner acceptance, followed by Phase 6 and checkpoint at three parent tasks.
- Decisions: clear within spec; no deadline/timebox; shared impact yes; no commit/push.
- Risks: TOCTOU and backend honesty remain re-observation requirements. Missing
  actual safe workspace/enforcement blocks implementation dispatch.
- Skills used: none; no active domain-skill trigger matches.
