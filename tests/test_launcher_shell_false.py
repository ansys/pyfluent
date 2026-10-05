# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.execution.launcher import standalone_launcher
from ansys.fluent.core.execution.launcher.standalone_launcher import StandaloneLauncher

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows subprocess semantics")


@pytest.mark.parametrize(
    "launch_args, expected_arguments",
    [
        ({}, []),
        (
            {"journal_file_names": [r"input & output\first journal.jou", "second.jou"]},
            ["-i", r"input & output\first journal.jou", "-i", "second.jou"],
        ),
        (
            {"case_file_name": r"case files\model (1).cas.h5"},
            ["-case", r"case files\model (1).cas.h5"],
        ),
        (
            {"case_file_name": "model.cas.h5", "case_data_file_name": "model.dat.h5"},
            ["-case", "model.cas.h5", "-data", "model.dat.h5"],
        ),
        (
            {"journal_file_names": r"%PYFLUENT_TEST_DIR%\input.jou"},
            ["-i", r"%PYFLUENT_TEST_DIR%\input.jou"],
        ),
        (
            {"journal_file_names": r"\\server\share\input & output\input.jou"},
            ["-i", r"\\server\share\input & output\input.jou"],
        ),
        (
            {
                "journal_file_names": r"C:\input files\input.jou",
                "topy": "output journal.py",
            },
            ["-i", r"C:\input files\input.jou", "-topy=output journal.py"],
        ),
        (
            {"additional_arguments": '-t2 -cnf="hosts file.txt"'},
            ["-t2", "-cnf=hosts file.txt"],
        ),
        (
            {"additional_arguments": '> "output.txt" & echo shell-marker | more'},
            [">", "output.txt", "&", "echo", "shell-marker", "|", "more"],
        ),
        (
            {"journal_file_names": "input ^ & (1) %USERNAME% !TOKEN!.jou"},
            ["-i", "input ^ & (1) %USERNAME% !TOKEN!.jou"],
        ),
    ],
    ids=[
        "defaults",
        "journals",
        "case",
        "case-data",
        "literal-env-token",
        "unc-journal",
        "journal-conversion",
        "parallel-options",
        "shell-operators",
        "literal-metacharacters",
    ],
)
def test_unc_launch_passes_command_and_environment(
    monkeypatch, tmp_path, launch_args, expected_arguments
):
    server_info = tmp_path / "server info.txt"
    server_info.touch()
    monkeypatch.setattr(
        standalone_launcher,
        "_get_server_info_file_names",
        lambda: (str(server_info), str(server_info)),
    )
    monkeypatch.setenv("PYFLUENT_SHELL_INHERITED", "inherited value")
    monkeypatch.setenv("PYFLUENT_TEST_DIR", str(tmp_path))
    monkeypatch.setattr(pyfluent.config, "fluent_debug", False)
    executable = '"C:\\Program Files\\ANSYS Inc\\fluent.exe"'
    launcher = StandaloneLauncher(
        fluent_path=r"C:\Program Files\ANSYS Inc\fluent.exe",
        cwd=r"\\server\share\work & results",
        env={"PYFLUENT_SHELL_OVERRIDE": "value & (literal) %USERNAME%"},
        ui_mode="no_gui",
        py=False,
        start_watchdog=False,
        **launch_args,
    )
    process = Mock(pid=12345)
    popen = Mock(return_value=process)
    original_popen = standalone_launcher.subprocess.Popen
    monkeypatch.setattr(standalone_launcher.subprocess, "Popen", popen)
    monkeypatch.setattr(standalone_launcher, "_await_fluent_launch", Mock())
    monkeypatch.setattr(launcher, "new_session", Mock())
    monkeypatch.setattr(launcher, "_disable_idle_timeout_guard", Mock())

    session = launcher()

    popen.assert_called_once_with(launcher._launch_cmd, **launcher._kwargs)
    assert session._process is process
    assert launcher._launch_cmd.startswith(executable + " ")
    assert f'-sifile="{server_info}"' in launcher._launch_cmd
    assert '-command="(set-session-idle-timeoutPLF+3)"' in launcher._launch_cmd
    assert launcher._kwargs["shell"] is False
    assert launcher._kwargs["cwd"] == r"\\server\share\work & results"
    assert launcher._kwargs["env"]["PYFLUENT_SHELL_INHERITED"] == "inherited value"
    assert (
        launcher._kwargs["env"]["PYFLUENT_SHELL_OVERRIDE"]
        == "value & (literal) %USERNAME%"
    )
    assert launcher._kwargs["creationflags"] & subprocess.CREATE_NEW_PROCESS_GROUP
    assert launcher._kwargs["creationflags"] & subprocess.CREATE_NO_WINDOW

    monkeypatch.setattr(standalone_launcher.subprocess, "Popen", original_popen)
    probe = (
        "import json, os, sys; print(json.dumps([sys.argv[1:], "
        "os.getenv('PYFLUENT_SHELL_INHERITED'), "
        "os.getenv('PYFLUENT_SHELL_OVERRIDE'), os.getcwd()]))"
    )
    command = subprocess.list2cmdline([sys.executable, "-c", probe])
    command += launcher._launch_cmd[len(executable) :]
    kwargs = dict(launcher._kwargs, cwd=tmp_path)
    kwargs.pop("stdout", None)
    kwargs.pop("stderr", None)
    result = subprocess.run(
        command, **kwargs, capture_output=True, text=True, check=True, timeout=30
    )
    arguments, inherited, override, cwd = json.loads(result.stdout)
    assert arguments[0] == "3ddp"
    assert f"-sifile={server_info}" in arguments
    assert "-command=(set-session-idle-timeoutPLF+3)" in arguments
    if expected_arguments:
        start = arguments.index(expected_arguments[0])
        assert arguments[start : start + len(expected_arguments)] == expected_arguments
    assert inherited == "inherited value"
    assert override == "value & (literal) %USERNAME%"
    assert Path(cwd) == tmp_path
    assert not (tmp_path / "output.txt").exists()


@pytest.mark.parametrize("shell", [False, True])
@pytest.mark.parametrize("quoted", [False, True])
def test_windows_environment_expansion_requires_shell(
    monkeypatch, tmp_path, shell, quoted
):
    monkeypatch.setenv("PYFLUENT_SHELL_TOKEN", "expanded value")
    probe = (
        "import json, os, sys; print(json.dumps([sys.argv[1:], "
        "os.getenv('PYFLUENT_SHELL_TOKEN'), os.getcwd()]))"
    )
    command = subprocess.list2cmdline([sys.executable, "-c", probe])
    token = '"%PYFLUENT_SHELL_TOKEN%"' if quoted else "%PYFLUENT_SHELL_TOKEN%"
    command += f' {token} "a & b (c) ^ d"'
    result = subprocess.run(
        command,
        shell=shell,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    arguments, environment_value, cwd = json.loads(result.stdout)
    expected = ["expanded value"] if quoted else ["expanded", "value"]
    if not shell:
        expected = ["%PYFLUENT_SHELL_TOKEN%"]
    assert arguments == expected + ["a & b (c) ^ d"]
    assert environment_value == "expanded value"
    assert Path(cwd) == tmp_path
