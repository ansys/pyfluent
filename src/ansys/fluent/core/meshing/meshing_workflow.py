
from ansys.fluent.core.workflow import WorkflowWrapper


class MeshingWorkflow(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)
        self.__workflow = None

    def watertight(self):
        self._workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
        self.__workflow = AutoWatertight(
            self._workflow, self._command_source)
        return self.__workflow

    def tolerant(self):
        self._workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
        self.__workflow = FaultTolerant(
            self._workflow, self._command_source)
        return self.__workflow


class AutoWatertight(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)

    def __getattr__(self, attr):
        try:
            result = super().__getattr__(attr)
            if result:
                return result
        except AttributeError:
            pass
        child_tasks = self.ordered_children()
        for task in child_tasks:
            cmd = task._command()
            # temp reuse helpString
            py_name = cmd.get_attr("helpString")
            if py_name == attr:
                return lambda: task


class Watertight(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)

    def import_geometry(self):
        return self.task("Import Geometry")

    def add_local_sizing(self, name=None):
        return self._compound_task(
            task_name="Add Local Sizing",
            child_name=name)

    def generate_surface_mesh(self):
        return self.task("Generate the Surface Mesh")

    def describe_geometry(self):
        return self.task("Describe Geometry")

    def cap(self, name=None):
        return self._compound_task(
            task_name="Enclose Fluid Regions (Capping)",
            child_name=name)

    def create_regions(self):
        return self.task("Create Regions")

    def update_regions(self):
        return self.task("Update Regions")

    def add_boundary_layers(self, name=None):
        return self._compound_task(
            task_name="Add Boundary Layers",
            child_name=name)

    def generate_volume_mesh(self):
        return self.task("Generate the Volume Mesh")


class FaultTolerant(WorkflowWrapper):

    def __init__(self, workflow, command_source):
        super().__init__(workflow, command_source)
