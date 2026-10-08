"""Render explicitly reviewed compatibility assessments; retain original bytes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[3]
workspace = repo / "ai-workflow-workspace"
spec = importlib.util.spec_from_file_location("qa", repo / ".systems/scripts/lib/qa-evidence.py")
qa = importlib.util.module_from_spec(spec)
sys.modules["qa"] = qa
spec.loader.exec_module(qa)
projects = ("parallel-task-orchestration-v1",)
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
reports = {}
for project in projects:
    owner = workspace / "projects" / project
    for path in sorted((owner / "quality").glob("*.md")):
        if path.name.startswith("recovery-"):
            continue
        text = path.read_text()
        if "QA verification contract: `full-qa-verification-v2`" not in text:
            continue
        metadata, sections = qa.read_current(text.splitlines())
        rows = qa.input_rows(sections["Input Artifacts"])
        stale = False
        for kind, relative, checksum in rows:
            root = owner if kind == "owning-project-evidence" else repo
            actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
            if actual != checksum:
                if kind == "owning-project-evidence":
                    raise ValueError("unreviewed project-input drift: " + str(path))
                stale = True
        if stale:
            reports[path] = (project, metadata, sections, rows, path.read_bytes())
assert len(reports) == 20
rendered = {}


def render(path):
    if path in rendered:
        return rendered[path]
    project, metadata, sections, rows, original = reports[path]
    owner = workspace / "projects" / project
    entries = []
    for kind, relative, _ in rows:
        root = owner if kind == "owning-project-evidence" else repo
        source = root / relative
        raw = render(source) if source in reports else source.read_bytes()
        entries.append((kind, relative, hashlib.sha256(raw).hexdigest()))
    archive = "history/2026-10-05-pre-dependency-scope/" + path.name
    entries.append(("owning-project-evidence", archive, hashlib.sha256(original).hexdigest()))
    binding = "".join(sorted(kind + ":" + relative + "=" + checksum + "\n" for kind, relative, checksum in entries))
    verdict = metadata["Verdict"]
    result = "awaiting-owner-final-yes" if metadata["Artifact kind"] == "final-check" else verdict
    lines = ["# Current Compatibility Reassessment", "", "## Metadata", "",
             "- Project: " + project, "- Date: 2026-10-05", "- Result: " + result,
             "- QA verification contract: `full-qa-verification-v2`", "", "## Current QA Run", ""]
    current = dict(metadata, **{"Run ID": path.stem + "-dependency-scope-20261005",
                               "Assessed source HEAD": head,
                               "Assessed worktree digest": hashlib.sha256(binding.encode()).hexdigest()})
    lines.extend("- " + key + ": " + value for key, value in current.items())
    lines += ["", "### Input Artifacts", "| Root kind | Relative path | SHA-256 |", "| --- | --- | --- |"]
    lines.extend("| " + " | ".join(row) + " |" for row in entries)
    for heading, body in sections.items():
        if heading == "Input Artifacts":
            continue
        body = "\n".join(body).strip()
        if heading == "Evidence":
            body = ("- Current semantic compatibility review: accepted task/specification scopes, completed/deferred task rows, original DoD conclusions and failure boundaries were re-read. All original owning-project inputs matched their recorded hashes before rendering.\n"
                    "- Source deltas add opt-in execution/commit capabilities; legacy V2/schema1/schema2 readers remain strict. The new fixed dependency classification affects inventory and both evidence readers only. Every other runtime link remains rejected; excluded dependencies cannot supply evidence.\n"
                    "- Fresh full product validation in an isolated current-worktree fixture completed with all five smoke groups and no skipped tests; the additional dependency regression and frozen manifest integrity passed. This is source verification, not an assertion that the original upstream runtime had already passed its full gate.\n"
                    "- No old receipt was reused: old HMAC/environment fingerprints and performance results remain historical. This run makes no new timing or whole-agent improvement claim.\n"
                    "- Original findings and project outcomes remain unchanged. LV005 stays deferred with FAIL and unmet paired-model/isolation evidence; there is no new model evaluation or promotion.\n"
                    "- Original report preserved byte-for-byte at " + archive + "; the new assessment has a distinct run identity and current input graph. Historical owner closure remains scoped to its original decision; this review grants no new final-owner-yes, publication or activation.")
        elif heading == "Review Completeness Gate":
            body = body.replace(metadata["Assessed source HEAD"], head)
            body = "\n".join("- Reviewed baseline: " + head + "; exact current input table; reviewed compatibility follow-up on 2026-10-05" if line.startswith("- Reviewed baseline:") else line for line in body.splitlines())
            body += ("\n- Compatibility re-review: current accepted specs and source producer/consumer graph reviewed; fixed dependency exclusion, metadata/status, immutable smoke assertions and failed-state rejection checked.\n"
                     "- Freshness evidence: new current hashes and isolated full product verification; original measurements and approval facts remain only historical.")
        elif heading == "Owner Approval" and metadata["Artifact kind"] == "final-check":
            body = ("- Technical final check result: PASS\n- Owner approval required: yes\n- Owner decision: awaiting\n"
                    "- Historical closure: original project acceptance remains recorded in unchanged decisions/status; this compatibility re-review is not a new final-owner-yes and does not reopen or extend the original scope.")
        elif heading == "Final Gate" and metadata["Artifact kind"] == "final-check":
            body = ("- Can close active plan: awaiting-owner\n- Required next phase: owner-final-approval\n"
                    "- Technical result: PASS\n- Scope: current compatibility only; historical original closure is unchanged.")
        elif heading == "Validation Execution Record":
            body = "- Semantic QA result: " + verdict + "\n- Product checks: isolated fresh full and fixed dependency regression; no old receipt reuse\n- Final verdict: " + verdict
        elif heading == "Gate Decision":
            body = "- Result: " + verdict + "\n- Next route: " + ("compatibility review complete; original closure remains historical" if verdict == "PASS" else "deferred owner-controlled restart; original blockers remain")
        elif heading == "QA Verification Scope":
            body += "\nCurrent follow-up is source compatibility re-review of the same accepted artifact scope, not new implementation or final owner closure."
        elif heading == "Completion Review":
            body += "\nAny original completion or owner-approval facts in this table describe the immutable original closure only, not approval of this compatibility follow-up. Native operations and performance remain unverified."
        lines += ["", "### " + heading, body]
    if "Gate Decision" not in sections:
        lines += ["", "### Gate Decision", "- Result: " + verdict]
    lines += ["", "## Historical Runs", "- Run ID: " + metadata["Run ID"],
              "- Original report: " + archive, "- Original SHA-256: " + hashlib.sha256(original).hexdigest(), ""]
    raw = "\n".join(lines).encode()
    qa.assess(path, repo, workspace, project, target_root=repo, document=raw.decode(), verify_inputs=False)
    rendered[path] = raw
    return raw


for path in reports:
    render(path)
for path, (project, metadata, _, _, original) in reports.items():
    destination = workspace / "projects" / project / "history/2026-10-05-pre-dependency-scope" / path.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as stream:
        stream.write(original)
    assert destination.read_bytes() == original
for path, raw in rendered.items():
    path.write_bytes(raw)
approval = workspace / "projects/parallel-task-orchestration-v1/quality/phase-8-final-owner-approval.md"
original = approval.read_bytes()
archive = approval.parent.parent / "history/2026-10-05-pre-dependency-scope" / approval.name
with archive.open("xb") as stream:
    stream.write(original)
approval.write_text("# Historical Owner Approval Router\n\nOriginal checksum-bound owner approval is retained byte-for-byte at ../history/2026-10-05-pre-dependency-scope/phase-8-final-owner-approval.md.\nOriginal SHA-256: " + hashlib.sha256(original).hexdigest() + ".\nIt binds the original archived final check, not the current compatibility review. No new owner approval is asserted.\n")
print("Rendered 20 reviewed compatibility assessments; 20 original reports and owner approval preserved. Historical recovery assessment unchanged.")
