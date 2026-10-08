# Lean Validation: AI System Handoff

## Concept And Outcome

Treat verdict integrity as a prerequisite for making validation faster. A negative test succeeds only for its intended exit status and cause-specific diagnostic. A formal QA result has one current, scope-bound assessment; the status consumer reads the same assessment rather than matching prose or combining fields from different runs.

AI Workflow has implemented verdict integrity (LV001), source-bound timing/baseline measurement (LV002), explicit scoped selection (LV003), assertion-preserving smoke partition (LV004) and included-scope integration (LV006). Instruction efficiency (LV005) is explicitly owner-deferred; no model-behavior benefit or promotion is claimed.

## Owner Decisions

- Shared impact with AI System: yes; prepare one conceptual handoff for the accepted lean-validation program.
- AI System adaptation is a separate future task. This artifact does not authorize editing its repository, running its migrations, or changing its workflow gates.
- Preserve historical QA evidence; do not rewrite prior outcomes to make a new validator green.

## Safety And Authority Boundaries

- Semantic findings-first QA, DoD and owner intent precede scripts. Green scripts alone cannot produce PASS.
- Missing, stale, cross-task, contradictory or unreadable evidence fails closed. A historical result cannot fill a missing current field.
- An exact legacy fingerprint may preserve historical admission but does not certify new evidence.
- Keep the counterpart's source-of-truth, permissions, risk, approvals and final-owner gates intact. No auto-commit, push, deployment or cross-repo write is implied.

## AI Workflow Source References

- `.systems/scripts/check-validator-smoke-tests`: expected-status/diagnostic contract and completion sentinel.
- `.systems/scripts/lib/qa-evidence.py`: versioned current assessment, scoped input hashes, identity and gate validation.
- `.systems/scripts/check-qa-evidence` and `.systems/scripts/check-status-consistency`: shared assessment consumers.
- `.systems/ai/core/full-qa-verification.md`: QA evidence and compatibility rules.
- `.systems/ai/templates/workflow/phase-5-quality.template.md`: current formal implementation-quality producer.

## Validators And Smoke Expectations

- Positive: intended negative-case rejection; coherent current QA report; same task and inputs recognized by QA and status; valid historical compatibility.
- Negative: zero or wrong/reserved exit, wrong diagnostic, incomplete runner, duplicate current run, contradictory verdict/gate, stale hash, wrong task, traversal or escaping symlink, failed current check hidden under PASS, and PASS routed into a fix loop.
- Validate the adapted producer and every consumer together. Compare actual failure diagnostics, not merely nonzero exits or the count of test IDs.
- Run counterpart semantic QA and applicable local validators; treat both as separate evidence. Do not claim equivalent behavior from source-copying alone.

## Adaptation Checklist For AI System

1. Inventory current QA producers, status consumers, old evidence admission and negative-test helpers.
2. Define a versioned current assessment and stable task/scope identity using AI System's own schema; avoid importing AI Workflow paths or runtime artifacts as authority.
3. Implement one parser or reader used by QA and status, with explicit input provenance and bounded approved roots.
4. Add positive and adversarial fixtures for process status, mixed history, stale/wrong-task evidence, privacy boundaries and phase routing.
5. Review actual current diff and failure paths before declaring quality readiness. Preserve immutable historical reports.

## LV002: Source-Bound Measurement And Output Safety

- Use monotonic timing and one versioned producer-consumer schema. Keep wall-clock separate from child attribution; never add a full suite wall to its child durations.
- Bind a run to its reviewed source digest, timing bytes and check/test inventories. Capture locally; reject incomplete, duplicate, drifted or mismatched runs. Keep earlier measurements as source-specific history rather than rewriting them.
- Require three equivalent complete samples before comparison; retain range/noise and conservative limitations. Green scripts and lower counts are not proof of safety, behavior equivalence or improvement.
- Inspect output tracking and ownership before opening a file, independently of TMPDIR and process CWD. Include foreign temporary repositories and deleted tracked paths in adverse fixtures. Isolate system-wrapper side effects during hostile-environment tests.
- Relevant implementation: .systems/scripts/lib/validation-timing.py; .systems/scripts/report-validation-comparison; validate-workflow and check-validator-smoke-tests; .systems/ai/core/validation-observability.md.
- Add counterpart-specific tests for sink containment, source drift, one completion marker, failure/timeout/interrupt, typed parent relationships, timing/manifest digest mismatch, duplicate inventory and conservative comparison. Runtime input IDs still need actual operator-reviewed equivalence.
- LV002's corrected baseline is complete locally; it is not a claimed speed gain. AI System should measure its own source and inputs, not import AI Workflow's numeric runtime as an acceptance threshold.

## LV003: Explicit Scope Is Not Quality Authority

- Separate requested execution, required dependency coverage and final-evidence eligibility. Bare selected checks cannot claim complete coverage; a manifest is evidence, not permission or semantic PASS.
- Bind canonical source Git facts and independent owned runtime inventories before/after dispatch. Deduplicate only identical check/root/options; distinct roots remain separate invocations.
- Bound runtime consumers to actual ownership. Tracked runtime is not automatically framework source, while deleted, raw, foreign, unselected, sensitive or escaping inputs remain conservative.
- If AI System adopts a runtime-only checkpoint exception, make it explicit and require all applicable privacy/capture/status/QA consumers, unchanged system source and fresh inputs. Keep CI/updater/high-impact source gates full-required.
- Preserve failure/timeout/interrupt and existing timing schema. Keep logs outside frozen assessed roots. Reassess changed source dependencies honestly; never update old QA hashes to manufacture freshness.
- Source references: .systems/scripts/lib/validation-scope.py; lib/validation-checks.json; validate-workflow; naming/status/QA/distillation runtime consumers; .systems/ai/core/validation-profiles.md and validation-routing.md; phase-7 checkpoint template.
- Counterpart tests: duplicate/distinct scopes, unknown/cyclic dependencies, staged/unstaged/rename/deletion/newline inventory, stale snapshot, sensitive/escaping roots, zero-result incomplete dispatch, changed registry/source and tracked owned runtime.
- These concepts require AI System-specific schemas and ownership mapping; source copying alone is not equivalent coverage or speed evidence.

## LV004: Independent Smoke Groups Require Semantic Ownership

- Keep one public dispatcher with exact ownership of tests, assertions, setup, mutations and cleanup. Pure shared helpers must not execute setup on import; each group uses fresh isolated source fixtures.
- Preserve whole transactions, not arbitrary line ranges. Map assertions outside wrappers and nested failure assertions explicitly; compare real typed rejection causes and protected mutations, not only ID counts or hashes.
- Bind literal integration references to live executed test/command contracts. Audit every structural consumer, including the full runner, alongside direct validators.
- Retain one public completion/timing wall; group markers are namespaced and subset runs cannot become full evidence. Full/CI continue all groups. Maintain source/manifest mapping atomically and rerun actual equivalence after membership/helper changes.
- Local process metadata supports cleanup of observed own descendants even after a leader fails. Test real interruption, timeout, ordinary failure, early-zero, missing source, and cleanup failure; do not globally kill by process name or claim containment of arbitrary malicious detached jobs.
- Use counterpart-specific disposable root names: canonical namespace components can change legacy reader behavior even when fixture contents match.
- Source references: .systems/scripts/check-validator-smoke-tests; .systems/scripts/smoke/manifest.json and common.sh; five owned group files; check-validation-observability and check-validation-completion; .systems/ai/core/validation-observability.md.
- Adoption must repeat AI System-specific original/partition, assertion/mutation and producer-consumer equivalence. AI Workflow's execution counts or local timings are not counterpart acceptance thresholds or speed evidence.

## LV006: Honest Included-Scope Integration

- Integrate accepted predecessor evidence using current input identities and whole-interface review. A final integration task is not permission to repair outside its ceiling or hide deferred work.
- Owner-approved deferral must agree across composite plan, specification, task index, status, capture state and final review. Preserve original unmet DoD and failed evidence; do not convert deferral to implementation acceptance.
- Completion/index changes can stale previously bound Plan/Spec QA. Perform real whole-artifact re-review and append a new current assessment, retaining old runs.
- Distinguish structural manifest verification, requested execution, complete coverage, semantic quality and final-owner approval. None grants the next authority automatically.
- Measure only equivalent sources/scenarios/populations. Different full test inventories cannot prove a speed gain; narrower justified iteration has a separate scope.
- Source references: changelog.md; validation profiles/routing/observability; current QA reader; full runner, CI/updater and smoke manifest. Program-specific local evidence is supporting context, not an AI System runtime schema.
- AI System should repeat its own scope/disposition, coverage, privacy and current-identity tests before adoption. No copied numeric timing threshold or imported project state.

## Current Privacy And Limits

- Privacy/scope check: pass; no raw client data, client names, secrets, credentials, production identifiers or private runtime content.
- This handoff contains system concepts and source references only. Accepted included integration does not mean LV005 or AI System adaptation is complete.
- Linux CI for the local-only AI Workflow commits and counterpart-specific behavior remain unverified; no commits have been pushed in this range.
