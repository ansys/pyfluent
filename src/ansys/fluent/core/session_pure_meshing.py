"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS MESHING WITHOUT THE SWITCH TO SOLVER***********
"""
import grpc

from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session import _CODEGEN_MSG_TUI, BaseSession, parse_server_info_file
from ansys.fluent.core.utils.logging import LOG

_CODEGEN_MSG_DATAMODEL = (
    "Currently calling the datamodel API in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local datamodel API classes."
)


class PureMeshing(BaseSession):
    """Encapsulates a Fluent - Pure Meshing session connection.
    PureMeshing(Session) which holds the top-level objects
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
        fluent_connection=None
    ):
        super().__init__(
            ip=ip,
            port=port,
            password=password,
            channel=channel,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
            remote_instance=remote_instance,
            fluent_connection=fluent_connection
        )
        self._tui_service = self.fluent_connection._datamodel_service_tui
        self._se_service = self.fluent_connection._datamodel_service_se
        self._tui = None
        self._meshing = None
        self._workflow = None
        self._part_management = None
        self._pm_file_management = None

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_filepath: str,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
    ) -> "PureMeshing":
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
        meshing_session = PureMeshing(
            ip=ip,
            port=port,
            password=password,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
        )
        return meshing_session

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            try:
                from ansys.fluent.core.meshing.tui import main_menu as MeshingMainMenu

                self._tui = MeshingMainMenu([], self._tui_service)
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenuGeneric([], self._tui_service)
        return self._tui

    @property
    def meshing(self):
        """meshing datamodel root."""
        if self._meshing is None:
            try:
                from ansys.fluent.core.datamodel.meshing import Root as meshing_root

                self._meshing = meshing_root(self._se_service, "meshing", [])
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_DATAMODEL)
                self._meshing = PyMenuGeneric(self._se_service, "meshing")
        return self._meshing

    @property
    def workflow(self):
        """workflow datamodel root."""
        if self._workflow is None:
            try:
                from ansys.fluent.core.datamodel.workflow import Root as workflow_root

                self._workflow = workflow_root(self._se_service, "workflow", [])
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_DATAMODEL)
                self._workflow = PyMenuGeneric(self._se_service, "workflow")
        return self._workflow

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        if self._part_management is None:
            try:
                from ansys.fluent.core.datamodel.PartManagement import (
                    Root as PartManagement_root,
                )

                self._part_management = PartManagement_root(
                    self._se_service, "PartManagement", []
                )
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_DATAMODEL)
                self._part_management = PyMenuGeneric(
                    self._se_service, "PartManagement"
                )
        return self._part_management

    @property
    def PMFileManagement(self):
        """PMFileManagement datamodel root."""
        if self._pm_file_management is None:
            try:
                from ansys.fluent.core.datamodel.PMFileManagement import (
                    Root as PMFileManagement_root,
                )

                self._pm_file_management = PMFileManagement_root(
                    self._se_service, "PMFileManagement", []
                )
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_DATAMODEL)
                self._pm_file_management = PyMenuGeneric(
                    self._se_service, "PMFileManagement"
                )
        return self._pm_file_management

    def exit(self) -> None:
        if self._channel_str:
            self._finalizer()
