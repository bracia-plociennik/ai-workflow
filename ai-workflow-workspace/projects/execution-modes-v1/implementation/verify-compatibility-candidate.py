"""Offline candidate installation with frozen counterpart code, never its installed profile."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FROZEN = HERE / "frozen-counterpart"
sys.path.insert(0, str(FROZEN / ".systems/scripts"))
import execution_modes as counterpart

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL, text=True).strip()

def main():
    code = sorted((FROZEN / ".systems/scripts").glob("*.py"))
    code += [FROZEN / ".systems/scripts/project-orchestration-preflight",
             FROZEN / ".systems/scripts/tests/verify_execution_modes_counterpart.py"]
    before = {str(path.relative_to(FROZEN)): digest(path) for path in code}
    candidate_inputs = {name: digest(ROOT / name) for name in sorted(counterpart.WORKFLOW_SOURCES)}
    with tempfile.TemporaryDirectory(prefix="workflow-execution-compat-") as directory:
        candidate = Path(directory)
        for name in sorted(counterpart.WORKFLOW_SOURCES):
            target = candidate / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
            target.chmod((ROOT / name).stat().st_mode & 0o777)
        (candidate / "AGENTS.md").write_text("# Isolated synthetic Workflow candidate\n")
        subprocess.run(["git", "init", str(candidate)], capture_output=True, check=True)
        git(candidate, "add", ".")
        git(candidate, "-c", "user.name=Synthetic Test", "-c", "user.email=test@example.invalid", "commit", "-m", "synthetic candidate")
        profile = dict(contract=1, tested_commit=git(candidate, "rev-parse", "HEAD"),
            mode_mapping={"auto": "auto", "human": "human-coop"},
            delivery_mapping={"auto-unconstrained": "auto-unbounded"},
            inspector=".systems/scripts/lib/execution-modes.py",
            sources={name: dict(sha256=digest(candidate / name),
                mode="100755" if (candidate / name).stat().st_mode & 0o111 else "100644")
                for name in sorted(counterpart.WORKFLOW_SOURCES)})
        # Generated profile is an explicit candidate fixture, not counterpart product input.
        profile_path = FROZEN / ".systems/ai/capabilities/workflow-execution-modes-v1.json"
        profile_path.write_text(json.dumps(profile, indent=2) + "\n")
        result = subprocess.run([sys.executable, "-B", str(FROZEN / ".systems/scripts/tests/verify_execution_modes_counterpart.py"),
            "--workflow-root", str(candidate)], capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise ValueError(result.stdout + result.stderr)
        output = json.loads(result.stdout)
        state = json.loads((candidate / ".systems/ai/templates/autopilot/execution-readiness.template.json").read_text())
        state["recovery"]["attempts"] = [dict(attempt_id="A-" + str(n), unit_id="UNIT-001",
            cause_id="C-1", progress_evidence=None) for n in (1, 2, 3)]
        state["recovery"]["retry_counts"]["total"] = 3
        path = candidate / "state.json"
        path.write_text(json.dumps(state))
        stalled = counterpart.inspect_workflow_state(candidate, path)["workflow_readiness"]
        assert stalled["ready_units"] == [] and stalled["result"] == "blocked"
        second = copy.deepcopy(state["units"][0])
        second.update(id="UNIT-002", resources=["files/independent"])
        state["units"].append(second)
        path.write_text(json.dumps(state))
        independent = counterpart.inspect_workflow_state(candidate, path)["workflow_readiness"]
        assert independent["ready_units"] == ["UNIT-002"]
        state["recovery"]["attempts"].append(dict(attempt_id="A-4", unit_id="UNIT-001", cause_id="C-1", progress_evidence="a" * 64))
        state["recovery"]["retry_counts"]["total"] = 4
        path.write_text(json.dumps(state))
        assert set(counterpart.inspect_workflow_state(candidate, path)["workflow_readiness"]["ready_units"]) == {"UNIT-001", "UNIT-002"}
        state["recovery"]["retry_counts"]["units"]["UNIT-001"]["quality"] = 2
        path.write_text(json.dumps(state))
        assert counterpart.inspect_workflow_state(candidate, path)["workflow_readiness"]["ready_units"] == ["UNIT-002"]
        source = candidate / ".systems/ai/core/execution-modes.md"
        source.write_text(source.read_text() + "\nSynthetic uncommitted tamper.\n")
        assert counterpart.workflow_support(candidate)["status"] == "invalid"
        output["additional_scenarios"] = ["three-stalled-blocked", "independent-continuation",
            "new-progress-reset", "stricter-quality-budget", "uncommitted-source-rejected"]
        output["frozen_counterpart_sources"] = before
        output["candidate_sources"] = candidate_inputs
        output["fixture_role"] = "isolated profile of synthetic committed candidate; not installed interoperability"
    if before != {str(path.relative_to(FROZEN)): digest(path) for path in code}:
        raise ValueError("frozen counterpart drift")
    if candidate_inputs != {name: digest(ROOT / name) for name in candidate_inputs}:
        raise ValueError("candidate source drift")
    for name, checksum in before.items():
        actual = Path("/private/tmp/ai-system-execution-modes-v1") / name
        if digest(actual) != checksum:
            raise ValueError("actual counterpart source drift; refresh and rerun")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
