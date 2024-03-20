"""Workflow module that wraps and extends the core functionality."""

from __future__ import annotations

import logging
import re
import threading
from typing import Any, Iterable, Iterator, List, Optional, Tuple, Union
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.services.datamodel_se import (
    PyCallableStateObject,
    PyCommand,
    PyMenuGeneric,
    PySingletonCommandArgumentsSubItem,
)


def camel_to_snake_case(camel_case_str: str) -> str:
    """Convert camel case input string to snake case output string."""
    try:
        return camel_to_snake_case.cache[camel_case_str]
    except KeyError:
        _snake_case_str = re.sub(
            "((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", camel_case_str
        ).lower()
        camel_to_snake_case.cache[camel_case_str] = _snake_case_str
        return _snake_case_str


camel_to_snake_case.cache = {}


def snake_to_camel_case(snake_case_str: str, camel_case_strs: Iterable):
    """Populate the snake-case attribute map and return camel case of the passed
    attribute."""
    try:
        return snake_to_camel_case.cache[snake_case_str]
    except KeyError:
        if snake_case_str.islower():
            for camel_case_str in camel_case_strs:
                _snake_case_str = camel_to_snake_case(camel_case_str)
                if _snake_case_str not in snake_to_camel_case.cache:
                    snake_to_camel_case.cache[_snake_case_str] = camel_case_str
                if _snake_case_str == snake_case_str:
                    return camel_case_str


snake_to_camel_case.cache = {}


logger = logging.getLogger("pyfluent.datamodel")


def _new_command_for_task(task, session):
    class NewCommandError(Exception):
        """Raised on an attempt to create command for a given task."""

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
    logger.debug(f"thread ID in _init_task_accessors {threading.get_ident()}")
    for task in obj.ordered_children(recompute=True):
        py_name = task.python_name()
        logger.debug(f"py_name: {py_name}")
        with obj._lock:
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
    logger.debug(f"thread ID in _refresh_task_accessors {threading.get_ident()}")
    with obj._lock:
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
    with obj._lock:
        obj._python_task_names = current_task_names
        logger.debug(f"updated_task_names: {obj._python_task_names}")
    for task in tasks:
        logger.debug(f"next task {task.python_name()} {id(task)}")
        _refresh_task_accessors(task)


def _convert_task_list_to_display_names(workflow_root, task_list):
    if pyfluent.DATAMODEL_USE_STATE_CACHE:
        workflow_state = DataModelCache.get_state("workflow", workflow_root)
        return [workflow_state[f"TaskObject:{x}"]["_name_"] for x in task_list]
    else:
        _display_names = []
        _org_path = workflow_root.path
        for _task_name in task_list:
            workflow_root.path = [("TaskObject", _task_name), ("_name_", "")]
            _display_names.append(workflow_root())
        workflow_root.path = _org_path
        return _display_names


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

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
        """Initialize BaseTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            Set of workflow commands.
        task : str
            Name of this task.
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
                _lock=command_source._lock,
                _ordered_children=[],
                _task_list=[],
                _task_objects={},
                _dynamic_interface=command_source._dynamic_interface,
            )
        )

    def get_direct_upstream_tasks(self) -> list:
        """Get the list of tasks upstream of this one and directly connected by a data
        dependency.

        Returns
        -------
        list
            Upstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="requiredInputs", other_attr="outputs"
        )

    def get_direct_upstream_tasks(self) -> list:
        """Get the list of tasks upstream of this one and directly connected by a data
        dependency.

        Returns
        -------
        list
            Upstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="requiredInputs", other_attr="outputs"
        )

    def get_direct_downstream_tasks(self) -> list:
        """Get the list of tasks downstream of this one and directly connected by a data
        dependency.

        Returns
        -------
        list
            Downstream task list.
        """
        return self._tasks_with_matching_attributes(
            attr="outputs", other_attr="requiredInputs"
        )

    def ordered_children(self, recompute=True) -> list:
        """Get the ordered task list held by this task. Sorting is in terms of the
        workflow order and only includes this task's top-level tasks, while other tasks
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
            task_list = _convert_task_list_to_display_names(self._workflow, task_list)
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
        """Get the inactive ordered child list.

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
        """Get the unique string identifier of this task, as it is in the application.

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
        """Get the unique integer index of this task, as it is in the application.

        Returns
        -------
        int
            The integer index.
        """
        return int(self.get_id()[len("TaskObject") :])

    def python_name(self) -> str:
        """Get the Pythonic name of this task, as it is in the underlying application.

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

    def _get_camel_case_arg_keys(self):
        _args = self.arguments
        _camel_args = []
        for arg in _args().keys():
            _camel_args.append(_args._snake_to_camel_map[arg])

        return _camel_args

    def __getattr__(self, attr):
        if self._dynamic_interface:
            if not attr.islower() and attr != "Arguments":
                raise AttributeError(
                    "Camel case attribute access is not supported. "
                    f"Try using '{camel_to_snake_case(attr)}' instead."
                )
            camel_attr = snake_to_camel_case(
                str(attr), [*self._get_camel_case_arg_keys(), *dir(self._task)]
            )
            attr = camel_attr or attr
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
        return self._task_objects.get(attr, None)

    def __setattr__(self, attr, value):
        logger.debug(f"BaseTask.__setattr__({attr}, {value})")
        if attr in self.__dict__:
            self.__dict__[attr] = value
        elif attr in self.arguments():
            getattr(self, attr).set_state(value)
        else:
            setattr(self._task, attr, value)

    def __dir__(self):
        arg_list = []
        if self._dynamic_interface:
            for arg in [*self._get_camel_case_arg_keys(), *dir(self._task)]:
                arg_list.append(camel_to_snake_case(arg))
        else:
            for arg in [*self.arguments().keys(), *dir(self._task)]:
                arg_list.append(arg)

        return sorted(set(list(self.__dict__.keys()) + dir(type(self)) + arg_list))

    def delete(self) -> None:
        """Delete this task from the workflow."""
        self._command_source.delete_tasks(list_of_tasks=[self.python_name()])

    def rename(self, new_name: str):
        """Rename the current task to a given name."""
        return self._task.Rename(NewName=new_name)

    def add_child_to_task(self):
        """Add a child task."""
        return self._task.AddChildToTask()

    def update_child_tasks(self, setup_type_changed: bool):
        """Update child tasks."""
        self._task.UpdateChildTasks(SetupTypeChanged=setup_type_changed)

    def insert_compound_child_task(self):
        """Insert a compound child task."""
        return self._task.InsertCompoundChildTask()

    def get_next_possible_tasks(self) -> list[str]:
        """Get the list of possible names of commands that can be inserted as tasks
        after this current task is executed."""
        return [camel_to_snake_case(task) for task in self._task.GetNextPossibleTasks()]

    def insert_next_task(self, command_name: str):
        """Insert a task based on the command name passed as argument after the current
        task is executed.

        Parameters
        ----------
        command_name: str
            Name of the new task.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the command name does not match a task name.
        """
        if command_name not in self.get_next_possible_tasks():
            raise ValueError(
                f"'{command_name}' cannot be inserted next to '{self.python_name()}'. \n"
                "Please use 'get_next_possible_tasks()' to view list of allowed tasks."
            )
        return self._task.InsertNextTask(
            CommandName=snake_to_camel_case(
                command_name, self._task.GetNextPossibleTasks()
            )
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

    def display_name(self):
        """Display name."""
        return self._name_()

    def __repr__(self):
        return f"<Task '{self.display_name()}'>"


class TaskContainer(PyCallableStateObject):
    """Wrap a workflow TaskObject container.

    Methods
    -------
    __iter__()
    __getitem__(attr)
    __getattr__(attr)
    __dir__()
    """

    def __init__(self, command_source: ClassicWorkflow) -> None:
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

    def items(self):
        """Get state items."""
        return self._task_container.get_state().items()

    def get_state(self):
        """Get state."""
        return self._task_container.get_state()

    def __call__(self):
        return self.get_state()


class ArgumentsWrapper(PyCallableStateObject):
    """Wrapper for a dictionary of task arguments."""

    def __init__(self, task: BaseTask) -> None:
        """Initialize ArgumentsWrapper.

        Parameters
        ----------
        task : BaseTask
            Task holding these arguments.
        """
        self.__dict__.update(
            dict(
                _task=task,
                _dynamic_interface=task._dynamic_interface,
                _snake_to_camel_map={},
            )
        )

    def set_state(self, args: dict) -> None:
        """Overwrite arguments.

        Parameters
        ----------
        args : dict
            State of the arguments.
        """
        if self._dynamic_interface:
            self.get_state()
            camel_args = {}
            for key, val in args.items():
                camel_args[self._snake_to_camel_map[key]] = val
            self._task.Arguments.set_state(camel_args)
        else:
            self._task.Arguments.set_state(args)

    def update_dict(self, args: dict) -> None:
        """Merge with arguments.

        Parameters
        ----------
        args : dict
            State of the arguments.
        """
        if self._dynamic_interface:
            self.get_state()
            camel_args = {}
            for key, val in args.items():
                camel_args[self._snake_to_camel_map[key]] = val
            self._task.Arguments.update_dict(camel_args)
        else:
            self._task.Arguments.update_dict(args)

    def get_state(self, explicit_only=False) -> dict:
        """Get the state of the arguments.

        Parameters
        ----------
        explicit_only : bool
            Whether to only include explicitly set values.
            Otherwise, all values are included.
        """
        state_dict = (
            self._task.Arguments() if explicit_only else self._task._command_arguments()
        )

        if self._dynamic_interface:
            snake_case_state_dict = {}
            for key, val in state_dict.items():
                nested_val = {}
                if isinstance(
                    getattr(self._task._command_arguments, key),
                    PySingletonCommandArgumentsSubItem,
                ):
                    for k, v in val.items():
                        self._snake_to_camel_map[camel_to_snake_case(k)] = k
                        nested_val[camel_to_snake_case(k)] = v
                else:
                    nested_val = val
                self._snake_to_camel_map[camel_to_snake_case(key)] = key
                snake_case_state_dict[camel_to_snake_case(key)] = nested_val
            return snake_case_state_dict

        return state_dict

    def __getattr__(self, attr):
        return getattr(self._task._command_arguments, attr)

    def __setattr__(self, key, value):
        try:
            getattr(self, key).set_state(value)
        except AttributeError:
            raise AttributeError(
                f"No attribute named '{key}' in '{self._task.name()}'."
            )

    def __setitem__(self, key, value):
        self._task._command_arguments.__setitem__(key, value)


class ArgumentWrapper(PyCallableStateObject):
    """Wrapper for a single task argument."""

    def __init__(self, task: BaseTask, arg: str) -> None:
        """Initialize ArgumentWrapper.

        Parameters
        ----------
        task : BaseTask
            The task holding these arguments.
        arg: str
            Argument name.
        """
        self.__dict__.update(
            dict(
                _task=task,
                _arg_name=arg,
                _arg=getattr(task._command_arguments, arg),
                _dynamic_interface=task._dynamic_interface,
                _snake_to_camel_map={},
            )
        )
        if self._arg is None:
            raise RuntimeError(f"{arg} is not an argument.")

    def set_state(self, value: Any) -> None:
        """Set the state of the argument.

        Parameters
        ----------
        value : Any
            Value of the argument.
        """
        self._task.Arguments.update_dict({self._arg_name: value})

    def get_state(self, explicit_only: bool = False) -> Any:
        """Get the state of this argument.

        Parameters
        ----------
        explicit_only : bool
            Whether to return the explicitly set value or the
            full derived value.
        """

        state_dict = (
            self._task.Arguments()[self._arg_name] if explicit_only else self._arg()
        )

        if self._dynamic_interface and isinstance(
            self._arg, PySingletonCommandArgumentsSubItem
        ):
            snake_case_state_dict = {}
            for key, val in state_dict.items():
                self._snake_to_camel_map[camel_to_snake_case(key)] = key
                snake_case_state_dict[camel_to_snake_case(key)] = val
            return snake_case_state_dict

        return state_dict

    def _get_camel_case_arg_keys(self):
        _args = self
        _camel_args = []
        for arg in _args().keys():
            try:
                _camel_args.append(self._snake_to_camel_map[arg])
            except KeyError:
                _camel_args.append(arg)

        return _camel_args

    def __getattr__(self, attr):
        if self._dynamic_interface:
            if not attr.islower():
                raise AttributeError(
                    "Camel case attribute access is not supported. "
                    f"Try using '{camel_to_snake_case(attr)}' instead."
                )
            camel_attr = snake_to_camel_case(str(attr), self._get_camel_case_arg_keys())
            attr = camel_attr or attr
        return getattr(self._arg, attr)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            if self._dynamic_interface:
                camel_attr = snake_to_camel_case(
                    str(attr), self._get_camel_case_arg_keys()
                )
                attr = camel_attr or attr
            self.set_state({attr: value})

    def __dir__(self):
        arg_list = []
        for arg in self():
            arg_list.append(
                camel_to_snake_case(arg) if self._dynamic_interface else arg
            )
        return sorted(set(list(self.__dict__.keys()) + dir(type(self)) + arg_list))


class CommandTask(BaseTask):
    """Intermediate base class task representation for wrapping a Workflow TaskObject
    instance, adding attributes related to commanding.

    Classes without these attributes cannot be commanded.
    """

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
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
    def command_arguments(self) -> ReadOnlyObject:
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
        return self._cmd_sub_items_read_only(cmd, cmd())

    def _cmd_sub_items_read_only(self, cmd, cmd_state):
        for key, value in cmd_state.items():
            if type(value) == dict:
                setattr(
                    cmd, key, self._cmd_sub_items_read_only(getattr(cmd, key), value)
                )
            setattr(cmd, key, getattr(cmd, key))
        return cmd

    def _command(self):
        if not self._cmd:
            self._cmd = _new_command_for_task(self._task, self._source)
        return self._cmd


class SimpleTask(CommandTask):
    """Simple task representation for wrapping a Workflow TaskObject instance of
    TaskType Simple."""

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
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
        """Get the ordered task list held by the workflow.

        SimpleTasks have no TaskList.
        """
        return []


class CompoundChild(SimpleTask):
    """Compound Child representation for wrapping a Workflow TaskObject instance of
    TaskType Compound Child."""

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
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
        """Get the Pythonic name of this task, as it is in the underlying application.

        Returns
        -------
        str
            The Pythonic name of this task.
        """
        pass


class CompositeTask(BaseTask):
    """Composite task representation for wrapping a Workflow TaskObject instance of
    TaskType Composite."""

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
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
    def command_arguments(self) -> ReadOnlyObject:
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

    def insert_composite_child_task(self, command_name: str):
        """Insert a composite child task based on the command name passed as
        argument."""
        return self._task.InsertCompositeChildTask(CommandName=command_name)


class ConditionalTask(CommandTask):
    """Conditional task representation for wrapping a Workflow TaskObject instance of
    TaskType Conditional."""

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
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
        list
            Inactive ordered children.
        """
        inactive_task_list = self._task.InactiveTaskList()
        inactive_task_list = _convert_task_list_to_display_names(inactive_task_list)
        return [
            self._command_source._task_by_id(task_id) for task_id in inactive_task_list
        ]


class CompoundTask(CommandTask):
    """Compound task representation for wrapping a Workflow TaskObject instance of
    TaskType Compound."""

    def __init__(
        self,
        command_source: Union[ClassicWorkflow, Workflow],
        task: str,
    ) -> None:
        """Initialize CompoundTask.

        Parameters
        ----------
        command_source : WorkflowWrapper
            The set of workflow commands.
        task : str
            The name of this task.
        """
        super().__init__(command_source, task)

    def _add_child(self, state: Optional[dict] = None) -> None:
        """Add a child to this CompoundTask.

        Parameters
        ----------
        state : Optional[dict]
            Optional state.
        """
        state = state or {}
        if self._dynamic_interface:
            state.update({"add_child": "yes"})
            self.arguments.set_state(state)
        else:
            state.update({"AddChild": "yes"})
            self._task.Arguments.set_state(state)

    def add_child_and_update(self, state=None):
        """Add a child to this CompoundTask and update.

        Parameters
        ----------
        state : Optional[dict]
            Optional state.
        """
        self._add_child(state)
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


class Workflow:
    """Wraps a workflow object, adding methods to discover more about the relationships
    between task objects.

    Methods
    -------
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
        self._lock = threading.RLock()
        self._refreshing = False
        self._refresh_count = 0
        self._ordered_children = []
        self._task_list = []
        self._getattr_recurse_depth = 0
        self._main_thread_ident = None
        self._task_objects = {}
        self._dynamic_interface = False
        self._help_string_command_id_map = {}
        self._help_string_display_text_map = {}
        self._unwanted_attrs = {
            "reset_workflow",
            "initialize_workflow",
            "load_workflow",
            "create_new_workflow",
            "rules",
            "service",
            "task_object",
            "workflow",
        }

    def task(self, name: str) -> BaseTask:
        """Get a TaskObject by name, in a ``BaseTask`` wrapper. The wrapper adds extra
        functionality.

        Parameters
        ----------
        name : str
            Task name - the display name, not the internal ID.
        Returns
        -------
        BaseTask
            wrapped task object.
        """
        return _makeTask(self, name)

    def ordered_children(self, recompute=True) -> list:
        """Get the ordered task list held by the workflow. Sorting is in terms of the
        workflow order and only includes the top-level tasks, while other tasks can be
        obtained by calling ordered_children() on a parent task. Consider the following
        workflow.

        Given the workflow::

            Workflow
            ├── A
            ├── B
            │   ├── C
            │   └── D
            └── E

        The ordered children of the workflow are A, B, E, while B has ordered children C
        and D.
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
        with self._lock:
            return self._python_task_names

    def inactive_ordered_children(self) -> list:
        """Get the inactive ordered task list held by this task.

        Returns
        -------
        list
            Inactive ordered children.
        """
        return []

    def __getattr__(self, attr):
        """Delegate attribute lookup to the wrapped workflow object."""
        _task_object = self._task_objects.get(attr)
        if _task_object:
            return _task_object
        if attr != "TaskObject" and attr not in self._unwanted_attrs:
            if not attr.islower():
                raise AttributeError(
                    "Camel case attribute access is not supported. "
                    f"Try using '{camel_to_snake_case(attr)}' instead."
                )
            camel_attr = snake_to_camel_case(str(attr), dir(self._workflow))
            attr = camel_attr or attr
            obj = self._attr_from_wrapped_workflow(attr)
            if obj:
                return obj
        return super().__getattribute__(attr)

    def __dir__(self):
        """Override the behavior of ``dir`` to include attributes in the
        ``WorkflowWrapper`` class and the underlying workflow."""
        arg_list = [camel_to_snake_case(arg) for arg in dir(self._workflow)]
        dir_set = set(
            list(self.__dict__)
            + dir(type(self))
            + arg_list
            + self.child_task_python_names()
        )
        dir_set = dir_set - self._unwanted_attrs
        return sorted(filter(None, dir_set))

    def __call__(self):
        """Delegate calls to the underlying workflow."""
        return self._workflow()

    def _workflow_state(self):
        return self._workflow()

    def _workflow_and_task_list_state(self) -> Tuple[dict, dict]:
        workflow_state = self._workflow_state()
        prefix = "TaskObject:"
        task_list = [
            x.removeprefix(prefix)
            for x in workflow_state.keys()
            if x.startswith(prefix)
        ]
        return workflow_state, task_list

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

    def _new_workflow(self, name: str, dynamic_interface: bool = True):
        self._dynamic_interface = dynamic_interface
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
                self._refreshing = True
                logger.debug("Call _refresh_task_accessors")
                _refresh_task_accessors(self)
                self._refresh_count += 1
                self._refreshing = False

            self.add_on_affected(refresh_after_sleep)

    def save_workflow(self, file_path: str):
        """Save the current workflow to the location provided."""
        self._workflow.SaveWorkflow(FilePath=file_path)

    def load_state(self, list_of_roots: list):
        """Load the state of the workflow."""
        self._workflow.LoadState(ListOfRoots=list_of_roots)

    def _populate_help_string_command_id_map(self):
        if not self._help_string_command_id_map:
            for command in dir(self._command_source):
                if command in ["SwitchToSolution", "set_state"]:
                    continue
                command_obj = getattr(self._command_source, command)
                if isinstance(command_obj, PyCommand):
                    command_obj_instance = command_obj.create_instance()
                    help_str = command_obj_instance.get_attr("helpString")
                    if help_str and help_str.islower():
                        self._help_string_command_id_map[help_str] = command
                        self._help_string_display_text_map[help_str] = (
                            command_obj_instance.get_attr("displayText")
                        )
                    del command_obj_instance

    def get_possible_tasks(self):
        """Get the list of possible names of commands that can be inserted as tasks."""
        self._populate_help_string_command_id_map()
        return list(self._help_string_command_id_map)

    def insert_new_task(self, command_name: str):
        """Insert a new task based on the command name passed as an argument.

        Parameters
        ----------
        command_name: str
            Name of the new task.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the command name does not match a task name.
            In this case, none of the tasks are deleted.
        """
        self._populate_help_string_command_id_map()
        if command_name not in self._help_string_command_id_map:
            raise ValueError(
                f"'{command_name}' is not an allowed command task.\n"
                "Use the 'get_possible_tasks()' method to view a list of allowed command tasks."
            )
        return self._workflow.InsertNewTask(
            CommandName=self._help_string_command_id_map[command_name]
        )

    def delete_tasks(self, list_of_tasks: list[str]):
        """Delete the provided list of tasks.

        Parameters
        ----------
        list_of_tasks: list[str]
            List of task items.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If command_name does not match a task name. None of the tasks is deleted.
        """
        self._populate_help_string_command_id_map()
        list_of_tasks_with_display_name = []
        for task_name in list_of_tasks:
            try:
                list_of_tasks_with_display_name.append(
                    self._help_string_display_text_map[task_name]
                )
            except KeyError as ex:
                raise ValueError(
                    f"'{task_name}' is not an allowed command task.\n"
                    "Use the 'get_possible_tasks()' method to view a list of allowed command tasks."
                ) from ex

        return self._workflow.DeleteTasks(ListOfTasks=list_of_tasks_with_display_name)

    def create_composite_task(self, list_of_tasks: list[str]):
        """Create the list of tasks passed as argument.

        Parameters
        ----------
        list_of_tasks: list[str]
            List of task items.

        Returns
        -------
        None

        Raises
        ------
        RuntimeError
            If the command name does not match a task name.
        """
        self._populate_help_string_command_id_map()
        list_of_tasks_with_display_name = []
        for task_name in list_of_tasks:
            try:
                list_of_tasks_with_display_name.append(
                    self._help_string_display_text_map[task_name]
                )
            except KeyError:
                raise RuntimeError(
                    f"'{task_name}' is not an allowed command task.\n"
                    "Use the 'get_possible_tasks()' method to view a list of allowed command tasks."
                )

        return self._workflow.CreateCompositeTask(
            ListOfTasks=list_of_tasks_with_display_name
        )


class ClassicWorkflow:
    """Wraps a meshing workflow object.

    Methods
    -------
    __getattr__(attr)
    __dir__()
    __call__()
    """

    def __init__(self, workflow: PyMenuGeneric, command_source: PyMenuGeneric) -> None:
        """Initialize ClassicWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            The workflow object.
        command_source : PyMenuGeneric
            The application root for commanding.
        """
        self._workflow = workflow
        self._command_source = command_source
        self._lock = (
            threading.RLock()
        )  # TODO: sort out issues with these un-used variables.
        self._dynamic_interface = False

    @property
    def TaskObject(self) -> TaskContainer:
        # missing from dir
        """Get a TaskObject container wrapper that 'holds' the underlying TaskObjects.

        The wrapper adds extra functionality.
        """
        return TaskContainer(self)

    def __getattr__(self, attr):
        """Delegate attribute lookup to the wrapped workflow object."""
        obj = self._attr_from_wrapped_workflow(
            attr
        )  # or self._task_with_cmd_matching_help_string(attr)
        if obj:
            return obj
        else:
            return super().__getattribute__(attr)

    def __dir__(self):
        """Override the behaviour of dir to include attributes in WorkflowWrapper and
        the underlying workflow."""
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._workflow))
        )

    def __call__(self):
        """Delegate calls to the underlying workflow."""
        return self._workflow()

    def _attr_from_wrapped_workflow(self, attr):
        try:
            result = getattr(self._workflow, attr)
            if result:
                return result
        except AttributeError:
            pass


class ReadOnlyObject:
    """Removes set_state() to implement read-only behaviour."""

    _unwanted_attr = ["set_state", "setState"]

    def __init__(self, cmd):
        """Initialize this object."""
        self._cmd = cmd

    def is_read_only(self):
        """Get the read-only status of this object."""
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
