import importlib
import logging

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.meshing.meshing_workflow import MeshingWorkflow
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenu
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

pyfluent_logger = logging.getLogger("pyfluent.general")
datamodel_logger = logging.getLogger("pyfluent.datamodel")
tui_logger = logging.getLogger("pyfluent.tui")


class BaseMeshing:
    """Encapsulates base methods of a meshing session."""

    def __init__(
        self,
        session_execute_tui,
        fluent_connection: FluentConnection,
        fluent_version,
        datamodel_service_tui,
        datamodel_service_se,
    ):
        """BaseMeshing session.

        Args:
            session_execute_tui (_type_): Executes Fluent’s SolverTUI methods.

            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        self._tui_service = datamodel_service_tui
        self._se_service = datamodel_service_se
        self._fluent_connection = fluent_connection
        self._tui = None
        self._meshing = None
        self._workflow = None
        self._part_management = None
        self._pm_file_management = None
        self._preferences = None
        self._session_execute_tui = session_execute_tui
        self._version = None
        self._fluent_version = fluent_version

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        pyfluent_logger.debug("Fluent version = " + str(self._fluent_version))
        return self._fluent_version

    @property
    def version(self):
        """Fluent's product version."""
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
            except ImportError:
                tui_logger.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenu([], self._tui_service)
        return self._tui

    @property
    def _meshing_root(self):
        """Datamodel root of meshing."""
        try:
            meshing_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.meshing"
            )
            meshing_root = meshing_module.Root(self._se_service, "meshing", [])
        except ImportError:
            datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
            meshing_root = PyMenuGeneric(self._se_service, "meshing")
        return meshing_root

    @property
    def meshing(self):
        if self._meshing is None:
            self._meshing = self._meshing_root
        return self._meshing

    @property
    def _workflow_se(self):
        """Datamodel root of workflow."""
        try:
            workflow_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.workflow"
            )
            workflow_se = workflow_module.Root(self._se_service, "workflow", [])
        except ImportError:
            datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
            workflow_se = PyMenuGeneric(self._se_service, "workflow")
        return workflow_se

    @property
    def workflow(self):
        """Datamodel root of workflow."""
        if not self._workflow:
            self._workflow = MeshingWorkflow(
                self._workflow_se,
                self.meshing,
                self.PartManagement,
                self.PMFileManagement,
            )
        return self._workflow

    @property
    def PartManagement(self):
        """Datamdoel root of PartManagement."""
        if self._part_management is None:
            try:
                pm_module = importlib.import_module(
                    f"ansys.fluent.core.datamodel_{self.version}.PartManagement"
                )
                self._part_management = pm_module.Root(
                    self._se_service, "PartManagement", []
                )
            except ImportError:
                datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
                self._part_management = PyMenuGeneric(
                    self._se_service, "PartManagement"
                )
        return self._part_management

    @property
    def PMFileManagement(self):
        """Datamodel root of PMFileManagement."""
        if self._pm_file_management is None:
            try:
                pmfm_module = importlib.import_module(
                    f"ansys.fluent.core.datamodel_{self.version}.PMFileManagement"
                )
                self._pm_file_management = pmfm_module.Root(
                    self._se_service, "PMFileManagement", []
                )
            except ImportError:
                datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
                self._pm_file_management = PyMenuGeneric(
                    self._se_service, "PMFileManagement"
                )
        return self._pm_file_management

    @property
    def preferences(self):
        """Datamodel root of preferences."""
        if self._preferences is None:
            from ansys.fluent.core.session import _get_preferences

            self._preferences = _get_preferences(self)
        return self._preferences
