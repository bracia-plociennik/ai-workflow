"""Synthetic run-summary implementation target."""


def summarize_runs(events):
    summary = {"total": 0, "ok": 0, "failed": 0}

    for event in events:
        state = event.get("state")
        if state not in ("ok", "failed"):
            raise ValueError("event state must be 'ok' or 'failed'")
        summary["total"] += 1
        summary[state] += 1

    return summary
