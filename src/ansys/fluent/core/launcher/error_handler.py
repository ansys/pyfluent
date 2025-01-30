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

"""Provides a module for customized error handling."""

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.utils.fluent_version import FluentVersion


class InvalidPassword(ValueError):
    """Raised when password is invalid."""

    def __init__(self):
        """Initialize InvalidPassword."""
        super().__init__("Provide correct 'password'.")


class GPUSolverSupportError(ValueError):
    """Raised when an unsupported Fluent version is specified."""

    def __init__(self):
        """Initialize GPUSolverSupportError."""
        super().__init__("Fluent GPU Solver is only supported for 3D.")


class IpPortNotProvided(ValueError):
    """Raised when IP address and port are not specified."""

    def __init__(self):
        """Initialize IpPortNotProvided."""
        super().__init__("Provide either 'ip' and 'port' or 'server_info_file_name'.")


class InvalidIpPort(ValueError):
    """Raised when IP address and port are invalid."""

    def __init__(self):
        """Initialize InvalidIpPort."""
        super().__init__("Provide a valid 'ip' and 'port'.")


class UnexpectedKeywordArgument(TypeError):
    """Raised when a valid keyword argument is not specified."""

    pass


class LaunchFluentError(Exception):
    """Exception class representing launch errors."""

    def __init__(self, launch_string):
        """__init__ method of LaunchFluentError class."""
        details = "\n" + "Fluent Launch string: " + launch_string
        super().__init__(details)


def _raise_non_gui_exception_in_windows(
    ui_mode, product_version: FluentVersion
) -> None:
    """Fluent user interface mode lower than ``UIMode.HIDDEN_GUI`` is not supported in
    Windows in Fluent versions earlier than 2024 R1."""
    from ansys.fluent.core.launcher.pyfluent_enums import UIMode

    if (
        launcher_utils.is_windows()
        and UIMode(ui_mode) not in [UIMode.GUI, UIMode.HIDDEN_GUI]
        and product_version < FluentVersion.v241
    ):
        raise InvalidArgument(
            f"'{ui_mode}' supported in Windows only for {str(FluentVersion.v241)} or later."
        )


def _process_kwargs(kwargs):
    """Verify whether keyword arguments are valid or not.

    Parameters
    ----------
    kwargs: Any
        Keyword arguments.

    Raises
    ------
    UnexpectedKeywordArgument
        If an unexpected keyword argument is provided.
    """
    if kwargs:
        if "meshing_mode" in kwargs:
            raise UnexpectedKeywordArgument(
                "Use 'launch_fluent(mode='meshing')' to launch Fluent in meshing mode."
            )
        else:
            raise UnexpectedKeywordArgument(
                f"launch_fluent() got an unexpected keyword argument {next(iter(kwargs))}"
            )
