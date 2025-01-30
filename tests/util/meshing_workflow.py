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


def assign_task_arguments(
    workflow, check_state: bool, task_name: str, **kwargs
) -> None:
    task = workflow.TaskObject[task_name]
    task.Arguments = kwargs
    if check_state:
        # the state that we have set must be a subset of the total state
        assert kwargs.items() <= task.Arguments().items()


def check_task_execute_preconditions(task) -> None:
    assert task.State() == "Out-of-date"
    assert not task.Errors() or not len(task.Errors())


def check_task_execute_postconditions(task) -> None:
    assert task.State() == "Up-to-date"
    assert not task.Errors() or not len(task.Errors())


def execute_task_with_pre_and_postcondition_checks(workflow, task_name: str) -> None:
    task = workflow.TaskObject[task_name]
    check_task_execute_preconditions(task)
    # Some tasks are wrongly returning False in meshing workflow itself
    # so we add a temporary caveat below
    result = task.Execute()
    if task_name not in (
        "Add Local Sizing",
        "Add Boundary Layers",
        "Import CAD and Part Management",
    ):
        assert result is True
    check_task_execute_postconditions(task)
