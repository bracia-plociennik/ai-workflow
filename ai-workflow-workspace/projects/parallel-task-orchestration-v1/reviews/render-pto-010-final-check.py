"""Publish supplied technical final review, never infer owner acceptance."""
import hashlib
import importlib.util
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[1]
R = P.parents[2]
s = importlib.util.spec_from_file_location('producer', R / '.systems/scripts/lib/quality-record.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
q.eff.verify_source(Path('/private/tmp/pto-010-full-source-003.json'), Path('/private/tmp/pto-004-receipt-key'))
closure = q.eff.read_json(Path('/private/tmp/pto-010-checkpoint-artifact-003.json'))
assert closure['exit_code'] == 0 and closure['coverage'] == 'complete'
legacy = P.parents[1] / 'repo/core/legacy-qa-evidence-v1.md'
runtime = q.eff.digest({'runtime': q.eff.scope.inventory_runtime(P.parents[1], ['projects/' + P.name]),
                        'legacy': q.eff.file_hash(legacy) if legacy.exists() else None})
assert closure['runtime_fingerprint'] == runtime, 'pre-final closure no longer matches actual runtime'
review = 'reviews/pto-010-final-system-review.md'
assert 'Independent final artifact re-review: completed' in (P / review).read_text()
assert 'Unresolved findings: none' in (P / review).read_text()
history = P / 'reviews/pto-pre-010-phase-8-history.md'
assert hashlib.sha256(history.read_bytes()).hexdigest().startswith('421eb892ce3d')
_, prior = q.qa.read_current(history.read_text().splitlines())
sections = {key: '\n'.join(value).strip() for key, value in prior.items() if key != 'Input Artifacts'}
inputs = set()
qualities = sorted((P / 'quality').glob('phase-5-*-quality.md'))
assert len(qualities) == 10
for path in qualities:
    q.qa.assess(path, R, P.parents[1], P.name, require_pass=True)
    _, current = q.qa.read_current(path.read_text().splitlines())
    inputs.update((kind, relative) for kind, relative, _ in q.qa.input_rows(current['Input Artifacts']))
    inputs.add(('owning-project-evidence', str(path.relative_to(P))))
distills = sorted((P / 'distillations').glob('phase-6-*-distillation.md'))
assert len(distills) == 10 and all('- memory-in-repo-memory: true' in path.read_text() for path in distills)
for pattern in ('quality/phase-1-architecture-qa.md', 'quality/phase-2-plan-qa.md',
                'quality/phase-3-*-spec-qa.md', 'specs/phase-3-*-specification.md',
                'distillations/phase-6-*-distillation.md', 'capture-state/*.md',
                'checkpoints/*.md', 'memory/*.md', 'change-requests/*.md', 'decisions/*.md'):
    for path in sorted(P.glob(pattern)):
        inputs.add(('owning-project-evidence', str(path.relative_to(P))))
for relative in ('context.md', 'architecture/phase-1-architecture.md',
                 'architecture/pre-final-compatibility-delta.md', 'planning/phase-2-project-plan.md',
                 'status.md', 'tasks.md', 'memory.md', 'change-requests.md', 'quality-assessments.json',
                 'quality/recovery-phase-8-final-check.md', 'reviews/pto-pre-010-phase-8-history.md', review):
    inputs.add(('owning-project-evidence', relative))
sections['Evidence'] = ('- Actual current parent and independent final review: ' + review + '.\n'
    '- Ten current formal task Quality records,57AC,accepted Phase6,completed capture and final checkpoint.\n'
    '- Full source003 passed with44 registered checks,758 smoke IDs and five groups; authenticated receipt in temporary storage.\n'
    '- Final owned artifact closure follows the final report/status writes; an earlier fingerprint cannot cover new bytes.\n'
    '- Seven-task registered recovery and nine-task raw review history retained unchanged; neither is current approval.')
sections['Review Completeness Gate'] = sections['Review Completeness Gate'].replace('PTO001..009', 'PTO001..010')
sections['Review Completeness Gate'] = re.sub(r'^- Evidence:.*$', '- Evidence: ' + review,
                                             sections['Review Completeness Gate'], flags=re.M)
sections['Scope Under Final Check'] = ('- Plan artifact: planning/phase-2-project-plan.md\n'
    '- Completed tasks/packages: PTO001..010,57AC within accepted protocol-only release and D10 adapter scope\n'
    '- Deferred tasks/packages: native operational verification; approved deferred/unverified, not a completed test\n'
    '- Out-of-scope: scheduler,executor,model speedup,target/AI System source changes and Git publication')
sections['Completion Review'] = ('| Area | Result | Evidence |\n| --- | --- | --- |\n'
    '| Owner intent/architecture/plan/spec/57AC | PASS | current artifact QA, D06/D08/D09/D10 and actual final review |\n'
    '| Ten implementation Quality records | PASS | actual current formal Phase5, immutable historical runs |\n'
    '| Phase6 and capture | PASS | ten accepted distillations, completed states and derived true |\n'
    '| Checkpoint and memory sync | PASS | checkpoints/phase-7-checkpoint-2026-10-04-pto-010.md |\n'
    '| Source/runtime freshness | PASS | authenticated full003 and fresh owned artifact checks |\n'
    '| History | PASS | seven-task recovery and nine-task history byte-preserving |\n'
    '| Privacy and shared impact | PASS | one updated privacy-safe handoff, counterpart impact yes |\n'
    '| Pre-final CR001/002/003 | PASS | technically resolved, no imported final approval |\n'
    '| Final owner approval | awaiting | explicit final-owner-yes remains absent |')
sections['Findings'] = ('- Blockers: none\n- Unresolved findings: none\n- Critical errors: none\n'
    '- System warnings: none in approved technical scope\n'
    '- Residual risk: finite offline evidence; native isolation/capacity and deployed interoperability remain unverified. '
    'Caller-supplied observations and green scripts grant no authority. No speedup or publication claim.')
sections['Owner Approval'] = ('- Technical final check result: PASS\n- Owner approval required: yes\n'
    '- Owner decision: awaiting\n- Owner comments captured as change request: CR001/002/003 resolved technically')
sections['Change Request Review'] = ('| Change request | Timing | Status | Blocks final-owner-yes? | Route |\n'
    '| --- | --- | --- | --- | --- |\n'
    '| PTO-CR-001-capture-parity | pre-final-approval | done | no | technical closure |\n'
    '| PTO-CR-002-phase-commits | pre-final-approval | done | no | technical closure |\n'
    '| PTO-CR-003-compatibility-adaptation | pre-final-approval | done | no | read-only adapter accepted technically |')
sections['Final Gate'] = ('- Can close active plan: awaiting-owner\n- Required next phase: owner approval\n'
    '- Blocking reason: none for technical scope; final owner acceptance still required\n'
    '- Commit/push/final-owner-yes: not authorized')
sections['Owner Decision Checkpoint'] = ('- Interaction mode: queued\n- Decision state: awaiting-owner\n'
    '- Material decisions: final-owner-yes\n- Questions asked: none\n- Auto-resolved reversible decisions: history-safe storage\n'
    '- Optional owner refinements: separately verified native adapter\n- Decision artifacts: decisions/pto-010-compatibility-approval.md\n'
    '- Next route: owner-final-approval, no automatic publication')
record = dict(schema=1, kind='final-check', task=None, run_id='pto-ten-task-final-check-001',
              date='2026-10-04', verdict='PASS',
              inputs=[{'root': kind, 'path': relative} for kind, relative in sorted(inputs)], sections=sections)
out, body = q.render(record, R, P.parents[1], P.name)
body += '\n## Historical Runs\n\n' + '\n'.join(history.read_text().splitlines()[q.qa.current_section(history.read_text().splitlines())[0]+1:q.qa.current_section(history.read_text().splitlines())[1]]) + '\n'
if '## Historical Runs' in history.read_text():
    body += history.read_text().split('## Historical Runs', 1)[1]
q.qa.assess(out, R, P.parents[1], P.name, document=body, require_pass=True)
q.publish(out, body)
print(out.name)
