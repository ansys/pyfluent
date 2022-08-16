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
        def __init__(self, meshing, name):
            self._workflow = meshing._workflow
            self._meshing = meshing._meshing
            self._task = self._workflow.TaskObject[name]
            self._cmd = None

        @property
        def CommandArguments(self):
            return self._refreshed_command()

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

        def __dir__(self):
            return sorted(
                set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._task))
            )

    def __init__(self, workflow, meshing):
        self._workflow = workflow
        self._meshing = meshing

    def task(self, name):
        return MeshingWorkflow.Task(self, name)

    def __getattr__(self, attr):
        return getattr(self._workflow, attr)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._workflow))
        )

    def __call__(self):
        return self._workflow()
