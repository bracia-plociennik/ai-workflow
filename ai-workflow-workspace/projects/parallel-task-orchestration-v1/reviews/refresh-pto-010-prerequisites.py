"""Publish reviewed regression assessments in dependency order, preserve old runs."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
R = P.parents[2]
s = importlib.util.spec_from_file_location('producer', R / '.systems/scripts/lib/quality-record.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
review = 'reviews/pto-010-regression-review.md'
paths = sorted((P / 'quality').glob('phase-*-qa.md')) + sorted((P / 'quality').glob('phase-5-*-quality.md'))
records = {}
for path in paths:
    old = path.read_text()
    meta, sections = q.qa.read_current(old.splitlines())
    records[path] = (old, meta, sections)
done = set()
while len(done) < len(records):
    progress = False
    for path, (old, meta, sections) in records.items():
        if path in done:
            continue
        rows = q.qa.input_rows(sections['Input Artifacts'])
        dependencies = {P / relative for kind, relative, _ in rows if kind == 'owning-project-evidence'} & records.keys()
        if not dependencies <= done:
            continue
        supplied = {key: '\n'.join(lines).strip() for key, lines in sections.items() if key != 'Input Artifacts'}
        supplied['Evidence'] = ('Fresh actual PTO010 regression assessment: ' + review +
                                '.49 original AC unchanged; existing89 orchestration/54runtime/26binding plus19 adapter tests passed. '
                                'Prior full source evidence is historical; expanded full gate is pending. No native support or publication claimed.')
        gate = supplied['Review Completeness Gate']
        gate = re.sub(r'^- Evidence:.*$', '- Evidence: ' + review + '; current original behaviors and adapter design reviewed.', gate, flags=re.M)
        supplied['Review Completeness Gate'] = gate
        inputs = [{'root': kind, 'path': relative} for kind, relative, _ in rows]
        inputs.append({'root': 'owning-project-evidence', 'path': review})
        record = dict(schema=1, kind=meta['Artifact kind'], task=meta['Project/task identity'].split(':', 1)[1] if ':' in meta['Project/task identity'] else None,
                      run_id='pto-010-regression-' + str(len(done)+1).zfill(3), date='2026-10-04', verdict='PASS', inputs=inputs, sections=supplied)
        out, body = q.render(record, R, P.parents[1], P.name)
        a, b = q.qa.current_section(old.splitlines())
        body += '\n## Historical Runs\n\n' + '\n'.join(old.splitlines()[a+1:b]) + '\n'
        if '## Historical Runs' in old:
            body += old.split('## Historical Runs', 1)[1]
        q.qa.assess(out, R, P.parents[1], P.name, document=body)
        out.write_text(body)
        done.add(path)
        progress = True
        print(path.name)
    if not progress:
        raise ValueError('quality dependency cycle')
old = P / 'quality/phase-8-final-check.md'
history = P / 'quality/recovery-phase-8-pre-010-final-check.md'
assert old.is_file() and not history.exists()
raw = old.read_bytes()
history.write_bytes(raw)
assert history.read_bytes() == raw
registry = P / 'quality-assessments.json'
value = json.loads(registry.read_text())
decision = 'decisions/pto-010-prior-final-history.md'
value['assessments'].append(dict(path=str(history.relative_to(P)), sha256=hashlib.sha256(raw).hexdigest(),
                               state='superseded', assessed_head='8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1',
                               decision=decision, decision_sha256=hashlib.sha256((P / decision).read_bytes()).hexdigest()))
registry.write_text(json.dumps(value, indent=2) + '\n')
old.unlink()
print('Prior nine-task final check preserved byte-for-byte; not current.')
