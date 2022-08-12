"""Module containing class encapsulating Fluent connection."""
import grpc

from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver


class Meshing(PureMeshing):
    """Encapsulates a Fluent - Meshing session connection.
    Meshing(PureMeshing) holds the top-level objects
    for meshing TUI and various meshing datamodel API calls."""

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

        self.solver_switch = False

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        return super().tui

    @property
    def meshing(self):
        """meshing datamodel root."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        return super().meshing

    @property
    def workflow(self):
        """workflow datamodel root."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        return super().workflow

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        return super().PartManagement

    @property
    def PMFileManagement(self):
        """PMFileManagement datamodel root."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        return super().PMFileManagement

    def switch_to_solver(self):
        """A switch to move to the solver session from meshing."""
        if self.solver_switch:
            raise AttributeError(
                "Mesh-Session-specific attributes are not available in Solver-Session"
            )
        self.tui.switch_to_solution_mode("yes")
        self.solver_switch = True
        solver_session = Solver(fluent_connection=self.fluent_connection)
        return solver_session
