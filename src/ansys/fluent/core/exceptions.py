"""Custom common higher level exceptions."""

from ansys.fluent.core.solver.error_message import allowed_name_error_message


class DisallowedValuesError(ValueError):
    """Raises exception if argument value is not in allowed values."""

    def __init__(self, context, name, allowed_values):
        super().__init__(
            allowed_name_error_message(
                context=context, trial_name=name, allowed_values=allowed_values
            )
        )


class InvalidArgument(ValueError):
    """Raises exception for invalid argument."""

    pass


class SurfaceNameIDsProvided(ValueError):
    """Raises exception for invalid surface names and IDs."""

    pass
