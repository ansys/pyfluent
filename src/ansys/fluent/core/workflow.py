"""Workflow module that wraps and extends the core functionality."""

from __future__ import annotations

import logging
import re
import threading
from typing import Any, Iterable, Iterator, Tuple
import warnings

from ansys.fluent.core.services.datamodel_se import (
    PyCallableStateObject,
    PyCommand,
    PyMenu,
    PyMenuGeneric,
    PySingletonCommandArgumentsSubItem,
)
from ansys.fluent.core.utils.dictionary_operations import get_first_dict_key_for_value
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.warnings import PyFluentDeprecationWarning, PyFluentUserWarning


class CommandInstanceCreationError(RuntimeError):
    """Raised when an attempt to create an instance of a task command fails."""

    def __init__(self, task_name):
        """Initialize CommandInstanceCreationError."""
        super().__init__(f"Could not create command instance for task {task_name}.")


def camel_to_snake_case(camel_case_str: str) -> str:
    """Convert camel case input string to snake case output string."""
    try:
        return camel_to_snake_case.cache[camel_case_str]
    except KeyError:
        if not camel_case_str.islower():
            _snake_case_str = (
                re.sub(
                    "((?<=[a-z])[A-Z0-9]|(?!^)[A-Z](?=[a-z0-9]))",
                    r"_\1",
                    camel_case_str,
                )
                .lower()
                .replace("__", "_")
            )
        else:
            _snake_case_str = camel_case_str
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
    task_cmd_name = task.CommandName()
    cmd_creator = getattr(session, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.create_instance()
        if new_cmd:
            return new_cmd
    raise CommandInstanceCreationError(task._name_())


def _init_task_accessors(obj):
    logger.debug("_init_task_accessors")
    logger.debug(f"thread ID in _init_task_accessors {threading.get_ident()}")
    for task in obj.tasks(recompute=True):
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
    tasks = obj.tasks(recompute=True)
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


def _call_refresh_task_accessors(obj):
    """This layer handles exception for PyConsole."""
    try:
        _refresh_task_accessors(obj)
    except Exception:
        # Is there a more specific Exception derived class
        # for which we know it is correct to pass?
        pass


def _convert_task_list_to_display_names(workflow_root, task_list):
    if workflow_root.service.cache is not None:
        workflow_state = workflow_root.service.cache.get_state(
            "workflow", workflow_root
        )
        return [workflow_state[f"TaskObject:{x}"]["_name_"] for x in task_list]
    else:
        _display_names = []
        for _task_name in task_list:
            name_obj = PyMenu(
                service=workflow_root.service,
                rules=workflow_root.rules,
                path=[("TaskObject", _task_name), ("_name_", "")],
            )
            _display_names.append(name_obj())
        return _display_names


class BaseTask:
    """Base class Task representation for wrapping a Workflow TaskObject instance,
    adding methods to discover more about the relationships between TaskObjects.

    Methods
    -------
    get_direct_upstream_tasks()
    get_direct_downstream_tasks()
    tasks()
    inactive_tasks()
    get_id()
    get_idx()
    __getattr__(attr)
    __setattr__(attr, value)
    __dir__()
    __call__()
    """

    def __init__(
        self,
        command_source: Workflow,
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
                _python_task_names_map={},
                _lock=command_source._lock,
                _ordered_children=[],
                _task_list=[],
                _task_objects={},
                _fluent_version=command_source._fluent_version,
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

    def mark_as_updated(self) -> None:
        """Mark tasks in workflow as updated."""
        state = getattr(self, "state", None)
        if state and "Forced-up-to-date" in state.allowed_values():
            state.set_state("Forced-up-to-date")

    def tasks(self, recompute=True) -> list:
        """Get the ordered task list held by this task.

        This method sort tasks in terms of the workflow order and only includes this task's top-level tasks.
        You can obtain other tasks by calling the ``tasks()`` method on a parent task.

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

    def task_names(self):
        """Get the list of the Python names for the available tasks."""
        return [child.python_name() for child in self.tasks()]

    def inactive_tasks(self) -> list:
        """Get the inactive ordered child list.

        Returns
        -------
        list
            Inactive ordered children.
        """
        return []

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

    def _populate_duplicate_task_list(self):
        disp_text = self.display_name()
        if disp_text.split()[-1].isdigit():
            new_task = "".join(disp_text.rsplit(f" {disp_text.split()[-1]}", 1))
            if (
                new_task
                == self._command_source._python_name_display_text_map[self._python_name]
            ):
                self._python_name = self._python_name + f"_{disp_text.split()[-1]}"
                self._command_source._python_name_display_text_map[
                    self._python_name
                ] = disp_text
                self._command_source._repeated_task_python_name_display_text_map[
                    self._python_name
                ] = disp_text

    def python_name(self) -> str:
        """Get the Pythonic name of this task from the underlying application.

        Returns
        -------
        str
            Pythonic name of the task.
        """
        if not self._python_name:
            if self._command_source._dynamic_python_names:
                display_name_map = self._command_source._python_name_display_text_map
                if self.display_name() not in display_name_map.values():
                    self._set_python_name()
                else:
                    self._python_name = get_first_dict_key_for_value(
                        display_name_map, self.display_name()
                    )
            else:
                self._set_python_name()

        return self._python_name

    def _set_python_name(self):
        this_command = self._command()
        self._python_name = camel_to_snake_case(
            this_command.get_attr("APIName") or this_command.get_attr("helpString")
        )
        self._cache_data(this_command)

    def _cache_data(self, command):
        disp_text = command.get_attr("displayText")
        if self._python_name in self._command_source._python_name_display_text_map:
            self._populate_duplicate_task_list()
        else:
            self._command_source._python_name_display_text_map[self._python_name] = (
                self.display_name()
                if self._command_source._dynamic_python_names
                else disp_text
            )
        self._command_source._python_name_command_id_map[self._python_name] = (
            command.command
        )
        self._command_source._python_name_display_id_map[self._python_name] = disp_text

    def _get_camel_case_arg_keys(self):
        args = self.arguments
        camel_args = []
        for arg in args().keys():
            camel_args.append(args._snake_to_camel_map[arg])

        return camel_args

    def __getattr__(self, attr):
        result = getattr(self._task, attr, None)
        if result:
            return result
        if not attr.islower() and attr != "Arguments":
            raise AttributeError(
                "Camel case attribute access is not supported. "
                f"Try using '{camel_to_snake_case(attr)}' instead."
            )
        camel_attr = (
            snake_to_camel_case(
                str(attr), [*self._get_camel_case_arg_keys(), *dir(self._task)]
            )
            if attr.islower()
            else attr
        )
        attr = camel_attr or attr
        result = getattr(self._task, attr, None)
        if result:
            return result
        try:
            return ArgumentWrapper(self, attr)
        except Exception as ex:
            logger.debug(str(ex))
        result = self._task_objects.get(attr, None)
        if result:
            return result
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        logger.debug(f"BaseTask.__setattr__({attr}, {value})")
        if attr in self.__dict__:
            self.__dict__[attr] = value
        elif attr in self.arguments() or attr == "arguments":
            getattr(self, attr).set_state(value)
        else:
            setattr(self._task, attr, value)

    def __dir__(self):
        arg_list = []
        for arg in [*self._get_camel_case_arg_keys(), *dir(self._task)]:
            arg_list.append(camel_to_snake_case(arg))

        return sorted(set(list(self.__dict__.keys()) + dir(type(self)) + arg_list))

    def delete(self) -> None:
        """Delete this task from the workflow."""
        self._command_source.delete_tasks(list_of_tasks=[self.python_name()])

    def rename(self, new_name: str):
        """Rename the current task to a given name."""
        self._command_source._dynamic_python_names = True
        py_name = self.python_name()
        if py_name in self._command_source._repeated_task_python_name_display_text_map:
            self._command_source._python_name_command_id_map[new_name] = (
                self._command_source._python_name_command_id_map.pop(py_name, None)
            )
            self._command_source._python_name_display_id_map[new_name] = (
                self._command_source._python_name_display_id_map.pop(py_name, None)
            )
            self._command_source._python_name_display_text_map.pop(py_name, None)
            self._command_source._repeated_task_python_name_display_text_map.pop(
                py_name, None
            )
        else:
            self._command_source._python_name_command_id_map[new_name] = (
                self._command_source._python_name_command_id_map[py_name]
            )
            self._command_source._python_name_display_id_map[new_name] = (
                self._command_source._python_name_display_id_map[py_name]
            )
            self._command_source._python_name_display_text_map.pop(py_name, None)

        self._command_source._python_name_display_text_map[new_name] = new_name
        self._command_source._repeated_task_python_name_display_text_map[new_name] = (
            new_name
        )
        self._python_name = new_name
        return self._task.Rename(NewName=new_name)

    def add_child_to_task(self):
        """Add a child task."""
        return self._task.AddChildToTask()

    def update_child_tasks(self, setup_type_changed: bool):
        """Update child tasks."""
        self._task.UpdateChildTasks(SetupTypeChanged=setup_type_changed)

    def _get_next_python_task_names(self) -> list[str]:
        self._python_task_names_map = {}
        for command_name in self._task.GetNextPossibleTasks():
            comm_obj = getattr(
                self._command_source._command_source, command_name
            ).create_instance()
            self._python_task_names_map[
                camel_to_snake_case(
                    comm_obj.get_attr("APIName") or comm_obj.get_attr("helpString")
                )
            ] = command_name
        return list(self._python_task_names_map.keys())

    def _insert_next_task(self, task_name: str):
        """Insert a task based on the Python name after the current task is executed.

        Parameters
        ----------
        task_name: str
            Python name of the new task.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the Python name does not match the next possible task names.
        """
        self._command_source._dynamic_python_names = True
        if task_name not in self._get_next_python_task_names():
            raise ValueError(
                f"'{task_name}' cannot be inserted next to '{self.python_name()}'."
            )
        self._task.InsertNextTask(CommandName=self._python_task_names_map[task_name])
        _call_refresh_task_accessors(self._command_source)

    @property
    def insertable_tasks(self):
        """Tasks that can be inserted after the current task."""
        return self._NextTask(self)

    class _NextTask:
        def __init__(self, base_task):
            """Initialize an ``_NextTask`` instance."""
            self._base_task = base_task
            self._insertable_tasks = []
            for item in self._base_task._get_next_python_task_names():
                insertable_task = type("Insert", (self._Insert,), {})(
                    self._base_task, item
                )
                setattr(self, item, insertable_task)
                self._insertable_tasks.append(insertable_task)

        def __call__(self):
            return self._insertable_tasks

        class _Insert:
            def __init__(self, base_task, name):
                """Initialize an ``_Insert`` instance."""
                self._base_task = base_task
                self._name = name

            def insert(self):
                """Insert a task in the workflow."""
                return self._base_task._insert_next_task(task_name=self._name)

            def __repr__(self):
                return f"<Insertable '{self._name}' task>"

    def __call__(self, **kwds) -> Any:
        if kwds:
            self._task.Arguments.set_state(**kwds)
        result = self._task.Execute()
        _call_refresh_task_accessors(self._command_source)
        return result

    def _tasks_with_matching_attributes(self, attr: str, other_attr: str) -> list:
        this_command = self._command()
        attrs = this_command.get_attr(attr)
        if not attrs:
            return []
        attrs = set(attrs)
        tasks = [
            task for task in self._command_source.tasks() if task.name() != self.name()
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
        for name in self.get_object_names():
            yield self[name]

    def __getitem__(self, name):
        logger.debug(f"TaskContainer.__getitem__({name})")
        return self._container._workflow.TaskObject[name]

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
                _snake_to_camel_map={},
            )
        )

    def set_state(self, args: dict) -> None:
        """Overwrite arguments.

        Parameters
        ----------
        args : dict
            State of the arguments.

        Raises
        ------
        ValueError
            If input is invalid.
        """
        self._assign(args, "set_state")

    def update_dict(self, args: dict) -> None:
        """Merge with arguments.

        Parameters
        ----------
        args : dict
            State of the arguments.

        Raises
        ------
        ValueError
            If input is invalid.
        """
        self._assign(args, "update_dict")

    def _camel_snake_arguments_map(self, input_dict, cmd_args=None):
        snake_case_state_dict = {}
        cmd_args = self._task._command_arguments if cmd_args is None else cmd_args
        for key, val in input_dict.items():
            self._snake_to_camel_map[camel_to_snake_case(key)] = key
            if isinstance(
                getattr(cmd_args, key),
                PySingletonCommandArgumentsSubItem,
            ):
                snake_case_state_dict[camel_to_snake_case(key)] = (
                    self._camel_snake_arguments_map(val)
                )
            else:
                snake_case_state_dict[camel_to_snake_case(key)] = val
        return snake_case_state_dict

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

        return self._camel_snake_arguments_map(state_dict)

    def _assign(self, args: dict, fn) -> None:
        # This function sets the task arguments' state, either via update_dict()
        # or set_state(). Datamodel dicts are not subject to rules at the
        # key-value level. In order to trigger rules validation, it's necessary
        # to apply the arguments' state to the actual command, and that is what
        # we do here. If the introduced arguments' state is invalid, we leave the
        # target state unaffected (by repairing it) and throw an exception.
        try:
            # We get the initial state for exception safety, but this also
            # has the positive side effect of populating the name map.
            # So, if this initial state access is removed then we must ensure
            # that we still populate that map. But we can also optimise by keeping
            # a global map and only fetching the remote state for unpopulated
            # paths. Furthermore we can generate all name information statically,
            # avoiding remote trips for such purposes. In order to avoid the initial
            # get_state (to support exception safety), we could optionally return the
            # current state from the prior set_state invocation.
            old_state = self.get_state()
        except Exception:
            old_state = None
        camel_args = {}
        # TODO: Figure out proper way to implement "add_child".
        if "add_child" in args:
            self._snake_to_camel_map["add_child"] = "AddChild"

        cmd_args = self._task._command_arguments
        for key, val in args.items():
            camel_arg = self._snake_to_camel_map[key] if key.islower() else key
            # TODO: Implement enhanced meshing workflow to hide away internal info.
            if isinstance(
                getattr(cmd_args, camel_arg), PySingletonCommandArgumentsSubItem
            ):
                updated_dict = {}
                for attr, attr_val in val.items():
                    camel_attr = snake_to_camel_case(
                        str(attr),
                        getattr(
                            self, camel_to_snake_case(key)
                        )._get_camel_case_arg_keys()
                        or [],
                    )
                    updated_dict[camel_attr] = attr_val
                camel_args[camel_arg] = updated_dict
            else:
                camel_args[camel_arg] = val
        if fn == "update_dict":
            self._task.Arguments.update_dict(camel_args, recursive=True)
        else:
            getattr(self._task.Arguments, fn)(camel_args)
        try:
            self._refresh_command_after_changing_args(old_state)
        except Exception as ex:
            raise ValueError(
                "Invalid task arguments, {args} for '{self._task.python_name()}'."
            ) from ex

    def _refresh_command_after_changing_args(self, recovery_state) -> None:
        try:
            self._task._refreshed_command()()
        except Exception as ex:
            self._just_set_state(recovery_state)
            try:
                self._task._refreshed_command()()
            except Exception:
                pass
            raise ex

    def _just_set_state(self, args):
        camel_args = {}
        if isinstance(args, dict):
            for key, val in args.items():
                camel_args[self._snake_to_camel_map[key]] = val
        self._task.Arguments.set_state(camel_args)

    def __getattr__(self, attr):
        return getattr(self._task, attr)

    def __setattr__(self, key, value):
        try:
            getattr(self, key).set_state(value)
        except AttributeError:
            raise AttributeError(
                f"No attribute named '{key}' in '{self._task.name()}'."
            )

    def __setitem__(self, key, value):
        getattr(self._task, key).set_state(value)

    def __getitem__(self, item):
        return getattr(self._task, item).get_state()


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
        self._task.arguments.update_dict({self._arg_name: value})

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

        if isinstance(self._arg, PySingletonCommandArgumentsSubItem):
            snake_case_state_dict = {}
            for key, val in state_dict.items():
                self._snake_to_camel_map[camel_to_snake_case(key)] = key
                snake_case_state_dict[camel_to_snake_case(key)] = val
            return snake_case_state_dict

        return state_dict

    def _get_camel_case_arg_keys(self):
        if not isinstance(self(), dict):
            return
        _args = self
        _camel_args = []
        for arg in _args().keys():
            try:
                _camel_args.append(self._snake_to_camel_map[arg])
            except KeyError:
                _camel_args.append(arg)

        return _camel_args

    def __getattr__(self, attr):
        if not attr.islower():
            raise AttributeError(
                "Camel case attribute access is not supported. "
                f"Try using '{camel_to_snake_case(attr)}' instead."
            )
        camel_attr = snake_to_camel_case(
            str(attr), self._get_camel_case_arg_keys() or []
        )
        attr = camel_attr or attr
        return getattr(self._arg, attr)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            self.set_state({attr: value})

    def __dir__(self):
        arg_state = self.get_state()
        arg_list = list(arg_state) if isinstance(arg_state, dict) else []
        dir_arg = [item for item in dir(self._arg) if item.islower()]
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + arg_list + dir_arg)
        )


class CommandTask(BaseTask):
    """Intermediate base class task representation for wrapping a Workflow TaskObject
    instance, adding attributes related to commanding.

    Classes without these attributes cannot be commanded.
    """

    def __init__(
        self,
        command_source: Workflow,
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
        warnings.warn("CommandArguments", PyFluentDeprecationWarning)
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
            if isinstance(value, dict):
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
        command_source: Workflow,
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

    def tasks(self, recompute=True) -> list:
        """Get the ordered task list held by the workflow.

        SimpleTasks have no TaskList.
        """
        return []


class CompoundChild(SimpleTask):
    """Compound Child representation for wrapping a Workflow TaskObject instance of
    TaskType Compound Child."""

    def __init__(
        self,
        command_source: Workflow,
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
        """Get the Pythonic name of this task.

        Returns
        -------
        str
            Pythonic name of the task.
        """
        if not self._python_name:
            self._python_name = self._get_python_names_for_compound_child()
        return self._python_name

    def _get_python_names_for_compound_child(self):
        if self._command_source._parent_of_compound_child:
            return (
                self._command_source._parent_of_compound_child
                + "_child_"
                + str(
                    self._command_source._compound_child_map[
                        self._command_source._parent_of_compound_child
                    ]
                )
            )


class CompositeTask(BaseTask):
    """Composite task representation for wrapping a Workflow TaskObject instance of
    TaskType Composite."""

    def __init__(
        self,
        command_source: Workflow,
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
        warnings.warn("CommandArguments", PyFluentDeprecationWarning)
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
        """Insert a composite child task based on the Python name."""
        return self._task.InsertCompositeChildTask(CommandName=command_name)


class ConditionalTask(CommandTask):
    """Conditional task representation for wrapping a Workflow TaskObject instance of
    TaskType Conditional."""

    def __init__(
        self,
        command_source: Workflow,
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

    def inactive_tasks(self) -> list:
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
        command_source: Workflow,
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

    def _add_child(self, state: dict | None = None) -> None:
        """Add a child to this CompoundTask.

        Parameters
        ----------
        state : dict | None
            Optional state.
        """
        state = state or {}
        state.update({"add_child": "yes"})
        self.arguments.update_dict(state)

    def insert_compound_child_task(self):
        """Insert a compound child task."""
        return self.add_child_and_update()

    def add_child_and_update(self, state=None, defer_update=None):
        """Add a child to this CompoundTask and update.

        Parameters
        ----------
        state : dict | None
            Optional state.
        defer_update : bool, default: False
            Whether to defer the update.
        """
        self._add_child(state)
        py_name = self.python_name()
        if py_name not in self._command_source._compound_child_map:
            self._command_source._compound_child_map[py_name] = 1
        else:
            self._command_source._compound_child_map[py_name] = (
                self._command_source._compound_child_map[py_name] + 1
            )
        self._command_source._compound_child = True
        self._command_source._parent_of_compound_child = py_name
        try:
            if self._fluent_version >= FluentVersion.v241:
                if defer_update is None:
                    defer_update = False
                self._task.AddChildAndUpdate(DeferUpdate=defer_update)
            else:
                if defer_update is not None:
                    warnings.warn(
                        "The 'defer_update()' method is supported in Fluent 2024 R1 and later.",
                        PyFluentUserWarning,
                    )
                self._task.AddChildAndUpdate()
        finally:
            self._command_source._compound_child = False
        return self.last_child()

    def last_child(self) -> BaseTask:
        """Get the last child of this CompoundTask and set their Python name.

        Returns
        -------
        BaseTask
            the last child of this CompoundTask
        """
        children = self.tasks()
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
            return next(filter(lambda t: t.name() == name, self.tasks()))
        except StopIteration:
            pass


def _makeTask(command_source, name: str) -> BaseTask:
    task = command_source._workflow.TaskObject[name]
    kinds = {
        "Simple": SimpleTask,
        "Compound Child": CompoundChild,
        "Compound": CompoundTask,
        "Composite": CompositeTask,
        "Conditional": ConditionalTask,
    }
    task_type = task.TaskType()
    if task_type is None:
        if command_source._compound_child:
            kind = CompoundChild
        else:
            kind = SimpleTask
    else:
        kind = kinds[task_type]
    if not kind:
        message = (
            "Unhandled empty workflow task type."
            if not task_type
            else f"Unhandled workflow task type, {task_type}."
        )
        raise RuntimeError(message)
    return kind(command_source, task)


class Workflow:
    """Wraps a workflow object, adding methods to discover more about the relationships
    between task objects.

    Methods
    -------
    tasks()
    __getattr__(attr)
    __dir__()
    __call__()
    """

    _root_affected_cb_by_server = {}

    def __init__(
        self,
        workflow: PyMenuGeneric,
        command_source: PyMenuGeneric,
        fluent_version: FluentVersion,
    ) -> None:
        """Initialize WorkflowWrapper.

        Parameters
        ----------
        workflow : PyMenuGeneric
            The workflow object.
        command_source : PyMenuGeneric
            The application root for commanding.
        """
        self.__dict__.update(
            dict(
                _workflow=workflow,
                _command_source=command_source,
                _python_task_names=[],
                _lock=threading.RLock(),
                _refreshing=False,
                _dynamic_python_names=False,
                _refresh_count=0,
                _ordered_children=[],
                _task_list=[],
                _getattr_recurse_depth=0,
                _main_thread_ident=None,
                _task_objects={},
                _python_name_command_id_map={},
                _python_name_display_id_map={},
                _python_name_display_text_map={},
                _repeated_task_python_name_display_text_map={},
                _initial_task_python_names_map={},
                _parent_of_compound_child=None,
                _compound_child_map={},
                _compound_child=False,
                _unwanted_attrs={
                    "reset_workflow",
                    "initialize_workflow",
                    "load_workflow",
                    "insert_new_task",
                    "create_composite_task",
                    "create_new_workflow",
                    "rules",
                    "service",
                    "task_object",
                    "workflow",
                },
                _fluent_version=fluent_version,
            )
        )

    def task(self, name: str) -> BaseTask:
        """Get a TaskObject by name, in a ``BaseTask`` wrapper.

        The wrapper adds extra functionality.

        Parameters
        ----------
        name : str
            Task name - the display name, not the internal ID.
        Returns
        -------
        BaseTask
            wrapped task object.
        """
        py_name = self.tasks()[
            [repr(task) for task in self.tasks()].index(repr(self._task(name)))
        ].python_name()
        warnings.warn(
            f"'task' is deprecated -> Use '{py_name}' instead.",
            PyFluentDeprecationWarning,
        )
        return self._task(name)

    def _task(self, name: str) -> BaseTask:
        """Get a TaskObject by name, in a ``BaseTask`` wrapper.

        The wrapper adds extra functionality.

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

    def tasks(self, recompute=True) -> list:
        """Get the ordered task list held by the workflow.

        This method sort tasks in terms of the workflow order and only includes this task's top-level tasks.
        You can obtain other tasks by calling the ``tasks()`` method on a parent task.

        Consider the following workflow.

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

    @staticmethod
    def inactive_tasks() -> list:
        """Get the inactive ordered task list held by this task.

        Returns
        -------
        list
            Inactive ordered children.
        """
        return []

    def __getattr__(self, attr):
        """Delegate attribute lookup to the wrapped workflow object."""
        if attr in self._repeated_task_python_name_display_text_map:
            return self._task(self._repeated_task_python_name_display_text_map[attr])
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
            try:
                return getattr(self._workflow, attr)
            except AttributeError:
                pass
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
        elif attr in self._task_objects:
            self._task_objects[attr].set_state(value)
        else:
            super().__setattr__(attr, value)

    def __dir__(self):
        """Override the behavior of ``dir`` to include attributes in the
        ``WorkflowWrapper`` class and the underlying workflow."""
        arg_list = [camel_to_snake_case(arg) for arg in dir(self._workflow)]
        dir_set = set(
            list(self.__dict__)
            + dir(type(self))
            + arg_list
            + self.task_names()
            + list(self._repeated_task_python_name_display_text_map)
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
        return self._task(task_state["_name_"])

    def _task_by_id(self, task_id):
        workflow_state = self._workflow_state()
        return self._task_by_id_impl(task_id, workflow_state)

    def _activate_dynamic_interface(self, dynamic_interface: bool):
        self._initialize_methods(dynamic_interface=dynamic_interface)

    def _unsubscribe_root_affected_callback(self):
        if self._workflow.service in self._root_affected_cb_by_server:
            self._root_affected_cb_by_server[self._workflow.service].unsubscribe()
            self._root_affected_cb_by_server.pop(self._workflow.service)

    def _new_workflow(self, name: str, dynamic_interface: bool = True):
        self._workflow.InitializeWorkflow(WorkflowType=name)
        self._activate_dynamic_interface(dynamic_interface=dynamic_interface)

    def _load_workflow(self, file_path: str, dynamic_interface: bool = True):
        self._workflow.LoadWorkflow(FilePath=file_path)
        self._activate_dynamic_interface(dynamic_interface=dynamic_interface)

    def _get_initial_task_list_while_creating_new_workflow(self):
        """Get a list of independent tasks that can be inserted at the initial level
        while creating a workflow."""
        self._populate_first_tasks_python_name_command_id_map()
        return list(self._initial_task_python_names_map)

    def _create_workflow(self, dynamic_interface: bool = True):
        self._workflow.CreateNewWorkflow()
        self._activate_dynamic_interface(dynamic_interface=dynamic_interface)

    @property
    def insertable_tasks(self):
        """Tasks that can be inserted on a blank workflow."""
        return self._FirstTask(self)

    class _FirstTask:
        def __init__(self, workflow):
            """Initialize an ``_FirstTask`` instance."""
            self._workflow = workflow
            self._insertable_tasks = []
            if len(self._workflow.task_names()) == 0:
                for (
                    item
                ) in (
                    self._workflow._get_initial_task_list_while_creating_new_workflow()
                ):
                    insertable_task = type("Insert", (self._Insert,), {})(
                        self._workflow, item
                    )
                    setattr(self, item, insertable_task)
                    self._insertable_tasks.append(insertable_task)

        def __call__(self):
            return self._insertable_tasks

        class _Insert:
            def __init__(self, workflow, name):
                """Initialize an ``_Insert`` instance."""
                self._workflow = workflow
                self._name = name

            def insert(self):
                """Insert a task in the workflow."""
                return self._workflow._workflow.InsertNewTask(
                    CommandName=self._workflow._initial_task_python_names_map[
                        self._name
                    ]
                )

            def __repr__(self):
                return f"<Insertable '{self._name}' task>"

    def _populate_first_tasks_python_name_command_id_map(self):
        if not self._initial_task_python_names_map:
            for command in dir(self._command_source):
                if command in ["SwitchToSolution", "set_state"]:
                    continue
                command_obj = getattr(self._command_source, command)
                if isinstance(command_obj, PyCommand):
                    command_obj_instance = command_obj.create_instance()
                    if not command_obj_instance.get_attr("requiredInputs"):
                        help_str = command_obj_instance.get_attr(
                            "APIName"
                        ) or command_obj_instance.get_attr("helpString")
                        if help_str:
                            self._initial_task_python_names_map[help_str] = command
                    del command_obj_instance

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
                _call_refresh_task_accessors(self)
                self._refresh_count += 1
                self._refreshing = False

            self._root_affected_cb_by_server[self._workflow.service] = (
                self.add_on_affected(refresh_after_sleep)
            )

    def save_workflow(self, file_path: str):
        """Save the current workflow to the location provided."""
        self._workflow.SaveWorkflow(FilePath=file_path)

    def load_state(self, list_of_roots: list):
        """Load the state of the workflow."""
        self._workflow.LoadState(ListOfRoots=list_of_roots)

    def task_names(self):
        """Get the list of the Python names for the available tasks."""
        return [child.python_name() for child in self.tasks()]

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
            If 'task' does not match a task name, no tasks are deleted.
        """
        list_of_tasks_with_display_name = []
        for task_name in list_of_tasks:
            try:
                list_of_tasks_with_display_name.append(
                    self._python_name_display_id_map[task_name]
                )
                self._python_name_display_text_map.pop(task_name, None)
                if task_name in self._repeated_task_python_name_display_text_map:
                    self._python_name_command_id_map.pop(task_name, None)
                    self._python_name_display_id_map.pop(task_name, None)
                self._repeated_task_python_name_display_text_map.pop(task_name, None)
            except KeyError as ex:
                raise ValueError(
                    f"'{task_name}' is not an allowed task.\n"
                    "Use the 'task_names()' method to view a list of allowed tasks."
                ) from ex

        return self._workflow.DeleteTasks(ListOfTasks=list_of_tasks_with_display_name)


class ClassicWorkflow:
    """Wraps a meshing workflow object.

    Methods
    -------
    __getattr__(attr)
    __dir__()
    __call__()
    """

    def __init__(
        self,
        workflow: PyMenuGeneric,
        command_source: PyMenuGeneric,
        fluent_version: FluentVersion,
    ) -> None:
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
        self._fluent_version = fluent_version

    @property
    def TaskObject(self) -> TaskContainer:
        # missing from dir
        """Get a TaskObject container wrapper that 'holds' the underlying TaskObjects.

        The wrapper adds extra functionality.
        """
        return TaskContainer(self)

    def __getattr__(self, attr):
        """Delegate attribute lookup to the wrapped workflow object."""
        try:
            return getattr(self._workflow, attr)
        except AttributeError:
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


class ReadOnlyObject:
    """Removes ``set_state()`` to implement read-only behavior."""

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
