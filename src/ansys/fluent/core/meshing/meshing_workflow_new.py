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

from ansys.fluent.core._types import PathType
from ansys.fluent.core.services.object_model import PyMenu
from ansys.fluent.core.session import Meshing, PureMeshing
from ansys.fluent.core.session._shared import _make_datamodel_module
from ansys.fluent.core.session.meshing import BaseMeshing
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.workflow_new import Workflow


def _validate_meshing_session(session: BaseMeshing) -> bool:
    """Check if the session is a meshing session.

    Parameters
    ----------
    session : BaseMeshing
        The session to check.

    Returns
    -------
    bool
        True if the session is a meshing session, False otherwise.

    Raises
    ------
    TypeError
        If the session is not an instance of BaseMeshing.
    """
    if not isinstance(session, BaseMeshing):
        raise TypeError(
            f"Expected a BaseMeshing session, got {type(session).__name__} instead."
        )
    return True


class MeshingWorkflow(Workflow):
    """Provides meshing specialization of the workflow wrapper that extends the core
    functionality in an object-oriented manner."""

    def __init__(
        self,
        session: BaseMeshing,
        workflow_type: str,
        initialize: bool = True,
    ) -> None:
        """Initialize MeshingWorkflow.

        Parameters
        ----------
        session : BaseMeshing
            The meshing session.
        workflow_type: str
            Workflow type to initialize it.
        initialize: bool
            Flag to initialize the workflow, defaults to True.
        """
        _validate_meshing_session(session)
        self._meshing = session.meshing
        super().__init__(
            workflow=_make_datamodel_module(session, "meshing_workflow"),
            command_source=self._meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._name = workflow_type
        if initialize:
            self._new_workflow(name=self._name)
        self._initialized = True


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
            initialize=initialize,
        )
        self._parent_workflow = _make_datamodel_module(session, "meshing_workflow")
        self._part_management = session.PartManagement
        self._pm_file_management = session.PMFileManagement

    @property
    def parts(self) -> PyMenu | None:
        """Access part-management in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            Part-management.
        """
        return self._parent_workflow.parts

    @property
    def parts_files(self):
        """Access the part-management file-management object in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            File management object in the part management object.
        """
        return self._parent_workflow.parts_files

    @property
    def part_management(self) -> PyMenu | None:
        """Access part-management in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            Part-management.
        """
        # TODO: Remove this after migrating to the new workflow
        return self._part_management

    @property
    def pm_file_management(self) -> PyMenu | None:
        """Access the part-management file-management object in fault-tolerant mode.

        Returns
        -------
        PyMenu | None
            File management object in the part management object.
        """
        # TODO: Remove this after migrating to the new workflow
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
        _validate_meshing_session(session)
        super().__init__(
            workflow=_make_datamodel_module(session, "meshing_workflow"),
            command_source=session.meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._meshing = session.meshing
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
        _validate_meshing_session(session)
        super().__init__(
            workflow=_make_datamodel_module(session, "meshing_workflow"),
            command_source=session.meshing,
            fluent_version=session.get_fluent_version(),
        )
        self._meshing = session.meshing
        if initialize:
            self._create_workflow()


def _get_current_workflow(current_workflow, name: str):
    if current_workflow and current_workflow._name == name:
        return current_workflow


def get_current_workflow(
    workflow_root, current_workflow, workflow_factories, load_workflow_handle
) -> Workflow:
    """Get the currently active workflow in new mode.

    Parameters
    ----------
    workflow_root : PyMenu
        Root workflow datamodel object.
    current_workflow : Workflow or None
        Currently cached workflow instance.
    workflow_factories : dict
        Mapping of workflow type names to factory functions.
    load_workflow_handle : callable
        Function to load a workflow from file.

    Returns
    -------
    Workflow
        The currently active workflow instance.

    Raises
    ------
    RuntimeError
        If no workflow is initialized.
    """
    # New mode: Check workflow type from meshing_workflow datamodel
    workflow_type = workflow_root.general.workflow.workflow_type()

    # Check if no workflow is initialized
    if workflow_type in ["Select Workflow Type", None]:
        return

    # Handle loaded workflows (not in the factory map)
    if workflow_type not in workflow_factories:
        # This is a loaded workflow
        if current_workflow and current_workflow.__class__.__name__ in [
            "LoadWorkflow",
            "LoadedWorkflow",
        ]:
            return current_workflow
        return load_workflow_handle(initialize=False)

    # Get or create workflow based on type
    factory = workflow_factories[workflow_type]
    return _get_current_workflow(current_workflow, workflow_type) or factory(
        initialize=False
    )


# Public aliases

WatertightMeshing = WatertightMeshingWorkflow
"""Alias for :class:`WatertightMeshingWorkflow`."""

FaultTolerantMeshing = FaultTolerantMeshingWorkflow
"""Alias for :class:`FaultTolerantMeshingWorkflow`."""

TwoDimensionalMeshing = TwoDimensionalMeshingWorkflow
"""Alias for :class:`TwoDimensionalMeshingWorkflow`."""

TopologyBasedMeshing = TopologyBasedMeshingWorkflow
"""Alias for :class:`TopologyBasedMeshingWorkflow`."""

CreateNewWorkflow = CreatedWorkflow
"""Alias for :class:`CreatedWorkflow`."""

LoadExistingWorkflow = LoadedWorkflow
"""Alias for :class:`LoadedWorkflow`."""
