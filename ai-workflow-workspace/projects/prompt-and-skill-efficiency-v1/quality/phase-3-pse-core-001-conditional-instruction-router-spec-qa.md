# Phase 3 Spec QA: PSE-CORE-001 Conditional Instruction Router

## Metadata

- Project: `prompt-and-skill-efficiency-v1`; task: `PSE-CORE-001-conditional-instruction-router`; re-QA date: 2026-09-25.
- Artifact: `specs/phase-3-pse-core-001-conditional-instruction-router-specification.md`.
- Phase: `phase-3-spec-qa`; result: `PASS` for corrected CORE-001 specification content after the second fix loop. Earlier failed and invalidated reviews are recorded in the fix-loop artifact and run ledger.
- QA verification contract: `full-qa-verification-v1`.

## QA Verification Scope

- Subject: specification correctness and readiness against accepted project context, owner objective, architecture, Plan QA, task index, risk/permissions and Phase 3 contract; not implementation code review.
- Full QA contract: `.systems/ai/core/full-qa-verification.md`.

## Artifact QA Completeness Gate

- Owner intent and governing sources reviewed: accepted project context, owner request, no-deadline decision, synthetic-subagent approval, PE-002 exact `AGENTS.md` approval, `AGENTS.md`, architecture and QA, plan and QA, task index, corrected spec and phase-3 spec QA contract.
- DoD / phase acceptance criteria reviewed: yes; router structure, behavioral safety, observed explicit read-efficiency and project-doc autoload coverage have test methods and fail-closed promotion routes. The single feasibility probe is not a paired result.
- Scope and out-of-scope consistency: aligned for an owner-approved `AGENTS.md`-only first candidate; other tracked files remain excluded.
- Artifact / relevant diff review: completed for the current ignored spec, decision, fix-loop evidence, measurement-feasibility note and task-index link. No tracked source diff exists.
- Findings-first review: completed; no unresolved spec blocker remains.
- Failure / rework / dependency scenarios: completed; missing policy, false formal quality approval, fixture drift, unapproved source write, ambiguous JSONL commands and project-doc truncation have stop/defer routes.
- Repository and source compatibility: aligned; tracked `main` remains untouched.
- Post-fix full artifact re-review: completed after restoring the accepted measurable-efficiency DoD and adding the CLI JSONL feasibility protocol. Current spec, context, architecture, plan, decision, fix-loop, eval note and task index were compared again.
- Evidence reviewed: current spec, accepted context, architecture/Plan QA, task index, PE-002 decision, fix-loop artifact, exploratory and controlled baseline reports, `evals/measurement-feasibility.md`, risk model and clean tracked `git status`.
- Skipped or unreadable sources: full candidate and instrumented per-case baseline do not exist; previous subagent full transcripts remain unavailable. The one CLI probe is not an efficiency result.
- Residual risk: JSONL commands may not identify all actual OS file opens and automatic `AGENTS.md` loading is separate. Later paired eval must classify ambiguous commands as unknown, verify candidate autoload safety and block promotion if evidence is insufficient.
- Closure freshness: current after the 2026-09-25 DoD correction, feasibility probe and full current-spec re-read.

## Checks

| Check | Result | Evidence | Finding |
| --- | --- | --- | --- |
| Spec contract complete | met | Goal, scope, steps, DoD, tests, edges, dependencies and risk present | none |
| Plan Quality Contract complete | met | Artifact QA, phase-5 closure and checks stated | none |
| Implementation Gate correct | met | Exact approved write set; spec content ready, while Phase 4 remains outside planning-range | none |
| Architecture consistency | met | Safety core and conditional details match architecture | none |
| Project-plan consistency | met | CORE task and sequencing match current plan | none |
| Dependencies explicit | met | Controlled baseline graded; PE-002 approval and later range/QA gates named | none for this spec |
| No hidden decisions | met | Owner decision artifact limits the first candidate to `AGENTS.md` | none |
| Tests and edge cases adequate | met | Direct/near-miss, policy/skill, status conflict and holdout cases listed | repair/retest branch needs added controlled fixture if claimed |
| Accepted efficiency DoD retained | met | Directly observed baseline/candidate explicit read comparison is a promotion condition; unknown measurement defers the task | none for specification |
| Autoload truncation covered | met | CLI probe exposed 32768-byte project-doc budget; candidate loaded-prefix audit and regression stop are specified | baseline coverage risk deferred to implementation evidence |

## Findings

### Blockers

- None in the corrected CORE-001 specification. PE-002 resolved the approval blocker. The second finding, which had invalidated an early favorable verdict, was fixed by restoring the accepted measurable-efficiency DoD and no-proxy-promotion rule. This is not approval to implement within planning-range.

### Warnings

- Controlled baseline is manually graded but unpaired. Candidate evidence is required for eventual phase-5 quality, not for this specification gate; exploratory baseline-002/003 remains excluded.
- Actual paired explicit-read/token savings are unmeasured. CLI JSONL can show completed read commands and turn token totals, but one probe is not an eval baseline; do not claim cost improvement from a shorter list alone.
- Current `AGENTS.md` is 34969 bytes; the CLI warned of a 32768-byte project-doc autoload limit in the probe. The candidate must be audited for loaded-prefix safety and cannot inherit truncation as a harmless default.
- The existing active `skill-creator` review route was missed in two controlled holdout repeats; avoid trigger narrowing that entrenches this false negative.
- Validator limitation: `check-qa-evidence` treats any uppercase success token in a file as the final artifact result. This artifact keeps component rows as `met`; a future validator fix should parse only the final result field.

## Evidence

- Artifacts-reviewed: accepted context, architecture, Architecture QA, project plan, Plan QA, task index, current spec, PE-002 decision, fix-loop evidence, `evals/baseline-review.md`, `evals/controlled-baseline-review.md`, `evals/measurement-feasibility.md`.
- Manual-checks: accepted measurable-DoD comparison, exact approved write set, dependency and failure-path audit, negative-space routing, corrected current-spec full read.
- Command: `.systems/scripts/check-naming` exited 0 after the spec filename correction; `.systems/scripts/check-status-consistency` exited 0 after the full workspace path was added to `tasks.md`.
- Command: independent `python3 -B test_math_utils.py` in the V4 local-loop fixture exited 0 (3 tests); this confirms only that synthetic fixture, not the CORE spec gate.
- Command: a read-only `codex exec --json` GPT-6 Sol High probe exited 0 and emitted a completed `head -n 5 AGENTS.md` command plus turn token usage; `wc -c AGENTS.md` reported 34969 bytes. No paired performance result was inferred.
- These commands are supporting-only; they do not replace the later paired candidate evaluation or implementation-range gates.

## Gate Decision

- Spec QA result: PASS for corrected CORE-001 specification content only; no candidate behavior or efficiency verdict.
- Can enter implementation in this run: no; planning-range stops before Phase 4 and later implementation-range requires its own readiness audit.
- Required next phase: `phase-3-specification` for the next planned task, subject to its own dependency and owner-decision gates.
- No formal phase-5 quality result exists; no implementation approval is implied.

## Delivery Constraints QA

- Constraint source: owner `Bez deadline'u i timeboxu`.
- Must-have outcome: evidence-backed routing improvement without mandatory-gate regression.
- Cutline: optional model/verbosity changes and unproven simplification.
- Quality floor: no lost required source, permission, DoD, QA or approval.
- Overrun route: owner decision on material scope/evidence uncertainty, no invented timer.
- Result: aligned.

## Validation Execution Record

- Semantic QA result: owner instruction, accepted measurable-efficiency DoD, plan, architecture, risk, exact write set and fail-closed implementation steps align. PE-002 and the second fix loop closed both prior spec findings; paired candidate evidence remains a later acceptance gate.
- Findings/blockers: none unresolved in CORE-001 spec; incomplete metric coverage, current autoload truncation and skill-review false-negative warnings remain for later work.
- Product checks: not applicable, no implementation.
- Workflow script applicability: targeted naming/status checks only; broad validation is not an ordinary Spec QA step.
- Targeted workflow commands: `check-naming`, `check-status-consistency`.
- Script evidence role: `supporting-only`.
- Final verdict: PASS for the corrected spec artifact; stop before Phase 4.

## Model Recommendation

- Recommended: GPT-6 Sol High, as owner selected for paired eval.
- Reason: high-impact routing and safety review.
- Criticality: high; current model known: eval subagents only; blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued decision resolved by owner before resuming planning-range.
- Decision state: clear for CORE-001 spec; later tasks need their own decision checks.
- Material decisions: PE-002 approved for `AGENTS.md` only.
- Questions asked: none mid-run.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: may defer CORE entirely if controlled comparison cannot support the change.
- Decision artifacts: `decisions/pe-002-agents-only-candidate.md`, current spec, fix-loop artifact, `evals/controlled-baseline-review.md`, this QA artifact.
- Next route: next planned task's phase-3 specification; implementation-range remains separate.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: the false-negative skill review and eval-fixture validity lessons may inform later design, but should be captured only after complete baseline review and privacy check.
- Owner decision required: no for proposal; durable write not authorized by this QA phase.
- Owner decision: defer-to-distillation.
- Privacy/scope check: pass; synthetic sources only.
- Suggested entry title: Skill-review trigger coverage and eval isolation.
- Suggested entry summary: Test review as well as creation, and freeze runtime inputs before paired comparisons.
