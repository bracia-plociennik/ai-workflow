"""Exercise the real project consumer without private owner source access."""
import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'prepare-wig-mentoring'
loader=importlib.machinery.SourceFileLoader('mentor_project_consumer',str(SCRIPT))
spec=importlib.util.spec_from_loader(loader.name,loader);consumer=importlib.util.module_from_spec(spec);loader.exec_module(consumer)


class Projection(unittest.TestCase):
    def value(self):
        return {'contract':'wig-mentoring-project-v1','authority':'none','execution_authorized':False,'task_hash':'a'*64,'context_hash':'b'*64,'action':'suggest-return','reason_codes':['task-diverges-from-confirmed-priority']}

    def test_current_minimal_projection_roundtrips(self):
        value=self.value();self.assertEqual(consumer.validate(value),value)
        p=subprocess.run([sys.executable,str(SCRIPT)],input=json.dumps(value),text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout);self.assertEqual(json.loads(p.stdout),value)

    def test_private_fields_permissions_unknown_versions_and_wrong_identities_reject(self):
        for key,value in [('private_sources',{'goal':'private'}),('goal','private'),('authority','owner-approved'),('execution_authorized',True),('contract','future-v2'),('task_hash','unhashed-private-id')]:
            row=self.value();row[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):consumer.validate(row)

    def test_all_supported_actions_and_consistent_reason_codes(self):
        for reason,action in [('current-goal-unknown','clarify'),('daily-weekly-intent-conflict','clarify'),('already-addressed-for-this-task','quiet'),('necessary-obligation-or-dependency','quiet'),('task-finished','quiet'),('aligned','quiet'),('alignment-not-established','quiet'),('mentor-disabled','quiet'),('not-a-decision-boundary','quiet')]:
            row=self.value();row.update(reason_codes=[reason],action=action);self.assertEqual(consumer.validate(row),row)
            row['action']='suggest-return'
            with self.assertRaises(ValueError):consumer.validate(row)

    def test_invalid_payloads_never_echo_private_input(self):
        for raw in ['{"private_goal":"private-secret"}',json.dumps(self.value()).replace('"authority": "none"','"authority":"none","authority":"none"'),'private-secret'*500]:
            p=subprocess.run([sys.executable,str(SCRIPT)],input=raw,text=True,capture_output=True)
            self.assertEqual(p.returncode,2);self.assertNotIn('private-secret',p.stdout+p.stderr)
            self.assertFalse(json.loads(p.stdout)['execution_authorized'])


if __name__=='__main__':unittest.main()
