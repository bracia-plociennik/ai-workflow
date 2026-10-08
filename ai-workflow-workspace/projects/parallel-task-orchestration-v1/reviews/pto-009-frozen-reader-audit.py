"""Compare actual baseline readers to synthetic V3 without changing source repos."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
def load(path):
    spec = importlib.util.spec_from_file_location('frozen_audit_' + path.stem, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

tests = load(ROOT / '.systems/scripts/tests/phase-commit-policy.py')
fixture = tests.BindingTests()
fixture.setUp()
results = {}
try:
    report, body = fixture.make_quality()
    frozen = Path(fixture.tmp.name) / 'old-workflow'
    scripts = frozen / '.systems/scripts'
    lib = scripts / 'lib'
    lib.mkdir(parents=True)
    names = ['lib/qa-evidence.py', 'lib/validation-scope.py', 'lib/capture-state.py',
             'check-qa-evidence', 'resolve-workflow-env']
    for name in names:
        out = scripts / name
        out.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show',
                                                '8a0eeef:.systems/scripts/' + name]))
    (frozen / 'AGENTS.md').write_text('Synthetic frozen reader audit only')
    old_qa = load(lib / 'qa-evidence.py')
    try:
        old_qa.assess(report, frozen, fixture.workspace, 'synthetic', fixture.repo, require_pass=True)
        raise RuntimeError('frozen QA accepted V3')
    except ValueError as error:
        if 'missing V2 contract marker' not in str(error): raise
        results['frozen-python-qa'] = 'rejects distinct V3 wire'
    capture = fixture.owner / 'capture-state/work-001.md'
    capture.parent.mkdir()
    capture.write_text('# State\n- Capture schema: 3\n- Work ID: WORK-001\n'
                       '- Work mode: full-project\n- Project/repo scope: synthetic\n'
                       '- Source artifact: implementation/synthetic.md\n'
                       '- Quality artifact: ' + report.relative_to(fixture.owner).as_posix() + '\n'
                       '- State: ready\n- Distillation artifact: none\n- Last reminder: none\n'
                       '- Owner disposition: capture-now\n- Privacy/scope check: pass\n'
                       '- Residual risk: synthetic only\n- is_distilled derived value: false\n')
    old_capture = load(lib / 'capture-state.py')
    inventory = old_capture.inventory(fixture.workspace, frozen, fixture.repo, 'synthetic')
    if not inventory['invalid'] or inventory['records']:
        raise RuntimeError('frozen capture accepted schema3')
    results['frozen-capture'] = 'rejects schema3; no verified-current record'
    env = {**os.environ, 'AI_WORKFLOW_MODE': 'official',
           'AI_WORKFLOW_WORKSPACE_HOME': str(fixture.workspace)}
    run = subprocess.run(['bash', str(scripts / 'check-qa-evidence'), '--project', 'synthetic'],
                         cwd=frozen, env=env, text=True, capture_output=True)
    if run.returncode != 1 or 'missing V1 QA marker' not in run.stdout:
        raise RuntimeError('unexpected frozen shell outcome: ' + run.stdout + run.stderr)
    results['frozen-shell-gate'] = 'rejects V3 through legacy fallback'
    print(json.dumps({'baseline': '8a0eeef', 'synthetic_only': True, 'results': results,
                      'result': 'verified', 'authority': 'none'}, sort_keys=True))
finally:
    fixture.doCleanups()
