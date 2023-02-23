import difflib
from functools import partial
from typing import List


def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
    """Checks if the 'trail_name' is closely matching the 'allowed_names'."""
    f = partial(difflib.get_close_matches, trial_name, allowed_names)
    return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)


def allowed_name_error_message(
    context: str, trial_name: str, allowed_values: List[str]
) -> str:
    """Provide the closest names matching the 'trial_name' from the
    'allowed_values' list."""
    message = f"{trial_name} is not an allowed {context} name.\n"
    matches = closest_allowed_names(trial_name, allowed_values)
    if matches:
        message += f"The most similar names are: {', '.join(matches)}."
    return message


def allowed_values_error(
    context: str, trial_name: str, allowed_values: List[str]
) -> str:
    return ValueError(allowed_name_error_message(context, trial_name, allowed_values))
