#!/usr/bin/env python3
"""Behavior tests: disposable fixtures only; mock activity where explicitly named."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import durable_runtime as rt
import task_resource_cleanup as tr


def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE).decode().strip()


def test_storage():
    bound = rt.load(SCRIPTS.parents[1])
    root = Path(os.environ['TASK_RESOURCE_TEST_STORAGE']) if os.environ.get('TASK_RESOURCE_TEST_STORAGE') else (Path(bound['workspace']) if bound else SCRIPTS.parents[1] / 'ai-workflow-workspace')
    created_workspace = not root.exists()
    rt.unlinked(root, exists=False)
    root.mkdir(parents=True, exist_ok=True)
    rt.durable(root)
    workspace = root
    owner = root / 'projects/task-resource-cleanup-v1'
    root = owner / 'evidence/synthetic-fixtures' if owner.is_dir() else root / '.task-resource-fixtures'
    root.mkdir(parents=True, exist_ok=True)
    return root, workspace, created_workspace


class Lifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage, cls.fixture_workspace, cls.created_workspace = test_storage()

    @classmethod
    def tearDownClass(cls):
        if cls.created_workspace:
            cls.storage.rmdir()
            cls.fixture_workspace.rmdir()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=self.storage, prefix='case-')
        self.root = Path(self.temp.name)
        self.repo = self.root/'projects/repo'
        self.repo.mkdir(parents=True)
        git(self.repo,'init','-b','dev')
        git(self.repo,'config','user.name','Synthetic Test')
        git(self.repo,'config','user.email','synthetic@example.invalid')
        (self.repo/'code.txt').write_text('initial\n')
        (self.repo/'.gitignore').write_text('.next/\nlocal-ignored\n')
        git(self.repo,'add','code.txt','.gitignore');git(self.repo,'commit','-m','test: initialize fixture')
        self.work = self.root/'.worktrees/repo/work-001'
        self.work.parent.mkdir(parents=True)
        git(self.repo,'worktree','add','-b','codex/fixture',str(self.work))
        (self.work/'code.txt').write_text('integrated result\n')
        git(self.work,'commit','-am','test: preserve synthetic result')
        git(self.repo,'merge','--ff-only','codex/fixture')
        self.workspace = self.root/'durable-runtime';self.workspace.mkdir()
        self.record = self.workspace/'work.json'
        self.record.write_text(json.dumps({'work_id':'work-001','project':'fixture','unrelated':'preserve-me'}))
        tr.init_record(self.record,self.repo,self.workspace,self.root)
        self.cache = self.work/'.next/cache';self.cache.mkdir(parents=True)
        (self.cache/'generated.pack').write_bytes(b'cache' * 30)
        self.report = self.workspace/'current-qa.md';self.report.write_text('Synthetic current review for integrated canonical source.\n')
        self.capture = self.workspace/'capture.md';self.capture.write_text('Synthetic capture; durable, not in execution environment.\n')
        self.proof = self.workspace/'closure.json'
        self.proof_value = {'schema':1,'kind':'reviewed-task-closure-v1','work_id':'work-001','reviewed_by':'synthetic-coordinator','state':'complete','workers':[],'claims':[],
          'reports':[{'path':str(p),'sha256':tr.digest(p)} for p in [self.report,self.capture]],'dependencies':[],
          'source_roots':[str(self.repo)],'commit':git(self.repo,'rev-parse','HEAD'),'ref':'refs/heads/dev',
          'push_required':False,'remote':None,'remote_ref':None}
        self.proof.write_text(json.dumps(self.proof_value))
        self.observer = patch.object(tr,'observe',return_value={'complete':True,'busy':False,'reason':'synthetic idle observation'})
        self.observer.start()

    def tearDown(self):
        self.observer.stop()
        self.temp.cleanup()

    def args(self, **kwargs):
        result = dict(id='cache',kind='cache',path=self.cache,closure=self.proof,target=self.work)
        result.update(kwargs)
        return argparse.Namespace(**result)

    def register(self, id='cache', kind='cache', path=None):
        return tr.mutate(self.record,'register',self.args(id=id,kind=kind,path=path or self.cache))

    def release(self,id='cache'):
        return tr.mutate(self.record,'release',self.args(id=id))

    def resource(self,id='cache'):
        _,policy=tr.load(self.record)
        return policy,next(r for r in policy['resources'] if r['id']==id)

    def decision(self,id='cache',future=False):
        policy,r=self.resource(id)
        return tr.eligible(policy,r,now=datetime.now(timezone.utc).timestamp()+tr.RETENTION+1 if future else None)

    def rewrite_proof(self):
        self.proof.write_text(json.dumps(self.proof_value))

    def test_cache_then_whole_worktree_and_evidence_survival(self):
        self.register();self.release()
        self.assertTrue(self.decision()['eligible'])
        result=tr.mutate(self.record,'apply',self.args())
        self.assertEqual(result['action'],'deleted');self.assertFalse(self.cache.exists())
        # Empty generated parent dirs are not data; ordinary Git removes them.
        (self.work/'.next').rmdir()
        self.register('tree','worktree',self.work);self.release('tree')
        self.assertFalse(self.decision('tree')['eligible'])
        self.assertTrue(self.decision('tree',future=True)['eligible'])
        future=datetime.now(timezone.utc)+timedelta(days=8)
        class Clock:
            @staticmethod
            def now(tz=None): return future
            fromisoformat=staticmethod(datetime.fromisoformat)
        before={p:tr.digest(p) for p in [self.report,self.capture]}
        with patch.object(tr,'datetime',Clock):
            result=tr.mutate(self.record,'apply',self.args(id='tree'))
        self.assertEqual(result['action'],'deleted');self.assertFalse(self.work.exists())
        self.assertEqual(before,{p:tr.digest(p) for p in before})
        self.assertEqual(git(self.repo,'show','dev:code.txt'),'integrated result')
        tr.read_proof(*self.resource('tree'))
        self.assertEqual(rt.read_json(self.record)['unrelated'],'preserve-me')

    def test_active_resource_retained(self):
        self.register();self.assertFalse(self.decision()['eligible'])

    def test_keep_and_resume(self):
        self.register();self.release();tr.mutate(self.record,'keep',self.args())
        self.assertFalse(self.decision()['eligible'])
        tr.mutate(self.record,'resume',self.args());_,r=self.resource()
        self.assertEqual(r['state'],'active');self.assertIsNone(r['released_at']);self.assertIsNone(r['closure'])

    def test_repeated_release_preserves_retention(self):
        self.register();self.release();_,first=self.resource()
        result=self.release();_,second=self.resource()
        self.assertEqual(first['released_at'],second['released_at']);self.assertEqual(result['status'],'already-released')

    def test_disabled_policy(self):
        self.register();self.release();tr.mutate(self.record,'disable',self.args())
        self.assertFalse(self.decision()['eligible']);self.assertTrue(self.cache.exists())

    def test_busy_observation_denies_release(self):
        self.register()
        with patch.object(tr,'observe',return_value={'complete':True,'busy':True,'reason':'active process'}):
            with self.assertRaises(ValueError):self.release()
        self.assertTrue(self.cache.exists())

    def test_missing_visibility_denies_apply(self):
        self.register();self.release()
        with patch.object(tr,'observe',return_value={'complete':False,'busy':False,'reason':'missing inspector'}):
            self.assertFalse(self.decision()['eligible'])

    def test_current_qa_source_pins_environment(self):
        self.register();self.proof_value['source_roots']=[str(self.work)];self.rewrite_proof()
        with self.assertRaises(ValueError):self.release()

    def test_current_report_reference_pins_resource(self):
        self.register();self.report.write_text(str(self.cache))
        self.proof_value['reports'][0]['sha256']=tr.digest(self.report);self.rewrite_proof()
        with self.assertRaises(ValueError):self.release()

    def test_changed_report_invalidates_cleanup(self):
        self.register();self.release();self.report.write_text('changed')
        self.assertFalse(self.decision()['eligible'])

    def test_changed_proof_invalidates_cleanup(self):
        self.register();self.release();self.proof.write_text('{}')
        self.assertFalse(self.decision()['eligible'])

    def test_worker_unknown_denies_release(self):
        self.register();self.proof_value['workers']=[{'state':'submitted','evidence':'not terminated'}];self.rewrite_proof()
        with self.assertRaises(ValueError):self.release()

    def test_active_claim_denies_release(self):
        self.register();self.proof_value['claims']=[{'state':'active','evidence':'claim'}];self.rewrite_proof()
        with self.assertRaises(ValueError):self.release()

    def test_unconfirmed_push_denies_release(self):
        self.register();self.proof_value.update(push_required=True,remote='missing',remote_ref='refs/heads/main');self.rewrite_proof()
        with self.assertRaises(ValueError):self.release()

    def test_canonical_cache_never_registered(self):
        cache=self.repo/'.next/cache';cache.mkdir(parents=True)
        with self.assertRaises(ValueError):self.register(path=cache)

    def test_only_exact_cache_profile(self):
        with self.assertRaises(ValueError):self.register(path=self.work/'.next')

    def test_cache_symlink_rejected(self):
        (self.cache/'outside').symlink_to(self.report)
        with self.assertRaises(ValueError):self.register()

    def test_hardlinked_cache_rejected(self):
        os.link(self.report,self.cache/'linked.bin')
        with self.assertRaises(ValueError):self.register()

    def test_cache_evidence_rejected(self):
        (self.cache/'qa.md').write_text('important')
        with self.assertRaises(ValueError):self.register()

    def test_secret_in_scratch_rejected(self):
        scratch=self.root/'.tmp/work-001/out';scratch.mkdir(parents=True)
        (scratch/'.env').write_text('synthetic-secret')
        with self.assertRaises(ValueError):self.register('scratch','scratch',scratch)

    def test_scratch_added_file_retained(self):
        scratch=self.root/'.tmp/work-001/out';scratch.mkdir(parents=True)
        (scratch/'build.bin').write_bytes(b'generated')
        self.register('scratch','scratch',scratch);self.release('scratch')
        (scratch/'unique.bin').write_bytes(b'new')
        self.assertFalse(self.decision('scratch')['eligible'])

    def test_directory_replaced_retained(self):
        self.register();self.release();self.cache.rename(self.work/'.next/old')
        self.cache.mkdir()
        self.assertFalse(self.decision()['eligible'])

    def test_ignored_data_retains_tree(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        (self.work/'local-ignored').write_text('unique')
        self.assertFalse(self.decision('tree',future=True)['eligible'])

    def test_untracked_data_retains_tree(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        (self.work/'new.txt').write_text('unique')
        self.assertFalse(self.decision('tree',future=True)['eligible'])

    def test_dirty_source_retains_tree(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        (self.work/'code.txt').write_text('uncommitted')
        self.assertFalse(self.decision('tree',future=True)['eligible'])

    def test_lock_blocks_concurrent_claim(self):
        self.register();policy,_=self.resource()
        with tr.lock(policy):
            with self.assertRaises(BlockingIOError):tr.mutate(self.record,'claim',self.args())

    def test_interrupted_delete_is_not_replayed(self):
        self.register();self.release()
        with patch.object(tr.shutil,'rmtree',side_effect=OSError('simulated interrupt')) as delete:
            delete.avoids_symlink_attacks=True
            with self.assertRaises(OSError):tr.mutate(self.record,'apply',self.args())
        self.assertFalse(self.decision()['eligible']);self.assertEqual(self.resource()[1]['state'],'deleting')
        self.assertTrue(self.cache.exists());self.assertEqual(self.resource()[0]['receipts'][-1]['action'],'delete-intent')

    def test_another_work_record_cannot_adopt_resource(self):
        self.register()
        other=self.workspace/'other.json';other.write_text(json.dumps({'work_id':'other'}))
        tr.init_record(other,self.repo,self.workspace,self.root)
        with self.assertRaises(ValueError):tr.mutate(other,'register',self.args())

    def test_read_only_plan_does_not_mutate_record(self):
        self.register();self.release()
        before=self.record.read_bytes()
        result=subprocess.run([str(SCRIPTS/'manage-task-resources'),'plan','--record',str(self.record)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(before,self.record.read_bytes())

    def test_binding_fresh_process_without_environment(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        env={k:v for k,v in os.environ.items() if not k.startswith('AI_WORKFLOW_')}
        output=subprocess.check_output([sys.executable,str(SCRIPTS/'durable_runtime.py'),'resolve','--target',str(self.work)],env=env,text=True).strip()
        self.assertEqual(output,str(self.workspace))

    def test_binding_conflicting_environment(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        with self.assertRaises(ValueError):rt.resolve(self.work,self.repo)

    def test_missing_binding_blocks_temporary_source(self):
        with self.assertRaises(ValueError):rt.resolve(self.work)

    def test_guard_blocks_output_in_worktree(self):
        with self.assertRaises(ValueError):rt.guard_output(self.work/'qa.md',target=self.work)

    def test_bound_output_requires_persistent_runtime(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        rt.guard_output(self.workspace/'new-qa.md',target=self.work)
        with self.assertRaises(ValueError):rt.guard_output(self.root/'elsewhere-qa.md',target=self.work)

    def test_legacy_read_only(self):
        old=self.workspace/'legacy.json';old.write_text('{"work_id":"legacy"}')
        result=subprocess.run([str(SCRIPTS/'manage-task-resources'),'inspect','--record',str(old)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0);self.assertIn('legacy-inspect-only',result.stdout)
        self.assertEqual(old.read_text(),'{"work_id":"legacy"}')

    def test_cli_mutation_requires_explicit_scope_flag(self):
        result=subprocess.run([str(SCRIPTS/'manage-task-resources'),'disable','--record',str(self.record)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertTrue(self.resource_policy()['enabled'])

    def resource_policy(self): return tr.load(self.record)[1]

    def test_real_linux_observer_detects_open_file(self):
        # Actual /proc walk (no mutation/mock); elevated visibility only if available.
        helper=SCRIPTS/'lib/task-resource-activity.py'
        handle=(self.cache/'generated.pack').open('rb')
        try:
            raw=subprocess.check_output([sys.executable,str(helper),str(self.cache)])
            value=json.loads(raw)
            # Unprivileged /proc denial is a valid conservative result, never eligible.
            self.assertTrue(value['busy'] or not value['complete'])
        finally:handle.close()

    def test_nested_git_retains_tree(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        nested=self.work/'nested';nested.mkdir();git(nested,'init')
        self.assertFalse(self.decision('tree',future=True)['eligible'])

    def test_tracked_cache_cannot_be_deleted(self):
        git(self.work,'add','-f','.next/cache/generated.pack')
        self.register();self.release()
        self.assertFalse(self.decision()['eligible'])

    def test_changed_canonical_identity_blocks_loading(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        value=rt.read_json(rt.binding_path(self.work));value['source']['git_common']+='-different'
        rt.binding_path(self.work).write_text(json.dumps(value))
        with self.assertRaises(ValueError):rt.resolve(self.work)

    def test_unknown_binding_version_blocks_loading(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        path=rt.binding_path(self.work);value=rt.read_json(path);value['schema']=9;path.write_text(json.dumps(value))
        with self.assertRaises(ValueError):rt.resolve(self.work)

    def test_bound_timing_output_in_durable_runtime(self):
        rt.bind(self.work,self.repo,self.workspace,self.record)
        env={k:v for k,v in os.environ.items() if not k.startswith('AI_WORKFLOW_')}
        output=self.workspace/'timing.tsv'
        result=subprocess.run([sys.executable,str(SCRIPTS/'lib/validation-timing.py'),'init',str(output)],cwd=self.work,env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(output.exists())
        blocked=self.work/'bad-timing.tsv'
        result=subprocess.run([sys.executable,str(SCRIPTS/'lib/validation-timing.py'),'init',str(blocked)],cwd=self.work,env=env,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertFalse(blocked.exists())

    def test_bootstrap_bound_runtime_roundtrip(self):
        # A completely local producer snapshot, no network or user installation mutation.
        origin=self.root/'workflow-origin';origin.mkdir()
        producer=SCRIPTS.parents[1]
        for name in ['.systems','AGENTS.md','HUMANS.md','README.md','.gitignore']:
            src=producer/name;dest=origin/name
            if src.is_dir():shutil.copytree(src,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            else:shutil.copyfile(src,dest)
        git(origin,'init','-b','main');git(origin,'config','user.name','Synthetic Test');git(origin,'config','user.email','synthetic@example.invalid')
        git(origin,'add','.systems','AGENTS.md','HUMANS.md','README.md','.gitignore');git(origin,'commit','-m','test: local workflow producer')
        marker=self.work/'workflow-marker';marker.write_text('Owner-accepted Workflow installation marker for synthetic test.')
        env={k:v for k,v in os.environ.items() if not k.startswith('AI_WORKFLOW_')}
        env.update(AI_WORKFLOW_BOOTSTRAP_TEST_MODE='1',AI_WORKFLOW_BOOTSTRAP_REMOTE=str(origin),TMPDIR=str(self.root))
        result=subprocess.run([str(SCRIPTS/'bootstrap-target-worktree'),'--target',str(self.work),'--approved','--accepted-marker','workflow-marker','--durable-workspace',str(self.workspace),'--canonical-target',str(self.repo),'--work-record',str(self.record)],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue((self.workspace/'repo/core/init.md').is_file())
        self.assertFalse((self.work/'ai-workflow-workspace').exists())
        env={k:v for k,v in env.items() if not k.startswith('AI_WORKFLOW_')}
        resolved=subprocess.check_output([str(self.work/'ai-workflow/.systems/scripts/resolve-workflow-env')],env=env,text=True)
        self.assertIn('AI_WORKFLOW_WORKSPACE_HOME='+str(self.workspace),resolved)
        nested = self.work/'ai-workflow'
        self.assertEqual(rt.execution_target(nested), self.work)
        rt.guard_output(self.workspace/'new-quality.md',target=nested,workspace=self.workspace)
        with self.assertRaises(ValueError):
            rt.guard_output(self.work/'bad-quality.md',target=nested,workspace=self.workspace)

    def test_repo_stop_marker_covers_other_loaded_records(self):
        self.register();self.release();policy,resource=self.resource()
        tr.mutate(self.record,'disable',self.args())
        # Even a caller that loaded another enabled record before disable sees the repo stop.
        self.assertFalse(tr.eligible(policy,resource)['eligible'])

    def test_locked_git_worktree_retained(self):
        self.register();self.release();git(self.repo,'worktree','lock',str(self.work))
        self.assertFalse(self.decision()['eligible'])

    def test_active_parent_resource_pins_cache(self):
        self.register();self.register('tree','worktree',self.work);self.release()
        self.assertFalse(self.decision()['eligible'])
        self.release('tree');self.assertTrue(self.decision()['eligible'])
        tr.mutate(self.record,'keep',self.args(id='tree'))
        self.assertFalse(self.decision()['eligible'])

    def test_plan_does_not_refresh_git_index(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        index=Path(git(self.work,'rev-parse','--path-format=absolute','--git-path','index'))
        before=index.read_bytes()
        file=self.work/'code.txt';info=file.stat();os.utime(file,ns=(info.st_atime_ns,info.st_mtime_ns+10000000))
        self.assertTrue(self.decision('tree',future=True)['eligible'])
        self.assertEqual(before,index.read_bytes())

    def test_os_temporary_storage_not_durable(self):
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(ValueError):rt.durable(raw)

    def test_remote_branch_advance_preserves_confirmed_push(self):
        remote=self.root/'remote.git';remote.mkdir();git(remote,'init','--bare')
        git(self.repo,'remote','add','synthetic',str(remote));git(self.repo,'push','synthetic','dev:main')
        self.register();self.proof_value.update(push_required=True,remote='synthetic',remote_ref='refs/heads/main');self.rewrite_proof();self.release()
        (self.repo/'later.txt').write_text('later independent task')
        git(self.repo,'add','later.txt');git(self.repo,'commit','-m','test: later result');git(self.repo,'push','synthetic','dev:main')
        self.assertTrue(self.decision()['eligible'])

    def test_executor_cannot_remove_its_own_environment(self):
        shutil.rmtree(self.work/'.next')
        self.register('tree','worktree',self.work);self.release('tree')
        with patch.object(tr,'HERE',self.work/'ai-workflow/.systems/scripts'):
            self.assertFalse(self.decision('tree',future=True)['eligible'])

    def test_binding_preview_is_read_only(self):
        path=rt.binding_path(self.work)
        value=rt.bind(self.work,self.repo,self.workspace,self.record,dry_run=True)
        self.assertEqual(value['workspace'],str(self.workspace))
        self.assertFalse(path.exists())

    def test_archival_run_provenance_does_not_pin_old_location(self):
        archive=self.workspace/'old-run.json';archive.write_text(json.dumps({'historical_location':str(self.cache)}))
        self.proof_value['dependencies']=[{'path':str(archive),'sha256':tr.digest(archive),'role':'archive'}];self.rewrite_proof()
        before=archive.read_bytes();self.register();self.release()
        self.assertTrue(self.decision()['eligible'])
        self.assertEqual(tr.mutate(self.record,'apply',self.args())['action'],'deleted')
        self.assertEqual(before,archive.read_bytes())

    def test_archive_role_never_overrides_live_source_pin(self):
        archive=self.workspace/'old-run.json';archive.write_text('provenance')
        self.proof_value['dependencies']=[{'path':str(archive),'sha256':tr.digest(archive),'role':'archive'}]
        self.proof_value['source_roots']=[str(self.work)];self.rewrite_proof();self.register()
        with self.assertRaises(ValueError):self.release()

    def test_current_reports_cannot_be_relabelled_archive(self):
        self.proof_value['reports'][0]['role']='archive';self.rewrite_proof();self.register()
        with self.assertRaises(ValueError):self.release()

    def test_discovery_only_reads_registered_owning_records(self):
        self.register();before=self.record.read_bytes()
        result=tr.discover(self.repo,self.workspace)
        self.assertEqual(result['records'],[{'record':str(self.record),'work_id':'work-001'}])
        self.assertEqual(before,self.record.read_bytes())

    def test_empty_discovery_creates_nothing(self):
        common=Path(git(self.repo,'rev-parse','--path-format=absolute','--git-common-dir'))
        self.assertEqual(tr.discover(self.repo,self.workspace)['records'],[])
        self.assertFalse((common/'task-resource-owners').exists())

    def test_foreign_discovery_pointer_not_read(self):
        common=Path(git(self.repo,'rev-parse','--path-format=absolute','--git-common-dir'))
        pointers=common/'task-resource-owners';pointers.mkdir()
        foreign=self.root/'foreign.json';foreign.write_text('private synthetic namespace')
        (pointers/'foreign.json').write_text(json.dumps({'path':str(self.cache),'record':str(foreign),'id':'cache'}))
        read=rt.read_json
        def guarded(path):
            if Path(path)==foreign:raise AssertionError('foreign namespace was read')
            return read(path)
        with patch.object(rt,'read_json',side_effect=guarded):result=tr.discover(self.repo,self.workspace)
        self.assertEqual(result['records'],[]);self.assertEqual(len(result['retained']),1)


if __name__=='__main__':
    unittest.main(verbosity=2)
