#!/usr/bin/env python3
"""Reproduce stale grading reuse using a synthetic local eval plan."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPTS = Path(__file__).resolve().parents[5] / ".systems/ai/skills/skill-creator/scripts"


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, capture_output=True, text=True)


def main():
    with tempfile.TemporaryDirectory(prefix="ai-workflow-stale-grading-") as temp:
        root = Path(temp)
        plan_path = root / "evals.json"
        run_dir = root / "run"
        plan = {
            "skill_name": "synthetic-skill",
            "mode": "manual-review",
            "configurations": ["baseline"],
            "evals": [{"id": "case-1", "prompt": "original prompt", "expected_behavior": ["old expectation"]}],
        }
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        run(SCRIPTS / "run_eval.py", plan_path, "--output-dir", run_dir)
        grading_path = run_dir / "case-1/baseline/grading.json"
        grading_path.write_text(
            json.dumps({"eval_id": "case-1", "configuration": "baseline", "passed": True, "score": 1.0}),
            encoding="utf-8",
        )

        plan["evals"][0]["prompt"] = "changed prompt"
        plan["evals"][0]["expected_behavior"] = ["new expectation"]
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        run(
            SCRIPTS / "run_loop.py",
            SCRIPTS.parent,
            "--evals-json", plan_path,
            "--run-dir", run_dir,
        )

        metadata = json.loads((run_dir / "case-1/eval_metadata.json").read_text(encoding="utf-8"))
        benchmark = json.loads((run_dir / "benchmark.json").read_text(encoding="utf-8"))
        stale_reused = (
            metadata["prompt"] == "changed prompt"
            and metadata["expected_output"] == ""
            and metadata["assertions"][0]["text"] == "new expectation"
            and benchmark["runs"][0]["passed"] is True
            and benchmark["runs"][0]["source"].endswith("case-1/baseline/grading.json")
        )
        print(json.dumps({"metadata_is_new": metadata["prompt"] == "changed prompt", "old_grade_reused": stale_reused}))
        return 0 if stale_reused else 1


if __name__ == "__main__":
    raise SystemExit(main())
