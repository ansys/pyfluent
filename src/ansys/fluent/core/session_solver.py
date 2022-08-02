"""Module containing class encapsulating Fluent connection."""
import grpc

from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session import _CODEGEN_MSG_TUI, Session, parse_server_info_file
from ansys.fluent.core.solver.flobject import get_root as settings_get_root
from ansys.fluent.core.utils.logging import LOG


class Solver(Session):
    """Encapsulates a Fluent - Solver session connection.
    Solver(Session) which holds the top-level objects
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
    ):
        super().__init__(
            ip=ip,
            port=port,
            password=password,
            channel=channel,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
            remote_instance=remote_instance,
        )
        self._tui_service = self._datamodel_service_tui
        self._settings_service = self._settings_service
        self._tui = None
        self._settings_root = None

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_filepath: str,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
    ) -> "Solver":
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
        solver_session = Solver(
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
            LOG.warning("The settings API is currently experimental.")
            self._settings_root = settings_get_root(flproxy=self._settings_service)
        return self._settings_root

    def exit(self) -> None:
        if self._channel_str:
            self._finalizer()
