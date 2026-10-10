#!/usr/bin/env python3
"""Behavioral/adversarial tests on disposable synthetic evidence."""
import copy
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

ROOT = Path(__file__).resolve().parents[3]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


eff = module("eff_tests", ROOT / ".systems/scripts/lib/execution-efficiency.py")
producer = module("quality_tests", ROOT / ".systems/scripts/lib/quality-record.py")
qa = producer.qa
COMPLETENESS = """- Status: complete
- Reviewed baseline: synthetic supplied review
- Closure freshness: current
- Post-fix full re-review: not-required
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Required-field mapping: complete"""
ARTIFACT = """- Owner intent and governing sources reviewed: synthetic owner scope and source
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned
- Post-fix full artifact re-review: not-required
- Evidence reviewed: synthetic source and test
- Skipped or unreadable sources: none
- Residual risk: synthetic artifact only
- Closure freshness: current"""


def supplied_review(kind="spec-qa"):
    sections = {
        "Evidence": "- Manual-checks: supplied synthetic semantic assessment.",
        "Review Completeness Gate": COMPLETENESS,
        "QA Verification Scope": "- QA subject: synthetic artifact",
        "Artifact QA Completeness Gate": ARTIFACT,
        "Findings": "- Blockers: none\n- Unresolved findings: none",
        "Gate Decision": "- QA result: PASS\n- Can proceed: yes\n- Required next phase: phase-4-implementation",
    }
    if kind == "final-check":
        sections.pop("Artifact QA Completeness Gate")
        sections["Completion Review"] = "| Area | Result | Evidence |\n| --- | --- | --- |\n| Scope | PASS | supplied synthetic review |"
        sections["Owner Approval"] = "- Technical final check result: PASS\n- Owner approval required: yes\n- Owner decision: awaiting"
        sections["Final Gate"] = "- Can close active plan: awaiting-owner\n- Required next phase: owner approval"
    return {"schema": 1, "kind": kind, "task": "EFF-001" if kind == "spec-qa" else None,
            "run_id": "synthetic-run-001", "verdict": "PASS", "date": "2026-10-02",
            "inputs": [{"root": "owning-project-evidence", "path": "context.md"}], "sections": sections}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        # Synthetic iteration probes are not the enclosing CI validation run.
        self.ci_environment = patch.dict(os.environ, {"CI": ""})
        self.ci_environment.start()
        self.addCleanup(self.ci_environment.stop)
        self.tmp = tempfile.TemporaryDirectory(prefix="eff-tests-")
        self.root = Path(self.tmp.name).resolve()
        self.workspace = self.root / "workspace"
        self.project = self.workspace / "projects/synthetic"
        (self.project / "quality").mkdir(parents=True)
        (self.project / "decisions").mkdir()
        (self.project / "context.md").write_text("Accepted synthetic DoD and source.")
        self.key = b"isolated-synthetic-key-at-least-32-bytes"

    def tearDown(self):
        self.tmp.cleanup()

    def receipt(self):
        value = {"schema": 1, "run_id": "source-run", "state": "completed", "exit_code": 0, "binding": "a"}
        value["authentication"] = eff.sign(value, self.key)
        return value

    def test_authenticated_success_reuses_without_child(self):
        result = eff.execute_bound(["invalid-never-executed"], "a", self.receipt(), self.key, cwd=self.root, timeout=1)
        self.assertEqual(result["execution"], "reused")
        self.assertEqual(result["source_run_id"], "source-run")

    def test_changed_binding_executes_failure_instead_of_reusing(self):
        result = eff.execute_bound([sys.executable, "-c", "raise SystemExit(7)"], "b", self.receipt(), self.key, cwd=self.root, timeout=2)
        self.assertEqual(result["exit_code"], 7)
        self.assertEqual(result["execution"], "invalidated")

    def test_timeout_stops_child_and_cannot_supply_success(self):
        result = eff.execute_bound([sys.executable, "-c", "import time; time.sleep(20)"], "new", None,
                                   self.key, cwd=self.root, timeout=0.05)
        self.assertEqual(result["exit_code"], 124)
        self.assertEqual(result["state"], "failed")

    def test_forged_receipt_rejected(self):
        record = self.receipt()
        record["binding"] = "forged"
        with self.assertRaisesRegex(ValueError, "authentication"):
            eff.verify_record(record, self.key)

    def test_failed_interrupted_timeout_incomplete_evidence_rejected(self):
        for state, code in (("failed", 1), ("failed", 124), ("failed", 130), ("started", 0)):
            with self.subTest(state=state, code=code):
                record = self.receipt()
                record.update(state=state, exit_code=code)
                record["authentication"] = eff.sign(record, self.key)
                with self.assertRaisesRegex(ValueError, "incomplete or failed"):
                    eff.verify_record(record, self.key)

    def test_private_key_and_link_boundaries(self):
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        self.assertEqual(eff.key_bytes(key), self.key)
        key.chmod(0o644)
        with self.assertRaisesRegex(ValueError, "owner-only"):
            eff.key_bytes(key)
        link = self.root / "key-link"
        link.symlink_to(key)
        with self.assertRaisesRegex(ValueError, "linked"):
            eff.key_bytes(link)

    def test_fifo_key_rejected_without_waiting_for_writer(self):
        fifo = self.root / "fifo-key"
        os.mkfifo(fifo, 0o600)
        probe = (
            "import importlib.util,sys; "
            "s=importlib.util.spec_from_file_location('fifo_probe',sys.argv[1]); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "m.key_bytes(sys.argv[2])"
        )
        result = subprocess.run([sys.executable, "-c", probe,
                                 str(ROOT / ".systems/scripts/lib/execution-efficiency.py"), str(fifo)],
                                cwd=ROOT, text=True, capture_output=True, timeout=2)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reuse key must be owner-only", result.stderr)

    def test_atomic_publish_no_clobber_and_link(self):
        output = self.root / "out.json"
        eff.publish(output, {"one": 1})
        with self.assertRaisesRegex(ValueError, "already exists"):
            eff.publish(output, {"two": 2})
        directory = self.root / "linked"
        directory.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "linked"):
            eff.publish(directory / "other.json", {})
        self.assertEqual(json.loads(output.read_text()), {"one": 1})

    def test_sensitive_traversal_and_missing_inputs_rejected(self):
        for relative in ("../context.md", ".env", "missing.md"):
            with self.subTest(relative=relative), self.assertRaises((ValueError, OSError)):
                eff.contained(self.root, relative)

    def test_unknown_plan_or_missing_dependency_rejected(self):
        plan = {"schema": 1, "purpose": "iteration", "workflow_root": str(ROOT),
                "scope_manifest": None, "checks": [{"id": "check-not-real"}]}
        plan_path = self.root / "plan.json"
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        for check in ("check-not-real", "check-status-consistency"):
            plan["checks"][0]["id"] = check
            plan_path.write_text(json.dumps(plan))
            with patch.object(eff, "preflight"), self.assertRaises(ValueError):
                eff.execute_plan(plan_path, self.root / "output.json", key)
        self.assertFalse((self.root / "output.json").exists())

    def test_full_and_ci_never_accept_iteration_reuse(self):
        path = self.root / "plan.json"
        path.write_text(json.dumps({"schema": 1, "purpose": "full", "workflow_root": str(ROOT), "scope_manifest": None, "checks": []}))
        with self.assertRaisesRegex(ValueError, "iteration-only"):
            eff.execute_plan(path, self.root / "out", "missing-key")
        plan = json.loads(path.read_text())
        plan["purpose"] = "iteration"
        path.write_text(json.dumps(plan))
        with patch.dict(os.environ, {"CI": "true"}), self.assertRaisesRegex(ValueError, "CI"):
            eff.execute_plan(path, self.root / "out", "missing-key")

    def test_public_shell_lifecycle_executes_before_success(self):
        binary = self.root / "bin"
        binary.mkdir()
        ps = binary / "ps"
        ps.write_text("#!/bin/sh\nprintf '123 1\\n'\n")
        ps.chmod(0o700)
        env = {**os.environ, "PATH": str(binary) + os.pathsep + os.environ["PATH"]}
        env.pop("CI", None)
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        plan = self.root / "public-plan.json"
        plan.write_text(json.dumps({"schema": 1, "purpose": "iteration", "workflow_root": str(ROOT), "scope_manifest": None,
                          "checks": [{"id": "check-required-artifacts", "category": "product", "inputs": ["AGENTS.md"], "arguments": [], "coverage": ["structure"]}]}))
        output = self.root / "public-result.json"
        command = [str(ROOT / ".systems/scripts/validate-workflow"), "--profile", "scoped", "--execution-plan", str(plan), "--evidence-output", str(output), "--receipt-key-file", str(key)]
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(output.is_file(), result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("AI_WORKFLOW_VALIDATE_COMPLETE "), 1)
        self.assertEqual(json.loads(output.read_text())["checks"][0]["execution"], "executed")

    def test_source_receipt_existing_output_rejected_before_checks(self):
        output = self.root / "existing-receipt.json"
        output.write_text("preserve existing evidence")
        result = subprocess.run([str(ROOT / ".systems/scripts/validate-workflow"),
                                 "--profile", "full", "--source-receipt", str(output),
                                 "--receipt-key-file", str(self.root / "missing-key")],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("AI_WORKFLOW_VALIDATE_START", result.stdout)
        self.assertNotIn("AI_WORKFLOW_VALIDATE_PROGRESS", result.stdout)
        self.assertEqual(output.read_text(), "preserve existing evidence")

    def test_receipt_failure_preserves_original_lifecycle_exit(self):
        source = (ROOT / ".systems/scripts/validate-workflow").read_text()
        # Execute the real EXIT trap in isolation, not a copied implementation.
        function = source.split("finish_validation() {", 1)[1].split(
            "\n}\n\nvalidation_started_at=", 1)[0]
        function = "finish_validation() {" + function + "\n}\n"
        for status, expected, result_name in [(0, 1, "fail"), (1, 1, "fail"),
                                               (124, 124, "timeout"), (130, 130, "interrupted"),
                                               (143, 143, "interrupted")]:
            with self.subTest(status=status):
                start = self.root / "source-start.json"
                start.write_text("synthetic start")
                script = "\n".join([
                    "set -euo pipefail", "scope_plan=; timing_output=; timing_initialized=0",
                    "source_start=\"$1\"; source_receipt=unused; receipt_key_file=unused; executed_checks=",
                    "validation_started=1; completion_emitted=0; profile=full",
                    "validation_started_at=$SECONDS; current_stage=synthetic; current_check=synthetic",
                    "python3() { return 1; }", function, "trap finish_validation EXIT",
                    "exit \"$2\"",
                ])
                run = subprocess.run(["bash", "-c", script, "synthetic", str(start), str(status)],
                                     cwd=ROOT, text=True, capture_output=True)
                self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
                self.assertEqual(run.stdout.count("AI_WORKFLOW_VALIDATE_COMPLETE "), 1)
                self.assertIn("result=" + result_name, run.stdout)
                self.assertIn("exit_code=" + str(expected), run.stdout)

    def test_timing_overlap_estimates_and_unknown(self):
        def interval(start, end, measurement="observed"):
            return {"phase": "review", "start": start, "end": end, "measurement": measurement,
                    "reason": "initial review", "input_fingerprint": "a" * 64}
        record = {"schema": 1, "clock": "monotonic", "intervals": [interval(1, 4), interval(2, 6), interval(7, 9), interval(0, 100, "estimate")],
                  "unknown": ["owner-waiting"]}
        result = eff.process_timing(record)
        self.assertEqual(result["observed_union_seconds"], 7)
        self.assertIn("owner-waiting", result["unmeasured_phases"])
        self.assertIn("implementation", result["unmeasured_phases"])
        for invalid in (float("nan"), True, -1):
            record["intervals"][0]["start"] = invalid
            with self.assertRaises(ValueError):
                eff.process_timing(record)

    def test_bounded_defect_strict_eligibility(self):
        record = {"risk": "medium", "scope": "one reversible fix", "dod": ["consumer output"],
                  "consumers": ["parser", "renderer"], "reversible": True, "approval": "owner scope",
                  "regressions": ["failure path"], "semantic_review": "current", "impacts": [], "capture": "useful lesson"}
        self.assertTrue(eff.bounded_defect(record)["eligible"])
        for field, value in (("risk", "high"), ("impacts", ["production"]), ("impacts", ["unknown"]),
                             ("dod", []), ("dod", True), ("approval", ""), ("regressions", [])):
            candidate = {**record, field: value}
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                eff.bounded_defect(candidate)

    def test_refresh_changed_authority_blocks_and_compaction_requires_full(self):
        (self.root / "AGENTS.md").write_text("source authority")
        (self.root / "status.md").write_text("accepted scope")
        snapshot = {"schema": 1, "scope": "approved", "stage": "quality", "approval_reference": "owner",
                    "repository": eff.digest(str(self.root)), "baseline": "a" * 40,
                    "contracts": {"AGENTS.md": eff.file_hash(self.root / "AGENTS.md")},
                    "authority_inputs": {"status.md": eff.file_hash(self.root / "status.md")}}
        with patch.object(eff.subprocess, "check_output", return_value="a" * 40):
            value = eff.refresh(snapshot, self.root, "approved", "compaction")
        self.assertEqual(value["required_refresh"], "full")
        self.assertEqual(value["status"], "verification-complete")
        self.assertFalse(value["permission_granted"])
        (self.root / "status.md").write_text("changed scope")
        with patch.object(eff.subprocess, "check_output", return_value="a" * 40):
            self.assertEqual(eff.refresh(snapshot, self.root, "approved", "resume")["status"], "blocked")
        with patch.object(eff.subprocess, "check_output", return_value="b" * 40), self.assertRaisesRegex(ValueError, "HEAD conflict"):
            eff.refresh(snapshot, self.root, "approved", "resume")
        with self.assertRaisesRegex(ValueError, "conflict"):
            eff.refresh(snapshot, self.root, "different-scope", "resume")

    def test_preflight_missing_process_metadata_fails_early(self):
        with patch.object(eff, "environment_identity", return_value="env"), patch.object(eff.subprocess, "run") as run:
            run.return_value.returncode = 1
            with self.assertRaisesRegex(ValueError, "process metadata"):
                eff.preflight(ROOT)

    def test_producer_roundtrip_all_artifact_kinds(self):
        for kind in ("architecture-qa", "plan-qa", "packaging-qa", "spec-qa", "final-check"):
            with self.subTest(kind=kind):
                record = supplied_review(kind)
                output, body = producer.render(record, ROOT, self.workspace, "synthetic")
                producer.publish(output, body)
                result = qa.assess(output, ROOT, self.workspace, "synthetic", require_pass=True)
                self.assertEqual(result["artifact_kind"], kind)
                self.assertTrue(result["current_gate_eligible"])
                if kind == "final-check":
                    self.assertIn("awaiting-owner-final-yes", body)

    def test_producer_missing_review_refuses_publication(self):
        record = supplied_review()
        del record["sections"]["Findings"]
        with self.assertRaises(qa.InvalidAssessment):
            producer.render(record, ROOT, self.workspace, "synthetic")
        self.assertEqual(list((self.project / "quality").iterdir()), [])

    def test_iteration_inventory_and_source_drift(self):
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        plan = {"schema": 1, "purpose": "iteration", "workflow_root": str(ROOT), "scope_manifest": None,
                "checks": [{"id": "check-required-artifacts", "category": "product", "inputs": ["AGENTS.md"],
                            "arguments": [], "coverage": ["structure"]}]}
        path = self.root / "plan.json"
        path.write_text(json.dumps(plan))
        original = eff.execute_bound
        def synthetic(argv, binding, previous, key, **options):
            return original([sys.executable, "-c", "pass"], binding, previous, key, **options)
        with patch.object(eff, "preflight"), patch.object(eff, "environment_identity", return_value="env"), \
                patch.object(eff, "source_identity", return_value="source"), patch.object(eff, "execute_bound", side_effect=synthetic):
            first, second = self.root / "first.json", self.root / "second.json"
            self.assertEqual(eff.execute_plan(path, first, key), 0)
            self.assertEqual(eff.execute_plan(path, second, key, first), 0)
            value = json.loads(second.read_text())
            self.assertEqual(value["checks"][0]["execution"], "reused")
            self.assertFalse(value["final_evidence_eligible"])
            with patch.object(eff, "source_identity", side_effect=["new-source", "changed-again"]):
                self.assertEqual(eff.execute_plan(path, self.root / "drift.json", key, first), 1)

    def test_full_source_receipt_success_and_stale_rejection(self):
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        start, final = self.root / "start.json", self.root / "full.json"
        checks = list(eff.read_json(eff.HERE / "validation-checks.json")["checks"])
        with patch.object(eff, "preflight"), patch.object(eff, "source_identity", return_value="source"), \
                patch.object(eff, "environment_identity", return_value="env"):
            eff.source_run_start(start, key)
            eff.source_run_finish(start, final, key, 0, checks)
            self.assertEqual(eff.verify_source(final, key)["state"], "completed")
            with patch.object(eff, "environment_identity", return_value="different"):
                with self.assertRaisesRegex(ValueError, "stale"):
                    eff.verify_source(final, key)

    def test_artifact_runtime_inventory_includes_history_registry(self):
        registry = self.project / "quality-assessments.json"
        registry.write_text('{"schema":1,"assessments":[]}')
        before = eff.digest(eff.scope.inventory_runtime(self.workspace, ["projects/synthetic"]))
        registry.write_text('{"schema":1,"assessments":[{}]}')
        after = eff.digest(eff.scope.inventory_runtime(self.workspace, ["projects/synthetic"]))
        self.assertNotEqual(before, after)

    def test_implementation_producer_uses_complete_consumer_schema(self):
        record = supplied_review()
        record["kind"] = "implementation-quality"
        sections = record["sections"]
        sections.pop("Artifact QA Completeness Gate")
        sections["Definition Of Done Validation"] = "| DoD Item | Result | Evidence |\n| --- | --- | --- |\n| Synthetic invariant | PASS | supplied test |"
        fields = {"Result": "PASS", "Owner instruction reviewed": "yes", "Accepted plan reviewed": "yes", "Accepted spec reviewed": "yes", "Scope/out-of-scope reviewed": "yes", "Acceptance criteria reviewed": "yes", "Compliance status": "aligned", "Wrong problem solved": "no", "Owner instruction mismatch": "no", "Accepted plan mismatch": "no", "Accepted spec mismatch": "no", "Acceptance criteria gap": "no", "Scope creep": "no", "Underbuild": "no", "Overbuild": "no", "Evidence": "supplied synthetic review"}
        sections["Intent / Plan / Spec Compliance"] = "\n".join("- " + k + ": " + v for k, v in fields.items())
        sections["Review Completeness Gate"] += "\n- Cross-contract consistency: aligned\n- Risk/work mode compatibility: aligned\n- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes\n- Negative-space / adversarial review: completed\n- Automated evidence role: supporting-only\n- Instruction refresh: performed-targeted\n- Instruction baseline: current\n- Producers/consumers reviewed: synthetic producer and consumer\n- Evidence: supplied boundary tests"
        sections["Adaptive Data / Integration Verification Matrix"] = "- Applicability: not-applicable\n- Not-applicable reason: isolated artifact producer, no real integration"
        gate_fields = ("Intent / Plan / Spec Compliance PASS", "Review Completeness Gate PASS", "Cross-contract consistency aligned", "Risk/work mode compatibility aligned", "Negative-space / adversarial review complete or not applicable", "Automated evidence treated as supporting-only", "Post-fix full re-review complete or not required", "Instruction baseline current", "Closure freshness current", "Policy-boundary adversarial matrix complete or not applicable", "Producer-consumer field audit complete or not applicable", "Required-field mapping complete or not applicable", "100% DoD satisfied", "No known bug in scope", "No regression in changed/direct paths", "Edge cases covered or explicitly rejected", "Explicit evidence attached")
        sections["Quality Gate"] = "\n".join("- " + k + ": yes" for k in gate_fields) + "\n- Quality result: PASS\n- Required next phase: phase-6-distillation"
        output, body = producer.render(record, ROOT, self.workspace, "synthetic")
        producer.publish(output, body)
        self.assertEqual(qa.assess(output, ROOT, self.workspace, "synthetic", require_pass=True)["verdict"], "PASS")

    def test_producer_rejects_injected_heading_and_fake_owner(self):
        record = supplied_review()
        record["sections"]["Evidence"] = "### Findings\n- Blockers: none"
        with self.assertRaisesRegex(ValueError, "injected"):
            producer.render(record, ROOT, self.workspace, "synthetic")
        record = supplied_review("final-check")
        for decision in ("approved", "`approved`", "final-owner-yes", "missing"):
            record["sections"]["Owner Approval"] = "- Owner decision: " + decision
            with self.assertRaisesRegex(ValueError, "explicit owner"):
                producer.render(record, ROOT, self.workspace, "synthetic")

    def test_historical_integrity_without_live_input_and_no_progression(self):
        output, body = producer.render(supplied_review(), ROOT, self.workspace, "synthetic")
        producer.publish(output, body)
        decision = self.project / "decisions/history.md"
        decision.write_text("- History decision: approved\n- Approved report: quality/" + output.name + "\n- Approved state: historical\n- Source: synthetic owner-approved preservation")
        registry = {"schema": 1, "assessments": [{"path": "quality/" + output.name, "sha256": eff.file_hash(output),
                     "state": "historical", "assessed_head": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
                     "decision": "decisions/history.md", "decision_sha256": eff.file_hash(decision)}]}
        (self.project / "quality-assessments.json").write_text(json.dumps(registry))
        (self.project / "context.md").unlink()
        result = qa.assess(output, ROOT, self.workspace, "synthetic", history_integrity=True)
        self.assertFalse(result["current_gate_eligible"])
        with self.assertRaisesRegex(qa.InvalidAssessment, "cannot supply current PASS"):
            qa.assess(output, ROOT, self.workspace, "synthetic", require_pass=True)
        with self.assertRaisesRegex(qa.InvalidAssessment, "cannot supply current PASS"):
            qa.assess(output, ROOT, self.workspace, "synthetic", require_pass=True, history_integrity=True)
        output.write_text(body + "\nchanged")
        with self.assertRaisesRegex(qa.InvalidAssessment, "integrity mismatch"):
            qa.assess(output, ROOT, self.workspace, "synthetic", history_integrity=True)

    def test_separate_owner_approval_needs_real_matching_decision(self):
        output, body = producer.render(supplied_review("final-check"), ROOT, self.workspace, "synthetic")
        producer.publish(output, body)
        approval = self.project / "decisions/owner.md"
        approval.write_text("- Owner decision: final-owner-yes\n- Approved scope: wrong-project\n- Source: synthetic owner message")
        record = {"schema": 1, "kind": "owner-approval", "approval_reference": "decisions/owner.md",
                  "final_check": "quality/phase-8-final-check.md"}
        with self.assertRaises(qa.InvalidAssessment):
            producer.render(record, ROOT, self.workspace, "synthetic")
        approval.write_text("- Owner decision: final-owner-yes\n- Approved scope: synthetic\n- Source: synthetic owner message")
        target, document = producer.render(record, ROOT, self.workspace, "synthetic")
        producer.publish(target, document)
        self.assertEqual(qa.owner_approval(target, ROOT, self.workspace, "synthetic")["scope"], "synthetic")

    def register_history(self, report):
        relative = report.relative_to(self.project).as_posix()
        decision = self.project / "decisions/history.md"
        decision.write_text("- History decision: approved\n- Approved report: " + relative +
                            "\n- Approved state: historical\n- Source: synthetic preservation")
        metadata, _ = qa.read_current(report.read_text().splitlines())
        registry = {"schema": 1, "assessments": [{"path": relative, "sha256": eff.file_hash(report),
                    "state": "historical", "assessed_head": metadata["Assessed source HEAD"],
                    "decision": "decisions/history.md", "decision_sha256": eff.file_hash(decision)}]}
        (self.project / "quality-assessments.json").write_text(json.dumps(registry))

    def approval_for(self, final):
        decision = self.project / "decisions/owner.md"
        decision.write_text("- Owner decision: final-owner-yes\n- Approved scope: synthetic\n- Source: synthetic test owner")
        report = self.project / "quality/phase-8-final-owner-approval.md"
        report.write_text("- Owner approval contract: owner-approval-v1\n- Scope: synthetic\n"
                          "- Owner decision: final-owner-yes\n- Approval reference: decisions/owner.md\n"
                          "- Approval SHA-256: " + eff.file_hash(decision) +
                          "\n- Final check: " + final.relative_to(self.project).as_posix() +
                          "\n- Final check SHA-256: " + eff.file_hash(final) + "\n")
        return report

    def test_nested_history_preserves_bytes_and_rejects_current_acceptance(self):
        output, body = producer.render(supplied_review(), ROOT, self.workspace, "synthetic")
        nested = output.parent / "cr-001" / output.name
        nested.parent.mkdir()
        nested.write_text(body)
        self.register_history(nested)
        (self.project / "context.md").unlink()
        result = qa.assess(nested, ROOT, self.workspace, "synthetic", history_integrity=True)
        self.assertEqual(result["lifecycle"], "historical")
        self.assertFalse(result["current_gate_eligible"])
        self.assertEqual(nested.read_text(), body)
        with self.assertRaisesRegex(qa.InvalidAssessment, "cannot supply current PASS"):
            qa.assess(nested, ROOT, self.workspace, "synthetic", require_pass=True)
        registry_path = self.project / "quality-assessments.json"
        registry = json.loads(registry_path.read_text())
        foreign = self.project / "context-report.md"
        foreign.write_text(body)
        registry["assessments"][0]["path"] = "context-report.md"
        registry_path.write_text(json.dumps(registry))
        with self.assertRaisesRegex(qa.InvalidAssessment, "owning quality root"):
            qa.history_entry(foreign, self.project)

    def test_historical_owner_approval_is_provenance_only_and_tamper_checked(self):
        output, body = producer.render(supplied_review("final-check"), ROOT, self.workspace, "synthetic")
        nested = output.parent / "cr-001" / output.name
        nested.parent.mkdir()
        nested.write_text(body)
        approval = self.approval_for(nested)
        self.register_history(nested)
        (self.project / "context.md").unlink()
        result = qa.owner_approval(approval, ROOT, self.workspace, "synthetic", history_integrity=True)
        self.assertEqual(result["lifecycle"], "historical")
        self.assertFalse(result["current_gate_eligible"])
        with self.assertRaisesRegex(qa.InvalidAssessment, "cannot supply current PASS"):
            qa.owner_approval(approval, ROOT, self.workspace, "synthetic")
        command = [sys.executable, str(ROOT / ".systems/scripts/lib/qa-evidence.py"), str(approval),
                   "--workflow-root", str(ROOT), "--workspace-root", str(self.workspace),
                   "--project", "synthetic", "--owner-approval", "--history-integrity", "--require-pass"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot supply current PASS", result.stderr)
        nested.write_text(body + "\nchanged")
        with self.assertRaisesRegex(qa.InvalidAssessment, "final check integrity mismatch"):
            qa.owner_approval(approval, ROOT, self.workspace, "synthetic", history_integrity=True)

    def test_current_owner_approval_verifies_real_approved_target_inputs(self):
        import re
        output, body = producer.render(supplied_review("final-check"), ROOT, self.workspace, "synthetic")
        target = self.root / "target"
        target.mkdir()
        source = target / "target.md"
        source.write_bytes((self.project / "context.md").read_bytes())
        body = body.replace("| owning-project-evidence | context.md |", "| approved-target-source | target.md |")
        digest = hashlib.sha256(("approved-target-source:target.md=" + eff.file_hash(source) + "\n").encode()).hexdigest()
        body = re.sub(r"(?m)^- Assessed worktree digest: .+$", "- Assessed worktree digest: " + digest, body)
        producer.publish(output, body)
        approval = self.approval_for(output)
        result = qa.owner_approval(approval, ROOT, self.workspace, "synthetic", target_root=target)
        self.assertTrue(result["current_gate_eligible"])
        source.write_text("changed target")
        with self.assertRaisesRegex(qa.InvalidAssessment, "stale or mismatched"):
            qa.owner_approval(approval, ROOT, self.workspace, "synthetic", target_root=target)

    def test_source_receipt_requires_all_checks_and_same_environment(self):
        key = self.root / "key"
        key.write_bytes(self.key)
        key.chmod(0o600)
        checks = list(eff.read_json(ROOT / ".systems/scripts/lib/validation-checks.json")["checks"])
        record = {"schema": 1, "run_id": "full-source", "purpose": "full-source-verification",
                  "source": "source", "environment": "env", "root": eff.digest(str(ROOT)), "state": "completed",
                  "exit_code": 0, "checks": checks}
        record["authentication"] = eff.sign(record, self.key)
        path = self.root / "full.json"
        path.write_text(json.dumps(record))
        with patch.object(eff, "source_identity", return_value="source"), patch.object(eff, "environment_identity", return_value="env"):
            self.assertEqual(eff.verify_source(path, key)["run_id"], "full-source")
            record["checks"].remove("check-validator-smoke-tests")
            record["authentication"] = eff.sign(record, self.key)
            path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "incomplete"):
                eff.verify_source(path, key)

    def test_capabilities_exact_boolean_inventory(self):
        value = eff.read_json(ROOT / ".systems/ai/capabilities/execution-efficiency-v1.json")
        self.assertEqual(value["contract"], 1)
        self.assertEqual(set(value["capabilities"]), set(eff.CAPABILITIES))
        self.assertTrue(all(type(v) is bool for v in value["capabilities"].values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
