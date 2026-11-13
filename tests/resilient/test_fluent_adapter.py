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

"""The Fluent adapter and the ``resilient_mode`` launch options."""

import inspect
from types import SimpleNamespace

import pytest

from ansys.fluent.core import connect_to_fluent, launch_fluent
from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning
from ansys.fluent.core.execution.session.session import BaseSession
from ansys.fluent.core.resilient import (
    FluentAdapter,
    _enable_on_new_session,
)
from ansys.fluent.core.solver.flobject import ReadOnlyActionError

pytestmark = pytest.mark.resilient


def _session(**attributes):
    connection = SimpleNamespace(
        _remote_instance=None,
        connection_properties=SimpleNamespace(inside_container=False),
        register_finalizer_cb=lambda callback: None,
    )
    defaults = dict(
        _fluent_connection=connection,
        _file_transfer_service=None,
        _error_state=SimpleNamespace(name="", details=""),
    )
    defaults.update(attributes)
    return SimpleNamespace(**defaults)


def test_error_classes_are_fluent_settings_errors():
    classes = FluentAdapter().error_classes()
    assert classes.read_only is ReadOnlyActionError


@pytest.mark.parametrize(
    "path, irreversible",
    [
        ("solution/run-calculation/iterate", True),
        ("solution/run-calculation/dual-time-iterate", True),
        ("file/read-case-data", True),
        ("file/write-case-data", False),
        ("solution/initialization/hybrid-initialize", False),
    ],
)
def test_server_command_names_are_normalized(path, irreversible):
    assert FluentAdapter().is_irreversible(path) is irreversible


def test_output_commands_are_not_replayed():
    adapter = FluentAdapter()
    assert not adapter.is_replayable("file/write-case")
    assert not adapter.is_replayable("solution/run-calculation/interrupt")
    assert adapter.is_replayable("solution/initialization/hybrid-initialize")


def test_fatal_state_and_health():
    adapter = FluentAdapter()
    session = _session()
    assert not adapter.is_fatal(session)
    session._error_state.name, session._error_state.details = "fatal", "crashed"
    assert adapter.is_fatal(session) and adapter.fatal_details(session) == "crashed"
    # A transport without a health service is never reported as dead.
    assert adapter.is_server_healthy(_session())
    assert not adapter.is_server_healthy(
        _session(_health_check=SimpleNamespace(is_serving=False))
    )


@pytest.mark.parametrize(
    "change, shared",
    [
        ({}, True),
        ({"_file_transfer_service": object()}, False),
        ({"_fluent_connection": None}, False),
    ],
)
def test_shared_file_system_detection(change, shared):
    assert FluentAdapter().shares_client_filesystem(_session(**change)) is shared


def test_remote_and_container_servers_do_not_share_the_file_system():
    adapter = FluentAdapter()
    remote = _session()
    remote._fluent_connection._remote_instance = object()
    assert not adapter.shares_client_filesystem(remote)
    container = _session()
    container._fluent_connection.connection_properties.inside_container = True
    assert not adapter.shares_client_filesystem(container)


def test_standby_launcher_repeats_a_local_launch():
    args = {
        "mode": "solver",
        "dimension": 2,
        "processor_count": 4,
        "dry_run": False,
        "fluent_debug": True,
    }
    launcher = FluentAdapter().standby_launcher(_session(_launcher_args=args))
    assert launcher.func is launch_fluent
    assert launcher.keywords == {"mode": "solver", "dimension": 2, "processor_count": 4}


@pytest.mark.parametrize(
    "ui_mode, forwarded",
    [("no_gui", False), ("no_gui_or_graphics", False), ("gui", True)],
)
def test_graphics_driver_is_forwarded_only_for_graphical_modes(ui_mode, forwarded):
    # The launcher records the driver it resolved and warns if it is passed back
    # for a mode without graphics.
    args = {"mode": "solver", "ui_mode": ui_mode, "graphics_driver": "null"}
    launcher = FluentAdapter().standby_launcher(_session(_launcher_args=args))
    assert ("graphics_driver" in launcher.keywords) is forwarded
    assert launcher.keywords["ui_mode"] == ui_mode


def test_standby_launcher_repeats_a_container_launch():
    args = {"mode": "solver", "container_dict": {"mount_source": "/data"}}
    session = _session(_launcher_args=args)
    session._fluent_connection.connection_properties.inside_container = True
    launcher = FluentAdapter().standby_launcher(session)
    assert launcher.func is launch_fluent
    assert launcher.keywords == {
        "mode": "solver",
        "container_dict": {"mount_source": "/data"},
        "start_container": True,
    }


@pytest.mark.parametrize(
    "attributes",
    [
        {"_launcher_args": None},
        {"_launcher_args": {"mode": "solver"}, "_file_transfer_service": object()},
        {
            "_launcher_args": {"container_dict": {}, "mode": "solver"},
            "_file_transfer_service": object(),
        },
    ],
)
def test_no_standby_launcher_for_unknown_or_remote_launches(attributes):
    assert FluentAdapter().standby_launcher(_session(**attributes)) is None


def test_checkpoint_files_include_the_data_file():
    assert FluentAdapter().checkpoint_artifacts("a/b.cas.h5", include_data=True) == [
        "a/b.cas.h5",
        "a/b.dat.h5",
    ]
    assert FluentAdapter().checkpoint_artifacts("a/b.cas.h5", include_data=False) == [
        "a/b.cas.h5"
    ]


def _file_session(data_valid=True):
    calls = []
    file = SimpleNamespace(
        read_case=lambda file_name: calls.append(("read_case", file_name)),
        read_data=lambda file_name: calls.append(("read_data", file_name)),
    )
    scheme = SimpleNamespace(eval=lambda expression: data_valid)
    return _session(settings=SimpleNamespace(file=file), scheme=scheme), calls


def test_checkpoint_case_and_data_are_read_separately():
    # A combined case and data read skips the data after a floating point
    # exception.
    session, calls = _file_session()
    FluentAdapter().read_checkpoint(session, "a/b.cas.h5", include_data=True)
    assert calls == [("read_case", "a/b.cas.h5"), ("read_data", "a/b.dat.h5")]
    calls.clear()
    FluentAdapter().read_checkpoint(session, "a/b.cas.h5", include_data=False)
    assert calls == [("read_case", "a/b.cas.h5")]


def test_checkpoint_read_fails_when_fluent_does_not_load_the_data():
    session, _ = _file_session(data_valid=False)
    with pytest.raises(RuntimeError, match="did not load the data"):
        FluentAdapter().read_checkpoint(session, "a/b.cas.h5", include_data=True)


def test_resilient_mode_is_ignored_with_a_warning_for_non_solver_sessions():
    meshing = SimpleNamespace()
    with pytest.warns(PyFluentUserWarning, match="solver sessions only"):
        assert _enable_on_new_session(meshing, None, launched=True) is meshing


def test_resilient_mode_is_not_applied_to_non_solver_with_a_settings_service():
    # Meshing sessions also have a settings service; they must not be wrapped.
    meshing = SimpleNamespace(_settings_service=object())
    with pytest.warns(PyFluentUserWarning, match="solver sessions only"):
        assert _enable_on_new_session(meshing, None, launched=True) is meshing
    assert not hasattr(meshing, "resilient")


def test_only_fluent_clean_stop_is_an_interrupt():
    adapter = FluentAdapter()
    assert adapter.is_interrupt(RuntimeError("()"))
    assert not adapter.is_interrupt(RuntimeError("Divergence detected"))
    assert not adapter.is_interrupt(ValueError("()"))


def test_launch_fluent_accepts_resilient_options():
    parameters = inspect.signature(launch_fluent).parameters
    assert parameters["resilient_mode"].default is False
    assert parameters["resilient_config"].default is None


@pytest.mark.parametrize("function", [connect_to_fluent, BaseSession.from_connection])
def test_connecting_does_not_offer_resilient_options(function):
    parameters = inspect.signature(function).parameters
    assert "resilient_mode" not in parameters
    assert "resilient_config" not in parameters


@pytest.mark.parametrize("method", ["from_install", "from_container", "from_pim"])
def test_session_factories_document_resilient_options(method):
    doc = inspect.getdoc(getattr(BaseSession, method))
    assert "resilient_mode : bool" in doc
    assert "resilient_config : ResilientConfig" in doc
