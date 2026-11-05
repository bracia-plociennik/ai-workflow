"""Regression checks for shared allocation and conservative recovery."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import storage_capacity as capacity


class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.snapshot = dict(device=1, total=100 * capacity.GIB,
                             available=12 * capacity.GIB, inodes=10000)

    def test_byte_floor_and_foreign_filesystem(self):
        other = dict(device=2, bytes=capacity.GIB, inodes=100)
        self.assertTrue(capacity.assess(self.snapshot, [other], 2 * capacity.GIB, 0)['allowed'])
        self.assertFalse(capacity.assess(self.snapshot, [], 3 * capacity.GIB, 0)['allowed'])

    def test_unknown_estimate_and_inode_exhaustion(self):
        for size in (None, True, -1):
            with self.assertRaises(ValueError):
                capacity.assess(self.snapshot, [], size, 0)
        self.assertFalse(capacity.assess(self.snapshot, [], 0, 9000)['allowed'])

    def test_concurrent_reservations_do_not_oversubscribe(self):
        def allocate(index):
            try:
                return capacity.reserve(self.root, self.root, str(index), 2 * capacity.GIB, 100)
            except ValueError:
                return None
        with patch.object(capacity, 'filesystem', return_value=self.snapshot):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(allocate, (1, 2)))
        self.assertEqual(sum(value is not None for value in results), 1)
        self.assertEqual(len(capacity.records(self.root)), 1)

    def test_release_requires_same_owner_and_is_idempotent(self):
        with patch.object(capacity, 'filesystem', return_value=self.snapshot):
            item = capacity.reserve(self.root, self.root, 'a', 10, 1)
        with self.assertRaises(ValueError):
            capacity.release(self.root, item['id'], 'b')
        self.assertTrue(capacity.release(self.root, item['id'], 'a')['released'])
        self.assertFalse(capacity.release(self.root, item['id'], 'a')['released'])

    def test_unknown_record_blocks_allocation(self):
        (self.root / 'unknown.json').write_text('{}')
        with self.assertRaises(ValueError):
            capacity.records(self.root)

    def test_linked_registry_rejected(self):
        link = self.root / 'link'
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            capacity.reserve(link, self.root, 'a', 1, 1)

    def test_cli_preview_does_not_create_lock(self):
        script = Path(capacity.__file__)
        args = [sys.executable, '-B', str(script), 'plan', '--state-dir', str(self.root),
                '--path', str(self.root), '--bytes', '1', '--inodes', '1']
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('allowed', json.loads(result.stdout))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_run_preserves_exit_status_and_releases(self):
        # The production floor is real. Exercise lifecycle using declared synthetic
        # filesystem facts so the test is portable to small smoke/CI filesystems.
        args = ['manage-storage-capacity', 'run', '--state-dir', str(self.root),
                '--path', str(self.root), '--work-id', 'cli', '--bytes', '1',
                '--inodes', '1', '--approved', '--', sys.executable,
                '-c', 'raise SystemExit(7)']
        with patch.object(sys, 'argv', args):
            with patch.object(capacity, 'filesystem', return_value=self.snapshot):
                result = capacity.main()
        self.assertEqual(result, 7)
        self.assertEqual(capacity.records(self.root), [])



if __name__ == '__main__':
    unittest.main()
