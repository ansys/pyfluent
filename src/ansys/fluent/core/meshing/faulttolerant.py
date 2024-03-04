"""Fault-tolerant workflow module."""

from typing import Union

from ..session_meshing import Meshing
from ..session_pure_meshing import PureMeshing
from .meshing_workflow import FaultTolerantMeshingWorkflow


def fault_tolerant_workflow(
    session: Union[Meshing, PureMeshing]
) -> FaultTolerantMeshingWorkflow:
    """Meshing workflow wrapper, initialized as fault-tolerant.

    Parameters
    ----------
    session: Union[Meshing, PureMeshing]
        Meshing session object.

    Returns
    -------
    FaultTolerantMeshingWorkflow
        Fault-tolerant meshing workflow wrapper.
    """
    return session.fault_tolerant()
