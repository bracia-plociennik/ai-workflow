# Skill Discovery And Eval Freshness Handoff

## Metadata

- Date: 2026-09-29.
- Source system: AI Workflow.
- Counterpart: AI System.
- Status: accepted-for-handoff.
- Privacy/scope check: pass.
- Raw client data included: no.

## Concept And Intended Outcome

Keep skill discovery cheap without missing a relevant skill: select candidates from active skill frontmatter through its closing delimiter, then load the full contract only for plausible matches. Prevent a changed eval plan from reusing existing grading evidence by validating the full plan identity, producer metadata and grade locations before scaffold writes in the standard eval loop.

## Owner Decisions

- The owner approved a conceptual AI System handoff for this bounded AI Workflow improvement.
- This handoff does not authorize AI System implementation, source edits, commit, push, new permissions or final acceptance.
- The source implementation remains the six-path PSE-FIX-004 scope; a standalone aggregator redesign was not included.

## Safety And Authority Boundaries

- Skill metadata is candidate-selection evidence, not an approval or authority source. Relevant full `SKILL.md` content still governs skill use after matching and remains subordinate to repository contracts.
- A filename containing `skill` is not sufficient evidence that the task concerns a skill artifact.
- Persisted grades are not fresh merely because a regenerated manifest looks plausible. Reject incompatible or orphan grades before any output write; do not delete or silently reset them.
- Respect AI System's own source-of-truth, privacy, risk, permissions, QA, owner decisions and commit gates. Green scripts remain supporting evidence, not a quality verdict.

## Source-System Reference Map

- `AGENTS.md`: metadata-first Phase Skill Discovery and skill-artifact routing.
- `.systems/ai/core/operating-model.md`: candidate selection, delimiter boundary and workspace-before-system precedence.
- `.systems/scripts/check-phase-skill-discovery`: static contract enforcement.
- `.systems/scripts/check-validator-smoke-tests`: removal/contradiction mutations for discovery wording.
- `.systems/ai/skills/skill-creator/scripts/run_eval.py`: full-plan fingerprint and pre-write graded-run compatibility guard.
- `.systems/scripts/test-skill-eval-freshness`: changed-plan, orphan/legacy, compatible rerun and unchanged-tree regression cases.
- `.systems/ai/skills/skill-creator/scripts/run_loop.py`: guarded producer invocation before aggregation.
- `.systems/ai/skills/skill-creator/scripts/aggregate_benchmark.py`: separate consumer requiring an independent decision if standalone invocation must be protected.

## Counterpart Adaptation Checklist

1. Inventory active AI System skill namespaces and their canonical frontmatter schema. Verify that metadata-only reads stop at the closing delimiter and preserve workspace/user precedence.
2. Test should-trigger and non-trigger task cases with actual file-open traces; a direct skill review must still load its relevant full contract. Avoid relying on self-reported skill selection.
3. Map AI System's eval producer, grader and aggregator paths. Decide explicitly whether the standard producer path or also standalone aggregation requires stale-grade protection.
4. If grades persist across runs, bind them to the full eval-plan identity and all graded producer fields. Reject changed plans, missing metadata, unknown grade locations and legacy records whose freshness cannot be proved before writes.
5. Preserve compatible reruns and ungraded overwrite semantics; assert that rejected runs leave existing files byte-identical.
6. Review the full current diff for owner intent, DoD, risk, false positives/negatives, failure paths and producer-consumer alignment before using targeted and final validators.

## Validation And Smoke Expectations

- Discovery: three distinct non-trigger cases must not load an irrelevant skill body; a positive skill-artifact case must load the relevant body. Verify tool-open traces.
- Eval integrity: changed prompt, expectations, assertions, forbidden behavior, files, configurations, eval membership or source identity must reject graded reuse before writes.
- Failure paths: orphan or unexpected grade path, missing/altered metadata, missing manifest and old manifest without fingerprint fail closed. Compatible graded rerun and changed ungraded scaffold remain usable.
- Static/smoke checks support semantic findings-first QA; they do not authorize formal PASS.

## Evidence Limits And Residual Risk

The source comparison used one final synthetic model run per case. It supports the observed routing behavior only, not broad reliability, latency or token savings. The source fix protects the standard `run_eval.py`/`run_loop.py` path; manually invoking a standalone aggregator on arbitrary stale grades remains a separate boundary. AI System must adapt to its own schemas and commands instead of copying runtime files or treating this handoff as implementation authority.
