"""2D Meshing workflow module."""

from typing import Union

from ..session_meshing import Meshing
from ..session_pure_meshing import PureMeshing
from .meshing_workflow import TwoDimensionalMeshingWorkflow


def two_dim_workflow(
    session: Union[Meshing, PureMeshing]
) -> TwoDimensionalMeshingWorkflow:
    """Meshing workflow wrapper, initialized as 2D Meshing.

    Parameters
    ----------
    session: Union[Meshing, PureMeshing]
        Meshing session object.

    Returns
    -------
    TwoDimensionalMeshingWorkflow
        2D meshing workflow wrapper.
    """
    return session.two_dimensional_meshing()
