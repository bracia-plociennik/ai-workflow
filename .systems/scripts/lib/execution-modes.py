#!/usr/bin/env python3
"""Pure readiness projection. Declarations are not verified approvals or isolation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


class InvalidState(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidState(message)


def keys(value, expected, label):
    require(isinstance(value, dict) and set(value) == set(expected), label + ": fields")


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + ": nonempty text")


def flag(value, label):
    require(type(value) is bool, label + ": boolean")


def identifiers(value, label):
    require(isinstance(value, list) and all(isinstance(x, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", x) for x in value), label + ": identifiers")
    require(len(set(value)) == len(value), label + ": duplicates")


def resolve_mode(task=None, session=None, project=None, resumed=None):
    # A new explicit choice is passed by the coordinator; otherwise resume wins.
    for value in (task, session, project, resumed):
        require(value is None or isinstance(value, str) and value in {"auto", "human-coop"}, "unknown execution mode")
    choice = task or resumed or session or project or "auto"
    require(choice in {"auto", "human-coop"}, "unknown execution mode")
    return choice


def overlap(left, right):
    a, b = left.casefold().rstrip("/"), right.casefold().rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


CAPABILITY_SOURCES = {".systems/ai/core/" + name + ".md" for name in (
    "execution-modes", "autopilot", "owner-decision-checkpoints", "delivery-constraints",
    "permissions", "risk-model", "phase-commit-policy", "quality-review")}
CAPABILITY_SOURCES.update({".systems/scripts/check-execution-modes",
    ".systems/scripts/lib/execution-modes.py"})
CAPABILITY_SOURCES.update({".systems/ai/templates/autopilot/" + name for name in (
    "execution-readiness.template.json", "readiness.template.md",
    "state.template.md", "task-decisions.template.md")})
CAPABILITY_BEHAVIORS = {"scoped-approval", "dependency-local-blocking", "auto-unconstrained",
                       "three-stalled-attempts", "technical-phase-8", "human-material-questions"}


def unlinked(path, label):
    aliases = {Path("/tmp"): Path("/private/tmp"), Path("/var"): Path("/private/var")}
    require(not any(p.is_symlink() and aliases.get(p) != p.resolve()
                    for p in (path, *path.parents)), "symlink " + label)


def capability(root):
    unlinked(root, "capability root")
    root = root.resolve(strict=True)
    path = root / ".systems/ai/capabilities/execution-modes-v1.json"
    unlinked(path, "capability")
    record = json.loads(path.read_text(), object_pairs_hook=unique_keys)
    keys(record, ("contract", "capability", "behaviors", "mode_mapping", "sources"), "capability")
    require(type(record["contract"]) is int and record["contract"] == 1, "unsupported capability contract")
    require(record["capability"] == "execution-modes-v1", "unknown capability")
    require(record["mode_mapping"] == {"auto": "auto", "human": "human-coop"}, "capability mode mapping")
    identifiers(record["behaviors"], "capability behaviors")
    require(set(record["behaviors"]) == CAPABILITY_BEHAVIORS, "capability behaviors incomplete/unknown")
    keys(record["sources"], CAPABILITY_SOURCES, "capability sources")
    for name, digest in record["sources"].items():
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest), "capability hash")
        source = root / name
        unlinked(source, "capability source")
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == digest,
                "capability source mismatch: " + name)
    return {"status": "source-bound", "authority": "support-metadata-only",
            "mode_mapping": record["mode_mapping"]}


def recovery(record, units):
    if record["schema"] == 1:
        return {}, "legacy-unverified"
    data = record["recovery"]
    keys(data, ("attempts", "retry_counts"), "recovery")
    keys(data["retry_counts"], ("units", "total"), "retry counts")
    counts = data["retry_counts"]
    require(type(counts["total"]) is int and counts["total"] >= 0, "total retries")
    require(isinstance(counts["units"], dict) and set(counts["units"]).issubset(units), "retry unit identity")
    for identifier, value in counts["units"].items():
        keys(value, ("spec", "quality"), "unit retries")
        require(all(type(n) is int and n >= 0 for n in value.values()), "unit retry count")
    require(counts["total"] >= sum(sum(v.values()) for v in counts["units"].values()), "inconsistent retry total")
    require(isinstance(data["attempts"], list), "recovery attempts")
    require(counts["total"] >= len(data["attempts"]), "attempt history exceeds retry total")
    attempts, stalled, evidence = set(), {}, {}
    for attempt in data["attempts"]:
        keys(attempt, ("attempt_id", "unit_id", "cause_id", "progress_evidence"), "recovery attempt")
        for field in ("attempt_id", "unit_id", "cause_id"):
            identifiers([attempt[field]], "attempt " + field)
        require(attempt["attempt_id"] not in attempts, "duplicate recovery attempt")
        attempts.add(attempt["attempt_id"])
        require(attempt["unit_id"] in units and attempt["unit_id"] in counts["units"], "unknown recovery unit/budget")
        fingerprint = attempt["progress_evidence"]
        require(fingerprint is None or isinstance(fingerprint, str) and re.fullmatch(r"[0-9a-f]{64}", fingerprint), "progress fingerprint")
        pair = (attempt["unit_id"], attempt["cause_id"])
        # Declared evidence is deduplicated across causes within a unit.
        seen = evidence.setdefault(attempt["unit_id"], set())
        if fingerprint is not None and fingerprint not in seen:
            seen.add(fingerprint)
            stalled[pair] = 0
        else:
            stalled[pair] = stalled.get(pair, 0) + 1
    blocked = {}
    for (identifier, cause), count in stalled.items():
        if count >= 3:
            blocked.setdefault(identifier, []).append("stalled-cause:" + cause)
    for identifier, value in counts["units"].items():
        for field in ("spec", "quality"):
            if value[field] >= 2:
                blocked.setdefault(identifier, []).append("retry-limit:" + field)
    if counts["total"] >= 32:
        for identifier, unit in units.items():
            if unit["status"] != "completed":
                blocked.setdefault(identifier, []).append("retry-limit:total")
    # Budget exhaustion stops retries, not a result already accepted after its last allowed fix.
    for identifier in list(blocked):
        if units[identifier]["status"] == "completed":
            require(counts["total"] <= 32 and all(n <= 2 for n in counts["units"].get(identifier, {}).values()),
                    "completed unit exceeds retry budgets")
            require(not any(x.startswith("stalled-cause:") for x in blocked[identifier]),
                    "completed unit has stalled recovery")
            del blocked[identifier]
    return blocked, "declared-schema-2"


def assess(record):
    require(isinstance(record, dict) and type(record.get("schema")) is int and record["schema"] in {1, 2}, "unsupported projection schema")
    fields = ("schema", "execution", "baseline", "units", "decisions", "requested_status", "final_check")
    keys(record, fields + (("recovery",) if record["schema"] == 2 else ()), "projection")
    execution = record["execution"]
    keys(execution, ("mode", "scope", "scope_id", "source", "approval_reference"), "execution")
    require(isinstance(execution["mode"], str) and execution["mode"] in {"auto", "human-coop"}, "unknown execution mode")
    require(execution["scope"] in {"task", "project", "session"}, "execution scope")
    for key in ("scope_id", "source"):
        text(execution[key], key)
    require(execution["approval_reference"] is None or isinstance(execution["approval_reference"], str) and bool(execution["approval_reference"].strip()), "approval reference")
    baseline = record["baseline"]
    keys(baseline, ("assessed", "current"), "baseline")
    for key in baseline:
        text(baseline[key], "baseline")
    require(isinstance(record["units"], list) and bool(record["units"]), "empty units")
    units = {}
    blocked = {}
    completed = []
    for unit in record["units"]:
        keys(unit, ("id", "work_kind", "dependencies", "dependencies_known", "isolation_verified", "resources",
                    "gates_ready", "dod_testable", "risk", "required_actions", "approved_actions",
                    "approval_reference", "status", "quality_current", "capture_complete"), "unit")
        identifiers([unit["id"]], "unit id")
        require(unit["work_kind"] in {"planning", "implementation", "read-only"}, "unknown work kind")
        require(unit["id"] not in units, "duplicate unit id")
        identifiers(unit["dependencies"], "dependencies")
        for field in ("dependencies_known", "isolation_verified", "gates_ready", "dod_testable", "quality_current", "capture_complete"):
            flag(unit[field], field)
        require(unit["risk"] in {"low", "medium", "high", "critical"}, "unknown risk")
        require(unit["status"] in {"pending", "completed"}, "unknown unit status")
        for field in ("required_actions", "approved_actions"):
            identifiers(unit[field], field)
            require(set(unit[field]).issubset({"artifact-write", "local-write", "product-write", "formal-quality", "local-commit", "production-deploy", "external-write", "billing", "destructive", "migration", "security-change"}), "unknown action")
        require(unit["work_kind"] != "planning" or set(unit["required_actions"]).issubset({"artifact-write", "formal-quality", "local-commit"}), "planning request cannot implement")
        require(unit["work_kind"] != "implementation" or bool(set(unit["required_actions"]) & {"artifact-write", "local-write", "product-write", "production-deploy", "external-write", "billing", "destructive", "migration", "security-change"}), "implementation unit lacks declared write action")
        require(unit["work_kind"] != "read-only" or not unit["required_actions"], "read-only unit cannot request writes")
        require(isinstance(unit["resources"], list), "resource list")
        require(not unit["required_actions"] or bool(unit["resources"]), "action unit lacks resource claims")
        for resource in unit["resources"]:
            text(resource, "resource")
            require(not any(x in resource for x in ("..", "\\", "\n", "\r")) and not resource.startswith("/") and all(x not in {"", "."} for x in resource.rstrip("/").split("/")), "unsafe resource identity")
        require(len(set(unit["resources"])) == len(unit["resources"]), "duplicate resource")
        require(unit["approval_reference"] is None or isinstance(unit["approval_reference"], str) and bool(unit["approval_reference"].strip()), "unit approval reference")
        units[unit["id"]] = unit

    visited, active = set(), set()
    def visit(identifier):
        require(identifier not in active, "dependency cycle")
        if identifier in visited:
            return
        active.add(identifier)
        for dependency in units[identifier]["dependencies"]:
            require(dependency in units, "unknown dependency id")
            visit(dependency)
        active.remove(identifier)
        visited.add(identifier)
    for identifier in units:
        visit(identifier)

    blocked, recovery_status = recovery(record, units)

    for unit in units.values():
        if unit["status"] == "completed":
            require(all(units[x]["status"] == "completed" for x in unit["dependencies"]), "completed unit has unfinished dependency")

    for identifier, unit in units.items():
        reasons = blocked.get(identifier, []).copy()
        if baseline["assessed"] != baseline["current"]:
            reasons.append("baseline-drift")
        for field in ("dependencies_known", "isolation_verified", "gates_ready", "dod_testable"):
            if not unit[field]:
                reasons.append(field)
        if not set(unit["required_actions"]).issubset(unit["approved_actions"]):
            reasons.append("unapproved-action")
        if unit["risk"] in {"high", "critical"} or unit["required_actions"]:
            if not unit["approval_reference"] or not execution["approval_reference"]:
                reasons.append("missing-approval-reference")
        if unit["risk"] == "critical":
            reasons.append("human-led-critical-route")
        if unit["status"] == "completed":
            if record["schema"] == 2:
                require(record["recovery"]["retry_counts"]["total"] <= 32,
                        "completed unit exceeds retry budgets")
            require(not reasons and unit["quality_current"] and unit["capture_complete"], "completed unit lacks DoD/gates/current QA/capture")
            completed.append(identifier)
        if reasons:
            blocked[identifier] = reasons

    require(isinstance(record["decisions"], list), "decisions list")
    seen, queue = set(), []
    for decision in record["decisions"]:
        keys(decision, ("id", "classification", "disposition", "affected_units", "reversible", "within_scope", "permission_covered", "reason", "override_impact"), "decision")
        identifiers([decision["id"]], "decision id")
        require(decision["id"] not in seen, "duplicate decision id")
        seen.add(decision["id"])
        require(decision["classification"] in {"auto-resolvable", "owner-preference", "high-impact", "critical-risk", "blocked-by-missing-facts"}, "decision classification")
        require(decision["disposition"] in {"pending", "agent-choice", "owner-approved"}, "decision disposition")
        identifiers(decision["affected_units"], "affected units")
        require(bool(decision["affected_units"]) and set(decision["affected_units"]).issubset(units), "unknown/empty affected units")
        for field in ("reversible", "within_scope", "permission_covered"):
            flag(decision[field], field)
        for field in ("reason", "override_impact"):
            text(decision[field], field)
        if decision["disposition"] == "agent-choice":
            require(decision["classification"] not in {"critical-risk", "blocked-by-missing-facts"} and all(decision[x] for x in ("reversible", "within_scope", "permission_covered")), "unsafe agent choice")
            require(execution["mode"] == "auto" or decision["classification"] == "auto-resolvable", "Human Coop material preference requires owner")
            if decision["classification"] == "high-impact":
                require(bool(execution["approval_reference"]) and all(units[x]["approval_reference"] for x in decision["affected_units"]), "high-impact choice lacks scoped approval references")
        if decision["disposition"] == "owner-approved":
            require(execution["approval_reference"] is not None and decision["permission_covered"] and decision["within_scope"], "uncovered owner decision")
        if decision["disposition"] == "pending":
            queue.append(decision["id"])
            for identifier in decision["affected_units"]:
                require(identifier not in completed, "pending decision affects claimed completion")
                blocked.setdefault(identifier, []).append("decision:" + decision["id"])

    # Simultaneous candidate reservations must be disjoint, even before dispatch.
    candidates = [x for x in units if x not in completed and x not in blocked]
    for index, left in enumerate(candidates):
        for right in candidates[index + 1:]:
            if any(overlap(a, b) for a in units[left]["resources"] for b in units[right]["resources"]):
                blocked.setdefault(left, []).append("shared-resource:" + right)
                blocked.setdefault(right, []).append("shared-resource:" + left)

    # Shared reservations and dependency uncertainty prevent a claim of independence.
    changed = True
    while changed:
        changed = False
        for identifier, unit in units.items():
            if identifier in blocked or identifier in completed:
                continue
            dependencies = [x for x in unit["dependencies"] if x not in completed]
            shared = [other for other in blocked if any(overlap(a, b) for a in unit["resources"] for b in units[other]["resources"])]
            if dependencies or shared:
                blocked[identifier] = ["dependency:" + x for x in dependencies] + ["shared-resource:" + x for x in shared]
                changed = True
    ready = [x for x in units if x not in blocked and x not in completed]
    requested = record["requested_status"]
    require(requested in {"inspect", "running", "completed"}, "requested status")
    require(requested != "running" or bool(ready), "running without independent ready unit")
    require(requested != "completed" or len(completed) == len(units) and not queue, "incomplete DoD cannot be completed")
    final = record["final_check"]
    keys(final, ("requested", "approval_reference", "owner_yes"), "final check")
    flag(final["requested"], "final requested")
    flag(final["owner_yes"], "final owner yes")
    require(final["approval_reference"] is None or isinstance(final["approval_reference"], str) and bool(final["approval_reference"].strip()), "final approval reference")
    require(not final["requested"] or final["approval_reference"] is not None, "final check lacks explicit request reference")
    require(not final["owner_yes"], "projection cannot attest final-owner-yes")
    result = "completed" if len(completed) == len(units) else "running" if ready else "awaiting-owner" if queue else "blocked"
    return {"mode": execution["mode"], "ready_units": ready, "blocked_units": blocked,
            "completed_units": completed, "pending_decisions": queue, "result": result,
            "recovery_status": recovery_status,
            "authority": "inspection-only"}


def unique_keys(pairs):
    output = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key")
        output[key] = value
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--state", type=Path)
    choice.add_argument("--capability-root", type=Path)
    args = parser.parse_args()
    try:
        if args.capability_root is not None:
            output = capability(args.capability_root)
        else:
            unlinked(args.state, "projection")
            data = json.loads(args.state.read_text(), object_pairs_hook=unique_keys)
            output = assess(data)
        print(json.dumps(output, sort_keys=True))
        return 0
    except (InvalidState, OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print("Execution modes error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
