from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI


class BaseMeshing:
    def __init__(
        self, tui_service: DatamodelService_TUI, se_service: DatamodelService_SE
    ):
        self._tui_service = tui_service
        self._se_service = se_service
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
