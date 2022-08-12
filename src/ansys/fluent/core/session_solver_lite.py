"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
import grpc

from ansys.fluent.core.session_solver import Solver


class SolverLite(Solver):
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

    # One can inherit methods from 'Solver' and re-define it here to make it unavailable in solver-Lite

    def switch_to_full_solver(self):
        """A switch to move to the full-solver session from solver-lite."""
        solver_session = Solver(fluent_connection=self.fluent_connection)
        return solver_session
