#!/usr/bin/env python3
"""Read-only audit regression fixtures. Never evict a real candidate."""
from datetime import datetime, timezone
import copy
import importlib.machinery
import importlib.util
import json
import os
import shlex
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
loader = importlib.machinery.SourceFileLoader('storage_audit', str(SCRIPTS / 'audit-storage'))
spec = importlib.util.spec_from_loader(loader.name, loader)
audit = importlib.util.module_from_spec(spec)
loader.exec_module(audit)


class StorageAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='storage-audit-')
        self.root = Path(self.temp.name)
        self.data = self.root / 'candidate'
        self.data.mkdir()
        (self.data / 'output.bin').write_bytes(b'synthetic' * 1024)
        self.october = datetime(2026, 10, 15, tzinfo=timezone.utc).timestamp()
        self.november = datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp()
        self.freeze()

    def tearDown(self):
        self.temp.cleanup()

    def freeze(self):
        for path in [*self.data.rglob('*'), self.data]:
            os.utime(path, (self.october, self.october), follow_symlinks=False)

    def report(self, paths=None, **kwargs):
        return audit.audit(paths or [self.data], self.root, **kwargs)

    def row(self, **kwargs):
        return self.report(**kwargs)['candidates'][0]

    def test_never_claims_deletion_eligibility(self):
        result = self.report()
        self.assertTrue(result['candidates'][0]['complete'])
        self.assertGreater(result['totals']['priority_allocated_bytes'], 0)
        self.assertEqual(result['totals']['safe_reclaimable_bytes'], 0)
        self.assertFalse(result['execution_authorized'])

    def test_metadata_only_and_no_file_or_directory_changes(self):
        def snapshot():
            return {str(p): (p.lstat().st_mtime_ns, p.lstat().st_ctime_ns,
                             p.read_bytes() if p.is_file() else None)
                    for p in [self.data, *self.data.rglob('*')]}
        before = snapshot()
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('content read')):
            self.assertTrue(self.row()['complete'])
        self.assertEqual(before, snapshot())

    def test_parent_child_duplicate_totals_are_not_added_twice(self):
        child = self.data / 'child'
        child.mkdir()
        (child / 'x').write_bytes(b'x' * 4096)
        expected = self.report()['totals']['priority_allocated_bytes']
        result = self.report([self.data, child, self.data])
        self.assertEqual(result['totals']['priority_allocated_bytes'], expected)
        self.assertEqual(sum(r['counted_in_totals'] for r in result['candidates']), 1)

    def test_new_file_in_old_directory_excludes_whole_candidate(self):
        os.utime(self.data / 'output.bin', (self.november, self.november))
        result = self.report(months=['2026-11'])
        self.assertTrue(result['candidates'][0]['excluded'])
        self.assertEqual(result['totals']['unexcluded_priority_allocated_bytes'], 0)

    def test_names_support_month_day_compact_and_underscore(self):
        for name in ['build-2026-11', 'build-2026-11-02', 'build-20261102', 'build-2026_11_02']:
            with self.subTest(name=name):
                path = self.data / name
                path.mkdir()
                self.freeze()
                self.assertTrue(self.row(months=['2026-11'])['excluded'])
                path.rmdir()
        path = self.data / 'build-20261199999'
        path.mkdir()
        self.freeze()
        self.assertFalse(self.row(months=['2026-11'])['excluded'])

    def test_month_boundary_uses_explicit_timezone(self):
        instant = datetime(2026, 10, 31, 23, 30, tzinfo=timezone.utc).timestamp()
        os.utime(self.data / 'output.bin', (instant, instant))
        self.assertFalse(self.row(months=['2026-11'], timezone='UTC')['excluded'])
        self.assertTrue(self.row(months=['2026-11'], timezone='Europe/Warsaw')['excluded'])

    def test_excluded_child_also_excludes_parent_estimate(self):
        self.assertTrue(self.row(excluded_paths=[self.data / 'child'])['excluded'])

    def test_symlink_target_and_ancestor_are_never_followed(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'unique').write_bytes(b'preserve')
        link = self.data / 'link'
        link.symlink_to(outside, target_is_directory=True)
        result = self.report()
        self.assertFalse(result['candidates'][0]['complete'])
        self.assertEqual(result['totals']['priority_allocated_bytes'], 0)
        self.assertFalse(self.row(paths=[link])['complete'])
        self.assertFalse(self.row(paths=[link / 'subdir'])['complete'])
        self.assertEqual((outside / 'unique').read_bytes(), b'preserve')

    def test_hardlinks_keep_candidate_incomplete(self):
        os.link(self.data / 'output.bin', self.data / 'other')
        self.assertFalse(self.row()['complete'])

    def test_nested_same_device_mount_is_not_traversed(self):
        child = self.data / 'mounted'
        child.mkdir()
        with patch.object(audit, 'mounts', return_value={child}):
            self.assertFalse(self.row()['complete'])

    def test_bound_and_missing_path_produce_no_aggregate_estimate(self):
        for paths, kwargs in [([self.data], {'limit': 1}), ([self.root / 'missing'], {})]:
            result = self.report(paths, **kwargs)
            self.assertFalse(result['candidates'][0]['complete'])
            self.assertEqual(result['totals']['priority_allocated_bytes'], 0)

    def test_different_device_has_zero_priority_gain(self):
        if Path('/proc').stat().st_dev == self.data.stat().st_dev:
            self.skipTest('separate proc filesystem unavailable')
        result = audit.audit([self.data], Path('/proc'))
        self.assertGreater(result['candidates'][0]['allocated_bytes'], 0)
        self.assertEqual(result['totals']['priority_allocated_bytes'], 0)

    def test_invalid_arguments_fail_closed(self):
        for kwargs in [{'months': ['2026-13']}, {'limit': 0}, {'canonical': self.root}]:
            with self.assertRaises(ValueError):
                self.report(**kwargs)

    def test_retention_report_keeps_all_overlapping_reasons(self):
        policies = [('synthetic-record', {'enabled': False, 'resources': [
            {'path': str(self.data), 'id': 'parent', 'state': 'kept', 'keep': True},
            {'path': str(self.data / 'subdir'), 'id': 'child', 'state': 'active', 'keep': False}]}, False)]
        with patch.object(audit, 'retention', return_value=(policies, [])):
            row = self.row(canonical=self.root, workspace=self.root)
        self.assertEqual(len(row['retention']), 2)
        self.assertTrue(row['retention'][0]['keep'])
        self.assertTrue(row['retention'][1]['cleanup_disabled'])

    def test_unknown_pointer_is_not_hidden(self):
        with patch.object(audit, 'retention', return_value=([], [{'reason': 'foreign or malformed pointer'}])):
            result = self.report(canonical=self.root, workspace=self.root)
        self.assertEqual(result['candidates'][0]['retention_visibility'], 'unknown')
        self.assertTrue(result['unknown_ownership_pointers'])

    def test_cli_is_read_only_json_and_reports_incomplete_with_nonzero_exit(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'audit-storage'),
                                 '--path', str(self.root / 'missing'),
                                 '--priority-filesystem', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['execution_authorized'])

    def test_direct_cli_with_retention_import_creates_no_bytecode(self):
        scripts = self.root / 'scripts'
        scripts.mkdir()
        command = scripts / 'audit-storage'
        command.write_bytes((SCRIPTS / 'audit-storage').read_bytes())
        (scripts / 'task_resource_cleanup.py').write_text(
            'def discover(canonical, workspace):\n'
            '    return {"records": [], "retained": []}\n')
        result = subprocess.run([sys.executable, str(command), '--path', str(self.data),
                                 '--priority-filesystem', str(self.root),
                                 '--canonical', str(self.root), '--workspace', str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((scripts / '__pycache__').exists())

    def aliases(self, child=False, excluded=False):
        nested = self.data / 'child'
        nested.mkdir()
        (nested / 'x').write_bytes(b'x' * 4096)
        def raw(path):
            return audit.scan(path, self.root.stat().st_dev, [], timezone.utc, [], 1000, set())
        first, second = raw(self.data), raw(nested if child else self.data)
        alias = self.root / 'separate-alias'
        second['path'] = str(alias)
        second['excluded'] = excluded
        with patch.object(audit, 'scan', side_effect=[copy.deepcopy(first), copy.deepcopy(second)]):
            result = self.report([self.data, alias])
        return first, result

    def test_same_physical_directory_alias_counted_once(self):
        first, result = self.aliases()
        self.assertEqual(result['totals']['priority_allocated_bytes'], first['allocated_bytes'])
        self.assertEqual(sum(r['counted_in_totals'] for r in result['candidates']), 1)

    def test_partial_physical_overlap_does_not_double_count(self):
        first, result = self.aliases(child=True)
        self.assertEqual(result['totals']['priority_allocated_bytes'], first['allocated_bytes'])

    def test_physical_alias_cannot_bypass_owner_exclusion(self):
        _, result = self.aliases(excluded=True)
        self.assertTrue(all(r['excluded'] for r in result['candidates']))
        self.assertEqual(result['totals']['unexcluded_priority_allocated_bytes'], 0)

    def test_directory_replacement_produces_incomplete_report(self):
        original = audit.open_directory
        count = 0
        def replacing(path):
            nonlocal count
            if path == self.data:
                count += 1
                if count == 2:
                    self.data.rename(self.root / 'old')
                    self.data.mkdir()
            return original(path)
        with patch.object(audit, 'open_directory', side_effect=replacing):
            self.assertFalse(self.row()['complete'])

    def test_deep_directory_tree_is_bounded(self):
        path = self.data
        for _ in range(130):
            path = path / 'd'
            path.mkdir()
        row = self.row()
        self.assertFalse(row['complete'])
        self.assertTrue(any('depth limit' in r for r in row['reasons']))

    def test_malformed_mount_inventory_is_rejected(self):
        with patch.object(Path, 'read_text', return_value='malformed'):
            with self.assertRaisesRegex(ValueError, 'mount inventory'):
                audit.mounts()

    def test_local_native_entrypoint_naming_is_narrow(self):
        for case, ignored, tracked, nested, expected in [
                ('local', True, False, False, 0),
                ('not-ignored', False, False, False, 1),
                ('tracked', True, True, False, 1),
                ('nested', True, False, True, 1)]:
            with self.subTest(case=case):
                root = self.root / case
                scripts = root / '.systems/scripts'
                scripts.mkdir(parents=True)
                check = scripts / 'check-naming'
                check.write_bytes((SCRIPTS / 'check-naming').read_bytes())
                check.chmod(0o755)
                (scripts / 'resolve-workflow-env').write_text(
                    'AI_WORKFLOW_HOME=' + shlex.quote(str(root)) + '\n'
                    'AI_WORKFLOW_WORKSPACE_HOME=' + shlex.quote(str(root / 'runtime')) + '\n')
                subprocess.run(['git', 'init', '-q', str(root)], check=True)
                override = root / ('nested/AGENTS.override.md' if nested else 'AGENTS.override.md')
                override.parent.mkdir(exist_ok=True)
                override.write_text('Synthetic local instruction entrypoint; no authority.\n')
                if ignored:
                    (root / '.git/info/exclude').write_text('AGENTS.override.md\n')
                if tracked:
                    subprocess.run(['git', '-C', str(root), 'add', '-f', 'AGENTS.override.md'], check=True)
                result = subprocess.run([str(check)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
