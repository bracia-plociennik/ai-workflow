#!/usr/bin/env python3
"""Offline compatibility regressions; fixture Git and data are entirely synthetic."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('compat', ROOT / '.systems/scripts/lib/parallel-compatibility.py')
c = importlib.util.module_from_spec(s)
s.loader.exec_module(c)


class Compatibility(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pto-compat-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        (self.repo / 'source.txt').write_text('synthetic source\n')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'source.txt'], check=True)
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Synthetic', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
        checksum = hashlib.sha256((self.repo / 'source.txt').read_bytes()).hexdigest()
        baseline = {'commit': c.head(self.repo), 'source_digest': hashlib.sha256(('source.txt=' + checksum + '\n').encode()).hexdigest()}
        self.unit = {'id': 'unit-a', 'goal': 'Read synthetic source', 'dod': 'Source unchanged', 'dependencies': [],
                     'mode': 'read-only', 'system': 'ai-system', 'write_paths': [], 'resources': [], 'worktree': None,
                     'status': 'pending', 'attempt_id': None, 'agent_id': None, 'termination_confirmed': False, 'result': None}
        self.run = {'contract': 1, 'run_id': 'run-a', 'coordinator_id': 'coordinator-a', 'approval_ref': 'synthetic-only',
                    'baseline': baseline, 'source_manifest': [{'path': 'source.txt', 'sha256': checksum}],
                    'retired_attempt_ids': [], 'retired_agent_ids': [], 'runtime_capacity': 2, 'dispatch_count': 2,
                    'checkpoint_open': True, 'workflow_parallel_supported': False, 'units': [copy.deepcopy(self.unit)]}
        self.mapping = {'schema': 1, 'peer_contract': 1, 'workflow_protocol': 1, 'run_id': 'run-a',
                        'coordinator_id': 'coordinator-a', 'project': 'synthetic-project',
                        'unit_mapping': [{'unit_id': 'unit-a', 'task_id': 'TASK-001', 'slice_id': 'slice-a', 'read_paths': ['source.txt']}],
                        'capacity': {'known': True, 'complete': True, 'total': 2, 'actors': []}}
        self.run_path, self.mapping_path = self.root / 'run.json', self.root / 'mapping.json'

    def inspect(self):
        self.run_path.write_text(json.dumps(self.run))
        self.mapping_path.write_text(json.dumps(self.mapping))
        return c.inspect(ROOT, self.repo, self.run_path, self.mapping_path)

    def rejects(self):
        with self.assertRaises((ValueError, OSError, TypeError, KeyError)):
            self.inspect()

    def start(self, state='running', terminated=False):
        unit = self.run['units'][0]
        unit.update(status=state, attempt_id='attempt-a', agent_id='agent-a', termination_confirmed=terminated)
        self.mapping['capacity']['actors'] = [{'agent_id': 'agent-a', 'role': 'worker', 'system': 'ai-system',
                                             'unit_id': 'unit-a', 'termination_confirmed': terminated}]
        if state in {'submitted', 'accepted'}:
            unit['result'] = {'baseline': copy.deepcopy(self.run['baseline']), 'attempt_id': 'attempt-a',
                              'evidence': copy.deepcopy(self.run['source_manifest']), 'test_summary': 'synthetic test', 'findings': []}
            if state == 'accepted':
                unit['result'].update(verified_by='coordinator-a', verified_checks=['intent', 'diff', 'tests', 'privacy'])

    def test_positive_no_authority(self):
        result = self.inspect()
        self.assertEqual(result['result'], 'compatible-inspection')
        self.assertFalse(result['execution_authorized'])
        self.assertFalse(result['operational_support'])
        self.assertIn('logical-rebase', result['unsupported'])

    def test_all_states(self):
        for state in c.DISPOSITIONS:
            with self.subTest(state=state):
                self.run['units'][0] = copy.deepcopy(self.unit)
                self.mapping['capacity']['actors'] = []
                if state in {'pending', 'ready', 'blocked'}:
                    self.run['units'][0]['status'] = state
                else:
                    self.start(state, state == 'cancelled')
                result = self.inspect()
                self.assertEqual(result['units'][0]['disposition'], c.DISPOSITIONS[state])
                self.assertEqual(result['occupied'], 0 if state in {'pending', 'ready', 'blocked', 'cancelled'} else 1)

    def test_closed_versions_and_fields(self):
        for obj, field in ((self.run, 'contract'), (self.mapping, 'schema'), (self.mapping, 'peer_contract'), (self.mapping, 'workflow_protocol')):
            for value in (True, 2, '1'):
                with self.subTest(field=field, value=value):
                    obj[field] = value
                    self.rejects()
            obj[field] = 1
        for obj in (self.run, self.mapping, self.run['units'][0], self.mapping['capacity']):
            obj['unknown'] = True
            self.rejects()
            del obj['unknown']

    def test_duplicate_json_and_sanitized_failure(self):
        self.inspect()
        self.run_path.write_text('{"secret":"do-not-print","contract":1,"contract":1}')
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('do-not-print', result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)['execution_authorized'])

    def cli(self):
        return subprocess.run(['bash', str(ROOT / '.systems/scripts/inspect-parallel-compatibility'), '--workflow', str(ROOT),
                               '--repo', str(self.repo), '--run', str(self.run_path), '--mapping', str(self.mapping_path)],
                              capture_output=True, text=True, timeout=15)

    def test_missing_special_and_oversized_inputs(self):
        self.inspect()
        self.run_path.unlink()
        self.assertEqual(self.cli().returncode, 1)
        os.mkfifo(self.run_path)
        self.assertEqual(self.cli().returncode, 1)
        self.run_path.unlink()
        self.run_path.write_text(' ' * (1048576 + 1))
        self.assertEqual(self.cli().returncode, 1)

    def test_capacity_full_pool(self):
        self.start('submitted')
        actor = {'agent_id': 'reviewer-a', 'role': 'reviewer', 'system': 'ai-workflow', 'unit_id': None, 'termination_confirmed': False}
        self.mapping['capacity']['actors'].append(actor)
        self.assertEqual(self.inspect()['free_observed'], 0)
        self.mapping['capacity']['actors'].append(dict(actor, agent_id='external-worker', role='worker'))
        self.rejects()

    def test_capacity_missing_contradictory_retired_duplicate(self):
        self.start()
        original = copy.deepcopy(self.mapping['capacity'])
        cases = [dict(original, known=False), dict(original, complete=False), dict(original, total=3),
                 dict(original, actors=[]), dict(original, total=True), dict(original, actors=original['actors'] * 2)]
        for capacity in cases:
            self.mapping['capacity'] = capacity
            self.rejects()
        self.mapping['capacity'] = original
        original['actors'][0]['termination_confirmed'] = True
        self.rejects()
        original['actors'][0]['termination_confirmed'] = False
        self.run['retired_agent_ids'] = ['agent-a']
        self.rejects()
        self.run['retired_agent_ids'] = []
        self.run['retired_attempt_ids'] = ['attempt-a']
        self.rejects()

    def test_identity_and_mapping(self):
        for field in ('run_id', 'coordinator_id'):
            old = self.mapping[field]
            self.mapping[field] = 'different-id'
            self.rejects()
            self.mapping[field] = old
        self.mapping['unit_mapping'][0]['unit_id'] = 'different-unit'
        self.rejects()

    def test_stale_result_and_acceptance(self):
        self.start('accepted')
        result = self.run['units'][0]['result']
        for field, value in (('attempt_id', 'old-attempt'), ('baseline', dict(self.run['baseline'], commit='0'*40)),
                             ('verified_by', 'other-coordinator'), ('verified_checks', ['tests']), ('findings', ['unresolved'])):
            old = result[field]
            result[field] = value
            self.rejects()
            result[field] = old
        self.run['units'][0]['termination_confirmed'] = True
        self.rejects()

    def test_head_content_and_unsafe_paths(self):
        self.run['baseline']['commit'] = '0' * 40
        self.rejects()
        self.run['baseline']['commit'] = c.head(self.repo)
        (self.repo / 'source.txt').write_text('changed\n')
        self.rejects()
        for path in ('../secret', '/tmp/secret', '.env', '.git/config', 'ai-workflow-workspace/private', 'a//b', 'a/./b', 'a\\b'):
            self.run['source_manifest'][0]['path'] = path
            self.rejects()

    def test_alias_and_duplicate_paths(self):
        self.run['source_manifest'].append(copy.deepcopy(self.run['source_manifest'][0]))
        self.rejects()
        self.run['source_manifest'].pop()
        self.run['source_manifest'].append(dict(self.run['source_manifest'][0], path='SOURCE.txt'))
        self.rejects()

    def test_symlink_and_hardlink(self):
        original = self.repo / 'source.txt'
        backup = self.repo / 'backup.txt'
        original.rename(backup)
        original.symlink_to(backup)
        self.rejects()
        original.unlink()
        os.link(backup, original)
        self.rejects()

    def test_graph_and_overlap(self):
        self.run['units'][0]['dependencies'] = ['unit-a']
        self.rejects()
        self.run['units'][0]['dependencies'] = ['missing']
        self.rejects()
        self.run['units'][0]['dependencies'] = []
        self.start()
        other = copy.deepcopy(self.run['units'][0])
        other.update(id='unit-b', agent_id='agent-b', attempt_id='attempt-b')
        self.run['units'].append(other)
        self.mapping['unit_mapping'].append(dict(self.mapping['unit_mapping'][0], unit_id='unit-b'))
        self.mapping['capacity']['actors'].append(dict(self.mapping['capacity']['actors'][0], agent_id='agent-b', unit_id='unit-b'))
        self.run['units'][0]['resources'] = ['shared-db']
        other['resources'] = ['shared-db']
        self.rejects()

    def test_readonly_and_unsupported_worktree(self):
        self.run['units'][0]['write_paths'] = ['source.txt']
        self.rejects()
        self.run['units'][0].update(mode='implementation', worktree=str(self.repo))
        result = self.inspect()
        self.assertIn('git-worktree-executor', result['unsupported'])
        self.assertFalse(result['operational_support'])
        self.run['workflow_parallel_supported'] = True
        self.rejects()

    def test_cli_no_side_effects(self):
        self.inspect()
        def snapshot():
            return {str(p.relative_to(self.root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode)
                    for p in self.root.rglob('*') if p.is_file()}
        before = snapshot()
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, snapshot())

    def test_retained_failed_and_cancelled_evidence(self):
        for state, terminated in (('failed', False), ('cancel-requested', False), ('cancelled', True)):
            self.start('submitted', terminated)
            self.run['units'][0]['status'] = state
            result = self.inspect()
            self.assertEqual(result['occupied'], 0 if terminated else 1)
            self.run['units'][0]['result']['attempt_id'] = 'stale-attempt'
            self.rejects()

    def test_result_recheck_and_mode_drift(self):
        self.start('submitted')
        evidence = self.repo / 'evidence.txt'
        evidence.write_text('synthetic result')
        self.run['units'][0]['result']['evidence'] = [{'path': evidence.name, 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        original = c.manifest
        for mutation in ('content', 'mode'):
            evidence.write_text('synthetic result')
            evidence.chmod(0o644)
            calls = 0
            def mutate(entries, root, observations=None):
                nonlocal calls
                result = original(entries, root, observations)
                if entries[0]['path'] == evidence.name:
                    calls += 1
                    if calls == 1:
                        if mutation == 'content':
                            evidence.write_text('changed result')
                        else:
                            evidence.chmod(0o600)
                return result
            with patch.object(c, 'manifest', side_effect=mutate):
                self.rejects()

    def test_missing_and_aliased_access(self):
        for paths in (['missing.txt'], ['source.txt', 'SOURCE.txt']):
            self.mapping['unit_mapping'][0]['read_paths'] = paths
            self.rejects()
        self.mapping['unit_mapping'][0]['read_paths'] = ['source.txt']
        self.run['units'][0].update(mode='implementation', worktree=str(self.repo), write_paths=['new/A', 'new/a'])
        self.rejects()

    def test_sensitive_names_reject_before_read(self):
        for name in ('id_rsa', 'cert.pem', 'api.key', 'private/source.txt', '.ssh/config', 'credentials/x'):
            self.run['source_manifest'] = [{'path': name, 'sha256': '0'*64}]
            with patch.object(c, 'read_file', wraps=c.read_file) as reader:
                self.rejects()
                self.assertFalse(any(str(call.args[0]).endswith(name) for call in reader.call_args_list))

    def test_git_environment_cannot_substitute_head(self):
        foreign = self.root / 'foreign'
        foreign.mkdir()
        subprocess.run(['git', 'init', '-q', str(foreign)], check=True)
        subprocess.run(['git', '-C', str(foreign), '-c', 'user.name=Synthetic', '-c', 'user.email=fixture@example.invalid',
                        'commit', '--allow-empty', '-qm', 'foreign'], check=True)
        expected = c.head(self.repo)
        with patch.dict(os.environ, {'GIT_DIR': str(foreign / '.git'), 'GIT_WORK_TREE': str(self.repo),
                                    'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.bare', 'GIT_CONFIG_VALUE_0': 'true'}):
            self.assertEqual(c.head(self.repo), expected)
            self.assertEqual(self.inspect()['result'], 'compatible-inspection')

    def test_closing_evidence_cannot_invalidate_source_or_head(self):
        self.start('submitted')
        evidence = self.repo / 'evidence.txt'
        evidence.write_text('synthetic result')
        self.run['units'][0]['result']['evidence'] = [{'path': evidence.name, 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        original = c.manifest
        for mutation in ('source', 'head'):
            calls = 0
            (self.repo / 'source.txt').write_text('synthetic source\n')
            self.run['baseline']['commit'] = c.head(self.repo)
            self.run['units'][0]['result']['baseline'] = copy.deepcopy(self.run['baseline'])
            def mutate(entries, root, observations=None):
                nonlocal calls
                result = original(entries, root, observations)
                if entries[0]['path'] == evidence.name:
                    calls += 1
                    if calls == 2:
                        if mutation == 'source':
                            (self.repo / 'source.txt').write_text('closing drift')
                        else:
                            subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Synthetic', '-c', 'user.email=fixture@example.invalid',
                                            'commit', '--allow-empty', '-qm', 'new baseline'], check=True)
                return result
            with patch.object(c, 'manifest', side_effect=mutate):
                self.rejects()

    def test_peer_lowercase_and_linear_fallback(self):
        self.run['units'][0]['id'] = self.mapping['unit_mapping'][0]['unit_id'] = 'Unit-a'
        self.rejects()
        self.run['units'][0]['id'] = self.mapping['unit_mapping'][0]['unit_id'] = 'unit-a'
        self.start()
        other = copy.deepcopy(self.run['units'][0])
        other.update(id='unit-b', agent_id='agent-b', attempt_id='attempt-b', system='ai-workflow')
        self.run['units'].append(other)
        self.mapping['unit_mapping'].append(dict(self.mapping['unit_mapping'][0], unit_id='unit-b'))
        self.mapping['capacity']['actors'].append(dict(self.mapping['capacity']['actors'][0], agent_id='agent-b', unit_id='unit-b', system='ai-workflow'))
        self.rejects()


if __name__ == '__main__':
    unittest.main()
