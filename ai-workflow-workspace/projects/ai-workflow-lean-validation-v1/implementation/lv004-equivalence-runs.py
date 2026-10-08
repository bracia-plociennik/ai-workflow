"""Run frozen reference and independent candidate without promoting source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--reference", type=Path, required=True)
args = parser.parse_args()
candidate = args.candidate.resolve()
manifest = json.loads((candidate / ".systems/scripts/smoke/manifest.json").read_text())
args.evidence.mkdir(exist_ok=True)
runner = candidate / ".systems/scripts/check-validator-smoke-tests"
runs = []
cases = [("reference-all", ["bash", str(args.reference.resolve()), "--group", "all"]),
         ("candidate-all", [str(runner), "--group", "all"])]
cases += [("reverse-" + group, [str(runner), "--group", group])
          for group in reversed(manifest["groups"])]
for name, command in cases:
    log = args.evidence / (name + ".log")
    diagnostics = args.evidence / (name + ".diagnostics.tsv")
    timing = args.evidence / (name + ".timing.tsv")
    if any(path.exists() for path in (log, diagnostics, timing)):
        raise SystemExit("Do not overwrite execution evidence: " + name)
    temporary = tempfile.TemporaryDirectory(prefix="lv004-timing-")
    runtime_timing = Path(temporary.name) / "timing.tsv"
    env = os.environ.copy()
    env.update(AI_WORKFLOW_SMOKE_DIAGNOSTICS_OUTPUT=str(diagnostics.resolve()),
               AI_WORKFLOW_TIMING_OUTPUT=str(runtime_timing.resolve()),
               AI_WORKFLOW_TIMING_RUN_ID="lv004-equivalence-" + name)
    start = time.monotonic()
    with log.open("w") as output:
        process = subprocess.run(command + ["--progress", "summary"], cwd=candidate, env=env,
                                 stdout=output, stderr=subprocess.STDOUT)
    text = log.read_text()
    if runtime_timing.exists():
        shutil.copy2(runtime_timing, timing)
    temporary.cleanup()
    ids = re.findall(r"^AI_WORKFLOW_SMOKE_PROGRESS test=(\S+) status=started$", text, re.M)
    expected = (manifest["reference_test_ids"] if name == "reference-all" else
                list(manifest["test_groups"]) if name == "candidate-all" else
                [i for i, group in manifest["test_groups"].items() if group == name.removeprefix("reverse-")])
    assert process.returncode == 0, (name, process.returncode, text[-2000:])
    assert len(ids) == len(set(ids)) and set(ids) == set(expected), (name, "coverage differs")
    completions = re.findall(r"^AI_WORKFLOW_SMOKE_COMPLETE .*", text, re.M)
    assert len(completions) == 1 and "result=pass" in completions[0], completions
    rows = timing.read_text().splitlines()
    wall_rows = [line for line in rows[1:] if line.split("\t")[0] == "smoke-suite-wall"]
    assert len(wall_rows) == 1, (name, "multiple/missing timing parents")
    runs.append({"name": name, "exit_code": process.returncode, "duration_seconds": time.monotonic()-start,
                 "ids": ids, "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                 "diagnostics_sha256": hashlib.sha256(diagnostics.read_bytes()).hexdigest(),
                 "one_public_completion": True, "one_smoke_timing_wall": True})
    (args.evidence / "execution-results.json").write_text(json.dumps({"runs": runs}, indent=2) + "\n")
    print(json.dumps({"run": name, "result": "pass", "ids": len(ids), "seconds": round(runs[-1]["duration_seconds"])}), flush=True)

# Negative diagnostics are compared by ID; host-specific disposable paths are
# normalized only for comparison, never by changing raw logs or test outcomes.
def diagnostics(name):
    rows = {}
    for line in (args.evidence / (name + ".diagnostics.tsv")).read_text().splitlines():
        identifier, status, message = line.split("\t", 2)
        message = re.sub(r"(?:/private)?/tmp/[^\s:]+|/var/folders/[^\s:]+", "<fixture-path>", message)
        rows[identifier] = (status, message)
    return rows
old, new = diagnostics("reference-all"), diagnostics("candidate-all")
assert all(new.get(i) == value for i, value in old.items()), "typed reference diagnostics differ"
(args.evidence / "equivalence-results.json").write_text(json.dumps({
    "result": "pass", "reference_ids": len(manifest["reference_test_ids"]),
    "supplemental_ids": len(manifest["supplemental_test_ids"]), "runs": runs,
    "negative_diagnostics_compared": len(old), "order": "reference, all, reversed standalone groups",
    "limits": "Frozen region/assertion audits and protected mutation/failure-path evidence are separately required; no performance claim."}, indent=2) + "\n")
