"""Watertight workflow module."""

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.launcher.launcher_utils import FluentMode

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
    EnhancedMeshingWorkflow
        Meshing workflow wrapper.
    """
    if "dynamic_interface" in launch_args:
        del launch_args["dynamic_interface"]
    if "session" in launch_args:
        session = launch_args["session"]
    else:
        args = dict(mode=FluentMode.PURE_MESHING_MODE)
        args.update(launch_args)
        try:
            session = launch_fluent(**args)
        except Exception:
            args["mode"] = FluentMode.MESHING_MODE
            session = launch_fluent(**args)
    meshing_workflow = session.watertight()
    if geometry_file_name:
        import_geometry = meshing_workflow.import_geometry
        # change it so we can do this:
        # import_geometry.arguments.FileName = geometry_file_name
        # or import_geometry.FileName = geometry_file_name
        import_geometry.arguments.update_dict(dict(file_name=geometry_file_name))
        import_geometry()
    return meshing_workflow
