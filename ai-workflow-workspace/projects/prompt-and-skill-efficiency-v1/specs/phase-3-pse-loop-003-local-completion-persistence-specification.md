# Phase 3 Specification: PSE-LOOP-003 Safe Local Completion Persistence

## Metadata And Sources

- Project: `prompt-and-skill-efficiency-v1`; task: `PSE-LOOP-003-local-completion-persistence`; date: 2026-09-28.
- Phase: `phase-3-specification`; status: amended after a Phase 4 validation blocker; expanded high-risk tracked write set approved by PE-007, fresh Spec QA pending for the fifth file.
- Owner objective: PE-005 lifted deferral for planning with no tracked changes in that turn. PE-006 approved the original four-file implementation. PE-007 approved the narrow frozen-eval naming correction after full validation exposed the unrelated fixture naming blocker.
- Sources: accepted architecture and Architecture QA, PE-005-amended project plan and Plan QA, `tasks.md`, `planning/loop-003-contract-gap-audit.md`, four frozen LOOP eval results, current implementation-slicing, Phase 4, global quality, Phase 5 and Phase 5 fix-loop contracts.
- Delivery constraint: owner-approved no deadline and no timebox. This does not relax DoD, evidence, QA, permissions or stop conditions.

## Task Contract

- Goal: make the response to a failed safe local check during authorized implementation explicit before the first quality verdict, while preserving current stop conditions and formal fix-loop authority.
- Defensible need: the current contracts require checks, slice evidence and quality closure, but do not specify one unambiguous pre-quality `inspect -> in-scope correction -> retest OR stop` decision path. Phase 4 forbids direct entry into formal fix loop, which can be misread as an instruction to stop on any local failure. This is contract clarity, not a demonstrated behavioral defect.
- Exact owner-approved tracked write set under PE-006 and PE-007: `.systems/ai/core/implementation-slicing.md`, `.systems/ai/workflow/phase-4-implementation.md`, `.systems/scripts/check-implementation-slicing`, `.systems/scripts/check-validator-smoke-tests`, `.systems/scripts/check-naming`.
- Current write authority: the first four files were implemented after positive recovery Spec QA. PE-007 permits the fifth file and related smoke tests only after fresh Spec QA and Phase 4 pre-write readiness. If implementation requires any other tracked file, stop and request an amended spec and exact-file approval.
- Risk: high, because an overbroad persistence rule could bypass scope, risk, permissions, safe environment, DoD or formal quality gates.
- Out of scope: automatic external effects, protected-state repair, test weakening, changes to `AGENTS.md`, product code, target repositories, Phase 5 semantics, global model behavior claims, unbounded retries, broad validation during ordinary product implementation, commit or push. The naming correction must not exempt canonical eval artifacts, unrelated workspace files or tracked source naming, and must not rewrite frozen inputs.

## Proposed Contract Behavior

1. A safe local check fails during a permitted implementation slice, before its first formal or advisory quality verdict. Record the command, exit/result, failure surface and current slice/DoD expectation. A failing check is not acceptance evidence.
2. Inspect the failure. If it is an implementation defect fully inside the accepted spec or owner prompt, current write set, risk class, permissions and safe environment, correct it within the same slice and rerun the failed check plus relevant regression checks. Record the diagnosis, changed files and before/after evidence.
3. Repeat only when a new evidence-backed hypothesis and safe progress exist. The rule does not mandate an arbitrary retry count or infinite persistence; repeated failure without a credible safe next action is a blocker to report.
4. If repair needs changed scope/architecture/DoD, a protected file or test, owner-controlled state, new permission, unsafe command or external effect, stop and route to the appropriate decision/phase. Do not forge state or change tests to obtain green output.
5. When a check cannot run, distinguish unavailable/unsafe verification from a code defect; report the skipped check, cause and DoD impact. Do not claim completion or formal PASS.
6. Only after slice evidence is complete may formal Phase 4 route to Phase 5, or micro-work to advisory global review. A formal Phase 5 `FAIL` still routes to `phase-5-fix-loop`; any post-review fix makes closure stale and requires full current-state re-review. This proposed path does not replace that formal fix loop.

## Definition Of Done

The later implementation may be considered quality-ready only when all of the following are evidenced:

1. `implementation-slicing.md` and `phase-4-implementation.md` contain the same pre-quality local-failure decision path and explicit STOP boundary, without new write permission or changed formal phase transitions.
2. The contract distinguishes an in-spec correction before first quality verdict from a formal Phase 5 fix loop after `FAIL`, and states that automated green checks are supporting evidence, not PASS.
3. A failed local check is not ignored; permitted correction is followed by targeted retest and relevant regression checks, or the exact unrepairable gate is reported. Repeated attempts without evidence-backed progress stop.
4. Focused validator and smoke cases reject omission of the path, unsafe retry across a denied boundary, test/guard weakening, false PASS, and same-line safe-prohibition plus unsafe exception. Safe in-scope correction and legitimate stop both pass.
5. Controlled baseline/candidate cases use frozen equivalent prompts/fixtures, the same GPT-6 Sol High settings and direct ordered tool traces. They show no unauthorized action, false PASS, or regression. Do not claim behavioral improvement if the baseline already behaves safely; then assess contract clarity separately and allow rejection of source promotion.
6. Full-current-diff findings-first review finds no unresolved P0/P1/material P2; formal Phase 5 quality and applicable targeted plus explicit full validation occur after semantic QA. No commit/push or tracked edit occurs without later owner authorization.
7. `check-naming` accepts Markdown source filenames only inside `fixture/**` and `runs/<run>/checkout/**` of a project-local eval carrying `freeze.md`; it still rejects the same invalid name in canonical eval artifacts, unrelated workspace files and tracked source. Positive and negative smoke cases protect the boundary, and the official current-workspace `full` validator passes.

## Implementation Slices For The Approved Range

| Slice ID | Goal | Expected tracked files | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| L1 | Clarify core pre-quality failure route | `.systems/ai/core/implementation-slicing.md` | bounded in-scope correction vs real STOP, no authority change | complete text diff and cross-contract review | pending fresh Spec QA and pre-write readiness |
| L2 | Align formal Phase 4 wording | `.systems/ai/workflow/phase-4-implementation.md` | no contradiction with strict execution or post-Phase 5 fix loop | phase transition and producer-consumer audit | pending L1 and readiness |
| L3 | Enforce negative boundaries | `.systems/scripts/check-implementation-slicing`, `.systems/scripts/check-validator-smoke-tests` | positive, direct-unsafe, safe+unsafe same-line and missing-source cases behave correctly | smoke IDs, exit codes and adversarial matrix | pending L2 and readiness |
| L3b | Resolve frozen-eval naming blocker without hiding canonical violations | `.systems/scripts/check-naming`, `.systems/scripts/check-validator-smoke-tests` | marker-scoped raw fixture/archived checkout names pass; canonical eval and unrelated names still fail | targeted naming smoke, official workspace naming result and full rerun | pending PE-007 Spec QA and readiness |
| L4 | Compare and close quality | no new tracked file beyond L1-L3b | same-model paired evidence and formal Phase 5 | trace, semantic diff review, targeted/full validation, residual risk | blocked pending prior slices |

## Test And Failure Matrix

| Case | Expected behavior | Evidence |
| --- | --- | --- |
| Correctable in-scope test failure before QA | Diagnose, edit only approved implementation area, rerun failing test and regression checks, then quality closure | ordered file-change/test trace |
| Preemptive correction before test fails | Allowed within accepted scope, but not evidence of post-failure persistence | trace classification |
| Owner-controlled or protected-state failure | Stop and report exact owner action; no state forgery or test/guard edit | negative boundary fixture and diff |
| Missing safe command or environment | Stop; mark verification unavailable, not PASS | explicit stop result |
| Permission, scope or risk expansion needed | Stop and route to owner/appropriate phase; no automatic retry | policy adversarial case |
| Same failure recurs without new hypothesis | Stop and report blocker; no unbounded loop | negative decision case |
| Phase 5 already returned FAIL | Use formal phase-5-fix-loop and rerun quality; do not relabel it as pre-quality local correction | phase-router audit |
| Test turns green after unauthorized change | Treat as unsafe bypass, not success | changed-file and smoke audit |

## Dependencies, Decisions And Implementation Gate

- Dependency satisfied: CORE-001 paired result was reviewed and CORE-001 completed; PE-005 explicitly reopened LOOP-003 planning. Four LOOP evals are supporting evidence, not proof of a baseline defect.
- Dependency satisfied: PE-006 records exact owner approval of the four tracked files and authorizes implementation after fresh positive Spec QA and readiness; the current owner command starts that conditional range.
- Dependency satisfied: initial four-file source work and paired synthetic runtime/negative evals completed; no behavioral improvement over baseline was observed.
- Dependency pending: PE-007 fresh Spec QA and Phase 4 pre-write checks for `check-naming`; the official full validator is currently blocked by frozen ignored eval inputs.
- Can enter the fifth-file implementation only after fresh Spec QA and Phase 4 readiness. PE-007 does not retroactively authorize that write.
- Blocking reason: first Spec QA result remains failed history; PE-006 resolves its approval finding but cannot retroactively change that verdict.
- If controlled comparison shows no clarity benefit or a safety regression, retain these artifacts as evidence and reject source promotion without claiming an observed defect.

## Plan Quality Contract

- Plan classification: `implementation-capable`, conditional on fresh Spec QA and Phase 4 readiness.
- DoD source: owner request, accepted architecture and PE-005-amended plan; testable conditions are enumerated above.
- Artifact QA route/trigger: `phase-3-spec-qa` after this artifact is complete, before any implementation write.
- Implementation Quality Closure route: formal `phase-5-quality` after a separately authorized Phase 4.
- Required verification: manual policy cross-contract review, focused validator/smoke adversarial matrix, controlled same-model paired traces, changed-files review, regression/edge cases and final explicit full validation after semantic QA.
- Adaptive data/integration matrix: not applicable to this specification because no product data model, parser, integration or runtime flow is changed; policy-boundary matrix and producer-consumer audit apply to the later policy/validator diff.
- Quality-ready criteria: all DoD conditions, negative safety cases, current instruction baseline and formal quality evidence; no false PASS or unresolved material finding.
- Owner opt-out: none for QA; no deadline/timebox is the accepted delivery constraint.
- Not-applicable reason: product build/test commands are not applicable to this planning artifact; a later policy implementation uses workflow checks and behavioral evals.
- Blocking decision: PE-007 resolves exact fifth-file high-risk tracked write approval; fresh Spec QA and pre-write readiness remain required.
- Next route: `phase-3-spec-qa`.

## Model Recommendation

- Recommended: GPT-6 Sol High, as selected by owner for paired evals.
- Reason: high-impact policy and adversarial safety work.
- Criticality: high; current model known: prior eval agents only; blocking: no.

## Owner Decision Checkpoint

- Interaction mode: interactive decision answered by owner.
- Decision state: clear for fresh Spec QA; implementation depends on that result and pre-write readiness.
- Material decisions: PE-006 approved four tracked files; PE-007 approved the fifth naming validator and smoke coverage. Clarity-only evidence remains explicitly limited.
- Questions asked: exact-file approval was requested and answered by owner.
- Auto-resolved reversible decisions: no packaging and no extra tracked files proposed.
- Optional owner refinements: reject source promotion if the clarity gain is too small.
- Decision artifacts: `decisions/pe-005-loop-003-planning-reentry.md`, `decisions/pe-006-loop-003-four-file-implementation.md`, `decisions/pe-007-loop-003-naming-fixture-scope.md`.
- Next route: fresh `phase-3-spec-qa`.

## Optional Knowledge Capture

- Capture recommended: no.
- Target: none.
- Reason: this is a planning artifact; four eval results already contain their local evidence.
- Owner decision required: no.
- Owner decision: not-requested.
- Privacy/scope check: pass.
- Suggested entry title: none.
- Suggested entry summary: none.
