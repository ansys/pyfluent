"""Custom common higher level exceptions."""

from typing import Any, Optional

from ansys.fluent.core.solver.error_message import allowed_name_error_message


class DisallowedValuesError(ValueError):
    """Provides the error when an argument value is not in allowed values."""

    def __init__(
        self,
        context: Optional[Any] = None,
        name: Optional[Any] = None,
        allowed_values: Optional[Any] = None,
    ):
        super().__init__(
            allowed_name_error_message(
                context=context, trial_name=name, allowed_values=allowed_values
            )
        )


class InvalidArgument(ValueError):
    """Provides the error when an argument value is inappropriate."""

    pass


class SurfaceSpecificationError(ValueError):
    """Provides the error when both ``surface_ids`` and ``surface_names`` are
    provided."""

    def __init__(self):
        super().__init__("Provide either 'surface_ids' or 'surface_names'.")
