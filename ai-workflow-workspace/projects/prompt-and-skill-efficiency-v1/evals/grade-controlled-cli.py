#!/usr/bin/env python3
"""Apply the frozen CORE-001 relevance rubric to completed direct-read traces."""

import argparse
import json
from pathlib import Path
import runpy


HELPER = runpy.run_path(str(Path(__file__).with_name("summarize-controlled-cli.py")))
COMMON = {
    "operating-model", "command-routing", "risk-model", "permissions",
    "response-contract", "model-selection-guidance", "contract-compliance",
    "instruction-adherence-refresh",
}
CASE_RELEVANT = {
    "tiny-doc-fix": {"task-intake", "owner-decision-checkpoints", "plan-quality-contract", "definition-of-done", "implementation-slicing", "delivery-constraints", "quality-review", "full-qa-verification", "knowledge-capture-reminder"},
    "frontend-ui": {"task-intake", "owner-decision-checkpoints", "plan-quality-contract", "definition-of-done"},
    "backend-only-near-miss": {"quality-review", "full-qa-verification", "owner-decision-checkpoints"},
    "blockchain-review": {"quality-review", "full-qa-verification", "owner-decision-checkpoints"},
    "skill-create": {"task-intake", "owner-decision-checkpoints", "plan-quality-contract", "definition-of-done"},
    "formal-phase-qa": {"workflow", "definition-of-done", "quality-review", "full-qa-verification"},
    "skill-review-near-miss": {"quality-review", "full-qa-verification"},
    "mixed-web3-ui": {"task-intake", "owner-decision-checkpoints", "plan-quality-contract", "definition-of-done"},
    "security-readonly": {"quality-review", "full-qa-verification", "owner-decision-checkpoints"},
    "local-completion-loop": {"task-intake", "owner-decision-checkpoints", "plan-quality-contract", "definition-of-done", "implementation-slicing", "delivery-constraints", "quality-review", "full-qa-verification", "knowledge-capture-reminder"},
}


def paths_for_trace(trace):
    result = set()
    for command in HELPER["completed_commands"](trace):
        result.update(path.removeprefix(".systems/ai/core/").removesuffix(".md") for path in HELPER["CORE_PATH"].findall(command))
        for names in HELPER["BRACED_CORE_PATH"].findall(command):
            result.update(names.split(","))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline_root", type=Path)
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    totals = {}
    for config, root in (("baseline", args.baseline_root), ("candidate", args.candidate_root)):
        totals[config] = 0
        for trace in sorted(root.glob("*/trace.jsonl")):
            case = trace.parent.name
            if case not in CASE_RELEVANT:
                raise SystemExit(f"unclassified case: {case}")
            metadata = trace.parent / "metadata.json"
            if not metadata.exists() or json.loads(metadata.read_text(encoding="utf-8"))["exit_code"] != 0:
                print(f"{config}/{case}: incomplete; excluded")
                continue
            paths = paths_for_trace(trace)
            irrelevant = sorted(paths - COMMON - CASE_RELEVANT[case])
            totals[config] += len(irrelevant)
            print(f"{config}/{case}: read={len(paths)} irrelevant={len(irrelevant)} [{', '.join(irrelevant)}]")
    print(f"TOTAL baseline={totals['baseline']} candidate={totals['candidate']}")


if __name__ == "__main__":
    main()
