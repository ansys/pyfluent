from ansys.fluent.core.services.datamodel_se import MakeReadOnly, PyCallableStateObject


def _new_command_for_task(task, session):
    class NewCommandError(Exception):
        def __init__(self, task_name):
            super().__init__(f"Could not create command for meshing task {task_name}")

    task_cmd_name = task.CommandName()
    cmd_creator = getattr(session, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.new()
        if new_cmd:
            return new_cmd
    raise NewCommandError(task._name_())


class WorkflowWrapper:
    class TaskContainer(PyCallableStateObject):
        def __init__(self, command_source):
            self._container = command_source
            self._task_container = command_source._workflow.TaskObject

        def __getitem__(self, name):
            return WorkflowWrapper.Task(self._container, name)

        def __getattr__(self, attr):
            return getattr(self._task_container, attr)

        def __dir__(self):
            return sorted(
                set(
                    list(self.__dict__.keys())
                    + dir(type(self))
                    + dir(self._task_container)
                )
            )

    class Task(PyCallableStateObject):
        def __init__(self, command_source, name):
            self.__dict__.update(
                dict(
                    _workflow=command_source._workflow,
                    _source=command_source._command_source,
                    _task=command_source._workflow.TaskObject[name],
                    _cmd=None,
                )
            )

        @property
        def CommandArguments(self):
            return self._refreshed_command()

        def _refreshed_command(self):
            task_arg_state = self.Arguments.get_state()
            cmd = self._command()
            if task_arg_state:
                cmd.set_state(task_arg_state)
            return MakeReadOnly(cmd)

        def _command(self):
            if not self._cmd:
                self._cmd = _new_command_for_task(self._task, self._source)
            return self._cmd

        def __getattr__(self, attr):
            return getattr(self._task, attr)

        def __setattr__(self, attr, value):
            if attr in self.__dict__:
                self.__dict__[attr] = value
            else:
                setattr(self._task, attr, value)

        def __dir__(self):
            return sorted(
                set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._task))
            )

    def __init__(self, workflow, command_source):
        self._workflow = workflow
        self._command_source = command_source

    def task(self, name):
        return WorkflowWrapper.Task(self, name)

    @property
    def TaskObject(self):
        return WorkflowWrapper.TaskContainer(self)

    def __getattr__(self, attr):
        return getattr(self._workflow, attr)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._workflow))
        )

    def __call__(self):
        return self._workflow()
