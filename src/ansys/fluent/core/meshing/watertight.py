"""Watertight workflow module."""

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.launcher.launcher_utils import FluentMode

from .meshing_workflow import MeshingWorkflow


def watertight_workflow(geometry_file_name, **launch_args) -> MeshingWorkflow:
    """A meshing workflow wrapper, initialized as watertight.

    Parameters
    ----------
    geometry_file_name : str
        The path of a valid geometry file to import. Can be unset.
    launch_args
        Additional arguments forwarded to the launch_fluent function.

    Returns
    -------
    MeshingWorkflow
        A meshing workflow wrapper
    """
    dynamic_interface = True
    if "dynamic_interface" in launch_args:
        dynamic_interface = launch_args["dynamic_interface"]
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
    meshing_workflow = session.workflow
    meshing_workflow.watertight(dynamic_interface=dynamic_interface)
    if geometry_file_name:
        import_geometry = meshing_workflow.task("Import Geometry")
        # change it so we can do this:
        # import_geometry.arguments.FileName = geometry_file_name
        # or import_geometry.FileName = geometry_file_name
        import_geometry.arguments.update_dict(dict(FileName=geometry_file_name))
        import_geometry.Execute()
    return meshing_workflow
