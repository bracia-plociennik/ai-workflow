#!/usr/bin/env python3
"""Run frozen synthetic SKILL-002 cases in a read-only Codex CLI sandbox."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


FIXTURE = Path("/private/tmp/ai-workflow-skill-002-residual-001-candidate")
RUNS = Path(__file__).resolve().parent / "runs"
PREFIX = (
    "Synthetic read-only AI Workflow evaluation. Use only the isolated fixture as source. "
    "Do not inspect the live repository, parent directories, clients, external services or user files. "
    "Do not write anything. Follow the fixture's AGENTS.md and cite actual tool-open evidence when possible.\n\n"
)
CASES = {
    "skill-review-direct": (
        "Read-only review of the active AI Workflow `skill-creator` skill. Inspect its trigger "
        "description and Resource Routing. Identify a concrete current false negative, false positive "
        "or missing resource route if one exists; otherwise say no demonstrated gap. Cite files actually "
        "opened. Do not edit files or run a formal phase gate."
    ),
    "skill-eval-resource": (
        "Plan, read-only, a small behavioral evaluation for the active AI Workflow `skill-creator` skill. "
        "Include should-trigger and should-not-trigger cases and the expected grading/output shape. "
        "Open only the skill resources needed for this planning task. Do not scaffold a run, write files "
        "or claim completed grading. Cite files actually opened."
    ),
    "generic-code-near-miss": (
        "Review `src/skill_creator_status.py` only as synthetic product code. The function should return "
        "the arithmetic mean as a decimal string (for example `[1, 2]` should yield `1.5`), and "
        "`empty` for an empty list. The `skill_creator` name is a product symbol, not a request to "
        "create, review, evaluate or package an AI Workflow skill. Findings first; read-only; do not "
        "edit files or claim formal PASS. Cite files actually opened."
    ),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=CASES)
    parser.add_argument("--repeat", default="001")
    args = parser.parse_args()
    if not args.repeat.isdigit() or len(args.repeat) != 3:
        parser.error("--repeat must be a three-digit run number")
    if not (FIXTURE / "AGENTS.md").is_file() or not (FIXTURE / ".systems/ai/skills/skill-creator/SKILL.md").is_file():
        parser.error("isolated fixture is incomplete")

    output = RUNS / args.case / args.repeat
    output.mkdir(parents=True, exist_ok=False)
    prompt = PREFIX + CASES[args.case]
    command = [
        "codex", "exec", "--ephemeral", "--ignore-user-config", "--json",
        "--skip-git-repo-check", "-m", "gpt-6-sol", "-c", 'model_reasoning_effort="high"',
        "-c", 'approval_policy="never"', "-c", "sandbox_workspace_write.network_access=false",
        "-s", "read-only", "-C", str(FIXTURE), "-o", str(output / "last-message.txt"), prompt,
    ]
    started = time.monotonic()
    with (output / "trace.jsonl").open("w") as trace, (output / "stderr.txt").open("w") as stderr:
        process = subprocess.Popen(command, stdout=trace, stderr=stderr, start_new_session=True)
        try:
            exit_code = process.wait(timeout=420)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            exit_code = 124

    metadata = {
        "case": args.case,
        "repeat": args.repeat,
        "fixture": str(FIXTURE),
        "model": "gpt-6-sol",
        "reasoning_effort": "high",
        "sandbox": "read-only",
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "agents_sha256": sha256(FIXTURE / "AGENTS.md"),
        "skill_sha256": sha256(FIXTURE / ".systems/ai/skills/skill-creator/SKILL.md"),
        "exit_code": exit_code,
        "duration_seconds": round(time.monotonic() - started, 2),
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
