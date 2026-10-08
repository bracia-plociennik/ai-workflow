"""Small synthetic task-state summary module."""

STATES = ("todo", "in-progress", "done")


def canonical_state(raw):
    if not isinstance(raw, str):
        raise ValueError("state must be text")
    state = raw.strip().lower().replace("_", "-")
    if state not in STATES:
        raise ValueError("unknown state")
    return state


def summarize_tasks(rows):
    raise NotImplementedError
