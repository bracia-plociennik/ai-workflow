#!/usr/bin/env python3
"""Offline regressions for mode selection and conservative readiness."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("execution_modes", ROOT / ".systems/scripts/lib/execution-modes.py")
em = importlib.util.module_from_spec(spec)
spec.loader.exec_module(em)


class ExecutionModes(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / ".systems/ai/templates/autopilot/execution-readiness.template.json").read_text())

    def add_unit(self, name="UNIT-002", dependencies=None, resources=None):
        unit = copy.deepcopy(self.record["units"][0])
        unit.update(id=name, dependencies=dependencies or [], resources=resources or ["files/" + name])
        self.record["units"].append(unit)
        return unit

    def decision(self, disposition="pending", classification="owner-preference"):
        decision = dict(id="D-001", classification=classification, disposition=disposition,
                        affected_units=["UNIT-001"], reversible=True, within_scope=True,
                        permission_covered=True, reason="accepted UX goal", override_impact="local rework and re-QA")
        self.record["decisions"].append(decision)
        return decision

    def test_selection_and_resume(self):
        self.assertEqual(em.resolve_mode(), "auto")
        self.assertEqual(em.resolve_mode(project="human-coop"), "human-coop")
        self.assertEqual(em.resolve_mode(task="auto", project="human-coop"), "auto")
        self.assertEqual(em.resolve_mode(session="human-coop", project="auto"), "human-coop")
        self.assertEqual(em.resolve_mode(resumed="human-coop"), "human-coop")
        self.assertEqual(em.resolve_mode(), "auto")  # next task has no expired override
        for invalid in ("", "unknown", [], False):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(em.InvalidState, "unknown execution mode"):
                em.resolve_mode(task=invalid)

    def test_projection_requires_explicit_mode(self):
        for invalid in (None, "", "unknown", [], False):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(em.InvalidState, "unknown execution mode"):
                self.record["execution"]["mode"] = invalid
                em.assess(self.record)

    def test_auto_reversible_preference(self):
        self.decision("agent-choice")
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])

    def test_human_preference_not_agent_chosen(self):
        self.record["execution"]["mode"] = "human-coop"
        self.decision("agent-choice")
        with self.assertRaisesRegex(em.InvalidState, "Human Coop"):
            em.assess(self.record)

    def test_human_trivial_choice(self):
        self.record["execution"]["mode"] = "human-coop"
        self.decision("agent-choice", "auto-resolvable")
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])

    def test_high_impact_choice_keeps_classification(self):
        self.decision("agent-choice", "high-impact")
        self.record["units"][0]["approval_reference"] = "owner-approved-local-options"
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])
        self.record["units"][0]["approval_reference"] = None
        with self.assertRaisesRegex(em.InvalidState, "scoped approval"):
            em.assess(self.record)

    def test_no_unsafe_choice(self):
        for field in ("reversible", "within_scope", "permission_covered"):
            with self.subTest(field=field):
                self.record["decisions"] = []
                self.decision("agent-choice")[field] = False
                with self.assertRaisesRegex(em.InvalidState, "unsafe agent choice"):
                    em.assess(self.record)
        for category in ("critical-risk", "blocked-by-missing-facts"):
            self.record["decisions"] = []
            self.decision("agent-choice", category)
            with self.assertRaises(em.InvalidState):
                em.assess(self.record)

    def test_independent_subset_and_transitive_dependents(self):
        self.decision()
        self.add_unit()
        self.add_unit("UNIT-003", ["UNIT-001"])
        self.add_unit("UNIT-004", ["UNIT-003"])
        self.record["requested_status"] = "running"
        result = em.assess(self.record)
        self.assertEqual(result["ready_units"], ["UNIT-002"])
        self.assertEqual(set(result["blocked_units"]), {"UNIT-001", "UNIT-003", "UNIT-004"})

    def test_owner_wait_when_no_independent_work(self):
        self.decision()
        self.assertEqual(em.assess(self.record)["result"], "awaiting-owner")
        self.record["requested_status"] = "running"
        with self.assertRaisesRegex(em.InvalidState, "running without"):
            em.assess(self.record)

    def test_shared_blocked_resource(self):
        self.decision()
        self.add_unit(resources=["files/example/child"])
        self.assertEqual(em.assess(self.record)["ready_units"], [])

    def test_case_alias_resource_overlap(self):
        self.add_unit(resources=["FILES/EXAMPLE"])
        self.assertEqual(em.assess(self.record)["ready_units"], [])

    def test_unknown_dependencies_or_isolation(self):
        for field in ("dependencies_known", "isolation_verified", "gates_ready", "dod_testable"):
            with self.subTest(field=field):
                unit = self.record["units"][0]
                unit[field] = False
                self.assertEqual(em.assess(self.record)["ready_units"], [])
                unit[field] = True

    def test_duplicate_unknown_cycle(self):
        self.add_unit()
        self.record["units"][1]["id"] = "UNIT-001"
        with self.assertRaisesRegex(em.InvalidState, "duplicate"):
            em.assess(self.record)
        self.record["units"][1]["id"] = "UNIT-002"
        self.record["units"][0]["dependencies"] = ["MISSING"]
        with self.assertRaisesRegex(em.InvalidState, "unknown dependency"):
            em.assess(self.record)
        self.record["units"][0]["dependencies"] = ["UNIT-002"]
        self.record["units"][1]["dependencies"] = ["UNIT-001"]
        with self.assertRaisesRegex(em.InvalidState, "cycle"):
            em.assess(self.record)

    def test_scoped_high_risk_approval(self):
        unit = self.record["units"][0]
        unit.update(risk="high", required_actions=["local-write", "formal-quality"],
                    approved_actions=["local-write", "formal-quality"], approval_reference="decisions/owner-scope.md")
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])
        unit["required_actions"].append("production-deploy")
        self.assertEqual(em.assess(self.record)["ready_units"], [])
        unit["required_actions"].pop()
        unit["approval_reference"] = None
        self.assertEqual(em.assess(self.record)["ready_units"], [])

    def test_critical_is_human_led(self):
        self.record["units"][0].update(risk="critical", approval_reference="owner-ref")
        self.assertEqual(em.assess(self.record)["ready_units"], [])

    def test_baseline_drift(self):
        self.record["baseline"]["current"] = "new-head"
        self.assertEqual(em.assess(self.record)["ready_units"], [])

    def test_no_false_completion_or_stale_quality(self):
        self.record["requested_status"] = "completed"
        with self.assertRaisesRegex(em.InvalidState, "incomplete DoD"):
            em.assess(self.record)
        unit = self.record["units"][0]
        unit.update(status="completed", quality_current=True, capture_complete=True)
        self.assertEqual(em.assess(self.record)["result"], "completed")
        for field in ("quality_current", "capture_complete"):
            unit[field] = False
            with self.assertRaisesRegex(em.InvalidState, "completed unit lacks"):
                em.assess(self.record)
            unit[field] = True
        self.decision()
        with self.assertRaisesRegex(em.InvalidState, "pending decision"):
            em.assess(self.record)

    def test_dependency_requires_accepted_quality(self):
        self.add_unit(dependencies=["UNIT-001"])
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])
        self.record["units"][0].update(status="completed", quality_current=True, capture_complete=True)
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-002"])

    def test_completed_dependency_cannot_be_unfinished(self):
        unit = self.add_unit(dependencies=["UNIT-001"])
        unit.update(status="completed", quality_current=True, capture_complete=True)
        with self.assertRaisesRegex(em.InvalidState, "unfinished dependency"):
            em.assess(self.record)

    def test_final_check_needs_explicit_scope(self):
        self.record["final_check"]["requested"] = True
        with self.assertRaisesRegex(em.InvalidState, "explicit request"):
            em.assess(self.record)
        self.record["final_check"]["approval_reference"] = "owner-plan-final-check"
        self.assertEqual(em.assess(self.record)["result"], "running")
        self.record["final_check"]["owner_yes"] = True
        with self.assertRaisesRegex(em.InvalidState, "final-owner-yes"):
            em.assess(self.record)

    def test_legacy_missing_field_has_no_new_authority(self):
        del self.record["execution"]
        with self.assertRaisesRegex(em.InvalidState, "fields"):
            em.assess(self.record)

    def test_plan_only_and_read_only_write_boundary(self):
        unit = self.record["units"][0]
        unit.update(work_kind="planning", required_actions=["product-write"], approved_actions=["product-write"])
        with self.assertRaisesRegex(em.InvalidState, "planning request"):
            em.assess(self.record)
        unit.update(required_actions=["local-write"], approved_actions=["local-write"])
        with self.assertRaisesRegex(em.InvalidState, "planning request"):
            em.assess(self.record)
        unit.update(required_actions=["artifact-write"], approved_actions=["artifact-write"], approval_reference="owner-plan")
        self.assertEqual(em.assess(self.record)["ready_units"], ["UNIT-001"])
        unit["work_kind"] = "read-only"
        with self.assertRaisesRegex(em.InvalidState, "read-only"):
            em.assess(self.record)

    def test_malformed_flags_and_resources(self):
        self.record["units"][0]["gates_ready"] = "yes"
        with self.assertRaisesRegex(em.InvalidState, "boolean"):
            em.assess(self.record)
        self.record["units"][0]["gates_ready"] = True
        for resource in ("../secret", "files/./secret", "/absolute", "files//secret"):
            self.record["units"][0]["resources"] = [resource]
            with self.assertRaisesRegex(em.InvalidState, "unsafe resource"):
                em.assess(self.record)

    def test_cli_duplicate_json_and_inspection(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state.json"
            path.write_text(json.dumps(self.record))
            cli = ROOT / ".systems/scripts/lib/execution-modes.py"
            result = subprocess.run(["python3", str(cli), "--state", str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["authority"], "inspection-only")
            path.write_text('{"schema": 1, "schema": 1}')
            result = subprocess.run(["python3", str(cli), "--state", str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate JSON key", result.stderr)

    def test_unknown_action_rejected(self):
        self.record["units"][0].update(required_actions=["invented-write"], approved_actions=["invented-write"])
        with self.assertRaisesRegex(em.InvalidState, "unknown action"):
            em.assess(self.record)

    def test_missing_write_and_resource_declarations_rejected(self):
        unit = self.record["units"][0]
        unit["required_actions"] = []
        with self.assertRaisesRegex(em.InvalidState, "lacks declared write action"):
            em.assess(self.record)
        unit["required_actions"] = ["local-write"]
        unit["resources"] = []
        with self.assertRaisesRegex(em.InvalidState, "lacks resource claims"):
            em.assess(self.record)

    def test_owner_approval_outside_scope_rejected(self):
        self.decision("owner-approved")["within_scope"] = False
        with self.assertRaisesRegex(em.InvalidState, "uncovered owner decision"):
            em.assess(self.record)

    def test_cli_rejects_symlink_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state.json"
            original = json.dumps(self.record)
            path.write_text(original)
            link = Path(temporary) / "linked.json"
            link.symlink_to(path)
            result = subprocess.run(["python3", str(ROOT / ".systems/scripts/lib/execution-modes.py"), "--state", str(link)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink projection", result.stderr)
            self.assertEqual(path.read_text(), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
