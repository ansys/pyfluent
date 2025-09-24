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

"""Module containing class encapsulating Fluent connection."""

import functools
from typing import TYPE_CHECKING, Any, Dict, cast

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.streaming_services.events_streaming import MeshingEvent
from ansys.fluent.core.utils.data_transfer import transfer_case
from ansys.fluent.core.utils.fluent_version import FluentVersion

if TYPE_CHECKING:
    from ansys.fluent.core.generated.datamodel_252.meshing import Root as meshing_root
    from ansys.fluent.core.generated.datamodel_252.meshing_utilities import (
        Root as meshing_utilities_root,
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


class PureMeshing(BaseSession):
    """Encapsulates a Fluent meshing session.

    A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. No ``switch_to_solver`` method is available
    in this mode.
    """

    _rules = [
        "workflow",
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
        launcher_args: Dict[str, Any] | None = None,
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
        super(PureMeshing, self).__init__(
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
        return cast("main_menu", self._base_meshing.tui)

    @property
    def meshing(self) -> "meshing_root":
        """Datamodel root of meshing."""
        return cast("meshing_root", self._base_meshing.meshing)

    @property
    def meshing_utilities(self) -> "meshing_utilities_root | None":
        """Datamodel root of meshing_utilities."""
        if self.get_fluent_version() >= FluentVersion.v242:
            return cast("meshing_utilities_root", self._base_meshing.meshing_utilities)
        return None

    @property
    def workflow(self) -> "workflow_root":
        """Datamodel root of workflow."""
        return cast("workflow_root", self._base_meshing.workflow)

    def watertight(self):
        """Get a new watertight workflow."""
        return self._base_meshing.watertight_workflow()

    def fault_tolerant(self):
        """Get a new fault-tolerant workflow."""
        return self._base_meshing.fault_tolerant_workflow()

    def two_dimensional_meshing(self):
        """Get a new 2D meshing workflow."""
        return self._base_meshing.two_dimensional_meshing_workflow()

    def load_workflow(self, file_path: str):
        """Load a saved workflow."""
        return self._base_meshing.load_workflow(file_path=file_path)

    def create_workflow(self):
        """Create a meshing workflow."""
        return self._base_meshing.create_workflow()

    @property
    def current_workflow(self):
        """Current meshing workflow."""
        return self._base_meshing.current_workflow

    def topology_based(self):
        """Get a new topology-based meshing workflow.

        Raises
        ------
        AttributeError
            If beta features are not enabled in Fluent.
        """
        if not self._is_beta_enabled:
            raise BetaFeaturesNotEnabled("Topology-based meshing")
        return self._base_meshing.topology_based_meshing_workflow()

    @property
    def PartManagement(self) -> "partmanagement_root":
        """Datamodel root of PartManagement."""
        return cast("partmanagement_root", self._base_meshing.PartManagement)

    @property
    def PMFileManagement(self) -> "pmfilemanagement_root":
        """Datamodel root of PMFileManagement."""
        return cast("pmfilemanagement_root", self._base_meshing.PMFileManagement)

    @property
    def preferences(self) -> "preferences_root":
        """Datamodel root of preferences."""
        return cast("preferences_root", self._base_meshing.preferences)

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
