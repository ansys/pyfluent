"""Watertight workflow module."""

from typing import Optional, Union

from ..session_meshing import Meshing
from ..session_pure_meshing import PureMeshing
from .meshing_workflow import WatertightMeshingWorkflow


def watertight_workflow(
    session: Union[Meshing, PureMeshing], geometry_file_name: Optional[str] = None
) -> WatertightMeshingWorkflow:
    """Meshing workflow wrapper, initialized as watertight.

    Parameters
    ----------
    session: Union[Meshing, PureMeshing]
        Meshing session object.
    geometry_file_name : Optional[str]
        The path of a valid geometry file to import. Can be unset.

    Returns
    -------
    WatertightMeshingWorkflow
        Watertight meshing workflow wrapper.
    """
    watertight = session.watertight()
    if geometry_file_name:
        import_geometry = watertight.import_geometry
        import_geometry.file_name = geometry_file_name
        import_geometry()
    return watertight
