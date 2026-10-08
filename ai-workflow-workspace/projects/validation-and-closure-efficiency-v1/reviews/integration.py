#!/usr/bin/env python3
"""Exercise the public iteration interface on the approved upstream source."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[4]
with tempfile.TemporaryDirectory(prefix="eff-integration-") as raw:
    tmp = Path(raw)
    key = tmp / "explicit-test-key"
    key.write_bytes(os.urandom(32))
    key.chmod(0o600)
    plan = tmp / "plan.json"
    plan.write_text(json.dumps({"schema": 1, "purpose": "iteration", "workflow_root": str(ROOT),
                               "scope_manifest": None, "checks": [{"id": "check-required-artifacts",
                               "category": "product", "inputs": ["AGENTS.md"], "arguments": [],
                               "coverage": ["structure"]}]}))
    results = []
    previous = None
    for stage in ("fresh", "reused"):
        output = tmp / (stage + ".json")
        argv = [str(ROOT / ".systems/scripts/validate-workflow"), "--profile", "scoped",
                "--execution-plan", str(plan), "--evidence-output", str(output),
                "--receipt-key-file", str(key), "--explain"]
        if previous:
            argv += ["--reuse-record", str(previous)]
        start = time.monotonic()
        run = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
        print(run.stdout + run.stderr, flush=True)
        assert run.returncode == 0, run.stdout + run.stderr
        assert run.stdout.count("AI_WORKFLOW_VALIDATE_COMPLETE ") == 1
        value = json.loads(output.read_text())
        assert value["checks"][0]["execution"] == ("executed" if stage == "fresh" else "reused")
        assert value["final_evidence_eligible"] is False
        results.append({"stage": stage, "duration_seconds": time.monotonic()-start,
                        "execution": value["checks"][0]["execution"], "completion_markers": 1})
        previous = output
    tampered = json.loads(previous.read_text())
    tampered["source"] = "forged"
    previous.write_text(json.dumps(tampered))
    invalid_command = argv[:-2] + ["--reuse-record", str(previous)]
    invalid_command[invalid_command.index("--evidence-output") + 1] = str(tmp / "tampered.json")
    run = subprocess.run(invalid_command, cwd=ROOT,
                         text=True, capture_output=True)
    assert run.returncode == 1, run.stdout + run.stderr
    assert "authentication mismatch" in run.stderr
    assert run.stdout.count("AI_WORKFLOW_VALIDATE_COMPLETE ") == 1
    report = {"schema": 1, "scope": "public iteration interface", "results": results,
              "tampered_receipt_rejected": True, "semantic_quality_replaced": False}
    destination = Path(__file__).with_name("integration-result.json")
    with destination.open("x") as out:
        json.dump(report, out, indent=2)
    print(json.dumps(report))
