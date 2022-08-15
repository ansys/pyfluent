from typing import Any

from ansys.fluent.core.services.datamodel_se import PyCallableStateObject


def _new_command_for_task(task, meshing):
    class NewCommandError(Exception):
        def __init__(self, task_name):
            super().__init__(f"Could not create command for meshing task {task_name}")

    task_cmd_name = task.CommandName()
    cmd_creator = getattr(meshing, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.new()
        if new_cmd:
            return new_cmd
    raise NewCommandError(task._name_())


class MeshingWorkflow:
    class Task(PyCallableStateObject):
        class Args(PyCallableStateObject):
            def __init__(self, task):
                self._task = task
                self._args = task.Arguments

            def __getattr__(self, attr):
                return getattr(self._args, attr)

            def get_command_argument_state(self) -> Any:
                return self._task.get_command_argument_state()

            def get_command_argument_attribute_value(
                self, attribute_sub_path: str
            ) -> Any:
                return self._task.get_command_argument_attribute_value(
                    attribute_sub_path
                )

        def __init__(self, meshing, name):
            self._workflow = meshing._workflow
            self._meshing = meshing._meshing
            self._task = self._workflow.TaskObject[name]
            self._cmd = None
            self.Arguments = MeshingWorkflow.Task.Args(self)

        def get_command_argument_attribute_value(self, attribute_sub_path: str) -> Any:
            cmd = self._refreshed_command()
            return cmd.get_attrib_value(attribute_sub_path)

        def get_command_argument_state(self) -> Any:
            return self._refreshed_command().get_state()

        def _refreshed_command(self):
            task_arg_state = self.Arguments.get_state()
            cmd = self._command()
            cmd.set_state(task_arg_state)
            return cmd

        def _command(self):
            if not self._cmd:
                self._cmd = _new_command_for_task(self._task, self._meshing)
            return self._cmd

        def __getattr__(self, attr):
            return getattr(self._task, attr)

    def __init__(self, workflow, meshing):
        self._workflow = workflow
        self._meshing = meshing

    def task(self, name):
        return MeshingWorkflow.Task(self, name)

    def __getattr__(self, attr):
        return getattr(self._workflow, attr)
