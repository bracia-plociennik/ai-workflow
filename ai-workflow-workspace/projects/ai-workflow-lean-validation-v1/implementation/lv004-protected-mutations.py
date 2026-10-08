"""Compare actual protected-mutation rejection in frozen and partitioned runs."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--reference", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
args = parser.parse_args()
args.evidence.mkdir(exist_ok=True)
results = []
with tempfile.TemporaryDirectory(prefix="lv004-protected-mutations-") as temporary:
    for command in ("check-status-consistency", "check-validation-observability"):
        fixture = Path(temporary) / command
        shutil.copytree(args.candidate, fixture)
        (fixture / ".systems/scripts" / command).write_text("#!/usr/bin/env bash\nexit 0\n")
        outcomes = []
        for mode, runner in (("reference", args.reference.resolve()),
                             ("candidate", fixture / ".systems/scripts/check-validator-smoke-tests")):
            log = args.evidence / (command + "-" + mode + ".log")
            if log.exists():
                raise SystemExit("Do not replace failed or completed mutation evidence")
            env = os.environ.copy()
            env.pop("AI_WORKFLOW_TIMING_OUTPUT", None)
            with log.open("w") as output:
                result = subprocess.run(["bash", str(runner), "--group", "all" if mode == "reference" else "core", "--progress", "summary"],
                                        cwd=fixture, env=env, stdout=output, stderr=subprocess.STDOUT)
            text = log.read_text()
            assert result.returncode == 1, (mode, command, result.returncode, text[-2000:])
            failed = re.findall(r"Expected (?:failure|success): (\S+)", text)
            if not failed:
                failed = re.findall(r"test=(\S+) status=started", text)[-1:]
            completions = re.findall(r"^AI_WORKFLOW_SMOKE_COMPLETE .*", text, re.M)
            assert len(completions) == 1 and "result=fail" in completions[0], completions
            outcomes.append({"mode": mode, "status": result.returncode, "rejected_case": failed})
        assert outcomes[0]["rejected_case"] == outcomes[1]["rejected_case"], outcomes
        results.append({"protected_command": command, "mutation": "incorrect unconditional exit zero", "outcomes": outcomes})
        print(json.dumps(results[-1]), flush=True)
args.evidence.joinpath("results.json").write_text(json.dumps({"result": "pass", "cases": results}, indent=2) + "\n")
