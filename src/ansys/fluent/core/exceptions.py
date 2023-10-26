"""Custom common higher level exceptions."""


class DisallowedValuesError(ValueError):
    """Raises exception if argument value is not in allowed values."""

    pass


class InvalidArgument(ValueError):
    """Raises exception for invalid argument."""

    pass
