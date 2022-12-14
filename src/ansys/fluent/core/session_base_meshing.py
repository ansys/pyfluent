import importlib

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.meshing.meshing import Meshing
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenu
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath
from ansys.fluent.core.utils.logging import LOG
from ansys.fluent.core.workflow import WorkflowWrapper


class _BaseMeshing:
    def __init__(self, session_execute_tui, fluent_connection: _FluentConnection):
        self._tui_service = fluent_connection.datamodel_service_tui
        self._se_service = fluent_connection.datamodel_service_se
        self._fluent_connection = fluent_connection
        self._tui = None
        self._meshing = None
        self._workflow = None
        self._part_management = None
        self._pm_file_management = None
        self._preferences = None
        self._session_execute_tui = session_execute_tui
        self._version = None

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        return self._fluent_connection.get_fluent_version()

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
                    f"ansys.fluent.core.meshing.tui_{self.version}"
                )
                self._tui = tui_module.main_menu([], self._tui_service)
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenu([], self._tui_service)
        return self._tui

    @property
    def _meshing_root(self):
        """meshing datamodel root."""
        try:
            meshing_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.meshing"
            )
            meshing_root = meshing_module.Root(self._se_service, "meshing", [])
        except (ImportError, ModuleNotFoundError):
            LOG.warning(_CODEGEN_MSG_DATAMODEL)
            meshing_root = PyMenuGeneric(self._se_service, "meshing")
        return meshing_root

    @property
    def meshing(self):
        if self._meshing is None:
            self._meshing = Meshing(
                self._session_execute_tui,
                self._meshing_root,
                self.tui,
                self._fluent_connection,
            )
        return self._meshing

    @property
    def _workflow_se(self):
        """workflow datamodel root."""
        try:
            workflow_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.workflow"
            )
            workflow_se = workflow_module.Root(self._se_service, "workflow", [])
        except (ImportError, ModuleNotFoundError):
            LOG.warning(_CODEGEN_MSG_DATAMODEL)
            workflow_se = PyMenuGeneric(self._se_service, "workflow")
        return workflow_se

    @property
    def workflow(self):
        if not self._workflow:
            self._workflow = WorkflowWrapper(self._workflow_se, self.meshing)
        return self._workflow

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        if self._part_management is None:
            try:
                pm_module = importlib.import_module(
                    f"ansys.fluent.core.datamodel_{self.version}.PartManagement"
                )
                self._part_management = pm_module.Root(
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
                pmfm_module = importlib.import_module(
                    f"ansys.fluent.core.datamodel_{self.version}.PMFileManagement"
                )
                self._pm_file_management = pmfm_module.Root(
                    self._se_service, "PMFileManagement", []
                )
            except (ImportError, ModuleNotFoundError):
                LOG.warning(_CODEGEN_MSG_DATAMODEL)
                self._pm_file_management = PyMenuGeneric(
                    self._se_service, "PMFileManagement"
                )
        return self._pm_file_management

    @property
    def preferences(self):
        """preferences datamodel root."""
        if self._preferences is None:
            from ansys.fluent.core.session import _get_preferences

            self._preferences = _get_preferences(self)
        return self._preferences
