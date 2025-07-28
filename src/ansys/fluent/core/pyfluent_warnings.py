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

"""Provides a module to get warnings for core functionality."""

import warnings


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


def warning_for_fluent_dev_version(version):
    """Provides warning if Fluent develop branch is used."""
    from ansys.fluent.core import FluentVersion, config

    if FluentVersion(version) > FluentVersion(config.fluent_release_version):
        warnings.warn(
            "⚠️ Warning: You are using PyFluent with an unreleased or development version of Fluent.\n"
            "Compatibility is not guaranteed, and unexpected behavior may occur. Please use a released "
            "version of Fluent that is officially supported by this version of PyFluent.",
            FluentDevVersionWarning,
        )


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
