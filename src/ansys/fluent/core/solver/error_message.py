# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module to customize exception messages."""

import difflib
from functools import partial
from typing import Any, List


def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
    """Checks if the 'trail_name' is closely matching the 'allowed_names'."""
    f = partial(difflib.get_close_matches, trial_name, allowed_names)
    return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)


def allowed_name_error_message(
    allowed_values: Any | None = None,
    context: str | None = None,
    trial_name: str | None = None,
    message: str | None = None,
    search_results: list | None = None,
) -> str:
    """Provide an error message with the closest names matching the 'trial_name' from
    the 'allowed_values' list."""
    if not message:
        message = f"'{context}' has no attribute '{trial_name}'"
    message += ".\n"
    matches = None
    if allowed_values:
        if isinstance(allowed_values, list) and isinstance(allowed_values[0], str):
            matches = closest_allowed_names(trial_name, allowed_values)
        if matches:
            message += f"The most similar names are: {', '.join(matches)}."
        else:
            message += f"The allowed values are: {allowed_values}."
    elif search_results:
        message = message + "\nThe most similar API names are:\n"
        for search_result in search_results:
            message += search_result + "\n"

    return message


def allowed_values_error(
    context: str, trial_name: str, allowed_values: List[str]
) -> ValueError:
    """Provide an error message for disallowed values."""
    return ValueError(
        allowed_name_error_message(
            context=context, trial_name=trial_name, allowed_values=allowed_values
        )
    )
