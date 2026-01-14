# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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
import os

from ansys.fluent.core._types import PathType
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.meshing.meshing_workflow import name_to_identifier_map
from ansys.fluent.core.pyfluent_warnings import PyFluentUserWarning
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
        self._meshing_workflow = None
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

    @property
    def meshing_workflow(self):
        """Full API to meshing and meshing_workflow."""
        if self._meshing_workflow is None:
            self._meshing_workflow = _make_datamodel_module(self, "meshing_workflow")
        return self._meshing_workflow

    def _fallback_check(self, legacy: bool | None):
        """Determine whether to use legacy workflow implementation.

        This method handles backward compatibility by automatically selecting the
        appropriate workflow implementation based on Fluent version and user preference.

        Parameters
        ----------
        legacy : bool or None
            User's preference for legacy mode:
            - None: Auto-detect based on Fluent version
            - True: Force legacy mode
            - False: Force new mode (with version check)

        Returns
        -------
        bool
            True to use legacy implementation, False to use new implementation.

        Notes
        -----
        **Version compatibility:**

        - Fluent < 26R1: Only legacy mode available (auto-fallback)
        - Fluent >= 26R1: New mode available (recommended)

        **Behavior by parameter value:**

        - ``legacy=None``: Auto-select based on version
        - Returns True for Fluent < 26R1
        - Returns False for Fluent >= 26R1

        - ``legacy=False``: Request new mode
        - Returns False for Fluent >= 26R1 (as requested)
        - Returns True for Fluent < 26R1 (fallback with warning)

        - ``legacy=True``: Force legacy mode
        - Returns True regardless of version
        """
        fluent_version = self.get_fluent_version()
        is_legacy_only = fluent_version < FluentVersion.v261

        # Case 1: Auto-detect based on version
        if legacy is None:
            return is_legacy_only

        # Case 2: User explicitly requests new mode
        if legacy is False:
            if is_legacy_only:
                # Fluent version doesn't support new mode - warn and fallback
                PyFluentUserWarning(
                    "Non-legacy workflow mode is only available from Fluent 26R1 onwards. "
                    "Falling back to legacy mode."
                )
                return True
            # New mode is available
            return False

        # Case 3: User explicitly requests legacy mode (legacy=True)
        return True

    def watertight_workflow(self, initialize: bool = True, legacy: bool | None = None):
        """Create a watertight meshing workflow."""
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import WorkflowMode
        self._current_workflow = WorkflowMode.WATERTIGHT_MESHING_MODE.value(
            _make_datamodel_module(self, root_module),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def fault_tolerant_workflow(
        self, initialize: bool = True, legacy: bool | None = None
    ):
        """Create a fault-tolerant meshing workflow."""
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import WorkflowMode
        self._current_workflow = WorkflowMode.FAULT_TOLERANT_MESHING_MODE.value(
            _make_datamodel_module(self, root_module),
            self.meshing,
            self.PartManagement,
            self.PMFileManagement,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def two_dimensional_meshing_workflow(
        self, initialize: bool = True, legacy: bool | None = None
    ):
        """Create a 2D meshing workflow."""
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import WorkflowMode
        self._current_workflow = WorkflowMode.TWO_DIMENSIONAL_MESHING_MODE.value(
            _make_datamodel_module(self, root_module),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def topology_based_meshing_workflow(
        self, initialize: bool = True, legacy: bool | None = None
    ):
        """Create a topology-based workflow (beta)."""
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import WorkflowMode

        self._current_workflow = WorkflowMode.TOPOLOGY_BASED_MESHING_MODE.value(
            _make_datamodel_module(self, root_module),
            self.meshing,
            self.get_fluent_version(),
            initialize,
        )
        return self._current_workflow

    def load_workflow(
        self,
        file_path: PathType = None,
        initialize: bool = True,
        legacy: bool | None = None,
    ):
        """Load a previously saved meshing workflow from file.

        Restores workflow configuration including tasks, settings, and state.
        """
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import LoadWorkflow

            self._current_workflow = LoadWorkflow(
                _make_datamodel_module(self, root_module),
                self.meshing,
                os.fspath(file_path),
                self.get_fluent_version(),
            )
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import LoadWorkflow

            self._current_workflow = LoadWorkflow(
                _make_datamodel_module(self, root_module),
                self.meshing,
                self.get_fluent_version(),
                os.fspath(file_path),
                initialize,
            )
        return self._current_workflow

    def create_workflow(self, initialize: bool = True, legacy: bool | None = None):
        """Create a new blank meshing workflow for manual task configuration.

        Provides an empty workflow to build custom task sequences from scratch.
        """
        legacy = self._fallback_check(legacy)
        if legacy:
            root_module = "workflow"
            from ansys.fluent.core.meshing.meshing_workflow import CreateWorkflow
        else:
            root_module = "meshing_workflow"
            from ansys.fluent.core.meshing.meshing_workflow_new import CreateWorkflow

        self._current_workflow = CreateWorkflow(
            _make_datamodel_module(self, root_module),
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

    def current_workflow(self, legacy: bool | None = None):
        """Get the currently active meshing workflow.

        Returns the workflow instance that is currently loaded in the session.

        Raises
        ------
        RuntimeError
            If no workflow is initialized.
        """
        legacy = self._fallback_check(legacy)
        if legacy:
            if self._check_workflow_type(
                "Watertight Geometry"
            ) and self._check_workflow_type("Fault-tolerant Meshing"):
                raise RuntimeError("No workflow initialized.")
            elif self._check_workflow_type("Watertight Geometry"):
                return self._get_current_workflow(
                    "Watertight Geometry"
                ) or self.watertight_workflow(initialize=False, legacy=True)
            elif self._check_workflow_type("Fault-tolerant Meshing"):
                return self._get_current_workflow(
                    "Fault-tolerant Meshing"
                ) or self.fault_tolerant_workflow(initialize=False, legacy=True)
            elif self._check_workflow_type("2D Meshing"):
                return self._get_current_workflow(
                    "2D Meshing"
                ) or self.two_dimensional_meshing_workflow(
                    initialize=False, legacy=True
                )
            elif self._check_workflow_type("Topology Based Meshing"):
                return self._get_current_workflow(
                    "Topology Based Meshing"
                ) or self.topology_based_meshing_workflow(initialize=False, legacy=True)
            else:
                return self.create_workflow(initialize=False, legacy=True)
        else:
            meshing_workflow = _make_datamodel_module(self, "meshing_workflow")
            if meshing_workflow.general.workflow.workflow_type() in [
                "Select Workflow Type",
                None,
            ]:
                raise RuntimeError("No workflow initialized.")
            elif (
                meshing_workflow.general.workflow.workflow_type()
                == "Watertight Geometry"
            ):
                return self._get_current_workflow(
                    "Watertight Geometry"
                ) or self.watertight_workflow(initialize=False)
            elif (
                meshing_workflow.general.workflow.workflow_type()
                == "Fault-tolerant Meshing"
            ):
                return self._get_current_workflow(
                    "Fault-tolerant Meshing"
                ) or self.fault_tolerant_workflow(initialize=False)
            elif meshing_workflow.general.workflow.workflow_type() == "2D Meshing":
                return self._get_current_workflow(
                    "2D Meshing"
                ) or self.two_dimensional_meshing_workflow(initialize=False)
            elif (
                meshing_workflow.general.workflow.workflow_type()
                == "Topology Based Meshing"
            ):
                return self._get_current_workflow(
                    "Topology Based Meshing"
                ) or self.topology_based_meshing_workflow(initialize=False)
            elif meshing_workflow.general.workflow.workflow_type() == "Create New":
                if self._current_workflow.__class__.__name__ == "CreateWorkflow":
                    return self._current_workflow
                return self.create_workflow(initialize=False)
            else:
                if self._current_workflow.__class__.__name__ == "LoadWorkflow":
                    return self._current_workflow
                return self.load_workflow(initialize=False)

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
