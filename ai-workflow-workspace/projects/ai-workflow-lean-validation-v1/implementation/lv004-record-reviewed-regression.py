"""Persist the separately performed LV004 current-source regression review."""
import importlib.util
import json
from pathlib import Path
import re
import shutil

root = Path.cwd()
project = root / 'ai-workflow-workspace/projects/ai-workflow-lean-validation-v1'
log = Path('/tmp/lv004-source-full-final-002.log').read_text()
assert len(re.findall(r'^AI_WORKFLOW_VALIDATE_COMPLETE .*result=pass exit_code=0 ', log, re.M)) == 1
ids = re.findall(r'^AI_WORKFLOW_SMOKE_PROGRESS test=([^ ]+) status=started$', log, re.M)
manifest = json.loads((root / '.systems/scripts/smoke/manifest.json').read_text())
assert len(ids) == len(set(ids)) == 694 and set(ids) == set(manifest['test_groups'])
assert len(re.findall(r'^AI_WORKFLOW_SMOKE_COMPLETE group=all result=pass ', log, re.M)) == 1
shutil.copy2('/tmp/lv004-source-full-current.log', project / 'implementation/lv004-source-full-failed-001.log')
shutil.copy2('/tmp/lv004-source-full-final-002.log', project / 'implementation/lv004-source-full-final-002.log')
spec = importlib.util.spec_from_file_location('assessment', project / 'implementation/record-current-assessment.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

def inputs(source, evidence):
    return [('workflow-source', p) for p in source] + [('owning-project-evidence', p) for p in evidence]

plan = 'planning/phase-2-project-plan.md'
q1 = 'quality/phase-5-lv-core-001-verdict-integrity-quality.md'
q2 = 'quality/phase-5-lv-obs-002-baseline-quality.md'
q3s = 'quality/recovery-phase-3-lv-val-003-scoped-selection-spec-qa.md'
q3q = 'quality/phase-5-lv-val-003-scoped-selection-quality.md'
q4s = 'quality/recovery-phase-3-lv-test-004-smoke-partition-spec-qa.md'
partition = ['.systems/scripts/check-validator-smoke-tests', '.systems/scripts/smoke/common.sh',
             '.systems/scripts/smoke/manifest.json'] + [f'.systems/scripts/smoke/{g}.sh' for g in manifest['groups']]
proof = ['implementation/lv004-current-source-audit.json', 'implementation/lv004-adversarial-source-final-results.json',
         'implementation/lv004-equivalence-retest/equivalence-results.json',
         'implementation/lv004-protected-mutations/results.json', 'implementation/lv004-source-full-final-002.log']

e1 = '''- New semantic regression assessment after reviewing the full LV004 thirteen-path diff, not a hash-only renewal.
- Original negative-outcome wrapper bodies are retained in pure common.sh. Exact status and cause diagnostics, reserved exits, typed current QA reader and source-bound verdict rejection remain intact.
- All 674 frozen reference IDs and 21 original transactions are byte-bound and executed; 552 negative diagnostics match the reference. Two real protected-validator mutations are rejected by both implementations.
- Final current source full executes 694 unique IDs (20 supplemental), no lost reference cases; public/group marker separation and early-zero rejection reviewed. The previous full failure from the missing system-skills reference is retained, fixed through a live test/command binding, and retested.
- Manual trace: unsafe/incomplete QA -> original typed reader rejection -> owned negative helper status/cause -> failure completion, never a historical PASS. Linux CI is not run locally.
'''
qa.record(project / q1, 'lv001-regression-lv004-2026-09-30', 'implementation-quality',
          'ai-workflow-lean-validation-v1:LV-CORE-001-verdict-integrity',
          inputs(partition + ['.systems/scripts/lib/qa-evidence.py', '.systems/scripts/check-status-consistency',
                              '.systems/scripts/check-qa-evidence'], [plan, 'specs/phase-3-lv-core-001-verdict-integrity-specification.md', *proof]),
          qa.body(e1, [('Exact negative outcome and diagnostic', 'Unchanged helper contracts and 552 matched diagnostics.'),
                       ('Current QA evidence and failure integrity', 'Typed reader unchanged; frozen quality cases and protected mutations reject bad outputs.'),
                       ('Original coverage retained', '674 reference IDs plus 20 separately owned supplemental cases; final source full.')]))

e2 = '''- Fresh review of parent/group timing producers against unchanged nine-column timing helper and comparison reader. All-mode child records retain smoke-all; exactly one suite wall is owned by the public dispatcher.
- Reference/candidate all and reverse-order standalone runs have actual raw timing and marker evidence. Named groups are subsets, not full evidence, and duplicate child/group walls cannot masquerade as the public wall.
- Current twelve lifecycle probes cover child failure, early zero, real interruption/timeout, metadata identity tracking, detached observed descendants and cleanup failure. No broad process-name kill or unrelated process changes.
- Original LV002 three-run baseline is immutable and source-specific (660 IDs), not relabelled as a current 694-ID baseline or speed proof. Full-suite speed improvement is not asserted.
- Manual success trace: parent start -> per-test monotonic child -> namespaced group completion -> exact executed ledger -> one suite wall. Failure trace: original child code -> identity-bound cleanup -> original failure/interrupt marker; a timing/cleanup error cannot produce success.
'''
qa.record(project / q2, 'lv002-regression-lv004-2026-09-30', 'implementation-quality',
          'ai-workflow-lean-validation-v1:LV-OBS-002-baseline',
          inputs(partition + ['.systems/scripts/validate-workflow', '.systems/scripts/lib/validation-timing.py',
                              '.systems/scripts/report-validation-comparison', '.systems/scripts/check-validation-observability'],
                 [plan, 'specs/phase-3-lv-obs-002-baseline-specification.md', q1, *proof]),
          qa.body(e2, [('Timing schema and original result preserved', 'Nine columns, child profile and single parent wall inspected against actual equivalence timings.'),
                       ('Safe failure and cleanup lifecycle', 'Twelve final-source synthetic probes and manual process-tree traces.'),
                       ('Source-specific historical baseline', 'Three original baseline records unchanged; no claimed current speed comparison.')]))

scope = ['.systems/scripts/validate-workflow', '.systems/scripts/lib/validation-scope.py',
         '.systems/scripts/lib/validation-checks.json', '.systems/scripts/check-status-consistency',
         '.systems/scripts/check-qa-evidence', '.systems/scripts/check-distillation-state', '.systems/scripts/check-naming',
         '.systems/ai/core/validation-profiles.md', '.systems/ai/core/validation-routing.md', '.systems/ai/core/contract-compliance.md']
e3s = '''- Fresh whole LV003 spec review against its unchanged scope engine/registry/runtime consumers and the LV004 dispatcher/group output. Explicit dependency closure, normalized root identities, complete Git inventory, bounded consumers and final eligibility are not altered.
- Shared-source workflow changes remain full-required; splitting smoke groups does not authorize an incomplete manifest, stale finish, subset-full claim or wider runtime scan.
- Current LV001/LV002 regression recorded separately; source-bound quality inputs are updated only after semantic review. No CI/updater/scope consumer outside the LV004 ceiling is edited.
- This verdict applies to specification coherence only; implementation regression is recorded separately.
'''
qa.record(project / q3s, 'lv003-spec-regression-lv004-2026-09-30', 'spec-qa',
          'ai-workflow-lean-validation-v1:LV-VAL-003-scoped-selection',
          inputs(scope + partition, [plan, 'specs/phase-3-lv-val-003-scoped-selection-specification.md', q1, q2, *proof]),
          qa.body(e3s, [], artifact=True))

e3q = '''- Genuine LV003 direct-path regression review: scope CLI/registry and four bounded runtime consumers unchanged; literal original core scope probe region and setup preserved. Actual current all runs execute all eleven scope scenarios and reject the protected status-consumer mutation.
- Reviewed canonical snapshot -> explicit dependency closure/dedup -> root/check normalization -> dispatch -> finish freshness -> execution/coverage/eligibility separation. Invalid input or changed finish cannot become full evidence.
- Current LV001/LV002 and LV003 Spec QA are separate current assessments; previous runs and LV002 baselines remain immutable. New smoke routing is a source change requiring full, not a runtime-only exception.
- No lost original case, new inferred selector/cache, widened roots, modified CI/updater or outside approved source ceiling. Linux CI remains unrun; full local source evidence is bounded.
'''
qa.record(project / q3q, 'lv003-quality-regression-lv004-2026-09-30', 'implementation-quality',
          'ai-workflow-lean-validation-v1:LV-VAL-003-scoped-selection',
          inputs(scope + partition, [plan, 'specs/phase-3-lv-val-003-scoped-selection-specification.md', q1, q2, q3s, *proof]),
          qa.body(e3q, [('V3-01..03 explicit dependency graph and dedup', 'All original dedup/projects/graph probes and source review.'),
                        ('V3-04..08 Git/freshness/ownership boundaries', 'All git/freshness/ownership/paths/finish/consumer probes unchanged and executed.'),
                        ('V3-09..10 source/full/checkpoint eligibility', 'Checkpoint/source/finish scenarios and unchanged full/CI/updater contract reviewed.')]))

e4s = '''- Fresh full LV004 specification and V4-01..09 review against all thirteen current paths, whole preserved transactions, exact field-level ownership and updated direct consumers.
- All 674 old cases, 110 semantically classified outside-wrapper points, 34 nested Python assertion/failure lines and 21 frozen regions have one explicit ownership mapping. Pure helper import has no setup effects.
- Actual reference/candidate all, repeated reverse standalone groups, 552 cause/status matches and two protected mutations prove preserved-reference behavior; final 694-case source full and twelve latest process/integrity probes cover subsequent supplemental/mapping/supervisor fixes.
- Missing system-skills literal discovered by the prior full is fixed as a live source/command binding, not a decorative comment or bypass. Re-read all 32 inventoried direct consumers including full runner structural checks; no consumer edit outside ceiling needed.
- Fallback is explicit and remains available from the frozen parent source; no speedup, CI execution, task completion or owner-final closure is inferred from counts.
'''
qa.record(project / q4s, 'lv004-spec-current-source-2026-09-30', 'spec-qa',
          'ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition',
          inputs(partition + ['.systems/scripts/check-validation-observability', '.systems/scripts/check-validation-completion',
                              '.systems/ai/core/commands.md', '.systems/ai/core/validation-observability.md', 'README.md'],
                 [plan, 'specs/phase-3-lv-test-004-smoke-partition-specification.md', q1, q2, q3q, *proof]),
          qa.body(e4s, [], artifact=True))
audit = json.loads((project / 'implementation/lv004-current-source-audit.json').read_text())
(project / 'quality/phase-4-lv-test-004-smoke-partition-implementation-result.md').write_text('''# Phase 4 Implementation Result: LV004

## Metadata

- Project: ai-workflow-lean-validation-v1
- Task/package ID: LV-TEST-004-smoke-partition
- Date: 2026-09-30
- Result: implemented; formal Phase 5 remains the next gate
- Owner authority: LV-DEC-008
- Changed files: exact thirteen-path ceiling in the current source audit
- Source baseline: 03fb788 plus reviewed LV004 worktree, digest ''' + audit['source_digest'] + '''

## Implementation Slice Plan And Slice Execution Evidence

- Plan and complete transaction/lifecycle investigation: implementation/phase-4-lv-test-004-smoke-partition-implementation.md
- Slices 1-4 complete; slice 5 semantic source and prerequisite regression review completed. Actual-runtime full and formal Phase 5 remain pending.
- No CI, updater, full runner, scope engine, domain skill or outside-ceiling consumer edit.

## Definition Of Done Evidence

| Condition | Evidence |
| --- | --- |
| all 674 reference identities and assertions owned once | manifest, 21 unchanged regions, 95 assertion points / 14 failure branches / one fixture, 34 nested Python lines |
| independent setup and repeat/order | clean standalone reverse-order groups and repeated all, pure common import without side effects |
| same mutation/status/cause | 552 matched negative outcomes and two real protected-validator mutations rejected by both runners |
| lifecycle and tree cleanup | twelve latest dispatcher probes: early zero, failure, interruption, timeout, missing/drifting source and cleanup failure |
| honest full/iteration evidence | final current source full: 694 unique IDs and one public completion; group timing and subset boundary checked |
| freshness and fallback | new actual prerequisite/spec regression, original monolith preserved; no speed or final closure claim |

## Findings-First Current-Diff Review

- Reviewed: full thirteen-path diff, all 32 original consumer references, CLI/manifest/common/group setup and original backup-mutation-restore transactions.
- Intent/plan/spec/DoD: aligned with V4-01..09; no source expansion, lost reference ID, hidden subset-full claim or changed formal authority.
- Producer-consumer: manifest exact command/group/line/digest contracts, executed ledger, public/group markers, timing parent, current QA reader and full/CI/updater consumers checked.
- Adversarial: missing/duplicate mappings and keys, symlinks, changed frozen assertion, early-zero leader, real signals/failures, retained identity cleanup, policy safe/direct/compound clauses and missing sources checked.
- Resolved findings: transaction boundaries, process metadata padding/zombie handling, ordinary-failure descendants, live assertion mappings, safe-prohibition false positive and full-run system-skills integration reference.
- Current unresolved findings/blockers: none identified after whole-diff re-review; final runtime verification still required before formal quality acceptance.
- Scripts are supporting-only. The initial source full failure remains implementation/lv004-source-full-failed-001.log; the corrected full is implementation/lv004-source-full-final-002.log.
- Skipped checks: Linux CI not run; actual runtime full is next, no final PASS asserted here.
- Residual risk: supervisor guards observed own processes, not arbitrary malicious detached jobs; no measured full speed improvement.

## Next Route

Actual-runtime full after this semantic review, then evidence-backed high-risk phase-5-quality under LV-DEC-008. No capture, commit, push or final-owner-yes from this result alone.
''')
print('Current LV001/LV002/LV003 regression and LV004 Spec QA/Phase4 result recorded after actual semantic review; prior runs preserved.')
