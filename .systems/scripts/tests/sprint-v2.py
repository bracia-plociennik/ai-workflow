#!/usr/bin/env python3
"""Synthetic behavior evidence: targeted results are never formal full QA."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('legacy_fixture',HERE/'sprint-iteration.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
import sprint_iteration as sprint
import sprint_v2 as v2


class DefaultSprint(unittest.TestCase):
    def setUp(self):
        fixture.Sprint.setUp(self)
        self.args.schema=2;self.args.command=[];self.args.result=None
    def tearDown(self):fixture.Sprint.tearDown(self)
    call=fixture.Sprint.call
    start_preview=fixture.Sprint.start_preview
    accept=fixture.Sprint.accept
    def stored(self):return json.loads(self.record.read_text())['sprint_iteration']
    def report(self):
        folder=self.owner/'reviews';folder.mkdir(exist_ok=True)
        p=folder/'targeted.md';p.write_text('Reviewed fixture select(): current behavior matches accepted scope. No full QA claimed.\n')
        return p
    def finish(self,result='passed'):
        return self.call('complete-targeted',result=result,report=self.report())

    def test_default_cli_and_three_visual_rounds(self):
        args=[str(fixture.SCRIPTS/'manage-sprint'),'start','--record',str(self.record),'--approved','--expected-revision','-1','--source',str(self.repo),'--project','fixture','--task','SP-001','--scope','src']
        subprocess.run(args,check=True,capture_output=True)
        self.assertEqual(self.stored()['schema'],2)
        for i in range(3):
            (self.code/'page.html').write_text('<button>'+str(i)+'</button>')
            self.assertEqual(self.call('preview',preview_id='p'+str(i))['state'],'iterating')
        result=self.accept();self.assertEqual(result['state'],'targeted');self.assertFalse(result['full_verification_requested'])

    def test_targeted_is_continuation_not_full_quality(self):
        self.start_preview();self.accept();view=self.finish()
        self.assertTrue(view['continuation_allowed']);self.assertFalse(view['closure_allowed'])
        self.assertTrue(sprint.progress(self.ws,'fixture',self.args.workflow_root)['continuation_ready'])
        with self.assertRaises(ValueError):sprint.guard_record(self.record,self.args.workflow_root)
        with self.assertRaises(ValueError):self.call('complete',report=self.report())
        with self.assertRaises(ValueError):sprint.project_guard(self.ws,'fixture',self.args.workflow_root,generating=True,task='SP-001')

    def test_request_full_requires_actual_explicit_intent(self):
        self.start_preview();self.accept();self.finish()
        with self.assertRaises(ValueError):self.call('request-full-verification',message='Podoba mi się, to finalna wersja')
        with self.assertRaises(ValueError):self.call('request-full-verification',message='Uruchom Phase 8',origin='worker')
        view=self.call('request-full-verification',message='Uruchom Phase 8',origin='owner')
        self.assertEqual(view['state'],'verifying')
        sprint.project_guard(self.ws,'fixture',self.args.workflow_root,generating=True,task='SP-001')
        with self.assertRaises(ValueError):self.call('complete',report=self.report())

    def test_real_full_qa_consumer_closes_only_after_explicit_request(self):
        self.start_preview();self.accept();self.finish()
        self.call('request-full-verification',message='Uruchom Phase 8')
        report=fixture.Sprint.make_quality(self)
        self.assertTrue(self.call('complete',report=report)['closure_allowed'])
        sprint.guard_record(self.record,self.args.workflow_root)
        report.write_text(report.read_text()+'\nChanged report.\n')
        self.assertFalse(sprint.inspect(self.record,self.args.workflow_root)['closure_allowed'])

    def test_persistent_budget_pause_resume_and_subprocess(self):
        self.start_preview();self.accept();start=self.stored()['cycles'][0]['started_at']
        self.call('pause');view=self.call('resume');self.assertEqual(view['state'],'targeted')
        output=subprocess.check_output([str(fixture.SCRIPTS/'manage-sprint'),'inspect','--record',str(self.record)],text=True)
        self.assertEqual(json.loads(output)['state'],'targeted')
        self.assertEqual(start,self.stored()['cycles'][0]['started_at'])

    def test_identical_fingerprint_does_not_renew_budget(self):
        self.start_preview();self.accept();self.finish()
        self.call('preview',preview_id='another-id')
        with self.assertRaises(ValueError):self.accept()
        self.assertEqual(len(self.stored()['cycles']),1)

    def test_changed_reaccepted_effect_can_start_new_cycle(self):
        self.start_preview();self.accept();self.finish()
        (self.code/'app.py').write_text('def select(items): return list(items)\n')
        self.call('preview',preview_id='new-effect');self.accept()
        self.assertEqual(len(self.stored()['cycles']),2)

    def test_timeout_logs_failure_and_keeps_original_source(self):
        self.start_preview();self.accept();source=(self.code/'app.py').read_bytes()
        with patch.object(v2,'remaining',return_value=.1):
            self.call('qa-run',command=[sys.executable,'-c','import time; print("started",flush=True); time.sleep(2)'])
        check=self.stored()['cycles'][-1]['checks'][-1]
        self.assertTrue(check['timed_out']);self.assertEqual(check['exit_code'],124)
        self.assertIn('started',Path(check['log']).read_text())
        with self.assertRaises(ValueError):self.finish('passed')
        self.finish('incomplete');self.assertEqual(source,(self.code/'app.py').read_bytes())

    def test_interrupted_launch_keeps_attempt_and_prevents_pass_or_duplicate(self):
        self.start_preview();self.accept()
        original=v2.subprocess.Popen
        def interrupt(argv,*args,**kwargs):
            if str(argv[0]).endswith('/timeout'):raise OSError('synthetic interruption')
            return original(argv,*args,**kwargs)
        with patch.object(v2.subprocess,'Popen',side_effect=interrupt):
            with self.assertRaises(OSError):self.call('qa-run',command=[sys.executable,'-c','pass'])
        self.assertEqual(self.stored()['cycles'][-1]['checks'][-1]['exit_code'],125)
        with self.assertRaises(ValueError):self.finish('passed')
        with self.assertRaises(ValueError):self.call('qa-run',command=[sys.executable,'-c','pass'])
        self.finish('incomplete')

    def test_exhaustion_not_pass_or_retry(self):
        self.start_preview();self.accept()
        with patch.object(v2,'now',return_value=time.time()+301):
            with self.assertRaises(ValueError):self.call('qa-run',command=[sys.executable,'-c','pass'])
            with self.assertRaises(ValueError):self.finish('passed')
            self.assertEqual(self.finish('incomplete')['targeted_result'],'incomplete')

    def test_negative_exit_cannot_be_pass(self):
        self.start_preview();self.accept()
        self.call('qa-run',command=[sys.executable,'-c','raise SystemExit(7)'])
        with self.assertRaises(ValueError):self.finish()
        self.assertFalse(self.finish('failed')['continuation_allowed'])

    def test_report_and_source_change_invalidates_confidence(self):
        self.start_preview();self.accept();self.finish();self.report().write_text('changed report')
        self.assertFalse(sprint.inspect(self.record,self.args.workflow_root)['continuation_allowed'])
        (self.code/'app.py').write_text('changed code')
        self.assertEqual(sprint.inspect(self.record,self.args.workflow_root)['state'],'iterating')

    def test_cas_stale_revision_has_no_write(self):
        self.start_preview();self.accept();before=self.record.read_bytes()
        self.args.expected_revision=-1
        with self.assertRaises(ValueError):sprint.mutate(self.record,'pause',self.args)
        self.assertEqual(before,self.record.read_bytes())

    def test_foreign_report_and_backwards_clock_rejected(self):
        self.start_preview();self.accept()
        outside=self.root/'foreign.md';outside.write_text('not owning evidence')
        with self.assertRaises(ValueError):self.call('complete-targeted',result='passed',report=outside)
        with patch.object(v2,'now',return_value=self.stored()['cycles'][0]['started_at']-1):
            with self.assertRaises(ValueError):sprint.inspect(self.record,self.args.workflow_root)

    def test_explicit_targeted_backend_request(self):
        self.start_preview();view=self.call('request-verification',message='Testuj teraz')
        self.assertEqual(view['state'],'targeted')
        self.call('qa-run',command=[sys.executable,'-c','assert sum([1,2])==3'])
        self.assertEqual(self.finish()['state'],'targeted-checked')


if __name__=='__main__':unittest.main()
