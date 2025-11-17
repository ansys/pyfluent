# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Workflow module that wraps and extends the core functionality."""

from __future__ import annotations

import re

from ansys.fluent.core.services.datamodel_se import PyMenu
from ansys.fluent.core.utils.fluent_version import FluentVersion


def _convert_task_list_to_display_names(workflow_root, task_list):
    _display_names = []
    for _task_name in task_list:
        name_obj = PyMenu(
            service=workflow_root.service,
            rules=workflow_root.rules,
            path=[("task_object", _task_name), ("_name_", "")],
        )
        _display_names.append(name_obj.get_remote_state())
    return _display_names


def camel_to_snake_case(camel_case_str: str) -> str:
    """Convert camel case input string to snake case output string."""
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
    return _snake_case_str


camel_to_snake_case.cache = {}


class Workflow:
    """Wraps a workflow object, adding methods to discover more about the relationships
    between task objects."""

    def __init__(
        self,
        workflow: PyMenu,
        command_source: PyMenu,
        fluent_version: FluentVersion,
    ) -> None:
        """Initialize WorkflowWrapper.

        Parameters
        ----------
        workflow : PyMenu
            The workflow object.
        command_source : PyMenu
            The application root for commanding.
        """
        self._workflow = workflow
        self._command_source = command_source
        self._fluent_version = fluent_version
        self._task_dict = {}
        self._compound_child_dict = {}

    def tasks(self) -> list:
        """Get the ordered task list held by the workflow."""
        self._task_dict = {}
        _state = self._workflow.task_object()
        for task in sorted(_state):
            name = task.split(":")[0]
            display_name = task.split(":")[-1]
            task_obj = getattr(self._workflow.task_object, name)[display_name]
            if task_obj.task_type() == "Compound Child":
                if name not in self._compound_child_dict:
                    self._compound_child_dict[name] = {
                        name + "_child_1": task_obj,
                    }
                else:
                    _name_list = []
                    for key, value in self._compound_child_dict[name].items():
                        _name_list.append(value._name_())
                    if task_obj._name_() not in _name_list:
                        child_key = (
                            int(sorted(self._compound_child_dict[name])[-1][-1]) + 1
                        )
                        self._compound_child_dict[name][
                            name + f"_child_{child_key}"
                        ] = task_obj
            else:
                if name not in self._task_dict:
                    self._task_dict[name] = task_obj
                else:
                    self._task_dict[name + f"_{task_obj.name().split()[-1]}"] = task_obj

        for key, value in self._compound_child_dict.items():
            for task_name, task_obj in value.items():
                self._task_dict[task_name] = task_obj

        return list(self._task_dict.values())

    def _workflow_state(self):
        return self._workflow()

    def _new_workflow(self, name: str):
        self._workflow.general.initialize_workflow(workflow_type=name)

    def _load_workflow(self, file_path: str):
        self._workflow.general.load_workflow(file_path=file_path)

    def _create_workflow(self):
        self._workflow.general.create_new_workflow()

    def save_workflow(self, file_path: str):
        """Save the current workflow to the location provided."""
        self._workflow.general.save_workflow(file_path=file_path)

    def load_state(self, list_of_roots: list):
        """Load the state of the workflow."""
        self._workflow.general.load_state(list_of_roots=list_of_roots)

    def task_names(self):
        """Get the list of the Python names for the available tasks."""
        names = []
        for name in self._workflow.task_object():
            names.append(name.split(":")[0])
        return names

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
        TypeError
            If 'task' does not match a task name, no tasks are deleted.
        """
        items_to_be_deleted = []
        for item in list_of_tasks:
            if not isinstance(item, TaskObject):
                if isinstance(item, str):
                    items_to_be_deleted.append(item)
                else:
                    raise TypeError(
                        "'list_of_tasks' only takes list of 'TaskObject' types."
                    )
            else:
                items_to_be_deleted.append(item.name())

        self._workflow.general.delete_tasks(list_of_tasks=items_to_be_deleted)

    def __getattr__(self, item):
        if item not in self._task_dict:
            self.tasks()
        if item in self._task_dict:
            return TaskObject(self._task_dict[item], item, self._workflow)
        return getattr(self._workflow, item)

    def __call__(self):
        return self._workflow_state()

    def __delattr__(self, item):
        if item not in self._task_dict:
            self.tasks()
        if item in self._task_dict:
            getattr(self, item).delete()
            del self._task_dict[item]
        else:
            raise LookupError(f"'{item}' is not a valid task name.'")


class TaskObject:
    """TaskObject"""

    def __init__(self, task_object, base_name, workflow):
        """__init__ method of TaskObject class."""
        super().__setattr__("_task_object", task_object)
        super().__setattr__("_name", base_name)
        super().__setattr__("_workflow", workflow)
        self._cache = {}

    def get_next_possible_tasks(self):
        """."""
        task_obj = super().__getattribute__("_task_object")
        ret_list = []
        for item in task_obj.get_next_possible_tasks():
            snake_case_name = camel_to_snake_case(item)
            if snake_case_name != item:
                self._cache[snake_case_name] = item
            ret_list.append(snake_case_name)
        return ret_list

    def insert_next_task(self, task_name):
        """."""
        task_obj = super().__getattribute__("_task_object")
        # This is just a precaution in case this method is directly called from the task level.
        self.get_next_possible_tasks()
        command_name = self._cache.get(task_name) or task_name
        task_obj.insert_next_task(command_name=command_name)

    @property
    def insertable_tasks(self):
        """Tasks that can be inserted after the current task."""
        return self._NextTask(self)

    class _NextTask:
        def __init__(self, base_task):
            """Initialize an ``_NextTask`` instance."""
            self._base_task = base_task
            self._insertable_tasks = []
            for item in self._base_task.get_next_possible_tasks():
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
                return self._base_task.insert_next_task(task_name=self._name)

            def __repr__(self):
                return f"<Insertable '{self._name}' task>"

    def __getattr__(self, item):
        task_obj = super().__getattribute__("_task_object")
        args = task_obj.arguments
        if item in args():
            return getattr(args, item)
        return getattr(task_obj, item)

    def __setattr__(self, key, value):
        task_obj = super().__getattribute__("_task_object")
        args = task_obj.arguments
        if hasattr(args, key):
            setattr(args, key, value)
        else:
            super().__setattr__(key, value)

    def __call__(self):
        task_obj = super().__getattribute__("_task_object")
        return task_obj.execute()

    def __getitem__(self, key):
        task_obj = super().__getattribute__("_task_object")
        name = super().__getattribute__("_name")
        workflow = super().__getattribute__("_workflow")
        name_1 = name
        name_2 = re.sub(r"\s+\d+$", "", task_obj.name().strip()) + f" {key}"
        try:
            return TaskObject(
                getattr(workflow.task_object, name_1)[name_2], name_1, workflow
            )
        except LookupError:
            try:
                return TaskObject(
                    getattr(workflow.task_object, name_1)[key], name_1, workflow
                )
            except LookupError as ex2:
                raise LookupError(
                    f"Neither '{name_2}' nor '{key}' not found in task object '{name_1}'."
                ) from ex2

    def __delitem__(self, key):
        self[key].delete()

    def task_list(self):
        """."""
        task_obj = super().__getattribute__("_task_object")
        # This is just a precaution in case this method is directly called from the task level.
        task_list = task_obj.task_list()
        if task_list:
            return _convert_task_list_to_display_names(
                super().__getattribute__("_workflow"), task_list
            )
        else:
            return []

    def delete(self):
        """."""
        workflow = super().__getattribute__("_workflow")
        workflow.general.delete_tasks(list_of_tasks=[self.name()])
