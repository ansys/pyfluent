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

"""Provides a module for the API upgrade advisor."""

from typing import TypeVar

from ansys.fluent.core.utils.fluent_version import FluentVersion

_TApiUpgradeAdvisor = TypeVar("_TApiUpgradeAdvisor", bound="ApiUpgradeAdvisor")


class ApiUpgradeAdvisor:
    """API upgrade advisor."""

    def __init__(
        self,
        application_runtime_service,
        scheme_interpreter_service,
        version: str,
        mode: str,
    ) -> None:
        """Initialize ApiUpgradeAdvisor."""
        self._app_utilities = application_runtime_service
        self._scheme_interpreter = scheme_interpreter_service
        self._version = version
        self._mode = mode
        self._id = None

    def _can_advise(self) -> bool:
        from ansys.fluent.core.module_config import config

        return not config.skip_api_upgrade_advice and self._mode == "solver"

    @staticmethod
    def _start_python_journal(
        scheme_eval_service, journal_name: str | None = None
    ) -> str | None:
        """Start python journal - scheme based implementation."""
        if journal_name:
            scheme_eval_service.exec([f'(api-start-python-journal "{journal_name}")'])
        else:
            scheme_eval_service.eval(
                "(define pyfluent-journal-str-port (open-output-string))"
            )
            scheme_eval_service.eval("(api-echo-python-port pyfluent-journal-str-port)")
            return "1"

    @staticmethod
    def _stop_python_journal(scheme_eval_service, journal_id: str | None = None) -> str:
        """Stop python journal - scheme based implementation."""
        if journal_id:
            scheme_eval_service.eval(
                "(api-unecho-python-port pyfluent-journal-str-port)"
            )
            journal_str = scheme_eval_service.eval(
                "(close-output-port pyfluent-journal-str-port)"
            )
            return journal_str
        else:
            scheme_eval_service.exec(["(api-stop-python-journal)"])
            return ""

    def __enter__(self) -> _TApiUpgradeAdvisor:
        if self._can_advise():
            if FluentVersion(self._version) >= FluentVersion.v252:
                self._id = self._app_utilities.start_python_journal()
            else:
                self._id = self._start_python_journal(self._scheme_interpreter)

        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if self._can_advise():
            if FluentVersion(self._version) >= FluentVersion.v252:
                journal_str = (
                    self._app_utilities.stop_python_journal(self._id)
                ).strip()
            else:
                journal_str = (
                    self._stop_python_journal(self._scheme_interpreter, self._id)
                ).strip()
            if (
                journal_str.startswith("solver.")
                and not journal_str.startswith("solver.tui")
                and not journal_str.startswith("solver.execute_tui")
            ):
                print(
                    "The following solver settings object method could also be used to execute the above command:"
                )
                print(f"<solver_session>.{journal_str[len('solver.'):]}")
