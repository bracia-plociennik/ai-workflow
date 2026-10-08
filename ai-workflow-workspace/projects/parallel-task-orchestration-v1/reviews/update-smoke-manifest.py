"""Mechanical supplemental smoke ID/hash synchronization; frozen coverage unchanged."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
path = root / '.systems/scripts/smoke/manifest.json'
record = json.loads(path.read_text())
identifier = 'parallel-compatibility-offline-regressions'
command = 'run_must_pass "' + identifier + '" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case compatibility'
assert command in (path.parent / 'core.sh').read_text()
if identifier not in record['supplemental_test_ids']:
    record['supplemental_test_ids'].append(identifier)
    record['test_groups'][identifier] = 'core'
    row = dict(record['tests'][-1])
    row.update(id=identifier, group='core', region_id='supplemental-core', helper='run_must_pass',
               command_contract=command, setup_id='synthetic-compatibility-temp-roots',
               cleanup_id='owned-temporary-directory-cleanup', mutation_id='capability-and-schema-negative-cases',
               expected_outcome='compatibility suite succeeds including rejection cases; no native dispatch')
    record['tests'].append(row)
else:
    assert sum(row['id'] == identifier for row in record['tests']) == 1
    assert next(row for row in record['tests'] if row['id'] == identifier)['command_contract'] == command
for name in record['files_sha256']:
    record['files_sha256'][name] = hashlib.sha256((path.parent / name).read_bytes()).hexdigest()
path.write_text(json.dumps(record, indent=2) + '\n')
print('Supplemental compatibility ID registered; frozen reference inventory unchanged.')
