#!/usr/bin/env python3
"""Synthetic regression fixtures for runtime integrity and policy eligibility."""
import hashlib
import importlib.util
import json
import os
import re
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


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='runtime-integrity-')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
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
