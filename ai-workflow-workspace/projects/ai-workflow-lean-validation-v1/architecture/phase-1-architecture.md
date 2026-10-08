# Phase 1 Architecture

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Date: 2026-09-29.
- Scope: LV001-LV006, Plan V2.
- Risk: high for eventual source implementation; this artifact is planning only.
- Sources: context.md, intake/phase-0-repo-intake.md, decisions/lv-decisions.md; current check-qa-evidence, check-validator-smoke-tests, validate-workflow, validation profiles/observability and full-qa-verification.
- Baseline: f362ce3; no tracked edits.

## Goals And Boundaries

Reduce redundant everyday work while increasing reliability of verdicts. Preserve source-of-truth order, semantic QA, risk/permission/approval boundaries, full CI and full canonical upstream-update checks.
Keep public standard/full/scoped/fast names and standard no-arg behavior. No result cache, auto changed-file selection, new production dependency or scheduler.
No historical report rewrite or fingerprint-based admission of newly invalid evidence.

## Components And Ownership

| Component | Producer | Consumer | Contract / invariant | Task |
| --- | --- | --- | --- | --- |
| Smoke outcome | child process and explicit assertion | smoke runner, timing, full validator | expected code AND expected diagnostic; infra error is never policy rejection | LV001 |
| Current QA assessment | formal QA template and phase executor | check-qa-evidence, status gate, human review | one explicit current run, its baseline/evidence/gate; bounded legacy support | LV001 |
| Timing stream | monotonic wrapper and smoke execution | baseline/candidate comparison | complete identified run; schema version, nesting, no payload leakage | LV002 |
| Scope selection | explicit owner/task scope + Git/runtime manifest | dependency map and validator dispatcher | requested-check success distinct from coverage completeness | LV003 |
| Smoke groups | authoritative test/assertion manifest | independent group runner and all/CI | all preserves every assertion, fixture invariant and failure path | LV004 |
| Instruction candidate | approved scope and eval rubric | identical synthetic baseline/candidate scenarios | behavior preservation before promotion; no eval approval inferred | LV005 |
| Closure | per-task reviews and comparisons | formal Phase 5, later Phase 6/7 | current semantic evidence first; scripts support, not decide | LV006 |

## Interfaces

1. Smoke helper: explicit expected statuses and diagnostic predicate, separate process/infrastructure outcome. Timeout tests opt into 124 explicitly. Log context must identify failed assertion and child command ID without exposing payload.
2. QA V2: structured fields embedded in Markdown under a unique current-run section, fenced-code-aware parsing and duplicate rejection. Single-run V1 compatibility remains; ambiguous legacy multi-run reports fail with a recovery route, never a guessed selection. No new run retroactively validates a historical one.
3. Timing: extend the existing TSV interface with versioned run metadata, record kind, parent ID and sub-second duration. Old five-column consumers require compatibility or same-scope migration. Never sum parent duration plus child durations as wall-clock.
4. Scoped: --checks remains explicit. A scope manifest supplies base/head/worktree facts and runtime roots; selection is deduplicated by check plus normalized scope/arguments, not bare name alone. Report execution-result and coverage-result independently. Unknown dependency escalates to full; unreadable/missing source stays blocked even after full.
5. Smoke: --group all remains default. Named groups get isolated fixtures and owner-attributed assertions. Full coverage is the union, and CI cannot silently substitute a subset.
6. Guidance: no global settings writes. Candidate instructions live in ignored synthetic eval inputs until owner-approved evaluation proves promotion safe. Current contract continues governing work.

## QA Run Identity And Compatibility

New evidence binds run-id, artifact-kind, task/project identity, reviewed source HEAD plus input-artifact SHA-256 map, verdict and one Gate Decision. Review content changes invalidate the assessed input identity. Evidence-record creation alone is not an input change.
Each acceptance assertion maps to evidence for that run. Assessment reports stay in the approved project/example quality root. Assessed inputs use a separate explicit root allowlist: canonical AI_WORKFLOW_HOME source, approved TARGET_REPO_ROOT source where applicable, and the owning project evidence root. No implicit widening, cross-project evidence borrowing, symlink escape or arbitrary last-PASS rule is allowed. Hashing follows read permissions: use explicitly approved non-secret inputs only. A discovered sensitive/unapproved path is metadata-only and blocks eligibility until safely resolved; do not open its contents merely to compute a digest.
V1 single-run reports retain their existing required evidence. Registered pre-V1 historical evidence remains exact-path/exact-hash only and cannot override V2 markers.
Status references must resolve the same assessment as the evidence validator; new producers and consumers ship together.

## Scope And Full-Gate Routing

| Work | Future intended route | Prerequisite |
| --- | --- | --- |
| Product work | semantic/code QA, product tests, relevant runtime checks | unchanged product/safety gates |
| Artifact QA | semantic artifact review then targeted checks | known artifact kind and owner namespace |
| Runtime-only capture/checkpoint | applicable capture/privacy/state/status evidence | explicit policy update, complete manifest, no shared framework change |
| Shared helper, validator, gate policy | targeted iteration then full final | high-risk source approval and fresh Spec QA |
| CI, release, final verification, upstream update | explicit full | all coverage, no skipped smoke |
| Unknown/unreadable sources | incomplete/blocked | resolve source issue; full cannot manufacture evidence |

The runtime-only checkpoint route is planned behavior, not permission to narrow current checkpoint validation now.

## Dependency Graph And Atomic Delivery

LV001 -> LV002 -> LV003 -> LV004 -> LV005 -> LV006.
LV005 requires the safe dispatcher/group route before replacing skill validation instructions.
Every task ships its matching contracts, templates, consumers and tests together. LV006 audits integration; it must not repair intentionally inconsistent earlier task deliveries.
LV002 records the post-correctness, instrumented monolith baseline before any selection/split optimization. LV006 compares eligible paths against that baseline.
A failed split retains monolith mode and records a fallback outcome; a deferred LV005 is not whole-project completion without a separate owner scope decision.

## Failure / Rework Matrix

| Source shape | Canonical state | Derived output | Forbidden state | Failure behavior | Planned verification |
| --- | --- | --- | --- | --- | --- |
| Policy test exits 127 | infrastructure failure | failed test/run | passing negative test | propagate nonzero and command ID | reserved-exit fixtures plus manual failure trace |
| Legacy report contains two candidate gates | ambiguous | recovery diagnostic | last/first PASS selected | block current gate without modifying history | multi-run parser fixtures |
| Deleted shared helper | high-impact scope | full-required selection | empty scoped success called complete | map historical path or fail unknown | rename/delete/base fixtures |
| Named group omits external assertion | coverage mismatch | split rejected | equal IDs called equivalence | retain monolith | assertion manifest plus mutation test |
| Candidate loses permission stop | behavioral regression | no promotion | shorter text accepted as improvement | retain current guidance | frozen forbidden-action cases |
| Run exits early with low wall time | incomplete measurement | excluded comparison | claimed speed gain | retain raw failure, no optimization verdict | incomplete-run comparison fixture |

## Security, Privacy And Recovery

No secrets/customer payloads in measurements or model fixtures; timing IDs and sanitized counts only. Full model execution requires LV-DEC-003. Use stdlib/local fixtures; external APIs remain disabled.
Revert only the scoped optimization with owner-approved Git action; preserve LV001 correctness fixes and historical evidence. No reset/rebase or rollback of unrelated commits.
No branch change for ignored planning; source work needs LV-DEC-002. Cross-system impact is LV-DEC-004 before commit/handoff.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted Plan V2 and context.md.
- Testable DoD / acceptance conditions: six components mapped to owners/consumers, unambiguous QA selection, scope coverage distinction, equivalence fallback, measurable baseline and behavioral promotion gate.
- Artifact QA route: phase-1-architecture-qa.
- Artifact QA trigger: after this architecture is reviewed, before phase-2-project-plan.
- Implementation Quality Closure route: phase-5-quality for each later task.
- Required verification: semantic artifact review; interface/producer-consumer mapping and failure matrix above; targeted artifact checks after QA.
- Quality-ready criteria: no unresolved planning blocker; implementation-only approvals explicitly separate.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: none for planning; LV-DEC-002/003/004 apply at later execution points.
- Next route: phase-1-architecture-qa.

## Delivery Constraints

- Mode: owner-opt-out.
- Deadline: none.
- Time budget: none.
- Timezone: Europe/Warsaw.
- Owner override: LV-DEC-001; explicit no-deadline/no-timebox for this project.
- Must-have outcome: preserve safety and coverage while reducing unnecessary validation cost.
- Should-have scope: measured workflow ergonomics improvements.
- Stretch scope: none.
- Explicitly deferred scope: automatic changed-file inference, cache, production changes.
- Quality floor: semantic QA, DoD, evidence, approvals and complete required coverage.
- Cutline rule: retain monolith if equivalence is inconclusive; defer LV005 promotion if behavioral evidence is inconclusive.
- Overrun checkpoint: no calendar limit; stop on material scope/permission conflict, infrastructure blocker or retry limit.

## Model Recommendation

- Recommended: GPT-5.6 Sol High.
- Reason: contract-preservation, parser and failure-path reasoning; advisory inherited guidance, not an assertion about current model availability.
- Criticality: high for future implementation.
- Current model known: no.
- Blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued.
- Decision state: clear.
- Material decisions: none blocking this planning phase; implementation gates remain explicit.
- Questions asked: none during running.
- Auto-resolved reversible decisions: kebab-case artifact names and sequential artifact writes.
- Optional owner refinements: none.
- Decision artifacts: decisions/lv-decisions.md.
- Next route: next declared planning phase only; stop before implementation.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: decision-artifact.
- Reason: preserve approved scope, safety boundaries and dependency gates.
- Owner decision required: no additional approval for requested planning artifacts.
- Owner decision: capture-now.
- Privacy/scope check: pass.
- Suggested entry title: Lean validation planning decisions.
- Suggested entry summary: current artifact and decisions/lv-decisions.md contain the planning evidence; no ad hoc global memory write.
