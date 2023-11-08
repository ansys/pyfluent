import difflib
from functools import partial
from typing import Any, List


def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
    """Checks if the 'trail_name' is closely matching the 'allowed_names'."""
    f = partial(difflib.get_close_matches, trial_name, allowed_names)
    return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)


def allowed_name_error_message(
    context: str, trial_name: str, allowed_values: Any
) -> str:
    """Provide an error message with the closest names matching the 'trial_name' from
    the 'allowed_values' list."""
    message = f"{trial_name} is not an allowed {context} name.\n"
    matches = None
    if allowed_values:
        if isinstance(allowed_values, list) and isinstance(allowed_values[0], str):
            matches = closest_allowed_names(trial_name, allowed_values)
        if matches:
            message += f"The most similar names are: {', '.join(matches)}."
        else:
            message += f"The allowed values are: {allowed_values}."

    return message


def allowed_values_error(
    context: str, trial_name: str, allowed_values: List[str]
) -> ValueError:
    return ValueError(allowed_name_error_message(context, trial_name, allowed_values))
