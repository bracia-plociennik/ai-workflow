"""Persist the explicitly performed 2026-09-30 regression and LV003 reviews."""
import importlib.util
from pathlib import Path

root = Path.cwd()
project = root / 'ai-workflow-workspace/projects/ai-workflow-lean-validation-v1'
spec = importlib.util.spec_from_file_location('assessment', project / 'implementation/record-current-assessment.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

def inputs(source, evidence):
    return [('workflow-source', p) for p in source] + [('owning-project-evidence', p) for p in evidence]

plan = 'planning/phase-2-project-plan.md'
q1 = 'quality/phase-5-lv-core-001-verdict-integrity-quality.md'
q2 = 'quality/phase-5-lv-obs-002-baseline-quality.md'
q3s = 'quality/recovery-phase-3-lv-val-003-scoped-selection-spec-qa.md'
spec3 = 'specs/phase-3-lv-val-003-scoped-selection-specification.md'
scope_sources = [
    '.systems/scripts/validate-workflow', '.systems/scripts/lib/validation-scope.py',
    '.systems/scripts/lib/validation-checks.json', '.systems/scripts/check-status-consistency',
    '.systems/scripts/check-qa-evidence', '.systems/scripts/check-distillation-state',
    '.systems/scripts/check-naming', '.systems/scripts/check-validation-profiles',
    '.systems/scripts/check-validation-routing', '.systems/scripts/check-validator-smoke-tests',
    '.systems/ai/core/validation-profiles.md', '.systems/ai/core/validation-routing.md',
    '.systems/ai/core/contract-compliance.md', '.systems/ai/core/commands.md',
    '.systems/ai/workflow/phase-7-checkpoint.md',
    '.systems/ai/templates/workflow/phase-7-checkpoint.template.md', 'AGENTS.md', 'HUMANS.md', 'README.md',
]
e1 = '''- This is a new regression assessment, not a hash-only renewal of the earlier PASS.
- Re-read the smoke outcome wrappers: ordinary negative cases require their exact expected status and cause-specific diagnostic; reserved exits remain rejected. The LV003 scope cases add exact diagnostics without relaxing old cases.
- Re-read the changed status/QA runtime branches against the unchanged typed qa-evidence.py reader. Runtime-only dispatch remains bounded; no current verdict is inferred from historical PASS or green scripts.
- The byte-matched final source full run completed forty checks and 674 distinct smoke IDs, preserving all 660 LV002 IDs. Source-only verification is not private-runtime completion; the current actual full gate follows these reviewed assessments.
- Manual failure trace: missing/stale current QA -> typed rejection -> original nonzero -> one failure completion marker. LV003 probes exercised incomplete finish and real runtime consumers. Linux CI remains unrun.
'''
d1 = [
    ('Exact negative outcome and diagnostic', 'Current wrapper source, reserved-exit clauses and unchanged old cases reviewed; full smoke supports the audit.'),
    ('Current QA and status bind evidence', 'Unchanged typed reader plus bounded real-consumer tests reject missing, conflicting and stale current evidence.'),
    ('Regression and authority boundaries', 'CI/updater and formal gates unchanged; no lost old IDs or source outside approved LV003 scope.'),
]
b1 = qa.body(e1, d1).replace('runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.', 'smoke outcome wrappers, typed current QA reader, status/runtime dispatch and lifecycle markers.')
qa.record(project / q1, 'lv001-regression-lv003-2026-09-30', 'implementation-quality', 'ai-workflow-lean-validation-v1:LV-CORE-001-verdict-integrity', inputs([
    '.systems/scripts/check-validator-smoke-tests', '.systems/scripts/lib/qa-evidence.py',
    '.systems/scripts/validate-workflow', '.systems/scripts/check-status-consistency',
    '.systems/scripts/check-qa-evidence', '.systems/scripts/lib/policy-boundaries.sh',
], [plan, 'specs/phase-3-lv-core-001-verdict-integrity-specification.md', 'implementation/lv003-source-full-final.log']), b1)

e2 = '''- Fresh semantic regression review covers the runner's new scoped dispatch and original timing/finish traps against unchanged validation-timing.py and report-validation-comparison.
- Re-executed ten sink-boundary probes and three comparison probes successfully. Five lifecycle probes confirm exits 7, 124, 1, 143 and 0, one completion marker and truthful fail/timeout/interrupted/pass wall results.
- Lifecycle harness required the runner's existing resolver dependency and a child-start handshake outside the fixture Git tree. Earlier race and real source-drift failures are not hidden; no tested exit expectation was weakened.
- The original three frozen LV002 full runs and their 40-check/660-ID inventories remain immutable historical baseline for their original source. They are not relabelled as a current baseline or used to claim speedup. The LV003 source full run covers 40 checks and 674 IDs on different inputs.
- Manual trace: normalized invocation ID -> nine-column timing child -> finish snapshot -> original failure propagation -> wall record. Malformed/partial/reused comparison runs remain rejected; output sinks remain exclusive, tracked/foreign-repo protected.
'''
d2 = [
    ('Timing producer-consumer schema', 'Nine columns unchanged; normalized scope IDs remain privacy-safe unique child identities.'),
    ('Original lifecycle outcome', 'Five current lifecycle probes, including actual SIGTERM handshake, preserve exit and single marker/wall result.'),
    ('Safe sinks and comparison evidence', 'Ten boundary and three comparison probes passed; current source review confirms typed reject paths.'),
    ('Historical baseline preservation', 'Three original complete frozen runs retained unchanged, explicitly not current performance evidence.'),
]
qa.record(project / q2, 'lv002-regression-lv003-2026-09-30', 'implementation-quality', 'ai-workflow-lean-validation-v1:LV-OBS-002-baseline', inputs([
    '.systems/scripts/validate-workflow', '.systems/scripts/check-validator-smoke-tests',
    '.systems/scripts/lib/validation-timing.py', '.systems/scripts/report-validation-comparison',
    '.systems/scripts/check-validation-observability', '.systems/ai/core/commands.md',
], [plan, 'specs/phase-3-lv-obs-002-baseline-specification.md', q1,
    'implementation/lv002-lifecycle-probes.py', 'implementation/lv003-lifecycle-regression.log',
    'implementation/lv002-final-reviewed-001.json', 'implementation/lv002-final-reviewed-002.json',
    'implementation/lv002-final-reviewed-003.json']), qa.body(e2, d2))

e3s = '''- Fresh full specification review against the current nineteen-path implementation, accepted plan and current LV001/LV002 regression assessments; old Spec QA remains historical.
- V3-01..10, typed manifest/registry, bounded runtime consumers, nine-column timing and finish freshness map coherently to accepted scope. Current docs implement the same narrowly bounded checkpoint exception, not broad scoped final evidence.
- Reviewed negative paths: no manifest, deleted/renamed source, unknown dependency, raw/unowned root, source drift, incomplete execution, tracked target-owned runtime and sensitive/symlink inputs. No permission or formal PASS comes from a manifest.
- Existing full CI/updater and high-impact source gates remain unchanged. Nineteen-path ceiling matches the actual diff; no outside consumer change. This is specification regression QA, not a substitute for implementation Phase 5.
'''
qa.record(project / q3s, 'lv003-spec-regression-2026-09-30', 'spec-qa', 'ai-workflow-lean-validation-v1:LV-VAL-003-scoped-selection', inputs(scope_sources, [plan, spec3, q1, q2]), qa.body(e3s, [], artifact=True))

e3 = '''- Owner LV-DEC-008 explicitly approves the high-risk gate and fresh prerequisite regression, followed by evidence-backed capture/commits and later tasks. No push or final-owner-yes.
- Findings-first review covers all nineteen current source paths, exact accepted V3 scope/DoD, manifest/registry schemas, CLI/traps, all four bounded runtime consumers, policies/templates and added smoke assertions.
- Manual success trace: canonical snapshot -> explicit dependency closure -> root/check normalization -> dispatch -> finish re-plan -> separate coverage/eligibility. Manual failure trace: changed assessed inputs or missing dependency -> nonzero/ineligible -> original lifecycle result retained.
- Eleven fresh synthetic probe groups passed: dedup, projects, graph, git, freshness, ownership, paths, checkpoint, source, finish and consumers. Consumer probes use actual scripts; dispatch stubs are not misrepresented as runtime consumer proof.
- Current LV001/LV002 regression and Spec QA are separately recorded with hashes, preserving earlier runs. The final byte-matched source full run passed in 553 seconds with forty checks and 674 unique smoke IDs, zero old ID loss. It is source-only evidence; the actual runtime full gate is still required before capture/commit.
- No performance improvement is claimed; no CI/updater, timing/comparison helper, cache, automatic selection, network or foreign repository change. Local Bash 3.2 dispatch, inherited child environment and tracked-runtime classification corrections were re-reviewed after their final edits.
'''
d3 = [
    ('V3-01 normalized dependency deduplication', 'dedup and projects probes; stable unique check/root/project IDs; framework checks once.'),
    ('V3-02 separate project invocations', 'projects probe; distinct timing IDs for distinct owned roots.'),
    ('V3-03 explicit known acyclic checks', 'graph probe and registry validation reject missing, empty, unknown and cyclic dependency.'),
    ('V3-04..05 complete Git inventory', 'git probe: NUL staged/unstaged/rename/deletion/newline/untracked, index/base binding.'),
    ('V3-06 freshness and honest coverage', 'freshness and finish probes; absent manifest unverified; drift and incomplete zero-result rejected.'),
    ('V3-07 owned runtime boundaries', 'ownership and consumers probes; raw/foreign roots not assessed as active producers.'),
    ('V3-08 missing/unreadable/escaping inputs', 'paths probe and content-before-read guards; symlink/sensitive/unreadable inputs fail.'),
    ('V3-09 bounded checkpoint policy', 'checkpoint probe, docs/templates and real QA/state consumers; semantic gates separate.'),
    ('V3-10 source/full and lifecycle integrity', 'source and finish probes; forty full checks retained; CI/updater unchanged; five LV002 lifecycle probes.'),
]
qa.record(project / 'quality/phase-5-lv-val-003-scoped-selection-quality.md', 'lv003-quality-2026-09-30', 'implementation-quality', 'ai-workflow-lean-validation-v1:LV-VAL-003-scoped-selection', inputs(scope_sources, [plan, spec3, q1, q2, q3s,
    'implementation/phase-4-lv-val-003-scoped-selection-implementation.md',
    'implementation/lv003-scope-probes.py', 'implementation/lv003-source-full-final.log']), qa.body(e3, d3))
