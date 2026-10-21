"""Real updater argument routing and actual validator scope/child isolation."""
from pathlib import Path
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('guard_fixture_helpers',SCRIPTS/'tests/test_validation_input_guard.py')
fixtures=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixtures)

class UpdateScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='update-scope-test-');self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.target=self.base/'target';self.clone=self.target/'ai-workflow';self.clone.mkdir(parents=True)
        self.scripts=self.clone/'.systems/scripts';self.scripts.mkdir(parents=True)
        shutil.copy2(SCRIPTS/'update-from-upstream',self.scripts/'update-from-upstream')
        validator=self.scripts/'validate-workflow';validator.write_text('#!/bin/sh\nprintf "FAKE_VALIDATOR args=%s scope=%s\\n" "$*" "${AI_WORKFLOW_VALIDATION_PROJECT:-all}"\n');validator.chmod(0o755)
        (self.clone/'README.md').write_text('Synthetic tool source\n')
        subprocess.run(['git','init','-q','--bare',str(self.base/'remote.git')],check=True)
        self.git('init','-q','-b','main');self.git('config','user.name','Synthetic');self.git('config','user.email','synthetic@example.invalid');self.git('add','.');self.git('commit','-qm','synthetic');self.git('remote','add','origin',str(self.base/'remote.git'));self.git('push','-qu','origin','main')
        self.workspace=self.target/'ai-workflow-workspace';self.selected=self.workspace/'projects/selected';self.selected.mkdir(parents=True);(self.selected/'status.md').write_text('synthetic immutable runtime\n')
        self.env={k:v for k,v in os.environ.items() if not k.startswith(('AI_WORKFLOW_','AI_SYSTEM_','TARGET_REPO_ROOT','TASK_RESOURCE_'))}
    def git(self,*args):return subprocess.run(['git','-C',str(self.clone),*args],check=True,capture_output=True)
    def run_update(self,*args,env=None):
        before=(self.selected/'status.md').read_bytes();head=self.git('rev-parse','HEAD').stdout
        r=subprocess.run([str(self.scripts/'update-from-upstream'),*args],cwd=self.clone,env=env or self.env,capture_output=True,text=True,timeout=30)
        self.assertEqual(before,(self.selected/'status.md').read_bytes());self.assertEqual(head,self.git('rev-parse','HEAD').stdout)
        return r
    def test_explicit_project_preserves_full_validator_arguments(self):
        r=self.run_update('--validation-project','selected');self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('FAKE_VALIDATOR args=--profile full --progress summary scope=selected',r.stdout)
        self.assertIn('AI_WORKFLOW_UPDATE_VALIDATION_SCOPE runtime_project=selected product=all',r.stdout)
        self.assertIn('AI_WORKFLOW_UPDATE_COMPLETE result=pass',r.stdout)
    def test_default_remains_global(self):
        r=self.run_update();self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('scope=all',r.stdout)
    def test_invalid_and_missing_scope_reject_without_validation(self):
        for value in ['../selected','missing']:
            with self.subTest(value=value):
                r=self.run_update('--validation-project',value);self.assertEqual(r.returncode,2,r.stdout+r.stderr);self.assertNotIn('FAKE_VALIDATOR',r.stdout)
    def test_explicit_environment_selection_and_cli_precedence(self):
        env={**self.env,'AI_WORKFLOW_VALIDATION_PROJECT':'missing'}
        r=self.run_update('--validation-project','selected',env=env);self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('scope=selected',r.stdout)
    def test_real_validator_consumes_selection_before_children(self):
        helper=fixtures.GuardTests();helper.setUp();self.addCleanup(helper.doCleanups)
        args,env=helper.install_runner_fixture();args=args[:-2]  # Remove explicit --project; this tests the documented bridge.
        env['AI_WORKFLOW_VALIDATION_PROJECT']='selected'
        hook=helper.scripts/'check-required-artifacts';s=hook.read_text().replace('import os,time\n','import os,time\nassert "AI_WORKFLOW_VALIDATION_PROJECT" not in os.environ, "scope leaked into child"\n');hook.write_text(s)
        (helper.base/'go').touch()
        r=subprocess.run(args,cwd=helper.repo,env=env,capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('AI_WORKFLOW_VALIDATION_SCOPE runtime_project=selected product=all',r.stdout)

if __name__=='__main__':unittest.main()
