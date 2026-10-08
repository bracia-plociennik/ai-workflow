"""Render fresh artifact QA after the documented prerequisite regression review."""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROJECT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location(
    "quality_record", ROOT / ".systems/scripts/lib/quality-record.py")
producer = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(producer)
workspace = PROJECT.parents[1]

paths = [PROJECT / "quality/phase-1-architecture-qa.md",
         PROJECT / "quality/phase-2-plan-qa.md"]
paths += sorted((PROJECT / "quality").glob("phase-3-*-spec-qa.md"))
for index, path in enumerate(paths):
    old = path.read_text()
    lines = old.splitlines()
    start, end = producer.qa.current_section(lines)
    metadata, sections = producer.qa.read_current(lines)
    inputs = []
    for line in sections["Input Artifacts"]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 3 and cells[0] in producer.qa.ROOTS:
            inputs.append({"root": cells[0], "path": cells[1]})
    review_input = {"root": "owning-project-evidence",
                    "path": "reviews/prerequisite-refresh-001.md"}
    if review_input not in inputs:
        inputs.append(review_input)
    supplied = {key: "\n".join(value).strip()
                for key, value in sections.items() if key != "Input Artifacts"}
    supplied["Evidence"] += (
        "\nFresh complete prerequisite regression review: "
        "reviews/prerequisite-refresh-001.md. Changed autopilot policy preserves "
        "all accepted architecture/plan/spec boundaries; implementation gate "
        "is distinct and current owner implementation approval is recorded.")
    identity = metadata["Project/task identity"]
    previous = re.match(r"pto-prerequisite-refresh-(\d+)-", metadata["Run ID"])
    revision = int(previous.group(1)) + 1 if previous else 1
    record = {"schema": 1, "kind": metadata["Artifact kind"],
              "task": identity.split(":", 1)[1] if ":" in identity else None,
              "run_id": f"pto-prerequisite-refresh-{revision:03d}-{index:03d}",
              "verdict": "PASS", "date": "2026-10-04",
              "inputs": inputs, "sections": supplied}
    output, body = producer.render(record, ROOT, workspace, PROJECT.name)
    history = "\n".join(lines[start + 1:end]).strip()
    prior_history = old.split("## Historical Runs", 1)[1].strip() if "## Historical Runs" in old else ""
    body += "\n## Historical Runs\n\nSuperseded input-bound assessments; not current eligibility.\n\n" + history + "\n\n" + prior_history + "\n"
    producer.qa.assess(output, ROOT, workspace, PROJECT.name, document=body)
    path.write_text(body)
    print(path.name)
