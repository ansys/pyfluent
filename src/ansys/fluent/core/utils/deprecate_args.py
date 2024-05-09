"""Deprecates old argument and replaces them with corresponding new argument."""


def deprecate_arguments(old_arg, new_arg, converter):
    """Deprecates old argument and replaces them with corresponding new argument."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        def wrapper(*args, **kwargs):
            """Performs deprecation operation on arguments of the original method."""
            if old_arg in kwargs:
                converter(old_arg, new_arg, kwargs)
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
