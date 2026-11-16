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

import pytest

from ansys.fluent.core.workflow import make_task_wrapper


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
