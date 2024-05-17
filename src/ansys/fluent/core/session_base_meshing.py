"""Provides a module to get base Meshing session."""

import logging

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.meshing.meshing_workflow import (
    CreateWorkflow,
    LoadWorkflow,
    WorkflowMode,
)
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenu
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI
from ansys.fluent.core.utils import load_module
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

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
        self._fluent_version = fluent_version
        self._meshing_utilities = None
        self._old_workflow = None
        self._wt_workflow = None
        self._ft_workflow = None
        self._2dm_workflow = None
        self._tb_workflow = None
        self._loaded_workflow = None
        self._created_workflow = None
        self._part_management = None
        self._pm_file_management = None
        self._preferences = None
        self._session_execute_tui = session_execute_tui
        self._product_version = None

    def get_fluent_version(self) -> FluentVersion:
        """Gets and returns the fluent version."""
        pyfluent_logger.debug("Fluent version = " + str(self._fluent_version))
        return FluentVersion(self._fluent_version)

    @property
    def _version(self):
        """Fluent's product version."""
        if self._product_version is None:
            self._product_version = get_version_for_file_name(session=self)
        return self._product_version

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            try:
                from ansys.fluent.core import CODEGEN_OUTDIR

                tui_module = load_module(
                    f"meshing_tui_{self._version}",
                    CODEGEN_OUTDIR / "meshing" / f"tui_{self._version}.py",
                )
                self._tui = tui_module.main_menu(
                    self._tui_service, self._version, "meshing", []
                )
            except ImportError:
                tui_logger.warning(_CODEGEN_MSG_TUI)
                self._tui = TUIMenu(self._tui_service, self._version, "meshing", [])
        return self._tui

    @property
    def _meshing_root(self):
        """Datamodel root of meshing."""
        try:
            from ansys.fluent.core import CODEGEN_OUTDIR

            meshing_module = load_module(
                f"meshing_{self._version}",
                CODEGEN_OUTDIR / f"datamodel_{self._version}" / "meshing.py",
            )
            meshing_root = meshing_module.Root(self._se_service, "meshing", [])
        except ImportError:
            datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
            meshing_root = PyMenuGeneric(self._se_service, "meshing")
        return meshing_root

    @property
    def meshing(self):
        """Meshing object."""
        if self._meshing is None:
            self._meshing = self._meshing_root
        return self._meshing

    @property
    def _meshing_utilities_root(self):
        """Datamodel root of meshing_utilities."""
        try:
            if self.get_fluent_version() >= FluentVersion.v242:
                from ansys.fluent.core import CODEGEN_OUTDIR

                meshing_utilities_module = load_module(
                    f"MeshingUtilities_{self._version}",
                    CODEGEN_OUTDIR
                    / f"datamodel_{self._version}"
                    / "MeshingUtilities.py",
                )
                meshing_utilities_root = meshing_utilities_module.Root(
                    self._se_service, "MeshingUtilities", []
                )
        except ImportError:
            datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
            if self.get_fluent_version() >= FluentVersion.v242:
                meshing_utilities_root = PyMenuGeneric(
                    self._se_service, "meshing_utilities"
                )
        return meshing_utilities_root

    @property
    def meshing_utilities(self):
        """A wrapper over the Fluent's meshing queries."""
        if self._meshing_utilities is None:
            self._meshing_utilities = self._meshing_utilities_root
        return self._meshing_utilities

    @property
    def _workflow_se(self):
        """Datamodel root of workflow."""
        try:
            from ansys.fluent.core import CODEGEN_OUTDIR

            workflow_module = load_module(
                f"workflow_{self._version}",
                CODEGEN_OUTDIR / f"datamodel_{self._version}" / "workflow.py",
            )
            workflow_se = workflow_module.Root(self._se_service, "workflow", [])
        except ImportError:
            datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
            workflow_se = PyMenuGeneric(self._se_service, "workflow")
        return workflow_se

    @property
    def workflow(self):
        """Datamodel root of workflow."""
        if not self._old_workflow:
            self._old_workflow = WorkflowMode.CLASSIC_MESHING_MODE.value(
                self._workflow_se,
                self.meshing,
                self.get_fluent_version(),
            )
        return self._old_workflow

    @property
    def watertight_workflow(self):
        """Datamodel root of workflow exposed in object-oriented manner."""
        if not self._wt_workflow:
            self._wt_workflow = WorkflowMode.WATERTIGHT_MESHING_MODE.value(
                self._workflow_se,
                self.meshing,
                self.get_fluent_version(),
            )
        return self._wt_workflow

    @property
    def fault_tolerant_workflow(self):
        """Datamodel root of workflow exposed in object-oriented manner."""
        if not self._ft_workflow:
            self._ft_workflow = WorkflowMode.FAULT_TOLERANT_MESHING_MODE.value(
                self._workflow_se,
                self.meshing,
                self.PartManagement,
                self.PMFileManagement,
                self.get_fluent_version(),
            )
        return self._ft_workflow

    @property
    def two_dimensional_meshing_workflow(self):
        """Data model root of the workflow exposed in an object-oriented manner."""
        if not self._2dm_workflow:
            self._2dm_workflow = WorkflowMode.TWO_DIMENSIONAL_MESHING_MODE.value(
                self._workflow_se,
                self.meshing,
                self.get_fluent_version(),
            )
        return self._2dm_workflow

    @property
    def topology_based_meshing_workflow(self):
        """Datamodel root of workflow exposed in object-oriented manner."""
        if not self._tb_workflow:
            self._tb_workflow = WorkflowMode.TOPOLOGY_BASED_MESHING_MODE.value(
                self._workflow_se,
                self.meshing,
                self.get_fluent_version(),
            )
        return self._tb_workflow

    def load_workflow(self, file_path: str):
        """Datamodel root of workflow exposed in object-oriented manner."""
        if not self._loaded_workflow:
            self._loaded_workflow = LoadWorkflow(
                self._workflow_se,
                self.meshing,
                file_path,
                self.get_fluent_version(),
            )
        return self._loaded_workflow

    @property
    def create_workflow(self):
        """Datamodel root of the workflow exposed in an object-oriented manner."""
        if not self._created_workflow:
            self._created_workflow = CreateWorkflow(
                self._workflow_se,
                self.meshing,
                self.get_fluent_version(),
            )
        return self._created_workflow

    @property
    def PartManagement(self):
        """Datamodel root of ``PartManagement``."""
        if self._part_management is None:
            try:
                from ansys.fluent.core import CODEGEN_OUTDIR

                pm_module = load_module(
                    f"PartManagement_{self._version}",
                    CODEGEN_OUTDIR / f"datamodel_{self._version}" / "PartManagement.py",
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
                from ansys.fluent.core import CODEGEN_OUTDIR

                pmfm_module = load_module(
                    f"PMFileManagement_{self._version}",
                    CODEGEN_OUTDIR
                    / f"datamodel_{self._version}"
                    / "PMFileManagement.py",
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
