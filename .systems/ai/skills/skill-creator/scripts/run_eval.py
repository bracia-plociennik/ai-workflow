#!/usr/bin/env python3
"""Validate a skill eval plan and create a local A/B eval run scaffold."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

try:
    from utils import dump_json, load_json, write_text
except ImportError:  # pragma: no cover
    from .utils import dump_json, load_json, write_text


ALLOWED_MODES = {"manual-review", "local-script", "approved-subagent"}
DEFAULT_CONFIGURATIONS = ("with_skill", "baseline")
SAFE_DIR_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def safe_dir_name(value: object, label: str) -> str:
    name = str(value)
    if (
        not SAFE_DIR_NAME_RE.fullmatch(name)
        or name in {".", ".."}
        or "/" in name
        or "\\" in name
        or Path(name).is_absolute()
    ):
        raise ValueError(
            f"Invalid {label} for filesystem directory: {name!r}. "
            "Use letters, digits, dots, underscores, or hyphens only; do not use path separators."
        )
    return name


def validate_plan(plan: dict, source: Path) -> list[dict]:
    mode = plan.get("mode")
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Invalid eval mode in {source}: {mode}")
    evals = plan.get("evals")
    if not isinstance(evals, list) or not evals:
        raise ValueError(f"Eval plan must contain a non-empty evals list: {source}")
    seen_ids: set[str] = set()
    for item in evals:
        if not isinstance(item, dict):
            raise ValueError("Each eval must be an object")
        for key in ("id", "prompt", "expected_behavior"):
            if key not in item:
                raise ValueError(f"Eval missing required key '{key}': {item}")
        eval_id = safe_dir_name(item["id"], "eval id")
        if eval_id in seen_ids:
            raise ValueError(f"Duplicate eval id in {source}: {eval_id}")
        seen_ids.add(eval_id)
        if not isinstance(item["expected_behavior"], list) or not item["expected_behavior"]:
            raise ValueError(f"Eval expected_behavior must be a non-empty list: {item.get('id')}")
        assertions = item.get("assertions", [])
        if assertions and not isinstance(assertions, list):
            raise ValueError(f"Eval assertions must be a list: {item.get('id')}")
    return evals


def plan_configurations(plan: dict, override: str | None) -> list[str]:
    if override:
        configs = [part.strip() for part in override.split(",") if part.strip()]
    else:
        configs = plan.get("configurations", list(DEFAULT_CONFIGURATIONS))
    if not isinstance(configs, list) or not configs:
        raise ValueError("Configurations must be a non-empty list")
    names = [safe_dir_name(config, "configuration") for config in configs]
    if len(names) != len(set(names)):
        raise ValueError("Configurations must be unique")
    return names


def eval_assertions(item: dict) -> list[dict]:
    assertions = item.get("assertions")
    if isinstance(assertions, list) and assertions:
        return assertions
    return [
        {
            "text": text,
            "type": "required",
            "method": "manual-review",
        }
        for text in item["expected_behavior"]
    ]


def plan_fingerprint(plan: dict) -> str:
    payload = json.dumps(plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def preflight_graded_run(run_dir: Path, manifest: dict, metadata_by_id: dict[str, dict]) -> None:
    grades = sorted(run_dir.rglob("grading.json")) if run_dir.is_dir() else []
    if not grades:
        return

    fresh_run = "Use a fresh --output-dir; existing grading.json evidence was not changed."
    old_manifest_path = run_dir / "run.json"
    if not old_manifest_path.is_file():
        raise ValueError(f"Graded run lacks run.json. {fresh_run}")
    old_manifest = load_json(old_manifest_path)
    stable_fields = ("source_plan", "skill_name", "target_path", "mode", "configurations", "eval_count", "plan_sha256")
    if any(old_manifest.get(field) != manifest[field] for field in stable_fields):
        raise ValueError(f"Graded run does not match the current eval plan or lacks its fingerprint. {fresh_run}")

    allowed_configs = set(manifest["configurations"])
    for grade in grades:
        parts = grade.relative_to(run_dir).parts
        if len(parts) != 3 or parts[2] != "grading.json" or parts[0] not in metadata_by_id or parts[1] not in allowed_configs:
            raise ValueError(f"Orphan or unexpected grading file: {grade}. {fresh_run}")
        metadata_path = run_dir / parts[0] / "eval_metadata.json"
        if not metadata_path.is_file() or load_json(metadata_path) != metadata_by_id[parts[0]]:
            raise ValueError(f"Grading metadata is missing or stale for {grade}. {fresh_run}")


def create_run(plan_path: Path, output_dir: Path, overwrite: bool, config_override: str | None) -> Path:
    plan = load_json(plan_path)
    evals = validate_plan(plan, plan_path)
    configurations = plan_configurations(plan, config_override)
    run_manifest = {
        "source_plan": str(plan_path),
        "skill_name": plan.get("skill_name", "unknown"),
        "target_path": plan.get("target_path", ""),
        "mode": plan["mode"],
        "configurations": configurations,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "eval_count": len(evals),
        "plan_sha256": plan_fingerprint(plan),
    }
    metadata_by_id = {}
    for item in evals:
        eval_id = safe_dir_name(item["id"], "eval id")
        metadata_by_id[eval_id] = {
            "eval_id": eval_id,
            "eval_name": item.get("name", eval_id),
            "prompt": item["prompt"],
            "files": item.get("files", []),
            "expected_output": item.get("expected_output", ""),
            "assertions": eval_assertions(item),
            "forbidden_behavior": item.get("forbidden_behavior", []),
            "configurations": configurations,
        }

    run_dir = output_dir
    preflight_graded_run(run_dir, run_manifest, metadata_by_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    dump_json(run_dir / "run.json", run_manifest, overwrite=overwrite)

    for eval_id, metadata in metadata_by_id.items():
        eval_dir = run_dir / eval_id
        eval_dir.mkdir(parents=True, exist_ok=True)
        dump_json(eval_dir / "eval_metadata.json", metadata, overwrite=overwrite)

        for config in configurations:
            config_dir = eval_dir / config
            (config_dir / "outputs").mkdir(parents=True, exist_ok=True)
            write_text(config_dir / "transcript.todo.md", "# Transcript Todo\n", overwrite=overwrite)
            write_text(config_dir / "outputs" / "README.md", "# Outputs\n\nPlace run outputs here.\n", overwrite=overwrite)
            write_text(
                config_dir / "grading.todo.md",
                "# Grading Todo\n\nUse `agents/grader.md` and write `grading.json` when reviewed.\n",
                overwrite=overwrite,
            )
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evals_json", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--configs", help="Comma-separated configuration names")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        run_dir = create_run(args.evals_json, args.output_dir, args.overwrite, args.configs)
    except (ValueError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Created eval run scaffold: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
