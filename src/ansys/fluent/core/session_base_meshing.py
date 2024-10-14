"""Provides a module to get base Meshing session."""

import logging

import ansys.fluent.core as pyfluent
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.meshing.meshing_workflow import (
    CreateWorkflow,
    LoadWorkflow,
    WorkflowMode,
    name_to_identifier_map,
)
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.session_shared import (
    _CODEGEN_MSG_DATAMODEL,
    _make_datamodel_module,
    _make_tui_module,
)
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

pyfluent_logger = logging.getLogger("pyfluent.general")
datamodel_logger = logging.getLogger("pyfluent.datamodel")


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

        Parameters
        ----------
        session_execute_tui (_type_):
            Executes Fluent’s SolverTUI methods.
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        """
        self._tui_service = datamodel_service_tui
        self._se_service = datamodel_service_se
        self._fluent_connection = fluent_connection
        self._tui = None
        self._meshing = None
        self._fluent_version = fluent_version
        self._meshing_utilities = None
        self._old_workflow = None
        self._part_management = None
        self._pm_file_management = None
        self._preferences = None
        self._session_execute_tui = session_execute_tui
        self._product_version = None
        self._current_workflow = None

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
            self._tui = _make_tui_module(self, "meshing")

        return self._tui

    @property
    def meshing(self):
        """Meshing object."""
        if self._meshing is None:
            self._meshing = _make_datamodel_module(self, "meshing")
        return self._meshing

    @property
    def _meshing_utilities_root(self):
        """Datamodel root of meshing_utilities."""
        try:
            if self.get_fluent_version() >= FluentVersion.v242:
                from ansys.fluent.core import CODEGEN_OUTDIR

                meshing_utilities_module = pyfluent.utils.load_module(
                    f"MeshingUtilities_{self._version}",
                    CODEGEN_OUTDIR
                    / f"datamodel_{self._version}"
                    / "MeshingUtilities.py",
                )
                meshing_utilities_root = meshing_utilities_module.Root(
                    self._se_service, "MeshingUtilities", []
                )
        except (ImportError, FileNotFoundError):
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
    def workflow(self):
        """Datamodel root of workflow."""
        if self._old_workflow is None:
            self._old_workflow = _make_datamodel_module(self, "workflow")
        return self._old_workflow

    def watertight_workflow(self, initialize: bool = True):
        """Datamodel root of workflow."""
        self._current_workflow = WorkflowMode.WATERTIGHT_MESHING_MODE.value(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def fault_tolerant_workflow(self, initialize: bool = True):
        """Datamodel root of workflow."""
        self._current_workflow = WorkflowMode.FAULT_TOLERANT_MESHING_MODE.value(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            self.PartManagement,
            self.PMFileManagement,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def two_dimensional_meshing_workflow(self, initialize: bool = True):
        """Data model root of the workflow."""
        self._current_workflow = WorkflowMode.TWO_DIMENSIONAL_MESHING_MODE.value(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def topology_based_meshing_workflow(self, initialize: bool = True):
        """Datamodel root of workflow."""
        self._current_workflow = WorkflowMode.TOPOLOGY_BASED_MESHING_MODE.value(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def load_workflow(self, file_path: str):
        """Datamodel root of workflow."""
        self._current_workflow = LoadWorkflow(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            file_path,
            self.get_fluent_version(),
        )
        return self._current_workflow

    def create_workflow(self, initialize: bool = True):
        """Datamodel root of the workflow."""
        self._current_workflow = CreateWorkflow(
            _make_datamodel_module(self, "workflow"),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def _check_workflow_type(self, name: str):
        return getattr(self.meshing.GlobalSettings, name_to_identifier_map[name])()

    def _get_current_workflow(self, name: str):
        if self._current_workflow and self._current_workflow._name == name:
            return self._current_workflow

    @property
    def current_workflow(self):
        """Datamodel root of the workflow.

        Raises
        ------
        RuntimeError
            If no workflow is initialized.
        """
        if self._check_workflow_type(
            "Watertight Geometry"
        ) and self._check_workflow_type("Fault-tolerant Meshing"):
            raise RuntimeError("No workflow initialized.")
        elif self._check_workflow_type("Watertight Geometry"):
            return self._get_current_workflow(
                "Watertight Geometry"
            ) or self.watertight_workflow(initialize=False)
        elif self._check_workflow_type("Fault-tolerant Meshing"):
            return self._get_current_workflow(
                "Fault-tolerant Meshing"
            ) or self.fault_tolerant_workflow(initialize=False)
        elif self._check_workflow_type("2D Meshing"):
            return self._get_current_workflow(
                "2D Meshing"
            ) or self.two_dimensional_meshing_workflow(initialize=False)
        elif self._check_workflow_type("Topology Based Meshing"):
            return self._get_current_workflow(
                "Topology Based Meshing"
            ) or self.topology_based_meshing_workflow(initialize=False)
        else:
            return self.create_workflow(initialize=False)

    @property
    def PartManagement(self):
        """Datamodel root of ``PartManagement``."""
        if self._part_management is None:
            self._part_management = _make_datamodel_module(self, "PartManagement")
        return self._part_management

    @property
    def PMFileManagement(self):
        """Datamodel root of PMFileManagement."""
        if self._pm_file_management is None:
            self._pm_file_management = _make_datamodel_module(self, "PMFileManagement")
        return self._pm_file_management

    @property
    def preferences(self):
        """Datamodel root of preferences."""
        if self._preferences is None:
            self._preferences = _make_datamodel_module(self, "preferences")
        return self._preferences
