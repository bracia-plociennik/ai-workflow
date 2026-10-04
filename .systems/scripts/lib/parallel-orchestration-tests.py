#!/usr/bin/env python3
"""Synthetic offline behavioral regressions; no worker spawning or model calls."""
import argparse
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("parallel_orchestration", HERE / "parallel-orchestration.py")
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)

coordinator_spec = importlib.util.spec_from_file_location('coordinator', HERE / 'coordinator-status.py')
coordinator = importlib.util.module_from_spec(coordinator_spec)
coordinator_spec.loader.exec_module(coordinator)


class CompatibilityTests(unittest.TestCase):
    samples = []

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pto-compat-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.path = self.root / coordinator.CAPABILITY
        self.path.parent.mkdir(parents=True)
        self.value = json.loads((ROOT / coordinator.CAPABILITY).read_text())
        self.path.write_text(json.dumps(self.value))
        for raw in coordinator.PARALLEL_FILES:
            path = self.root / raw
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / raw).read_bytes())

    def result(self):
        out = coordinator.parallel_capability(self.root)
        self.assertFalse(out['execution_authorized'])
        self.assertFalse(out['operational_support'])
        self.assertEqual(out['owner_permission'], 'not-assessed')
        self.assertEqual(out['native_backend_verification'], 'unverified')
        self.assertEqual(out['fallback'], 'serial')
        return out

    def save(self):
        self.path.write_text(json.dumps(self.value))

    def test_installed_does_not_mean_operational_or_approved(self):
        self.assertEqual(self.result()['state'], 'installed')
        self.assertEqual(self.result()['installed_protocol']['protocol_version'], 1)

    def test_missing_and_invalid_capability(self):
        for raw in ('{}', 'null', '[]', '{', '{"schema_version":1,"schema_version":1}', '"private-secret-input"', '[' * 2000 + '0' + ']' * 2000):
            self.path.write_text(raw)
            out = self.result()
            self.assertEqual(out['state'], 'unknown')
            self.assertNotIn('private-secret-input', json.dumps(out))
        self.path.unlink()
        self.assertEqual(self.result()['state'], 'unknown')

    def test_installed_sources_must_match_hashes_and_schemas(self):
        for raw in coordinator.PARALLEL_FILES:
            path = self.root / raw
            original = path.read_bytes()
            path.write_text('{}' if raw.endswith('.json') else 'changed installed source')
            self.assertEqual(self.result()['state'], 'unknown')
            path.write_bytes(original)
        unit = self.root / '.systems/ai/templates/orchestration/unit.template.json'
        for content in ('{"schema":2}', '{', '[' * 2000 + '0' + ']' * 2000):
            unit.write_text(content)
            self.value['installed_sources_sha256'][str(unit.relative_to(self.root))] = hashlib.sha256(unit.read_bytes()).hexdigest()
            self.save()
            self.assertEqual(self.result()['state'], 'unknown')
        self.value['installed_sources_sha256'] = {}
        self.save()
        self.assertEqual(self.result()['state'], 'unknown')

    def test_deep_json_cli_is_conservative_without_traceback(self):
        workspace = self.git_fixture()
        self.path.write_text('[' * 2000 + '0' + ']' * 2000)
        result = subprocess.run([sys.executable, str(HERE / 'coordinator-status.py'),
                                 '--workflow', str(self.root), '--workspace', str(workspace),
                                 '--repo', str(self.root), '--project', 'synthetic', '--schema-version', '2'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(json.loads(result.stdout)['parallel_capability']['state'], 'unknown')

    def test_closed_versions_and_authority(self):
        original = copy.deepcopy(self.value)
        for key in ('schema_version', 'protocol_version', 'manifest_schema', 'unit_schema', 'result_schema'):
            for value in (True, 2, '1', None):
                self.value = copy.deepcopy(original)
                self.value[key] = value
                self.save()
                self.assertEqual(self.result()['state'], 'unknown')
        for key, value in (('execution_authorized', True), ('fallback', 'parallel'),
                           ('unexpected', 'field'), ('installed_modes', ['serial', 'native']),
                           ('feature', '../other')):
            self.value = copy.deepcopy(original)
            self.value[key] = value
            self.save()
            self.assertEqual(self.result()['state'], 'unknown')

    def test_native_assertions_rejected(self):
        for key, value in (('verification', 'verified'), ('isolation', 'verified'),
                           ('capacity', 2), ('tested_backends', ['codex'])):
            self.value['native_backend'] = {'verification': 'unverified', 'isolation': 'unknown',
                                             'capacity': None, 'tested_backends': []}
            self.value['native_backend'][key] = value
            self.save()
            self.assertEqual(self.result()['state'], 'unknown')

    def test_link_hardlink_oversize_and_missing_installation(self):
        raw = self.path.read_bytes()
        foreign = self.root / 'foreign.json'
        foreign.write_bytes(raw)
        self.path.unlink()
        self.path.symlink_to(foreign)
        self.assertEqual(self.result()['state'], 'unknown')
        self.path.unlink()
        os.link(foreign, self.path)
        self.assertEqual(self.result()['state'], 'unknown')
        self.path.unlink()
        self.path.write_bytes(b' ' * 32769)
        self.assertEqual(self.result()['state'], 'unknown')
        self.path.write_bytes(raw)
        (self.root / coordinator.PARALLEL_FILES[0]).unlink()
        self.assertEqual(self.result()['state'], 'unknown')

    def git_fixture(self):
        env = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull}
        def git(*args):
            subprocess.run(['git', '-C', str(self.root), *args], env=env, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git('init', '--initial-branch=main')
        git('add', '.')
        git('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid', 'commit', '-m', 'fixture')
        workspace = self.root / 'runtime'
        owner = workspace / 'projects/synthetic'
        owner.mkdir(parents=True)
        (owner / 'status.md').write_text('| current-phase | phase-4-implementation |\n| current-task | SYNTH-001 |\n')
        return workspace

    def test_schema1_exact_shape_and_schema2_opt_in(self):
        workspace = self.git_fixture()
        one = coordinator.status(self.root, workspace, self.root, 'synthetic')
        self.assertEqual(one, coordinator.status(self.root, workspace, self.root, 'synthetic', 1))
        two = coordinator.status(self.root, workspace, self.root, 'synthetic', 2)
        self.assertEqual(two['schema_version'], 2)
        self.assertEqual({key: value for key, value in two.items() if key != 'parallel_capability'},
                         {**one, 'schema_version': 2})
        self.assertNotIn('parallel_capability', one)
        self.assertEqual(two['parallel_capability']['state'], 'installed')
        self.path.unlink()
        removed = coordinator.status(self.root, workspace, self.root, 'synthetic')
        self.assertNotEqual(removed['baseline'], one['baseline'])
        self.assertEqual({key: value for key, value in removed.items() if key != 'baseline'},
                         {key: value for key, value in one.items() if key != 'baseline'})
        self.assertEqual(coordinator.status(self.root, workspace, self.root, 'synthetic', 2)['parallel_capability']['state'], 'unknown')

    def test_real_cli_schema_and_unknown_capability(self):
        workspace = self.git_fixture()
        args = [sys.executable, str(HERE / 'coordinator-status.py'), '--workflow', str(self.root),
                '--workspace', str(workspace), '--repo', str(self.root), '--project', 'synthetic']
        before = planner.file_inventory(self.root / '.systems')
        for version in (1, 2):
            result = subprocess.run(args + ['--schema-version', str(version)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)  # No formal QA in this synthetic project.
            value = json.loads(result.stdout)
            self.assertEqual(value['schema_version'], version)
            self.assertFalse(value['execution_authorized'])
            self.assertEqual('parallel_capability' in value, version == 2)
        self.assertEqual(before, planner.file_inventory(self.root / '.systems'))

    def test_capability_change_during_status_is_rejected(self):
        workspace = self.git_fixture()
        real = coordinator.parallel_capability
        calls = []
        def drifting(root):
            if calls:
                (self.root / coordinator.PARALLEL_FILES[0]).write_text('changed after initial read')
            calls.append(True)
            return real(root)
        with patch.object(coordinator, 'parallel_capability', drifting):
            with self.assertRaisesRegex(ValueError, 'capability changed'):
                coordinator.status(self.root, workspace, self.root, 'synthetic', 2)

    def test_unknown_isolation_does_not_become_a_native_proposal(self):
        run = json.loads((ROOT / '.systems/ai/templates/orchestration/run.template.json').read_text())
        unit = json.loads((ROOT / '.systems/ai/templates/orchestration/unit.template.json').read_text())
        run.update(repository_root=str(self.root), units=[{**unit, 'id': name, 'write_set': ['out/' + name]} for name in ('a', 'b')])
        run['checkpoint']['known'] = True
        run['capacity'] = {'verified': False, 'total': None, 'active_workers': 0}
        run['isolation_verified'] = False
        out = planner.plan(run)
        self.assertEqual(out['mode'], 'serial')
        self.assertFalse(out['execution_authorized'])

    def test_three_paired_offline_samples(self):
        def sample(parallel):
            started = time.perf_counter()
            payload = b'synthetic-only-data' * 4096
            with tempfile.TemporaryDirectory(prefix='pto-measure-') as raw:
                root = Path(raw)
                workers = [root / name for name in ('a', 'b')]
                for worker in workers:
                    worker.mkdir()
                    (worker / 'input.bin').write_bytes(payload)
                def work(worker):
                    data = (worker / 'input.bin').read_bytes()
                    (worker / 'output.txt').write_text(hashlib.sha256(data).hexdigest())
                worker_start = time.perf_counter()
                if parallel:
                    with ThreadPoolExecutor(max_workers=2) as pool:
                        list(pool.map(work, workers))
                else:
                    for worker in workers:
                        work(worker)
                worker_wall = time.perf_counter() - worker_start
                integration_start = time.perf_counter()
                destination = root / 'integrated'
                destination.mkdir()
                for worker in workers:
                    (destination / worker.name).write_bytes((worker / 'output.txt').read_bytes())
                output = [file.read_text() for file in sorted(destination.iterdir())]
                self.assertEqual(output, [hashlib.sha256(payload).hexdigest()] * 2)
                integration = time.perf_counter() - integration_start
            return {'total_seconds': time.perf_counter() - started, 'worker_wall_seconds': worker_wall,
                    'integration_seconds': integration, 'rework_seconds': 0, 'conflicts': 0,
                    'quality': 'same-assertions-satisfied', 'output_digest': hashlib.sha256(json.dumps(output).encode()).hexdigest(),
                    'active_workers': 2 if parallel else 1, 'native_workers': 0}
        self.__class__.samples = []
        for index in range(3):
            serial, parallel = sample(False), sample(True)
            self.assertEqual(serial['output_digest'], parallel['output_digest'])
            self.__class__.samples.append({'pair': index + 1, 'serial': serial, 'parallel': parallel})

class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.run = json.loads((ROOT / ".systems/ai/templates/orchestration/run.template.json").read_text())
        self.unit = json.loads((ROOT / ".systems/ai/templates/orchestration/unit.template.json").read_text())
        self.run.update(repository_root=str(self.root), units=[])
        self.run["capacity"] = {"verified": True, "total": 4, "active_workers": 0}
        self.run["isolation_verified"] = True
        self.run["checkpoint"]["known"] = True

    def add(self, name, task="TASK-001", **changes):
        unit = copy.deepcopy(self.unit)
        unit.update(id=name, task_id=task, write_set=["src/" + name])
        unit.update(changes)
        self.run["units"].append(unit)
        return unit

    def result(self):
        result = planner.plan(self.run)
        self.assertFalse(result["execution_authorized"])
        return result

    def invalid(self, value=None):
        with self.assertRaises((planner.InvalidManifest, TypeError)):
            planner.plan(self.run if value is None else value)

    def test_four_then_active_capacity(self):
        for name in "abcd":
            self.add(name)
        self.assertEqual(self.result()["selected_count"], 4)
        self.run["capacity"]["active_workers"] = 2
        self.assertEqual(self.result()["proposed_units"], ["a", "b"])

    def test_zero_unknown_and_isolation(self):
        self.add("a")
        self.run["capacity"]["total"] = 0
        self.assertEqual(self.result()["selected_count"], 0)
        self.run["capacity"] = {"verified": False, "total": None, "active_workers": 0}
        self.add("b")
        self.assertEqual(self.result()["mode"], "serial")
        self.assertEqual(self.result()["selected_count"], 1)
        self.run["capacity"]["active_workers"] = 1
        self.assertEqual(self.result()["selected_count"], 0)
        self.run["capacity"] = {"verified": True, "total": 4, "active_workers": 0}
        self.run["isolation_verified"] = False
        self.assertEqual(self.result()["selected_count"], 1)

    def test_chain_requires_accepted_snapshot(self):
        a = self.add("a")
        b = self.add("b", dependencies=["a"])
        self.add("c", dependencies=["b"])
        self.assertEqual(self.result()["proposed_units"], ["a"])
        a.update(state="accepted", accepted_output="a" * 64)
        self.assertEqual(self.result()["selected_count"], 0)
        b["expected_inputs"] = {"a": "a" * 64}
        self.assertEqual(self.result()["proposed_units"], ["b"])
        b["expected_inputs"]["a"] = "b" * 64
        self.assertEqual(self.result()["selected_count"], 0)

    def test_diamond_submitted_not_accepted(self):
        self.add("a", state="accepted", accepted_output="a" * 64)
        self.add("b", dependencies=["a"], expected_inputs={"a": "a" * 64},
                 state="accepted", accepted_output="b" * 64)
        self.add("c", dependencies=["a"], expected_inputs={"a": "a" * 64}, state="submitted")
        self.add("d", dependencies=["b", "c"], expected_inputs={"b": "b" * 64})
        self.run["reservations"] = ["c"]
        self.run["checkpoint"]["active_tasks"] = ["TASK-001"]
        self.assertEqual(self.result()["selected_count"], 0)

    def test_graph_invalid_all_components(self):
        self.add("a")
        b = self.add("b", dependencies=["c"])
        self.add("c", dependencies=["b"])
        self.invalid()
        b["dependencies"] = ["missing"]
        self.invalid()
        b["dependencies"] = ["b"]
        self.invalid()
        b["dependencies"] = ["a", "a"]
        self.invalid()
        self.run["units"].append(copy.deepcopy(self.run["units"][0]))
        self.invalid()

    def test_read_write_and_prefix(self):
        self.add("a", write_set=["build"])
        self.add("b", read_set=["build/new/file"], write_set=[])
        self.add("c", write_set=["builder"])
        self.assertEqual(self.result()["proposed_units"], ["a", "c"])

    def test_read_read_parallel(self):
        self.add("a", read_set=["source"], write_set=[])
        self.add("b", read_set=["source"], write_set=[])
        self.assertEqual(self.result()["mode"], "parallel-read-only")

    def test_active_pool_and_reserved_paths(self):
        self.add("a", task="TASK-OTHER", state="running", write_set=["build"])
        self.add("b", read_set=["build/output"])
        self.add("c")
        self.run["capacity"]["active_workers"] = 1
        self.run["reservations"] = ["a"]
        self.run["checkpoint"]["active_tasks"] = ["TASK-OTHER"]
        self.assertEqual(self.result()["proposed_units"], ["c"])
        self.run["capacity"]["active_workers"] = 0
        self.invalid()
        self.run["capacity"]["active_workers"] = 1
        self.run["reservations"] = []
        self.invalid()

    def test_resources(self):
        a = self.add("a", resources=[{"name": "database"}])
        b = self.add("b", resources=[{"name": "database", "mode": "shared-read"}])
        self.assertEqual(self.result()["selected_count"], 1)
        a["resources"][0]["mode"] = "shared-read"
        self.assertEqual(self.result()["selected_count"], 2)
        b["resources"][0]["mode"] = "shraed-read"
        self.invalid()

    def test_checkpoint_wave_accumulates_parent_slots(self):
        self.run["checkpoint"]["completed_since_checkpoint"] = 2
        self.add("a", task="TASK-003")
        self.add("b", task="TASK-004")
        self.add("c", task="TASK-003")
        self.assertEqual(self.result()["proposed_units"], ["a", "c"])
        self.run["checkpoint"]["active_tasks"] = ["TASK-004"]
        self.assertEqual(self.result()["proposed_units"], ["b"])
        self.run["checkpoint"]["known"] = False
        self.assertEqual(self.result()["selected_count"], 0)

    def test_three_active_tasks_block_fourth(self):
        self.run["checkpoint"]["active_tasks"] = ["TASK-001", "TASK-002", "TASK-003"]
        self.add("a", task="TASK-004")
        self.assertEqual(self.result()["selected_count"], 0)

    def test_cross_task_gate_not_replaced_by_unit(self):
        self.add("a", task="TASK-001", state="accepted", accepted_output="a" * 64)
        self.add("b", task="TASK-002", dependencies=["a"], expected_inputs={"a": "a" * 64})
        self.assertEqual(self.result()["selected_count"], 0)
        self.assertIn("cross-task", str(self.result()["rejected_candidates"]))

    def test_priority_and_permutation(self):
        self.add("c")
        self.add("b", priority=1)
        self.add("a", priority=1)
        expected = self.result()
        self.run["units"].reverse()
        self.assertEqual(self.result(), expected)
        self.assertEqual(expected["proposed_units"], ["a", "b", "c"])

    def test_unknown_keys_and_wrong_types(self):
        self.add("a")
        for container, key, value in [(self.run, "approved", True),
                                      (self.run["capacity"], "permission", True),
                                      (self.run["units"][0], "command", "touch outside")]:
            container[key] = value
            self.invalid()
            del container[key]
        for key, value in [("revision", True), ("schema", True), ("isolation_verified", 1)]:
            original = self.run[key]
            self.run[key] = value
            self.invalid()
            self.run[key] = original
        for value in [-1, True, 1.5]:
            self.run["capacity"]["active_workers"] = value
            self.invalid()

    def test_path_rejections_and_missing_outputs(self):
        unit = self.add("a")
        for path in ["../outside", "/absolute", "a/../b", "a//b", "./b", "a\\b", ""]:
            unit["write_set"] = [path]
            self.invalid()
        unit["write_set"] = ["new/nested/output"]
        self.assertEqual(self.result()["selected_count"], 1)
        (self.root / "link").symlink_to(self.root, target_is_directory=True)
        unit["write_set"] = ["link/not-yet-existing"]
        self.invalid()
        (self.root / "dangling").symlink_to(self.root / "absent")
        unit["write_set"] = ["dangling/out"]
        self.invalid()

    def test_aliases(self):
        (self.root / "first").write_text("data")
        os.link(self.root / "first", self.root / "second")
        self.add("a", write_set=["first"])
        self.add("b", write_set=["second"])
        self.invalid()
        self.run["units"][0]["write_set"] = ["future/File"]
        self.run["units"][1]["write_set"] = ["future/file"]
        self.assertEqual(self.result()["selected_count"], 1)

    def test_unicode_parent_aliases_candidate_and_reserved(self):
        (self.root / "caf\u00e9").mkdir()
        self.add("a", write_set=["caf\u00e9/new"])
        self.add("b", read_set=["cafe\u0301/new"], write_set=[])
        self.assertEqual(self.result()["proposed_units"], ["a"])
        self.run["units"][0]["state"] = "running"
        self.run["capacity"]["active_workers"] = 1
        self.run["reservations"] = ["a"]
        self.run["checkpoint"]["active_tasks"] = ["TASK-001"]
        self.assertEqual(self.result()["selected_count"], 0)

    def test_subtree_hardlinks_candidate_and_reserved(self):
        (self.root / "tree").mkdir()
        (self.root / "tree/file").write_text("data")
        os.link(self.root / "tree/file", self.root / "alias")
        self.add("a", read_set=["tree"], write_set=[])
        self.add("b", write_set=["alias"])
        self.invalid()
        self.run["units"][0]["state"] = "running"
        self.run["capacity"]["active_workers"] = 1
        self.run["reservations"] = ["a"]
        self.run["checkpoint"]["active_tasks"] = ["TASK-001"]
        self.invalid()
        self.run["units"][1]["write_set"] = ["other"]
        self.invalid()

    def test_unicode_order_aliases_candidate_and_reserved(self):
        first, second = "\u03b1\u0345\u0301", "\u03b1\u0301\u0345"
        (self.root / first).mkdir()
        self.add("a", write_set=[first + "/new"])
        self.add("b", write_set=[second + "/new"])
        self.assertEqual(self.result()["proposed_units"], ["a"])
        self.run["units"][0]["state"] = "running"
        self.run["capacity"]["active_workers"] = 1
        self.run["reservations"] = ["a"]
        self.run["checkpoint"]["active_tasks"] = ["TASK-001"]
        self.assertEqual(self.result()["selected_count"], 0)

    def test_symlink_ancestors_root_and_manifest(self):
        (self.root / "tree/repo").mkdir(parents=True)
        (self.root / "via").symlink_to(self.root / "tree", target_is_directory=True)
        self.add("a")
        self.run["repository_root"] = str(self.root / "via/repo")
        self.invalid()
        manifest = self.root / "tree/manifest.json"
        manifest.write_text(json.dumps(self.run))
        with self.assertRaises(planner.InvalidManifest):
            planner.load(self.root / "via/manifest.json")

    def test_subtree_special_entries_rejected(self):
        (self.root / "tree").mkdir()
        os.mkfifo(self.root / "tree/pipe")
        self.add("a", read_set=["tree"], write_set=[])
        self.invalid()
        (self.root / "tree/pipe").unlink()
        (self.root / "tree/link").symlink_to(self.root / "missing")
        self.invalid()

    def test_special_path(self):
        fifo = self.root / "pipe"
        os.mkfifo(fifo)
        self.add("a", read_set=["pipe"])
        self.invalid()
        with self.assertRaises(planner.InvalidManifest):
            planner.load(fifo)

    def test_unknown_or_failed_not_complete(self):
        self.add("a", state="rejected")
        self.assertEqual(self.result()["status"], "blocked")
        self.run["units"][0].update(state="accepted", accepted_output="a" * 64)
        self.assertEqual(self.result()["status"], "complete")
        self.run["units"][0]["accepted_output"] = None
        self.invalid()

    def test_json_duplicate_and_nonfinite(self):
        path = self.root / "manifest.json"
        for content in ['{"schema":1,"schema":1}', '{"x":{"y":1,"y":2}}', '{"x":NaN}']:
            path.write_text(content)
            with self.assertRaises(planner.InvalidManifest):
                planner.load(path)

    def test_cli_read_only(self):
        self.add("a")
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps(self.run))
        before = manifest.read_bytes()
        inventory = sorted(self.root.rglob("*"))
        command = [str(ROOT / ".systems/scripts/plan-parallel-work"), "--manifest", str(manifest)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["execution_authorized"])
        human = subprocess.run(command + ["--format", "human"], capture_output=True, text=True, timeout=10)
        self.assertEqual(human.returncode, 0)
        self.assertIn("Execution authorized: false", human.stdout)
        self.assertEqual(manifest.read_bytes(), before)
        self.assertEqual(sorted(self.root.rglob("*")), inventory)
        manifest.write_text('{"bad":1}')
        invalid = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, "")
        manifest.write_bytes(b"\xff")
        invalid = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, "")

class ProtocolTests(unittest.TestCase):
    add = PlannerTests.add
    invalid = PlannerTests.invalid

    def setUp(self):
        PlannerTests.setUp(self)
        self.worker = self.root.parent / (self.root.name + "-worker")
        self.worker.mkdir()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.worker))
        (self.worker / "input.txt").write_text("bounded input")
        (self.worker / "out").mkdir()
        self.u = self.add("a", read_set=["input.txt"], write_set=["out"])
        self.u["execution"] = {
            "input_hashes": {"input.txt": __import__("hashlib").sha256(b"bounded input").hexdigest()},
            "required_checks": ["unit-check"], "stop_conditions": ["scope drift"],
            "minimal_context": ["input.txt"]}
        self.obs = {"backend": "fake", "version": "1", "handle": "handle-a", "cwd": str(self.worker),
                    "writable_roots": [str(self.worker)], "constraints_verified": True,
                    "source_snapshot": self.run["source_snapshot"], "kind": "synthetic"}

    def submission(self):
        attempt = planner.preflight(self.run, "a", self.obs)
        attempt["attempt_id"] = "attempt-001"
        attempt["termination_verified"] = True
        (self.worker / "out/result.txt").write_text("done")
        (self.worker / "out/check.txt").write_text("asserted result")
        inventory = planner.file_inventory(self.worker)
        result = json.loads((ROOT / ".systems/ai/templates/orchestration/result.template.json").read_text())
        result.update(run_id=self.run["run_id"], unit_id="a", handle="handle-a",
                      source_snapshot=self.run["source_snapshot"], baseline_digest=attempt["baseline_digest"],
                      output_digest=planner.digest_json(inventory), changed_files=["out/check.txt", "out/result.txt"],
                      checks=[{"id": "unit-check", "result": "pass", "evidence": "out/check.txt"}])
        return attempt, result

    def reject(self, attempt, result):
        with self.assertRaises(planner.InvalidManifest):
            planner.verify_result(self.run, "a", attempt, result)

    def test_protocol_submission_not_acceptance(self):
        a, result = self.submission()
        actual = planner.verify_result(self.run, "a", a, result)
        self.assertTrue(actual["quality_ready"])
        self.assertFalse(actual["accepted"])
        self.assertFalse(actual["execution_authorized"])
        self.assertEqual(self.u["state"], "planned")

    def test_actual_omitted_write_delete_and_mode(self):
        a, result = self.submission()
        for path in (self.worker / "secret.txt", self.worker / "status.md"):
            path.write_text("omitted write")
            self.reject(a, result)
            path.unlink()
        (self.worker / "input.txt").chmod(0o700)
        self.reject(a, result)
        (self.worker / "input.txt").unlink()
        self.reject(a, result)

    def test_protected_write_even_allowlisted(self):
        for path in ("status.md", "decisions/a", "capture-state/a", "quality/a", "orchestration/a"):
            self.u["write_set"] = [path]
            with self.assertRaises(planner.InvalidManifest):
                planner.preflight(self.run, "a", self.obs)

    def test_observation_constraints_and_shared_cwd(self):
        for key, value in (("constraints_verified", False), ("source_snapshot", "f" * 64),
                           ("writable_roots", [str(self.root.parent)]), ("handle", ""),
                           ("cwd", str(self.root)), ("kind", "assumed")):
            observation = copy.deepcopy(self.obs)
            observation[key] = value
            with self.assertRaises(planner.InvalidManifest):
                planner.preflight(self.run, "a", observation)

    def test_stale_input_and_no_context(self):
        (self.worker / "input.txt").write_text("stale")
        with self.assertRaises(planner.InvalidManifest):
            planner.preflight(self.run, "a", self.obs)
        self.u["execution"]["minimal_context"] = []
        self.invalid()

    def test_attempt_replay_and_contract_drift(self):
        a, result = self.submission()
        for key in ("attempt_id", "handle", "unit_id", "run_id", "baseline_digest", "source_snapshot"):
            value = copy.deepcopy(result)
            value[key] = "foreign"
            self.reject(a, value)
        self.u["dod"] = ["different acceptance"]
        self.reject(a, result)

    def test_evidence_missing_failed_and_findings(self):
        a, result = self.submission()
        result["checks"] = []
        self.reject(a, result)
        result["checks"] = [{"id": "unit-check", "result": "fail", "evidence": "out/check.txt"}]
        self.assertFalse(planner.verify_result(self.run, "a", a, result)["quality_ready"])
        result["checks"][0]["result"] = "pass"
        result["findings"] = ["P2 wrong behavior"]
        self.assertFalse(planner.verify_result(self.run, "a", a, result)["quality_ready"])
        result["checks"][0]["evidence"] = "../foreign"
        self.reject(a, result)

    def test_special_output_blocks_before_hash(self):
        a, result = self.submission()
        os.mkfifo(self.worker / "out/fifo")
        self.reject(a, result)
        (self.worker / "out/fifo").unlink()
        (self.worker / "out/alias").symlink_to(self.root)
        self.reject(a, result)

    def test_empty_directory_and_unknown_liveness(self):
        a, result = self.submission()
        (self.worker / "unexpected-empty-directory").mkdir()
        self.reject(a, result)
        (self.worker / "unexpected-empty-directory").rmdir()
        a["termination_verified"] = False
        self.reject(a, result)

    def test_run_and_coordinator_replay_rejected(self):
        a, result = self.submission()
        for key, value in (("run_id", "foreign-run"), ("project", "foreign-project"),
                           ("coordinator_id", "foreign-coordinator"), ("execution_owner", "ai-system")):
            old = self.run[key]
            self.run[key] = value
            if key == "run_id":
                result[key] = value
            self.reject(a, result)
            self.run[key] = old
            result["run_id"] = self.run["run_id"]

    def test_additional_failed_or_skipped_check_not_ready(self):
        a, result = self.submission()
        for outcome in ("fail", "skipped"):
            result["checks"] = [{"id": "unit-check", "result": "pass", "evidence": "out/check.txt"},
                                {"id": "additional-check", "result": outcome, "evidence": "out/check.txt"}]
            self.assertFalse(planner.verify_result(self.run, "a", a, result)["quality_ready"])

    def test_worker_root_mode_change_rejected(self):
        a, result = self.submission()
        self.worker.chmod(0o777)
        self.reject(a, result)
        self.worker.chmod(a["root_mode"])
        self.assertTrue(planner.verify_result(self.run, "a", a, result)["quality_ready"])
        a["root_identity"][1] += 1
        self.reject(a, result)


class LifecycleTests(unittest.TestCase):
    add = PlannerTests.add
    invalid = PlannerTests.invalid
    submission = ProtocolTests.submission

    def setUp(self):
        ProtocolTests.setUp(self)
        self.project = self.root / "ws/projects/example-project"
        self.runroot = self.project / "orchestration/runs/run-001"
        self.runroot.mkdir(parents=True)
        self.run["lifecycle"] = {"schema": 1, "initial_revision": 0, "attempts": [], "events": [],
                                 "parent_retry_budget": {"limit": None, "reference": None, "sha256": None},
                                 "retry_counts": {}, "completed_tasks": [], "parent_gates": {},
                                 "checkpoint_epoch": 0, "checkpoint_evidence": None}
        self.save()
        (self.project / "reviews").mkdir()
        (self.project / "reviews/unit.md").write_text("Synthetic supplied DoD/diff/limits review.")

    def save(self):
        (self.runroot / "manifest.json").write_text(json.dumps(self.run))

    def refresh(self):
        self.run = planner.load(self.runroot / "manifest.json")
        self.u = self.run["units"][0]

    def change(self, request, revision=None, owner=None):
        value = planner.update_run(self.runroot, owner or self.run["coordinator_id"],
                                   self.run["revision"] if revision is None else revision, request)
        self.refresh()
        self.assertFalse(value["execution_authorized"])
        self.assertFalse(value["dispatch_performed"])
        return value

    def fail(self, request, revision=None, owner=None):
        before = (self.runroot / "manifest.json").read_bytes()
        with self.assertRaises((planner.InvalidManifest, OSError, ValueError)):
            self.change(request, revision, owner)
        self.assertEqual((self.runroot / "manifest.json").read_bytes(), before)

    def start(self):
        self.change({"action": "ready", "unit_id": "a"})
        output = self.change({"action": "start", "unit_id": "a", "attempt_id": "attempt-001",
                              "observation": self.obs})
        self.attempt = output["private_preflight"]

    def result_value(self):
        self.attempt["termination_verified"] = True
        (self.worker / "out/check.txt").write_text("synthetic asserted checks")
        (self.worker / "out/result.txt").write_text("result")
        actual = planner.file_inventory(self.worker)
        return {"schema": 1, "run_id": self.run["run_id"], "unit_id": "a", "attempt_id": "attempt-001",
                "handle": "handle-a", "source_snapshot": self.run["source_snapshot"],
                "baseline_digest": self.attempt["baseline_digest"], "output_digest": planner.digest_json(actual),
                "changed_files": ["out/check.txt", "out/result.txt"],
                "checks": [{"id": "unit-check", "result": "pass", "evidence": "out/check.txt"}],
                "findings": [], "skipped_checks": [], "residual_risk": "synthetic observation, not sandbox proof"}

    def submit(self):
        self.result = self.result_value()
        self.change({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                     "preflight": self.attempt, "result": self.result})

    def observation(self, status="stopped", known=True):
        return [{"attempt_id": "attempt-001", "handle": "handle-a", "status": status,
                 "effects_known": known, "preflight": self.attempt}]

    def review(self, decision="accept"):
        return {"action": "review", "unit_id": "a", "attempt_id": "attempt-001",
                "preflight": self.attempt, "result": self.result,
                "review": {"reviewer": "synthetic-reviewer", "decision": decision, "dod_checked": True,
                           "scope_checked": True, "findings_reviewed": True,
                           "source_snapshot": self.run["source_snapshot"], "output_digest": self.result["output_digest"],
                           "evidence": "reviews/unit.md"}}

    def prepare(self):
        (self.root / "out").mkdir(exist_ok=True)
        prepared = self.change({"action": "integration-prepare", "integration_id": "integration-a",
                                "unit_id": "a", "attempt_id": "attempt-001", "preflight": self.attempt,
                                "result": self.result, "target_scope": "out"})
        self.proof = prepared["private_integration"]

    def integration_review(self, decision="accept"):
        _, actual = planner.integration_inventory(self.run, self.project, "out")
        return {"reviewer": "synthetic-reviewer", "decision": decision, "diff_checked": True,
                "scope_checked": True, "conflicts_checked": True, "findings_reviewed": True,
                "effects_known": True, "after_digest": planner.digest_json(actual), "evidence": "reviews/unit.md"}

    def confirm(self):
        self.change({"action": "integration-confirm", "integration_id": "integration-a", "proof": self.proof,
                     "preflight": self.attempt, "result": self.result, "review": self.integration_review()})

    def integrate(self):
        self.prepare()
        # Explicit fake platform action, not a helper executor or real repository operation.
        import shutil
        for path in self.result["changed_files"]:
            shutil.copy2(self.worker / path, self.root / path)
        self.confirm()

    def test_ready_start_reservation_and_no_dispatch(self):
        self.start()
        self.assertEqual(self.run["reservations"], ["a"])
        self.assertEqual(self.run["capacity"]["active_workers"], 1)
        self.assertEqual(self.run["checkpoint"]["active_tasks"], ["TASK-001"])
        self.assertEqual(self.run["revision"], 2)
        self.assertEqual(self.attempt["attempt_id"], "attempt-001")
        self.fail({"action": "start", "unit_id": "a", "attempt_id": "attempt-001", "observation": self.obs})

    def test_revision_owner_lock_and_invalid_bytes_unchanged(self):
        self.fail({"action": "ready", "unit_id": "a"}, revision=1)
        self.fail({"action": "ready", "unit_id": "a"}, owner="foreign")
        self.fail({"action": "ready", "unit_id": "a", "force": True})
        lock = self.runroot / ".update.lock"
        lock.write_text("existing lock, never remove automatically")
        self.fail({"action": "ready", "unit_id": "a"})
        self.assertTrue(lock.exists())

    def test_submission_sealed_duplicate_and_acceptance_separate(self):
        self.start()
        self.submit()
        self.assertEqual(self.u["state"], "submitted")
        self.fail({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                   "preflight": self.attempt, "result": self.result})
        request = self.review()
        request["result"] = copy.deepcopy(self.result)
        request["result"]["findings"] = ["changed disclosure"]
        self.fail(request)
        self.change(self.review())
        self.assertEqual(self.u["state"], "accepted")
        self.assertEqual(self.run["reservations"], [])
        self.assertEqual(self.run["checkpoint"]["active_tasks"], ["TASK-001"])
        self.assertEqual(self.run["checkpoint"]["completed_since_checkpoint"], 0)

    def test_cancel_unknown_liveness_retains_capacity_and_parent(self):
        self.start()
        self.change({"action": "cancel-request", "unit_id": "a", "attempt_id": "attempt-001"})
        self.assertEqual(self.u["state"], "running")
        value = planner.reconcile(self.run, self.observation("unknown"))
        self.assertTrue(value["rows"][0]["reservation_retained"])
        self.fail({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                   "observations": self.observation("unknown")})
        self.fail({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                   "observations": self.observation("stopped", False)})
        self.change({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                     "observations": self.observation()})
        self.assertEqual(self.u["state"], "cancelled")
        self.assertEqual(self.run["capacity"]["active_workers"], 0)
        self.assertEqual(self.run["checkpoint"]["active_tasks"], ["TASK-001"])

    def test_missing_observations_and_partial_writes_block_reuse(self):
        self.start()
        self.assertTrue(planner.reconcile(self.run, [])["rows"][0]["reservation_retained"])
        (self.worker / "extra.txt").write_text("forbidden write")
        self.assertFalse(planner.reconcile(self.run, self.observation())["rows"][0]["effects_known"])
        self.fail({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                   "observations": self.observation()})

    def test_retry_consumes_existing_parent_ceiling(self):
        self.start()
        self.change({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                     "observations": self.observation()})
        self.fail({"action": "retry", "unit_id": "a", "observations": self.observation()})
        self.fail({"action": "retry", "unit_id": "a", "observations": []})
        (self.project / "decisions").mkdir()
        proof = self.project / "decisions/parent-budget.json"
        proof.write_text(json.dumps({"schema": 1, "project": self.run["project"],
                                    "coordinator_id": self.run["coordinator_id"], "retry_limit": 1}))
        self.run["lifecycle"]["parent_retry_budget"] = {"limit": 1, "reference": "decisions/parent-budget.json",
                                                       "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()}
        self.save()
        self.change({"action": "retry", "unit_id": "a", "observations": self.observation()})
        self.assertEqual(self.run["lifecycle"]["retry_counts"], {"TASK-001": 1})
        self.fail({"action": "start", "unit_id": "a", "attempt_id": "attempt-001", "observation": self.obs})
        self.change({"action": "start", "unit_id": "a", "attempt_id": "attempt-002", "observation": self.obs})

    def test_retry_budget_exhaustion_after_second_terminal_attempt(self):
        self.start()
        self.change({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-001",
                     "observations": self.observation()})
        (self.project / "decisions").mkdir()
        proof = self.project / "decisions/budget.json"
        proof.write_text(json.dumps({"schema": 1, "project": self.run["project"],
                                    "coordinator_id": self.run["coordinator_id"], "retry_limit": 1}))
        self.run["lifecycle"]["parent_retry_budget"] = {"limit": 1, "reference": "decisions/budget.json",
                                                       "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()}
        self.save()
        self.change({"action": "retry", "unit_id": "a", "observations": self.observation()})
        new = self.change({"action": "start", "unit_id": "a", "attempt_id": "attempt-002", "observation": self.obs})
        observations = [{"attempt_id": "attempt-002", "handle": "handle-a", "status": "stopped",
                         "effects_known": True, "preflight": new["private_preflight"]}]
        self.change({"action": "cancel", "unit_id": "a", "attempt_id": "attempt-002", "observations": observations})
        self.fail({"action": "retry", "unit_id": "a", "observations": observations})

    def test_accepted_output_drift_reconciliation_proposes_invalidation(self):
        self.start()
        self.submit()
        self.change(self.review())
        before = (self.runroot / "manifest.json").read_bytes()
        (self.worker / "out/result.txt").write_text("changed after acceptance")
        observed = planner.reconcile(self.run, self.observation())["rows"][0]
        self.assertTrue(observed["invalidation_recommended"])
        self.assertFalse(observed["effects_known"])
        self.assertTrue(observed["reservation_retained"])
        self.assertEqual((self.runroot / "manifest.json").read_bytes(), before)

    def test_parent_and_checkpoint_use_existing_quality_consumers(self):
        from unittest.mock import patch
        self.start()
        self.submit()
        self.change(self.review())
        self.integrate()
        # Only the parent-gate adapter is mocked: state/transaction checks are real.
        # The neighboring fake-quality test invokes the real fail-closed consumer.
        with patch.object(planner, "check_parent_gate") as gate:
            self.change({"action": "parent-complete", "task_id": "TASK-001",
                         "quality": "quality/current.md", "capture": "capture-state/current.md"})
            self.assertEqual(gate.call_count, 1)
            self.assertEqual(self.run["checkpoint"]["completed_since_checkpoint"], 1)
            (self.project / "checkpoints").mkdir()
            proof = self.project / "checkpoints/current.md"
            proof.write_text("Unfinished checkpoint from another epoch")
            self.fail({"action": "checkpoint", "evidence": "checkpoints/current.md",
                       "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()})
            proof.write_text(self.checkpoint_text())
            self.change({"action": "checkpoint", "evidence": "checkpoints/current.md",
                         "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()})
            self.assertEqual(gate.call_count, 2)
        self.assertEqual(self.run["checkpoint"]["completed_since_checkpoint"], 0)
        self.assertEqual(self.run["lifecycle"]["checkpoint_epoch"], 1)
        self.run["checkpoint"]["active_tasks"] = ["EMPTY-PARENT"]
        self.save()
        with patch.object(planner, "check_parent_gate") as gate:
            self.fail({"action": "parent-complete", "task_id": "EMPTY-PARENT",
                       "quality": "quality/current.md", "capture": "capture-state/current.md"})
            gate.assert_not_called()

    def test_competing_process_revisions_commit_only_once(self):
        program = ("import importlib.util,json,sys;sys.dont_write_bytecode=True;"
                   "s=importlib.util.spec_from_file_location('p',sys.argv[1]);"
                   "p=importlib.util.module_from_spec(s);s.loader.exec_module(p);"
                   "p.update_run(sys.argv[2],sys.argv[3],0,{'action':'ready','unit_id':'a'})")
        children = [subprocess.Popen([sys.executable, "-c", program, str(HERE / "parallel-orchestration.py"),
                                      str(self.runroot), self.run["coordinator_id"]],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for child in children:
            child.communicate(timeout=15)
        self.assertEqual(sum(c.returncode == 0 for c in children), 1)
        self.refresh()
        self.assertEqual(self.run["revision"], 1)
        self.assertEqual(len(self.run["lifecycle"]["events"]), 1)

    def checkpoint_text(self):
        return ("# Synthetic Checkpoint\n## Metadata\n- Project: example-project\n"
                "- Workflow phase: phase-7-checkpoint\n- Result: completed\n"
                "## Checkpoint Gate\n- Distillations processed atomically: yes\n"
                "- Memory updated without mechanical copy-paste: yes\n"
                "- Critical drift resolved or escalated: none\n"
                "- Can continue project workflow: yes\n- Blocking reason: none\n"
                "## Orchestration Checkpoint Binding\n- Run ID: run-001\n"
                "- Coordinator ID: " + self.run["coordinator_id"] + "\n- Epoch: 0\n"
                "- Source snapshot: " + self.run["source_snapshot"] + "\n"
                '- Completed tasks: ["TASK-001"]\n')

    def test_checkpoint_rejects_wrong_epoch_tasks_and_incomplete_gate(self):
        self.start()
        self.submit()
        self.change(self.review())
        self.integrate()
        from unittest.mock import patch
        with patch.object(planner, "check_parent_gate"):
            self.change({"action": "parent-complete", "task_id": "TASK-001",
                         "quality": "quality/current.md", "capture": "capture-state/current.md"})
        (self.project / "checkpoints").mkdir()
        proof = self.project / "checkpoints/other.md"
        for old, new in (("- Epoch: 0", "- Epoch: 1"), ('["TASK-001"]', '["TASK-OTHER"]'),
                         ("- Run ID: run-001", "- Run ID: run-other"),
                         ("- Result: completed", "- Result: blocked"),
                         ("Can continue project workflow: yes", "Can continue project workflow: no")):
            proof.write_text(self.checkpoint_text().replace(old, new))
            self.fail({"action": "checkpoint", "evidence": "checkpoints/other.md",
                       "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()})

    def test_completed_parent_invalidation_retains_slot_and_blocks_checkpoint(self):
        from unittest.mock import patch
        self.start()
        self.submit()
        self.change(self.review())
        self.integrate()
        with patch.object(planner, "check_parent_gate"):
            self.change({"action": "parent-complete", "task_id": "TASK-001",
                         "quality": "quality/current.md", "capture": "capture-state/current.md"})
        prior = copy.deepcopy(self.run["lifecycle"]["attempts"][0])
        self.change({"action": "invalidate", "unit_id": "a", "reason_digest": "f" * 64})
        self.assertEqual(self.u["state"], "blocked")
        self.assertEqual(self.run["lifecycle"]["completed_tasks"], [])
        self.assertEqual(self.run["lifecycle"]["parent_gates"], {})
        self.assertEqual(self.run["checkpoint"]["active_tasks"], ["TASK-001"])
        self.assertEqual(self.run["lifecycle"]["attempts"][0], prior)
        (self.project / "checkpoints").mkdir()
        proof = self.project / "checkpoints/completed.md"
        proof.write_text(self.checkpoint_text())
        with patch.object(planner, "check_parent_gate") as gate:
            self.fail({"action": "checkpoint", "evidence": "checkpoints/completed.md",
                       "sha256": __import__("hashlib").sha256(proof.read_bytes()).hexdigest()})
            gate.assert_not_called()

    def test_damaged_referenced_result_has_bounded_recovery_invalidation(self):
        self.start()
        self.submit()
        self.change(self.review())
        result = self.runroot / "results/attempt-001.json"
        broken = json.loads(result.read_text())
        broken["quality_ready"] = False
        result.write_text(json.dumps(broken))
        with self.assertRaises(planner.InvalidManifest):
            planner.inspect_run(self.runroot)
        observed, records = planner.inspect_run(self.runroot, recovery=True)
        self.assertIsNone(records["results/attempt-001.json"])
        before_attempt = copy.deepcopy(observed["lifecycle"]["attempts"][0])
        cli = subprocess.run([sys.executable, str(ROOT / ".systems/scripts/manage-parallel-run"),
                              "--run-root", str(self.runroot), "--coordinator-id", self.run["coordinator_id"],
                              "reconcile"], capture_output=True, text=True)
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertEqual(json.loads(cli.stdout)["damaged_result_attempts"], ["attempt-001"])
        self.assertFalse(json.loads(cli.stdout)["runtime_layout_complete"])
        self.change({"action": "invalidate", "unit_id": "a", "reason_digest": "f" * 64})
        self.assertEqual(self.u["state"], "blocked")
        self.assertEqual(self.run["lifecycle"]["attempts"][0], before_attempt)
        self.assertEqual(json.loads(result.read_text()), broken)

    def test_result_directory_synced_before_manifest_publication(self):
        from unittest.mock import patch
        self.start()
        self.result = self.result_value()
        synced = []
        real_fsync, real_replace = planner.os.fsync, planner.os.replace
        def tracked_fsync(fd):
            if __import__("stat").S_ISDIR(os.fstat(fd).st_mode):
                synced.append((os.fstat(fd).st_dev, os.fstat(fd).st_ino))
            real_fsync(fd)
        def checked_replace(old, new):
            result_dir = self.runroot / "results"
            self.assertIn((result_dir.stat().st_dev, result_dir.stat().st_ino), synced)
            real_replace(old, new)
        with patch.object(planner.os, "fsync", tracked_fsync), patch.object(planner.os, "replace", checked_replace):
            self.change({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                         "preflight": self.attempt, "result": self.result})

    def test_finished_attempt_immutable_invalidation_local_dependencies(self):
        self.start()
        self.submit()
        self.change(self.review())
        prior = copy.deepcopy(self.run["lifecycle"]["attempts"][0])
        self.add("dependent", dependencies=["a"], expected_inputs={"a": self.u["accepted_output"]})
        self.add("independent")
        self.save()
        self.change({"action": "invalidate", "unit_id": "a", "reason_digest": "f" * 64})
        self.assertEqual(self.run["lifecycle"]["attempts"][0], prior)
        self.assertEqual(self.run["units"][1]["state"], "blocked")
        self.assertEqual(self.run["units"][2]["state"], "planned")
        self.assertEqual(planner.plan(self.run)["proposed_units"], ["independent"])

    def test_parent_slots_block_fourth_and_unit_acceptance_is_not_parent_pass(self):
        self.run["checkpoint"]["active_tasks"] = ["TASK-OTHER", "TASK-SECOND", "TASK-THIRD"]
        self.save()
        self.fail({"action": "ready", "unit_id": "a"})
        self.run["checkpoint"]["active_tasks"] = []
        self.save()
        self.start()
        self.submit()
        self.change(self.review())
        self.integrate()
        self.fail({"action": "parent-complete", "task_id": "TASK-001",
                   "quality": "quality/fake.md", "capture": "capture-state/fake.md"})

    def test_crash_before_and_after_replace_preserves_atomic_event(self):
        from unittest.mock import patch
        before = (self.runroot / "manifest.json").read_bytes()
        with patch.object(planner.os, "replace", side_effect=OSError("crash before replace")):
            self.fail({"action": "ready", "unit_id": "a"})
        self.assertEqual((self.runroot / "manifest.json").read_bytes(), before)
        real_fsync = planner.os.fsync
        def fail_directory(fd):
            if __import__("stat").S_ISDIR(os.fstat(fd).st_mode):
                raise OSError("crash after replace")
            return real_fsync(fd)
        with patch.object(planner.os, "fsync", side_effect=fail_directory):
            with self.assertRaises(planner.InvalidManifest):
                self.change({"action": "ready", "unit_id": "a"})
        self.refresh()
        self.assertEqual(self.run["revision"], 1)
        self.assertEqual(self.run["lifecycle"]["events"][0]["revision"], 1)
        self.fail({"action": "ready", "unit_id": "a"}, revision=0)

    def test_orphan_result_after_submission_crash_is_not_adopted(self):
        from unittest.mock import patch
        self.start()
        self.result = self.result_value()
        with patch.object(planner.os, "replace", side_effect=OSError("before manifest replace")):
            self.fail({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                       "preflight": self.attempt, "result": self.result})
        orphan = self.runroot / "results/attempt-001.json"
        self.assertTrue(orphan.is_file())
        self.assertEqual(self.u["state"], "running")
        with self.assertRaises(planner.InvalidManifest):
            planner.inspect_run(self.runroot)
        manifest, records = planner.inspect_run(self.runroot, recovery=True)
        self.assertEqual(records, {})
        self.assertTrue(planner.recovery_layout(self.runroot, records))
        self.assertEqual(manifest["units"][0]["state"], "running")

    def test_runtime_inventory_exact_sanitized_and_drift(self):
        s = importlib.util.spec_from_file_location("lifecycle_scope", HERE / "validation-scope.py")
        scope = importlib.util.module_from_spec(s)
        s.loader.exec_module(scope)
        ws = self.project.parents[1]
        before = scope.inventory_runtime(ws, ["projects/example-project"])
        self.start()
        self.submit()
        after = scope.inventory_runtime(ws, ["projects/example-project"])
        self.assertNotEqual(before, after)
        paths = [p["path"] for p in after[0]["files"]]
        self.assertIn("projects/example-project/orchestration/runs/run-001/results/attempt-001.json", paths)
        self.assertFalse(any("worker" in p for p in paths))
        row = {"path": str(self.runroot.relative_to(self.root) / "manifest.json"), "sha256": "a" * 64}
        self.assertTrue(scope.owned_runtime_input(self.root, ws, ["projects/example-project"], row))
        result = self.runroot / "results/attempt-001.json"
        parsed = json.loads(result.read_text())
        self.assertNotIn("residual_risk", parsed)
        parsed["raw_log"] = "not permitted"
        result.write_text(json.dumps(parsed))
        with self.assertRaises(ValueError):
            scope.inventory_runtime(ws, ["projects/example-project"])

    def test_unknown_runtime_files_links_and_locks_reject_inventory(self):
        s = importlib.util.spec_from_file_location("lifecycle_scope", HERE / "validation-scope.py")
        scope = importlib.util.module_from_spec(s)
        s.loader.exec_module(scope)
        ws = self.project.parents[1]
        foreign = self.runroot / "raw.log"
        foreign.write_text("not ingested")
        with self.assertRaises(ValueError):
            scope.inventory_runtime(ws, ["projects/example-project"])
        foreign.unlink()
        foreign.symlink_to(self.worker / "input.txt")
        with self.assertRaises(ValueError):
            scope.inventory_runtime(ws, ["projects/example-project"])
        foreign.unlink()
        (self.runroot / ".update.lock").write_text("stale")
        with self.assertRaises(ValueError):
            scope.inventory_runtime(ws, ["projects/example-project"])

    def test_foreign_runtime_ancestors_and_manifest_inode_alias_rejected(self):
        for parent in (self.runroot.parent, self.runroot.parent.parent, self.project.parents[1]):
            marker = parent / ".git"
            marker.mkdir()
            with self.assertRaises(planner.InvalidManifest):
                planner.inspect_run(self.runroot)
            marker.rmdir()
        alias = self.root / "foreign-manifest.json"
        os.link(self.runroot / "manifest.json", alias)
        with self.assertRaises(planner.InvalidManifest):
            planner.inspect_run(self.runroot)


    def test_actual_process_crash_before_and_after_atomic_replace(self):
        original = (self.runroot / "manifest.json").read_bytes()
        for when, code in (("before", 77), ("after", 78)):
            if when == "after":
                # A separate fixture, not cleanup of an active production run.
                self.runroot = self.project / "orchestration/runs/run-002"
                self.runroot.mkdir()
                self.run["run_id"] = "run-002"
                self.save()
            before = (self.runroot / "manifest.json").read_bytes()
            program = (
                "import importlib.util,os,sys;sys.dont_write_bytecode=True;"
                "s=importlib.util.spec_from_file_location('p',sys.argv[1]);"
                "p=importlib.util.module_from_spec(s);s.loader.exec_module(p);"
                "original=p.os.replace;"
                "exec('def crashed(a,b):\\n "
                + ("os._exit(77)" if when == "before" else "original(a,b);os._exit(78)")
                + "');p.os.replace=crashed;"
                "p.update_run(sys.argv[2],sys.argv[3],0,{'action':'ready','unit_id':'a'})")
            result = subprocess.run([sys.executable, "-c", program, str(HERE / "parallel-orchestration.py"),
                                     str(self.runroot), self.run["coordinator_id"]], capture_output=True)
            self.assertEqual(result.returncode, code, result.stderr.decode())
            self.assertTrue((self.runroot / ".update.lock").exists())
            after = (self.runroot / "manifest.json").read_bytes()
            if when == "before":
                self.assertEqual(before, after)
            else:
                parsed = json.loads(after)
                self.assertEqual(parsed["revision"], 1)
                self.assertEqual(parsed["lifecycle"]["events"][0]["revision"], 1)
            cli = subprocess.run([sys.executable, str(ROOT / ".systems/scripts/manage-parallel-run"),
                                  "--run-root", str(self.runroot), "--coordinator-id", self.run["coordinator_id"],
                                  "reconcile"], capture_output=True, text=True)
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertTrue(json.loads(cli.stdout)["update_lock_present"])
            self.assertEqual((self.runroot / "manifest.json").read_bytes(), after)
            self.assertTrue((self.runroot / ".update.lock").exists())


    def test_cli_invalid_request_has_no_success(self):
        request = self.root / "request.json"
        request.write_text('{"action":"ready","unit_id":"a","force":true}')
        before = (self.runroot / "manifest.json").read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / ".systems/scripts/manage-parallel-run"),
                                 "--run-root", str(self.runroot), "--coordinator-id", self.run["coordinator_id"],
                                 "--expected-revision", "0", "--request", str(request), "transition"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual((self.runroot / "manifest.json").read_bytes(), before)


class IntegrationTests(unittest.TestCase):
    setUp = LifecycleTests.setUp
    add = PlannerTests.add
    save = LifecycleTests.save
    refresh = LifecycleTests.refresh
    change = LifecycleTests.change
    fail = LifecycleTests.fail
    start = LifecycleTests.start
    submit = LifecycleTests.submit
    result_value = LifecycleTests.result_value
    review = LifecycleTests.review
    prepare = LifecycleTests.prepare
    confirm = LifecycleTests.confirm
    integrate = LifecycleTests.integrate
    integration_review = LifecycleTests.integration_review

    def accepted(self):
        self.start()
        self.submit()
        self.change(self.review())

    def test_submitted_not_integrated_and_persisted_serial_reservation(self):
        self.start()
        self.submit()
        self.fail({"action": "integration-prepare", "integration_id": "integration-a", "unit_id": "a",
                   "attempt_id": "attempt-001", "preflight": self.attempt, "result": self.result, "target_scope": "out"})
        self.change(self.review())
        self.add("independent", write_set=["other"])
        self.save()
        self.prepare()
        self.assertFalse((self.root / "out/result.txt").exists())
        self.assertEqual(planner.plan(self.run)["selected_count"], 0)
        self.fail({"action": "ready", "unit_id": "independent"})
        self.fail({"action": "parent-complete", "task_id": "TASK-001", "quality": "quality/fake.md", "capture": "capture-state/fake.md"})
        self.assertEqual(planner.reconcile(self.run, [])["integration_reservations"], ["integration-a"])
        before = (self.runroot / "manifest.json").read_bytes()
        command = [sys.executable, str(ROOT / ".systems/scripts/manage-parallel-run"), "--run-root", str(self.runroot),
                   "--coordinator-id", self.run["coordinator_id"], "reconcile"]
        output = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertEqual(json.loads(output.stdout)["integration_reservations"], ["integration-a"])
        self.assertEqual((self.runroot / "manifest.json").read_bytes(), before)

    def test_actual_integration_is_separate_from_common_quality(self):
        self.accepted()
        prior = copy.deepcopy(self.run["lifecycle"]["attempts"])
        self.integrate()
        self.assertEqual(self.run["lifecycle"]["attempts"], prior)
        self.assertEqual(self.run["lifecycle"]["integrations"][0]["state"], "verified")
        self.assertEqual(self.run["checkpoint"]["completed_since_checkpoint"], 0)
        self.fail({"action": "parent-complete", "task_id": "TASK-001", "quality": "quality/fake.md", "capture": "capture-state/fake.md"})
        self.assertEqual((self.root / "out/result.txt").read_text(), "result")
        (self.root / "out/result.txt").write_text("integration-only regression")
        from unittest.mock import patch
        with patch.object(planner, "check_parent_gate") as gate:
            self.fail({"action": "parent-complete", "task_id": "TASK-001", "quality": "quality/fake.md", "capture": "capture-state/fake.md"})
            gate.assert_not_called()

    def test_conflict_and_proof_tampering_reject_without_integration(self):
        self.accepted()
        (self.root / "out").mkdir()
        (self.root / "out/result.txt").write_text("concurrent destination work")
        self.fail({"action": "integration-prepare", "integration_id": "integration-a", "unit_id": "a",
                   "attempt_id": "attempt-001", "preflight": self.attempt, "result": self.result, "target_scope": "out"})
        (self.root / "out/result.txt").unlink()
        self.prepare()
        proof = copy.deepcopy(self.proof)
        proof["expected_files"] = proof["before_files"]
        self.fail({"action": "integration-confirm", "integration_id": "integration-a", "proof": proof,
                   "preflight": self.attempt, "result": self.result, "review": self.integration_review()})
        self.assertEqual(self.run["lifecycle"]["integrations"][0]["state"], "pending")

    def test_partial_abandonment_retains_parent_and_blocks_dependents(self):
        import shutil
        self.accepted()
        prior = copy.deepcopy(self.run["lifecycle"]["attempts"])
        self.add("dependent", dependencies=["a"], expected_inputs={"a": self.u["accepted_output"]})
        self.add("independent", write_set=["other"])
        self.save()
        self.prepare()
        shutil.copy2(self.worker / "out/result.txt", self.root / "out/result.txt")
        (self.root / "out/result.txt").write_text("unknown partial value")
        request = {"action": "integration-abandon", "integration_id": "integration-a", "proof": self.proof,
                   "review": self.integration_review("abandon")}
        self.fail(request)
        shutil.copy2(self.worker / "out/result.txt", self.root / "out/result.txt")
        request["review"] = self.integration_review("abandon")
        self.change(request)
        self.assertEqual(self.run["lifecycle"]["integrations"][0]["state"], "abandoned")
        self.assertEqual(self.run["lifecycle"]["attempts"], prior)
        self.assertEqual(self.run["checkpoint"]["active_tasks"], ["TASK-001"])
        self.assertEqual(self.run["units"][1]["state"], "blocked")
        self.assertEqual(planner.plan(self.run)["proposed_units"], ["independent"])
        self.assertEqual((self.root / "out/result.txt").read_text(), "result")

    def test_no_change_abandonment_after_explicit_invalidation(self):
        self.accepted()
        self.prepare()
        self.change({"action": "invalidate", "unit_id": "a", "reason_digest": "f" * 64})
        self.assertEqual(self.run["lifecycle"]["integrations"][0]["state"], "blocked")
        self.change({"action": "integration-abandon", "integration_id": "integration-a", "proof": self.proof,
                     "review": self.integration_review("abandon")})
        self.assertEqual(self.run["lifecycle"]["integrations"][0]["state"], "abandoned")

    def test_deletion_mode_and_unrelated_target_entries_are_covered(self):
        import shutil
        (self.worker / "out/delete.txt").write_text("old")
        (self.worker / "out/mode.txt").write_text("same bytes")
        (self.root / "out").mkdir()
        for name in ("delete.txt", "mode.txt"):
            shutil.copy2(self.worker / "out" / name, self.root / "out" / name)
        (self.root / "out/unrelated.txt").write_text("keep unrelated target")
        self.start()
        self.result = self.result_value()
        (self.worker / "out/delete.txt").unlink()
        (self.worker / "out/mode.txt").chmod(0o700)
        actual = planner.file_inventory(self.worker)
        self.result["changed_files"] = sorted(p for p in set(actual) | set(self.attempt["baseline_files"])
                                             if actual.get(p) != self.attempt["baseline_files"].get(p))
        self.result["output_digest"] = planner.digest_json(actual)
        self.change({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001", "preflight": self.attempt, "result": self.result})
        self.change(self.review())
        self.prepare()
        for path in self.result["changed_files"]:
            if (self.worker / path).exists():
                shutil.copy2(self.worker / path, self.root / path)
            else:
                (self.root / path).unlink()
        (self.root / "out/unrelated.txt").write_text("hidden extra write")
        self.fail({"action": "integration-confirm", "integration_id": "integration-a", "proof": self.proof,
                   "preflight": self.attempt, "result": self.result, "review": self.integration_review()})
        (self.root / "out/unrelated.txt").write_text("keep unrelated target")
        self.confirm()
        self.assertEqual((self.root / "out/mode.txt").stat().st_mode & 0o777, 0o700)
        self.assertFalse((self.root / "out/delete.txt").exists())

    def test_dependency_delivery_verifies_separate_actual_copy_and_modes(self):
        import shutil
        self.accepted()
        path = "out/result.txt"
        producer = planner.file_inventory(self.worker)
        consumer = self.add("consumer", read_set=[path], write_set=["other"], dependencies=["a"],
                            expected_inputs={"a": self.u["accepted_output"]})
        consumer["execution"] = {"input_hashes": {path: producer[path]["sha256"]}, "required_checks": ["consumer-check"],
                                 "stop_conditions": ["input drift"], "minimal_context": [path]}
        self.save()
        other = self.root.parent / (self.root.name + "-consumer")
        other.mkdir()
        self.addCleanup(lambda: shutil.rmtree(other))
        (other / "out").mkdir()
        shutil.copy2(self.worker / path, other / path)
        observation = {**self.obs, "handle": "handle-consumer", "cwd": str(other), "writable_roots": [str(other)]}
        _, records = planner.inspect_run(self.runroot)
        def delivered():
            return planner.verify_dependency_delivery(self.run, "consumer", "a", self.attempt, self.result, records, observation, [path])
        self.assertFalse(delivered()["execution_authorized"])
        self.change({"action": "ready", "unit_id": "consumer"})
        request = {"action": "start", "unit_id": "consumer", "attempt_id": "attempt-consumer",
                   "observation": observation}
        self.fail(request)
        request["dependency_deliveries"] = {"a": {"preflight": self.attempt, "result": self.result, "paths": [path]}}
        (other / path).chmod(0o700)
        with self.assertRaises(planner.InvalidManifest):
            delivered()
        self.fail(request)
        shutil.copy2(self.worker / path, other / path)
        self.run["units"][1]["task_id"] = "OTHER-TASK"
        with self.assertRaises(planner.InvalidManifest):
            delivered()
        self.run["units"][1]["task_id"] = "TASK-001"
        (self.worker / path).write_text("stale accepted output")
        with self.assertRaises(planner.InvalidManifest):
            delivered()
        self.fail(request)
        (self.worker / path).write_text("result")
        self.change(request)
        self.assertEqual(self.run["units"][1]["state"], "running")

    def test_unsafe_boundary_and_missing_review_do_not_release(self):
        self.accepted()
        (self.root / "out").mkdir()
        (self.root / "out/.git").mkdir()
        self.fail({"action": "integration-prepare", "integration_id": "integration-a", "unit_id": "a",
                   "attempt_id": "attempt-001", "preflight": self.attempt, "result": self.result, "target_scope": "out"})
        (self.root / "out/.git").rmdir()
        self.prepare()
        review = self.integration_review("abandon")
        review["effects_known"] = False
        self.fail({"action": "integration-abandon", "integration_id": "integration-a", "proof": self.proof, "review": review})
        self.assertTrue(planner.integration_pending(self.run))

    def test_root_replacement_and_stale_review_fail_closed(self):
        import shutil
        self.accepted()
        self.prepare()
        for path in self.result["changed_files"]:
            shutil.copy2(self.worker / path, self.root / path)
        review = self.integration_review()
        review["after_digest"] = "f" * 64
        self.fail({"action": "integration-confirm", "integration_id": "integration-a", "proof": self.proof,
                   "preflight": self.attempt, "result": self.result, "review": review})
        (self.root / "out").rename(self.root / "old-out")
        shutil.copytree(self.root / "old-out", self.root / "out")
        self.fail({"action": "integration-confirm", "integration_id": "integration-a", "proof": self.proof,
                   "preflight": self.attempt, "result": self.result, "review": self.integration_review()})
        self.assertTrue(planner.integration_pending(self.run))

    def test_crash_after_prepare_reservation_and_review_drift(self):
        from unittest.mock import patch
        self.accepted()
        (self.root / "out").mkdir()
        real_replace = planner.os.replace
        def crash(a, b):
            real_replace(a, b)
            raise OSError("uncertain integration acknowledgement")
        with patch.object(planner.os, "replace", side_effect=crash):
            with self.assertRaises(OSError):
                self.prepare()
        self.refresh()
        self.assertTrue(planner.integration_pending(self.run))
        self.fail({"action": "integration-prepare", "integration_id": "second", "unit_id": "a",
                   "attempt_id": "attempt-001", "preflight": self.attempt, "result": self.result, "target_scope": "out"})

    def test_confirmed_review_must_remain_current(self):
        self.accepted()
        self.integrate()
        (self.project / "reviews/unit.md").write_text("changed review")
        self.fail({"action": "parent-complete", "task_id": "TASK-001",
                   "quality": "quality/fake.md", "capture": "capture-state/fake.md"})

    def test_confirmed_destination_replacement_blocks_parent_and_checkpoint(self):
        import shutil
        from unittest.mock import patch
        self.accepted()
        self.integrate()
        (self.root / "out").rename(self.root / "old-out")
        shutil.copytree(self.root / "old-out", self.root / "out")
        with patch.object(planner, "check_parent_gate") as gate:
            self.fail({"action": "parent-complete", "task_id": "TASK-001",
                       "quality": "quality/fake.md", "capture": "capture-state/fake.md"})
            gate.assert_not_called()
        with self.assertRaises(planner.InvalidManifest):
            planner.check_integrated_parent(self.project, self.run, "TASK-001")

    def consumer_delivery(self, hashed_paths, read_set):
        import shutil
        other = self.root.parent / (self.root.name + "-consumer")
        other.mkdir()
        self.addCleanup(lambda: shutil.rmtree(other))
        shutil.copytree(self.worker / "out", other / "out")
        shutil.copy2(self.worker / "input.txt", other / "input.txt")
        consumer = self.add("consumer", read_set=read_set, write_set=["other"], dependencies=["a"],
                            expected_inputs={"a": self.u["accepted_output"]})
        inventory = planner.file_inventory(other)
        consumer["execution"] = {"input_hashes": {p: inventory[p]["sha256"] for p in hashed_paths},
                                 "required_checks": ["consumer-check"], "stop_conditions": ["input drift"],
                                 "minimal_context": hashed_paths}
        self.save()
        observation = {**self.obs, "handle": "handle-consumer", "cwd": str(other), "writable_roots": [str(other)]}
        _, records = planner.inspect_run(self.runroot)
        return other, consumer, observation, records

    def test_counterfeit_required_output_cannot_hide_behind_unrelated_delivery(self):
        self.accepted()
        other, consumer, observation, records = self.consumer_delivery(
            ["input.txt", "out/result.txt"], ["input.txt", "out/result.txt"])
        (other / "out/result.txt").write_text("counterfeit pinned input")
        consumer["execution"]["input_hashes"]["out/result.txt"] = planner.file_inventory(other)["out/result.txt"]["sha256"]
        self.save()
        self.change({"action": "ready", "unit_id": "consumer"})
        request = {"action": "start", "unit_id": "consumer", "attempt_id": "consumer-attempt",
                   "observation": observation, "dependency_deliveries": {
                       "a": {"preflight": self.attempt, "result": self.result, "paths": ["input.txt"]}}}
        self.fail(request)
        request["dependency_deliveries"]["a"]["paths"].append("out/result.txt")
        self.fail(request)

    def test_directory_delivery_requires_unchanged_outputs_and_deletion_tombstones(self):
        (self.worker / "out/unchanged.txt").write_text("unchanged owned output")
        (self.worker / "out/deleted.txt").write_text("deleted by producer")
        self.start()
        self.result = self.result_value()
        (self.worker / "out/deleted.txt").unlink()
        self.result["changed_files"] = sorted(self.result["changed_files"] + ["out/deleted.txt"])
        self.result["output_digest"] = planner.digest_json(planner.file_inventory(self.worker))
        self.change({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                     "preflight": self.attempt, "result": self.result})
        self.change(self.review())
        paths = ["out/check.txt", "out/result.txt", "out/unchanged.txt"]
        other, consumer, observation, records = self.consumer_delivery(paths, ["out"])
        def delivered(values):
            return planner.verify_dependency_delivery(self.run, "consumer", "a", self.attempt,
                                                      self.result, records, observation, values)
        with self.assertRaises(planner.InvalidManifest):
            delivered(paths[:2])
        (other / "out/deleted.txt").write_text("resurrected prior output")
        with self.assertRaises(planner.InvalidManifest):
            delivered(paths)
        (other / "out/deleted.txt").unlink()
        (other / "out").chmod(0o700)
        with self.assertRaises(planner.InvalidManifest):
            delivered(paths)
        (other / "out").chmod((self.worker / "out").stat().st_mode & 0o777)
        self.assertFalse(delivered(paths)["execution_authorized"])

    def test_intended_target_directory_mode_and_unintended_mode(self):
        import shutil
        (self.root / "out").mkdir()
        (self.root / "out").chmod((self.worker / "out").stat().st_mode & 0o777)
        self.start()
        self.result = self.result_value()
        (self.worker / "out").chmod(0o700)
        actual = planner.file_inventory(self.worker)
        self.result["changed_files"].insert(0, "out")
        self.result["output_digest"] = planner.digest_json(actual)
        self.change({"action": "submit", "unit_id": "a", "attempt_id": "attempt-001",
                     "preflight": self.attempt, "result": self.result})
        self.change(self.review())
        self.prepare()
        for path in self.result["changed_files"][1:]:
            shutil.copy2(self.worker / path, self.root / path)
        (self.root / "out").chmod(0o711)
        self.fail({"action": "integration-confirm", "integration_id": "integration-a", "proof": self.proof,
                   "preflight": self.attempt, "result": self.result, "review": self.integration_review()})
        (self.root / "out").chmod(0o700)
        self.confirm()

    def test_directory_delivery_rejects_extra_consumer_entries(self):
        self.accepted()
        paths = ["out/check.txt", "out/result.txt"]
        other, consumer, observation, records = self.consumer_delivery(paths, ["out"])
        self.change({"action": "ready", "unit_id": "consumer"})
        request = {"action": "start", "unit_id": "consumer", "attempt_id": "consumer-attempt",
                   "observation": observation, "dependency_deliveries": {
                       "a": {"preflight": self.attempt, "result": self.result, "paths": paths}}}
        for extra in (other / "out/injected.txt", other / "out/empty-extra"):
            if extra.suffix:
                extra.write_text("not in accepted snapshot")
            else:
                extra.mkdir()
            self.fail(request)
            if extra.is_dir():
                extra.rmdir()
            else:
                extra.unlink()
        (other / "unrelated.txt").write_text("outside producer namespace")
        self.change(request)
        self.assertEqual(self.run["units"][1]["state"], "running")

    def test_next_integration_cannot_absorb_prior_destination_or_review_drift(self):
        import shutil
        self.accepted()
        self.integrate()
        other = self.root.parent / (self.root.name + "-second")
        other.mkdir()
        self.addCleanup(lambda: shutil.rmtree(other))
        shutil.copytree(self.root / "out", other / "out")
        shutil.copy2(self.worker / "input.txt", other / "input.txt")
        self.add("b", read_set=["input.txt"], write_set=["out/b.txt"],
                 execution=copy.deepcopy(self.u["execution"]))
        self.save()
        self.change({"action": "ready", "unit_id": "b"})
        observation = {**self.obs, "handle": "handle-b", "cwd": str(other), "writable_roots": [str(other)]}
        private = self.change({"action": "start", "unit_id": "b", "attempt_id": "attempt-b",
                               "observation": observation})["private_preflight"]
        private["termination_verified"] = True
        (other / "out/b.txt").write_text("second accepted output")
        output = planner.file_inventory(other)
        result = {**self.result, "unit_id": "b", "attempt_id": "attempt-b", "handle": "handle-b",
                  "baseline_digest": private["baseline_digest"], "output_digest": planner.digest_json(output),
                  "changed_files": ["out/b.txt"]}
        self.change({"action": "submit", "unit_id": "b", "attempt_id": "attempt-b",
                     "preflight": private, "result": result})
        review = self.review()
        review.update(unit_id="b", attempt_id="attempt-b", preflight=private, result=result)
        review["review"]["output_digest"] = result["output_digest"]
        self.change(review)
        request = {"action": "integration-prepare", "integration_id": "integration-b", "unit_id": "b",
                   "attempt_id": "attempt-b", "preflight": private, "result": result, "target_scope": "out"}
        (self.root / "out/result.txt").write_text("unreviewed prior drift")
        self.fail(request)
        (self.root / "out/result.txt").write_text("result")
        prior_review = (self.project / "reviews/unit.md").read_bytes()
        (self.project / "reviews/unit.md").write_text("unreviewed prior evidence drift")
        self.fail(request)
        (self.project / "reviews/unit.md").write_bytes(prior_review)
        proof = self.change(request)["private_integration"]
        shutil.copy2(other / "out/b.txt", self.root / "out/b.txt")
        self.change({"action": "integration-confirm", "integration_id": "integration-b", "proof": proof,
                     "preflight": private, "result": result, "review": self.integration_review()})
        planner.check_integrated_parent(self.project, self.run, "TASK-001")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("planner", "protocol", "lifecycle", "integration", "compatibility"), required=True)
    args = parser.parse_args()
    cls = {"planner": PlannerTests, "protocol": ProtocolTests, "lifecycle": LifecycleTests, "integration": IntegrationTests,
           "compatibility": CompatibilityTests}[args.case]
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    if args.case == 'compatibility' and result.wasSuccessful():
        print(json.dumps({'evidence_kind': 'offline-threaded-synthetic-only', 'native_backend_verified': False,
                          'model_speedup_claim': False, 'samples': CompatibilityTests.samples}, sort_keys=True))
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main())
