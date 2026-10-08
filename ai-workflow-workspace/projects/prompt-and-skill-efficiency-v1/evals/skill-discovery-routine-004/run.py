#!/usr/bin/env python3
"""Run one read-only routine skill-discovery case against a synthetic fixture."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


FIXTURE = Path("/private/tmp/ai-workflow-skill-discovery-20260928")
OUTPUT_ROOT = Path(__file__).resolve().parent / "runs"
PREFIX = (
    "Synthetic read-only AI Workflow evaluation. Use only the isolated fixture as source. "
    "Do not inspect the live repository, parent directories, clients, external services or user files. "
    "Do not write anything. Follow the fixture's AGENTS.md. Report the skill selected, if any, "
    "and distinguish actual source opens from inference.\n\n"
)
CASES = {
    "generic-review": (
        "Review `src/report.py` against the contract average([1, 2]) == '1.5' and "
        "average([]) == 'empty'. First discover whether any available AI Workflow skill "
        "supports this product-code review. Identify findings; do not edit files."
    ),
    "name-collision-review": (
        "Review `src/skill_creator_status.py` against the contract "
        "report_status([1, 2]) == '1.5' and report_status([]) == 'empty'. "
        "First discover whether any available AI Workflow skill supports this product-code review. "
        "The filename is product terminology, not a request to work on AI Workflow skills. "
        "Identify findings; do not edit files."
    ),
    "catalog-only": (
        "For a future review of `src/report.py`, which available AI Workflow skill, if any, "
        "would be relevant? Do not review the code yet. Report your selection and why."
    ),
    "direct-skill-review": (
        "Review the active AI Workflow `skill-creator` skill's trigger and resource routing. "
        "Inspect its `SKILL.md` and relevant referenced resources, identify actionable findings "
        "or state that none were found. Do not edit files."
    ),
}


def fixture_digest(fixture):
    entries = []
    for path in sorted(fixture.rglob("*")):
        if path.is_file():
            entries.append((str(path.relative_to(fixture)), hashlib.sha256(path.read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=CASES)
    parser.add_argument("--repeat", default="001")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    args = parser.parse_args()
    if not args.repeat.isdigit() or len(args.repeat) != 3:
        parser.error("--repeat must be a three-digit run number")
    if not args.fixture.is_dir():
        parser.error(f"missing frozen fixture: {args.fixture}")

    output = args.output_root / args.case / args.repeat
    output.mkdir(parents=True, exist_ok=False)
    prompt = PREFIX + CASES[args.case]
    before = fixture_digest(args.fixture)
    command = [
        "codex", "exec", "--ephemeral", "--ignore-user-config", "--json",
        "--skip-git-repo-check", "-m", "gpt-6-sol",
        "-c", 'model_reasoning_effort="high"', "-c", 'approval_policy="never"',
        "-c", "sandbox_workspace_write.network_access=false", "-s", "read-only",
        "-C", str(args.fixture), "-o", str(output / "last-message.txt"), prompt,
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
    after = fixture_digest(args.fixture)
    result = {
        "case": args.case,
        "repeat": args.repeat,
        "model": "gpt-6-sol",
        "reasoning_effort": "high",
        "sandbox": "read-only",
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "fixture_before": before,
        "fixture_after": after,
        "fixture_unchanged": before == after,
        "exit_code": code,
        "duration_seconds": round(time.monotonic() - started, 2),
    }
    (output / "metadata.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
