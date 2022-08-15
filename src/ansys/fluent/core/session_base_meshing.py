from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.meshing.workflow import MeshingWorkflow
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI
from ansys.fluent.core.utils.logging import LOG


class _BaseMeshing:

    meshing_attrs = ("tui", "meshing", "workflow", "PartManagement", "PMFileManagement")

    def __init__(self, fluent_connection: _FluentConnection):
        self._tui_service = fluent_connection.datamodel_service_tui
        self._se_service = fluent_connection.datamodel_service_se
        self._tui = None
        self._meshing = None
        self._workflow = None
        self._part_management = None
        self._pm_file_management = None

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
    def _workflow_se(self):
        """workflow datamodel root."""
        try:
            from ansys.fluent.core.datamodel.workflow import Root as workflow_root

            workflow_se = workflow_root(self._se_service, "workflow", [])
        except (ImportError, ModuleNotFoundError):
            LOG.warning(_CODEGEN_MSG_DATAMODEL)
            workflow_se = PyMenuGeneric(self._se_service, "workflow")
        return workflow_se

    @property
    def workflow(self):
        if not self._workflow:
            self._workflow = MeshingWorkflow(self._workflow_se, self.meshing)
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
