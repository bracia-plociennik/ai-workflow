"""Render explicitly reviewed CR planning records, preserving prior QA runs."""
import importlib.util
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parents[1]
ROOT = WORKSPACE.parent
spec = importlib.util.spec_from_file_location(
    "review_producer", ROOT / ".systems/scripts/lib/quality-record.py")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)

for name in ("architecture", "plan", "spec-008", "spec-009"):
    record = producer.strict_json(PROJECT / ("evidence/pre-final-" + name + "-review.json"))
    output, body = producer.render(record, ROOT, WORKSPACE, PROJECT.name)
    if output.exists():
        old = output.read_text()
        lines = old.splitlines()
        start, end = producer.qa.current_section(lines)
        current, _ = producer.qa.read_current(lines)
        if current["Run ID"] == record["run_id"]:
            raise ValueError("already published run; do not silently refresh hashes")
        old_run = "\n".join(lines[start + 1:end]).strip()
        history = old.split("## Historical Runs", 1)[1].strip() if "## Historical Runs" in old else ""
        body += ("\n## Historical Runs\n\nEarlier assessments retained as history, not authority "
                 "for the added CR scope.\n\n" + old_run + "\n\n" + history + "\n")
    producer.qa.assess(output, ROOT, WORKSPACE, PROJECT.name, document=body)
    output.write_text(body)
    print(output.name)
