"""Render the supplied completed PTO010 review; never infer QA from scripts alone."""
import importlib.util
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
R = P.parents[2]
s = importlib.util.spec_from_file_location('producer', R / '.systems/scripts/lib/quality-record.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
q.eff.verify_source(Path('/private/tmp/pto-010-full-source-003.json'), Path('/private/tmp/pto-004-receipt-key'))
review_path = 'reviews/pto-010-final-quality-review.md'
review = (P / review_path).read_text()
assert 'Independent post-fix review: complete; unresolved findings: none' in review
assert 'Actual full source003: pass' in review
base = json.loads((P / 'reviews/pto-008-formal-quality-input.json').read_text())
sections = dict(base['sections'])
evidence = ['Closed supported versions, no authority, CLI unknown/missing inputs reject',
            'Actual Git HEAD, separate peer manifest digest, bounded source/result closing hashes and modes',
            'One complete worker/reviewer budget, exact observations, missing/duplicate/retired/contradictory actors reject',
            'Nine peer states mapped without transitions; retained failed evidence current; accepted needs local receipt',
            'Native/worktree/rebase unsupported and parent cross-task gates preserved',
            'CLI bounded duplicate-safe JSON, privacy path rejection, sanitized errors and no effects',
            '22 adapter tests,89 orchestration,54 runtime,26 binding and758 smoke IDs preserved',
            'Parent and independent post-fix current-diff review, all8AC, actual full003 and current formal prerequisites']
sections['Definition Of Done Validation'] = '| DoD Item | Result | Evidence |\n| --- | --- | --- |\n' + '\n'.join(
    '| PTO-010-AC' + str(i) + ' | PASS | ' + detail + ' |' for i, detail in enumerate(evidence, 1))
sections['Evidence'] = 'Fresh actual review: ' + review_path + '; full source003 authenticated receipt, exit0,705seconds.22 adapter tests and original89/54/26 regressions. No native calls, counterpart writes, commit, push or final-owner-yes.'
sections['Findings'] = '- Blockers: none\n- Unresolved findings: none\n- Resolved findings: privacy paths, result/source closing drift, missing mapped inputs, aliases, retained failed evidence, Git environment and peer semantics.\n- Residual risk: finite synthetic tests; supplied occupancy is not native proof; no operational interop claim.'
sections['Intent / Plan / Spec Compliance'] = sections['Intent / Plan / Spec Compliance'].split('- Evidence:')[0] + '- Evidence: accepted PTO-D10 and exact PTO010 specification; eight observable AC and approved source set only.'
sections['Review Completeness Gate'] = ('- Status: complete\n- Reviewed baseline:8a0eeef, approved current PTO001..010 source\n'
    '- Closure freshness: current\n- Post-fix full re-review: completed\n- Policy-boundary adversarial matrix: completed\n'
    '- Producer-consumer field audit: completed\n- Required-field mapping: complete\n- Cross-contract consistency: aligned\n'
    '- Risk/work mode compatibility: aligned\n- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes\n'
    '- Negative-space / adversarial review: completed\n- Automated evidence role: supporting-only\n'
    '- Instruction refresh: performed-full\n- Instruction baseline: current\n'
    '- Producers/consumers reviewed: peer contract1 run, closed mapping, actual target source/results, actor budget and local parent gates\n- Evidence: ' + review_path)
sections['Adaptive Data / Integration Verification Matrix'] = '- Applicability: required\n' + review.split('## Adaptive Data / Integration Verification Matrix\n', 1)[1].split('\n## ', 1)[0].strip()
sections['Owner Decision Checkpoint'] = '- Interaction mode: queued\n- Decision state: clear\n- Material decisions: PTO-D10\n- Questions asked: none\n- Auto-resolved reversible decisions: existing branch and serial inspector verification\n- Optional owner refinements: native adapter later\n- Decision artifacts: decisions/pto-010-compatibility-approval.md\n- Next route: phase-6-distillation'
sections['Optional Knowledge Capture'] = '- Capture recommended: yes\n- Target: project-memory\n- Reason: preserve compatibility/authority boundaries\n- Owner decision required: no\n- Owner decision: defer-to-distillation\n- Privacy/scope check: pass\n- Suggested entry title: Inspection is not execution\n- Suggested entry summary: peer acceptance and supplied occupancy remain supporting-only.'
source = ['.systems/ai/core/parallel-compatibility.md', '.systems/ai/templates/orchestration/compatibility.template.json',
          '.systems/scripts/lib/parallel-compatibility.py', '.systems/scripts/inspect-parallel-compatibility',
          '.systems/scripts/tests/parallel-compatibility.py', '.systems/ai/core/parallel-task-orchestration.md',
          '.systems/ai/core/commands.md', '.systems/scripts/check-parallel-task-orchestration',
          '.systems/scripts/check-required-artifacts', '.systems/scripts/smoke/core.sh', '.systems/scripts/smoke/manifest.json',
          '.systems/scripts/check-validator-smoke-tests', '.systems/ai/core/changelog.md',
          '.systems/scripts/lib/coordinator-status.py', '.systems/scripts/lib/parallel-orchestration.py']
owned = ['specs/phase-3-pto-bridge-010-compatibility-adaptation-specification.md',
         'implementation/phase-4-pto-bridge-010-compatibility-adaptation.md',
         'decisions/pto-010-compatibility-approval.md', review_path,
         'quality/phase-3-pto-bridge-010-compatibility-adaptation-spec-qa.md']
record = dict(schema=1, kind='implementation-quality', task='PTO-BRIDGE-010-compatibility-adaptation',
              run_id='pto-010-formal-quality-001', verdict='PASS', date='2026-10-04',
              inputs=[{'root':'workflow-source','path':x} for x in source] + [{'root':'owning-project-evidence','path':x} for x in owned], sections=sections)
out, body = q.render(record, R, P.parents[1], P.name)
q.publish(out, body)
print(out.name)
