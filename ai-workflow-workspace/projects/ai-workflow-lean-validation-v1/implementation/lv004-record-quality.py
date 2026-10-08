"""Record the evidence-backed LV004 gate only after actual full completion."""
import importlib.util
import json
from pathlib import Path
import re
import shutil

root = Path.cwd()
project = root / 'ai-workflow-workspace/projects/ai-workflow-lean-validation-v1'
text = Path('/tmp/lv004-actual-runtime-full-001.log').read_text()
markers = re.findall(r'^AI_WORKFLOW_VALIDATE_COMPLETE .*$', text, re.M)
assert len(markers) == 1 and 'result=pass exit_code=0 ' in markers[0], markers
manifest = json.loads((root / '.systems/scripts/smoke/manifest.json').read_text())
ids = re.findall(r'^AI_WORKFLOW_SMOKE_PROGRESS test=([^ ]+) status=started$', text, re.M)
assert len(ids) == len(set(ids)) == 694 and set(ids) == set(manifest['test_groups'])
shutil.copy2('/tmp/lv004-actual-runtime-full-001.log', project / 'implementation/lv004-actual-runtime-full-001.log')
spec = importlib.util.spec_from_file_location('assessment', project / 'implementation/record-current-assessment.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
audit = json.loads((project / 'implementation/lv004-current-source-audit.json').read_text())
evidence = '''- Formal high-risk quality is authorized by LV-DEC-008; it does not authorize push, scope expansion or final-owner-yes.
- Findings-first full-current-diff review covers thirteen approved paths, V4-01..09, all original 32 source consumer references, phase/risk/permissions, typed negative wrappers, transaction boundaries, manifest schema/line ownership and timing/lifecycle contracts.
- Semantic QA was performed before source and actual-runtime full scripts; scripts support rather than create this verdict. Actual current full now completes with 694 unique IDs and one public completion. The first source full failure is retained and the system-skills integration corrected via a live source/command binding.
- Whole reference/candidate execution plus repeated reverse standalone groups preserve 674 old identities, 21 byte-bound transactions, 110 classified outside points and 34 nested Python assertion/failure lines. All 552 negative status/cause outcomes match; two actual protected mutations are rejected by both reference and partition.
- Twelve final dispatcher adversarial cases test missing/drifting sources, duplicate fields, wrong live index, early-zero execution, direct failure, actual interruption/timeout, retained observed own-process identity cleanup and cleanup failure. No live owned orphan remained in measured paths. Twenty supplemental cases test manifest mapping and policy safe/direct/compound/missing-source boundaries.
- Fresh LV001/LV002/LV003 regression and LV004 Spec QA are separately recorded from current source review; earlier reports and the three original LV002 baselines are preserved, not recycled as a current speed proof.
- Manual success trace: manifest and live command binding -> isolated group/setup -> actual typed assertion -> private ID ledger -> exact owned union -> namespaced group marker -> one parent wall/public completion.
- Manual failure trace: source/line tampering rejects before launch; early-zero ledger gap fails; observed own descendant retained after leader failure -> identity checked -> cleanup -> original code/result. Timing or cleanup error cannot produce successful completion.
- No known in-scope bug, unresolved material finding, missing required evidence or source expansion remains. Linux CI is unrun; no full-suite performance improvement or arbitrary detached-process containment is asserted.
'''
dod = [
    ('V4-01 complete unique ownership', '674 reference + 20 supplemental IDs; exact command/group/line/digest/region mapping and missing/duplicate mutation rejection.'),
    ('V4-02 real outside assertion preservation', '21 exact raw regions, 95 assertion points / 14 failure branches / one fixture; removal of a post-call assertion rejected.'),
    ('V4-03..04 independent repeat/order', 'Fresh standalone groups in reverse order and repeated all runs; pure common import without filesystem effects.'),
    ('V4-05 failure, timeout, interrupt and cleanup', 'Twelve latest actual fault probes; original statuses and one parent marker retained; no live own orphan in measured paths.'),
    ('V4-06 protected real mutations', 'Both original and split reject unconditional-zero status and observability validators with the same case/cause.'),
    ('V4-07 all coverage and typed outcome equivalence', 'All 674 original identities executed; 552 negative diagnostic/status matches; actual final full 694 unique cases.'),
    ('V4-08 invalid CLI/manifest cannot succeed', 'Enum parser and exact live manifest rejection; missing fields/source, duplicate JSON keys, altered owner/region/source tested.'),
    ('V4-09 fallback and honest evidence', 'Immutable parent runner retained; completed reference equivalence permits split, not speed/quality inference; full/CI/updater untouched.'),
]
body = qa.body(evidence, dod)
body = body.replace('runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.',
                    'manifest/group/common producers, exact executed ledger, public/group lifecycle, full/CI/updater structural consumers, timing reader and current QA inputs.')
start = body.index('| explicit checks and input records |')
end = body.index('\n\n', start)
body = body[:start] + '''| 674 reference / 20 supplemental cases and source-bound manifest | exactly one owner/command/region per ID, pure common setup | standalone subset or complete all | omitted/moved assertion, duplicate/missing execution, false full | nonzero before launch or final coverage failure | current full and manifest corruption cases | manifest to live command to ledger to parent completion |
| negative helper and mutated protected validator | exact expected status and cause | same rejection as original runner | reserved or unrelated exit accepted as intended failure | original failure propagated | 552 matched diagnostics and two old/new mutations | mutated status consumer to typed negative outcome |
| observed own process tree and timing sink | retained PID/start identity plus one wall | truthful failure/interrupt/timeout, no live own orphan in tested paths | successful completion on incomplete execution or cleanup failure | preserved nonzero; cleanup failure explicitly fails | twelve final-source fault probes | failing leader to retained descendant to cleanup to marker/wall |''' + body[end:]
sources = [('workflow-source', path) for path in audit['paths_sha256']]
sources += [('workflow-source', path) for path in ['.systems/scripts/validate-workflow', '.systems/scripts/update-from-upstream',
            '.github/workflows/ai-workflow-validate.yml', '.systems/scripts/lib/validation-timing.py']]
sources += [('owning-project-evidence', path) for path in [
    'planning/phase-2-project-plan.md', 'specs/phase-3-lv-test-004-smoke-partition-specification.md',
    'quality/recovery-phase-3-lv-test-004-smoke-partition-spec-qa.md',
    'quality/phase-4-lv-test-004-smoke-partition-implementation-result.md',
    'quality/phase-5-lv-core-001-verdict-integrity-quality.md', 'quality/phase-5-lv-obs-002-baseline-quality.md',
    'quality/phase-5-lv-val-003-scoped-selection-quality.md', 'implementation/lv004-current-source-audit.json',
    'implementation/lv004-adversarial-source-final-results.json', 'implementation/lv004-equivalence-retest/equivalence-results.json',
    'implementation/lv004-protected-mutations/results.json', 'implementation/lv004-source-full-final-002.log',
    'implementation/lv004-actual-runtime-full-001.log']]
qa.record(project / 'quality/phase-5-lv-test-004-smoke-partition-quality.md', 'lv004-quality-2026-09-30',
          'implementation-quality', 'ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition', sources, body)
print(markers[0])
print('LV004 evidence-backed high-risk Phase5 recorded; Phase6/commit follow separate capture compliance.')
