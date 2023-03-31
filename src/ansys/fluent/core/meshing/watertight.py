from ansys.fluent.core.launcher.launcher import LaunchMode, launch_fluent

from .meshing_workflow import MeshingWorkflow


def watertight_workflow(geometry_filepath, **launch_args) -> MeshingWorkflow:
    if "session" in launch_args:
        session = launch_args["session"]
    else:
        args = dict(mode=LaunchMode.PURE_MESHING_MODE)
        args.update(launch_args)
        try:
            session = launch_fluent(**args)
        except BaseException:
            args["mode"] = LaunchMode.MESHING_MODE
            session = launch_fluent(**args)
    meshing_workflow = session.workflow
    meshing_workflow.watertight()
    if geometry_filepath:
        import_geometry = meshing_workflow.task("Import Geometry")
        # change it so we can do this:
        # import_geometry.arguments.FileName = geometry_filepath
        # or import_geometry.FileName = geometry_filepath
        import_geometry.arguments.update_dict(dict(FileName=geometry_filepath))
        import_geometry.Execute()
    return meshing_workflow
