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
from typing import TYPE_CHECKING, cast
import warnings

from ansys.fluent.core._types import PathType
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.pyfluent_warnings import PyFluentUserWarning
from ansys.fluent.core.session_shared import (
    _make_datamodel_module,
    _make_tui_module,
)
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

if TYPE_CHECKING:
    from ansys.fluent.core import workflow as _workflow
    from ansys.fluent.core import workflow_new
    from ansys.fluent.core.generated.datamodel_252.meshing import Root as meshing_root
    from ansys.fluent.core.generated.datamodel_252.meshing_utilities import (
        Root as meshing_utilities_root,
    )
    from ansys.fluent.core.generated.datamodel_252.meshing_workflow import (
        Root as meshing_workflow_root,
    )
    from ansys.fluent.core.generated.datamodel_252.part_management import (
        Root as partmanagement_root,
    )
    from ansys.fluent.core.generated.datamodel_252.pm_file_management import (
        Root as pmfilemanagement_root,
    )
    from ansys.fluent.core.generated.datamodel_252.preferences import (
        Root as preferences_root,
    )
    from ansys.fluent.core.generated.datamodel_252.workflow import Root as workflow_root
    from ansys.fluent.core.generated.meshing.tui_252 import main_menu
    from ansys.fluent.core.meshing import (
        meshing_workflow_new,
    )
    from ansys.fluent.core.meshing import meshing_workflow as _meshing_workflow


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
    def tui(self) -> "main_menu":
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            self._tui = _make_tui_module(self, "meshing")

        return cast("main_menu", self._tui)

    @property
    def meshing(self) -> "meshing_root":
        """Meshing object."""
        if self._meshing is None:
            self._meshing = _make_datamodel_module(self, "meshing")
        return cast("meshing_root", self._meshing)

    @property
    def _meshing_utilities_root(self) -> "meshing_utilities_root":
        """Datamodel root of meshing_utilities."""
        return cast(
            "meshing_utilities_root", _make_datamodel_module(self, "MeshingUtilities")
        )

    @property
    def meshing_utilities(self) -> "meshing_utilities_root":
        """A wrapper over the Fluent's meshing queries."""
        if self._meshing_utilities is None:
            self._meshing_utilities = self._meshing_utilities_root
        return self._meshing_utilities

    @property
    def workflow(self) -> "workflow_root":
        """Datamodel root of workflow."""
        if self._old_workflow is None:
            self._old_workflow = cast(
                "workflow_root", _make_datamodel_module(self, "workflow")
            )
        return self._old_workflow

    @property
    def meshing_workflow(self) -> "meshing_workflow_root":
        """Full API to meshing and meshing_workflow."""
        if self._meshing_workflow is None:
            self._meshing_workflow = cast(
                "meshing_workflow_root",
                _make_datamodel_module(self, "meshing_workflow"),
            )
        return self._meshing_workflow

    def _fallback_check(self, legacy: bool | None) -> bool:
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
        only_legacy_allowed = fluent_version < FluentVersion.v261

        # Case 1: Auto-detect based on version
        if legacy is None:
            return only_legacy_allowed

        # Case 2: User explicitly requests new mode
        if legacy is False:
            if only_legacy_allowed:
                # Fluent version doesn't support new mode - warn and fallback
                warnings.warn(
                    "Non-legacy workflow mode is only available from Fluent 26R1 onwards. "
                    "Falling back to legacy mode.",
                    PyFluentUserWarning,
                )
                return True
            # New mode is available
            return False

        # Case 3: User explicitly requests legacy mode (legacy=True)
        return True

    def watertight_workflow(
        self, initialize: bool = True, legacy: bool | None = None
    ) -> "_meshing_workflow.WatertightMeshingWorkflow | meshing_workflow_new.WatertightMeshingWorkflow":
        """Create a watertight meshing workflow.

        Parameters
        ----------
        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
        """
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
    ) -> "_meshing_workflow.FaultTolerantMeshingWorkflow | meshing_workflow_new.FaultTolerantMeshingWorkflow":
        """Create a fault-tolerant meshing workflow.

        Parameters
        ----------
        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
        """
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
    ) -> "_meshing_workflow.TwoDimensionalMeshingWorkflow | meshing_workflow_new.TwoDimensionalMeshingWorkflow":
        """Create a 2D meshing workflow.

        Parameters
        ----------
        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
        """
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
    ) -> "_meshing_workflow.TopologyBasedMeshingWorkflow | meshing_workflow_new.TopologyBasedMeshingWorkflow":
        """Create a topology-based workflow (beta).

        Parameters
        ----------
        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
        """
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
    ) -> "_meshing_workflow.LoadWorkflow | meshing_workflow_new.LoadWorkflow":
        """Load a previously saved meshing workflow from file.

        Restores workflow configuration including tasks, settings, and state.

        Parameters
        ----------
        file_path : str or PathType
            Path to the saved workflow file (typically with .wft extension).

        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
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

    def create_workflow(
        self, initialize: bool = True, legacy: bool | None = None
    ) -> "_meshing_workflow.CreateWorkflow | meshing_workflow_new.CreateWorkflow":
        """Create a new blank meshing workflow for manual task configuration.

        Provides an empty workflow to build custom task sequences from scratch.

        Parameters
        ----------
        initialize: bool, optional
            If True (default), initializes the workflow with default settings and
            prepares it for immediate use. If False, creates the workflow without
            initialization, useful when loading a saved state or applying custom
            configuration before starting.

        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).
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

    def current_workflow(
        self, legacy: bool | None = None
    ) -> "_workflow.Workflow | workflow_new.Workflow":
        """Get the currently active meshing workflow.

        Returns the workflow instance that is currently loaded in the session.

        Parameters
        ----------
        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Raises
        ------
        RuntimeError
            If no workflow is initialized.
        """
        legacy = self._fallback_check(legacy)

        # Define workflow type to factory method mapping
        workflow_factories = {
            "Watertight Geometry": self.watertight_workflow,
            "Fault-tolerant Meshing": self.fault_tolerant_workflow,
            "2D Meshing": self.two_dimensional_meshing_workflow,
            "Topology Based Meshing": self.topology_based_meshing_workflow,
            "Create New": self.create_workflow,
        }

        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow import get_current_workflow

            return get_current_workflow(
                meshing_root=self.meshing,
                current_workflow=self._current_workflow,
                workflow_factories=workflow_factories,
            )

        else:
            from ansys.fluent.core.meshing.meshing_workflow_new import (
                get_current_workflow,
            )

            return get_current_workflow(
                workflow_root=_make_datamodel_module(self, "meshing_workflow"),
                current_workflow=self._current_workflow,
                workflow_factories=workflow_factories,
                load_workflow_handle=self.load_workflow,
            )

    @property
    def PartManagement(self) -> "partmanagement_root":
        """Datamodel root of ``PartManagement``."""
        if self._part_management is None:
            self._part_management = cast(
                "partmanagement_root", _make_datamodel_module(self, "PartManagement")
            )
        return self._part_management

    @property
    def PMFileManagement(self) -> "pmfilemanagement_root":
        """Datamodel root of PMFileManagement."""
        if self._pm_file_management is None:
            self._pm_file_management = cast(
                "pmfilemanagement_root",
                _make_datamodel_module(self, "PMFileManagement"),
            )
        return self._pm_file_management

    @property
    def preferences(self) -> "preferences_root":
        """Datamodel root of preferences."""
        if self._preferences is None:
            self._preferences = cast(
                "preferences_root", _make_datamodel_module(self, "preferences")
            )
        return self._preferences
