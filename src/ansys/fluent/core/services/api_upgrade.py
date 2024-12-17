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
