# Phase 3 Specification: PSE-FIX-004 Discovery And Eval Integrity

## Metadata

- Project: `prompt-and-skill-efficiency-v1`
- Task ID: `PSE-FIX-004-discovery-eval-integrity`
- Date: `2026-09-28`; readiness: `conditional` until Spec QA PASS.
- Risk: high; PE-012 and CR-001 bound the approved source scope.

## Sources And Intent

- Owner instruction: adversarially review Eval 004, then plan and implement its findings.
- Inputs: Eval 004 plan/result/traces, adversarial review, architecture and Architecture QA, PE-012, Plan QA addendum, current `AGENTS.md`, operating model, discovery validator, `run_eval.py`, `run_loop.py` and aggregator.
- Goal: stop full-body reads of unrelated active skills during routine discovery, and stop changed graded eval plans from reusing stale PASS evidence.
- Out of scope: `skill-creator/SKILL.md`, SKILL-002 reopening, model defaults, target repos, client data, `run_loop.py`, aggregator, commit, push and Phase 8.

## Definition Of Done

1. Candidate selection uses only active `SKILL.md` frontmatter name/description, checking workspace before system. Full body is read only after plausible match; non-matches are not read in full. Ambiguous plausible candidates may be inspected narrowly. Positive skill-artifact review still loads the relevant full body; generic product filenames with `skill` do not automatically trigger that route.
2. Three distinct synthetic non-trigger cases use no skill and do not open the irrelevant full skill body after the tracked change. A positive direct skill-review control loads the active skill. Actual tool-open traces, not self-report, establish this criterion.
3. On `run_eval.py --overwrite`, if any `grading.json` exists in the run tree, preflight compares the old manifest (including a canonical full-plan fingerprint) and all graded eval metadata against the desired plan. A changed prompt, expected behavior/assertions, files, forbidden behavior, configuration set, eval membership or source-plan identity rejects before any output write. A legacy graded run lacking that fingerprint cannot prove freshness and fails closed with a fresh-run instruction.
4. Grading at an unexpected eval/config path, missing old `run.json` or missing old `eval_metadata.json` rejects before writes. The error explains that a fresh output directory is needed; no grade is deleted or silently reset.
5. A same-plan graded rerun remains resumable. A changed ungraded scaffold can still be overwritten. Existing no-overwrite semantics remain unchanged.
6. Focused regression and smoke tests cover the positive and negative cases. No material P0/P1/P2 remains after findings-first current-diff review; formal Phase 5 considers the behavioral and runtime evidence before scripts, followed by applicable full validation.

## Exact Implementation Scope And Slices

| Slice | Files | Work | Check |
| --- | --- | --- | --- |
| S1 | `AGENTS.md`, `.systems/ai/core/operating-model.md`, `.systems/scripts/check-phase-skill-discovery`, smoke suite | Add frontmatter-first discovery, distinguish candidate selection from skill execution, enforce static boundary | Validator mutation tests and four-case model eval |
| S2 | `.systems/ai/skills/skill-creator/scripts/run_eval.py`, `.systems/scripts/test-skill-eval-freshness`, smoke suite | Build desired manifest/metadata in memory; preflight existing grade compatibility before `mkdir` or `dump_json`; reject changed/orphan grades | Tempdir runtime tests with pre/post hashes and actual loop path |
| S3 | Same approved files only | Review full current diff and run targeted/full checks | Formal Phase 5 quality evidence |

The six paths above are the entire approved tracked write set. Any extra path requires a new decision and refreshed Spec QA. Slice order does not grant write permission, phase approval or PASS.

## Producer-Consumer And Failure Rules

- `run_eval.py` produces `run.json` and `eval_metadata.json`; graders produce `grading.json`; `aggregate_benchmark.py` consumes grades. A grade is valid only for matching producer metadata.
- Grade discovery is recursive because the existing loop and aggregator use recursive discovery. Preflight rejects unknown locations rather than ignoring them.
- Construct desired metadata for all evals before touching the output tree. Store a canonical JSON fingerprint of the full source plan in `run.json`; compare stable manifest fields excluding only `created_at`. This catches `expected_behavior` changes even when explicit assertions mask them in `eval_metadata.json`.
- Compare full normalized JSON metadata for graded evals. Changed eval membership rejects even if an old grade happened to belong to an unchanged eval.
- A failure must leave all existing files byte-for-byte unchanged. No implicit reset, copy, deletion or downgrade to advisory grading.
- A plan with duplicate eval IDs/configurations is invalid before writes; otherwise one grade could ambiguously bind to multiple producers.
- If post-edit model eval still overreads, Phase 5 cannot claim DoD completion. Stop in fix loop or request a scoped decision rather than promoting a text-only fix.

## Edge Cases And Verification

| Case | Expected behavior | Evidence |
| --- | --- | --- |
| Grade on changed prompt or expected assertion | Reject before mutation | Snapshot hashes and error |
| Grade with missing metadata/manifest | Reject before mutation | Snapshot hashes and error |
| Grade in unknown eval or config directory | Reject before mutation | Snapshot hashes and error |
| Duplicate eval ID or config | Reject before mutation | CLI exit and unchanged tree |
| Same-plan graded rerun | Preserve grade; allow loop/report | Runtime test |
| Changed plan, no grades | Keep existing `--overwrite` flow | Runtime test |
| Three routine non-triggers | No full irrelevant body; no skill selected | Synthetic GPT-6 Sol High tool-open traces |
| Direct skill review | Relevant active `SKILL.md` body loaded | Synthetic GPT-6 Sol High tool-open trace |

## Plan Quality Contract And Implementation Gate

- Classification: implementation-capable; tracked writes: yes, exact six-file set above.
- DoD source: owner request, confirmed Eval 004 findings, PE-012 and this spec.
- Artifact QA route: `phase-3-spec-qa` before first tracked write.
- Post-implementation route: formal `phase-5-quality`, followed by owner-directed phase 6/7 as applicable; Phase 8 separately owner-triggered.
- Required checks: source-level semantic review, producer-consumer audit, targeted regression, discovery smoke, actual behavioral eval, full workflow validation after semantic review.
- Quality-ready: no unresolved P0/P1/material P2, complete runtime/behavioral evidence and current-diff review.
- Opt-out: none. Adaptive product data/integration matrix: not applicable to product data; eval producer-consumer matrix above is required.
- Blocking decision: none within PE-012; stop on expanded write set or failed behavioral eval.
- Can enter implementation: only after fresh Spec QA PASS and targeted instruction refresh.
- Next route: `phase-3-spec-qa`.

## Delivery Constraints And Owner Decision Checkpoint

- Owner-approved no deadline/timebox; quality floor and stop rules unchanged.
- Interaction mode: none; decision state: clear inside PE-012; material decisions: PE-012; questions asked: none.
- Auto-resolved reversible decisions: none; optional refinements: none; decision artifact: `decisions/pe-012-eval-004-remediation.md`.
- Model recommendation: GPT-6 Sol High for high-risk policy/evidence integrity; advisory only, blocking: no.

## Optional Knowledge Capture

- Capture recommended: yes; target: project-memory; reason: save the verified eval-integrity lesson after Phase 5.
- Owner decision required: no; owner decision: defer-to-distillation; privacy/scope check: pass.
- Suggested entry title: Skill discovery and graded-eval freshness.
- Suggested entry summary: Record only evidence-backed behavior and fail-closed grade compatibility.
