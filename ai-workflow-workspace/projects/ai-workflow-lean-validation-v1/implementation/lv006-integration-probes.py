"""Local integration evidence; synthetic fixtures are not performance measurements."""
import collections
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
results = []
env = os.environ.copy()
env["AI_WORKFLOW_MODE"] = "official"
env["AI_WORKFLOW_WORKSPACE_HOME"] = str(root / "ai-workflow-workspace")
env.pop("AI_WORKFLOW_SKIP_SMOKE_TESTS", None)

def check(name, command, code=0, reason=None):
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
    assert result.returncode == code, (name, result.returncode, result.stdout, result.stderr)
    if reason:
        assert reason in result.stdout + result.stderr, (name, result.stdout, result.stderr)
    results.append({"id": name, "exit": result.returncode, "expected": code,
                    "diagnostic": reason or "successful supporting check"})
    return result

check("current-qa-inputs", [".systems/scripts/check-qa-evidence", "--project", project.name])
check("manifest-structural-only", [".systems/scripts/check-validator-smoke-tests", "--verify-manifest"])
manifest = json.loads((root / ".systems/scripts/smoke/manifest.json").read_text())
assert len(manifest["test_groups"]) == 694
assert len(manifest["reference_test_ids"]) == 674
assert len(manifest["supplemental_test_ids"]) == 20
assert set(manifest["reference_test_ids"] + manifest["supplemental_test_ids"]) == set(manifest["test_groups"])
baselines = [project / f"implementation/lv002-final-reviewed-{n:03d}.json" for n in (1, 2, 3)]
baseline = check("immutable-baseline-valid", [".systems/scripts/report-validation-comparison",
                "summarize", *(str(path) for path in baselines)])
assert len(json.loads(baselines[0].read_text())["tests"]) == 660
assert set(json.loads(baselines[0].read_text())["tests"]) != set(manifest["test_groups"])
for path in [".github/workflows/ai-workflow-validate.yml", ".systems/scripts/update-from-upstream"]:
    assert "validate-workflow --profile full" in (root / path).read_text()
assert 'profile="standard"' in (root / ".systems/scripts/validate-workflow").read_text()
check("bad-profile", [".systems/scripts/validate-workflow", "--profile", "partial"], 1, "Unknown validation profile")
check("bad-group", [".systems/scripts/check-validator-smoke-tests", "--group", "partial"], 2, "invalid choice")
assert "- State: deferred" in (project / "capture-state/lv-ux-005-instruction-efficiency.md").read_text()
assert "LV005" in (project / "decisions/lv-dec-010-lv005-deferral.md").read_text()

module_spec = importlib.util.spec_from_file_location("comparison", root / ".systems/scripts/report-validation-comparison")
from importlib.machinery import SourceFileLoader
module_spec = importlib.util.spec_from_loader("comparison", SourceFileLoader("comparison", str(root / ".systems/scripts/report-validation-comparison")))
comparison = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(comparison)
with tempfile.TemporaryDirectory(prefix="lv006-synthetic-") as temp:
    folder = Path(temp)
    # Build truthful synthetic metadata to exercise the real CLI reader.
    groups = []
    for label, tests in (("before", ["a", "b"]), ("after", ["a", "b", "c"])):
        paths = []
        for n in range(3):
            run_id = ("a" * 64) + f"-synthetic-{label}-{n}"
            def row(identifier, group, duration, profile, kind, parent):
                return dict(zip(comparison.timing.HEADER.strip().split("\t"),
                    [identifier, group, str(duration), "pass", profile, "2", run_id, kind, parent]))
            rows = [row("check-validator-smoke-tests", "smoke", 10, "full", "child", "validation-wall"),
                    row("validation-wall", "wall", 20, "full", "wall", "none"),
                    row("smoke-suite-wall", "smoke", 5, "smoke-all", "wall", "validation-wall")]
            rows += [row(test, "core", 1, "smoke-all", "child", "smoke-suite-wall") for test in tests]
            timing = folder / f"{label}-{n}.tsv"
            timing.write_text(comparison.timing.HEADER + "".join("\t".join(r.values()) + "\n" for r in rows))
            info = comparison.characterize(rows)
            data = dict(schema_version=2, revision="synthetic-only", source_digest="a"*64,
                        runtime="synthetic", profile="full", scope_fingerprint="same", input_fingerprint="same",
                        setup_regime="same", timing_file=timing.name,
                        timing_digest=hashlib.sha256(timing.read_bytes()).hexdigest(), **info)
            path = folder / f"{label}-{n}.json"
            path.write_text(json.dumps(data))
            paths.append(str(path))
        groups.append(paths)
    check("unequal-coverage-rejected", [".systems/scripts/report-validation-comparison", "compare",
          "--baseline", *groups[0], "--candidate", *groups[1]], 2, "inputs or coverage differ")
    policy = root / ".systems/scripts/lib/policy-boundaries.sh"
    for name, text, expected in [
        ("safe-prohibition", "must not allow bypass", 0),
        ("direct-unsafe", "may allow bypass", 1),
        ("compound-unsafe", "must not allow bypass; but may allow bypass", 1),
    ]:
        fixture = folder / "policy.md"
        fixture.write_text(text + "\n")
        check(name, ["bash", "-c", 'fail=0; source "$1"; policy_reject_unsafe_pattern "allow bypass" "unsafe policy" "$2"; exit "$fail"',
                     "probe", str(policy), str(fixture)], expected)
    check("missing-policy-source", ["bash", "-c", 'fail=0; source "$1"; policy_reject_unsafe_pattern "allow bypass" "unsafe policy" "$2"; exit "$fail"',
          "probe", str(policy), str(folder / "absent.md")], 1, "scan failed")

paths = subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines()
assert paths == [".systems/ai/core/changelog.md"], paths
assert not subprocess.check_output(["git", "ls-files", "ai-workflow-workspace"], text=True)
report = {"source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
          "source_diff": paths, "checks": results,
          "baseline_tests": 660, "current_tests": 694, "full_speed_claim": "ineligible",
          "groups": dict(collections.Counter(manifest["test_groups"].values())),
          "limits": "Synthetic reader/policy checks and structural audit; new full execution remains separate."}
(project / "implementation/lv006-integration-probes.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
