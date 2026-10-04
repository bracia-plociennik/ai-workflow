#!/usr/bin/env python3
"""Offline synthetic Git/evidence mutations; never commit the caller repository."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
LIB = ROOT / '.systems/scripts/lib'


def load(path):
    spec = importlib.util.spec_from_file_location('fixture_' + path.stem.replace('-', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='phase-commit-policy-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name).resolve() / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        git(self.repo, 'config', 'user.email', 'fixture@example.invalid')
        git(self.repo, 'config', 'user.name', 'Synthetic Fixture')
        self.lib = self.repo / '.systems/scripts/lib'
        self.lib.mkdir(parents=True)
        for name in ('qa-commit-binding', 'qa-evidence', 'quality-record', 'validation-scope',
                     'execution-efficiency', 'validation-timing', 'capture-record',
                     'capture-state', 'coordinator-status', 'parallel-orchestration'):
            shutil.copy2(LIB / (name + '.py'), self.lib / (name + '.py'))
        (self.lib / 'validation-checks.json').write_text(json.dumps({'checks': {'check-fixture': {}}}))
        (self.repo / 'AGENTS.md').write_text('Synthetic source baseline')
        (self.repo / '.gitignore').write_text('ai-workflow-workspace/\n.systems/ignored/\n__pycache__/\n*.pyc\n')
        (self.repo / '.systems/ai/capabilities').mkdir(parents=True)
        shutil.copy2(ROOT / '.systems/ai/capabilities/phase-commit-policy-v1.json',
                     self.repo / '.systems/ai/capabilities/phase-commit-policy-v1.json')
        # Synthetic adapter covers fixture sources only; no real runner claim.
        adapter = self.repo / '.systems/scripts/report-validation-comparison'
        adapter.write_text('#!/usr/bin/env python3\nimport hashlib,pathlib\nr=pathlib.Path(__file__).resolve().parents[2]\nh=hashlib.sha256()\nfor p in sorted(r.rglob("*")):\n if p.is_file() and ".git" not in p.parts and "ai-workflow-workspace" not in p.parts and "__pycache__" not in p.parts and p.suffix != ".pyc": h.update(str(p.relative_to(r)).encode()+p.read_bytes())\nprint(h.hexdigest())\n')
        adapter.chmod(0o755)
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'synthetic baseline')
        self.base = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.workspace = self.repo / 'ai-workflow-workspace'
        self.owner = self.workspace / 'projects/synthetic'
        self.evidence = []
        for role, directory in (('spec-dod', 'specs'), ('owner-approval', 'decisions'),
                                ('implementation', 'implementation'), ('review', 'reviews')):
            path = self.owner / directory / 'synthetic.md'
            path.parent.mkdir(parents=True)
            path.write_text('Synthetic accepted ' + role + ', WORK-001. No external authority.')
            self.evidence.append({'role': role, 'path': path.relative_to(self.owner).as_posix()})
        (self.owner / 'quality').mkdir()
        self.key = self.owner / 'reviews/key'
        self.key.write_bytes(b'k' * 32)
        self.key.chmod(0o600)
        old = os.environ.get('AI_WORKFLOW_QA_BINDING_KEY_FILE')
        os.environ['AI_WORKFLOW_QA_BINDING_KEY_FILE'] = str(self.key)
        def restore():
            if old is None:
                os.environ.pop('AI_WORKFLOW_QA_BINDING_KEY_FILE', None)
            else:
                os.environ['AI_WORKFLOW_QA_BINDING_KEY_FILE'] = old
        self.addCleanup(restore)
        self.binding = load(self.lib / 'qa-commit-binding.py')
        self.eff = load(self.lib / 'execution-efficiency.py')
        self.snapshot = self.owner / 'reviews/snapshot.json'

    def make_snapshot(self):
        value = self.binding.snapshot(self.repo, self.workspace, 'synthetic', 'WORK-001', self.evidence,
                                      ['.gitignore'])
        self.snapshot.write_text(json.dumps(value))
        return value

    def verify(self):
        return self.binding.verify_snapshot(self.snapshot, self.eff.file_hash(self.snapshot), self.repo,
                                            self.workspace, 'synthetic', 'WORK-001')

    def commit(self):
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'synthetic reviewed change')

    def test_original_baseline_and_exact_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        self.make_snapshot()
        self.assertFalse(self.verify()['repositories'][0]['post_commit'])
        self.commit()
        self.assertTrue(self.verify()['repositories'][0]['post_commit'])

    def test_partial_staging(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        (self.repo / 'README.md').write_text('reviewed addition')
        self.make_snapshot()
        git(self.repo, 'add', 'AGENTS.md')
        git(self.repo, 'commit', '-qm', 'synthetic partial stage')
        with self.assertRaisesRegex(ValueError, 'tree/index'):
            self.verify()

    def test_live_mode_content_and_new_path_drift(self):
        for mutation in ('mode', 'permissions', 'content', 'new-path', 'delete'):
            with self.subTest(mutation=mutation):
                path = self.repo / 'AGENTS.md'
                path.write_text('Synthetic source baseline')
                path.chmod(0o644)
                extra = self.repo / 'README.md'
                extra.unlink(missing_ok=True)
                self.make_snapshot()
                if mutation == 'mode': path.chmod(0o755)
                elif mutation == 'permissions': path.chmod(0o666)
                elif mutation == 'content': path.write_text('unreviewed')
                elif mutation == 'new-path': extra.write_text('unreviewed')
                else: path.unlink()
                with self.assertRaisesRegex(ValueError, 'population'):
                    self.verify()

    def test_deleted_path_tombstone_commits(self):
        (self.repo / 'AGENTS.md').unlink()
        value = self.make_snapshot()
        self.assertEqual(value['sources'][0]['population']['AGENTS.md']['type'], 'deleted')
        self.commit()
        self.verify()

    def test_unrelated_commit_reject(self):
        self.make_snapshot()
        (self.repo / 'unapproved.txt').write_text('outside source roots')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'unexpected commit path'):
            self.verify()

    def test_artifact_chain_and_source_second_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        self.make_snapshot()
        self.commit()
        git(self.repo, 'commit', '--allow-empty', '-qm', 'synthetic artifact-only noop')
        self.verify()
        (self.repo / 'AGENTS.md').write_text('changed again')
        self.commit()
        with self.assertRaises(ValueError): self.verify()

    def test_git_replacement_cannot_hide_unauthorized_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        self.make_snapshot()
        self.commit()
        reviewed = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        (self.repo / 'unauthorized.txt').write_text('outside reviewed population')
        self.commit()
        unauthorized = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        git(self.repo, 'replace', unauthorized, reviewed)
        git(self.repo, 'read-tree', reviewed)
        (self.repo / 'unauthorized.txt').unlink()
        self.assertEqual(git(self.repo, 'rev-parse', 'HEAD').decode().strip(), unauthorized)
        with self.assertRaises(ValueError): self.verify()

    def test_git_graft_cannot_hide_intermediate_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        self.make_snapshot()
        self.commit()
        git(self.repo, 'commit', '--allow-empty', '-qm', 'synthetic intermediate')
        git(self.repo, 'commit', '--allow-empty', '-qm', 'synthetic last')
        head = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        (self.repo / '.git/info/grafts').write_text(head + ' ' + self.base + '\n')
        with self.assertRaisesRegex(ValueError, 'history'): self.verify()

    def test_ignored_source_nested_repository_and_symlink(self):
        bad = self.repo / '.systems/ignored'
        bad.mkdir()
        (bad / 'unknown.txt').write_text('must not be read')
        with self.assertRaisesRegex(ValueError, 'ignored source'): self.make_snapshot()
        shutil.rmtree(bad)
        nested = self.repo / '.systems/nested'
        nested.mkdir()
        git(nested, 'init', '-q')
        (nested / 'a.txt').write_text('foreign')
        with self.assertRaises(ValueError): self.make_snapshot()
        shutil.rmtree(nested)
        (self.repo / 'README.md').symlink_to(self.repo / 'AGENTS.md')
        with self.assertRaises(ValueError): self.make_snapshot()

    def test_required_roles_and_evidence_change(self):
        for role in self.binding.ROLES:
            with self.subTest(role=role), self.assertRaises(ValueError):
                self.binding.snapshot(self.repo, self.workspace, 'synthetic', 'WORK-001',
                                      [e for e in self.evidence if e['role'] != role])
        self.make_snapshot()
        (self.owner / 'decisions/synthetic.md').write_text('changed approval scope')
        with self.assertRaisesRegex(ValueError, 'evidence changed'): self.verify()

    def test_population_omission_and_unknown_schema(self):
        value = self.make_snapshot()
        del value['sources'][0]['population']['AGENTS.md']
        self.snapshot.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'population'): self.verify()
        value = self.make_snapshot()
        value['schema'] = True
        self.snapshot.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'schema'): self.verify()

    def test_data_dependency_and_repository_swap(self):
        with self.assertRaises(ValueError):
            self.binding.snapshot(self.repo, self.workspace, 'synthetic', 'WORK-001', self.evidence,
                                  ['.systems/ai/skills/legacy/a.md'])
        self.make_snapshot()
        value = json.loads(self.snapshot.read_text())
        value['sources'][0]['identity']['git_common'] = '/tmp/unrelated'
        self.snapshot.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'identity'): self.verify()

    def test_environment_check_and_dependency_drift(self):
        value = self.make_snapshot()
        value['environment'] = '0' * 64
        self.snapshot.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'environment'): self.verify()
        value = self.make_snapshot()
        value['dependencies'] = ['unbound.py']
        self.snapshot.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'dependency'): self.verify()

    def test_receipt_authentication_and_key_permissions(self):
        record = {'schema': 1, 'state': 'completed', 'exit_code': 0}
        record['authentication'] = self.eff.sign(record, self.eff.key_bytes(self.key))
        self.eff.verify_record(record, self.eff.key_bytes(self.key))
        record['exit_code'] = 1
        with self.assertRaises(ValueError): self.eff.verify_record(record, self.eff.key_bytes(self.key))
        self.key.chmod(0o644)
        with self.assertRaises(ValueError): self.eff.key_bytes(self.key)

    def make_quality(self, extra_inputs=()):
        self.make_snapshot()
        receipt = {'schema': 1, 'run_id': 'synthetic-source-001',
                   'purpose': 'full-source-verification', 'state': 'completed', 'exit_code': 0,
                   'source': self.eff.source_identity(self.repo),
                   'environment': self.eff.environment_identity(),
                   'root': self.eff.digest(str(self.repo)), 'checks': ['check-fixture']}
        receipt['authentication'] = self.eff.sign(receipt, self.eff.key_bytes(self.key))
        receipt_path = self.owner / 'reviews/receipt.json'
        receipt_path.write_text(json.dumps(receipt))
        producer = load(self.lib / 'quality-record.py')
        example = ROOT / '.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md'
        _, sections = producer.qa.read_current(example.read_text().splitlines())
        sections = {name: '\n'.join(lines).strip() for name, lines in sections.items()
                    if name != 'Input Artifacts'}
        record = {'schema': 2, 'kind': 'implementation-quality', 'task': 'WORK-001',
                  'run_id': 'synthetic-bound-001', 'verdict': 'PASS', 'date': '2026-10-04',
                  'inputs': [{'root': 'owning-project-evidence', 'path': e['path']}
                             for e in [*self.evidence, *extra_inputs]],
                  'sections': sections, 'binding': {'snapshot': 'reviews/snapshot.json',
                                                    'receipt': 'reviews/receipt.json'}}
        output, body = producer.render(record, self.repo, self.workspace, 'synthetic')
        producer.publish(output, body)
        return output, body

    def assess(self, report):
        return load(self.lib / 'qa-evidence.py').assess(report, self.repo, self.workspace, 'synthetic',
                                                     self.repo, 'implementation-quality',
                                                     'synthetic:WORK-001', require_pass=True)

    def test_v3_real_producer_current_and_post_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        report, body = self.make_quality()
        self.assertEqual(self.assess(report)['wire_version'], 3)
        self.commit()
        assessed = self.assess(report)
        self.assertTrue(assessed['source_equivalence_verified'])
        self.assertEqual(report.read_text(), body)
        self.assertEqual(assessed['binding']['authority'], 'none')
        self.assertTrue(assessed['binding']['repositories'][0]['post_commit'])
        result = subprocess.run([os.sys.executable, str(self.lib / 'qa-commit-binding.py'), 'verify',
                                 '--report', str(report), '--workflow-root', str(self.repo),
                                 '--workspace-root', str(self.workspace), '--project', 'synthetic',
                                 '--key-file', str(self.key)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['source_equivalence_verified'])

    def test_v3_missing_proof_fail_identity_modes_and_saved_result(self):
        report, body = self.make_quality()
        for mutation in ('fail', 'identity', 'snapshot', 'mixed', 'role', 'capability', 'key'):
            with self.subTest(mutation=mutation):
                report.write_text(body)
                before = json.loads(self.snapshot.read_text())
                key = os.environ['AI_WORKFLOW_QA_BINDING_KEY_FILE']
                if mutation == 'fail':
                    report.write_text(body.replace('Verdict: PASS', 'Verdict: FAIL'))
                elif mutation == 'identity':
                    report.write_text(body.replace('synthetic:WORK-001', 'synthetic:WORK-002'))
                elif mutation == 'snapshot':
                    report.write_text(body.replace('Source snapshot SHA-256:', 'Missing proof:'))
                elif mutation == 'mixed':
                    report.write_text(body + '\n- QA verification contract: \x60full-qa-verification-v2\x60\n')
                elif mutation == 'role':
                    report.write_text(body.replace('| owning-project-evidence | decisions/synthetic.md |',
                                                    '| owning-project-evidence | decisions/omitted.md |'))
                elif mutation == 'capability':
                    report.write_text(body.replace('Binding capability: phase-commit-policy-v1',
                                                    'Binding capability: unknown-v99'))
                else:
                    os.environ.pop('AI_WORKFLOW_QA_BINDING_KEY_FILE')
                with self.assertRaises(ValueError): self.assess(report)
                os.environ['AI_WORKFLOW_QA_BINDING_KEY_FILE'] = key
        report.write_text(body)
        # Saved eligible output is not accepted as a report or source proof.
        saved = self.owner / 'quality/phase-5-work-002-quality.md'
        saved.write_text(json.dumps(self.assess(report)))
        with self.assertRaises(ValueError): self.assess(saved)

    def test_runtime_commit_is_not_ambient_authority(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        self.make_snapshot()
        foreign = self.workspace / 'projects/foreign/status.md'
        foreign.parent.mkdir()
        foreign.write_text('unapproved foreign runtime')
        git(self.repo, 'add', 'AGENTS.md')
        git(self.repo, 'add', '-f', str(foreign))
        git(self.repo, 'commit', '-qm', 'synthetic unauthorized runtime')
        with self.assertRaisesRegex(ValueError, 'runtime chain'): self.verify()

    def test_unrelated_staged_input_rejects_before_commit(self):
        self.make_snapshot()
        (self.repo / 'unapproved.txt').write_text('outside approved population')
        git(self.repo, 'add', 'unapproved.txt')
        with self.assertRaisesRegex(ValueError, 'unrelated staged'): self.verify()

    def test_sensitive_inputs_are_rejected_without_blob_read(self):
        path = self.repo / '.systems/secret.key'
        path.write_text('synthetic only')
        with self.assertRaisesRegex(ValueError, 'sensitive'): self.make_snapshot()
        git(self.repo, 'add', str(path))
        with self.assertRaisesRegex(ValueError, 'sensitive'): self.make_snapshot()

    def test_hook_mutation_and_failed_commit_have_no_freshness(self):
        source = self.repo / 'AGENTS.md'
        source.write_text('reviewed change')
        self.make_snapshot()
        hook = self.repo / '.git/hooks/pre-commit'
        hook.write_text('#!/bin/sh\nprintf unreviewed >> AGENTS.md\nexit 1\n')
        hook.chmod(0o755)
        git(self.repo, 'add', '.')
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.repo, 'commit', '-qm', 'synthetic failing hook')
        self.assertEqual(git(self.repo, 'rev-parse', 'HEAD').decode().strip(), self.base)
        with self.assertRaisesRegex(ValueError, 'population'): self.verify()

    def test_current_consumers_agree_before_and_after_commit(self):
        (self.repo / 'AGENTS.md').write_text('reviewed change')
        report, _ = self.make_quality()
        namespace = self.owner / 'capture-state'
        namespace.mkdir()
        capture = namespace / 'work-001.md'
        body = ('# Distillation State\n- Capture schema: 3\n- Work ID: WORK-001\n'
                '- Work mode: full-project\n- Project/repo scope: synthetic\n'
                '- Source artifact: implementation/synthetic.md\n'
                '- Quality artifact: ' + report.relative_to(self.owner).as_posix() + '\n'
                '- State: completed\n- Distillation artifact: distillations/synthetic.md\n- Last reminder: none\n'
                '- Owner disposition: capture-now\n- Privacy/scope check: pass\n'
                '- Residual risk: synthetic only\n- is_distilled derived value: true\n')
        capture.write_text(body)
        distillation = self.owner / 'distillations/synthetic.md'
        distillation.parent.mkdir()
        distillation.write_text('# Accepted synthetic distillation\n- Task/package ID: WORK-001\n'
                                '## Distillation Gate\n- Ready for checkpoint processing: yes\n')
        status = self.owner / 'status.md'
        status.write_text('| Field | Value |\n| --- | --- |\n'
                          '| current-phase | phase-5-quality |\n| current-task | WORK-001 |\n')
        canonical = load(self.lib / 'capture-state.py')
        scoped = load(self.lib / 'validation-scope.py')
        coordinator = load(self.lib / 'coordinator-status.py')
        parallel = load(self.lib / 'parallel-orchestration.py')
        for committed in (False, True):
            with self.subTest(committed=committed):
                if committed: self.commit()
                inventory = canonical.inventory(self.workspace, self.repo, self.repo, 'synthetic')
                self.assertEqual(inventory['invalid'], [])
                self.assertEqual(inventory['records'][0]['quality_verification'], 'verified-current')
                scoped.validate_distillation(self.workspace, 'projects/synthetic', self.repo, self.repo)
                self.assertEqual(coordinator.status(self.repo, self.workspace, self.repo, 'synthetic')['gate'],
                                 'verified-pass')
                parallel.check_parent_gate(self.owner, {'repository_root': str(self.repo)}, 'WORK-001',
                                           report.relative_to(self.owner).as_posix(), 'capture-state/work-001.md')
        # Isolate the checkpoint quality consumer; full manifest/lifecycle validation
        # is covered by parallel-orchestration-tests.py, never mock the QA/capture gate.
        manifest = {'repository_root': str(self.repo), 'project': 'synthetic', 'run_id': 'fixture-001',
                    'coordinator_id': 'fixture-owner', 'source_snapshot': 'a' * 64, 'revision': 1,
                    'units': [], 'reservations': [],
                    'checkpoint': {'active_tasks': [], 'completed_since_checkpoint': 1},
                    'lifecycle': {'attempts': [], 'events': [], 'completed_tasks': ['WORK-001'],
                                  'checkpoint_epoch': 0, 'checkpoint_evidence': None,
                                  'parent_gates': {'WORK-001': {'quality': report.relative_to(self.owner).as_posix(),
                                                              'capture': 'capture-state/work-001.md',
                                                              'source_snapshot': 'a' * 64}}}}
        proof = self.owner / 'checkpoints/current.md'
        proof.parent.mkdir()
        proof.write_text('# Checkpoint\n## Metadata\n- Project: synthetic\n'
                         '- Workflow phase: phase-7-checkpoint\n- Result: completed\n'
                         '## Checkpoint Gate\n- Distillations processed atomically: yes\n'
                         '- Memory updated without mechanical copy-paste: yes\n'
                         '- Critical drift resolved or escalated: none\n'
                         '- Can continue project workflow: yes\n- Blocking reason: none\n'
                         '## Orchestration Checkpoint Binding\n- Run ID: fixture-001\n'
                         '- Coordinator ID: fixture-owner\n- Epoch: 0\n- Source snapshot: ' + 'a' * 64 + '\n'
                         '- Completed tasks: ["WORK-001"]\n')
        request = {'action': 'checkpoint', 'evidence': 'checkpoints/current.md', 'sha256': self.eff.file_hash(proof)}
        with mock.patch.object(parallel, 'validate', return_value=(self.repo, {}, {})):
            result, _, _ = parallel.apply_transition(manifest, request, self.owner, {})
            self.assertEqual(result['checkpoint']['completed_since_checkpoint'], 0)
        capture.write_text(body.replace('Capture schema: 3', 'Capture schema: 2'))
        self.assertTrue(canonical.inventory(self.workspace, self.repo, self.repo, 'synthetic')['invalid'])
        with self.assertRaises(ValueError):
            scoped.validate_distillation(self.workspace, 'projects/synthetic', self.repo, self.repo)
        self.assertEqual(coordinator.status(self.repo, self.workspace, self.repo, 'synthetic')['gate'], 'unknown')
        with mock.patch.object(parallel, 'validate', return_value=(self.repo, {}, {})), self.assertRaises(ValueError):
            parallel.apply_transition(manifest, request, self.owner, {})

    def test_wire_discriminator_and_v2_notes_are_not_opt_in(self):
        report, body = self.make_quality()
        self.assertNotIn('QA verification contract: \x60full-qa-verification-v2\x60', body)
        self.assertIn('Artifact kind: bound:implementation-quality', body)
        producer = load(self.lib / 'quality-record.py')
        example = ROOT / '.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md'
        _, sections = producer.qa.read_current(example.read_text().splitlines())
        sections = {k: '\n'.join(v).strip() for k, v in sections.items() if k != 'Input Artifacts'}
        sections['Evidence'] += '\n- Advisory note: full-qa-verification-v3 is not enabled.'
        record = {'schema': 1, 'kind': 'implementation-quality', 'task': 'WORK-002',
                  'run_id': 'ordinary-note-001', 'verdict': 'PASS', 'date': '2026-10-04',
                  'inputs': [{'root': 'owning-project-evidence', 'path': self.evidence[0]['path']}],
                  'sections': sections}
        output, ordinary = producer.render(record, self.repo, self.workspace, 'synthetic')
        self.assertEqual(producer.qa.assess(output, self.repo, self.workspace, 'synthetic',
                                          document=ordinary)['wire_version'] if 'wire_version' in
                         producer.qa.assess(output, self.repo, self.workspace, 'synthetic', document=ordinary)
                         else 2, 2)
        producer.publish(output, ordinary)
        result = subprocess.run([os.sys.executable, str(self.lib / 'qa-commit-binding.py'), 'verify',
                                 '--report', str(output), '--workflow-root', str(self.repo),
                                 '--workspace-root', str(self.workspace), '--project', 'synthetic',
                                 '--key-file', str(self.key)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('V3 source binding proof required', result.stderr)

    def test_foreign_owning_namespace_rejects(self):
        (self.workspace / 'projects/.git').mkdir()
        with self.assertRaisesRegex(ValueError, 'foreign repository'): self.make_snapshot()

    def test_source_changes_during_read_reject(self):
        report, _ = self.make_quality()
        qa = load(self.lib / 'qa-evidence.py')
        original = self.binding.load
        eff = original('execution-efficiency')
        verify_source = eff.verify_source
        def drift(*args):
            value = verify_source(*args)
            (self.repo / 'AGENTS.md').write_text('changed during receipt read')
            return value
        with mock.patch.object(eff, 'verify_source', side_effect=drift):
            with self.assertRaisesRegex(ValueError, 'population'):
                self.binding.assess_v3(report, self.repo, self.workspace, 'synthetic', self.repo,
                                      'implementation-quality', 'synthetic:WORK-001', False, True,
                                      None, True, False, qa)

    def test_non_role_qa_input_changes_during_read_reject(self):
        extra = self.owner / 'specs/additional.md'
        extra.write_text('Additional accepted planning evidence')
        report, _ = self.make_quality([{'path': 'specs/additional.md'}])
        qa = load(self.lib / 'qa-evidence.py')
        eff = self.binding.load('execution-efficiency')
        verify_source = eff.verify_source
        def drift(*args):
            value = verify_source(*args)
            extra.write_text('Changed after initial QA input validation')
            return value
        with mock.patch.object(eff, 'verify_source', side_effect=drift):
            with self.assertRaisesRegex(ValueError, 'stale or mismatched input'):
                self.binding.assess_v3(report, self.repo, self.workspace, 'synthetic', self.repo,
                                      'implementation-quality', 'synthetic:WORK-001', False, True,
                                      None, True, False, qa)

    def test_malformed_duplicate_unknown_wire_cannot_downgrade(self):
        qa = load(self.lib / 'qa-evidence.py')
        source = ROOT / '.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md'
        body = source.read_text()
        for declaration in ('- QA verification contract: \x60full-qa-verification-v3\x60 ',
                            '- QA verification contract: \x60full-qa-verification-v99\x60 ',
                            '- QA verification contract: full-qa-verification-v3',
                            '- QA verification contract: \x60full-qa-verification-v2\x60'):
            with self.subTest(declaration=declaration), self.assertRaises(ValueError):
                qa.assess(source, ROOT, ROOT / 'ai-workflow-workspace', 'EXAMPLE', schema_only=True,
                          document=body.replace('## Metadata\n', '## Metadata\n' + declaration + '\n', 1))


if __name__ == '__main__':
    unittest.main()
