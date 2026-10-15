#!/usr/bin/env python3
"""Public work-lead inspection behavior; metadata must never authenticate consent."""
import copy
import datetime
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
MODULE = runpy.run_path(str(ROOT / '.systems/scripts/lib/coordinator-status.py'))


class WorkLead(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.resource = self.root / 'src' / 'feature.py'
        self.lead = dict(schema_version=1, lead_id='lead', lead_kind='human', owner_id='owner',
                         parent_work_id='parent', mandate_ref='decisions/current-owner.md',
                         mandate_revision=1, allowed_actions=['inspect', 'implementation'],
                         resource_roots=[str(self.root)], phase_ceiling='phase-5-quality',
                         reserved_actions=['final-owner-yes'], escalation_target='owner')
        self.record = dict(work_lead=self.lead, mandate_state='issued', valid_until=None,
                           context_binding='resolved', evidence_refs=['decisions/current-owner.md'])

    def inspect(self, record=None, **kw):
        return MODULE['inspect_work_lead'](record or self.record, action=kw.get('action', 'implementation'),
                                         resource=kw.get('resource', str(self.resource)),
                                         phase=kw.get('phase', 'phase-4-implementation'))

    def test_equal_scopes_have_equal_gates_without_actor_only_question(self):
        human = self.inspect()
        self.lead['lead_kind'] = 'ai-system'
        self.assertEqual(human, self.inspect())
        self.assertEqual(human['scope_check'], 'matched')
        self.assertFalse(human['execution_authorized'])
        self.assertEqual(human['authority_check'], 'unknown')
        self.assertFalse(human['provenance_verified'])

    def test_outside_action_resource_and_phase_are_rejected(self):
        for opts in ({'action': 'publish'}, {'resource': str(self.root.parent / 'foreign')},
                     {'phase': 'phase-8-final-check'}):
            with self.subTest(opts=opts):
                out = self.inspect(**opts)
                self.assertEqual(out['authority_check'], 'out-of-scope')
                self.assertEqual(out['next_allowed_action'], 'inspect')

    def test_revoked_and_superseded_records_never_resume_execution(self):
        for state in ('revoked', 'superseded', 'unknown'):
            self.record['mandate_state'] = state
            self.assertNotEqual(self.inspect()['scope_check'], 'matched')

    def test_expiry_read_only_and_reserved_action(self):
        self.record['valid_until'] = '2000-01-01T00:00:00+00:00'
        self.assertEqual(self.inspect()['authority_check'], 'expired')
        self.record['valid_until'] = None
        self.lead['allowed_actions'] = ['inspect']
        self.assertEqual(self.inspect()['authority_check'], 'out-of-scope')
        self.assertEqual(self.inspect(action='final-owner-yes')['authority_check'], 'out-of-scope')

    def test_forged_fields_unknown_versions_wildcards_and_bool_revision_fail(self):
        for key, value in [('approved', True), ('schema_version', 99), ('mandate_revision', True),
                           ('allowed_actions', ['*']), ('resource_roots', ['/tmp/../']),
                           ('lead_kind', 'worker')]:
            item = copy.deepcopy(self.record)
            item['work_lead'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.inspect(item)

    def test_binding_and_evidence_absence_are_descriptive_blockers(self):
        self.record['context_binding'] = 'unavailable'
        self.assertEqual(self.inspect()['scope_check'], 'blocked')
        self.record['context_binding'] = 'resolved'
        self.record['evidence_refs'] = []
        self.assertEqual(self.inspect()['authority_check'], 'missing')

    def test_symlink_alias_rejected(self):
        link = self.root / 'link'
        link.symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.inspect(resource=str(link / 'foreign'))

    def test_explicit_schema3_cli_preserves_unknown_quality_gate(self):
        owner = self.root / 'workspace/projects/synthetic'
        owner.mkdir(parents=True)
        (owner / 'status.md').write_text('| `current-phase` | `phase-4-implementation` |\n')
        (owner / 'lead.json').write_text(json.dumps(self.record))
        result = subprocess.run([sys.executable, '-B', str(ROOT / '.systems/scripts/lib/coordinator-status.py'),
                                 '--workflow', str(ROOT), '--workspace', str(self.root / 'workspace'),
                                 '--repo', str(ROOT), '--project', 'synthetic', '--schema-version', '3',
                                 '--lead-record', 'lead.json', '--resource', str(self.resource),
                                 '--requested-action', 'implementation'], capture_output=True, text=True)
        out = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(out['schema_version'], 3)
        self.assertEqual(out['scope_check'], 'matched')
        self.assertEqual(out['actual_gate'], 'unknown')
        self.assertFalse(out['execution_authorized'])


if __name__ == '__main__':
    unittest.main()
