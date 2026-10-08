#!/usr/bin/env python3
"""Summarize completed explicit contract reads from a controlled Codex JSONL run."""

import argparse
import json
from pathlib import Path
import re
import shlex


CORE_PATH = re.compile(r"\.systems/ai/core/[a-z0-9-]+\.md")
BRACED_CORE_PATH = re.compile(r"\.systems/ai/core/\{([a-z0-9,-]+)\}\.md")
SKILL_PATH = re.compile(r"(?:\.systems/ai/skills|ai-workflow-workspace/skills)/[^\s'\"]+/SKILL\.md")
READ_COMMANDS = {"cat", "sed", "head", "tail", "nl", "awk", "less", "rg"}
LOOP = re.compile(r"\bfor\s+(\w+)\s+in\s+([^;]+);\s*do\s+(.+?)\bdone\b", re.DOTALL)


def completed_commands(trace):
    with trace.open(encoding="utf-8") as source:
        for line in source:
            event = json.loads(line)
            item = event.get("item", {})
            if event.get("type") != "item.completed" or item.get("type") != "command_execution":
                continue
            command = item.get("command", "")
            try:
                outer = shlex.split(command)
            except ValueError:
                continue
            script = outer[-1] if outer else ""
            for variable, values, body in LOOP.findall(script):
                if ".systems/ai/core/" not in body or f"${variable}" not in body:
                    continue
                if not re.search(r"\b(?:cat|sed|head|tail|nl|awk|less|rg)\b", body):
                    continue
                names = [name for name in shlex.split(values) if re.fullmatch(r"[a-z0-9-]+\.md", name)]
                yield "cat " + " ".join(f".systems/ai/core/{name}" for name in names)
            for segment in re.split(r"\s*(?:;|&&|\|\|?|\n)\s*", script):
                try:
                    tokens = shlex.split(segment)
                except ValueError:
                    continue
                if not tokens or Path(tokens[0]).name not in READ_COMMANDS:
                    continue
                if Path(tokens[0]).name == "rg" and "--files" in tokens:
                    continue
                yield segment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    for config in ("baseline", "candidate"):
        for trace in sorted((args.run_root / config).glob("*/trace.jsonl")):
            case = trace.parent.name
            paths = set()
            skills = set()
            for command in completed_commands(trace):
                paths.update(CORE_PATH.findall(command))
                for names in BRACED_CORE_PATH.findall(command):
                    paths.update(f".systems/ai/core/{name}.md" for name in names.split(","))
                skills.update(SKILL_PATH.findall(command))
            metadata_path = trace.parent / "metadata.json"
            state = "running"
            if metadata_path.exists():
                state = str(json.loads(metadata_path.read_text(encoding="utf-8"))["exit_code"])
            print(f"{config}/{case} exit={state} core_reads={len(paths)}")
            for path in sorted(paths):
                print(f"  {path}")
            for path in sorted(skills):
                print(f"  skill: {path}")


if __name__ == "__main__":
    main()
