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

"""Meshing workflow specialization of the Workflow module that wraps and extends the
core functionality."""

from __future__ import annotations

from enum import Enum
import os
from typing import TYPE_CHECKING

from ansys.fluent.core._types import PathType
from ansys.fluent.core.services.object_model import PyMenu
from ansys.fluent.core.session import Meshing, PureMeshing
from ansys.fluent.core.session._shared import _make_datamodel_module
from ansys.fluent.core.workflow_old import Workflow

name_to_identifier_map = {
    "Watertight Geometry": "EnableCleanCAD",
    "Fault-tolerant Meshing": "EnableComplexMeshing",
    "2D Meshing": "EnablePrime2dMeshing",
    "Topology Based Meshing": "EnablePrimeMeshing",
}


class MeshingWorkflow(Workflow):
    """Provides meshing specialization of the workflow wrapper that extends the core
    functionality in an object-oriented manner."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        workflow_type: PyMenu,
        identifier: str,
        initialize: bool = True,
    ) -> None:
        """Initialize MeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session object.
        workflow_type : PyMenu
            Type of the workflow.
        identifier : str
            Workflow name to identify it from global settings.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
        """
        self._meshing = session.meshing
        super().__init__(
            workflow=_make_datamodel_module(self, "workflow"),
            command_source=self._meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._name = workflow_type
        self._identifier = identifier
        self._unsubscribe_root_affected_callback()
        if initialize:
            self._new_workflow(name=workflow_type)
        else:
            self._activate_dynamic_interface(dynamic_interface=True)
        self._initialized = True

    if not TYPE_CHECKING:

        def __getattribute__(self, item: str):
            if (
                not item.startswith("_")
                and super().__getattribute__("_initialized")
                and not getattr(self._meshing.GlobalSettings, self._identifier)()
            ):
                raise RuntimeError(
                    f"'{self._name}' objects are inaccessible from other workflows."
                )
            return super().__getattribute__(item)


class WatertightMeshingWorkflow(MeshingWorkflow):
    """Provides watertight meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize WatertightMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        super().__init__(
            session=session,
            workflow_type="Watertight Geometry",
            identifier=name_to_identifier_map["Watertight Geometry"],
            initialize=initialize,
        )


class FaultTolerantMeshingWorkflow(MeshingWorkflow):
    """Provides fault-tolerant meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize FaultTolerantMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        super().__init__(
            session=session,
            workflow_type="Fault-tolerant Meshing",
            identifier=name_to_identifier_map["Fault-tolerant Meshing"],
            initialize=initialize,
        )
        self._part_management = session.PartManagement
        self._pm_file_management = session.PMFileManagement

    @property
    def part_management(self) -> PyMenu | None:
        """Access part-management in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            Part-management.
        """
        return self._part_management

    @property
    def pm_file_management(self) -> PyMenu | None:
        """Access the part-management file-management object in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            File management object in the part management object.
        """
        return self._pm_file_management


class TwoDimensionalMeshingWorkflow(MeshingWorkflow):
    """Provides 2D meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize TwoDimensionalMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            Meshing session object.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        super().__init__(
            session=session,
            workflow_type="2D Meshing",
            identifier=name_to_identifier_map["2D Meshing"],
            initialize=initialize,
        )


class TopologyBasedMeshingWorkflow(MeshingWorkflow):
    """Provides topology-based meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize TopologyBasedMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            Meshing session object.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        super().__init__(
            session=session,
            workflow_type="Topology Based Meshing",
            identifier=name_to_identifier_map["Topology Based Meshing"],
            initialize=initialize,
        )


class WorkflowMode(Enum):
    """Provides an enum of supported Fluent meshing workflow modes."""

    WATERTIGHT_MESHING_MODE = WatertightMeshingWorkflow
    FAULT_TOLERANT_MESHING_MODE = FaultTolerantMeshingWorkflow
    TWO_DIMENSIONAL_MESHING_MODE = TwoDimensionalMeshingWorkflow
    TOPOLOGY_BASED_MESHING_MODE = TopologyBasedMeshingWorkflow


class LoadedWorkflow(Workflow):
    """Provides a specialization of the workflow wrapper for a loaded workflow."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        file_path: PathType = None,
        initialize: bool = True,
    ) -> None:
        """Initialize a ``LoadedWorkflow`` instance.

        Parameters
        ----------
        session : PureMeshing | Meshing
            Meshing session object.
        file_path: os.PathLike[str | bytes] | str | bytes
            Path to the saved workflow file.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        self._meshing = session.meshing
        super().__init__(
            workflow=_make_datamodel_module(self, "workflow"),
            command_source=self._meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._unsubscribe_root_affected_callback()
        if initialize:
            self._load_workflow(file_path=os.fspath(file_path))


class CreatedWorkflow(Workflow):
    """Provides a specialization of the workflow wrapper for a newly created
    workflow."""

    def __init__(
        self,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize a ``CreatedWorkflow`` instance.

        Parameters
        ----------
        session : PureMeshing | Meshing
            Meshing session object.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        self._meshing = session.meshing
        super().__init__(
            workflow=_make_datamodel_module(self, "workflow"),
            command_source=self._meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._unsubscribe_root_affected_callback()
        if initialize:
            self._create_workflow()
        else:
            self._activate_dynamic_interface(dynamic_interface=True)


def _is_workflow_active(meshing_root, name: str):
    return getattr(meshing_root.GlobalSettings, name_to_identifier_map[name])()


def _get_current_workflow(current_workflow, name: str):
    if current_workflow and current_workflow._name == name:
        return current_workflow


def get_current_workflow(
    meshing_root, current_workflow, workflow_factories
) -> Workflow:
    """Get the currently active meshing workflow (legacy mode).

    Determines which workflow type is currently active by checking GlobalSettings
    flags, and returns the appropriate workflow instance. This is the legacy
    implementation.

    Parameters
    ----------
    meshing_root : PyMenu
        Root meshing datamodel object containing GlobalSettings and workflow state.
    current_workflow : Workflow or None
        Currently cached workflow instance (may be None or outdated).
    workflow_factories : dict[str, callable]
        Mapping of workflow type names to factory functions that create workflow instances.

    Returns
    -------
    Workflow
        The currently active workflow instance (either cached or newly created).

    Raises
    ------
    RuntimeError
        If no workflow is initialized (both watertight and fault-tolerant are active).

    """
    if _is_workflow_active(meshing_root, "Watertight Geometry") and _is_workflow_active(
        meshing_root, "Fault-tolerant Meshing"
    ):
        raise RuntimeError("No workflow initialized.")

    # Find active workflow type
    for workflow_name, factory in workflow_factories.items():
        if _is_workflow_active(meshing_root, workflow_name):
            return _get_current_workflow(current_workflow, workflow_name) or factory(
                initialize=False, legacy=True
            )
    # Default to create_workflow if no specific type matches
    return _get_current_workflow(current_workflow, "Create New") or workflow_factories[
        "Create New"
    ](initialize=False, legacy=True)
