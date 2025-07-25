# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module to get base Meshing session."""

import logging

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.meshing.meshing_workflow import (
    CreateWorkflow,
    LoadWorkflow,
    WorkflowMode,
    name_to_identifier_map,
)
from ansys.fluent.core.session_shared import (
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
        if self.get_fluent_version() >= FluentVersion.v242:
            return _make_datamodel_module(self, "MeshingUtilities")

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
