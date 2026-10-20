#!/usr/bin/env python3
"""Canonical inherited source context stays data with an external active runtime."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


class NamingContext(unittest.TestCase):
    def check(self, relative, frozen=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'; root.mkdir()
            scripts = root / '.systems/scripts'; scripts.mkdir(parents=True)
            for name in ('check-naming', 'resolve-workflow-env', 'durable_runtime.py'):
                shutil.copy2(ROOT / '.systems/scripts' / name, scripts / name)
            (root / 'AGENTS.md').write_text('# Synthetic official repo')
            file = root / relative; file.parent.mkdir(parents=True); file.write_text('# Synthetic source')
            if frozen:
                (root / 'ai-workflow-workspace/projects/import/evals/frozen/freeze.md').write_text('# Synthetic accepted freeze')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            workspace = Path(tmp) / 'private-runtime'; workspace.mkdir()
            env = dict(os.environ, AI_WORKFLOW_MODE='official', AI_WORKFLOW_WORKSPACE_HOME=str(workspace))
            return subprocess.run([str(scripts / 'check-naming')], cwd=root, env=env, capture_output=True, text=True)

    def test_canonical_source_imports_remain_exempt_with_external_runtime(self):
        for path in ('ai-workflow-workspace/projects/import/context/Original_Notes.md',
                     'ai-workflow-workspace/repo/context/Original_Notes.md',
                     'ai-workflow-workspace/repo/legacy/Original_Notes.md'):
            with self.subTest(path=path):
                result = self.check(path)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_artifacts_still_require_kebab_case(self):
        result = self.check('ai-workflow-workspace/projects/import/New_Artifact.md')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('New_Artifact.md', result.stdout)

    def test_frozen_eval_owner_is_independent_of_active_runtime(self):
        path = 'ai-workflow-workspace/projects/import/evals/frozen/fixture/Original_Input.md'
        self.assertEqual(self.check(path, frozen=True).returncode, 0)
        self.assertNotEqual(self.check(path).returncode, 0)


if __name__ == '__main__':
    unittest.main()
