"""Bind the documented fresh PTO-001 assessment and preserve prior QA bytes."""
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[2]
spec = importlib.util.spec_from_file_location("quality_record", ROOT / ".systems/scripts/lib/quality-record.py")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)
record = json.loads((PROJECT / "reviews/pto-001-formal-quality-input.json").read_text())
record["run_id"] = "pto-001-regression-quality-002"
record["inputs"].append({"root": "owning-project-evidence", "path": "reviews/pto-001-regression-reassessment.md"})
record["sections"]["Evidence"] = (
    "- Fresh eighteen-source regression assessment: reviews/pto-001-regression-reassessment.md.\n"
    "- Current core smoke passed in 64 seconds; all 37 PTO-001 policy regressions retained.\n"
    "- Original 666-second full run is historical; new PTO-002 final source full is not claimed.\n"
    "- Unchanged human high-risk approval: decisions/pto-001-quality-approval.md.")
record["sections"]["Review Completeness Gate"] = record["sections"]["Review Completeness Gate"].replace(
    "8a0eeef and reviews/pto-001-source-snapshot.json, all eighteen files unchanged",
    "8a0eeef, all eighteen current source paths; three shared additive smoke integration changes reviewed")
record["sections"]["Review Completeness Gate"] += (
    "\n- Fresh regression assessment: reviews/pto-001-regression-reassessment.md; original history preserved.")
output, body = producer.render(record, ROOT, PROJECT.parents[1], PROJECT.name)
old = output.read_text()
start, end = producer.qa.current_section(old.splitlines())
history = "\n".join(old.splitlines()[start + 1:end]).strip()
prior = old.split("## Historical Runs", 1)[1].strip() if "## Historical Runs" in old else ""
body += "\n## Historical Runs\n\nSuperseded assessments; not current eligibility.\n\n" + history + "\n\n" + prior + "\n"
producer.qa.assess(output, ROOT, PROJECT.parents[1], PROJECT.name, document=body)
output.write_text(body)
print(output)
