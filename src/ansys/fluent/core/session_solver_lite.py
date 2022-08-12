"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
import grpc

from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session import (
    _CODEGEN_MSG_TUI,
    BaseSession,
    parse_server_info_file,
)
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.solver.flobject import get_root as settings_get_root
from ansys.fluent.core.utils.logging import LOG


class SolverLite(BaseSession):
    """Encapsulates a Fluent - Solver(Lite) session connection.
    SolverLite(Session) holds the top-level objects
    for solver TUI and settings objects calls."""

    def __init__(
        self,
        ip: str = None,
        port: int = None,
        password: str = None,
        channel: grpc.Channel = None,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        remote_instance=None,
        fluent_connection=None,
    ):
        super().__init__(
            ip=ip,
            port=port,
            password=password,
            channel=channel,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
            remote_instance=remote_instance,
            fluent_connection=fluent_connection,
        )
        self._tui_service = self.fluent_connection.datamodel_service_tui
        self._settings_service = self.fluent_connection.settings_service
        self._tui = None
        self._settings_root = None

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_filepath: str,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
    ) -> "SolverLite":
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_filepath : str
            Path to server-info file written out by Fluent server
        cleanup_on_exit : bool, optional
            When True, the connected Fluent session will be shut down
            when PyFluent is exited or exit() is called on the session
            instance, by default True.
        start_transcript : bool, optional
            The Fluent transcript is started in the client only when
            start_transcript is True. It can be started and stopped
            subsequently via method calls on the Session object.
            Defaults to true.

        Returns
        -------
        Session
            Session instance
        """
        ip, port, password = parse_server_info_file(server_info_filepath)
        solver_session = SolverLite(
            ip=ip,
            port=port,
            password=password,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
        )
        return solver_session

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            try:
                from ansys.fluent.core.solver.tui import main_menu as SolverMainMenu

                self._tui = SolverMainMenu([], self._tui_service)
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenuGeneric([], self._tui_service)
        return self._tui

    @property
    def root(self):
        """root settings object."""
        if self._settings_root is None:
            self._settings_root = settings_get_root(flproxy=self._settings_service)
        return self._settings_root

    def switch_to_full_solver(self):
        """A switch to move to the full-solver session from solver-lite."""
        solver_session = Solver(fluent_connection=self.fluent_connection)
        return solver_session
