"""Synthetic behavior for bounded reference repairs, including history protection."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('artifact_maintenance', Path(__file__).parents[1] / 'lib/dreaming-maintenance.py')
maintenance = importlib.util.module_from_spec(spec); spec.loader.exec_module(maintenance)


class ArtifactMaintenance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.project = self.root / 'projects/example'
        (self.project / 'specs').mkdir(parents=True)
        (self.project / 'specs/current.md').write_text('An existing specification.')
        self.tasks = self.project / 'tasks.md'
        self.old = 'AI_WORKFLOW_WORKSPACE_HOME/projects/example/specs/missing.md'
        self.new = 'AI_WORKFLOW_WORKSPACE_HOME/projects/example/specs/current.md'
        self.tasks.write_text('| spec | ' + self.old + ' |\n')
        self.request = {'file': 'projects/example/tasks.md', 'sha256': maintenance.fingerprint(self.tasks),
                        'old': self.old, 'new': self.new, 'target': 'projects/example/specs/current.md'}

    def test_audit_exposes_real_gap_without_creating_documents(self):
        result = maintenance.audit(self.root, 'projects/example')
        self.assertEqual(len(result['findings']), 1)
        self.assertFalse(result['historical_quality_revalidated'])
        self.assertFalse((self.project / 'specs/missing.md').exists())

    def test_grounded_repair_is_idempotent(self):
        self.assertEqual(maintenance.repair(self.root, self.request)['status'], 'executed')
        self.assertEqual(maintenance.repair(self.root, self.request)['status'], 'no-change')
        self.assertIn(self.new, self.tasks.read_text())

    def test_changed_file_blocks(self):
        self.tasks.write_text(self.tasks.read_text() + 'owner edit\n')
        with self.assertRaisesRegex(ValueError, 'artifact-changed'):
            maintenance.repair(self.root, self.request)

    def test_historical_quality_and_status_cannot_be_restamped(self):
        for relative in ['projects/example/quality/tasks.md', 'projects/example/status.md']:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                maintenance.repair(self.root, {**self.request, 'file': relative})

    def test_existing_reference_cannot_be_reinterpreted(self):
        (self.project / 'specs/missing.md').write_text('Historical spec')
        with self.assertRaisesRegex(ValueError, 'existing-reference-not-repairable'):
            maintenance.repair(self.root, self.request)

    def test_outside_and_linked_targets_are_blocked(self):
        for relative in ['../foreign.md', '/tmp/foreign.md']:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                maintenance.owned(self.root, relative)
        (self.project / 'linked').symlink_to(self.project / 'specs', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'linked-path'):
            maintenance.owned(self.root, 'projects/example/linked/current.md')

    def test_unambiguous_same_identity_move_is_repaired_without_manifest_rewrite(self):
        moved = self.project / 'specs/moved/missing.md'; moved.parent.mkdir(); moved.write_text('Existing same identity spec')
        result = maintenance.reconcile(self.root, 'projects/example')
        self.assertEqual(result['status'], 'executed')
        self.assertIn('specs/moved/missing.md', self.tasks.read_text())
        self.assertFalse(result['semantic_quality_pass_implied'])
        self.assertEqual(maintenance.reconcile(self.root, 'projects/example')['status'], 'no-change')

    def test_ambiguous_moves_remain_unrepaired(self):
        before = self.tasks.read_bytes()
        for sub in ['one', 'two']:
            path = self.project / ('specs/' + sub + '/missing.md'); path.parent.mkdir(); path.write_text('Candidate')
        result = maintenance.reconcile(self.root, 'projects/example')
        self.assertEqual(result['status'], 'no-change'); self.assertEqual(self.tasks.read_bytes(), before)
        self.assertEqual(result['repairs'][0]['reason'], 'missing-or-ambiguous-current-target')


if __name__ == '__main__': unittest.main()
