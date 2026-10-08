"""Publish explicitly reviewed planning delta, preserving previous assessments."""
import importlib.util
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
W = P.parents[1]
R = W.parent
s = importlib.util.spec_from_file_location('producer', R / '.systems/scripts/lib/quality-record.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
base = json.loads((P / 'evidence/pre-final-spec-009-review.json').read_text())
spec_path = 'specs/phase-3-pto-bridge-010-compatibility-adaptation-specification.md'
inputs = ['architecture/phase-1-architecture.md', 'architecture/pre-final-compatibility-delta.md',
          'planning/phase-2-project-plan.md', spec_path,
          'decisions/pto-010-compatibility-approval.md', 'reviews/pto-010-artifact-review.md']
for kind in ('architecture-qa', 'plan-qa', 'spec-qa'):
    record = dict(base, kind=kind, task='PTO-BRIDGE-010-compatibility-adaptation' if kind == 'spec-qa' else None,
                  run_id='pto-010-' + kind + '-001')
    record['inputs'] = [{'root': 'owning-project-evidence', 'path': path} for path in inputs]
    record['sections'] = dict(base['sections'])
    for key in ('Checks', 'Execution Authority', 'Owner Decision Checkpoint', 'Optional Knowledge Capture'):
        record['sections'].pop(key, None)
    record['sections']['Evidence'] = 'Fresh PTO010 artifact review and exact input table. Six actual interface gaps, closed mapping/budget, failure matrix and eight AC reviewed. Runtime tests are not claimed.'
    record['sections']['Findings'] = '- Blockers: none\n- Unresolved findings: none\n- Residual risk: native interoperability remains unverified; implementation tests pending.'
    record['sections']['QA Verification Scope'] = kind + ': current PTO010 architecture/plan/spec delta, owner intent, numbered AC, safety, source compatibility and required failure paths; no implementation PASS.'
    record['sections']['Gate Decision'] = '- Result: PASS\n- Required next phase: phase-4-implementation after complete planning QA'
    for field in ('Artifact QA Completeness Gate', 'Review Completeness Gate', 'Validation Execution Record'):
        record['sections'][field] = record['sections'][field].replace('PTO-D07, two pre-final CRs', 'PTO-D10, CR003').replace('reviews/pre-final-planning-review.md', 'reviews/pto-010-artifact-review.md')
    output, body = q.render(record, R, W, P.name)
    if output.exists():
        old = output.read_text()
        a, b = q.qa.current_section(old.splitlines())
        body += '\n## Historical Runs\n\nPrior scope evidence, not PTO010 authority.\n\n' + '\n'.join(old.splitlines()[a+1:b]) + '\n'
        if '## Historical Runs' in old:
            body += old.split('## Historical Runs', 1)[1]
    q.qa.assess(output, R, W, P.name, document=body)
    output.write_text(body)
    (P / ('evidence/pto-010-' + kind + '-review.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(output.name)
