"""Synthetic product module; the name does not refer to an AI Workflow skill."""


def report_status(values: list[int]) -> str:
    if not values:
        return "empty"
    return str(sum(values) // len(values))
