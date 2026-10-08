"""Mechanical manifest refresh for added execution-modes supplemental tests."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
folder = root / '.systems/scripts/smoke'
path = folder / 'manifest.json'
data = json.loads(path.read_text())
commands = {
    'execution-modes-valid': 'run_must_pass "execution-modes-valid" bash .systems/scripts/check-execution-modes',
    'execution-modes-behavioral': 'run_must_pass "execution-modes-behavioral" python3 .systems/scripts/tests/execution-modes.py',
    'execution-modes-qualified-independent-policy': 'run_must_pass "execution-modes-qualified-independent-policy" bash .systems/scripts/check-owner-decision-checkpoints',
    'execution-modes-blocked-unit-policy': 'run_must_fail "execution-modes-blocked-unit-policy" --expect-literal \'Unsafe owner decision checkpoint wording\' bash .systems/scripts/check-owner-decision-checkpoints',
    'execution-modes-safe-prohibition': 'run_must_pass "execution-modes-safe-prohibition" bash .systems/scripts/check-execution-modes',
    'execution-modes-false-completion': 'run_must_fail "execution-modes-false-completion" --expect-literal \'Unsafe execution mode completion wording\' bash .systems/scripts/check-execution-modes',
    'execution-modes-missing-contract': 'run_must_fail "execution-modes-missing-contract" --expect-literal \'Execution modes contract missing\' bash .systems/scripts/check-execution-modes',
    'execution-modes-missing-producer-field': 'run_must_fail "execution-modes-missing-producer-field" --expect-literal \'Execution modes producer field missing\' bash .systems/scripts/check-execution-modes',
}
for join in ('direct', 'but', 'however', 'period', 'colon', 'semicolon', 'unless', 'yet'):
    commands['execution-modes-boundary-' + join] = 'run_must_fail "execution-modes-boundary-$em_join" --expect-literal \'Unsafe execution mode authority wording\' bash .systems/scripts/check-execution-modes'
for identifier, command in commands.items():
    if identifier in data['test_groups']:
        continue
    data['supplemental_test_ids'].append(identifier)
    data['test_groups'][identifier] = 'core'
    data['tests'].append(dict(id=identifier, group='core', helper=command.split()[0],
        region_id='supplemental-core', command_contract=command,
        setup_id='execution-mode-source-copy', cleanup_id='restore-execution-mode-source',
        mutation_id=identifier, expected_outcome='success' if command.startswith('run_must_pass') else 'reject intended boundary with diagnostic'))
for name in data['files_sha256']:
    data['files_sha256'][name] = hashlib.sha256((folder / name).read_bytes()).hexdigest()
path.write_text(json.dumps(data, indent=2) + '\n')
