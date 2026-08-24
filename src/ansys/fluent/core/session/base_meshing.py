# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Internal base class for all meshing sessions.

This module is private.  Do not import from it directly; use
:class:`~ansys.fluent.core.session.pure_meshing.PureMeshing` or
:class:`~ansys.fluent.core.session.meshing.Meshing` instead.

Both leaf classes are lightweight and add no further public API beyond what
is defined here.  ``PureMeshing`` targets deployments where meshing and
solving run as separate processes; ``Meshing`` additionally exposes
:meth:`~ansys.fluent.core.session.meshing.Meshing.switch_to_solver`.
"""

import functools
import logging
import os
from typing import TYPE_CHECKING, Any, cast
import warnings

from ansys.fluent.core._types import PathType
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.module_config import config
from ansys.fluent.core.pyfluent_warnings import PyFluentUserWarning
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.session._shared import (
    _make_datamodel_module,
    _make_tui_module,
)
from ansys.fluent.core.session.session import BaseSession
from ansys.fluent.core.streaming_services.events_streaming import MeshingEvent
from ansys.fluent.core.utils.data_transfer import transfer_case
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

if TYPE_CHECKING:
    from ansys.fluent.core import workflow as _workflow
    from ansys.fluent.core import workflow_new
    from ansys.fluent.core.generated.datamodel_261.meshing import Root as meshing_root
    from ansys.fluent.core.generated.datamodel_261.meshing_utilities import (
        Root as meshing_utilities_root,
    )
    from ansys.fluent.core.generated.datamodel_261.meshing_workflow import (
        Root as meshing_workflow_root,
    )
    from ansys.fluent.core.generated.datamodel_261.part_management import (
        Root as partmanagement_root,
    )
    from ansys.fluent.core.generated.datamodel_261.pm_file_management import (
        Root as pmfilemanagement_root,
    )
    from ansys.fluent.core.generated.datamodel_261.preferences import (
        Root as preferences_root,
    )
    from ansys.fluent.core.generated.datamodel_261.workflow import Root as workflow_root
    from ansys.fluent.core.generated.meshing.tui_261 import main_menu
    from ansys.fluent.core.meshing import (
        meshing_workflow_new,
    )
    from ansys.fluent.core.meshing import meshing_workflow as _meshing_workflow


pyfluent_logger = logging.getLogger("pyfluent.general")
datamodel_logger = logging.getLogger("pyfluent.datamodel")


class BaseMeshing(BaseSession):
    """Base class providing the full public API for all meshing sessions.

    Both :class:`~ansys.fluent.core.session.pure_meshing.PureMeshing` and
    :class:`~ansys.fluent.core.session.meshing.Meshing` inherit from this
    class and add no further public methods.
    """

    _rules = [
        "workflow",
        "meshing_workflow",
        "meshing",
        "MeshingUtilities",
        "PartManagement",
        "PMFileManagement",
    ]

    def __new__(cls, *args, **kwargs):
        if cls is BaseMeshing:
            raise TypeError(
                "BaseMeshing cannot be instantiated directly. "
                "Use Meshing or PureMeshing."
            )
        return super().__new__(cls)

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeInterpreter,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: dict[str, Any] | None = None,
    ):
        """BaseMeshing session.

        Parameters
        ----------
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        scheme_eval: SchemeInterpreter
            Instance of ``SchemeInterpreter`` to execute Fluent's scheme code on.
        file_transfer_service : Optional
            Service for uploading and downloading files.
        start_transcript : bool, optional
            Whether to start the Fluent transcript in the client.
            The default is ``True``, in which case the Fluent
            transcript can be subsequently started and stopped
            using method calls on the ``Session`` object.
        """
        super().__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
            event_type=MeshingEvent,
        )
        # Aliases required by _shared.py
        self._tui_service = self._datamodel_service_tui
        self._se_service = self._datamodel_service_se
        self._tui = None
        self._meshing = None
        self._meshing_utilities = None
        self._old_workflow = None
        self._meshing_workflow = None
        self._part_management = None
        self._pm_file_management = None
        self._preferences = None
        self._product_version = None
        self._current_workflow = None

        self.datamodel_streams = {}
        if self._datamodel_service_se._cache is not None:
            for rules in BaseMeshing._rules:
                self._datamodel_service_se._cache.set_config(
                    rules,
                    "name_key",
                    (
                        NameKey.DISPLAY
                        if DataModelCache.use_display_name
                        else NameKey.INTERNAL
                    ),
                )
                stream = fluent_connection._service_factory.object_model_streaming
                stream.register_callback(
                    functools.partial(
                        self._datamodel_service_se._cache.update_cache,
                        rules=rules,
                        version=self._datamodel_service_se._version,
                    )
                )
                self.datamodel_streams[rules] = stream
                stream.start(
                    rules=rules,
                    no_commands_diff_state=config.datamodel_use_nocommands_diff_state,
                )
                self._fluent_connection.register_finalizer_cb(stream.stop)

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

    def _watertight_workflow(
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

    def _fault_tolerant_workflow(
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

    def _two_dimensional_meshing_workflow(
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

    def _topology_based_meshing_workflow(
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
        file_path: PathType,
        legacy: bool | None = None,
        initialize: bool = True,
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
        self, legacy: bool | None = None, initialize: bool = True
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

    def _get_current_workflow(
        self, legacy: bool | None = None
    ) -> "_workflow.Workflow | workflow_new.Workflow":
        """Return the active workflow; called by the current_workflow property."""
        legacy = self._fallback_check(legacy)

        # Define workflow type to factory method mapping
        workflow_factories = {
            "Watertight Geometry": self._watertight_workflow,
            "Fault-tolerant Meshing": self._fault_tolerant_workflow,
            "2D Meshing": self._two_dimensional_meshing_workflow,
            "Topology Based Meshing": self._topology_based_meshing_workflow,
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

    def watertight(
        self, legacy: bool | None = None
    ) -> "_meshing_workflow.WatertightMeshingWorkflow | meshing_workflow_new.WatertightMeshingWorkflow":
        """Get a new watertight meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), auto-selects based on Fluent version: legacy for
            versions up to 25R2, new implementation from 26R1 onwards.

        Returns
        -------
        WatertightMeshingWorkflow
        """
        return self._watertight_workflow(legacy=legacy)

    def fault_tolerant(
        self, legacy: bool | None = None
    ) -> "_meshing_workflow.FaultTolerantMeshingWorkflow | meshing_workflow_new.FaultTolerantMeshingWorkflow":
        """Get a new fault-tolerant meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), auto-selects based on Fluent version: legacy for
            versions up to 25R2, new implementation from 26R1 onwards.

        Returns
        -------
        FaultTolerantMeshingWorkflow
        """
        return self._fault_tolerant_workflow(legacy=legacy)

    def two_dimensional_meshing(
        self, legacy: bool | None = None
    ) -> "_meshing_workflow.TwoDimensionalMeshingWorkflow | meshing_workflow_new.TwoDimensionalMeshingWorkflow":
        """Get a new 2D meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), auto-selects based on Fluent version: legacy for
            versions up to 25R2, new implementation from 26R1 onwards.

        Returns
        -------
        TwoDimensionalMeshingWorkflow
        """
        return self._two_dimensional_meshing_workflow(legacy=legacy)

    def topology_based(self, legacy: bool | None = None):
        """Get a new topology-based meshing workflow (beta feature).

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), auto-selects based on Fluent version: legacy for
            versions up to 25R2, new implementation from 26R1 onwards.

        Raises
        ------
        BetaFeaturesNotEnabled
            If beta features are not enabled in the Fluent session.
        """
        if not self._is_beta_enabled:
            raise BetaFeaturesNotEnabled("Topology-based meshing")
        return self._topology_based_meshing_workflow(legacy=legacy)

    @property
    def current_workflow(self):
        """Get the currently active meshing workflow."""
        return self._get_current_workflow()

    @property
    def legacy_current_workflow(self):
        """Get the currently active meshing workflow using the legacy implementation."""
        return self._get_current_workflow(legacy=True)

    def transfer_mesh_to_solvers(
        self,
        solvers,
        file_type: str = "case",
        file_name_stem: str | None = None,
        num_files_to_try: int = 1,
        clean_up_mesh_file: bool = True,
        overwrite_previous: bool = True,
    ):
        """Transfer mesh to Fluent solver instances.

        Parameters
        ----------
        solvers : iterable
            Sequence of solver instances.
        file_type : str, optional
            ``"case"`` or ``"mesh"``.  Default is ``"case"``.
        file_name_stem : str, optional
            Stem for the generated file name.
        num_files_to_try : int, optional
            Number of candidate file names to try.  Default is ``1``.
        clean_up_mesh_file : bool, optional
            Remove the mesh file after transfer.  Default is ``True``.
        overwrite_previous : bool, optional
            Overwrite an existing file with the same name.  Default is ``True``.
        """
        transfer_case(
            self,
            solvers,
            file_type,
            file_name_stem,
            num_files_to_try,
            clean_up_mesh_file,
            overwrite_previous,
        )
