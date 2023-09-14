"""Workflow module that wraps and extends the core functionality."""

from __future__ import annotations

import logging
import threading
from time import sleep, time
from typing import Any, Iterator, List, Optional, Tuple
import warnings

from ansys.fluent.core.services.datamodel_se import PyCallableStateObject

logger = logging.getLogger("pyfluent.datamodel")


def _new_command_for_task(task, session):
    class NewCommandError(Exception):
        def __init__(self, task_name):
            super().__init__(f"Could not create command for task {task_name}")

    task_cmd_name = task.CommandName()
    cmd_creator = getattr(session, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.create_instance()
        if new_cmd:
            return new_cmd
    raise NewCommandError(task._name_())


def _init_task_accessors(obj):
    logger.debug("_init_task_accessors")
    logger.debug(f"thread id in _init_task_accessors {threading.get_ident()}")
    for task in obj.ordered_children(recompute=True):
        py_name = task.python_name()
        logger.debug(f"py_name: {py_name}")
        obj._python_task_names.append(py_name)
        if py_name not in obj._task_objects:
            logger.debug(f"adding {py_name} {type(task)}")
            obj._task_objects[py_name] = task
        else:
            logger.debug(
                f"Could not add task {py_name} {type(getattr(obj, py_name, None))}"
            )
        _init_task_accessors(task)


def _refresh_task_accessors(obj):
    logger.debug(f"thread id in _refresh_task_accessors {threading.get_ident()}")
    old_task_names = set(obj._python_task_names)
    logger.debug(f"_refresh_task_accessors old_task_names: {old_task_names}")
    tasks = obj.ordered_children(recompute=True)
    current_task_names = [task.python_name() for task in tasks]
    logger.debug(f"current_task_names: {current_task_names}")
    current_task_name_set = set(current_task_names)
    created_task_names = current_task_name_set - old_task_names
    deleted_task_names = old_task_names - current_task_name_set
    for task_name in deleted_task_names:
        try:
            del obj._task_objects[task_name]
        except KeyError:
            pass
    for task_name in created_task_names:
        if task_name not in obj._task_objects:
            logger.debug(f"Add task {task_name}")
            obj._task_objects[task_name] = tasks[current_task_names.index(task_name)]
        else:
            logger.debug(
                f"Could not add task {task_name} {type(getattr(obj, task_name, None))}"
            )
    obj._python_task_names = current_task_names
    logger.debug(f"updated_task_names: {obj._python_task_names}")
    for task in tasks:
        logger.debug(f"next task {task.python_name()} {id(task)}")
        _refresh_task_accessors(task)


class BaseTask:
    """Base class Task representation for wrapping a Workflow TaskObject instance,
    adding methods to discover more about the relationships between TaskObjects.
    Methods
    -------
    get_direct_upstream_tasks()
    get_direct_downstream_tasks()
    ordered_children()
    inactive_ordered_children()
    get_id()
    get_idx()
    __getattr__(attr)
    __setattr__(attr, value)
    __dir__()
    __call__()
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize BaseTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        self.__dict__.update(
            dict(
                _command_source=command_source,
                _workflow=command_source._workflow,
                _source=command_source._command_source,
                _task=task,
                _cmd=None,
                _python_name=None,
                _python_task_names=[],
                _ordered_children=[],
                _task_list=[],
                _task_objects={},
            )
        )

    def get_direct_upstream_tasks(self) -> list:
        """Get the list of tasks upstream of this one and directly connected by
        a data dependency.

        Returns
        -------
        list
            Upstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="requiredInputs", other_attr="outputs"
        )

    def get_direct_upstream_tasks(self) -> list:
        """Get the list of tasks upstream of this one and directly connected by a data dependency.

        Returns
        -------
        upstreams : list
            Upstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="requiredInputs", other_attr="outputs"
        )

    def get_direct_downstream_tasks(self) -> list:
        """Get the list of tasks downstream of this one and directly connected
        by a data dependency.

        Returns
        -------
        list
            Downstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="outputs", other_attr="requiredInputs"
        )

    def ordered_children(self, recompute=True) -> list:
        """Get the ordered task list held by this task. Sorting is in terms
        of the workflow order and only includes this task's top-level tasks, while other tasks
        can be obtained by calling ordered_children() on a parent task.

        Given the workflow::

            Workflow
            ├── A
            ├── B
            │   ├── C
            │   └── D
            └── E

        C and D are the ordered children of task B.

        Returns
        -------
        list
            Ordered children.
        """
        if recompute:

            def task_by_id(mappings):
                def _task_by_id(task_id):
                    if task_id in mappings:
                        return mappings[task_id]
                    try:
                        return self._command_source._task_by_id(task_id)
                    except Exception:
                        pass

                return _task_by_id

            task_list = self._task.TaskList()
            if task_list != self._task_list:
                mappings = {
                    k: v for k, v in zip(self._task_list, self._ordered_children)
                }
                self._ordered_children = list(
                    filter(None, map(task_by_id(mappings), task_list))
                )
                self._task_list = task_list
        return self._ordered_children

    def inactive_ordered_children(self) -> list:
        """Get the inactive ordered child list

        Returns
        -------
        list
            Inactive ordered children.
        """
        return []

    def child_task_python_names(self) -> List[str]:
        """Get the Pythonic names of the child tasks.

        Returns
        -------
        List[str]
            Pythonic names of the child tasks.
        """
        return self._python_task_names

    def get_id(self) -> str:
        """Get the unique string identifier of this task, as it is in the
        application.

        Returns
        -------
        str
            The string identifier.
        """
        workflow_state = self._command_source._workflow_state()
        for k, v in workflow_state.items():
            if isinstance(v, dict) and "_name_" in v:
                if v["_name_"] == self.name():
                    type_, id_ = k.split(":")
                    if type_ == "TaskObject":
                        return id_

    def get_idx(self) -> int:
        """Get the unique integer index of this task, as it is in the
        application.

        Returns
        -------
        int
            The integer index.
        """
        return int(self.get_id()[len("TaskObject") :])

    def python_name(self) -> str:
        """Get the Pythonic name of this task, as it is in the underlying
        application.

        Returns
        -------
        str
            The Pythonic name of this task.
        """
        if not self._python_name:
            try:
                this_command = self._command()
                # temp reuse helpString
                self._python_name = this_command.get_attr("helpString")
            except Exception:
                pass
        return self._python_name

    def delete(self) -> None:
        """Delete this task from the workflow."""
        self._command_source.DeleteTasks(ListOfTasks=[self.name()])

    def __getattr__(self, attr):
        try:
            result = getattr(self._task, attr)
            if result:
                return result
        except AttributeError:
            pass
        try:
            return ArgumentWrapper(self, attr)
        except Exception as ex:
            logger.debug(str(ex))
        self._command_source._wait_on_refresh()
        return self._task_objects.get(attr, None)

    def __setattr__(self, attr, value):
        logger.debug(f"BaseTask.__setattr__({attr}, {value})")
        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            setattr(self._task, attr, value)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._task))
        )

    def __call__(self, **kwds) -> Any:
        if kwds:
            self._task.Arguments.set_state(**kwds)
        return self._task.Execute()

    def _tasks_with_matching_attributes(self, attr: str, other_attr: str) -> list:
        this_command = self._command()
        attrs = this_command.get_attr(attr)
        if not attrs:
            return []
        attrs = set(attrs)
        tasks = [
            task
            for task in self._command_source.ordered_children()
            if task.name() != self.name()
        ]
        matches = []
        for task in tasks:
            command = task._command()
            other_attrs = command.get_attr(other_attr)
            if other_attrs and (attrs & set(other_attrs)):
                matches.append(task)
        return matches


class TaskContainer(PyCallableStateObject):
    """Wrap a workflow TaskObject container.

    Methods
    -------
    __iter__()
    __getitem__(attr)
    __getattr__(attr)
    __dir__()
    """

    def __init__(self, command_source: WorkflowWrapper) -> None:
        """Initialize TaskContainer.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        """
        self._container = command_source
        self._task_container = command_source._workflow.TaskObject

    def __iter__(self) -> Iterator[BaseTask]:
        """Yield the next child object.
        Yields
        ------
        Iterator[BaseTask]
            Iterator of child objects.
        """
        for name in self._get_child_object_display_names():
            yield self[name]

    def __getitem__(self, name):
        logger.debug(f"TaskContainer.__getitem__({name})")
        return _makeTask(self._container, name)

    def __getattr__(self, attr):
        return getattr(self._task_container, attr)

    def __dir__(self):
        return sorted(
            set(
                list(self.__dict__.keys()) + dir(type(self)) + dir(self._task_container)
            )
        )


class ArgumentsWrapper(PyCallableStateObject):
    """Wrapper for a dictionary of task arguments."""

    def __init__(self, task: BaseTask) -> None:
        """Initialize ArgumentsWrapper.

        Parameters
        ----------
        task : BaseTask
            The task holding these arguments.
        """
        self._task = task

    def set_state(self, args: dict) -> None:
        """
        Overwrite arguments.

        Parameters
        ----------
        args : dict
            New argument state.
        """
        self._task.Arguments.set_state(args)

    def update_dict(self, args: dict) -> None:
        """
        Merge with arguments.

        Parameters
        ----------
        args : dict
            new arguments state
        """
        self._task.Arguments.update_dict(args)

    def get_state(self, explicit_only=False) -> dict:
        """
        Get arguments state.

        Parameters
        ----------
        explicit_only : bool
            Whether to only include explicitly set values,
            otherwise all values are included.
        """
        return (
            self._task.Arguments() if explicit_only else self._task._command_arguments()
        )

    def __getattr__(self, attr):
        return getattr(self._task._command_arguments, attr)

    def __setitem__(self, key, value):
        self._task._command_arguments.__setitem__(key, value)


class ArgumentWrapper(PyCallableStateObject):
    """Wrapper for a single task argument"""

    def __init__(self, task: BaseTask, arg: str) -> None:
        """Initialize ArgumentWrapper.

        Parameters
        ----------
        task : BaseTask
            The task holding these arguments.
        arg: str
            Argument name.
        """
        self._task = task
        self._arg_name = arg
        self._arg = getattr(task._command_arguments, arg)
        if self._arg is None:
            raise RuntimeError(f"{arg} is not an argument")

    def set_state(self, value: Any) -> None:
        """
        Set the state of this argument.

        Parameters
        ----------
        value : Any
            New argument value.
        """
        self._task.Arguments.update_dict({self._arg_name: value})

    def get_state(self, explicit_only: bool = False) -> Any:
        """
        Get argument state.

        Parameters
        ----------
        explicit_only : bool
            Whether to return the explicitly set value or the
            full derived value.
        """
        return self._task.Arguments()[self._arg_name] if explicit_only else self._arg()

    def __getattr__(self, attr):
        return getattr(self._arg, attr)


class CommandTask(BaseTask):
    """Intermediate base class task representation for wrapping a Workflow TaskObject instance,
    adding attributes related to commanding. Classes without these attributes cannot be commanded.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize CommandTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    @property
    def CommandArguments(self) -> ReadOnlyObject:
        """Get the task's arguments in read-only form (deprecated).

        Returns
        -------
        ReadOnlyObject
            The task's arguments.
        """
        warnings.warn("CommandArguments", DeprecationWarning)
        return self._refreshed_command()

    @property
    def _command_arguments(self) -> ReadOnlyObject:
        return self._refreshed_command()

    @property
    def arguments(self) -> ArgumentsWrapper:
        """Get the task's arguments.

        Returns
        -------
        ArgumentsWrapper
            The task's arguments.
        """
        return ArgumentsWrapper(self)

    def _refreshed_command(self) -> ReadOnlyObject:
        task_arg_state = self._task.Arguments.get_state()
        cmd = self._command()
        if task_arg_state:
            cmd.set_state(task_arg_state)
        return ReadOnlyObject(self._cmd_sub_items_read_only(cmd))

    def _cmd_sub_items_read_only(self, cmd):
        for item in cmd():
            if type(getattr(cmd, item).get_state()) == dict:
                setattr(cmd, item, self._cmd_sub_items_read_only(getattr(cmd, item)))
            setattr(cmd, item, ReadOnlyObject(getattr(cmd, item)))
        return cmd

    def _command(self):
        if not self._cmd:
            self._cmd = _new_command_for_task(self._task, self._source)
        return self._cmd


class SimpleTask(CommandTask):
    """Simple task representation for wrapping a Workflow TaskObject
    instance of TaskType Simple.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize SimpleTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    def ordered_children(self, recompute=True) -> list:
        """Get the ordered task list held by the workflow. SimpleTasks have no TaskList"""
        return []


class CompoundChild(SimpleTask):
    """Compound Child representation for wrapping a Workflow TaskObject
    instance of TaskType Compound Child.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize CompoundChild.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    def python_name(self) -> str:
        """Get the Pythonic name of this task, as it is in the underlying
        application.

        Returns
        -------
        str
            The Pythonic name of this task.
        """
        pass


class CompositeTask(BaseTask):
    """Composite task representation for wrapping a Workflow TaskObject
    instance of TaskType Composite.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize CompositeTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    @property
    def CommandArguments(self) -> ReadOnlyObject:
        """Get the task's arguments in read-only form (deprecated).

        Returns
        -------
        ReadOnlyObject
            The task's arguments.
        """
        warnings.warn("CommandArguments", DeprecationWarning)
        return {}

    @property
    def _command_arguments(self) -> ReadOnlyObject:
        return {}

    @property
    def arguments(self) -> dict:
        """Get the task's arguments (empty for CompositeTask).

        Returns
        -------
        dict
            The task's arguments (empty).
        """
        return {}


class ConditionalTask(CommandTask):
    """Conditional task representation for wrapping a Workflow TaskObject
    instance of TaskType Conditional.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize ConditionalTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    def inactive_ordered_children(self) -> list:
        """Get the inactive ordered task list held by this task.

        Returns
        -------
        children : list
            Inactive ordered children.
        """
        return [
            self._command_source._task_by_id(task_id)
            for task_id in self._task.InactiveTaskList()
        ]


class CompoundTask(CommandTask):
    """Compound task representation for wrapping a Workflow TaskObject
    instance of TaskType Compound.
    """

    def __init__(self, command_source: WorkflowWrapper, task: str) -> None:
        """Initialize CompoundTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    def add_child(self, state: Optional[dict] = None) -> None:
        """Add a child to this CompoundTask.

        Parameters
        ----------
        state : Optional[dict]
            Optional state.
        """
        state = state or {}
        state.update({"AddChild": "yes"})
        self._task.Arguments.set_state(state)

    def add_child_and_update(self, state=None):
        """Add a child to this CompoundTask and update.

        Parameters
        ----------
        state : Optional[dict]
            Optional state.
        """
        self.add_child(state)
        self._task.AddChildAndUpdate()
        return self.last_child()

    def last_child(self) -> BaseTask:
        """Get the last child of this CompoundTask.

        Returns
        -------
        BaseTask
            the last child of this CompoundTask
        """
        children = self.ordered_children()
        if children:
            return children[-1]

    def compound_child(self, name: str):
        """Get the compound child task of this CompoundTask by name.

        Parameters
        ----------
        name : str
            name

        Returns
        -------
        BaseTask
            the named child of this CompoundTask
        """
        try:
            return next(filter(lambda t: t.name() == name, self.ordered_children()))
        except StopIteration:
            pass


def _makeTask(command_source, name: str) -> BaseTask:
    task = command_source._workflow.TaskObject[name]
    task_type = task.TaskType()
    kinds = {
        "Simple": SimpleTask,
        "Compound Child": CompoundChild,
        "Compound": CompoundTask,
        "Composite": CompositeTask,
        "Conditional": ConditionalTask,
    }
    kind = kinds[task.TaskType()]
    if not kind:
        message = (
            "Unhandled empty workflow task type."
            if not task.TaskType()
            else f"Unhandled workflow task type, {task.TaskType()}."
        )
        raise RuntimeError(message)
    return kind(command_source, task)


class WorkflowWrapper:
    """Wrap a Workflow object, adding methods to discover more about the
    relationships between TaskObjects.

    Methods
    -------
    task(name)
    ordered_children()
    __getattr__(attr)
    __dir__()
    __call__()
    """

    def __init__(self, workflow: PyMenuGeneric, command_source: PyMenuGeneric) -> None:
        """Initialize WorkflowWrapper.

        Parameters
        ----------
        workflow : PyMenuGeneric
            The workflow object.
        command_source : PyMenuGeneric
            The application root for commanding.
        """
        self._workflow = workflow
        self._command_source = command_source
        self._python_task_names = []
        self._refreshing = False
        self._refresh_count = 0
        self._ordered_children = []
        self._task_list = []
        self._getattr_recurse_depth = 0
        self._main_thread_ident = None
        self._task_objects = {}

    def task(self, name: str) -> BaseTask:
        """Get a TaskObject by name, in a BaseTask wrapper. The wrapper adds extra
        functionality.

        Parameters
        ----------
        name : str
            Task name - the display name, not the internal ID.

        Returns
        -------
        task : BaseTask
            wrapped task object.
        """
        return _makeTask(self, name)

    @property
    def TaskObject(self) -> TaskContainer:
        # missing from dir
        """Get a TaskObject container wrapper that 'holds' the underlying
        TaskObjects.

        The wrapper adds extra functionality.
        """
        return TaskContainer(self)

    def ordered_children(self, recompute=True) -> list:
        """Get the ordered task list held by the workflow. Sorting is in terms
        of the workflow order and only includes the top-level tasks, while other tasks
        can be obtained by calling ordered_children() on a parent task. Given the
        workflow:

            Workflow
            ├── A
            ├── B
            │   ├── C
            │   └── D
            └── E

        the ordered children of the workflow are A, B, E, while B has ordered children
        C and D.
        """
        if recompute:
            workflow_state, task_list = self._workflow_and_task_list_state()

            def task_by_id(mappings):
                def _task_by_id(task_id):
                    if task_id in mappings:
                        return mappings[task_id]
                    try:
                        return self._task_by_id_impl(task_id, workflow_state)
                    except Exception:
                        pass

                return _task_by_id

            if task_list != self._task_list:
                mappings = {
                    k: v for k, v in zip(self._task_list, self._ordered_children)
                }
                self._ordered_children = list(
                    filter(None, map(task_by_id(mappings), task_list))
                )
                self._task_list = task_list
        return self._ordered_children

    def child_task_python_names(self) -> List[str]:
        """Get the Pythonic names of the child tasks.

        Returns
        -------
        List[str]
            Pythonic names of the child tasks.
        """
        return self._python_task_names

    def inactive_ordered_children(self) -> list:
        """Get the inactive ordered task list held by this task.

        Returns
        -------
        children : list
            Inactive ordered children.
        """
        return []

    def __getattr__(self, attr):
        """Delegate attribute lookup to the wrapped workflow object
        Parameters
        ----------
        attr : str
            An attribute not defined in WorkflowWrapper
        """
        obj = self._attr_from_wrapped_workflow(
            attr
        )  # or self._task_with_cmd_matching_help_string(attr)
        if obj:
            return obj
        self._wait_on_refresh()
        return self._task_objects.get(attr, None)

    def __dir__(self):
        """Override the behaviour of dir to include attributes in
        WorkflowWrapper and the underlying workflow."""
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._workflow))
        )

    def __call__(self):
        """Delegate calls to the underlying workflow."""
        return self._workflow()

    def _wait_on_refresh(self, time_unit=0.1, skip_check=False):
        if not skip_check:
            t0 = time()
        if skip_check or threading.get_ident() == self._main_thread_ident:
            refresh_count = self._refresh_count
            orig_refresh_count = refresh_count
            sleep(20 * time_unit)
            while self._refreshing or self._refresh_count > refresh_count:
                refresh_count = self._refresh_count
                sleep(time_unit)
            if self._refresh_count > orig_refresh_count:
                self._wait_on_refresh(time_unit=time_unit, skip_check=True)
        if not skip_check:
            logger.debug("_wait_on_refresh time taken {time() - t0}")

    def _workflow_state(self):
        return self._workflow()

    def _workflow_and_task_list_state(self) -> Tuple[dict, dict]:
        workflow_state = self._workflow_state()
        workflow_state_workflow = workflow_state["Workflow"]
        return (workflow_state, workflow_state_workflow["TaskList"])

    def _task_by_id_impl(self, task_id, workflow_state):
        task_key = "TaskObject:" + task_id
        task_state = workflow_state[task_key]
        return self.task(task_state["_name_"])

    def _task_by_id(self, task_id):
        workflow_state = self._workflow_state()
        return self._task_by_id_impl(task_id, workflow_state)

    def _attr_from_wrapped_workflow(self, attr):
        try:
            result = getattr(self._workflow, attr)
            if result:
                return result
        except AttributeError:
            pass

    def _new_workflow(self, name: str, dynamic_interface: bool):
        self._workflow.InitializeWorkflow(WorkflowType=name)
        self._initialize_methods(dynamic_interface=dynamic_interface)

    def _initialize_methods(self, dynamic_interface: bool):
        _init_task_accessors(self)
        if dynamic_interface:
            self._main_thread_ident = threading.get_ident()
            logger.debug(f"setting main thread to {self._main_thread_ident}")

            def refresh_after_sleep(_):
                while self._refreshing:
                    logger.debug("Already _refreshing, ...")
                    sleep(0.1)
                self._refreshing = True
                logger.debug("Call _refresh_task_accessors")
                _refresh_task_accessors(self)
                self._refresh_count += 1
                self._refreshing = False

            self.add_on_affected(refresh_after_sleep)


class ReadOnlyObject:
    """Removes 'set_state()' attribute to implement read-only behaviour."""

    _unwanted_attr = ["set_state", "setState"]

    def __init__(self, cmd):
        self._cmd = cmd

    def is_read_only(self):
        return True

    def __getattr__(self, attr):
        if attr in ReadOnlyObject._unwanted_attr:
            raise AttributeError("Command Arguments are read-only.")
        return getattr(self._cmd, attr)

    def __dir__(self):
        returned_list = sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._cmd))
        )
        for attr in ReadOnlyObject._unwanted_attr:
            if attr in returned_list:
                returned_list.remove(attr)
        return returned_list

    def __call__(self):
        return self._cmd()
