"""Performs some operations on Python dictionaries."""

from typing import Any


def get_first_dict_key_for_value(input_dict: dict, value: Any):
    """Get the first dictionary key that matches a value. Typical usage is where the
    value is known to be unique in the input dictionary.

    Parameters
    ----------
    input_dict : dict
    value : Any

    Returns
    -------
    Any
        Key associated with the first match.

    Raises
    ------
    ValueError
        If the value is absent from the dictionary.
    """

    try:
        return next((key for key, val in input_dict.items() if val == value))
    except StopIteration:
        raise ValueError()
