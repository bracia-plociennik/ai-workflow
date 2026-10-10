#!/usr/bin/env python3
"""Synthetic regression fixtures for runtime integrity and policy eligibility."""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
LIB = ROOT / '.systems/scripts/lib'


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), LIB / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


capture, fixture, reads, policy, coordinator = [load(n) for n in
    ['capture-state', 'smoke-fixture', 'command-read-evidence', 'work-policy', 'coordinator-status']]


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def public_fixture(root, destination, extras=()):
    try:
        git_root = Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel').strip())).resolve()
    except subprocess.CalledProcessError:
        git_root = None
    if git_root is not None:
        if git_root != root:
            raise ValueError('public fixture source is not a Git root')
        return fixture.build(root, destination, extras)
    # Only the dispatcher's already-selected, isolated product copy is Gitless.
    temporary_root = Path(os.environ.get('TMPDIR', tempfile.gettempdir())).resolve()
    if os.environ.get('AI_WORKFLOW_SMOKE_CHILD') != '1' or not root.is_relative_to(temporary_root):
        raise ValueError('unknown Gitless product source')
    destination.mkdir()
    for top in sorted(fixture.TOP):
        entry = root / top
        paths = entry.rglob('*') if entry.is_dir() else [entry]
        for path in paths:
            raw = path.relative_to(root).as_posix()
            if not path.is_file() or not fixture.selected(raw):
                continue
            fixture.scope.contained(root, raw)
            target = destination / raw
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='runtime-integrity-')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name).resolve()
        self.repo = self.home / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        git(self.repo, 'config', 'user.email', 'fixture@example.invalid')
        git(self.repo, 'config', 'user.name', 'Synthetic Fixture')
        (self.repo / 'AGENTS.md').write_text('baseline')
        (self.repo / '.gitignore').write_text('ignored/\nai-workflow-workspace/\n.systems/ignored/\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'synthetic baseline')
        self.workspace = self.repo / 'ai-workflow-workspace'
        self.owner = self.workspace / 'repo'
        self.ns = self.owner / 'capture-state'
        self.ns.mkdir(parents=True)

    def state(self, state='completed', schema='1', work='WORK-001'):
        (self.owner / 'source.md').write_text('accepted synthetic source')
        (self.owner / 'quality.md').write_text('historical advisory closure')
        (self.owner / 'distillations').mkdir(exist_ok=True)
        (self.owner / 'distillations/work.md').write_text('# Distillation\n- Task/package ID: '+work+'\n## Distillation Gate\n- Ready for checkpoint processing: yes\n')
        fields = {'Capture schema': schema, 'Work ID': work, 'Work mode': 'workflow-maintenance',
                  'Project/repo scope': 'repo', 'Source artifact': 'source.md', 'Quality artifact': 'quality.md',
                  'State': state, 'Distillation artifact': 'distillations/work.md' if state == 'completed' else 'none',
                  'Last reminder': 'none', 'Owner disposition': 'capture-now', 'Privacy/scope check': 'pass',
                  'Residual risk': 'historical evidence only', 'is_distilled derived value': 'true' if state == 'completed' else 'false'}
        file = self.ns / 'work.md'
        file.write_text('# Capture\n'+'\n'.join('- '+k+': '+v for k,v in fields.items())+'\n')
        return file

    def inventory(self):
        return capture.inventory(self.workspace, ROOT, self.repo)

    def event(self, command, exit_code=0, status='completed'):
        return {'type':'item.completed','item':{'type':'command_execution','status':status,'command':command,'exit_code':exit_code}}

    def test_repo_namespace_and_historical_not_pass(self):
        self.state()
        result=self.inventory()
        self.assertEqual(result['total'],1)
        self.assertEqual(result['invalid'],[])
        self.assertEqual(result['records'][0]['quality_verification'],'unknown-historical-or-advisory')

    def test_completed_requires_owned_unique_distillation(self):
        self.state()
        (self.owner/'distillations/work.md').unlink()
        self.assertTrue(self.inventory()['invalid'])

    def test_completed_requires_source_artifact(self):
        file = self.state()
        file.write_text(file.read_text().replace('- Source artifact: source.md', '- Source artifact: none'))
        self.assertTrue(self.inventory()['invalid'])

    def test_duplicate_work_rejected(self):
        file=self.state()
        (self.ns/'duplicate.md').write_bytes(file.read_bytes())
        self.assertTrue(self.inventory()['invalid'])

    def test_missing_required_state_field_rejected(self):
        file=self.state()
        file.write_text(file.read_text().replace('- Privacy/scope check: pass\n',''))
        self.assertTrue(self.inventory()['invalid'])

    def test_symlink_evidence_rejected(self):
        self.state()
        (self.owner/'source.md').unlink()
        (self.owner/'source.md').symlink_to(self.repo/'AGENTS.md')
        self.assertTrue(self.inventory()['invalid'])

    def test_traversal_evidence_rejected(self):
        file=self.state()
        file.write_text(file.read_text().replace('source.md','../../AGENTS.md'))
        self.assertTrue(self.inventory()['invalid'])

    def test_unknown_schema_rejected(self):
        self.state(schema='99')
        self.assertTrue(self.inventory()['invalid'])

    def test_schema2_cannot_promote_advisory_to_pass(self):
        self.state(schema='2')
        self.assertTrue(self.inventory()['invalid'])

    def test_foreign_project_excluded(self):
        p=self.workspace/'projects/foreign'; p.mkdir(parents=True); (p/'.git').mkdir()
        (p/'capture-state').mkdir(); (p/'capture-state/unsafe.md').write_text('private fixture')
        self.assertEqual(self.inventory()['skipped'],['projects/foreign:foreign-repository'])
        self.assertEqual(self.inventory()['total'],0)

    def test_scoped_v1_population_unchanged(self):
        (self.owner/'core').mkdir(); (self.owner/'core/status.md').write_text('core')
        self.state()
        files=capture.scope.runtime_files(self.workspace,'repo/core')
        self.assertEqual([p.name for p in files],['status.md'])

    def capture_paths(self, project=True):
        if project:
            self.owner = self.workspace / 'projects/synthetic'
            self.ns = self.owner / 'capture-state'
            self.ns.mkdir(parents=True)
        return self.owner

    def capture_parity(self):
        inventory = capture.inventory(self.workspace, ROOT, self.repo, 'synthetic')
        try:
            scoped = capture.scope.validate_distillation(self.workspace, 'projects/synthetic', ROOT, self.repo)
        except ValueError:
            scoped = None
        self.assertEqual(bool(inventory['invalid']), scoped is None)
        if scoped is not None:
            self.assertEqual(inventory['records'], scoped['records'])
        return inventory

    def test_capture_legacy_absent_derived_and_legacy_gate_parity(self):
        self.capture_paths()
        file = self.state()
        file.write_text(file.read_text().replace('- is_distilled derived value: true\n', ''))
        (self.owner / 'distillations/work.md').write_text(
            '- Work ID: WORK-001\n- State after accepted distillation: completed\n')
        out = self.capture_parity()
        self.assertFalse(out['invalid'])
        self.assertEqual(out['records'][0]['quality_verification'], 'unknown-historical-or-advisory')
        self.assertTrue(out['records'][0]['is_distilled'])

    def test_capture_duplicate_invalid_claim_still_blocks_valid_sibling(self):
        self.capture_paths()
        file = self.state()
        (self.ns / 'invalid.md').write_text(file.read_text().replace('- Privacy/scope check: pass\n', ''))
        out = self.capture_parity()
        self.assertTrue(out['invalid'])
        self.assertEqual(out['records'], [])

    def test_capture_reused_distillation_invalid_identity_still_blocks(self):
        self.capture_paths()
        file = self.state()
        (self.ns / 'second.md').write_text(file.read_text().replace('WORK-001', 'WORK-002'))
        out = self.capture_parity()
        self.assertTrue(out['invalid'])
        self.assertEqual(out['records'], [])

    def test_capture_normalized_duplicate_claims_share_record_parser(self):
        self.capture_paths()
        file = self.state('pending-quality')
        (self.ns / 'second.md').write_text(file.read_text().replace('WORK-001', 'WO`RK-001'))
        out = self.capture_parity()
        self.assertTrue(out['invalid'])
        self.assertEqual(out['records'], [])

    def test_capture_pending_quality_without_quality_and_ready_without_distillation(self):
        self.capture_paths()
        file = self.state('pending-quality', '2')
        file.write_text(file.read_text().replace('Quality artifact: quality.md', 'Quality artifact: none'))
        self.assertFalse(self.capture_parity()['invalid'])
        file = self.state('ready', '1')
        self.assertFalse(self.capture_parity()['invalid'])

    def current_capture_fixture(self):
        self.capture_paths()
        file = self.state('ready', '2')
        (self.owner / 'quality').mkdir()
        producer = load('quality-record')
        compliance = {
            'Result': 'PASS', 'Owner instruction reviewed': 'yes', 'Accepted plan reviewed': 'yes',
            'Accepted spec reviewed': 'yes', 'Scope/out-of-scope reviewed': 'yes',
            'Acceptance criteria reviewed': 'yes', 'Compliance status': 'aligned',
            'Wrong problem solved': 'no', 'Owner instruction mismatch': 'no',
            'Accepted plan mismatch': 'no', 'Accepted spec mismatch': 'no',
            'Acceptance criteria gap': 'no', 'Scope creep': 'no', 'Underbuild': 'no',
            'Overbuild': 'no', 'Evidence': 'synthetic accepted source'}
        completeness = {
            'Status': 'complete', 'Reviewed baseline': 'synthetic repository/source',
            'Closure freshness': 'current', 'Post-fix full re-review': 'not-required',
            'Policy-boundary adversarial matrix': 'completed', 'Producer-consumer field audit': 'completed',
            'Required-field mapping': 'complete', 'Cross-contract consistency': 'aligned',
            'Risk/work mode compatibility': 'aligned',
            'Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed': 'yes',
            'Negative-space / adversarial review': 'completed', 'Automated evidence role': 'supporting-only',
            'Instruction refresh': 'performed-targeted', 'Instruction baseline': 'current',
            'Producers/consumers reviewed': 'synthetic accepted input and QA', 'Evidence': 'synthetic regression'}
        flags = ('Intent / Plan / Spec Compliance PASS', 'Review Completeness Gate PASS',
                 'Cross-contract consistency aligned', 'Risk/work mode compatibility aligned',
                 'Negative-space / adversarial review complete or not applicable',
                 'Automated evidence treated as supporting-only', 'Post-fix full re-review complete or not required',
                 'Instruction baseline current', 'Closure freshness current',
                 'Policy-boundary adversarial matrix complete or not applicable',
                 'Producer-consumer field audit complete or not applicable',
                 'Required-field mapping complete or not applicable', '100% DoD satisfied',
                 'No known bug in scope', 'No regression in changed/direct paths',
                 'Edge cases covered or explicitly rejected', 'Explicit evidence attached')
        bullets = lambda fields: '\n'.join('- ' + key + ': ' + val for key, val in fields.items())
        sections = {
            'Findings': '- Blockers: none\n- Unresolved findings: none',
            'Evidence': 'Synthetic fixture with actual complete QA consumer verification.',
            'Definition Of Done Validation': '| DoD Item | Result | Evidence |\n| --- | --- | --- |\n| Synthetic source | PASS | fixture |',
            'Intent / Plan / Spec Compliance': bullets(compliance),
            'Review Completeness Gate': bullets(completeness),
            'Adaptive Data / Integration Verification Matrix': '- Applicability: not-applicable\n- Not-applicable reason: isolated synthetic input',
            'Quality Gate': '\n'.join('- ' + key + ': yes' for key in flags) + '\n- Quality result: PASS\n- Required next phase: phase-6-distillation',
            'Gate Decision': '- Quality result: PASS\n- Required next phase: phase-6-distillation'}
        review = {'schema': 1, 'kind': 'implementation-quality', 'task': 'WORK-001',
                  'run_id': 'synthetic-capture-current', 'verdict': 'PASS', 'date': '2026-10-04',
                  'inputs': [{'root': 'owning-project-evidence', 'path': 'source.md'}], 'sections': sections}
        report, body = producer.render(review, self.repo, self.workspace, 'synthetic')
        producer.publish(report, body)
        file.write_text(file.read_text().replace('quality.md', 'quality/' + report.name))
        valid = file.read_text()
        return file, report, body, valid

    def admit_capture_history(self, report):
        metadata, _ = load('qa-evidence').read_current(report.read_text().splitlines())
        relative = report.relative_to(self.owner).as_posix()
        (self.owner / 'decisions').mkdir(exist_ok=True)
        decision = self.owner / 'decisions/history.md'
        decision.write_text('- History decision: approved\n- Approved report: ' + relative +
                            '\n- Approved state: historical\n- Source: synthetic owner preservation')
        registry = {'schema': 1, 'assessments': [{'path': relative,
                    'sha256': hashlib.sha256(report.read_bytes()).hexdigest(), 'state': 'historical',
                    'assessed_head': metadata['Assessed source HEAD'], 'decision': 'decisions/history.md',
                    'decision_sha256': hashlib.sha256(decision.read_bytes()).hexdigest()}]}
        (self.owner / 'quality-assessments.json').write_text(json.dumps(registry))

    def test_capture_admitted_history_is_not_current_parent_acceptance(self):
        file, report, body, valid = self.current_capture_fixture()
        completed = valid.replace('State: ready', 'State: completed').replace(
            'derived value: false', 'derived value: true').replace(
            'Distillation artifact: none', 'Distillation artifact: distillations/work.md')
        file.write_text(completed)
        git(self.repo, 'commit', '--allow-empty', '-qm', 'changed source baseline')
        self.assertTrue(self.capture_parity()['invalid'])
        self.admit_capture_history(report)
        result = self.capture_parity()
        self.assertFalse(result['invalid'])
        self.assertEqual(result['records'][0]['quality_verification'], 'verified-historical')
        self.assertTrue(result['records'][0]['is_distilled'])
        self.assertEqual(result['unresolved'], 0)
        self.assertEqual(file.read_text(), completed)
        self.assertEqual(report.read_text(), body)
        with self.assertRaisesRegex(ValueError, 'historical assessment cannot supply current PASS'):
            load('parallel-orchestration').check_parent_gate(
                self.owner, {'repository_root': str(self.repo)}, 'WORK-001',
                'quality/' + report.name, 'capture-state/work.md')

    def test_capture_historical_original_source_qa_and_decision_integrity(self):
        file, report, body, valid = self.current_capture_fixture()
        self.admit_capture_history(report)
        self.assertFalse(self.capture_parity()['invalid'])
        source = self.owner / 'source.md'
        source.write_text('changed historical source')
        self.assertTrue(self.capture_parity()['invalid'])
        source.write_text('accepted synthetic source')
        report.write_text(body + '\nchanged')
        self.assertTrue(self.capture_parity()['invalid'])
        report.write_text(body)
        decision = self.owner / 'decisions/history.md'
        decision.write_text(decision.read_text() + '\nchanged')
        self.assertTrue(self.capture_parity()['invalid'])

    def test_capture_schema2_real_current_qa_and_negative_parity(self):
        file, report, body, valid = self.current_capture_fixture()
        self.assertEqual(self.capture_parity()['records'][0]['quality_verification'], 'verified-current')
        for mutation in ('derived', 'identity', 'head', 'hash', 'gate', 'kind', 'unbound-source'):
            with self.subTest(mutation=mutation):
                file.write_text(valid)
                report.write_text(body)
                if mutation == 'derived':
                    file.write_text(valid.replace('derived value: false', 'derived value: true'))
                elif mutation == 'identity':
                    report.write_text(body.replace('synthetic:WORK-001', 'synthetic:WORK-002'))
                elif mutation == 'head':
                    report.write_text(body.replace(git(self.repo, 'rev-parse', 'HEAD').decode().strip(), '0' * 40))
                elif mutation == 'hash':
                    (self.owner / 'source.md').write_text('changed source')
                elif mutation == 'gate':
                    report.write_text(body.replace('- Verdict: PASS', '- Verdict: FAIL'))
                elif mutation == 'unbound-source':
                    (self.owner / 'other.md').write_text('existing unreviewed source')
                    file.write_text(valid.replace('Source artifact: source.md', 'Source artifact: other.md'))
                else:
                    report.write_text(body.replace('Artifact kind: implementation-quality', 'Artifact kind: spec-qa'))
                self.assertTrue(self.capture_parity()['invalid'])
                (self.owner / 'source.md').write_text('accepted synthetic source')
        report.write_text(body)
        file.write_text(valid)
        completed = valid.replace('State: ready', 'State: completed').replace(
            'derived value: false', 'derived value: true').replace(
            'Distillation artifact: none', 'Distillation artifact: distillations/work.md')
        file.write_text(completed)
        self.assertFalse(self.capture_parity()['invalid'])
        orchestration = load('parallel-orchestration')
        manifest = {'repository_root': str(self.repo)}
        gate = lambda: orchestration.check_parent_gate(
            self.owner, manifest, 'WORK-001', 'quality/' + report.name, 'capture-state/work.md')
        gate()
        accepted_text = (self.owner / 'distillations/work.md').read_text()
        for bad_gate in (
            accepted_text.replace('processing: yes', 'processing: no') +
            '\n## Other\n- Ready for checkpoint processing: yes\n',
            accepted_text + '- Ready for checkpoint processing: no\n',
            accepted_text + '\n## Distillation Gate\n- Ready for checkpoint processing: yes\n'):
            (self.owner / 'distillations/work.md').write_text(bad_gate)
            self.assertTrue(self.capture_parity()['invalid'])
            with self.assertRaisesRegex(ValueError, 'parent capture collection invalid'):
                gate()
        (self.owner / 'distillations/work.md').write_text(accepted_text)
        vendor = self.owner / 'distillations/vendor'
        vendor.mkdir()
        (vendor / '.git').mkdir()
        (vendor / 'work.md').write_text(accepted_text)
        file.write_text(completed.replace('distillations/work.md', 'distillations/vendor/work.md'))
        self.assertTrue(self.capture_parity()['invalid'])
        with self.assertRaisesRegex(ValueError, 'parent capture collection invalid'):
            gate()
        # Do not leave a foreign root in the synthetic owner for subsequent public checks.
        (vendor / 'work.md').unlink()
        (vendor / '.git').rmdir()
        vendor.rmdir()
        file.write_text(completed)
        for sibling in ('missing', 'duplicate', 'reuse', 'normalized-duplicate'):
            with self.subTest(sibling=sibling):
                bad = self.ns / 'sibling.md'
                if sibling == 'missing':
                    bad.write_text('- Work ID: OTHER-001\n')
                elif sibling == 'duplicate':
                    bad.write_text(completed)
                elif sibling == 'normalized-duplicate':
                    (self.owner / 'distillations/second.md').write_text(accepted_text)
                    bad.write_text(completed.replace('WORK-001', 'WO`RK-001').replace(
                        'distillations/work.md', 'distillations/second.md'))
                else:
                    bad.write_text(completed.replace('WORK-001', 'WORK-002'))
                with self.assertRaisesRegex(ValueError, 'parent capture collection invalid'):
                    gate()
                bad.unlink()
        (self.owner / 'distillations/work.md').write_text(
            '- Task/package ID: WORK-001\n## Distillation Gate\n- Ready for checkpoint processing: no\n')
        self.assertTrue(self.capture_parity()['invalid'])
        (self.owner / 'distillations/work.md').write_text(
            '- Task/package ID: WORK-001\n## Distillation Gate\n- Ready for checkpoint processing: yes\n')
        file.write_text(valid)
        # Exercise all public shell routes on the identical selected population.
        installed = self.repo / 'ai-workflow'
        public_fixture(ROOT, installed, ['.systems/scripts/lib/capture-record.py'])
        env = {**os.environ, 'AI_WORKFLOW_MODE': 'target',
               'AI_WORKFLOW_WORKSPACE_HOME': str(self.workspace)}
        for args in ([], ['--project', 'synthetic'],
                     ['--runtime-only', '--scope-root', 'projects/synthetic']):
            result = subprocess.run(['bash', str(installed / '.systems/scripts/check-distillation-state'), *args],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_fixture_preserves_git_selected_privacy_boundary(self):
        source = self.repo / '.systems/local-notes.md'
        source.parent.mkdir()
        source.write_text('synthetic excluded input')
        (self.repo / '.git/info/exclude').write_text('.systems/local-notes.md\n')
        output = self.home / 'public-fixture'
        public_fixture(self.repo, output)
        self.assertFalse((output / '.systems/local-notes.md').exists())
        self.assertEqual((output / 'AGENTS.md').read_text(), 'baseline')

    def test_public_fixture_rejects_unknown_gitless_source(self):
        source = self.home / 'unknown-source'
        source.mkdir()
        with patch.dict(os.environ, {'AI_WORKFLOW_SMOKE_CHILD': '0'}):
            with self.assertRaisesRegex(ValueError, 'unknown Gitless'):
                public_fixture(source, self.home / 'unknown-output')

    def test_fixture_current_worktree_not_head(self):
        (self.repo/'AGENTS.md').write_text('current')
        output=self.home/'fixture'
        fixture.build(self.repo,output)
        self.assertEqual((output/'AGENTS.md').read_text(),'current')

    def test_fixture_excludes_ignored_and_unrelated(self):
        (self.repo/'ignored').mkdir(); (self.repo/'ignored/private.md').write_text('private')
        (self.repo/'unrelated.md').write_text('untracked')
        output=self.home/'fixture'; fixture.build(self.repo,output)
        self.assertFalse((output/'ignored').exists()); self.assertFalse((output/'unrelated.md').exists())
        self.assertFalse((output/'ai-workflow-workspace').exists())

    def test_fixture_explicit_new_product_only(self):
        (self.repo/'.systems').mkdir(); (self.repo/'.systems/new.py').write_text('source')
        output=self.home/'fixture'; fixture.build(self.repo,output,['.systems/new.py'])
        self.assertTrue((output/'.systems/new.py').exists())

    def test_fixture_retains_synthetic_context_but_not_raw_skill_context(self):
        example = self.repo / '.systems/ai/examples/projects/example/context/brief.md'
        raw = self.repo / '.systems/ai/skills/example/context/raw.md'
        for path in (example, raw):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic fixture')
        git(self.repo, 'add', '.systems')
        output = self.home / 'fixture'
        fixture.build(self.repo, output)
        self.assertTrue((output / example.relative_to(self.repo)).is_file())
        self.assertFalse((output / raw.relative_to(self.repo)).exists())

    def test_fixture_rejects_ignored_extra(self):
        p=self.repo/'.systems/ignored/private.md'; p.parent.mkdir(parents=True); p.write_text('private')
        with self.assertRaises(ValueError): fixture.build(self.repo,self.home/'fixture',['.systems/ignored/private.md'])

    def test_fixture_rejects_extra_traversal(self):
        with self.assertRaises(ValueError): fixture.build(self.repo,self.home/'fixture',['../repo/AGENTS.md'])

    def test_fixture_rejects_symlink(self):
        (self.repo/'AGENTS.md').unlink(); (self.repo/'AGENTS.md').symlink_to(self.repo/'.gitignore')
        with self.assertRaises(ValueError): fixture.build(self.repo,self.home/'fixture')

    def test_fixture_preserves_deletion(self):
        (self.repo/'AGENTS.md').unlink(); output=self.home/'fixture'; fixture.build(self.repo,output)
        self.assertFalse((output/'AGENTS.md').exists())

    def test_fixture_rejects_nonempty_output(self):
        with self.assertRaises(ValueError): fixture.build(self.repo,self.repo)

    def test_false_and_cat_not_executed(self):
        out=reads.summarize([self.event("/bin/zsh -lc 'false && cat .systems/ai/core/permissions.md'",1)])
        self.assertEqual(out['confirmed_paths'],[]); self.assertEqual(out['reads'][0]['state'],'not-executed')

    def test_success_survives_later_failure(self):
        out=reads.summarize([self.event('cat AGENTS.md'),self.event('false',1)])
        self.assertEqual(out['confirmed_paths'],['AGENTS.md'])

    def test_compound_pipeline_branch_unknown(self):
        for command in ['cat AGENTS.md; false','cat AGENTS.md | cat','if true; then cat AGENTS.md; fi','cat AGENTS.md && false','echo cat AGENTS.md']:
            with self.subTest(command=command):
                out=reads.summarize([self.event(command)])
                self.assertEqual(out['confirmed_paths'],[])
                self.assertEqual(out['reads'][0]['state'],'unknown')

    def test_incomplete_read_attempted(self):
        out=reads.summarize([self.event('cat AGENTS.md',None,'in_progress')])
        self.assertEqual(out['reads'][0]['state'],'attempted')

    def test_comment_and_expression_are_not_file_reads(self):
        out=reads.summarize([self.event('cat AGENTS.md # .systems/ai/core/permissions.md')])
        self.assertEqual(out['confirmed_paths'],['AGENTS.md'])
        for command in ["sed 's/AGENTS.md/replacement/' unrelated.txt", "rg 'AGENTS.md' unrelated.txt"]:
            self.assertEqual(reads.summarize([self.event(command)])['confirmed_paths'],[])

    def test_sed_literal_filename_confirmed(self):
        out=reads.summarize([self.event("sed -n '1,80p' .systems/ai/core/permissions.md")])
        self.assertEqual(out['confirmed_paths'],['.systems/ai/core/permissions.md'])

    def test_absolute_literal_read_path_is_retained(self):
        path = '/tmp/synthetic/.systems/ai/core/permissions.md'
        out = reads.summarize([self.event('cat '+path)])
        self.assertEqual(out['confirmed_paths'], [path])
        out = reads.summarize([self.event('false && cat '+path, 1)])
        self.assertEqual(out['reads'][0]['state'], 'not-executed')

    def test_rg_filename_listing_is_not_content_read(self):
        for binary in ['rg', '/usr/bin/rg']:
            out = reads.summarize([self.event(binary+' --files AGENTS.md')])
            self.assertEqual(out['confirmed_paths'], [])
            self.assertEqual(out['reads'][0]['state'], 'unknown')

    def test_help_and_started_events_not_confirmed(self):
        for command in ['cat --help AGENTS.md','head --version AGENTS.md']:
            self.assertEqual(reads.summarize([self.event(command)])['confirmed_paths'],[])
        event=self.event('cat AGENTS.md'); event['type']='item.started'
        self.assertEqual(reads.summarize([event])['confirmed_paths'],[])

    def test_unrelated_tracked_secret_not_inspected(self):
        p=self.repo/'credentials/private.md';p.parent.mkdir();p.write_text('synthetic private')
        git(self.repo,'add','credentials/private.md')
        output=self.home/'fixture';fixture.build(self.repo,output)
        self.assertFalse((output/'credentials').exists())

    def test_foreign_workspace_root_rejected(self):
        (self.workspace/'.git').mkdir()
        with self.assertRaises(ValueError): self.inventory()

    def test_micro_eligibility_and_growth(self):
        args=dict(risk='low',files=['a','b','test'],reversible=True,local=True,themes=[],one_change=True)
        self.assertTrue(policy.micro_exempt(**args))
        self.assertFalse(policy.micro_exempt(**{**args,'files':['a','b','c','d']}))
        self.assertFalse(policy.micro_exempt(**{**args,'risk':'medium'}))
        self.assertFalse(policy.micro_exempt(**{**args,'active_plan':True}))
        for theme in policy.EXCLUDED:
            self.assertFalse(policy.micro_exempt(**{**args,'themes':[theme]}))

    def test_compact_cannot_hide_material_boundary(self):
        self.assertEqual(policy.response_mode(simple_answer=True),'compact')
        for field in ['formal','decision','blocker','handoff','material_limits']:
            self.assertEqual(policy.response_mode(simple_answer=True,**{field:True}),'full')

    def test_capability_not_frozen_model(self):
        self.assertEqual(policy.model_capability(risk='low'),'efficient-reasoning')
        self.assertEqual(policy.model_capability(risk='high'),'strong-reasoning')
        self.assertEqual(policy.model_capability(risk='low',adversarial=True),'strong-reasoning')

    def project_status(self,phase='phase-4-implementation'):
        p=self.workspace/'projects/synthetic'; p.mkdir(parents=True)
        (p/'status.md').write_text('| Field | Value |\n| --- | --- |\n| project | synthetic |\n| current-phase | '+phase+' |\n| current-task | TEST-001 |\n| phase-result | PASS |\n')
        return p

    def test_coordinator_does_not_promote_declared_pass(self):
        self.project_status()
        out=coordinator.status(self.repo,self.workspace,self.repo,'synthetic')
        self.assertIsNone(out['verified_qa']); self.assertEqual(out['gate'],'unknown'); self.assertFalse(out['execution_authorized'])

    def test_coordinator_missing_evidence_unknown(self):
        self.project_status('phase-5-quality')
        out=coordinator.status(self.repo,self.workspace,self.repo,'synthetic')
        self.assertEqual(out['freshness'],'unknown'); self.assertTrue(out['blockers'])

    def current_architecture(self):
        p=self.project_status('phase-1-architecture-qa')
        (p/'quality').mkdir()
        source=p/'architecture.md'; source.write_text('accepted synthetic architecture')
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        binding=hashlib.sha256(('owning-project-evidence:architecture.md='+digest+'\n').encode()).hexdigest()
        head=git(self.repo,'rev-parse','HEAD').decode().strip()
        (p/'quality/phase-1-architecture-qa.md').write_text('''# Synthetic QA
- QA verification contract: `full-qa-verification-v2`
## Current QA Run
- Run ID: synthetic-architecture
- Artifact kind: architecture-qa
- Project/task identity: synthetic
- Assessed source HEAD: '''+head+'''
- Assessed worktree digest: '''+binding+'''
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS
### Input Artifacts
| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | architecture.md | '''+digest+''' |
### Findings
- Blockers: none
- Unresolved findings: none
### Evidence
- Read accepted synthetic input and verified source hash.
### Review Completeness Gate
- Status: complete
- Reviewed baseline: synthetic architecture and bound source hash
- Closure freshness: current
- Post-fix full re-review: not-required
- Policy-boundary adversarial matrix: not-applicable
- Producer-consumer field audit: not-applicable
- Required-field mapping: not-applicable
### QA Verification Scope
Synthetic artifact intent and criteria review, no implementation claim.
### Artifact QA Completeness Gate
- Owner intent and governing sources reviewed: synthetic accepted architecture
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned
- Post-fix full artifact re-review: not-required
- Evidence reviewed: architecture.md and bound source hash
- Skipped or unreadable sources: none
- Residual risk: synthetic fixture only
- Closure freshness: current
### Gate Decision
- Result: PASS
''')
        return p

    def test_coordinator_reuses_real_qa_reader(self):
        self.current_architecture()
        out=coordinator.status(self.repo,self.workspace,self.repo,'synthetic')
        self.assertEqual(out['gate'],'verified-pass'); self.assertEqual(out['freshness'],'current')
        self.assertFalse(out['execution_authorized'])

    def test_coordinator_rejects_stale_hash_and_verdict_conflict(self):
        p=self.current_architecture(); source=p/'architecture.md'
        source.write_text('changed')
        self.assertEqual(coordinator.status(self.repo,self.workspace,self.repo,'synthetic')['gate'],'unknown')
        source.write_text('accepted synthetic architecture')
        report=p/'quality/phase-1-architecture-qa.md'
        report.write_text(report.read_text().replace('- Gate Decision: PASS','- Gate Decision: FAIL'))
        self.assertEqual(coordinator.status(self.repo,self.workspace,self.repo,'synthetic')['gate'],'unknown')

    def test_coordinator_rejects_stale_head(self):
        self.current_architecture()
        (self.repo/'AGENTS.md').write_text('new baseline'); git(self.repo,'add','AGENTS.md');git(self.repo,'commit','-qm','new baseline')
        self.assertEqual(coordinator.status(self.repo,self.workspace,self.repo,'synthetic')['freshness'],'unknown')

    def test_coordinator_unsupported_version_and_json_failure(self):
        self.project_status()
        args=['python3',str(LIB/'coordinator-status.py'),'--workflow',str(self.repo),'--workspace',str(self.workspace),
              '--repo',str(self.repo),'--project','synthetic']
        run=subprocess.run(args+['--schema-version','99'],capture_output=True,text=True)
        self.assertEqual(run.returncode,2)
        run=subprocess.run(args,capture_output=True,text=True)
        self.assertEqual(run.returncode,1); self.assertEqual(json.loads(run.stdout)['gate'],'unknown')

    def test_coordinator_git_failure_is_controlled_json(self):
        nonrepo = self.home / 'nonrepo'
        nonrepo.mkdir()
        run = subprocess.run(['python3', str(LIB/'coordinator-status.py'), '--workflow', str(self.repo),
                              '--workspace', str(self.workspace), '--repo', str(nonrepo), '--project', 'synthetic'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(json.loads(run.stdout)['gate'], 'unknown')
        self.assertNotIn('Traceback', run.stderr)

    def test_coordinator_rejects_identity_mismatch(self):
        p=self.project_status(); (p/'status.md').write_text('| project | another |\n')
        with self.assertRaises(ValueError): coordinator.status(self.repo,self.workspace,self.repo,'synthetic')

    def test_coordinator_rejects_source_symlink(self):
        p=self.project_status(); (p/'status.md').unlink(); (p/'status.md').symlink_to(self.repo/'AGENTS.md')
        with self.assertRaises(ValueError): coordinator.status(self.repo,self.workspace,self.repo,'synthetic')

    def test_coordinator_detects_baseline_change(self):
        self.project_status()
        with patch.object(coordinator,'baseline',side_effect=[{'head':'a'}, {'head':'b'}]):
            with self.assertRaises(ValueError): coordinator.status(self.repo,self.workspace,self.repo,'synthetic')

    def test_contract_integration(self):
        for raw, terms in {
            '.systems/ai/core/runtime-integrity.md':['confirmed','attempted','unknown','execution_authorized','schema-v1'],
            '.systems/ai/core/delivery-constraints.md':['micro-exempt','three files','focused QA','reclassify'],
            '.systems/ai/core/response-contract.md':['Response Mode','compact','full','blocker','skipped checks'],
            '.systems/ai/core/model-selection-guidance.md':['efficient-reasoning','strong-reasoning','current authoritative availability source','do not guess'],
            '.systems/scripts/validate-workflow':['check-runtime-integrity'],
            '.systems/scripts/check-required-artifacts':['runtime-integrity.md','check-runtime-integrity'],
        }.items():
            text=(ROOT/raw).read_text()
            for term in terms:
                with self.subTest(path=raw,term=term): self.assertIn(term,text)
        for path in ['.systems/ai/core/command-routing.md', '.systems/ai/core/operating-model.md']:
            text = (ROOT / path).read_text()
            self.assertIn('When capability choice is material', text)
            self.assertNotIn('Every new planning, implementation, and QA scope reports', text)

    def test_runtime_policy_adversarial_matrix(self):
        script=(ROOT/'.systems/scripts/check-runtime-integrity').read_text()
        patterns=re.findall(r"policy_reject_unsafe_pattern \\\n  '([^']+)'",script)
        clauses=['micro-exempt may skip QA','coordinator may grant execution','command text proves read']
        self.assertEqual(len(patterns),len(clauses))
        source=self.home/'policy.md'
        command='source "$1"; fail=0; policy_reject_unsafe_pattern "$2" unsafe "$3"; exit "$fail"'
        for pattern,clause in zip(patterns,clauses):
            for text,expected in [('Do not '+clause,0),(clause,1),('Do not '+clause+', but '+clause,1)]:
                source.write_text(text+'\n')
                run=subprocess.run(['bash','-c',command,'_',str(LIB/'policy-boundaries.sh'),pattern,str(source)],capture_output=True,text=True)
                with self.subTest(text=text): self.assertEqual(run.returncode,expected)


if __name__=='__main__':
    unittest.main(verbosity=2)
