# 2026-09-29 - Skill Discovery And Eval Freshness

- Date: `2026-09-29`
- Topic: `PSE-FIX-004 metadata-first skill routing and graded-eval integrity`
- Type: `testing-note`
- Status: `active`
- Scope: future skill-discovery and eval work in `prompt-and-skill-efficiency-v1`.
- Source: `distillations/phase-6-pse-fix-004-discovery-eval-integrity-distillation.md` and its formal Phase 5 quality artifact.
- Evidence: three final synthetic non-trigger tool traces read frontmatter only, a direct skill-review control loaded the relevant body, runtime freshness regression passed, and full workflow validation completed on the six-path diff.
- Rule: select skill candidates from `name` and `description` through the closing frontmatter delimiter; open full `SKILL.md` only after a plausible match. Bind persisted grades to the complete plan fingerprint and graded producer metadata before standard-loop aggregation.
- Boundary: the manually invoked standalone aggregator is outside the guarded path. A one-run-per-case synthetic eval does not prove reliability or performance savings.
- Review trigger: a new skill-routing change, eval metadata/schema change, or observed stale-grade aggregation path.
