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

import os

import pytest

from ansys.fluent.core import FluentVersion
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.services.datamodel_tui import TUIMenu


@pytest.mark.skip("Failing in github")
def test_report_system_proc_stats_tui(new_solver_session, capsys) -> None:
    new_solver_session.tui.report.system.sys_stats()
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_runtime_tui_menus(static_mixer_case_session) -> None:
    solver = static_mixer_case_session
    solver.tui.define.models.addon_module(3)
    rmf = solver.tui.define.models.resolved_MEA_fuelcells
    assert rmf is not None
    assert rmf.__class__ == TUIMenu


@pytest.mark.codegen_required
def test_python_keyword_menu_name(new_meshing_session):
    meshing = new_meshing_session
    assert "cad_options" in dir(meshing.tui.file.import_)
    assert "create_cad_assemblies" in dir(meshing.tui.file.import_.cad_options)
    meshing.tui.file.import_.cad_options.create_cad_assemblies("yes")


@pytest.mark.skip("Failing in github")
def test_api_upgrade_message(new_solver_session):
    solver = new_solver_session
    case_name = download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer", save_path=os.getcwd()
    )
    from contextlib import redirect_stdout
    import io

    f = io.StringIO()
    with redirect_stdout(f):
        solver.tui.file.read_case(case_name)
    s = f.getvalue()
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert (
            s.split("\n")[-2].split("(")[0]
            == r"<solver_session>.settings.file.read_case"
        )
    else:
        assert s.split("\n")[-2].split("(")[0] == r"<solver_session>.file.read_case"


def test_exit_not_in_meshing_tui(new_meshing_session):
    meshing = new_meshing_session

    assert "exit" not in dir(meshing.tui)

    with pytest.raises(AttributeError):
        meshing.tui.exit()


def test_commands_not_in_solver_tui(new_solver_session):
    solver = new_solver_session

    deleted_commands = ["exit"]
    hidden_commands = ["switch_to_meshing_mode"]

    for command in deleted_commands:
        assert command not in dir(solver.tui)
        with pytest.raises(AttributeError):
            getattr(solver.tui, command)

    for command in hidden_commands:
        assert command not in dir(solver.tui)
        assert getattr(solver.tui, command)
