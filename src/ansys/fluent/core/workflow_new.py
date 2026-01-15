# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Workflow module that wraps and extends the core functionality.

This module provides a high-level, Pythonic interface for working with Ansys Fluent
workflows. It wraps the underlying datamodel service layer to provide intuitive
navigation, task management, and workflow operations.

The main classes are:

- **Workflow**: Top-level workflow container that manages tasks and provides
  navigation between them.
- **TaskObject**: Individual task wrapper that provides access to task properties,
  arguments, execution, and navigation to sibling/child tasks.


Notes
-----
This module is designed for Fluent 26R1 and later versions. Some features may not
be available in earlier versions.

The workflow system provides both imperative and declarative approaches to building
simulation workflows, with automatic dependency management and validation.
"""

from __future__ import annotations

from collections import OrderedDict
import re
from typing import ValuesView

from ansys.fluent.core.services.datamodel_se import PyMenu
from ansys.fluent.core.utils.fluent_version import FluentVersion


def _get_task_type_name(task_obj: PyMenu) -> str:
    """Extract the task type name from a task object's class name.

    The datamodel generates task classes with leading underscores (e.g., "_import_geometry").
    This function strips the leading underscore to get the clean task type name.

    Parameters
    ----------
    task_obj : PyMenu
        The task datamodel object.

    Returns
    -------
    str
        Clean task type name without leading underscore (e.g., "import_geometry").

    Notes
    -----
    This is needed because the datamodel service generates class names with a leading
    underscore convention (e.g., `_import_geometry`), but we want clean names for
    internal use and type creation.
    """
    return task_obj.__class__.__name__.lstrip("_")


def is_compound_child(task_type: str) -> bool:
    """Check if a task type represents a compound child task. This encapsulates
    a string comparison to avoid repetition.

    Parameters
    ----------
    task_type : str
        The task type string to check.

    Returns
    -------
    bool
        True if the task type is "Compound Child", False otherwise.
    """
    return task_type == "Compound Child"


def _convert_task_list_to_display_names(
    workflow_root: PyMenu, task_list: list[str]
) -> list[str]:
    """Convert a list of task IDs to their corresponding display names.

    Parameters
    ----------
    workflow_root : PyMenu
        The root workflow datamodel object that provides service access.
    task_list : list[str]
        List of internal task identifiers (e.g., ["TaskObject1", "TaskObject2"]).

    Returns
    -------
    list[str]
        List of display names corresponding to the task IDs
        (e.g., ["Import Geometry", "Add Local Sizing"]).
    """
    _display_names = []
    for _task_name in task_list:
        name_obj = PyMenu(
            service=workflow_root.service,
            rules=workflow_root.rules,
            path=[("task_object", _task_name), ("_name_", "")],
        )
        _display_names.append(name_obj.get_remote_state())
    return _display_names


def _get_child_task_by_task_id(workflow_root, task_id):
    """Get a child task's display name by its internal task ID.

    Parameters
    ----------
    workflow_root : PyMenu
        The root workflow datamodel object.
    task_id : str
        Internal identifier for the task (e.g., "TaskObject1").

    Returns
    -------
    str
        The display name of the task (e.g., "Import Geometry").
    """
    return PyMenu(
        service=workflow_root.service,
        rules=workflow_root.rules,
        path=[("task_object", task_id), ("_name_", "")],
    ).get_remote_state()


def command_name_to_task_name(meshing_root, command_name: str) -> str:
    """Convert a command name to its corresponding task display name.

    This function maps internal command names (used by the Fluent core) to
    user-facing task names.

    Parameters
    ----------
    meshing_root : PyMenu
        The root meshing datamodel object.
    command_name : str
        Internal command name (e.g., "ImportGeometry").

    Returns
    -------
    str
        User-facing task name (e.g., "import_geometry").

    Notes
    -----
    This is a workaround for Fluent 26R1.
    """
    # TODO: This fix is applicable till the server lacks the mechanism to return mapped values
    #  for '<Task Object>.get_next_possible_tasks()' and
    #  for '<Workflow>.get_new_insertable_tasks()'.
    command_instance = getattr(meshing_root, command_name).create_instance()
    return command_instance.get_attr("APIName") or command_instance.get_attr(
        "helpString"
    )


class Workflow:
    """High-level workflow container that manages tasks and provides navigation.

    The Workflow class wraps the underlying datamodel workflow object and provides
    a Pythonic interface for:

    - Discovering and accessing tasks
    - Creating, loading, and saving workflows
    - Navigating task hierarchies
    - Managing task lifecycles (creation/deletion)
    """

    def __init__(
        self,
        workflow: PyMenu,
        command_source: PyMenu,
        fluent_version: FluentVersion,
    ) -> None:
        """Initialize Workflow."""
        self._workflow = workflow
        self._command_source = command_source
        self._fluent_version = fluent_version
        self._task_dict = {}
        self._compound_child_dict = {}

    def tasks(self) -> ValuesView[PyMenu]:
        """Get the complete list of tasks in the workflow.

        This method builds and returns a comprehensive list of all task objects
        currently present in the workflow, including:

        - Top-level tasks
        - Compound child tasks (tasks with multiple instances)
        - Dynamically created tasks

        The method rebuilds its internal task cache on each call to ensure
        freshness, though this can be expensive for large workflows.
        """
        self._task_dict = {}
        _state = self._workflow.task_object()
        for task in sorted(_state):
            name, display_name = task.split(":")
            task_obj = getattr(self._workflow.task_object, name)[display_name]
            if is_compound_child(task_obj.task_type()):
                if name not in self._compound_child_dict:
                    # CASE 1: First instance of this compound child type
                    # ===================================================
                    # This is the first time we've seen this task type (e.g., "add_boundary_layers")
                    # Create a new entry in the compound child dictionary with the first child
                    #
                    # Example: For "Boundary Layer 1" task with name="add_boundary_layers"
                    # Creates: {"add_boundary_layers": {"add_boundary_layers_child_1": task_obj}}
                    self._compound_child_dict[name] = {
                        name + "_child_1": task_obj,
                    }
                else:
                    # CASE 2: Subsequent instance of this compound child type
                    # ========================================================
                    # We've already seen this task type before. Now we need to determine if this
                    # specific task instance is new or if we've already processed it.
                    #
                    # Why check for duplicates?
                    # The workflow datamodel may return the same task multiple times during iteration,
                    # so we need to verify this is actually a NEW instance (e.g., "Boundary Layer 2")
                    # and not a duplicate reference to an existing one (e.g., "Boundary Layer 1" again).

                    # Check if this specific task instance already exists in the compound child dict
                    # We compare by display name using task_obj._name_() which returns names like
                    # "Boundary Layer 1", "Boundary Layer 2", etc.
                    if task_obj._name_() not in (
                        value._name_()
                        for value in self._compound_child_dict[name].values()
                    ):
                        # This is genuinely a NEW instance - add it with the next available number
                        #
                        # Calculate the next child number:
                        # 1. Sort existing keys: ["add_boundary_layers_child_1", "add_boundary_layers_child_2"]
                        # 2. Take the last key: "add_boundary_layers_child_2"
                        # 3. Extract the last character (the number): "2"
                        # 4. Convert to int and add 1: 3
                        # 5. Result: "add_boundary_layers_child_3"
                        #
                        # Example progression:
                        #   First:  "add_boundary_layers_child_1" -> number is 1
                        #   Second: "add_boundary_layers_child_2" -> number is 2
                        #   Third:  "add_boundary_layers_child_3" -> number is 3
                        child_key = (
                            int(sorted(self._compound_child_dict[name])[-1][-1]) + 1
                        )
                        self._compound_child_dict[name][
                            name + f"_child_{child_key}"
                        ] = task_obj
            else:
                # Store regular (non-compound-child) tasks in the task dictionary
                if name not in self._task_dict:
                    # CASE 1: First occurrence of this task type
                    # =============================================
                    # Store using the base name (e.g., "import_geometry")
                    # This allows access via: workflow.import_geometry
                    self._task_dict[name] = task_obj
                else:
                    # CASE 2: Duplicate task type (e.g., second "Import Geometry")
                    # =============================================================
                    # Multiple tasks of the same type can exist in a workflow.
                    # Their display names have numeric suffixes: "Import Geometry 1", "Import Geometry 2"
                    #
                    # To create unique dictionary keys, we:
                    # 1. Extract the numeric suffix from the display name
                    # 2. Append it to the base name with an underscore
                    #
                    # Example transformation:
                    #   Display name: "Import Geometry 2"
                    #   Base name: "import_geometry"
                    #   Suffix: "2" (last word from display name)
                    #   Final key: "import_geometry_2"
                    #
                    # This allows access via: workflow.import_geometry_2
                    self._task_dict[name + f"_{task_obj.name().split()[-1]}"] = task_obj

        # Merge all compound child tasks into main dictionary
        for child_tasks in self._compound_child_dict.values():
            self._task_dict.update(child_tasks)

        return self._task_dict.values()

    def _workflow_state(self):
        """Get the complete state dictionary of the workflow."""
        return self._workflow()

    def _new_workflow(self, name: str):
        """Initialize a new workflow from a predefined template."""
        self._workflow.general.initialize_workflow(workflow_type=name)

    def _load_workflow(self, file_path: str):
        """Load a workflow from a saved workflow file (.wft)."""
        self._workflow.general.load_workflow(file_path=file_path)

    def _create_workflow(self):
        """Create a new empty workflow."""
        self._workflow.general.create_new_workflow()

    def save_workflow(self, file_path: str):
        """Save the current workflow to a file."""
        self._workflow.general.save_workflow(file_path=file_path)

    def load_state(self, list_of_roots: list):
        """Load the state of the workflow."""
        self._workflow.general.load_state(list_of_roots=list_of_roots)

    def task_names(self):
        """Get Python-friendly names for all available tasks.

        Returns the list of task names as they would be accessed via Python
        attribute syntax (e.g., "import_geometry" for "Import Geometry").
        """
        return [name.split(":")[0] for name in self._workflow.task_object()]

    def children(self) -> list[TaskObject]:
        """Get the top-level tasks in the workflow in display order.

        Returns an ordered list of the workflow's main tasks (those directly under
        the workflow root, not nested child tasks). The order reflects the execution
        sequence in the workflow.

        Returns
        -------
        List[TaskObject]
            Ordered list of top-level task wrappers.
        """
        ordered_names = _convert_task_list_to_display_names(
            self._workflow,
            self._workflow.general.workflow.task_list(),
        )

        # Create lightweight lookup: task name -> task datamodel object
        tasks_by_name = {task_obj.name(): task_obj for task_obj in self.tasks()}

        # Wrap only the top-level tasks in the correct order
        wrapped_tasks = []
        for name in ordered_names:
            if name in tasks_by_name:
                task_obj = tasks_by_name[name]
                wrapped = make_task_wrapper(
                    task_obj,
                    _get_task_type_name(task_obj),
                    self._workflow,
                    self,
                    self._command_source,
                )
                wrapped_tasks.append(wrapped)

        return wrapped_tasks

    def first_child(self) -> TaskObject | None:
        """Get the first top-level task in the workflow.

        Returns
        -------
        TaskObject or None
            The first task in the workflow, or None if the workflow is empty.

        Examples
        --------
        >>> first = '<workflow>'.first_child()
        >>> if first:
        ...     print(f"Starting task: {first.name()}")
        ...     first()  # Execute it

        >>> # Navigate from first to last
        >>> current = '<workflow>'.first_child()
        >>> while current and current.has_next():
        ...     print(current.name())
        ...     current()  # Execute it
        ...     current = current.next()

        Notes
        -----
        Returns None for empty workflows. Always check before accessing properties.
        """
        task_list = self._workflow.general.workflow.task_list()
        if task_list:
            first_name = _get_child_task_by_task_id(self._workflow, task_list[0])
        else:
            return None
        for task_obj in self.tasks():
            if task_obj.name() == first_name:
                return make_task_wrapper(
                    task_obj,
                    _get_task_type_name(task_obj),
                    self._workflow,
                    self,
                    self._command_source,
                )

    def last_child(self) -> TaskObject | None:
        """Get the last top-level task in the workflow.

        Returns
        -------
        TaskObject or None
            The last task in the workflow, or None if the workflow is empty.

        Examples
        --------
        >>> last = '<workflow>'.last_child()
        >>> if last:
        ...     print(f"Final task: {last.name()}")
        ...     last()  # Execute it

        >>> # Execute workflow in reverse
        >>> current = '<workflow>'.last_child()
        >>> while current and current.has_previous():
        ...     print(current.name())
        ...     current()  # Execute it
        ...     current = current.previous()
        """
        task_list = self._workflow.general.workflow.task_list()
        if task_list:
            last_name = _get_child_task_by_task_id(self._workflow, task_list[-1])
        else:
            return None
        for task_obj in self.tasks():
            if task_obj.name() == last_name:
                return make_task_wrapper(
                    task_obj,
                    _get_task_type_name(task_obj),
                    self._workflow,
                    self,
                    self._command_source,
                )

    def _task_names(self):
        """Gets a list of display names of all tasks in the workflow."""
        return _convert_task_list_to_display_names(
            self._workflow, self._workflow.general.workflow.task_list()
        )

    def _ordered_tasks(self):
        """Get ordered dictionary mapping task names to task objects."""
        ordered_names = _convert_task_list_to_display_names(
            self._workflow,
            self._workflow.general.workflow.task_list(),
        )

        # Create lightweight lookup: display name -> task datamodel object
        tasks_by_name = {task_obj.name(): task_obj for task_obj in self.tasks()}

        # Build ordered dict by wrapping only the tasks in ordered_names
        sorted_dict = OrderedDict()
        for name in ordered_names:
            if name in tasks_by_name:
                task_obj = tasks_by_name[name]
                wrapped = make_task_wrapper(
                    task_obj,
                    _get_task_type_name(task_obj),
                    self._workflow,
                    self,
                    self._command_source,
                )
                sorted_dict[name] = wrapped

        return sorted_dict

    def delete_tasks(self, list_of_tasks: list[TaskObject]):
        """Delete multiple tasks from the workflow.

        Removes the specified tasks from the workflow. Tasks are identified by TaskObject instances.

        Parameters
        ----------
        list_of_tasks: list[TaskObject]
            List of task objects to delete.

        Raises
        ------
        TypeError
            If list contains items that are neither TaskObject nor str.
        """
        items_to_be_deleted = []
        for item in list_of_tasks:
            if not isinstance(item, TaskObject):
                # This is done to support backwards compatibility.
                if isinstance(item, str):
                    items_to_be_deleted.append(item)
                else:
                    raise TypeError(
                        "'list_of_tasks' only takes list of 'TaskObject' types."
                    )
            else:
                items_to_be_deleted.append(item.name())

        self._workflow.general.delete_tasks(list_of_tasks=items_to_be_deleted)

    @property
    def insertable_tasks(self) -> FirstTask:
        """Tasks that can be inserted into an empty workflow.

        Returns a helper that exposes the set of valid starting tasks for a blank
        workflow as attributes. Each attribute is an object with an `insert()`
        method that inserts that task into the workflow.

        Notes
        -----
        - This helper only populates insertable tasks when the workflow is empty.
        - Task names are exposed using Python-friendly identifiers (snake_case).
        """
        return self.FirstTask(self)

    class FirstTask:
        """Helper exposing insertable tasks for an empty workflow.

        This container dynamically creates attributes for each command that the
        server allows as the first task in a new workflow.

        Access an attribute and call `.insert()` to insert that task.
        """

        def __init__(self, workflow):
            """Initialize a ``FirstTask`` instance."""
            self._workflow = workflow
            self._insertable_tasks: list = []
            # Map: server command name -> python-friendly task name
            self._initial_task_map: dict[str, str] = {}

            # Query server for commands that can start a new workflow.
            # Older Fluent versions don’t provide this API; use a fallback list.
            try:
                initial_tasks = self._workflow.general.get_insertable_tasks()
            except AttributeError:
                # For Fluent Version 26R1 or before.
                initial_tasks = ["ImportGeometry", "PartManagement", "RunCustomJournal"]
            for command in initial_tasks:
                self._initial_task_map[command] = command_name_to_task_name(
                    self._workflow._command_source, command
                )
            # Only expose these attributes when the workflow is empty.
            if self._workflow._workflow.general.workflow.task_list() == []:
                for command_name, python_name in self._initial_task_map.items():
                    # Build a lightweight proxy object with an insert() method.
                    insertable_task = type("Insert", (self._Insert,), {})(
                        self._workflow,
                        command_name,
                        self._initial_task_map,
                    )
                    # Expose as attribute: e.g., <workflow>.insertable_tasks.import_geometry.insert()
                    setattr(self, python_name, insertable_task)
                    self._insertable_tasks.append(insertable_task)

        def __call__(self) -> list:
            """Return all insertable task proxies as a list."""
            return self._insertable_tasks

        class _Insert:
            """Represents a single insertable starting task.

            Provides the `insert()` method to add this task to the workflow.
            """

            def __init__(self, workflow, name, task_map):
                """Initialize an _Insert instance.

                Parameters
                ----------
                workflow : Workflow
                    Target workflow.
                name : str
                    Server command name (e.g., "ImportGeometry").
                task_map : dict[str, str]
                    Mapping from server command name -> python-friendly task name.
                """
                self._workflow = workflow
                self._name = name
                self._task_map = task_map

            def insert(self) -> None:
                """Insert this task into the workflow as the first task."""
                self._workflow.general.insert_new_task(command_name=self._name)

            def __repr__(self) -> str:
                return f"<Insertable '{self._task_map[self._name]}' task>"

    def __getattr__(self, item):
        """Enable attribute-style access to tasks."""
        if item in ["parts", "parts_files"]:
            raise AttributeError(
                f"'{item}' is only supported in Fault-tolerant Meshing workflows."
            )
        if item not in self._task_dict:
            self.tasks()
        if item in self._task_dict:
            return make_task_wrapper(
                self._task_dict[item], item, self._workflow, self, self._command_source
            )
        return getattr(self._workflow, item)

    def __call__(self):
        """Get workflow state when called as a function."""
        return self._workflow_state()

    def __delattr__(self, item):
        """Delete a task using Python's del statement.

        Parameters
        ----------
        item : str
            Python attribute name of the task to delete.

        Examples
        --------
        >>> del '<workflow>'.import_geometry

        Raises
        ------
        LookupError
            If the task name is not valid.
        """
        if item not in self._task_dict:
            self.tasks()
        if item in self._task_dict:
            getattr(self, item).delete()
            del self._task_dict[item]
        else:
            raise LookupError(f"'{item}' is not a valid task name.'")


class TaskObject:
    """Wrapper for individual workflow task objects.

    TaskObject provides a high-level interface for interacting with individual
    tasks in a workflow. It exposes task properties, arguments, execution methods,
    and navigation capabilities.

    Key Features
    ------------
    - Access task arguments and properties
    - Execute tasks
    - Navigate to parent, sibling, and child tasks
    - Insert new tasks after the current task
    - Access compound child tasks (for multi-instance tasks)
    """

    def __init__(
        self,
        task_object: PyMenu,
        base_name: str,
        workflow: PyMenu,
        parent: Workflow | TaskObject,
        meshing_root: PyMenu,
    ):
        """Initialize a TaskObject wrapper.

        Parameters
        ----------
        task_object : PyMenu
            The underlying datamodel task object.
        base_name : str
            Python-friendly base name for the task.
        workflow : PyMenu
            Reference to the parent workflow datamodel.
        parent : Union[Workflow, TaskObject]
            Parent container (Workflow or parent TaskObject).

        Notes
        -----
        This constructor is called internally by `make_task_wrapper()`.
        Users should not instantiate TaskObject directly.
        """
        super().__setattr__("_task_object", task_object)
        super().__setattr__("_name", base_name)
        super().__setattr__("_workflow", workflow)
        super().__setattr__("_parent", parent)
        super().__setattr__("_meshing_root", meshing_root)
        self._cache = {}

    def _get_next_possible_tasks(self):
        """Get display names of tasks that can be inserted after this task."""
        task_obj = self._task_object
        ret_list = []
        for item in task_obj.get_next_possible_tasks():
            snake_case_name = command_name_to_task_name(self._meshing_root, item)
            if snake_case_name != item:
                self._cache[snake_case_name] = item
            ret_list.append(snake_case_name)
        return ret_list

    def _insert_next_task(self, task_name):
        """Insert a task after the current task.

        Notes
        -----
        Internal method. Users should use `insertable_tasks.<task>.insert()` instead.
        """
        self._get_next_possible_tasks()
        command_name = self._cache.get(task_name) or task_name
        self._task_object.insert_next_task(command_name=command_name)

    @property
    def insertable_tasks(self):
        """Get interface for inserting tasks after this one.

        Returns a dynamic object that exposes all valid task types that can be
        inserted after the current task. Each insertable task is accessible as
        an attribute with an `insert()` method.

        Returns
        -------
        _NextTask
            Object with attributes for each insertable task type.

        Examples
        --------
        Basic usage::

            >>> task = '<workflow>'.import_geometry
            >>>
            >>> # See what's available
            >>> available = task.insertable_tasks()
            >>> for insertable in available:
            ...     print(insertable)
            <Insertable 'import_boi_geometry' task>
            <Insertable 'set_up_rotational_periodic_boundaries' task>
            <Insertable 'create_local_refinement_regions' task>
            <Insertable 'custom_journal_task' task>

        Insert specific task::

            >>> # Insert by accessing as attribute
            >>> task.insertable_tasks.import_boi_geometry.insert()

        Access specific task after insertion::

            >>> # Access task as attribute
            >>> '<workflow>'.import_boi_geometry
        """
        return self._NextTask(self)

    class _NextTask:
        """Container for insertable task operations.

        This internal class provides a dynamic interface for task insertion.
        It creates attributes on-the-fly for each valid insertable task type.

        Attributes are created dynamically based on the result of
        `_get_next_possible_tasks()`, with each attribute being an `_Insert`
        instance that provides the `insert()` method.
        """

        def __init__(self, base_task):
            """Initialize insertable tasks container.

            Parameters
            ----------
            base_task : TaskObject
                The task after which new tasks can be inserted.
            """
            self._base_task = base_task
            self._insertable_tasks = []
            for item in self._base_task._get_next_possible_tasks():
                insertable_task = type("Insert", (self._Insert,), {})(
                    self._base_task, item
                )
                setattr(self, item, insertable_task)
                self._insertable_tasks.append(insertable_task)

        def __call__(self) -> list[_Insert]:
            """Get list of all insertable task objects.

            Returns
            -------
            List[_Insert]
                List of insertable task objects.
            """
            return self._insertable_tasks

        class _Insert:
            """Represents a single insertable task.

            Provides the `insert()` method to actually insert the task into
            the workflow after the base task.
            """

            def __init__(self, base_task, name):
                """Initialize an insertable task reference.

                Parameters
                ----------
                base_task : TaskObject
                    The task after which this will be inserted.
                name : str
                    Python friendly name of the insertable task.
                """
                self._base_task = base_task
                self._name = name

            def insert(self):
                """Insert this task into the workflow.

                Creates a new instance of this task type and inserts it
                immediately after the base task in the workflow sequence.
                """
                return self._base_task._insert_next_task(task_name=self._name)

            def __repr__(self):
                return f"<Insertable '{self._name}' task>"

    def __getattr__(self, item):
        """Enable attribute access to task properties and arguments.

        Notes
        -----
        Arguments take precedence over task object properties.
        """
        task_obj = self._task_object
        args = task_obj.arguments
        if item in args():
            return getattr(args, item)
        return getattr(task_obj, item)

    def __setattr__(self, key, value):
        """Enable attribute assignment to task arguments."""
        args = self._task_object.arguments
        if hasattr(args, key):
            setattr(args, key, value)
        else:
            super().__setattr__(key, value)

    def __call__(self):
        """Execute the task when called as a function."""
        return self._task_object.execute()

    def __getitem__(self, key):
        task_obj = self._task_object
        name = self._name
        workflow = self._workflow
        parent = self._parent
        meshing_root = self._meshing_root
        name_1 = name
        name_2 = re.sub(r"\s+\d+$", "", task_obj.name().strip()) + f" {key}"
        try:
            task_obj = getattr(workflow.task_object, name_1)[name_2]
            if is_compound_child(task_obj.task_type):
                temp_parent = self
            else:
                temp_parent = parent
            return make_task_wrapper(
                task_obj, name_1, workflow, temp_parent, meshing_root
            )
        except LookupError:
            task_obj = getattr(workflow.task_object, name_1)[key]
            if is_compound_child(task_obj.task_type):
                temp_parent = self
            else:
                temp_parent = parent
            try:
                return make_task_wrapper(
                    getattr(workflow.task_object, name_1)[key],
                    name_1,
                    workflow,
                    temp_parent,
                    meshing_root,
                )
            except LookupError as ex2:
                raise LookupError(
                    f"Neither '{name_2}' nor '{key}' found in task object '{name_1}'."
                ) from ex2

    def __delitem__(self, key):
        self[key].delete()

    def _task_names(self):
        """Gets the display names of the child tasks of a task item."""
        task_list = self._task_object.task_list()
        if task_list:
            return _convert_task_list_to_display_names(self._workflow, task_list)
        else:
            return []

    def children(self):
        """Get ordered list of direct child tasks.

        Returns
        -------
        List[TaskObject]
            Ordered list of child task wrappers, or empty list if no children.
        """
        child_names = self._task_names()
        if not child_names:
            return []

        workflow = self._workflow

        # Create reverse lookup: display name -> task type
        name_to_type = {
            display_name: task_type
            for task_type, display_name in (
                item.split(":") for item in workflow.task_object()
            )
        }

        # Build list by wrapping only the child tasks in the correct order
        wrapped_children = []
        for display_name in child_names:
            if display_name in name_to_type:
                task_type = name_to_type[display_name]
                wrapped = make_task_wrapper(
                    getattr(workflow.task_object, task_type)[display_name],
                    task_type,
                    workflow,
                    self,
                    self._meshing_root,
                )
                wrapped_children.append(wrapped)

        return wrapped_children

    def first_child(self):
        """Get the first child task of this task.

        Returns
        -------
        TaskObject or None
            The first child task, or None if no children exist.

        Examples
        --------
        >>> parent = '<workflow>'.describe_geometry
        >>> first = parent.first_child()
        >>> if first:
        ...     print(f"First child: {first.name()}")

        Navigate through children::

            >>> current = parent.first_child()
            >>> while current:
            ...     print(current.name())
            ...     if current.has_next():
            ...         current = current.next()
            ...     else:
            ...         break
        """
        task_list = self._task_names()
        if task_list:
            first_name = task_list[0]
        else:
            return None
        workflow = self._workflow

        type_to_name = {
            item.split(":")[0]: item.split(":")[-1] for item in workflow.task_object()
        }
        for key, val in type_to_name.items():
            if val == first_name:
                return make_task_wrapper(
                    getattr(workflow.task_object, key)[val],
                    key,
                    workflow,
                    self,
                    self._meshing_root,
                )

    def last_child(self):
        """Get the last child task of this task.

        Returns
        -------
        TaskObject or None
            The last child task, or None if no children exist.

        Examples
        --------
        >>> parent = '<workflow>'.describe_geometry
        >>> last = parent.last_child()
        >>> if last:
        ...     print(f"Last child: {last.name()}")
        """
        task_list = self._task_names()
        if task_list:
            last_name = task_list[-1]
        else:
            return None
        workflow = self._workflow

        type_to_name = {
            item.split(":")[0]: item.split(":")[-1] for item in workflow.task_object()
        }
        for key, val in type_to_name.items():
            if val == last_name:
                return make_task_wrapper(
                    getattr(workflow.task_object, key)[val],
                    key,
                    workflow,
                    self,
                    self._meshing_root,
                )

    @staticmethod
    def _get_next_key(input_dict, current_key):
        """Get the key that follows current_key in an ordered dictionary.

        Parameters
        ----------
        input_dict : Dict
            Ordered dictionary of tasks.
        current_key : str
            Current task name.

        Returns
        -------
        str
            Next task name.

        Raises
        ------
        IndexError
            If current_key is the last key in the dictionary.
        """
        keys = list(input_dict)
        idx = keys.index(current_key)
        if idx == len(keys) - 1:
            raise IndexError("Reached the end.")
        return keys[idx + 1]

    @staticmethod
    def _get_previous_key(input_dict, current_key):
        """Get the key that precedes current_key in an ordered dictionary.

        Parameters
        ----------
        input_dict : Dict
            Ordered dictionary of tasks.
        current_key : str
            Current task name.

        Returns
        -------
        str
            Previous task name.

        Raises
        ------
        IndexError
            If current_key is the first key in the dictionary.
        """
        keys = list(input_dict)
        idx = keys.index(current_key)
        if idx == 0:
            raise IndexError("In the beginning.")
        return keys[idx - 1]

    def has_parent(self):
        """Check if this task has a parent container.

        Returns
        -------
        bool
            True if task has a parent (Workflow or TaskObject), False otherwise.
        """
        try:
            super().__getattribute__("_parent")
            return True
        except AttributeError:
            return False

    def parent(self):
        """Get the parent container of this task.

        Returns
        -------
        Union[Workflow, TaskObject]
            The parent container. Can be:
            - Workflow instance for top-level tasks
            - TaskObject instance for nested child tasks
        """
        return self._parent

    def has_next(self) -> bool:
        """Check if there is a next sibling task.

        Determines whether this task has a sibling task that follows it in the
        workflow sequence at the same level.

        Returns
        -------
        bool
            True if a next sibling exists, False if this is the last task.
        """
        task_dict = self._parent._ordered_tasks()
        try:
            self._get_next_key(task_dict, self.name())
            return True
        except IndexError:
            return False

    def next(self):
        """Returns the next sibling task item."""
        task_dict = self._parent._ordered_tasks()
        next_key = self._get_next_key(task_dict, self.name())
        return task_dict[next_key]

    def has_previous(self) -> bool:
        """Check if there is a previous sibling task.

        Determines whether this task has a sibling task that precedes it in the
        workflow sequence at the same level.

        Returns
        -------
        bool
            True if a previous sibling exists, False if this is the first task.
        """
        task_dict = self._parent._ordered_tasks()
        try:
            self._get_previous_key(task_dict, self.name())
            return True
        except IndexError:
            return False

    def previous(self):
        """Returns the previous sibling task item."""
        task_dict = self._parent._ordered_tasks()
        previous_key = self._get_previous_key(task_dict, self.name())
        return task_dict[previous_key]

    def _ordered_tasks(self):
        if not self._task_names():
            return OrderedDict()

        workflow = self._workflow

        # Create lightweight lookup: task type -> display name
        type_to_name = dict(item.split(":") for item in workflow.task_object())

        # Get ordered list of display names for this level
        ordered_names = self._task_names()

        # Build ordered dict by wrapping only the tasks that are in ordered_names
        sorted_dict = OrderedDict()
        for display_name in ordered_names:
            # Find the matching task type for this display name
            for task_type, name in type_to_name.items():
                if name == display_name:
                    wrapped = make_task_wrapper(
                        getattr(workflow.task_object, task_type)[display_name],
                        task_type,
                        workflow,
                        self,
                        self._meshing_root,
                    )
                    sorted_dict[display_name] = wrapped
                    break

        return sorted_dict

    def delete(self):
        """Deletes the task item on which it is called."""
        self._workflow.general.delete_tasks(list_of_tasks=[self.name()])

    def __repr__(self):
        try:
            suffix = int(self.name().split()[-1])
        except (TypeError, ValueError):
            suffix = 0
        return f"task < {self._name}: {suffix} >"


def build_specific_interface(task_object):
    """
    Build a dynamic interface type that exposes task-specific
    commands/properties while delegating back to the task_object.
    """

    def make_delegate(attr):
        def delegate(self, *args, **kwargs):
            return getattr(self._task_object, attr)(*args, **kwargs)

        return delegate

    # Determine the API surface of the underlying task:
    public_members = {
        name
        for name in dir(task_object)
        if not name.startswith("_") and callable(getattr(task_object, name))
    }

    namespace = {name: make_delegate(name) for name in public_members}

    iface_name = f"{task_object.task_type}SpecificInterface"

    return type(iface_name, (), namespace)


def make_task_wrapper(task_obj, name, workflow, parent, meshing_root):
    """Wraps TaskObjects."""

    specific_interface = build_specific_interface(task_obj)

    combined_type = type(
        f"{task_obj.task_type}Task", (specific_interface, TaskObject), {}
    )

    return combined_type(task_obj, name, workflow, parent, meshing_root)
