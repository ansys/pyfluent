
from ansys.fluent.core.workflow import WorkflowWrapper

class MeshingWorkflow(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)

    def import_geometry(self):
        return self.task("Import Geometry")

    def add_local_sizing(self, name=None):
        return self._compound_task(
            task_name="Add Local Sizing",
            child_name=name)

