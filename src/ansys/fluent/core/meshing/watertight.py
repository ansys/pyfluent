from ansys.fluent.core.launcher.launcher import LaunchMode, launch_fluent


class WatertightWorkflow:
    def __init__(self, geometry_filepath, **launch_args) -> None:
        args = dict(mode=LaunchMode.PURE_MESHING_MODE)
        args.update(launch_args)
        self._session = launch_fluent(**args)
        self._meshing_workflow = self._session.workflow
        self._meshing_workflow.watertight()
        if geometry_filepath:
            import_geometry = self._meshing_workflow.task("Import Geometry")
            # change it so we can do this:
            # import_geometry.arguments.FileName = geometry_filepath
            import_geometry.arguments.update_dict(dict(FileName=geometry_filepath))
            import_geometry.Execute()

    def __getattr__(self, attr):
        return getattr(self._meshing_workflow, attr)

    def __dir__(self):
        return dir(self._meshing_workflow)

    def __call__(self):
        """Delegate calls to the underlying workflow."""
        return self._meshing_workflow()
