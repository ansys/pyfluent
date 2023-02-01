
from ansys.fluent.core.workflow import ExtendedWorkflow


class MeshingWorkflow(ExtendedWorkflow):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)

    def watertight(self):
        self._workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    def tolerant(self):
        self._workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
