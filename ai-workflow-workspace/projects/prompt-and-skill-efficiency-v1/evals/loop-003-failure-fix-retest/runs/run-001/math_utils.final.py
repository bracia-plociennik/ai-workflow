"""Synthetic numerical fixture for the LOOP-003 persistence eval."""


def normalize_bounds(lower, upper):
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    return lower, upper


def clamp(value, lower, upper):
    lower, upper = normalize_bounds(lower, upper)
    return min(max(value, lower), upper)
