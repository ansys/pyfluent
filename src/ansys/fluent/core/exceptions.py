"""Custom common higher level exceptions."""

from typing import Any

from ansys.fluent.core.solver.error_message import allowed_name_error_message


class DisallowedValuesError(ValueError):
    """Raised when an argument value is not in the allowed values."""

    def __init__(
        self,
        context: Any | None = None,
        name: Any | None = None,
        allowed_values: Any | None = None,
    ):
        """Initialize DisallowedValuesError."""
        super().__init__(
            allowed_name_error_message(
                context=context, trial_name=name, allowed_values=allowed_values
            )
        )


class InvalidArgument(ValueError):
    """Raised when an argument value is inappropriate."""

    pass
