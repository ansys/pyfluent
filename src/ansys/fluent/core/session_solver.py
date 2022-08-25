"""Module containing class encapsulating Fluent connection."""

import importlib

from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session import _CODEGEN_MSG_TUI, _BaseSession
from ansys.fluent.core.solver.flobject import get_root as settings_get_root
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath
from ansys.fluent.core.utils.logging import LOG


class Solver(_BaseSession):
    """Encapsulates a Fluent - Solver session connection.
    Solver(Session) holds the top-level objects
    for solver TUI and settings objects calls."""

    def __init__(
        self,
        fluent_connection,
    ):
        super(Solver, self).__init__(fluent_connection=fluent_connection)
        self._tui_service = self.fluent_connection.datamodel_service_tui
        self._settings_service = self.fluent_connection.settings_service
        self._tui = None
        self._settings_root = None
        self._version = None

    @property
    def version(self):
        if self._version is None:
            self._version = get_version_for_filepath(session=self)
        return self._version

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            try:
                tui_module = importlib.import_module(
                    f"ansys.fluent.core.solver.tui_{self.version}"
                )
                self._tui = tui_module.main_menu([], self._tui_service)
            except ImportError:
                LOG.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenuGeneric([], self._tui_service)
        return self._tui

    @property
    def _root(self):
        """root settings object."""
        if self._settings_root is None:
            self._settings_root = settings_get_root(
                flproxy=self._settings_service, version=self.version
            )
        return self._settings_root

    @property
    def file(self):
        """file settings."""
        return self._root.file

    @property
    def mesh(self):
        """mesh settings."""
        return self._root.mesh

    @property
    def setup(self):
        """setup settings."""
        return self._root.setup

    @property
    def solution(self):
        """solution settings."""
        return self._root.solution

    @property
    def results(self):
        """results settings."""
        return self._root.results

    @property
    def parametric_studies(self):
        """parametric_studies settings."""
        return self._root.parametric_studies

    @property
    def current_parametric_study(self):
        """current_parametric_study settings."""
        return self._root.current_parametric_study

    @property
    def parallel(self):
        """parallel settings."""
        return self._root.parallel

    @property
    def report(self):
        """report settings."""
        return self._root.report
