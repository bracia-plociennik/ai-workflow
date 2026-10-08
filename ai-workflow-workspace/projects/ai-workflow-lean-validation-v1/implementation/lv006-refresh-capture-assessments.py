"""Record the real post-capture Plan/Spec/current quality re-review, retaining history."""
import importlib.util
from pathlib import Path
import re
import sys

project = Path.cwd() / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
spec = importlib.util.spec_from_file_location("assessment", project / "implementation/record-current-assessment.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

def read_current(path):
    text = path.read_text().split("## Current QA Run\n")[1]
    inputs = []
    for line in text.splitlines():
        match = re.fullmatch(r"\| (workflow-source|owning-project-evidence) \| ([^|]+) \| [0-9a-f]{64} \|", line)
        if match:
            inputs.append((match[1], match[2].strip()))
    assert inputs
    return inputs, text[text.index("### Evidence"):]

assert "- State: completed" in (project / "capture-state/lv-qa-006-integration.md").read_text()
assert "| high | done |" in (project / "tasks.md").read_text()
review = project / "reviews/lv006-post-capture-review.md"
assert review.exists() and "Semantic re-review: completed" in review.read_text()
suffix = "-" + sys.argv[1] if len(sys.argv) > 1 else ""
for filename, run, kind, identity, scope in [
    ("recovery-phase-2-plan-qa.md", "lv-plan-included-completion-2026-10-01", "plan-qa", project.name,
     "Composite plan/index with completed included tasks and explicitly deferred LV005; artifact quality only."),
    ("recovery-phase-3-lv-qa-006-integration-spec-qa.md", "lv006-spec-included-completion-2026-10-01", "spec-qa",
     project.name + ":LV-QA-006-integration",
     "Composite LV006 spec and dependency/closure disposition; artifact quality only."),
]:
    path = project / "quality" / filename
    inputs, previous_body = read_current(path)
    evidence = """- Whole preserved base plus approved amendment, current task and plan routers, explicit decision010 and current included quality/capture reviewed against unchanged architecture and owner intent.
- Completion changes only actual execution disposition, not scope, risk, DoD or source authority. LV001-LV004 and LV006 included; LV005 deferred with its original failed isolation evidence and false distilled value.
- Checked producer-consumer mapping from decision to task row, current QA, capture state, memory and required checkpoint. No hidden unfinished task, fabricated behavior grade or incomparable speed claim.
- Source interfaces unchanged except reviewed changelog integration; current full and exact 694-ID execution support implementation quality separately.
- Semantic re-review: reviews/lv006-post-capture-review.md. No unresolved material planning/specification finding.
"""
    body = qa.body(evidence, [], artifact=True).replace(
        "Current specification coherence, scope, DoD, producer-consumer mapping and dependency interfaces; not a product implementation verdict.", scope
    ).replace("runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.",
              "composite plan/spec, task index, actual quality/capture, deferral decision, current QA reader and checkpoint.")
    body = body.replace("- Spec QA result: PASS", "- Result: PASS")
    checkpoint_done = "- Result: PASS" in (project / "checkpoints/phase-7-checkpoint-2026-10-01-final.md").read_text()
    disposition = ("Included implementation, Phase 6 and required final checkpoint completed; Phase 8 remains separately owner-triggered."
                   if checkpoint_done else "Included implementation accepted; required final checkpoint remains separate.")
    body += "\n### Current Disposition\n\n" + disposition + " LV005 remains deferred, never accepted by this artifact.\n"
    if ("owning-project-evidence", "reviews/lv006-post-capture-review.md") not in inputs:
        inputs.append(("owning-project-evidence", "reviews/lv006-post-capture-review.md"))
    qa.record(path, run + suffix, kind, identity, inputs, body)
path = project / "quality/phase-5-lv-qa-006-integration-quality.md"
inputs, body = read_current(path)
if ("owning-project-evidence", "reviews/lv006-post-capture-review.md") not in inputs:
    inputs.append(("owning-project-evidence", "reviews/lv006-post-capture-review.md"))
if "### Current Capture Re-review" not in body:
    body += "\n### Current Capture Re-review\n\nFull current state re-reviewed after capture/index synchronization. Source bytes and full execution unchanged; renewed Plan/Spec assessments reflect actual done/deferred dispositions. No unsupported freshness or extra authority.\n"
qa.record(path, "lv006-quality-capture-current-2026-10-01" + suffix, "implementation-quality",
          project.name + ":LV-QA-006-integration", inputs, body)
print("Recorded actual post-capture Plan/Spec and LV006 quality re-review; historical runs preserved.")
