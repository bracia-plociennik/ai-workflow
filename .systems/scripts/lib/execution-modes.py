#!/usr/bin/env python3
"""Pure readiness projection. Declarations are not verified approvals or isolation."""
import argparse
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


def assess(record):
    keys(record, ("schema", "execution", "baseline", "units", "decisions", "requested_status", "final_check"), "projection")
    require(type(record["schema"]) is int and record["schema"] == 1, "unsupported projection schema")
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

    for unit in units.values():
        if unit["status"] == "completed":
            require(all(units[x]["status"] == "completed" for x in unit["dependencies"]), "completed unit has unfinished dependency")

    for identifier, unit in units.items():
        reasons = []
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
            "authority": "inspection-only"}


def unique_keys(pairs):
    output = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key")
        output[key] = value
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    args = parser.parse_args()
    try:
        aliases = {Path("/tmp"): Path("/private/tmp"), Path("/var"): Path("/private/var")}
        require(not any(path.is_symlink() and aliases.get(path) != path.resolve() for path in (args.state, *args.state.parents)), "symlink projection")
        data = json.loads(args.state.read_text(), object_pairs_hook=unique_keys)
        print(json.dumps(assess(data), sort_keys=True))
        return 0
    except (InvalidState, OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print("Execution modes error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
