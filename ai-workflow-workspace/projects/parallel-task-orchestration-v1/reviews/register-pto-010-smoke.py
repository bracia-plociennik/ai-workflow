"""Mechanical manifest update preserving every existing ID and frozen region."""
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[4]
path = R / '.systems/scripts/smoke/manifest.json'
record = json.loads(path.read_text())
old = [item['id'] for item in record['tests']]
identifier = 'parallel-cross-system-offline-regressions'
command = 'run_must_pass "' + identifier + '" python3 .systems/scripts/tests/parallel-compatibility.py'
assert command in (path.parent / 'core.sh').read_text()
assert identifier not in old
record['supplemental_test_ids'].append(identifier)
record['test_groups'][identifier] = 'core'
row = dict(record['tests'][-1])
row.update(id=identifier, group='core', region_id='supplemental-core', helper='run_must_pass',
           command_contract=command, setup_id='synthetic-cross-system-temp-roots',
           cleanup_id='owned-temporary-directory-cleanup', mutation_id='peer-envelope-boundary-cases',
           expected_outcome='offline positive and adversarial cases; no dispatch or writes')
record['tests'].append(row)
for name in record['files_sha256']:
    record['files_sha256'][name] = hashlib.sha256((path.parent / name).read_bytes()).hexdigest()
assert [item['id'] for item in record['tests'] if item['id'] != identifier] == old
assert len(set(item['id'] for item in record['tests'])) == len(record['tests'])
path.write_text(json.dumps(record, indent=2) + '\n')
print('Preserved', len(old), 'IDs; added one. Frozen region hashes unchanged.')
