#!/usr/bin/env python3
"""Pure eligibility helpers; classification never grants write or QA authority."""
EXCLUDED = {'api', 'schema', 'protocol', 'policy', 'routing', 'approval', 'privacy', 'permissions',
            'security', 'migration', 'client', 'production', 'external-effects', 'dependency', 'cross-module'}


def micro_exempt(*, risk, files, reversible, local, themes, one_change, active_plan=False):
    return (risk == 'low' and reversible is True and local is True and one_change is True
            and active_plan is False and 1 <= len(set(files)) <= 3 and len(set(files)) == len(files)
            and not EXCLUDED.intersection(themes))


def response_mode(*, simple_answer=False, micro_eligible=False, formal=False, decision=False,
                  blocker=False, handoff=False, material_limits=False):
    return 'compact' if (simple_answer or micro_eligible) and not any(
        (formal, decision, blocker, handoff, material_limits)) else 'full'


def model_capability(*, risk, ambiguous=False, adversarial=False):
    return 'strong-reasoning' if risk in {'high', 'critical'} or ambiguous or adversarial else 'efficient-reasoning'
