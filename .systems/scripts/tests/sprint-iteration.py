#!/usr/bin/env python3
"""Public Sprint behavior on disposable synthetic projects; never real owner approval."""
import argparse
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

SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
import durable_runtime as rt
import sprint_iteration as sprint
import task_resource_cleanup as cleanup


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE,text=True).strip()


def storage():
    bound=rt.load(SCRIPTS.parents[1])
    explicit=os.environ.get('SPRINT_TEST_STORAGE') or os.environ.get('TASK_RESOURCE_TEST_STORAGE')
    root=Path(explicit) if explicit else (Path(bound['workspace']) if bound else SCRIPTS.parents[1]/'ai-workflow-workspace')
    root.mkdir(parents=True,exist_ok=True);rt.durable(root)
    folder=root/'projects/sprint-iteration-v1/evidence/synthetic-fixtures' if (root/'projects/sprint-iteration-v1').is_dir() else root/'.sprint-fixtures'
    folder.mkdir(parents=True,exist_ok=True)
    return folder


class Sprint(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=storage(),prefix='sprint-')
        self.root=Path(self.temp.name);self.repo=self.root/'projects/app';self.repo.mkdir(parents=True)
        git(self.repo,'init','-b','dev');git(self.repo,'config','user.name','Synthetic Test');git(self.repo,'config','user.email','synthetic@example.invalid')
        self.code=self.repo/'src';self.code.mkdir();(self.code/'app.py').write_text('def select(items):\n    return items\n')
        git(self.repo,'add','src');git(self.repo,'commit','-m','test: initialize fixture')
        self.ws=self.root/'runtime';self.owner=self.ws/'projects/fixture';self.owner.mkdir(parents=True)
        self.record=self.owner/'work-record.json';self.record.write_text(json.dumps({'work_id':'fixture-work','project':'fixture','unrelated':'keep'}))
        cleanup.init_record(self.record,self.repo,self.ws,self.root)
        self.args=argparse.Namespace(source=self.repo,project='fixture',task='SP-001',scope=['src'],environment='dev-test',production_approval=None,
          expected_revision=-1,reference='synthetic preview',preview_id='p1',message=None,origin='owner',owner_reference='synthetic test conversation',
          report=None,workflow_root=SCRIPTS.parents[1],correction_review=None)

    def tearDown(self):self.temp.cleanup()

    def call(self,action,**kw):
        v=json.loads(self.record.read_text());self.args.expected_revision=v.get('sprint_iteration',{}).get('revision',-1)
        for k,val in kw.items():setattr(self.args,k,val)
        return sprint.mutate(self.record,action,self.args)

    def start_preview(self):self.call('start');return self.call('preview')
    def accept(self):return self.call('accept',message='Podoba mi się, to finalna wersja')

    def test_three_frontend_rounds_defer_until_final_acceptance(self):
        self.call('start')
        calls=[]
        for n in range(3):
            (self.code/'page.html').write_text('<button style="padding:'+str(n+1)+'px">Preview</button>')
            view=self.call('preview',preview_id='p'+str(n))
            self.assertEqual(view['checks'],[]);self.assertTrue(view['deferred']);self.assertFalse(view['closure_allowed'])
            calls.append('preview')
        self.assertEqual(calls,['preview']*3)
        view=self.accept();self.assertEqual(view['state'],'verifying');self.assertIn('tests',view['checks'])
        self.assertFalse(view['closure_allowed'])

    def test_backend_deferred_edge_bug_then_internal_fix(self):
        self.call('start')
        for n in range(3):
            (self.code/'app.py').write_text('def select(items):\n    return items[0]\n# round '+str(n)+'\n')
            self.call('preview',preview_id='p'+str(n))
        self.accept()
        namespace={};exec((self.code/'app.py').read_text(),namespace)
        with self.assertRaises(IndexError):namespace['select']([])
        (self.code/'app.py').write_text('def select(items):\n    return items[0] if items else None\n')
        self.assertEqual(sprint.inspect(self.record)['state'],'iterating')
        review=self.owner/'reviews/internal-fix.md';review.parent.mkdir();review.write_text('Synthetic semantic review: empty list correction preserves accepted selection behavior and original scope; no visible effect change.')
        view=self.call('refresh-verification',correction_review=review)
        self.assertEqual(view['state'],'verifying')
        namespace={};exec((self.code/'app.py').read_text(),namespace);self.assertIsNone(namespace['select']([]));self.assertEqual(namespace['select']([7]),7)
        self.assertEqual(json.loads(self.record.read_text())['sprint_iteration']['verification_request']['preview_id'],'p2')

    def test_partial_quotes_silence_and_foreign_origins_do_not_accept(self):
        self.start_preview();before=self.record.read_bytes()
        for message in ['Ładnie, ale jeszcze popraw przycisk','Podoba mi się','Działa','', '"Podoba mi się, to finalna wersja"','Nie, to finalna wersja','Działa, tak zostawiamy, ale jeszcze zmień API']:
            self.assertEqual(sprint.classify(message,'owner'),'continue')
            with self.assertRaises(ValueError):self.call('accept',message=message)
        for origin in ['source','worker']:
            with self.assertRaises(ValueError):self.call('accept',message='Działa, tak zostawiamy',origin=origin)
        self.assertEqual(before,self.record.read_bytes())

    def test_explicit_test_without_effect_acceptance(self):
        self.start_preview();v=self.call('request-verification',message='Testuj teraz');self.assertEqual(v['state'],'verifying')
        self.assertEqual(json.loads(self.record.read_text())['sprint_iteration']['verification_request']['kind'],'verify')

    def test_stale_or_wrong_preview_rejects_without_write(self):
        self.start_preview();before=self.record.read_bytes()
        with self.assertRaises(ValueError):self.call('accept',message='Działa, tak zostawiamy',preview_id='old')
        (self.code/'app.py').write_text('changed')
        with self.assertRaises(ValueError):self.call('accept',message='Działa, tak zostawiamy',preview_id='p1')
        self.assertEqual(before,self.record.read_bytes())

    def test_pause_resume_and_new_process_preserve_deferred(self):
        self.start_preview();self.call('pause');before=self.record.read_bytes()
        out=subprocess.check_output([str(SCRIPTS/'manage-sprint'),'inspect','--record',str(self.record)],text=True)
        self.assertEqual(json.loads(out)['state'],'paused');self.assertEqual(before,self.record.read_bytes())
        self.assertTrue(self.call('resume')['deferred']);self.assertEqual(json.loads(self.record.read_text())['unrelated'],'keep')

    def test_pending_pins_cleanup_including_spoofed_release(self):
        self.start_preview()
        for action in ['iterating','paused','verifying']:
            if action=='paused':self.call('pause')
            if action=='verifying':self.call('resume');self.accept()
            with self.assertRaises(ValueError):sprint.guard_record(self.record,self.args.workflow_root)
            args=argparse.Namespace(id='unknown',closure=None)
            with self.assertRaisesRegex(ValueError,'Sprint'):cleanup.mutate(self.record,'release',args)
            with self.assertRaisesRegex(ValueError,'Sprint'):cleanup.mutate(self.record,'apply',args)

    def test_current_qa_producer_rejects_before_acceptance(self):
        self.start_preview()
        with self.assertRaisesRegex(ValueError,'deferred'):sprint.project_guard(self.ws,'fixture',self.args.workflow_root,generating=True,task='SP-001')
        self.accept();sprint.project_guard(self.ws,'fixture',self.args.workflow_root,generating=True,task='SP-001')

    def make_quality(self):
        spec=importlib.util.spec_from_file_location('fixture_quality',SCRIPTS/'lib/quality-record.py')
        producer=importlib.util.module_from_spec(spec);spec.loader.exec_module(producer)
        template=(SCRIPTS.parents[1]/'.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md').read_text()
        _,sections=producer.qa.read_current(template.splitlines())
        sections={key:'\n'.join(value) for key,value in sections.items() if key!='Input Artifacts'}
        sections['Evidence']='Synthetic test assessment only: exercising strict actual QA consumer, not real product acceptance.'
        (self.owner/'spec.md').write_text('Synthetic fixture accepted selection scope.')
        rec={'schema':1,'kind':'implementation-quality','task':'SP-001','run_id':'synthetic-sprint-quality','verdict':'PASS','date':'2026-10-20',
             'inputs':[{'root':'owning-project-evidence','path':'spec.md'}], 'sections':sections}
        (self.owner/'quality').mkdir(exist_ok=True)
        # A smoke dispatcher's public product copy can be Gitless. Assess the actual
        # fixture Git source; the real installed parser below still verifies the result.
        out,body=producer.render(rec,self.repo,self.ws,'fixture')
        producer.qa.assess(out,SCRIPTS.parents[1],self.ws,'fixture',self.repo,document=body,require_pass=True)
        producer.publish(out,body)
        return out

    def test_real_current_qa_consumer_allows_verified_then_invalidates(self):
        self.start_preview();self.accept();report=self.make_quality()
        self.assertTrue(self.call('complete',report=report)['closure_allowed'])
        sprint.guard_record(self.record,SCRIPTS.parents[1])
        report.write_text(report.read_text()+'\nChanged report.\n')
        self.assertFalse(sprint.inspect(self.record,SCRIPTS.parents[1])['closure_allowed'])
        with self.assertRaises(ValueError):sprint.guard_record(self.record,SCRIPTS.parents[1])

    def test_actual_quality_producer_does_not_publish_prematurely(self):
        self.start_preview();before=self.record.read_bytes()
        with self.assertRaisesRegex(ValueError,'deferred'):self.make_quality()
        self.assertFalse((self.owner/'quality/phase-5-sp-001-quality.md').exists())
        self.assertEqual(before,self.record.read_bytes())

    def test_missing_report_no_complete(self):
        self.start_preview();self.accept();before=self.record.read_bytes()
        with self.assertRaises((ValueError,TypeError)):self.call('complete',report=self.owner/'missing.md')
        self.assertEqual(before,self.record.read_bytes())

    def test_no_sprint_legacy_behavior(self):
        before=self.record.read_bytes();v=sprint.inspect(self.record)
        self.assertEqual(v['state'],'inactive');self.assertTrue(v['closure_allowed']);self.assertEqual(before,self.record.read_bytes())

    def test_production_needs_exact_separate_record(self):
        before=self.record.read_bytes()
        with self.assertRaises(ValueError):self.call('start',environment='production')
        self.assertEqual(before,self.record.read_bytes())
        approval=self.owner/'production-reference.json';approval.write_text(json.dumps({'target':'synthetic-only','scope':'preview styling','rollback':'synthetic previous ref','owner_reference':'synthetic fixture, not actual deployment permission'}))
        self.call('start',production_approval=approval);self.assertFalse(sprint.inspect(self.record)['closure_allowed'])

    def test_unknown_version_field_and_forged_verified_reject(self):
        self.start_preview();original=json.loads(self.record.read_text())
        for change in [{'schema':2},{'schema':True},{'unexpected':True},{'state':'verified'}]:
            data=json.loads(json.dumps(original));data['sprint_iteration'].update(change);self.record.write_text(json.dumps(data))
            with self.assertRaises(ValueError):sprint.inspect(self.record)
        self.record.write_text(json.dumps(original))

    def test_revision_compare_and_lock_contention(self):
        self.start_preview();before=self.record.read_bytes();self.args.expected_revision=999
        with self.assertRaises(ValueError):sprint.mutate(self.record,'pause',self.args)
        self.assertEqual(before,self.record.read_bytes())
        _,policy,_=sprint.read(self.record)
        with cleanup.lock(policy):
            with self.assertRaises(BlockingIOError):self.call('pause')
        self.assertEqual(before,self.record.read_bytes())

    def test_source_modes_membership_and_deletion_detected(self):
        self.start_preview();old=sprint.read(self.record)[2]['preview']['digest']
        added=self.code/'new.py';added.write_text('new')
        self.assertNotEqual(old,sprint.population(sprint.read(self.record)[2]));added.unlink()
        self.assertEqual(old,sprint.population(sprint.read(self.record)[2]))
        (self.code/'app.py').chmod(0o755);self.assertNotEqual(old,sprint.population(sprint.read(self.record)[2]))

    def test_unsafe_scopes_do_not_write(self):
        before=self.record.read_bytes()
        for scope in [['../src'],['/tmp'],['src','src/app.py'],['src','src'],['.git'],['src//app.py']]:
            with self.assertRaises(ValueError):self.call('start',scope=scope)
            self.assertEqual(before,self.record.read_bytes())

    def test_link_and_secret_scope_rejected(self):
        (self.code/'linked').symlink_to(self.root)
        with self.assertRaises(ValueError):self.call('start')
        (self.code/'linked').unlink();(self.code/'.env').write_text('synthetic canary')
        with self.assertRaises(ValueError):self.call('start')

    def test_unknown_check_set_rejected(self):
        self.start_preview();v=json.loads(self.record.read_text());v['sprint_iteration']['deferred_checks']=[];self.record.write_text(json.dumps(v))
        with self.assertRaises(ValueError):sprint.inspect(self.record)

    def test_cli_mutations_need_approval_and_are_read_only_on_failure(self):
        before=self.record.read_bytes()
        out=subprocess.run([str(SCRIPTS/'manage-sprint'),'start','--record',str(self.record)],capture_output=True)
        self.assertNotEqual(out.returncode,0);self.assertEqual(before,self.record.read_bytes())


if __name__=='__main__':unittest.main()
