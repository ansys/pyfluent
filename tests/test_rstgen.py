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

import pytest

from ansys.fluent.core.services.object_model import PyMenu, PyNamedObjectContainer
from doc import rstgen


@pytest.mark.parametrize("mode", ["meshing", "solver"])
def test_datamodel_named_object_instance_pages(tmp_path, monkeypatch, mode):
    class Root(PyMenu):
        class Tasks(PyNamedObjectContainer):
            class _Tasks(PyMenu):
                class Name:
                    pass

                class Children(PyNamedObjectContainer):
                    class _Children(PyMenu):
                        class Value:
                            pass

    classes = [
        Root,
        Root.Tasks,
        Root.Tasks._Tasks,
        Root.Tasks._Tasks.Name,
        Root.Tasks._Tasks.Children,
        Root.Tasks._Tasks.Children._Children,
        Root.Tasks._Tasks.Children._Children.Value,
    ]
    for cls in classes:
        cls.__module__ = "ansys.fluent.core.generated.v261.object_model.workflow"
        cls.__qualname__ = cls.__qualname__.split("<locals>.")[1]
    monkeypatch.setattr(rstgen, "_THIS_DIRNAME", str(tmp_path / "doc"))

    rstgen.generate(Root, mode, is_datamodel=True)

    output = tmp_path / "doc" / "source" / "api" / mode / "datamodel" / "workflow"
    container = (output / "Tasks" / "Tasks_contents.rst").read_text()
    instance_dir = output / "Tasks" / "_Tasks"
    instance = (instance_dir / "_Tasks_contents.rst").read_text()
    children = (instance_dir / "Children" / "Children_contents.rst").read_text()
    child_instance = (
        instance_dir / "Children" / "_Children" / "_Children_contents.rst"
    ).read_text()

    ref = f"ref_{mode}_datamodel_workflow_Tasks__Tasks"
    assert f":ref:`Tasks_item <{ref}>`" in container
    assert (
        "organised like a Python dictionary holding objects of type "
        f":ref:`Tasks_item <{ref}>` by name."
    ) in container
    assert "``Tasks['<name>']``" in container
    assert "   _Tasks/_Tasks_contents\n" in container
    assert f".. _{ref}:\n\nTasks_item\n==========\n" in instance
    assert instance.startswith(":html_theme.sidebar_secondary.remove:\n\n")
    assert ":html_theme.sidebar_secondary.remove:" not in container
    assert (
        ".. autoclass:: ansys.fluent.core.generated.v261.object_model."
        "workflow.Root.Tasks._Tasks\n"
    ) in instance
    assert ":ref:`Children_item <" in children
    assert "Children_item\n=============\n" in child_instance
    assert child_instance.startswith(":html_theme.sidebar_secondary.remove:\n\n")


def test_tui_page_unchanged(tmp_path, monkeypatch):
    main_menu = type(
        "main_menu",
        (),
        {"__module__": "ansys.fluent.core.generated.v261.meshing.tui"},
    )
    monkeypatch.setattr(rstgen, "_THIS_DIRNAME", str(tmp_path / "doc"))

    rstgen.generate(main_menu, "meshing", is_datamodel=False)

    page = (
        tmp_path / "doc" / "source" / "api" / "meshing" / "tui" / "tui_contents.rst"
    ).read_text()
    assert page.startswith(".. _ref_meshing_tui:\n\ntui\n===\n")
    assert ":html_theme.sidebar_secondary.remove:" not in page
    assert "_item" not in page
