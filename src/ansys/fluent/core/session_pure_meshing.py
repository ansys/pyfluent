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

"""Module containing class encapsulating Fluent connection."""

import functools
import os
from typing import TYPE_CHECKING, Any

import ansys.fluent.core as pyfluent
from ansys.fluent.core._types import PathType
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.streaming_services.events_streaming import MeshingEvent
from ansys.fluent.core.utils.data_transfer import transfer_case

if TYPE_CHECKING:
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


class PureMeshing(BaseSession):
    """Encapsulates a Fluent meshing session with a meshing-only Python interface.

    ``PureMeshing`` is designed for workflows where meshing and solving are run as
        separate stages or in different environments, such as modular or containerized
        deployments. It provides a clean API that focuses solely on meshing tasks.

        This interface exposes:

        - ``workflow`` and ``meshing`` objects for task-based meshing operations.
        - ``tui`` for scripting via the legacy Text User Interface (when needed).
    """

    _rules = [
        "workflow",
        "meshing_workflow",
        "meshing",
        "MeshingUtilities",
        "PartManagement",
        "PMFileManagement",
    ]

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: dict[str, Any] | None = None,
    ):
        """PureMeshing session.

        Parameters
        ----------
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        scheme_eval: SchemeEval
            Instance of ``SchemeEval`` to execute Fluent's scheme code on.
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
        self._base_meshing = BaseMeshing(
            self.execute_tui,
            fluent_connection,
            self.get_fluent_version().value,
            self._datamodel_service_tui,
            self._datamodel_service_se,
        )

        datamodel_service_se = self._datamodel_service_se
        self.datamodel_streams = {}
        if datamodel_service_se.cache is not None:
            for rules in PureMeshing._rules:
                datamodel_service_se.cache.set_config(
                    rules,
                    "name_key",
                    (
                        NameKey.DISPLAY
                        if DataModelCache.use_display_name
                        else NameKey.INTERNAL
                    ),
                )
                stream = DatamodelStream(datamodel_service_se)
                stream.register_callback(
                    functools.partial(
                        datamodel_service_se.cache.update_cache,
                        rules=rules,
                        version=datamodel_service_se.version,
                    )
                )
                self.datamodel_streams[rules] = stream
                stream.start(
                    rules=rules,
                    no_commands_diff_state=pyfluent.config.datamodel_use_nocommands_diff_state,
                )
                self._fluent_connection.register_finalizer_cb(stream.stop)

    @property
    def tui(self) -> "main_menu":
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        return self._base_meshing.tui

    @property
    def meshing(self) -> "meshing_root":
        """Datamodel root of meshing."""
        return self._base_meshing.meshing

    @property
    def meshing_utilities(self) -> "meshing_utilities_root | None":
        """Datamodel root of meshing_utilities."""
        return self._base_meshing.meshing_utilities

    @property
    def workflow(self) -> "workflow_root":
        """Datamodel root of workflow."""
        return self._base_meshing.workflow

    @property
    def meshing_workflow(self):
        """Full API to meshing and meshing_workflow."""
        return self._base_meshing.meshing_workflow

    def watertight(
        self, legacy: bool | None = None
    ) -> (
        _meshing_workflow.WatertightMeshingWorkflow
        | meshing_workflow_new.WatertightMeshingWorkflow
    ):
        """Get a new watertight meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            A new watertight workflow instance ready for configuration and execution.
        """
        return self._base_meshing.watertight_workflow(legacy=legacy)

    def fault_tolerant(self, legacy: bool | None = None):
        """Get a new fault-tolerant meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            A new fault-tolerant workflow instance ready for configuration and execution.
        """
        return self._base_meshing.fault_tolerant_workflow(legacy=legacy)

    def two_dimensional_meshing(self, legacy: bool | None = None):
        """Get a new 2D meshing workflow.

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            A new 2D meshing workflow instance ready for configuration and execution.
        """
        return self._base_meshing.two_dimensional_meshing_workflow(legacy=legacy)

    def load_workflow(self, file_path: PathType, legacy: bool | None = None):
        """Load a saved meshing workflow from a file.

        Restores a previously saved workflow configuration, including all task
        settings, sizing controls, and intermediate state. This allows resuming
        work or reusing established workflows on new geometry.

        Parameters
        ----------
        file_path : str or PathType
            Path to the saved workflow file (typically with .wft extension).
        legacy : bool, optional
            If True, loads as a legacy workflow implementation.
            If False, loads as a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            The loaded workflow instance with all saved state restored.
        """
        return self._base_meshing.load_workflow(
            file_path=os.fspath(file_path), legacy=legacy
        )

    def create_workflow(self, legacy: bool | None = None):
        """Create a new blank meshing workflow.

        Initializes an empty workflow that can be manually configured with tasks.
        Unlike predefined workflows (watertight, fault-tolerant), this gives you
        full control to build a custom task sequence from scratch.

        Parameters
        ----------
        legacy : bool, optional
            If True, creates a legacy workflow implementation.
            If False, creates a new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            A new empty workflow instance ready for task insertion.
        """
        return self._base_meshing.create_workflow(legacy=legacy)

    @property
    def current_workflow(self):
        """Get the current active meshing workflow.

        Returns the workflow instance that is currently loaded and active in the
        meshing session. This is the workflow you're actively working on, whether
        it was created from scratch, loaded from a file, or initiated as a
        predefined workflow type.

        Returns
        -------
        Workflow
            The currently active workflow instance, or None if no workflow is loaded.
        """
        return self._base_meshing.current_workflow()

    @property
    def legacy_current_workflow(self):
        """Get the current active meshing workflow (legacy implementation).

        Returns the legacy implementation of the currently active workflow. This
        is provided for backward compatibility with code written for Fluent 25R2
        and earlier versions.
        """
        return self._base_meshing.current_workflow(legacy=True)

    def topology_based(self, legacy: bool | None = None):
        """Get a new topology-based meshing workflow (beta feature).

        Parameters
        ----------
        legacy : bool, optional
            If True, returns the legacy workflow implementation.
            If False, returns the new workflow implementation.
            If None (default), uses the legacy workflow implementation for Fluent versions up to 25R2
            and uses the new workflow implementation for later versions (since 26R1).

        Returns
        -------
        Workflow
            A new topology-based workflow instance ready for configuration and execution.

        Raises
        ------
        BetaFeaturesNotEnabled
            If beta features are not enabled in the Fluent session. Enable by launching
            Fluent with the ``-beta`` flag or setting the appropriate environment variable.
        """
        if not self._is_beta_enabled:
            raise BetaFeaturesNotEnabled("Topology-based meshing")
        return self._base_meshing.topology_based_meshing_workflow(legacy=legacy)

    @property
    def PartManagement(self) -> "partmanagement_root":
        """Datamodel root of PartManagement."""
        return self._base_meshing.PartManagement

    @property
    def PMFileManagement(self) -> "pmfilemanagement_root":
        """Datamodel root of PMFileManagement."""
        return self._base_meshing.PMFileManagement

    @property
    def preferences(self) -> "preferences_root":
        """Datamodel root of preferences."""
        return self._base_meshing.preferences

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
            Sequence of solver instances
        file_type : str, default "case"
            "case" or "mesh"
        file_name_stem : str
            Optional file name stem
        num_files_to_try : int, default 1
            Optional number of files to try to write,
            each with a different generated name.
            Defaults to 1
        clean_up_mesh_file: bool, default True
            Whether to remove the file at the end
        overwrite_previous: bool, default True
            Whether to overwrite the file if it already exists
        Returns
        -------
        None
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
