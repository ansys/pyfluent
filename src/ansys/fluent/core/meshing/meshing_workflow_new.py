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

"""Meshing workflow specialization of the Workflow module that wraps and extends the
core functionality."""

from __future__ import annotations

from enum import Enum
import os

from ansys.fluent.core._types import PathType
from ansys.fluent.core.services.datamodel_se import PyMenu
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_shared import _make_datamodel_module
from ansys.fluent.core.workflow_new import Workflow


def _get_base_meshing(session) -> "BaseMeshing":
    """Extract a ``BaseMeshing`` instance from a session object.

    Parameters
    ----------
    session : PureMeshing | Meshing
        A meshing session or its internal ``BaseMeshing`` helper.

    Returns
    -------
    BaseMeshing
        The underlying ``BaseMeshing`` instance.

    Raises
    ------
    TypeError
        If *session* is not a recognised meshing session type.
    """
    from ansys.fluent.core.session_base_meshing import BaseMeshing

    if isinstance(session, BaseMeshing):
        return session

    # PureMeshing / Meshing expose _base_meshing
    base = getattr(session, "_base_meshing", None)
    if base is not None and isinstance(base, BaseMeshing):
        return base

    raise TypeError(
        f"Expected a PureMeshing, Meshing, or BaseMeshing instance, "
        f"got {type(session).__name__}."
    )


class MeshingWorkflow(Workflow):
    """Provides meshing specialization of the workflow wrapper that extends the core
    functionality in an object-oriented manner.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    name : str
        Workflow name used to initialise the workflow
        (e.g. ``"Watertight Geometry"``).
    initialize : bool, optional
        If ``True`` (default), the workflow is initialised immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> wf = MeshingWorkflow(session=meshing, name="Watertight Geometry")
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        name: str,
        initialize: bool = True,
    ) -> None:
        base = _get_base_meshing(session)
        workflow_root = _make_datamodel_module(base, "meshing_workflow")
        meshing_root = base.meshing
        fluent_version = base.get_fluent_version()

        super().__init__(
            workflow=workflow_root,
            command_source=meshing_root,
            fluent_version=fluent_version,
        )
        self._meshing = meshing_root
        self._base_meshing = base
        self._name = name
        if initialize:
            self._new_workflow(name=self._name)
        self._initialized = True
        base._current_workflow = self


class WatertightMeshingWorkflow(MeshingWorkflow):
    """Watertight meshing workflow.

    Initialises the *Watertight Geometry* guided workflow on the connected
    Fluent meshing session.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    initialize : bool, optional
        If ``True`` (default), the workflow is initialised immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> watertight = WatertightMeshing(session=meshing)
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        initialize: bool = True,
    ) -> None:
        super().__init__(
            session=session,
            name="Watertight Geometry",
            initialize=initialize,
        )


class FaultTolerantMeshingWorkflow(MeshingWorkflow):
    """Fault-tolerant meshing workflow.

    Initialises the *Fault-tolerant Meshing* guided workflow on the connected
    Fluent meshing session.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    initialize : bool, optional
        If ``True`` (default), the workflow is initialised immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> fault_tolerant = FaultTolerantMeshing(session=meshing)
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        initialize: bool = True,
    ) -> None:
        base = _get_base_meshing(session)
        super().__init__(
            session=base,
            name="Fault-tolerant Meshing",
            initialize=initialize,
        )
        self._parent_workflow = self._workflow
        self._part_management = base.PartManagement
        self._pm_file_management = base.PMFileManagement

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
    """2-D meshing workflow.

    Initialises the *2D Meshing* guided workflow on the connected Fluent
    meshing session.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    initialize : bool, optional
        If ``True`` (default), the workflow is initialised immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> two_d = TwoDimensionalMeshing(session=meshing)
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        initialize: bool = True,
    ) -> None:
        super().__init__(
            session=session,
            name="2D Meshing",
            initialize=initialize,
        )


class TopologyBasedMeshingWorkflow(MeshingWorkflow):
    """Topology-based meshing workflow.

    Initialises the *Topology Based Meshing* guided workflow on the connected
    Fluent meshing session.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    initialize : bool, optional
        If ``True`` (default), the workflow is initialised immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> topo = TopologyBasedMeshing(session=meshing)
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        initialize: bool = True,
    ) -> None:
        super().__init__(
            session=session,
            name="Topology Based Meshing",
            initialize=initialize,
        )


class WorkflowMode(Enum):
    """Provides an enum of supported Fluent meshing workflow modes."""

    WATERTIGHT_MESHING_MODE = WatertightMeshingWorkflow
    FAULT_TOLERANT_MESHING_MODE = FaultTolerantMeshingWorkflow
    TWO_DIMENSIONAL_MESHING_MODE = TwoDimensionalMeshingWorkflow
    TOPOLOGY_BASED_MESHING_MODE = TopologyBasedMeshingWorkflow


class LoadWorkflow(Workflow):
    """Load a previously saved meshing workflow from a file.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    file_path : str or PathType, optional
        Path to the saved workflow file.
    initialize : bool, optional
        If ``True`` (default), the workflow is loaded immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> loaded = LoadWorkflow(session=meshing, file_path="my_workflow.wft")
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        file_path: PathType = None,
        initialize: bool = True,
    ) -> None:
        base = _get_base_meshing(session)
        workflow_root = _make_datamodel_module(base, "meshing_workflow")
        meshing_root = base.meshing
        fluent_version = base.get_fluent_version()

        super().__init__(
            workflow=workflow_root,
            command_source=meshing_root,
            fluent_version=fluent_version,
        )
        self._meshing = meshing_root
        self._base_meshing = base
        self._name = "Load Workflow"
        if initialize:
            self._load_workflow(file_path=os.fspath(file_path))
        base._current_workflow = self


class CreateWorkflow(Workflow):
    """Create a new blank meshing workflow for manual task configuration.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session from which the workflow is constructed.
    initialize : bool, optional
        If ``True`` (default), an empty workflow is created immediately.

    Examples
    --------
    >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
    >>> blank = CreateWorkflow(session=meshing)
    """

    def __init__(
        self,
        session: "PureMeshing | Meshing ",
        initialize: bool = True,
    ) -> None:
        base = _get_base_meshing(session)
        workflow_root = _make_datamodel_module(base, "meshing_workflow")
        meshing_root = base.meshing
        fluent_version = base.get_fluent_version()

        super().__init__(
            workflow=workflow_root,
            command_source=meshing_root,
            fluent_version=fluent_version,
        )
        self._meshing = meshing_root
        self._base_meshing = base
        self._name = "Create New"
        if initialize:
            self._create_workflow()
        base._current_workflow = self


# ---------------------------------------------------------------------------
# Public aliases – short, user-facing names
# ---------------------------------------------------------------------------
WatertightMeshing = WatertightMeshingWorkflow
"""Alias for :class:`WatertightMeshingWorkflow`."""

FaultTolerantMeshing = FaultTolerantMeshingWorkflow
"""Alias for :class:`FaultTolerantMeshingWorkflow`."""

TwoDimensionalMeshing = TwoDimensionalMeshingWorkflow
"""Alias for :class:`TwoDimensionalMeshingWorkflow`."""

TopologyBasedMeshing = TopologyBasedMeshingWorkflow
"""Alias for :class:`TopologyBasedMeshingWorkflow`."""


def _get_current_workflow(current_workflow, name: str):
    if current_workflow and getattr(current_workflow, "_name", None) == name:
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
        raise RuntimeError("No workflow initialized.")

    # Handle loaded workflows (not in the factory map)
    if workflow_type not in workflow_factories:
        # This is a loaded workflow
        if current_workflow and current_workflow.__class__.__name__ == "LoadWorkflow":
            return current_workflow
        return load_workflow_handle(initialize=False)

    # Get or create workflow based on type
    factory = workflow_factories[workflow_type]
    return _get_current_workflow(current_workflow, workflow_type) or factory(
        initialize=False
    )
