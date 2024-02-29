"""Watertight workflow module."""

from .meshing_workflow import EnhancedMeshingWorkflow


def watertight_workflow(geometry_file_name, **launch_args) -> EnhancedMeshingWorkflow:
    """Meshing workflow wrapper, initialized as watertight.

    Parameters
    ----------
    geometry_file_name : str
        The path of a valid geometry file to import. Can be unset.
    launch_args
        Additional arguments forwarded to the launch_fluent function.

    Returns
    -------
    WatertightMeshingWorkflow
        Watertight meshing workflow wrapper.
    """
    watertight = EnhancedMeshingWorkflow.pyfluent_launch_code(
        is_ftm=False, **launch_args
    )
    if geometry_file_name:
        import_geometry = watertight.import_geometry
        import_geometry.file_name = geometry_file_name
        import_geometry()
    return watertight
