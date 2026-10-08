"""Synthetic numerical fixture for the LOOP-003 persistence eval."""


def normalize_bounds(lower, upper):
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    return upper, lower


def clamp(value, lower, upper):
    raise NotImplementedError
