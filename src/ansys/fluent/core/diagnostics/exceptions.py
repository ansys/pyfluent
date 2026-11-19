# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Custom common higher level exceptions."""

from collections.abc import Iterable
from typing import Any
import warnings

__all__ = (
    "DisallowedValuesError",
    "InvalidArgument",
    "BetaFeaturesNotEnabled",
    "PyFluentDeprecationWarning",
    "PyFluentUserWarning",
    "FluentDevVersionWarning",
    "warning",
)


class DisallowedValuesError(ValueError):
    """Raised when an argument value is not in the allowed values."""

    def __init__(
        self,
        context: str | None = None,
        name: Any | None = None,
        allowed_values: Iterable[Any] | None = None,
    ) -> None:
        """Initialize DisallowedValuesError."""
        from ansys.fluent.core.solver.error_message import allowed_name_error_message

        self._message = allowed_name_error_message(
            context=context,
            trial_name=name,
            allowed_values=allowed_values,
            message=f"{name} is not an allowed {context}",
        )
        # Forward the original arguments so pickle and copy.copy can
        # reconstruct the exception via ``cls(*exc.args)``.
        super().__init__(context, name, allowed_values)

    def __str__(self) -> str:
        """Return the formatted error message."""
        return self._message


class InvalidArgument(ValueError):
    """Raised when an argument value is inappropriate."""

    pass


class BetaFeaturesNotEnabled(RuntimeError):
    """Raised when a beta feature is accessed without enabling beta features."""

    def __init__(self, feature_name: str | None = None) -> None:
        base_message = (
            " is a Fluent beta feature. To enable it from Python "
            "call '<session>.enable_beta_features()'."
        )
        message = (
            f"'{feature_name}'" + base_message
            if feature_name
            else "This " + base_message
        )
        super().__init__(message)


class PyFluentDeprecationWarning(FutureWarning):
    """Provides the common warning class for warnings about deprecated PyFluent
    features."""

    pass


class PyFluentUserWarning(UserWarning):
    """Provides the common warning class for warnings generated from user code."""

    pass


class FluentDevVersionWarning(PyFluentUserWarning):
    """Warning raised when a released PyFluent version is used with a development version of Fluent."""

    pass


# Deriving from the base Warning instead of any derived classes
# to have less chance of being ignored by user configurations.
class InsecureGrpcWarning(Warning):
    """Warning raised when gRPC connection is insecure."""

    pass


class DeprecatedSettingWarning(PyFluentDeprecationWarning):
    """Provides deprecated settings warning."""

    pass


warnings.filterwarnings("always", category=InsecureGrpcWarning)


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


def _format_bytes(num_bytes: int) -> str:
    """Return a human-readable binary size string for a byte count."""
    size = float(num_bytes)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024.0 or unit == "TiB":
            return f"{int(size)} B" if unit == "B" else f"{size:.2f} {unit}"
        size /= 1024.0


class IncompleteSolutionVariableDataError(RuntimeError):
    """Raised when streamed solution variable data ends before all elements arrive.

    The server first declares how many elements it will send for a zone
    (``field_size``), and the client reconstructs the array from the streamed
    chunks. If the stream ends before ``field_size`` elements have been
    received, the data for that zone is incomplete and this error is raised.

    The usual cause is that a *single* zone's data is too large for the server
    to stream in one response, so the server stops sending before all elements
    are delivered. This is common for large multi-component fields -- for
    example ``SV_CENTROID`` (3 components) on a cell zone with hundreds of
    millions of cells.

    Note that the client ``chunk_size`` setting does not help here: it only
    controls how a response is sliced into messages, not the total amount of
    data requested for a zone.

    To work around it:

    * If several zones were requested in one call, request each zone separately
      so no single response is oversized.
    * If a single zone is itself too large, reduce the amount of data (for
      example request a scalar field rather than a multi-component one), split
      the zone into smaller cell zones, or read the values from the case/data
      file offline instead of over gRPC.

    Attributes
    ----------
    received : int
        Number of elements actually received before the stream ended.
    expected : int
        Number of elements the server declared it would send for the zone.
    item_size : int | None
        Size in bytes of a single element, when known. Used to report the
        approximate payload size in the error message.
    """

    def __init__(self, received: int, expected: int, item_size: int | None = None):
        """Initialize IncompleteSolutionVariableDataError."""
        self.received = received
        self.expected = expected
        self.item_size = item_size

        if item_size:
            size_note = f" (~{_format_bytes(expected * item_size)} requested)"
        else:
            size_note = ""

        self._message = (
            f"Solution variable data stream ended prematurely: received "
            f"{received:,} of {expected:,} expected elements{size_note}. "
            f"This usually means a single zone's data is too large for the "
            f"server to stream in one response. Note that changing the client "
            f"chunk size does not help, because it does not reduce the per-zone "
            f"total. To work around it: if you requested several zones in one "
            f"call, request each zone separately; if a single zone is too large "
            f"(common for multi-component fields such as 'SV_CENTROID' on very "
            f"large cell zones), request a smaller field, or split the zone into "
            f"smaller cell zones."
        )
        super().__init__(received, expected, item_size)

    def __str__(self) -> str:
        """Return the formatted error message."""
        return self._message


class BadReductionRequest(Exception):
    """Raised on an attempt to make a bad reduction request."""

    def __init__(self, err):
        """Initialize BadReductionRequest."""
        super().__init__(f"Could not complete reduction function request: {err}")


warning = WarningControl()
