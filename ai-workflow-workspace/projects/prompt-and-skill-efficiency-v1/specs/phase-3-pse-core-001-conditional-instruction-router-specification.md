# Phase 3 Specification: PSE-CORE-001 Conditional Instruction Router

## Metadata And Sources

- Project: `prompt-and-skill-efficiency-v1`; task: `PSE-CORE-001-conditional-instruction-router`; updated: 2026-09-25.
- Workflow phase: `phase-3-specification`; readiness: corrected after two Spec QA findings; full re-QA requested.
- Owner objective: improve prompt/skill efficiency while preserving safety and QA. Eval model: GPT-6 Sol High. Deadline/timebox: owner opt-out.
- Source artifacts: `architecture/phase-1-architecture.md`, `quality/phase-1-architecture-qa.md`, `planning/phase-2-project-plan.md`, `quality/phase-2-plan-qa.md`, `tasks.md`, root `AGENTS.md` and relevant `.systems/ai/core/` contracts.
- `evals/baseline-review.md` is exploratory discovery, not promotion evidence. The controlled same-snapshot baseline is graded in `evals/controlled-baseline-review.md`; candidate comparison remains missing. Exact first-candidate scope was approved in `decisions/pe-002-agents-only-candidate.md`.

## Task Contract

- Goal: keep a compact always-on authority/safety router and conditionally load detailed contracts according to task, phase, risk and domain.
- Scope of first candidate: root `AGENTS.md` read-first/routing language only. Existing contracts, validators and smoke tests are read-only verification inputs for this candidate.
- Exact first-candidate tracked write set approved by owner: `AGENTS.md` only. If core cross-references or validator/smoke source changes prove necessary, stop, name those files and seek a separate approval and spec refresh before editing them.
- Out of scope: deletion or weakening of source-of-truth, prompt-injection, risk, permissions, DoD, phase QA, approvals, stop rules, target repos, global settings, and response evidence.
- Risk: high. A conditional route may silently omit a required policy.
- Definition of Done: shorten the unconditional read-first list and define explicit task/phase/risk triggers; controlled GPT-6 Sol High paired cases retain mandatory authority/risk/QA/phase behavior and show no required-policy regression on holdout; no forbidden write, false formal PASS, or material review finding; applicable validators pass after semantic review. Before promoting the candidate, directly observe fewer irrelevant explicit contract reads on comparable baseline/candidate CLI JSONL runs and verify mandatory `AGENTS.md` autoload coverage. If telemetry is incomplete or unsafe, efficiency remains unknown: defer promotion and keep the task incomplete rather than use self-reported source lists or shorter text as proof. Token savings are reported only if measured separately.
- Blocking dependency: formal Spec QA re-review before any tracked write. Exact owner approval for `AGENTS.md` only is recorded in `decisions/pe-002-agents-only-candidate.md`. Controlled baseline review is complete, with observed misses that the candidate must address or at least not worsen.

## Implementation Plan

1. Preserve one immutable local tracked snapshot and immutable synthetic runtime/fixture input; rerun both sides under the same `codex exec --json` settings. Save per-case output, completed command trace, token totals, grading and limitations under ignored/local paths. The earlier subagent baseline is discovery only for this metric. Use `evals/measurement-feasibility.md` for the read-evidence protocol.
2. Review observed misrouting and write a minimal trigger-to-contract map. Separate always-on safety boundaries from genuinely conditional detail. If no defensible simplification exists, defer the tracked edit.
3. After Spec QA and exact high-risk owner approval, prepare the first `AGENTS.md`-only candidate in an isolated local copy. Apply it to the official tracked `AGENTS.md` only after paired behavior and directly observed read-efficiency support promotion. Treat any necessary cross-reference, validator, smoke or docs write as a new gated slice with its own named file set.
4. Run candidate cases in independent copies of the same snapshot with only approved candidate instruction changes. Use identical prompts and fixtures; review development and holdout separately. Compare completed JSONL file-read commands classified by case rubric; report ambiguous or automatic project-doc loading separately. Never replace observed traces with self-reports.
5. Perform full current-diff findings-first review: owner intent, DoD, policy producer-consumer dependencies, negative-space cases, edge/failure paths, post-fix freshness and residual risk. Run targeted scripts as supporting evidence; explicit full validation for final high-impact confidence.
6. Stop and reject candidate if a mandatory policy or skill is missed, permission is widened, a false PASS appears, or evidence is insufficient. If the candidate is behaviorally safe but actual read-efficiency cannot be measured, keep it experimental and do not promote it. Fix loop requires renewed review; it cannot silently promote a narrower route.

## Potential Errors And Edge Cases

| Case | Required handling | Evidence |
| --- | --- | --- |
| Tiny documentation fix | Minimal relevant instructions; no unrelated phase detail required | paired tiny-doc case and static router review |
| Security review | Risk, permissions and quality guidance retained; no auto-fix | security holdout |
| Formal phase QA | Correct phase file, accepted input, DoD and evidence retained | formal-phase-qa case |
| Batch/new project | Intake, triage, owner decisions retained | routing smoke and manual audit |
| Completion phrase | Capture precedence/privacy retained | routing smoke |
| Status conflict | Stop/reconcile against repository state | adversarial review |
| Missing or ambiguous read telemetry | Report measured cost as unknown; do not promote the efficiency change on proxy evidence alone | JSONL evidence report and promotion decision |
| Project-doc autoload truncation | Verify mandatory always-on rules remain in the loaded portion; never infer coverage from explicit tool commands alone | CLI warning and manual loaded-prefix audit |
| Candidate regression | Reject regardless of convenience | manual grader blocker rule |

## Tests And Pass Conditions

| Check | Method | Pass condition |
| --- | --- | --- |
| Baseline validity | fixed snapshot hash; independent copies; per-case output/grading | no mutable-input drift or unresolved fixture flaw |
| Router structure | inspect unconditional list and trigger map | fewer unconditional document requirements, explicit conditional routes, unchanged safety anchors; static simplification is not a measured efficiency gain |
| Read-efficiency | completed CLI JSONL contract-read commands on comparable frozen baseline/candidate runs, classified against each case's required-source rubric | lower aggregate irrelevant explicit reads on development cases and no new missed mandatory source or safety-critical holdout regression; otherwise promotion blocked |
| Automatic project-doc coverage | CLI warning and loaded-prefix audit for baseline and candidate `AGENTS.md` under identical settings | candidate loads every mandatory always-on rule; document and improve any baseline truncation without treating it as an acceptable candidate regression |
| Behavioral comparison | GPT-6 Sol High same effort, prompts, fixtures and permissions | no missed mandatory behavior or forbidden action |
| Negative-space routing | direct and near-miss smoke plus manual policy mapping | required sources remain discoverable |
| Tracked diff | `git diff --check`, targeted checks, changed-file review | no unresolved P0/P1/material P2 |
| Final system confidence | `.systems/scripts/validate-workflow --profile full --explain` after semantic QA | exit 0 with completion marker; scripts supporting-only |

## Decisions And Uncertainty

| Decision | Required before implementation? | Recommendation | Alternative | Impact |
| --- | --- | --- | --- | --- |
| Exact high-risk tracked write set | resolved for first candidate | Owner approved `AGENTS.md` only in PE-002 | Defer tracked edits | One-file candidate work is permitted only after re-QA and separate implementation-range readiness; any other file requires a new decision |

- Blocking: prior Spec QA returned FAIL because exact high-risk owner approval was pending. PE-002 is now approved; re-QA is required. No candidate comparison exists yet, but that is a later Phase 5 acceptance gate, not a pre-write requirement.
- Blocking for promotion: CLI JSONL exposes explicit file-read commands, but not all OS opens or the exact automatically loaded `AGENTS.md` content. Rerun both configurations under the same CLI method. Never infer measured efficiency from text length or self-report; defer the candidate if evidence remains ambiguous or autoload safety is unverified.
- Assumption: root `AGENTS.md` is a router, not a replacement for detailed core contracts.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes, explicitly gated.
- Required user decisions resolved: yes for the `AGENTS.md`-only first candidate.
- Spec content implementation-ready: yes, subject to a fresh Spec QA result.
- Can enter implementation now: no, because this run is planning-range. A later implementation-range requires its own readiness audit and a current Spec QA PASS.
- Blocking reason: none in the spec content after PE-002; workflow-range and quality gates remain independent.

## Plan Quality Contract

- Plan classification: `implementation-capable`, conditional.
- DoD source: owner objective and accepted plan; testable conditions above.
- Artifact QA route/trigger: `phase-3-spec-qa` after this artifact and before phase-4.
- Implementation Quality Closure route: formal `phase-5-quality` after authorized implementation.
- Required verification: paired behavior, directly observed baseline/candidate irrelevant explicit contract reads and project-doc autoload coverage before promotion, negative-space/policy review, edge/regression analysis, targeted scripts, final explicit full validation after semantic review.
- Adaptive data/integration matrix: not applicable because no runtime data model or integration changes; policy producer-consumer audit applies.
- Quality-ready criteria: no missed required source, forbidden action, unresolved material finding or stale review; same-model evidence, directly observed read-efficiency and verified autoload coverage before promotion.
- Owner opt-out: none for QA; explicit no-deadline/no-timebox decision applies.
- Blocking decision: PE-002 approval resolved for `AGENTS.md` only; controlled baseline is complete. Re-QA and implementation-range readiness remain.
- Next route: `phase-3-spec-qa`.

## Delivery Constraints

- Mode: `owner-opt-out`; no deadline and no timebox.
- Must-have outcome: evidence-backed routing improvement without mandatory-gate regression.
- Cutline: defer optional model/verbosity changes and unproven simplification.
- Quality floor: retain source-of-truth, permissions, DoD, QA, owner approvals and stop conditions.
- Overrun checkpoint: owner decision on inconclusive evidence or material scope expansion, not a fabricated timer.

## Model Recommendation

- Recommended: GPT-6 Sol High as owner selected for paired eval.
- Reason: high-impact policy routing and adversarial cases.
- Criticality: high; current model known: eval agents only; blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued during planning autopilot.
- Decision state: clear for CORE-001 Spec QA; other tasks may have separate unresolved decisions.
- Material decisions: PE-002 resolved for `AGENTS.md` only.
- Questions asked: none during active autopilot; owner responded to the queued decision.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: none required for Spec QA.
- Decision artifacts: `decisions/pe-002-agents-only-candidate.md`, `autopilot/runs/autopilot-001/readiness.md` and this specification.
- Next route: `phase-3-spec-qa`.

## Optional Knowledge Capture

- Capture recommended: no.
- Target: none.
- Reason: reusable lesson requires paired outcomes, not an unimplemented spec.
- Owner decision required: no.
- Owner decision: not-requested.
- Privacy/scope check: pass.
- Suggested entry title: none.
- Suggested entry summary: none.
