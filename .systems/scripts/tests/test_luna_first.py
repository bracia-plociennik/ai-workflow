#!/usr/bin/env python3
"""Behavioral routing tests; synthetic ownership/handles, not native proof."""
import copy,importlib.util,json,sys,tempfile,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import luna_first as m

class Routing(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.target=self.root/'source';self.target.mkdir();(self.target/'a.py').write_text('before\n')
  self.owner=self.root/'runtime/projects/demo';self.owner.mkdir(parents=True);self.record=self.owner/'work.json';self.record.write_text(json.dumps({'unrelated':{'preserve':True}}));self.proof=self.owner/'review.md';self.proof.write_text('Synthetic QA feedback, no native approval.')
  self.r={'schema':1,'project':'demo','task':'T-001','target_root':str(self.target),'inputs':['a.py'],'goal':'Correct one deterministic behavior','mode':'implementation','risk':'low','clear':True,'bounded':True,'reversible':True,'dod':['Exact output'],'checks':['Known input/expected output'],'concerns':[],'ready':{'input':True,'access':True,'permission':True},'owner_reference':'synthetic-fixture-only'}
 def call(self,op,**kw):
  if op!='start':kw.setdefault('revision',m.read(self.record)['model_routing']['revision'])
  return m.transition(self.record,op,**kw)
 def start(self):return self.call('start',request=self.r)
 def active(self,handle='native-fixture-1'):
  self.call('reserve');self.call('bind',handle=handle)
 def finish(self,outcome='qa-failed',handle='native-fixture-1',model=m.LUNA):return self.call('finish',handle=handle,outcome=outcome,evidence=self.proof,actual_model=model,terminated=True)
 def test_clear_selects_luna(self):self.assertEqual(m.choose(self.r)['model'],m.LUNA)
 def test_high_risk_strong(self):self.r['risk']='high';self.assertEqual(m.choose(self.r)['model'],m.SOL)
 def test_architecture_strong(self):self.r['concerns']=['architecture'];self.assertEqual(m.choose(self.r)['model'],m.SOL)
 def test_ambiguity_strong(self):self.r['clear']=False;self.assertEqual(m.choose(self.r)['model'],m.SOL)
 def test_unknown_risk_strong(self):self.r['risk']='unknown';self.assertEqual(m.choose(self.r)['model'],m.SOL)
 def test_missing_inputs_hold(self):self.r['ready']['input']=False;self.assertIsNone(m.choose(self.r)['model'])
 def test_missing_permission_hold(self):self.r['ready']['permission']=False;self.assertIsNone(m.choose(self.r)['model'])
 def test_unavailable_no_silent_switch(self):self.assertIsNone(m.choose(self.r,[m.SOL])['model'])
 def test_conversation_no_agent(self):self.r['mode']='conversation';self.assertIsNone(m.choose(self.r)['model'])
 def test_explicit_boolean(self):
  self.r['bounded']='yes'
  with self.assertRaises(ValueError):m.choose(self.r)
 def test_unknown_fields(self):
  self.r['approved']=True
  with self.assertRaises(ValueError):m.choose(self.r)
 def test_reservation_survives_reload(self):
  self.start();self.call('reserve')
  with self.assertRaises(ValueError):self.call('reserve')
  with self.assertRaises(ValueError):self.start()
 def test_foreign_record(self):
  other=self.root/'foreign.json';other.write_text('{}')
  with self.assertRaises(ValueError):m.transition(other,'start',request=self.r)
 def test_source_drift_blocks_reserve(self):
  self.start();(self.target/'a.py').write_text('unreviewed change')
  with self.assertRaises(ValueError):self.call('reserve')
 def test_symlink_input_rejected(self):
  (self.target/'link.py').symlink_to(self.target/'a.py');self.r['inputs']=['link.py']
  with self.assertRaises(ValueError):self.start()
 def test_traversal_rejected(self):
  self.r['inputs']=['../outside']
  with self.assertRaises(ValueError):self.start()
 def test_stale_revision(self):
  self.start()
  with self.assertRaises(ValueError):self.call('reserve',revision=99)
 def test_missing_handle(self):
  self.start();self.call('reserve')
  with self.assertRaises(ValueError):self.call('bind',handle='')
 def test_model_mismatch(self):
  self.start();self.active()
  with self.assertRaises(ValueError):self.finish(model=m.SOL)
 def test_no_termination_no_release(self):
  self.start();self.active()
  with self.assertRaises(ValueError):self.call('finish',handle='native-fixture-1',outcome='qa-failed',evidence=self.proof,actual_model=m.LUNA,terminated=False)
 def test_preview_preserves_native_reservation(self):
  self.start();self.active();self.call('report-preview',handle='native-fixture-1',evidence=self.proof)
  self.assertEqual(m.read(self.record)['model_routing']['state'],'live')
  with self.assertRaises(ValueError):self.call('reserve')
 def test_preview_is_not_qa(self):
  value=m.read(self.record);value['sprint_iteration']={'schema':2,'state':'iterating','project':'demo','task':'T-001','cycles':[]};m.write(self.record,value);self.start();self.active()
  with self.assertRaises(ValueError):self.finish('qa-passed')
 def test_one_repair_then_sol(self):
  self.start();self.active();self.assertEqual(self.finish()['model_routing']['selection']['model'],m.LUNA)
  self.active('native-fixture-2');self.assertEqual(self.finish(handle='native-fixture-2')['model_routing']['selection']['model'],m.SOL)
  self.active('native-fixture-3');self.assertEqual(self.finish(handle='native-fixture-3',model=m.SOL)['model_routing']['state'],'blocked')
  with self.assertRaises(ValueError):self.call('reserve')
 def test_all_other_fields_preserved(self):
  self.start();self.active();self.finish('qa-passed');self.assertEqual(m.read(self.record)['unrelated'],{'preserve':True})
 def test_failure_evidence_bound(self):
  self.start();self.active();self.finish();a=m.read(self.record)['model_routing']['attempts'][0];self.assertEqual(a['evidence']['sha256'],m.hashlib.sha256(self.proof.read_bytes()).hexdigest())
 def test_no_handle_reuse(self):
  self.start();self.active();self.finish();self.call('reserve')
  with self.assertRaises(ValueError):self.call('bind',handle='native-fixture-1')
 def test_budget_not_reset_by_handoff(self):
  value=m.read(self.record);s={'schema':2,'state':'targeted','project':'demo','task':'T-001','cycles':[{'started_at':time.time()-75}]};value['sprint_iteration']=s;m.write(self.record,value);self.start();self.active();self.finish();self.assertEqual(m.read(self.record)['sprint_iteration'],s);self.assertLessEqual(m.qa_remaining(m.read(self.record)),225)
 def test_expired_budget_blocks_dispatch(self):
  value=m.read(self.record);value['sprint_iteration']={'schema':2,'state':'targeted','project':'demo','task':'T-001','cycles':[{'started_at':time.time()-301}]};m.write(self.record,value);self.start()
  with self.assertRaises(ValueError):self.call('reserve')
 def test_expired_qa_cannot_pass(self):
  self.start();self.active();v=m.read(self.record);v['sprint_iteration']={'schema':2,'state':'targeted','project':'demo','task':'T-001','cycles':[{'started_at':time.time()-301}]};m.write(self.record,v)
  s=self.finish('qa-passed')['model_routing'];self.assertEqual(s['state'],'held');self.assertEqual(s['hold_reason'],'qa-incomplete');self.assertEqual(s['attempts'][-1]['status'],'terminated')
 def test_backwards_clock_blocks(self):
  with self.assertRaises(ValueError):m.qa_remaining({'sprint_iteration':{'schema':2,'state':'targeted','cycles':[{'started_at':500}]}},now=400)
 def test_read_only_no_state_write(self):
  self.r['mode']='read-only';before=self.record.read_bytes()
  with self.assertRaises(ValueError):self.start()
  self.assertEqual(self.record.read_bytes(),before)
 def test_unknown_version(self):
  with self.assertRaises(ValueError):m.qa_remaining({'sprint_iteration':{'schema':99}})
 def test_foreign_sprint(self):
  v=m.read(self.record);v['sprint_iteration']={'project':'other','task':'T-001'};m.write(self.record,v)
  with self.assertRaises(ValueError):self.start()
 def test_blocked_input_does_not_escalate(self):
  self.start();self.active();self.assertEqual(self.finish('blocked-input')['model_routing']['state'],'held')
 def test_scope_drift_holds(self):
  self.start();self.active();self.assertEqual(self.finish('scope-drift')['model_routing']['hold_reason'],'scope-drift')

if __name__=='__main__':unittest.main()
