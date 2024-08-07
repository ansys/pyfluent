"""Provides a module for the API upgrade advisor."""

import os
from typing import TypeVar

from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.utils.fluent_version import FluentVersion

_TApiUpgradeAdvisor = TypeVar("_TApiUpgradeAdvisor", bound="ApiUpgradeAdvisor")


class ApiUpgradeAdvisor:
    """API upgrade advisor."""

    def __init__(self, scheme_eval: SchemeEval, version: str, mode: str) -> None:
        self._scheme_eval = scheme_eval.scheme_eval
        self._version = version
        self._mode = mode

    def _can_advise(self) -> bool:
        return (
            not os.getenv("PYFLUENT_SKIP_API_UPGRADE_ADVICE")
            and FluentVersion(self._version) >= FluentVersion.v231
            and self._mode == "solver"
        )

    def __enter__(self) -> _TApiUpgradeAdvisor:
        if self._can_advise():
            self._scheme_eval("(define pyfluent-journal-str-port (open-output-string))")
            self._scheme_eval("(api-echo-python-port pyfluent-journal-str-port)")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if self._can_advise():
            self._scheme_eval("(api-unecho-python-port pyfluent-journal-str-port)")
            journal_str = self._scheme_eval(
                "(close-output-port pyfluent-journal-str-port)"
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
