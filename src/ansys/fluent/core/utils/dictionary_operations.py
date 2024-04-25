"""Performs some operations on Python dictionaries."""


def get_first_dict_key_for_value(input_dict, value):
    """Get the first dictionary key that matches a value."""
    return next((key for key, val in input_dict.items() if val == value), None)
