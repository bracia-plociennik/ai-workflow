#!/usr/bin/env python3
"""Run the frozen routine skill-discovery near-miss in a synthetic fixture."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


FIXTURE = Path("/private/tmp/ai-workflow-skill-002-residual-001-candidate")
OUTPUT_ROOT = Path(__file__).resolve().parent / "runs" / "routine-discovery-near-miss"
PROMPT = (
    "Synthetic read-only AI Workflow evaluation. Use only the isolated fixture as source. "
    "Do not inspect the live repository, parent directories, clients, external services or user files. "
    "Do not write anything. Follow the fixture's AGENTS.md and cite actual tool-open evidence when possible.\n\n"
    "Review `src/skill_creator_status.py` for compliance with the arithmetic-mean contract "
    "`[1, 2] -> '1.5'` and empty input -> `'empty'`. First check whether any available "
    "AI Workflow skill should support this task. Read-only; report findings and which skill you "
    "selected, if any. Do not edit files."
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", default="001")
    args = parser.parse_args()
    if not args.repeat.isdigit() or len(args.repeat) != 3:
        parser.error("--repeat must be a three-digit run number")

    output = OUTPUT_ROOT / args.repeat
    output.mkdir(parents=True, exist_ok=False)
    source = FIXTURE / "src/skill_creator_status.py"
    skill = FIXTURE / ".systems/ai/skills/skill-creator/SKILL.md"
    before = {"source": digest(source), "skill": digest(skill), "agents": digest(FIXTURE / "AGENTS.md")}
    command = [
        "codex", "exec", "--ephemeral", "--ignore-user-config", "--json",
        "--skip-git-repo-check", "-m", "gpt-6-sol", "-c", 'model_reasoning_effort="high"',
        "-c", 'approval_policy="never"', "-c", "sandbox_workspace_write.network_access=false",
        "-s", "read-only", "-C", str(FIXTURE), "-o", str(output / "last-message.txt"), PROMPT,
    ]
    started = time.monotonic()
    with (output / "trace.jsonl").open("w") as trace, (output / "stderr.txt").open("w") as stderr:
        process = subprocess.Popen(command, stdout=trace, stderr=stderr, start_new_session=True)
        try:
            code = process.wait(timeout=420)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
    after = {"source": digest(source), "skill": digest(skill), "agents": digest(FIXTURE / "AGENTS.md")}
    result = {
        "case": "routine-discovery-near-miss", "repeat": args.repeat,
        "model": "gpt-6-sol", "reasoning_effort": "high", "sandbox": "read-only",
        "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
        "fixture_before": before, "fixture_after": after, "fixture_unchanged": before == after,
        "exit_code": code, "duration_seconds": round(time.monotonic() - started, 2),
    }
    (output / "metadata.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
