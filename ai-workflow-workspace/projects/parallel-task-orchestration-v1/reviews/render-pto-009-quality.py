"""Render the actual completed PTO009 reviewer assessment; no automatic verdict."""
import importlib.util
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parents[1]
R = P.parents[2]
spec = importlib.util.spec_from_file_location('producer', R / '.systems/scripts/lib/quality-record.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
receipt = q.eff.verify_source(Path('/tmp/pto-009-full-source-002.json'),
                              Path('/private/tmp/pto-004-receipt-key'))
review = (P / 'reviews/pto-009-quality-review.md').read_text()
if 'Final full002: completed and accepted' not in review:
    raise ValueError('required final source evidence and completed review missing')
base = json.loads((P / 'reviews/pto-008-formal-quality-input.json').read_text())
sections = base['sections']
sections['Evidence'] = (
    '- Fresh full002 result=pass, complete registered checks and all five smoke groups; '
    '/tmp/pto-009-full-source-002.json.\n'
    '- 26 actual synthetic binding/CLI tests,54 runtime,89 orchestration regressions; '
    'actual frozen old Python/shell/capture consumers reject V3/schema3.\n'
    '- Parent and independent post-fix semantic/adversarial current-diff review: '
    'reviews/pto-009-quality-review.md. All seven AC reviewed before scripts.\n'
    '- High-risk authority PTO-D08/D09; no source commit/push/final-owner-yes. '
    'Earlier incomplete full001 is historical, not final evidence.')
ac = (
    'Future planning/6/7/8 matrix, no-commit wins, ignored/no-op no Git',
    'Owned branch and single coordinator; no destructive/publication inference',
    'Independently complete typed snapshot union, modes, dependencies and wire versions',
    'Actual first commit/tree/index/live, hook/mode/history/input mutation regressions',
    'Acyclic immutable proof, V3 current-only, forged/FAIL/history/identity rejection',
    'Actual QA/capture/scoped/coordinator/parent/checkpoint conformance; fresh artifacts separate',
    'Adversarial source/CLI/regressions, current independent review and full002; pending impact blocks publication')
sections['Definition Of Done Validation'] = (
    '| DoD Item | Result | Evidence |\n| --- | --- | --- |\n' +
    '\n'.join(f'| PTO-009-AC{i} | PASS | {e} |' for i, e in enumerate(ac, 1)))
sections['Intent / Plan / Spec Compliance'] = sections['Intent / Plan / Spec Compliance'].replace(
    'exact PTO-008 implementation/specification, D08/D09 approvals and current semantic review; no freshness-policy change.',
    'exact PTO-009 implementation/specification, D08/D09 and current review; future policy is non-retroactive and V3 is opt-in.')
sections['Review Completeness Gate'] = (
    '- Status: complete\n- Reviewed baseline:8a0eeef, entire approved current source and exact009 scope\n'
    '- Closure freshness: current\n- Post-fix full re-review: completed\n'
    '- Policy-boundary adversarial matrix: completed\n- Producer-consumer field audit: completed\n'
    '- Required-field mapping: complete\n- Cross-contract consistency: aligned\n'
    '- Risk/work mode compatibility: aligned\n'
    '- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes\n'
    '- Negative-space / adversarial review: completed\n- Automated evidence role: supporting-only\n'
    '- Instruction refresh: performed-full\n- Instruction baseline: current\n'
    '- Producers/consumers reviewed: actual V3 producer, QA, capture, scoped, coordinator, parent and checkpoint\n'
    '- Evidence: reviews/pto-009-quality-review.md; all seven AC, actual manual success/failure traces, independent final review and full002.')
sections['Adaptive Data / Integration Verification Matrix'] = (
    '- Applicability: required\n'
    '| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |\n'
    '| --- | --- | --- | --- | --- | --- | --- |\n'
    '| Snapshot to exact source commit | equivalent current inputs | supporting binding | HEAD-only or partial stage | reject drift | positive/negative Git fixtures | inventory to actual tree/index/live |\n'
    '| Replacement/graft/hook mutation | actual raw history and bytes | no false reuse | substituted commits | reject | actual replacement/graft/hook tests | no-replace to raw parents to full path checks |\n'
    '| Additional QA input mutates during read | stale input | ineligible | roles-only closing proof | reject all-input recheck | runtime mutation test | initial QA to receipt to complete re-assess |\n'
    '| V3/schema3 or ordinary V2 | exact version-specific qualification | computed current evidence | downgrade or V2 CLI exit0 | reject missing proof | actual CLI/old readers/current consumers | producer to discriminator to canonical gate |\n'
    '| Unsupported target or runtime commit chain | fresh QA required | no reuse | broad workspace/ancestry allowlist | reject | coverage/commit negatives | coverage contract to conservative fallback |')
sections['Findings'] = (
    '- Blockers: none\n- Unresolved findings: none\n'
    '- Resolved: replacement/graft history, closing input drift, CLI proof omission, wire fallback, modes, runtime-prefix authority and producer/consumer gaps.\n'
    '- Residual risk: finite synthetic coverage; target-product receipt and tracked runtime-chain reuse unsupported; native unverified; no real source publication test.')
sections['Owner Decision Checkpoint'] = (
    '- Interaction mode: queued\n- Decision state: clear\n'
    '- Material decisions: PTO-D08/D09 covers this high-risk gate; added-scope counterpart pending only before publication/handoff\n'
    '- Questions asked: none\n- Auto-resolved reversible decisions: serial local verification\n'
    '- Optional owner refinements: none\n'
    '- Decision artifacts: decisions/pto-008-009-implementation-approval.md; decisions/pto-capability-scope-extension.md\n'
    '- Next route: phase-6-distillation')
sections['Optional Knowledge Capture'] = (
    '- Capture recommended: yes\n- Target: project-memory\n'
    '- Reason: preserve immutable source-binding and truthful publication boundaries\n'
    '- Owner decision required: no\n- Owner decision: defer-to-distillation\n'
    '- Privacy/scope check: pass\n- Suggested entry title: Commit identity is not evidence equivalence\n'
    '- Suggested entry summary: Independently verify complete actual inputs and keep fresh artifact closure separate.')
source_paths = re.findall(r'^- (\.systems/[^\n]+|AGENTS.md|HUMANS.md|README.md)$',
                         (P / 'specs/phase-3-pto-git-009-phase-commits-specification.md').read_text(), re.M)
if len(source_paths) != 47 or len(set(source_paths)) != 47:
    raise ValueError('approved write set changed')
owned = ['specs/phase-3-pto-git-009-phase-commits-specification.md',
         'implementation/phase-4-pto-git-009-phase-commits.md',
         'reviews/pto-009-quality-review.md', 'reviews/pto-009-prewrite-readiness.md',
         'reviews/pto-009-frozen-reader-audit.py', 'reviews/pto-008-prerequisite-regression.md',
         'decisions/pto-008-009-implementation-approval.md', 'decisions/pto-capability-scope-extension.md',
         'architecture/pre-final-capture-and-commit-delta.md', 'planning/phase-2-project-plan.md',
         'quality/phase-3-pto-git-009-phase-commits-spec-qa.md',
         'quality/phase-5-pto-cap-008-capture-parity-quality.md']
record = dict(schema=1, kind='implementation-quality', task='PTO-GIT-009-phase-commits',
              run_id='pto-009-formal-quality-001', verdict='PASS', date='2026-10-04',
              inputs=[{'root': 'workflow-source', 'path': s} for s in source_paths] +
                     [{'root': 'owning-project-evidence', 'path': s} for s in owned], sections=sections)
output, body = q.render(record, R, P.parents[1], P.name)
q.publish(output, body)
print(output)
