from ansys.fluent.core.services.datamodel_se import PyCallableStateObject


def _new_command_for_task(task, session):
    class NewCommandError(Exception):
        def __init__(self, task_name):
            super().__init__(f"Could not create command for meshing task {task_name}")

    task_cmd_name = task.CommandName()
    cmd_creator = getattr(session, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.create_instance()
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
                    _command_source=command_source,
                    _workflow=command_source._workflow,
                    _source=command_source._command_source,
                    _task=command_source._workflow.TaskObject[name],
                    _cmd=None,
                )
            )

        def _task_by_id(self, task_id):
            workflow_state = self._workflow()
            workflow_state_workflow = workflow_state["Workflow"]
            workflow_state_tasklist = workflow_state_workflow["TaskList"]
            task_key = "TaskObject:" + task_id
            task_state = workflow_state[task_key]
            return self._command_source.task(task_state["_name_"])

        def _all_task_objects(self):
            workflow_state = self._workflow()
            workflow_state_workflow = workflow_state["Workflow"]
            workflow_state_tasklist = workflow_state_workflow["TaskList"]
            tasks = []
            for task_id in workflow_state_tasklist:
                task_key = "TaskObject:" + task_id
                task_state = workflow_state[task_key]
                tasks.append(self._command_source.task(task_state["_name_"]))
            return tasks

        def _tasks_with_matching_attributes(self, attr, other_attr):
            this_command = self._command()
            attrs = this_command.get_attr(attr)
            if not attrs:
                return []
            attrs = set(attrs)
            tasks = [
                task for task in self._all_task_objects() if
                task.name() != self.name()
            ]
            matches = []
            for task in tasks:
                command = task._command()
                other_attrs = command.get_attr(other_attr)
                if other_attrs and (attrs & set(other_attrs)):
                    matches.append(task)
            return matches

        def get_direct_upstream_tasks(self):
            return self._tasks_with_matching_attributes(
                attr="requiredInputs",
                other_attr="outputs"
                )

        def get_direct_downstream_tasks(self):
            return self._tasks_with_matching_attributes(
                attr="outputs",
                other_attr="requiredInputs"
                )

        def get_sub_tasks(self):
            sub_task_ids = self._task.TaskList()
            return [self._task_by_id(task_id) for task_id in self._task.TaskList()]

        @property
        def CommandArguments(self):
            return self._refreshed_command()

        def _refreshed_command(self):
            task_arg_state = self.Arguments.get_state()
            cmd = self._command()
            if task_arg_state:
                cmd.set_state(task_arg_state)
            return _MakeReadOnly(self._cmd_sub_items_read_only(cmd))

        def _cmd_sub_items_read_only(self, cmd):
            for item in cmd():
                if type(getattr(cmd, item).get_state()) == dict:
                    setattr(
                        cmd, item, self._cmd_sub_items_read_only(getattr(cmd, item))
                    )
                setattr(cmd, item, _MakeReadOnly(getattr(cmd, item)))
            return cmd

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
        # missing from dir
        return WorkflowWrapper.TaskContainer(self)

    def __getattr__(self, attr):
        return getattr(self._workflow, attr)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._workflow))
        )

    def __call__(self):
        return self._workflow()


class _MakeReadOnly:
    """Removes 'set_state()' attribute to implement read-only behaviour."""

    _unwanted_attr = ["set_state", "setState"]

    def __init__(self, cmd):
        self._cmd = cmd

    def __getattr__(self, attr):
        if attr in _MakeReadOnly._unwanted_attr:
            raise AttributeError("Command Arguments are read-only.")
        return getattr(self._cmd, attr)

    def __dir__(self):
        returned_list = sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._cmd))
        )
        for attr in _MakeReadOnly._unwanted_attr:
            if attr in returned_list:
                returned_list.remove(attr)
        return returned_list

    def __call__(self):
        return self._cmd()
