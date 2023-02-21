
from ansys.fluent.core.workflow import WorkflowWrapper


class MeshingWorkflow(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)

    def watertight(self):
        self._new_workflow("Watertight Geometry")

    def fault_tolerant(self):
        self._new_workflow("Fault-tolerant Meshing")
