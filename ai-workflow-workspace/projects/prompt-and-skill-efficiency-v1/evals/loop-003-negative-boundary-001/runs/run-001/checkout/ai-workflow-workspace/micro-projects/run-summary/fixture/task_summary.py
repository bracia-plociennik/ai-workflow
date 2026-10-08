"""Summarize synthetic run events."""


def summarize_runs(events):
    summary = {"total": 0, "ok": 0, "failed": 0}

    for event in events:
        state = event.get("state")
        if state not in ("ok", "failed"):
            raise ValueError(f"invalid run state: {state!r}")

        summary["total"] += 1
        summary[state] += 1

    return summary
