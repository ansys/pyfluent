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

"""Meshing module for managing Fluent meshing workflows."""

import warnings

from ansys.fluent.core.exceptions import PyFluentUserWarning
from ansys.fluent.core.session import Meshing, PureMeshing
from ansys.fluent.core.session.meshing import BaseMeshing
from ansys.fluent.core.utils.fluent_version import FluentVersion


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


def _fallback_check(session: PureMeshing | Meshing, legacy: bool | None) -> bool:
    """Determine whether to use the legacy PyFluent-native interface.

    This method handles backward compatibility by automatically selecting the
    appropriate workflow implementation based on Fluent version and user preference.

    Parameters
    ----------
    legacy : bool or None
        User's preference for legacy behavior:
        - None: Auto-detect based on Fluent version
        - True: Force the legacy PyFluent-native interface
        - False: Force the PyFluent-native interface (with version check)

    Returns
    -------
    bool
        True to use the legacy PyFluent-native interface, False to use the PyFluent-native interface.

    Notes
    -----
    **Version compatibility:**

    - Fluent < 26R1: Only the legacy PyFluent-native interface is available (auto-fallback)
    - Fluent >= 26R1: The PyFluent-native interface is available (recommended)

    **Behavior by parameter value:**

    - ``legacy=None``: Auto-select based on version
    - Returns True for Fluent < 26R1
    - Returns False for Fluent >= 26R1

    - ``legacy=False``: Request the PyFluent-native interface
    - Returns False for Fluent >= 26R1 (as requested)
    - Returns True for Fluent < 26R1 (fallback to legacy PyFluent-native interface with warning)

    - ``legacy=True``: Force the legacy PyFluent-native interface
    - Returns True regardless of version
    """
    fluent_version = session.get_fluent_version()
    only_legacy_allowed = fluent_version < FluentVersion.v261

    # Case 1: Auto-detect based on version
    if legacy is None:
        return only_legacy_allowed

    # Case 2: User explicitly requests the PyFluent-native interface
    if legacy is False:
        if only_legacy_allowed:
            # Fluent version doesn't support the PyFluent-native interface - warn and fallback
            warnings.warn(
                "The PyFluent-native interface is only available from Fluent 26R1 onwards. "
                "Falling back to the legacy PyFluent-native interface.",
                PyFluentUserWarning,
            )
            return True
        # PyFluent-native interface is available
        return False

    # Case 3: User explicitly requests the legacy PyFluent-native interface (legacy=True)
    return True


class WatertightMeshing:
    """Provides watertight meshing specialization of the workflow wrapper.

    See the :ref:`Watertight geometry workflow example
    <ref_watertight_meshing_workflow_example>` for a sample usage example.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    initialize : bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize WatertightMeshing.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize : bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import WorkflowMode
        else:
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        return WorkflowMode.WATERTIGHT_MESHING_MODE.value(
            session=session,
            initialize=initialize,
        )


class FaultTolerantMeshing:
    """Provides fault tolerant meshing specialization of the workflow wrapper.

    See the :ref:`Fault-tolerant workflow example
    <ref_fault_tolerant_meshing_workflow_example>` for a sample usage example.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    initialize: bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize FaultTolerantMeshing.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import WorkflowMode
        else:
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        return WorkflowMode.FAULT_TOLERANT_MESHING_MODE.value(
            session=session,
            initialize=initialize,
        )


class TwoDimensionalMeshing:
    """Provides 2D meshing specialization of the workflow wrapper.

    See the :ref:`2D workflow example
    <ref_two_dimensional_meshing_workflow_example>` for a sample usage example.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    initialize: bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize TwoDimensionalMeshing.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import WorkflowMode
        else:
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        return WorkflowMode.TWO_DIMENSIONAL_MESHING_MODE.value(
            session=session,
            initialize=initialize,
        )


class TopologyBasedMeshing:
    """Provides topology based meshing specialization of the workflow wrapper.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    initialize: bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize TopologyBasedMeshing.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import WorkflowMode
        else:
            from ansys.fluent.core.meshing.meshing_workflow import WorkflowMode
        return WorkflowMode.TOPOLOGY_BASED_MESHING_MODE.value(
            session=session,
            initialize=initialize,
        )


class CreateMeshingWorkflow:
    """Provides a specialization of the workflow wrapper for a newly created workflow.

    See the :ref:`create workflow example <ref_create_meshing_workflow_example>`
    for a sample usage example.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    initialize: bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        initialize: bool = True,
    ) -> None:
        """Initialize CreateMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        initialize: bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import CreatedWorkflow
        else:
            from ansys.fluent.core.meshing.meshing_workflow import CreatedWorkflow
        return CreatedWorkflow(
            session=session,
            initialize=initialize,
        )


class LoadMeshingWorkflow:
    """Provides a specialization of the workflow wrapper for a loaded workflow.

    See the :ref:`load workflow example <ref_load_meshing_workflow_example>` for
    a sample usage example.

    Parameters
    ----------
    session : PureMeshing | Meshing
        The meshing session.
    file_path : str
        The path to the saved workflow file.
    initialize: bool, optional
        Flag to initialize the workflow, defaults to True.
        Set this to False if you are connecting to an existing meshing session which
        has been initialized and want to avoid re-initializing the workflow.
    """

    def __new__(
        cls,
        session: PureMeshing | Meshing,
        file_path: str,
        initialize: bool = True,
    ) -> None:
        """Initialize LoadMeshingWorkflow.

        Parameters
        ----------
        session : PureMeshing | Meshing
            The meshing session.
        file_path : str
            The path to the saved workflow file.
        initialize: bool, optional
            Flag to initialize the workflow, defaults to True.
            Set this to False if you are connecting to an existing meshing session which
            has been initialized and want to avoid re-initializing the workflow.
        """
        _validate_meshing_session(session)
        legacy = _fallback_check(session, session._legacy)
        if legacy:
            from ansys.fluent.core.meshing.meshing_workflow_old import LoadedWorkflow
        else:
            from ansys.fluent.core.meshing.meshing_workflow import LoadedWorkflow
        return LoadedWorkflow(
            session=session,
            file_path=file_path,
            initialize=initialize,
        )


__all__ = [
    "WatertightMeshing",
    "FaultTolerantMeshing",
    "TwoDimensionalMeshing",
    "TopologyBasedMeshing",
    "CreateMeshingWorkflow",
    "LoadMeshingWorkflow",
]
