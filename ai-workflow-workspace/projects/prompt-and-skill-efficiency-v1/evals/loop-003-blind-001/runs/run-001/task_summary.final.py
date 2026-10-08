"""Small synthetic task-state summary module."""

STATES = ("todo", "in-progress", "done")


def canonical_state(raw):
    if not isinstance(raw, str):
        raise ValueError("state must be text")
    state = raw.strip().lower().replace("_", "-").replace(" ", "-")
    if state not in STATES:
        raise ValueError("unknown state")
    return state


def summarize_tasks(rows):
    counts = {state: 0 for state in STATES}
    for row in rows:
        counts[canonical_state(row.get("state"))] += 1
    return counts
