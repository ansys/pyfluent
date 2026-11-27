# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

from copy import deepcopy
import inspect
import warnings

import pytest

from ansys.fluent.core.diagnostics.exceptions import PyFluentDeprecationWarning
from ansys.fluent.core.services.object_model import PyMenu, PyStateContainer
from ansys.fluent.core.workflow import Workflow, make_task_wrapper
from ansys.fluent.core.workflow_old import ArgumentsWrapper, ArgumentWrapper


class FakeTask:
    def __init__(self, state):
        self.state = state
        self.arguments = FakeArguments()
        self.set_calls = []

    def _name_(self):
        return "Example"

    def get_state(self):
        return self.state

    def getState(self):
        return self.state

    def set_state(self, state=None, **kwargs):
        self.set_calls.append((state, kwargs))
        return "set"

    def setState(self, state=None, **kwargs):
        return self.set_state(state, **kwargs)

    def execute(self):
        return "executed"


class FakeArguments:
    def __call__(self):
        return {"length_unit": "mm", "controls": {}, "state": "argument"}


def test_task_argument_assignment_warns_at_caller(mocker):
    task_object = FakeTask({})
    arguments = PyMenu(mocker.Mock(), "test")
    child = PyStateContainer(mocker.Mock(), "test")
    object.__setattr__(arguments, "length_unit", child)
    task_object.arguments = arguments
    task = make_task_wrapper(task_object, "example", None, None, None)
    set_state = mocker.patch.object(PyStateContainer, "set_state", autospec=True)

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", PyFluentDeprecationWarning)
        line = inspect.currentframe().f_lineno + 1
        task.length_unit = "in"
    assert len(captured) == 1
    assert captured[0].filename == __file__
    assert captured[0].lineno == line
    set_state.assert_called_once_with(child, "in")


def test_legacy_argument_assignment_warns_but_index_assignment_does_not(mocker):
    task = mocker.Mock()
    wrapper = ArgumentsWrapper(task)

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", PyFluentDeprecationWarning)
        wrapper.length_unit = "in"
        wrapper["length_unit"] = "mm"
    assert len(captured) == 1
    assert captured[0].category is PyFluentDeprecationWarning
    assert task.length_unit.set_state.call_args_list == [
        mocker.call("in"),
        mocker.call("mm"),
    ]

    argument = object.__new__(ArgumentWrapper)
    argument.__dict__.update(_task=task, _arg_name="controls")
    with pytest.warns(PyFluentDeprecationWarning, match="set_state.*size"):
        argument.size = 3
    task.arguments.update_dict.assert_called_once_with({"controls": {"size": 3}})


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (
            {
                "arguments": {"length_unit": "mm", "controls": {"size": 1}},
                "state": "ready",
            },
            {"length_unit": "mm", "controls": {"size": 1}, "state": "ready"},
        ),
        ({"arguments": {}, "state": "ready"}, {"state": "ready"}),
        ({"arguments": {"state": "argument"}, "state": "task"}, {"state": "argument"}),
        ({"state": "ready"}, {"state": "ready"}),
        (None, None),
        ("ready", "ready"),
    ],
)
def test_task_get_state(state, expected):
    original_state = deepcopy(state)
    task_object = FakeTask(state)
    task = make_task_wrapper(task_object, "example", None, None, None)

    assert task.get_state() == expected
    assert task_object.get_state() is state
    assert state == original_state
    assert task.getState() is state
    assert task() == "executed"


@pytest.mark.parametrize(
    ("state", "kwargs", "expected_state", "expected_kwargs"),
    [
        (
            {"length_unit": "in", "check_point": "default-off"},
            {},
            {"arguments": {"length_unit": "in"}, "check_point": "default-off"},
            {},
        ),
        (
            {"arguments": {"controls": {"size": 1}}, "length_unit": "in"},
            {},
            {"arguments": {"controls": {"size": 1}, "length_unit": "in"}},
            {},
        ),
        (
            {"arguments": {"length_unit": "mm"}, "length_unit": "in"},
            {},
            {"arguments": {"length_unit": "in"}},
            {},
        ),
        ({"state": "argument"}, {}, {"arguments": {"state": "argument"}}, {}),
        ({"check_point": "default-off"}, {}, {"check_point": "default-off"}, {}),
        (
            {"arguments": {"length_unit": "in"}},
            {},
            {"arguments": {"length_unit": "in"}},
            {},
        ),
        (None, {}, None, {}),
        ("invalid", {}, "invalid", {}),
        (
            {"length_unit": "ignored"},
            {"length_unit": "in", "check_point": "default-off"},
            {"length_unit": "ignored"},
            {"arguments": {"length_unit": "in"}, "check_point": "default-off"},
        ),
    ],
)
def test_task_set_state(state, kwargs, expected_state, expected_kwargs):
    task_object = FakeTask({})
    task = make_task_wrapper(task_object, "example", None, None, None)
    original_state, original_kwargs = deepcopy((state, kwargs))

    assert task.set_state(state, **kwargs) == "set"
    assert task_object.set_calls == [(expected_state, expected_kwargs)]
    assert (state, kwargs) == (original_state, original_kwargs)


def test_task_set_state_alias_remains_delegated():
    task_object = FakeTask({})
    task = make_task_wrapper(task_object, "example", None, None, None)

    task.setState({"length_unit": "in"})
    assert task_object.set_calls == [({"length_unit": "in"}, {})]


def test_task_set_state_rejects_non_dictionary_nested_arguments():
    task_object = FakeTask({})
    task = make_task_wrapper(task_object, "example", None, None, None)

    with pytest.raises(TypeError, match="Task arguments must be a dictionary"):
        task.set_state({"arguments": None, "length_unit": "in"})
    assert task_object.set_calls == []


def test_workflow_dir_tracks_accessible_task_names():
    class WorkflowTasks:
        def __init__(self):
            self.import_geometry = {
                "Import Geometry": FakeTask({}),
                "Import Geometry 2": FakeTask({}),
            }
            for name, task in self.import_geometry.items():
                task.name = lambda name=name: name
                task.task_type = lambda: "Simple"
            child = FakeTask({})
            child.name = lambda: "Boundary Layer 1"
            child._name_ = child.name
            child.task_type = lambda: "Compound Child"
            self.add_boundary_layers = {"Boundary Layer 1": child}

        def __call__(self):
            return [
                f"{task_type}:{name}"
                for task_type in ("import_geometry", "add_boundary_layers")
                for name in getattr(self, task_type)
            ]

    class WorkflowRoot:
        task_object = WorkflowTasks()

    workflow = Workflow(WorkflowRoot(), None, None)

    assert {
        "tasks",
        "task_names",
        "import_geometry",
        "import_geometry_2",
        "add_boundary_layers_child_1",
    } <= set(dir(workflow))
    assert (
        workflow.import_geometry._task_object
        is WorkflowRoot.task_object.import_geometry["Import Geometry"]
    )
    assert (
        workflow.import_geometry_2._task_object
        is WorkflowRoot.task_object.import_geometry["Import Geometry 2"]
    )
    assert workflow.add_boundary_layers_child_1._task_object is (
        WorkflowRoot.task_object.add_boundary_layers["Boundary Layer 1"]
    )

    del WorkflowRoot.task_object.import_geometry["Import Geometry 2"]
    assert "import_geometry_2" not in dir(workflow)
    added_task = FakeTask({})
    added_task.name = lambda: "Import Geometry 3"
    added_task.task_type = lambda: "Simple"
    WorkflowRoot.task_object.import_geometry["Import Geometry 3"] = added_task
    assert "import_geometry_3" in dir(workflow)
    assert workflow.import_geometry_3._task_object is added_task


def test_task_dir_tracks_arguments_and_preserves_task_members():
    class Arguments:
        def __init__(self):
            self.values = {"length_unit": "mm"}
            self.length_unit = object()

        def __call__(self):
            return self.values

    task_object = FakeTask({})
    task_object.arguments = Arguments()
    task = make_task_wrapper(task_object, "example", None, None, None)

    assert {"length_unit", "get_state", "execute", "state"} <= set(dir(task))
    assert task.length_unit is task_object.arguments.length_unit
    task_object.arguments.values["file_name"] = ""
    task_object.arguments.file_name = object()
    assert "file_name" in dir(task)
    assert task.file_name is task_object.arguments.file_name
    del task_object.arguments.values["length_unit"]
    assert "length_unit" not in dir(task)


def test_workflow_discovery_does_not_call_public_tasks():
    class WorkflowTasks:
        example = {"Example": FakeTask({})}

        def __call__(self):
            return ["example:Example"]

    class WorkflowRoot:
        task_object = WorkflowTasks()

    class CustomWorkflow(Workflow):
        def tasks(self):
            raise AssertionError("Public tasks() must not be used for discovery.")

    WorkflowRoot.task_object.example["Example"].task_type = lambda: "Simple"
    workflow = CustomWorkflow(WorkflowRoot(), None, None)

    assert "example" in dir(workflow)
    assert workflow.example._task_object is WorkflowRoot.task_object.example["Example"]
    assert list(Workflow.tasks(workflow)) == [
        WorkflowRoot.task_object.example["Example"]
    ]


def test_workflow_dir_preserves_static_members_when_refresh_fails(mocker, caplog):
    root = mocker.Mock()
    root.task_object.side_effect = RuntimeError("Server unavailable")
    workflow = Workflow(root, None, None)

    with caplog.at_level("DEBUG", logger="pyfluent.datamodel"):
        members = dir(workflow)

    assert {"tasks", "task_names", "save_workflow"} <= set(members)
    assert "Server unavailable" in caplog.text
    with pytest.raises(RuntimeError, match="Server unavailable"):
        workflow.tasks()


def test_task_dir_preserves_static_members_when_arguments_fail(mocker, caplog):
    task_object = FakeTask({})
    task = make_task_wrapper(task_object, "example", None, None, None)
    task_object.arguments = mocker.Mock(
        side_effect=RuntimeError("Arguments unavailable")
    )

    with caplog.at_level("DEBUG", logger="pyfluent.datamodel"):
        members = dir(task)

    assert {"get_state", "set_state", "execute", "state"} <= set(members)
    assert "length_unit" not in members
    assert "Arguments unavailable" in caplog.text
