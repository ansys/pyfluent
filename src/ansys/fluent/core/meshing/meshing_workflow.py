from ansys.fluent.core.workflow import WorkflowWrapper


class MeshingWorkflow(WorkflowWrapper):
    def __init__(self, workflow, meshing, part_management, pm_file_management):
        super().__init__(workflow=workflow, command_source=meshing)
        self._is_ftm = False
        self._part_management = part_management
        self._pm_file_management = pm_file_management

    def watertight(self, dynamic_interface: bool):
        self._new_workflow(
            name="Watertight Geometry", dynamic_interface=dynamic_interface
        )
        self._is_ftm = False

    def fault_tolerant(self, dynamic_interface: bool):
        self._new_workflow(
            "Fault-tolerant Meshing", dynamic_interface=dynamic_interface
        )
        self._is_ftm = True

    @property
    def part_management(self):
        if self._is_ftm:
            return self._part_management

    @property
    def pm_file_management(self):
        if self._is_ftm:
            return self._pm_file_management
