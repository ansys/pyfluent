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

"""Meshing-only Fluent session (:class:`PureMeshing`).

Inheritance
-----------
::

    BaseSession (private)
    └── BaseMeshing (private)
        └── PureMeshing          ← this class
            └── Meshing
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansys.fluent.core.meshing import meshing_workflow as _meshing_workflow
    from ansys.fluent.core.meshing import meshing_workflow_new

from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.session._base_meshing import BaseMeshing
from ansys.fluent.core.utils.data_transfer import transfer_case


class PureMeshing(BaseMeshing):
    """Fluent meshing session without solver-switching capability.

    Designed for deployments where meshing and solving run as separate
    processes (e.g. containerised pipelines).  Use
    :class:`~ansys.fluent.core.session.meshing.Meshing` when you also need
    :meth:`~ansys.fluent.core.session.meshing.Meshing.switch_to_solver`.

    Attributes
    ----------
    tui : main_menu
        Root of the Fluent meshing TUI.  Access commands as Python
        attributes, e.g. ``session.tui.mesh.check()``.
    meshing : meshing_root
        Root of the ``meshing`` datamodel.
    meshing_utilities : meshing_utilities_root
        Utility queries on the current mesh state.
    workflow : workflow_root
        Root of the legacy ``workflow`` datamodel.  Prefer the typed
        workflow factory methods below.
    meshing_workflow : meshing_workflow_root
        Root of the new-style ``meshing_workflow`` datamodel (26R1+).
    PartManagement : partmanagement_root
        Root of the ``PartManagement`` datamodel.
    PMFileManagement : pmfilemanagement_root
        Root of the ``PMFileManagement`` datamodel.
    preferences : preferences_root
        Root of the ``preferences`` datamodel.
    scheme : SchemeInterpreter
        Direct access to Fluent's Scheme interpreter.
    journal : Journal
        Fluent journal recorder; call :meth:`~Journal.start` /
        :meth:`~Journal.stop`.
    fields : Fields
        Container for ``field_data`` and ``field_data_streaming``.
    transcript : TranscriptStreaming
        Fluent console transcript; call ``.start()`` / ``.stop()``.
    events : EventsManager
        Subscribe to meshing events (``MeshingEvent``).
    datamodel_streams : dict[str, ObjectModelStreaming]
        Live object-model streaming handles, keyed by rule name.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeInterpreter,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: dict[str, Any] | None = None,
    ):
        """PureMeshing session.

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
        )

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
            A new watertight workflow instance ready for configuration and execution.
        """
        return self.watertight_workflow(legacy=legacy)

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
            A new fault-tolerant workflow instance ready for configuration and execution.
        """
        return self.fault_tolerant_workflow(legacy=legacy)

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
            A new 2D meshing workflow instance ready for configuration and execution.
        """
        return self.two_dimensional_meshing_workflow(legacy=legacy)

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
        return super().current_workflow()

    @property
    def legacy_current_workflow(self):
        """Get the current active meshing workflow (legacy implementation).

        Returns the legacy implementation of the currently active workflow. This
        is provided for backward compatibility with code written for Fluent 25R2
        and earlier versions.
        """
        return super().current_workflow(legacy=True)

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
        return self.topology_based_meshing_workflow(legacy=legacy)

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
