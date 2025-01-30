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

"""Provides a module for the API upgrade advisor."""

import os
from typing import TypeVar

from ansys.fluent.core.services.app_utilities import AppUtilities
from ansys.fluent.core.utils.fluent_version import FluentVersion

_TApiUpgradeAdvisor = TypeVar("_TApiUpgradeAdvisor", bound="ApiUpgradeAdvisor")


class ApiUpgradeAdvisor:
    """API upgrade advisor."""

    def __init__(
        self,
        app_utilities: AppUtilities,
        version: str,
        mode: str,
    ) -> None:
        """Initialize ApiUpgradeAdvisor."""
        self._app_utilities = app_utilities
        self._version = version
        self._mode = mode
        self._id = None

    def _can_advise(self) -> bool:
        return (
            not os.getenv("PYFLUENT_SKIP_API_UPGRADE_ADVICE")
            and FluentVersion(self._version) >= FluentVersion.v231
            and self._mode == "solver"
        )

    def __enter__(self) -> _TApiUpgradeAdvisor:
        if self._can_advise():
            self._id = self._app_utilities.start_python_journal()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if self._can_advise():
            journal_str = (self._app_utilities.stop_python_journal(self._id)).strip()
            if (
                journal_str.startswith("solver.")
                and not journal_str.startswith("solver.tui")
                and not journal_str.startswith("solver.execute_tui")
            ):
                print(
                    "The following solver settings object method could also be used to execute the above command:"
                )
                print(f"<solver_session>.{journal_str[len('solver.'):]}")
