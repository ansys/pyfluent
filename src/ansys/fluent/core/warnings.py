"""Provides a module to get warnings for core functionality."""

import warnings


class PyFluentDeprecationWarning(FutureWarning):
    """Provides the common warning class for warnings about deprecated PyFluent
    features."""

    pass


class PyFluentUserWarning(UserWarning):
    """Provides the common warning class for warnings generated from user code."""

    pass


class WarningControl:
    """Class to control warnings in PyFluent."""

    def enable(self):
        """Enables all PyFluent warnings."""
        warnings.simplefilter("default", PyFluentDeprecationWarning)
        warnings.simplefilter("default", PyFluentUserWarning)

    def disable(self):
        """Disables all PyFluent warnings."""
        warnings.simplefilter("ignore", PyFluentDeprecationWarning)
        warnings.simplefilter("ignore", PyFluentUserWarning)


warning = WarningControl()
